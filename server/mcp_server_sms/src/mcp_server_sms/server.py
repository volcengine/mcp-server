"""Named SMS API tools over stdio and stateless Streamable HTTP."""

import argparse
import json
from contextlib import asynccontextmanager
from typing import Annotated, Any, Literal
from urllib.parse import urlsplit

from mcp.server import MCPServer
from mcp.server.mcpserver.context import Context
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from pydantic import Field
from starlette.requests import Request
from starlette.responses import JSONResponse

from . import __version__
from .auth import AuthenticationError, Credentials
from .client import SmsClient
from .models import (
    BatchTask,
    Channel,
    Mobile,
    QualificationApplication,
    SignatureApplication,
    TemplateApplication,
    Text,
)

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


def build_server(client: SmsClient | None = None) -> MCPServer:
    api = client if client is not None else SmsClient()

    @asynccontextmanager
    async def lifespan(server: MCPServer):
        async with api:
            yield

    mcp = MCPServer(
        "Volcengine SMS",
        version=__version__,
        lifespan=lifespan,
        instructions=(
            "国内短信 API 工具。调用凭据来自宿主配置，不在工具参数中传递。"
            "有写入或费用的操作由客户端取得用户授权后调用；工具注解不能代替授权。"
            "接口受理成功不等于短信送达；结果未知的写请求不要自动重试。"
            "服务未开通（RE:0001）时由用户在 https://console.volcengine.com/sms 阅读协议并开通。"
        ),
    )

    async def invoke(ctx: Context, action: str, params: dict) -> dict[str, Any]:
        try:
            credentials = Credentials.from_headers(ctx.headers)
        except AuthenticationError as exc:
            raise ToolError(str(exc)) from None
        result = await api.call(action, params, credentials)
        if result["success"] is False:
            raise ToolError(json.dumps(result, ensure_ascii=False))
        return result

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

    @mcp.tool(annotations=READ, structured_output=True)
    async def recognize_qualification_document(
        ctx: Context,
        business_certificate_type: Literal[1, 4, 6, 7] | None = None,
        certificate: str | None = None,
        id_card_front_image: str | None = None,
        id_card_back_image: str | None = None,
    ) -> dict[str, Any]:
        """OCR 识别短信材料服务中的营业证件或身份证图片。

        营业证件传 business_certificate_type 和 certificate；身份证传正反面引用。
        图片引用由调用方通过现有材料渠道取得。返回原始识别字段供客户核对，不缓存或提交。
        """
        business = business_certificate_type is not None and bool(certificate)
        person = bool(id_card_front_image) and bool(id_card_back_image)
        if not (
            (business and id_card_front_image is None and id_card_back_image is None)
            or (person and business_certificate_type is None and certificate is None)
        ):
            raise ToolError("请选择一种材料，并提供完整的营业证件或身份证正反面参数")
        return await invoke(
            ctx,
            "GetOCRLicenseForAgent",
            {
                "businessCertificateType": business_certificate_type,
                "certificate": certificate,
                "iDCardFrontImage": id_card_front_image,
                "iDCardBackImage": id_card_back_image,
            },
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def check_qualification_enterprise(
        ctx: Context,
        business_certificate_name: Text,
        unified_social_credit_identifier: Text,
        legal_person_name: Text,
    ) -> dict[str, Any]:
        """调用企业信息校验接口，返回上游 status/ticket。票据由调用方保管，不生成跳过校验票据。"""
        return await invoke(
            ctx,
            "ThreeElementEnterpriseCheckForAgent",
            {
                "businessCertificateName": business_certificate_name,
                "unifiedSocialCreditIdentifier": unified_social_credit_identifier,
                "legalPersonName": legal_person_name,
            },
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def check_qualification_person(
        ctx: Context,
        person_name: Text,
        person_id_card: Text,
        person_mobile: Mobile | None = None,
    ) -> dict[str, Any]:
        """调用人员信息校验接口，原样返回上游校验状态和后续申请所需票据。"""
        return await invoke(
            ctx,
            "ThreeElementPersonCheckForAgent",
            {
                "personName": person_name,
                "personIDCard": person_id_card,
                "personMobile": person_mobile,
            },
        )

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

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def apply_qualification(
        ctx: Context, request: QualificationApplication
    ) -> dict[str, Any]:
        """直接提交客户已授权的资质申请，返回上游资质 ID。

        输入为完整申请参数和上游校验票据，不使用 MCP 草稿或 operationId。
        材料要求、票据有效性及审核规则由短信服务校验。结果未知时禁止自动重试。
        """
        return await invoke(ctx, "ApplySignatureIdentificationForAgent", request.payload())

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

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def apply_signature(ctx: Context, request: SignatureApplication) -> dict[str, Any]:
        """直接提交已获用户授权的签名申请；资质、绑定关系与审核由短信服务校验。"""
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
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def apply_template(ctx: Context, request: TemplateApplication) -> dict[str, Any]:
        """直接提交已获用户授权的国内短信模板申请，返回申请结果。"""
        return await invoke(ctx, "ApplySmsTemplateV2", request.payload())

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

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_send_logs(
        ctx: Context,
        sub_account: Text,
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
        channel_type: Channel | None = None,
        signature: str | None = None,
        template_id: str | None = None,
    ) -> dict[str, Any]:
        """按 Unix 秒时间范围查询提交及送达数量，保留上游统计字段，不自动计算成功率。"""
        if end_time <= start_time:
            raise ToolError("end_time 必须大于 start_time")
        return await invoke(
            ctx,
            "ListTotalSendCountStatForAgent",
            {
                "StartTime": start_time,
                "EndTime": end_time,
                "SubAccount": sub_account,
                "ChannelType": channel_type,
                "Signature": signature,
                "TemplateId": template_id,
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
        force_update: bool | None = None,
    ) -> dict[str, Any]:
        """获取普通群发模板的 CSV 表头及示例；支持上游 CSV 文件响应。"""
        return await invoke(
            ctx,
            "TemplateUploadDemo",
            {
                "subAccount": sub_account,
                "templateId": template_id,
                "forceUpdate": force_update,
            },
        )

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def create_batch_task(ctx: Context, request: BatchTask) -> dict[str, Any]:
        """创建普通通知/营销群发任务，不自动启动；使用已上传 CSV 的 file 对象 Key。

        不支持验证码或特殊通知群发。时间窗口、模板、文件和任务状态由短信服务校验。
        """
        return await invoke(ctx, "SetBatchTask", request.payload())

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
        """查询一页普通群发任务。已知 taskId 时使用 get_batch_task 查询。"""
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


def create_http_app(mcp: MCPServer, public_url: str | None = None):
    hosts = ["127.0.0.1:*", "localhost:*", "[::1]:*"]
    origins = ["http://127.0.0.1:*", "http://localhost:*", "http://[::1]:*"]
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
        hosts.append(parsed.netloc)
        origins.append("https://" + parsed.netloc)
    app = mcp.streamable_http_app(
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
    parser = argparse.ArgumentParser(description="Volcengine SMS MCP Server")
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--public-url", help="远程 HTTP 服务的外部 HTTPS origin")
    args = parser.parse_args()
    mcp = build_server()
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        import uvicorn

        uvicorn.run(create_http_app(mcp, args.public_url), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
