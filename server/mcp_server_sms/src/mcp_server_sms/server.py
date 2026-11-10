"""Named SMS API tools over stdio and stateless Streamable HTTP."""

import argparse
import json
import logging
import sys
from contextlib import asynccontextmanager
from time import time
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit

from mcp.server import MCPServer
from mcp.server.mcpserver.context import Context
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, ToolAnnotations
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import __version__
from .auth import AuthenticationError, Credentials
from .batch_checks import (
    BatchTestSend,
    BatchTrafficCheck,
    batch_test_receipt,
    check_batch_traffic,
    validate_batch_test,
)
from .client import _UNCERTAIN_WRITE_ERRORS, SmsClient, failure
from .forms import (
    APP_ONLY_META,
    FORM_META,
    FormToolResult,
    form_extension,
    open_form,
    private_result,
    tool_result,
)
from .models import (
    BatchTask,
    Channel,
    Mobile,
    QualificationApplication,
    SignatureApplication,
    TemplateApplication,
    Text,
)
from .operations import ServiceOperation, TrafficRegistration
from .prefill import (
    BatchFormPrefill,
    QualificationFormPrefill,
    SignatureFormPrefill,
    TrafficFormPrefill,
)
from .protocol import SmsAPIError, SmsMCPServer
from .qualification_checks import check_enterprise, enterprise_ticket
from .queries import ResourceQuery
from .service_onboarding import ServiceConfirmation, ServiceOnboarding
from .signature_checks import SignatureFormConfirmation, check_signature_confirmation
from .traffic_checks import read_back_traffic, validate_traffic_form
from .upload_models import FileUpload, SmsRequestError
from .uploads import FileUploader, recipient_columns

READ = ToolAnnotations(
    readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True
)
WRITE = ToolAnnotations(
    readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=True
)
CANCEL = ToolAnnotations(
    readOnlyHint=False, destructiveHint=True, idempotentHint=False, openWorldHint=True
)
Page = Annotated[int, Field(ge=1)]
PageSize = Annotated[int, Field(ge=1, le=100)]
PositiveInt = Annotated[int, Field(gt=0)]


def build_server(client: SmsClient | None = None, uploader: FileUploader | None = None) -> MCPServer:
    api = client if client is not None else SmsClient()
    uploads = uploader if uploader is not None else FileUploader(api)
    onboarding = ServiceOnboarding()
    logging.getLogger("mcp_server_sms.calls").setLevel(logging.INFO)
    # 上传地址和签名材料不能随宿主的 INFO/DEBUG 设置进入第三方请求日志。
    for logger in ("httpx", "botocore.auth"):
        logging.getLogger(logger).setLevel(logging.WARNING)

    @asynccontextmanager
    async def lifespan(server: MCPServer):
        async with api, uploads:
            yield

    mcp = SmsMCPServer(
        "Volcengine SMS",
        version=__version__,
        lifespan=lifespan,
        extensions=[form_extension()],
        # SDK 默认 INFO 会启用 HTTPX 的完整 GET URL 日志，可能包含短信正文。
        log_level="WARNING",
        instructions=(
            "国内短信 API 工具。调用凭据来自宿主配置，不在工具参数中传递。"
            "有写入或费用的操作由客户端取得用户授权后调用；工具注解不能代替授权。"
            "接口受理成功不等于短信送达；结果未知的写请求不要自动重试。"
            "服务未开通（RE:0001）时先查询账号和协议，客户明确同意后分别签署协议、开通短信商品。"
            "支持表单时用 open_sms_service_onboarding 交由客户核对协议、计费及开通状态。"
            "query_sms_resources 提供按行业的签名、群发目录、运营商报备和引流查询。"
            "创建群发使用稳定 idempotencyKey，创建不自动启动，特殊通知正文按模板 TaskFields 提供。"
            "材料、验证码和个人信息应通过客户端私密渠道传入，不放进普通聊天。"
            "用户要填写资质、签名、引流或群发表单时，宿主 Agent 可把已确认的字段放入 prefill，"
            "未知项留空，不传 request。打开和恢复页面不等于授权提交。"
        ),
    )

    def credentials_for(ctx: Context) -> Credentials:
        try:
            return Credentials.from_headers(ctx.headers)
        except AuthenticationError as exc:
            raise ToolError(str(exc)) from None

    async def invoke_as(credentials: Credentials, action: str, params: dict) -> dict[str, Any]:
        result = await api.call(action, params, credentials)
        if result["success"] is False:
            raise SmsAPIError(result)
        return result

    async def invoke(ctx: Context, action: str, params: dict) -> dict[str, Any]:
        return await invoke_as(credentials_for(ctx), action, params)

    @mcp.tool(annotations=WRITE, structured_output=False, meta=APP_ONLY_META)
    async def upload_sms_file(ctx: Context, request: FileUpload) -> CallToolResult:
        """由表单上传材料或 CSV，单文件不超过 10 MB。只返回私密文件引用，不暴露上传凭据。

        名单按对应模板的真实 CSV 表头校验；不接受文件系统路径或调用方指定的上传地址。
        """
        try:
            credentials = Credentials.from_headers(ctx.headers)
            result = await uploads.upload(request, credentials)
        except AuthenticationError as exc:
            raise ToolError(str(exc)) from None
        except SmsRequestError as exc:
            raise SmsAPIError(exc.result) from None
        return private_result({"success": True, "action": "upload_sms_file", "result": result, "error": None})

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_message_groups(ctx: Context, name: str | None = None) -> dict[str, Any]:
        """查询当前短信账号的消息组。RE:0001 表示服务未开通。"""
        return await invoke(ctx, "ListSubAccountForAgent", {"SubAccountName": name})

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_message_group(ctx: Context, sub_account: Text) -> dict[str, Any]:
        """查询指定消息组详情；不推断空的行业配置意味着无法发送。"""
        return await invoke(ctx, "GetSubAccountDetail", {"subAccount": sub_account})

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_account_information(ctx: Context) -> dict[str, Any]:
        """查询短信账号的服务信息、企业名称和用户类型。"""
        return await invoke(ctx, "ListAllSmsProduct", {})

    @mcp.tool(annotations=READ, structured_output=True)
    async def query_sms_resources(ctx: Context, request: ResourceQuery) -> dict[str, Any]:
        """补充国内短信只读查询；action 与 params 使用对应的明确契约。

        覆盖启用消息组、按行业签名、群发模板目录、链接/号码及关联模板、正文引流检查、
        组合模板报备、三网报备状态和任务级正文预检。每次只查当前页，不推断已查完。
        Approved=false 或报备未完成是业务结果，不等于请求失败；报备成功不等于短信送达。
        """
        return await invoke(ctx, request.action, request.params.payload())

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def manage_sms_service(ctx: Context, request: ServiceOperation) -> dict[str, Any]:
        """分别签署当前国内短信协议或开通国内短信商品，会产生真实业务操作。

        先用 get_account_information 获取当前协议清单与状态，并由客户阅读协议、确认计费。
        ConfirmProtocolDocument 的 fail 必须为空才能另行调用 ActivateSmsProductInOneStep。
        不串联自动开通；返回后重新查状态，orderStatus 或 success/fail 按原值解释。
        """
        return await invoke(ctx, request.action, request.params.payload())

    @mcp.tool(annotations=READ, structured_output=True, meta=FORM_META)
    async def open_sms_service_onboarding() -> FormToolResult:
        """打开国内短信开通与协议更新表单，客户在表单内阅读并确认。"""
        return open_form("service", None, None)

    @mcp.tool(annotations=READ, structured_output=False, meta=APP_ONLY_META)
    async def get_sms_service_onboarding(ctx: Context) -> CallToolResult:
        """读取本账号的国内短信状态、待确认协议和计费说明。"""
        credentials = credentials_for(ctx)
        view = await onboarding.read(
            lambda action, params: invoke_as(credentials, action, params), credentials
        )
        return private_result({"success": True, "action": "get_sms_service_onboarding", "result": view})

    @mcp.tool(annotations=WRITE, structured_output=False, meta=APP_ONLY_META)
    async def submit_sms_service_onboarding(
        ctx: Context, confirmation: ServiceConfirmation
    ) -> CallToolResult:
        """提交客户在当前账号上明确确认的协议更新或开通申请，提交后回查状态。"""
        credentials = credentials_for(ctx)
        view = await onboarding.submit(
            lambda action, params: invoke_as(credentials, action, params), credentials, confirmation
        )
        return private_result({
            "success": True, "action": "submit_sms_service_onboarding",
            "request_id": view.get("requestId"), "result": view,
        })

    @mcp.tool(annotations=WRITE, structured_output=True, meta=FORM_META)
    async def register_traffic_resource(
        ctx: Context,
        request: TrafficRegistration | None = None,
        prefill: TrafficFormPrefill | None = None,
        read_back: bool = False,
    ) -> FormToolResult:
        """按客户已确认的原始信息录入引流链接或联系号码，录入后回查资源。

        链接每次最多 10 条，号码最多 100 条。个人姓名、证件需客户端私密输入。
        保留 URL 路径、参数和号码原文；资源录入、模板审核、报备和实际发送分别确认。
        不传 request 只打开表单。用 prefill.kind 选择 link 或 phone，data 填已知字段。
        prefill 与 request 互斥；完整 request 会直接录入，必须已经获得用户授权。
        表单传 read_back 时重新校验，并在受理后查询精确匹配的资源 ID。
        """
        if read_back and request is None:
            raise ToolError("录入后核对需要完整的引流请求。")
        draft = open_form("traffic", request, prefill)
        if draft is not None:
            return draft
        if read_back:
            validate_traffic_form(request)
        result = await invoke(ctx, request.action, request.params.payload())
        if read_back:
            if result["result"] != "":
                raise SmsAPIError(failure(
                    request.action, "outcome_unknown", "未收到明确的引流录入结果，请查询原资源",
                    result["request_id"], outcome_unknown=True,
                ))
            result = {**result, "result": await read_back_traffic(
                lambda action, params: invoke(ctx, action, params), request
            )}
        return tool_result({**result, "form": "traffic"}, private=False)

    @mcp.tool(annotations=READ, structured_output=True, meta=APP_ONLY_META)
    async def preview_traffic_resource(request: TrafficRegistration) -> dict[str, Any]:
        """校验表单的链接、号码、协议和重复项，只返回可预览的记录数量。"""
        validate_traffic_form(request)
        return {"success": True, "result": {"count": len(request.params.data)}}

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_qualification_requirements(ctx: Context) -> dict[str, Any]:
        """查询当前账号的资质材料及人员校验要求；不创建草稿。"""
        return await invoke(ctx, "GetAccountIdentRankForAgent", {})

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_qualifications(
        ctx: Context,
        qualification_id: PositiveInt | None = None,
        material_name: str | None = None,
        status: list[int] | None = None,
        page: Page = 1,
        page_size: PageSize = 20,
    ) -> dict[str, Any]:
        """按资质 ID、名称或审核状态查询一页资质记录。"""
        return await invoke(
            ctx,
            "GetSignatureIdentificationList",
            {
                "id": qualification_id,
                "materialName": material_name,
                "status": status,
                "pageIndex": page,
                "pageSize": page_size,
            },
        )

    @mcp.tool(annotations=READ, structured_output=False)
    async def recognize_qualification_document(
        ctx: Context,
        business_certificate_type: Literal[1, 4, 6, 7] | None = None,
        certificate: str | None = None,
        id_card_front_image: str | None = None,
        id_card_back_image: str | None = None,
        private: bool = True,
    ) -> CallToolResult:
        """OCR 识别短信材料服务中的营业证件或身份证图片。

        营业证件传 business_certificate_type 和 certificate；身份证传正反面引用。
        图片引用由调用方通过现有材料渠道取得，识别字段供客户核对，不缓存或提交。
        默认 private=True：完整字段仅放入私密元数据 _meta["sms/form"]，
        普通 content 和 structuredContent 只含操作状态，避免姓名、身份证号进入模型上下文。
        仅在客户明确同意识别结果进入模型上下文时设置 private=False；
        此时完整识别字段会出现在 content 和 structuredContent 中。
        """
        business = business_certificate_type is not None and bool(certificate)
        person = bool(id_card_front_image) and bool(id_card_back_image)
        if not (
            (business and id_card_front_image is None and id_card_back_image is None)
            or (person and business_certificate_type is None and certificate is None)
        ):
            raise ToolError("请选择一种材料，并提供完整的营业证件或身份证正反面参数")
        result = await invoke(
            ctx,
            "GetOCRLicenseForAgent",
            {
                "businessCertificateType": business_certificate_type,
                "certificate": certificate,
                "iDCardFrontImage": id_card_front_image,
                "iDCardBackImage": id_card_back_image,
            },
        )
        return tool_result(result, private)

    @mcp.tool(annotations=READ, structured_output=False)
    async def check_qualification_enterprise(
        ctx: Context,
        business_certificate_name: Text,
        unified_social_credit_identifier: Text,
        legal_person_name: Text,
        private: bool = False,
        offer_manual_review: bool = False,
    ) -> CallToolResult:
        """校验企业信息。私密表单可请求人工审核选项，操作由客户单独确认。"""
        if offer_manual_review and not private:
            raise ToolError("人工审核选项仅供私密表单使用。")
        result = await check_enterprise(
            lambda action, params: invoke(ctx, action, params),
            {
                "businessCertificateName": business_certificate_name,
                "unifiedSocialCreditIdentifier": unified_social_credit_identifier,
                "legalPersonName": legal_person_name,
            },
            offer_manual_review=offer_manual_review,
        )
        return tool_result(result, private)

    @mcp.tool(annotations=READ, structured_output=False)
    async def check_qualification_person(
        ctx: Context,
        person_name: Text,
        person_id_card: Text,
        person_mobile: Mobile | None = None,
        private: bool = False,
    ) -> CallToolResult:
        """调用人员信息校验接口，原样返回上游校验状态和后续申请所需票据。"""
        result = await invoke(
            ctx,
            "ThreeElementPersonCheckForAgent",
            {
                "personName": person_name,
                "personIDCard": person_id_card,
                "personMobile": person_mobile,
            },
        )
        return tool_result(result, private)

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def send_verification_code(
        ctx: Context,
        app_id: PositiveInt,
        scene: int,
        mobile: Mobile,
        template_id: PositiveInt,
        code_type: Literal[0, 1],
        channel_id: PositiveInt | None = None,
    ) -> dict[str, Any]:
        """发送一次短信验证消息。应用、场景、模板及通道使用已有业务配置，不由 MCP 猜测。

        code_type：0 为四位数字，1 为六位数字。会实际发送，需客户端取得用户授权。
        """
        return await invoke(
            ctx,
            "SendSmsVerifyCodeByMobile",
            {
                "appId": app_id,
                "scene": scene,
                "mobile": mobile,
                "templateId": template_id,
                "codeType": code_type,
                "channelId": channel_id,
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def verify_code(
        ctx: Context,
        app_id: PositiveInt,
        scene: int,
        mobile: Mobile,
        code: Annotated[str, Field(pattern=r"^[0-9]{4}([0-9]{2})?$")],
        function: int | None = None,
    ) -> dict[str, Any]:
        """校验用户提供的验证码，可能消耗验证次数；func 使用已有应用场景配置。

        原样返回上游 status，HTTP 成功不等于验证码正确。客户端应私密传递验证码。
        """
        return await invoke(
            ctx,
            "CheckSmsVerifyCodeByMobile",
            {
                "appId": app_id,
                "scene": scene,
                "mobile": mobile,
                "code": code,
                "func": function,
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True, meta=FORM_META)
    async def apply_qualification(
        ctx: Context,
        request: QualificationApplication | None = None,
        prefill: QualificationFormPrefill | None = None,
        confirm_manual_review: bool = False,
    ) -> FormToolResult:
        """直接提交客户已授权的资质申请，返回上游资质 ID。

        输入为完整申请参数和上游校验票据，不使用 MCP 草稿或 operationId。
        材料要求、票据有效性及审核规则由短信服务校验。结果未知时禁止自动重试。
        不传 request 只打开表单，可用 prefill 填已确认的企业、用途、人员和材料字段。
        个人信息和附件仅由宿主的私密渠道传入；校验和验证码仍在页面完成。
        客户在表单确认转人工审核时才传 confirm_manual_review，不传企业校验票据。
        prefill 与 request 互斥；完整 request 会直接提交申请，必须已获得用户授权。
        """
        if confirm_manual_review and (request is None or request.business_check_ticket is not None):
            raise ToolError("转人工审核需要完整申请，并由服务端重新核验企业信息。")
        draft = open_form("qualification", request, prefill)
        if draft is not None:
            return draft
        body = request.payload()
        if confirm_manual_review:
            business = request.business_info
            checked = await check_enterprise(
                lambda action, params: invoke(ctx, action, params),
                {
                    "businessCertificateName": business.business_certificate_name,
                    "unifiedSocialCreditIdentifier": business.unified_social_credit_identifier,
                    "legalPersonName": business.legal_person_name,
                },
                offer_manual_review=True,
            )
            body["businessCheckTicket"] = enterprise_ticket(checked)
        result = await invoke(ctx, "ApplySignatureIdentificationForAgent", body)
        return tool_result({**result, "form": "qualification"}, private=False)

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_signatures(
        ctx: Context,
        signature: str | None = None,
        sub_accounts: list[str] | None = None,
        page: Page = 1,
        page_size: PageSize = 20,
    ) -> dict[str, Any]:
        """查询短信签名和审核状态，返回一页原始业务结果。"""
        return await invoke(
            ctx,
            "ListSignatureForAgent",
            {
                "Signature": signature,
                "SubAccounts": sub_accounts,
                "Page": page,
                "PageSize": page_size,
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True, meta=FORM_META)
    async def apply_signature(
        ctx: Context,
        request: SignatureApplication | None = None,
        prefill: SignatureFormPrefill | None = None,
        confirmation: SignatureFormConfirmation | None = None,
    ) -> FormToolResult:
        """不传 request 打开签名表单；完整 request 直接提交已获授权的申请。

        用 prefill 填已知的签名、来源、资质 ID、消息组范围、证明资料和说明；
        prefill 与 request 互斥。私密表单提交时，confirmation 绑定已核对的主体与名称风险。
        """
        if confirmation is not None and request is None:
            raise ToolError("确认签名风险需要完整申请。")
        draft = open_form("signature", request, prefill)
        if draft is not None:
            return draft
        if confirmation is not None:
            await check_signature_confirmation(
                lambda action, params: invoke(ctx, action, params), request, confirmation
            )
        result = await invoke(ctx, "ApplySmsSignatureV2", request.payload())
        return tool_result({**result, "form": "signature"}, private=False)

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_templates(
        ctx: Context,
        template_id: str | None = None,
        signatures: list[str] | None = None,
        sub_accounts: list[str] | None = None,
        page: Page = 1,
        page_size: PageSize = 20,
    ) -> dict[str, Any]:
        """查询一页模板、审核状态和变量，不在 MCP 中进行内容匹配或缓存。"""
        return await invoke(
            ctx,
            "ListSmsTemplateForAgent",
            {
                "TemplateId": template_id,
                "Signatures": signatures,
                "SubAccounts": sub_accounts,
                "Page": page,
                "PageSize": page_size,
            },
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_second_templates(
        ctx: Context,
        template_id: str | None = None,
        second_template_id: str | None = None,
        signatures: str | None = None,
        project: str | None = None,
        sub_accounts: list[str] | None = None,
    ) -> dict[str, Any]:
        """查询模板详情和二级模板，保留接口返回的正文、变量及绑定信息。"""
        return await invoke(
            ctx,
            "ListSecondTemplate",
            {
                "templateId": template_id,
                "secondTemplateId": second_template_id,
                "signatures": signatures,
                "project": project,
                "subAccounts": sub_accounts,
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def apply_template(ctx: Context, request: TemplateApplication) -> dict[str, Any]:
        """直接提交已获用户授权的国内短信模板申请，返回申请结果。"""
        return await invoke(ctx, "ApplySmsTemplateV2ForAgent", request.payload())

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def send_sms(
        ctx: Context,
        sub_account: Text,
        signature: Text,
        template_id: Text,
        mobiles: Annotated[list[Mobile], Field(min_length=1, max_length=200)],
        template_params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """向 1 至 200 个国内号码发送相同模板内容，会实际产生短信及费用。

        客户端先取得用户对号码和内容的授权。签名不含外围括号；变量按模板提供。
        不自动替换签名、匹配模板、去重号码或重试。返回 Message ID 只表示受理。
        """
        return await invoke(
            ctx,
            "SendSmsForAgent",
            {
                "SubAccount": sub_account,
                "Signature": signature,
                "TemplateId": template_id,
                "Mobiles": ",".join(mobiles),
                "TemplateParam": (
                    json.dumps(template_params, ensure_ascii=False, separators=(",", ":"))
                    if template_params is not None
                    else None
                ),
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=False, meta=APP_ONLY_META)
    async def send_batch_test_sms(ctx: Context, request: BatchTestSend) -> CallToolResult:
        """向表单中单独确认的一个号码试发，产生短信及费用，返回回执查询用的 Message ID。"""
        await validate_batch_test(lambda action, params: invoke(ctx, action, params), request)
        requested_at = int(time())
        try:
            envelope = await send_sms(
                ctx, request.sub_account, request.signature, request.template_id, [request.mobile],
                request.template_params or None,
            )
        except SmsAPIError as exc:
            error = exc.result["error"]
            if error["code"] not in _UNCERTAIN_WRITE_ERRORS or error["outcome_unknown"]:
                raise
            raise SmsAPIError({
                **exc.result, "error": {**error, "outcome_unknown": True},
            }) from None
        return private_result({**envelope, "result": batch_test_receipt(envelope, requested_at)})

    @mcp.tool(annotations=READ, structured_output=True, meta=APP_ONLY_META)
    async def check_batch_traffic_resources(ctx: Context, request: BatchTrafficCheck) -> dict[str, Any]:
        """用当前模板逐行渲染 CSV 的实际短信正文，返回引流检查覆盖数量与缺失行号。"""
        result = await check_batch_traffic(lambda action, params: invoke(ctx, action, params), request)
        return {"success": True, "result": result}

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_send_logs(
        ctx: Context,
        sub_account: Text | None = None,
        message_id: str | None = None,
        mobile: Mobile | None = None,
        template_id: str | None = None,
        signature: str | None = None,
        from_time: int | None = None,
        to_time: int | None = None,
        page: Page = 1,
        page_size: PageSize = 20,
    ) -> dict[str, Any]:
        """查询发送日志和回执。请求时间为 Unix 秒；返回 SendTime/ReceiptTime 为毫秒。

        省略消息组查询当前主账户。完整号码和正文不进入返回；保留回执和公开错误码。
        核对某次发送时使用其 Message ID。列表为空不等于发送失败，不据此重发。
        """
        return await invoke(
            ctx,
            "ListSmsSendLogForAgent",
            {
                "SubAccount": sub_account,
                "MessageId": message_id,
                "Mobile": mobile,
                "TemplateId": template_id,
                "Signature": signature,
                "FromTime": from_time,
                "ToTime": to_time,
                "Page": page,
                "PageSize": page_size,
            },
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_send_statistics(
        ctx: Context,
        start_time: PositiveInt,
        end_time: PositiveInt,
        sub_account: str | None = None,
        channel_type: Channel | list[Channel] | None = None,
        signature: str | list[str] | None = None,
        template_id: str | list[str] | None = None,
        project: str | None = None,
        standard_error_codes: list[str] | None = None,
        not_split: bool = False,
        date_group: Literal[0, 1] | None = None,
        sms_account_group: Literal[0, 1] | None = None,
        channel_group: Literal[0, 1] | None = None,
        signature_group: Literal[0, 1] | None = None,
        template_id_group: Literal[0, 1] | None = None,
        standard_error_code_group: Literal[0, 1] | None = None,
    ) -> dict[str, Any]:
        """查询国内短信 V4 聚合统计；支持按日期、消息组、模板和失败码分组。

        时间为 Unix 秒，最多 90 天。省略消息组/项目查询账号全量，NotSplit 选择拆分口径。
        类型、签名、模板可传单个值或数组；服务端 DataPoints 和计数原样返回。
        历史数据的日粒度与近期实时数据分别解释，不把聚合条数当作消息数量。
        """
        if end_time <= start_time:
            raise ToolError("end_time 必须大于 start_time")
        return await invoke(
            ctx,
            "GetTotalSendCountStatV4ForAgent",
            {
                "StartTime": start_time,
                "EndTime": end_time,
                "SmsAccount": sub_account,
                "Project": project,
                "ChannelType": [channel_type] if isinstance(channel_type, str) else channel_type,
                "Signature": [signature] if isinstance(signature, str) else signature,
                "TemplateId": [template_id] if isinstance(template_id, str) else template_id,
                "StandardErrorCode": standard_error_codes,
                "IsDomestic": 1,
                "NotSplit": not_split,
                "DateGroup": date_group,
                "SmsAccountGroup": sms_account_group,
                "ChannelGroup": channel_group,
                "SignatureGroup": signature_group,
                "TemplateIdGroup": template_id_group,
                "StandardErrorCodeGroup": standard_error_code_group,
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def get_batch_upload_url(ctx: Context) -> dict[str, Any]:
        """获取 CSV 的上游上传地址和 file 对象 Key，不在 MCP 中保存文件。

        调用方用返回的短期签名 URL 上传原文件，创建任务时传 file。URL 应私密使用。
        """
        return await invoke(ctx, "GetUploadTosURL", {"suffix": "csv"})

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_batch_csv_template(
        ctx: Context,
        sub_account: Text,
        template_id: Text,
        include_variables: bool = False,
    ) -> dict[str, Any]:
        """获取当前群发模板的原生 CSV 表头与示例，适用于普通及特殊通知模板。

        返回 value 中的实际 CSV 内容。include_variables 返回首列 phone 之外的变量名。
        """
        envelope = await invoke(
            ctx,
            "TemplateUploadDemoForAgent",
            {
                "subAccount": sub_account,
                "templateId": template_id,
            },
        )
        if include_variables:
            try:
                variables = recipient_columns(envelope["result"]["value"])[1:]
            except SmsRequestError as exc:
                raise SmsAPIError(exc.result) from None
            envelope = {**envelope, "result": {**envelope["result"], "variables": variables}}
        return envelope

    @mcp.tool(annotations=WRITE, structured_output=True, meta=FORM_META)
    async def create_batch_task(
        ctx: Context,
        request: BatchTask | None = None,
        prefill: BatchFormPrefill | None = None,
    ) -> FormToolResult:
        """创建国内群发任务，不自动启动；使用已上传 CSV 的 file 对象 Key。

        普通/特殊通知模板均从群发目录选择，类型、示例和 TaskFields 由服务器提供。
        特殊通知需要的任务正文先用 ValidateBatchTaskContentForAgent 检查。
        同一确认的请求保留 idempotencyKey；时间窗口、文件和状态由短信服务校验。
        不传 request 只打开群发表单。prefill 可包含任意已知的消息组、签名、模板、任务名、
        任务正文、发送时间及待上传 CSV。未确定的字段省略，定时时间使用 Unix 秒。
        prefill 与 request 不可同时传入。完整 request 才创建任务，必须已经获得用户授权。
        """
        draft = open_form("batch", request, prefill)
        if draft is not None:
            return draft
        result = await invoke(ctx, "SetBatchTaskForAgent", request.payload())
        return tool_result({**result, "form": "batch"}, private=False)

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_batch_task(ctx: Context, sub_account: Text, task_id: Text) -> dict[str, Any]:
        """查询指定群发任务；任务处理完成不等于全部短信送达。"""
        return await invoke(
            ctx, "GetBatchTaskDetail", {"subAccount": sub_account, "taskId": task_id}
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_batch_tasks(
        ctx: Context,
        sub_account: Text,
        task_name: str | None = None,
        signature: str | None = None,
        template_id: str | None = None,
        page: Page = 1,
        page_size: PageSize = 20,
    ) -> dict[str, Any]:
        """查询一页群发任务。状态 2 可能不在列表中，已知 taskId 时直接查详情。"""
        return await invoke(
            ctx,
            "GetBatchTaskList",
            {
                "subAccount": sub_account,
                "taskName": task_name,
                "signature": signature,
                "templateId": template_id,
                "pageIndex": page,
                "pageSize": page_size,
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def start_batch_task(ctx: Context, sub_account: Text, task_id: Text) -> dict[str, Any]:
        """启动用户明确授权的指定群发任务。会实际发送短信，不能因为任务已创建就自动调用。"""
        return await invoke(ctx, "ConsentBatchTask", {"subAccount": sub_account, "taskId": task_id})

    @mcp.tool(annotations=CANCEL, structured_output=True)
    async def cancel_batch_task(ctx: Context, sub_account: Text, task_id: Text) -> dict[str, Any]:
        """取消指定群发任务，是否仍可取消由短信服务根据最新状态判断。"""
        return await invoke(ctx, "DeleteBatchTask", {"subAccount": sub_account, "taskId": task_id})

    return mcp


def create_http_app(
    mcp: MCPServer, public_url: str | None = None, *, host: str = "127.0.0.1"
):
    if public_url is not None:
        parsed = urlsplit(public_url)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
            or parsed.path not in ("", "/")
        ):
            raise ValueError("public-url 必须是无路径、凭据或查询参数的 HTTPS origin")
    app = mcp.streamable_http_app(host=host, stateless_http=True, json_response=True)

    class CredentialBoundary:
        async def __call__(self, scope, receive, send):
            if scope["type"] == "http":
                try:
                    Credentials.from_headers(Request(scope).headers)
                except AuthenticationError:
                    return await JSONResponse(
                        {"error": "invalid_sms_credentials"},
                        status_code=401,
                        headers={"WWW-Authenticate": "Bearer", "Cache-Control": "no-store"},
                    )(scope, receive, send)

            async def no_cache(message):
                if message["type"] == "http.response.start":
                    message = {
                        **message,
                        "headers": [*message.get("headers", []), (b"cache-control", b"no-store")],
                    }
                await send(message)

            return await app(scope, receive, no_cache)

    return CredentialBoundary()


def main():
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
    parser = argparse.ArgumentParser(description="Volcengine SMS MCP Server")
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--public-url", help="兼容旧版启动命令的外部 HTTPS origin")
    args = parser.parse_args()
    mcp = build_server()
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        import uvicorn

        uvicorn.run(
            create_http_app(mcp, args.public_url, host=args.host), host=args.host, port=args.port
        )


if __name__ == "__main__":
    main()
