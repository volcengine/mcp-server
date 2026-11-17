"""Named SMS API tools over stdio and stateless Streamable HTTP."""

import argparse
import hmac
import json
import logging
import sys
from collections.abc import Sequence
from contextlib import asynccontextmanager
from time import time
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit

import httpx
from mcp.server import MCPServer
from mcp.server.mcpserver.context import Context
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
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
)
from .client import SmsClient, failure
from .forms import (
    APP_ONLY_META,
    FORM_META,
    FormToolResult,
    form_extension,
    open_form,
    private_result,
)
from .models import (
    BatchTask,
    Channel,
    Mobile,
    QualificationApplication,
    SignatureApplication,
    SmsSendRequest,
    TemplateApplication,
    Text,
)
from .operations import TrafficRegistration
from .prefill import (
    BatchFormPrefill,
    QualificationFormPrefill,
    SignatureFormPrefill,
    TemplateFormPrefill,
    TrafficFormPrefill,
)
from .protocol import SmsAPIError, SmsMCPServer
from .qualification_checks import check_enterprise, enterprise_ticket
from .queries import BatchTaskQuery, BatchTaskReference, ResourceQuery
from .send_checks import SendConfirmation, prepare_sms_send
from .service_onboarding import ServiceConfirmation, ServiceOnboarding
from .template_checks import (
    TemplateConfirmation,
    prepare_template_application,
    template_apply_payload,
)
from .traffic_checks import validate_traffic_form
from .upload_models import (
    MaterialUploadConfirmation,
    MaterialUploadMetadata,
    RecipientsUploadConfirmation,
    RecipientsUploadMetadata,
    SmsRequestError,
)
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
            "国内短信工具与表单应用。除单条短信外，业务写入由客户在页面确认后执行。"
            "有写入或费用的操作由客户端取得用户授权后调用；工具注解不能代替授权。"
            "接口受理成功不等于短信送达；结果未知的写请求不要自动重试。"
            "服务未开通（RE:0001）时使用开通页面核对协议与商品状态。"
            "用 open_sms_service_onboarding 交由客户阅读协议、计费说明并确认办理。"
            "query_sms_resources 提供按行业的签名、群发目录、运营商报备和引流查询。"
            "创建群发使用稳定 idempotencyKey；页面一次确认后先创建任务，再启动同一 taskId。"
            "特殊通知正文按模板 TaskFields 提供。"
            "材料、验证码和个人信息应通过客户端私密渠道传入，不放进普通聊天。"
            "用户要办理资质、签名、引流、模板或群发时，调用对应 open_* 工具并用 prefill 填已知字段。"
            "单条短信不打开页面；对话中补齐消息组、签名、模板、收件号码和变量值，"
            "先调用 preview_sms_send 展示掩码号码和渲染正文，用户明确确认该预览后，"
            "再把原请求与 confirmation 交给 send_sms；确认后参数或资源变化须重新预览。"
            "未知项留空，打开和恢复页面不等于授权提交。"
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
    async def prepare_material_upload(ctx: Context, request: MaterialUploadMetadata) -> CallToolResult:
        """为表单申请单文件直传地址，只接收文件元信息，上传凭证仅通过私密结果返回。"""
        try:
            result = await uploads.prepare_material(request, credentials_for(ctx))
        except SmsRequestError as exc:
            raise SmsAPIError(exc.result) from None
        return private_result({
            "success": True, "action": "prepare_material_upload", "result": result, "error": None,
        })

    @mcp.tool(annotations=WRITE, structured_output=False, meta=APP_ONLY_META)
    async def complete_material_upload(
        ctx: Context, request: MaterialUploadConfirmation
    ) -> CallToolResult:
        """核对本次上传会话并确认 ImageX 结果；不会提交资质或签名申请。"""
        try:
            result = await uploads.complete_material(request, credentials_for(ctx))
        except SmsRequestError as exc:
            raise SmsAPIError(exc.result) from None
        return private_result({
            "success": True, "action": "complete_material_upload", "result": result, "error": None,
        })

    @mcp.tool(annotations=WRITE, structured_output=False, meta=APP_ONLY_META)
    async def prepare_recipients_upload(
        ctx: Context, request: RecipientsUploadMetadata
    ) -> CallToolResult:
        """为所选 CSV 申请当前账号的直传地址，不接收名单正文或本地路径。"""
        try:
            result = await uploads.prepare_recipients(request, credentials_for(ctx))
        except SmsRequestError as exc:
            raise SmsAPIError(exc.result) from None
        return private_result({
            "success": True, "action": "prepare_recipients_upload", "result": result, "error": None,
        })

    @mcp.tool(annotations=READ, structured_output=False, meta=APP_ONLY_META)
    async def complete_recipients_upload(
        ctx: Context, request: RecipientsUploadConfirmation,
        columns: Annotated[list[Text], Field(min_length=1)], traffic: BatchTrafficCheck | None = None,
    ) -> CallToolResult:
        """回读名单，按页面已加载的列定义核对格式和数量；正式任务仍由短信接口校验。"""
        try:
            context = request.context
            if traffic is not None and (
                context.sub_account != traffic.sub_account or context.template_id != traffic.template_id
            ):
                raise SmsAPIError(failure(
                    "ValidateRecipients", "uploaded_selection_changed",
                    "消息组或模板与上传名单不一致，请重新上传",
                ))
            async with uploads.validated_recipients(request, credentials_for(ctx), columns) as (data, result):
                if traffic is not None:
                    result["trafficReport"] = await check_batch_traffic(
                        lambda action, params: invoke(ctx, action, params), traffic,
                        data=data, columns=result["columns"],
                    )
        except SmsRequestError as exc:
            raise SmsAPIError(exc.result) from None
        return private_result({
            "success": True, "action": "complete_recipients_upload", "result": result, "error": None,
        })






    @mcp.tool(annotations=READ, structured_output=True, meta=FORM_META)
    async def open_qualification_form(prefill: QualificationFormPrefill | None = None) -> FormToolResult:
        """打开资质申请页面，可预填已知企业、人员和材料；不会提交申请。"""
        return open_form("qualification", prefill)

    @mcp.tool(annotations=READ, structured_output=True, meta=FORM_META)
    async def open_signature_form(prefill: SignatureFormPrefill | None = None) -> FormToolResult:
        """打开签名申请页面，可预填名称、来源、资质和适用范围；不会提交申请。"""
        return open_form("signature", prefill)

    @mcp.tool(annotations=READ, structured_output=True, meta=FORM_META)
    async def open_traffic_form(prefill: TrafficFormPrefill | None = None) -> FormToolResult:
        """打开链接或联系号码的引流报备页面，保留用户已提供的原始信息。"""
        return open_form("traffic", prefill)

    @mcp.tool(annotations=READ, structured_output=True, meta=FORM_META)
    async def open_batch_task_form(
        prefill: BatchFormPrefill | None = None, task: BatchTaskReference | None = None,
    ) -> FormToolResult:
        """打开群发任务页面：prefill 准备新任务，task 查看并管理已知任务；不会创建或发送。"""
        if prefill is not None and task is not None:
            raise ToolError("新建草稿与已有群发任务只能选择一种。")
        return open_form("batch", prefill, task=task)

    @mcp.tool(annotations=READ, structured_output=True, meta=FORM_META)
    async def open_template_form(prefill: TemplateFormPrefill | None = None) -> FormToolResult:
        """打开国内短信模板申请页面，预填正文、用途、变量、签名和适用消息组。"""
        return open_form("template", prefill)

    @mcp.tool(annotations=READ, structured_output=True)
    async def query_batch_tasks(ctx: Context, request: BatchTaskQuery) -> dict[str, Any]:
        """查询群发列表或按 ID 读取详情；列表未出现任务不能代替详情查询。"""
        return await invoke(ctx, request.action, request.params.payload())

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_account_information(ctx: Context) -> dict[str, Any]:
        """查询短信账号的服务信息、企业名称和用户类型。"""
        return await invoke(ctx, "ListAllSmsProduct", {})

    @mcp.tool(annotations=READ, structured_output=True)
    async def query_sms_resources(ctx: Context, request: ResourceQuery) -> dict[str, Any]:
        """补充国内短信只读查询；action 与 params 使用对应的明确契约。

        覆盖签名可绑定资质、启用消息组、按行业签名、群发模板目录、链接/号码及关联模板、
        正文引流检查、组合模板报备、三网报备状态和任务级正文预检。
        GetApplySignatureBind 返回审核通过的资质候选数组，不分页；purpose 为 1 自用、
        2 他用，不传或 0 不限制用途。其他分页接口每次只查当前页，不推断已查完。
        Approved=false 或报备未完成是业务结果，不等于请求失败；报备成功不等于短信送达。
        """
        return await invoke(ctx, request.action, request.params.payload())



    @mcp.tool(annotations=READ, structured_output=True, meta=FORM_META)
    async def open_sms_service_onboarding() -> FormToolResult:
        """打开国内短信开通与协议更新表单，客户在表单内阅读并确认。"""
        return open_form("service")

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

    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
    async def submit_traffic_resources(ctx: Context, request: TrafficRegistration) -> dict[str, Any]:
        """提交页面已确认的引流资料，按短信接口的原生响应报告受理结果。"""
        validate_traffic_form(request)
        result = await invoke(ctx, request.action, request.params.payload())
        if result["result"] != "":
            raise SmsAPIError(failure(
                request.action, "outcome_unknown", "未收到明确的引流录入结果，请查询原资源",
                result["request_id"], outcome_unknown=True,
            ))
        return result

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
        page_size: PageSize = 10,
    ) -> dict[str, Any]:
        """按资质 ID、名称或审核状态查询一页资质记录，默认10条，按需调整。"""
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

    @mcp.tool(annotations=READ, structured_output=False, meta=APP_ONLY_META)
    async def recognize_qualification_document(
        ctx: Context,
        business_certificate_type: Literal[1, 4, 6, 7] | None = None,
        certificate: str | None = None,
        id_card_front_image: str | None = None,
        id_card_back_image: str | None = None,
    ) -> CallToolResult:
        """OCR 识别短信材料服务中的营业证件或身份证图片。

        营业证件传 business_certificate_type 和 certificate；身份证传正反面引用。
        图片引用由调用方通过现有材料渠道取得，识别字段供客户核对，不缓存或提交。
        完整字段仅放入私密元数据 _meta["sms/form"]，
        普通 content 和 structuredContent 只含操作状态，避免姓名、身份证号进入模型上下文。
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
        return private_result(result)

    @mcp.tool(annotations=READ, structured_output=False, meta=APP_ONLY_META)
    async def check_qualification_enterprise(
        ctx: Context,
        business_certificate_name: Text,
        unified_social_credit_identifier: Text,
        legal_person_name: Text,
    ) -> CallToolResult:
        """校验企业信息。私密表单可请求人工审核选项，操作由客户单独确认。"""
        result = await check_enterprise(
            lambda action, params: invoke(ctx, action, params),
            {
                "businessCertificateName": business_certificate_name,
                "unifiedSocialCreditIdentifier": unified_social_credit_identifier,
                "legalPersonName": legal_person_name,
            },
            offer_manual_review=True,
        )
        return private_result(result)

    @mcp.tool(annotations=READ, structured_output=False, meta=APP_ONLY_META)
    async def check_qualification_person(
        ctx: Context,
        person_name: Text,
        person_id_card: Text,
        person_mobile: Mobile | None = None,
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
        return private_result(result)

    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
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

    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
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

    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
    async def submit_qualification(
        ctx: Context, request: QualificationApplication, confirm_manual_review: bool = False,
    ) -> dict[str, Any]:
        """提交客户在资质页面已确认的申请；结果未知时禁止自动重试。"""
        if confirm_manual_review and request.business_check_ticket is not None:
            raise ToolError("转人工审核应由服务端重新核验，不能同时提供企业校验票据。")
        body = request.payload()
        if confirm_manual_review:
            business = request.business_info
            checked = await check_enterprise(
                lambda action, params: invoke(ctx, action, params),
                {"businessCertificateName": business.business_certificate_name,
                 "unifiedSocialCreditIdentifier": business.unified_social_credit_identifier,
                 "legalPersonName": business.legal_person_name},
                offer_manual_review=True,
            )
            body["businessCheckTicket"] = enterprise_ticket(checked)
        return await invoke(ctx, "ApplySignatureIdentificationForAgent", body)



    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
    async def submit_signature(
        ctx: Context, request: SignatureApplication,
    ) -> dict[str, Any]:
        """提交客户在页面确认的签名申请，资质归属及审核状态由短信接口校验。"""
        return await invoke(ctx, "ApplySmsSignatureV2", request.payload())

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

    @mcp.tool(annotations=READ, structured_output=False, meta=APP_ONLY_META)
    async def preview_template(ctx: Context, request: TemplateApplication) -> CallToolResult:
        """核对当前账号、变量绑定与固定引流，返回仅给页面的模板预览；不会申请。"""
        credentials = credentials_for(ctx)
        view = await prepare_template_application(
            lambda action, params: invoke_as(credentials, action, params), request, credentials
        )
        return private_result({"success": True, "action": "preview_template", "result": view})

    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
    async def submit_template(
        ctx: Context, request: TemplateApplication, confirmation: TemplateConfirmation
    ) -> dict[str, Any]:
        """再次前检后提交当前预览的申请；参数、账号或引流变化须重新核对。"""
        credentials = credentials_for(ctx)

        async def call(action, params):
            return await invoke_as(credentials, action, params)

        view = await prepare_template_application(call, request, credentials)
        if not hmac.compare_digest(confirmation, view["confirmation"]):
            raise SmsAPIError(failure(
                "ApplySmsTemplateV2ForAgent", "template_confirmation_changed",
                "模板参数、账号或引流核对结果已变化，请重新核对模板申请",
            ))
        return await call("ApplySmsTemplateV2ForAgent", template_apply_payload(view))

    @mcp.tool(annotations=READ, structured_output=True)
    async def preview_sms_send(ctx: Context, request: SmsSendRequest) -> dict[str, Any]:
        """核对单条短信的当前模板、消息组和变量，返回掩码号码与渲染正文；不会发送。"""
        credentials = credentials_for(ctx)
        view = await prepare_sms_send(
            lambda action, params: invoke_as(credentials, action, params),
            request,
            credentials,
        )
        return {"success": True, "action": "preview_sms_send", "result": view, "error": None}

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def send_sms(
        ctx: Context, request: SmsSendRequest, confirmation: SendConfirmation
    ) -> dict[str, Any]:
        """复核已确认的单条短信预览后发送；产生费用，结果未知时不自动重试。"""
        credentials = credentials_for(ctx)

        async def call(action, params):
            return await invoke_as(credentials, action, params)

        view = await prepare_sms_send(call, request, credentials)
        if not hmac.compare_digest(confirmation, view["confirmation"]):
            raise SmsAPIError(failure(
                "SendSmsForAgent",
                "send_confirmation_changed",
                "短信参数、账号或模板资源已变化，请重新预览并确认",
            ))
        return await call("SendSmsForAgent", {
            "SubAccount": request.sub_account, "Signature": request.signature,
            "TemplateId": request.template_id, "Mobiles": ",".join(request.mobiles),
            "TemplateParam": json.dumps(request.template_params, ensure_ascii=False, separators=(",", ":")),
        })

    @mcp.tool(annotations=WRITE, structured_output=False, meta=APP_ONLY_META)
    async def send_batch_test_sms(ctx: Context, request: BatchTestSend) -> CallToolResult:
        """向表单中单独确认的一个号码试发，产生短信及费用，返回回执查询用的 Message ID。"""
        requested_at = int(time())
        envelope = await invoke(ctx, "SendSmsForAgent", {
            "SubAccount": request.sub_account, "Signature": request.signature,
            "TemplateId": request.template_id, "Mobiles": request.mobile,
            "TemplateParam": json.dumps(request.template_params, ensure_ascii=False, separators=(",", ":")),
        })
        return private_result({**envelope, "result": batch_test_receipt(envelope, requested_at)})

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

    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
    async def create_batch_task(ctx: Context, request: BatchTask) -> dict[str, Any]:
        """创建客户在页面确认的群发任务，不启动发送；同次确认保留稳定幂等键。"""
        return await invoke(ctx, "SetBatchTaskForAgent", request.payload())





    @mcp.tool(annotations=WRITE, structured_output=True, meta=APP_ONLY_META)
    async def start_batch_task(ctx: Context, sub_account: Text, task_id: Text) -> dict[str, Any]:
        """启动用户明确授权的指定群发任务。会实际发送短信，不能因为任务已创建就自动调用。"""
        return await invoke(ctx, "ConsentBatchTask", {"subAccount": sub_account, "taskId": task_id})

    @mcp.tool(annotations=CANCEL, structured_output=True, meta=APP_ONLY_META)
    async def cancel_batch_task(ctx: Context, sub_account: Text, task_id: Text) -> dict[str, Any]:
        """取消指定群发任务，是否仍可取消由短信服务根据最新状态判断。"""
        return await invoke(ctx, "DeleteBatchTask", {"subAccount": sub_account, "taskId": task_id})

    return mcp


def _parse_https_origin(value: str, option: str) -> httpx.URL:
    message = f"{option} 必须是无路径、凭据、查询参数或通配符的 HTTPS origin"
    try:
        parsed = urlsplit(value)
        origin = httpx.URL(parsed.geturl())
    except (ValueError, httpx.InvalidURL):
        raise ValueError(message) from None
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
        or "*" in parsed.netloc
    ):
        raise ValueError(message)
    return origin


def create_http_app(
    mcp: MCPServer,
    public_url: str | None = None,
    *,
    host: str = "127.0.0.1",
    allowed_origins: Sequence[str] = (),
):
    hosts = ["127.0.0.1:*", "localhost:*", "[::1]:*"]
    origins = ["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"]
    if public_url is not None:
        parsed = _parse_https_origin(public_url, "public-url")
        authority = parsed.netloc.decode("ascii")
        hosts.append(authority)
        if parsed.port is None:
            hosts.append(f"{authority}:443")
        origins.append(f"https://{authority}")
    for origin in allowed_origins:
        parsed = _parse_https_origin(origin, "allowed-origin")
        origins.append(f"https://{parsed.netloc.decode('ascii')}")
    app = mcp.streamable_http_app(
        host=host,
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=hosts,
            allowed_origins=origins,
        ),
    )

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
    parser.add_argument("--public-url", help="短信 MCP 服务的外部 HTTPS origin")
    parser.add_argument(
        "--allowed-origin",
        action="append",
        default=[],
        help="额外允许的浏览器 HTTPS origin，可重复指定",
    )
    args = parser.parse_args()
    mcp = build_server()
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        import uvicorn

        uvicorn.run(
            create_http_app(mcp, args.public_url, host=args.host, allowed_origins=args.allowed_origin),
            host=args.host,
            port=args.port,
        )


if __name__ == "__main__":
    main()
