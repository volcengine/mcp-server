"""MCP 2026-07-28 entry point and explicit SMS tool contracts."""

import argparse
import asyncio
import json
from typing import Any, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.context import Context
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, ConfigDict, Field

from . import __version__
from .auth import AuthenticationError
from .config import Settings
from .core.workflows import CliError
from .core.qualification_upload import QualificationUploadError
from .core.qualification import BusinessData, PersonData
from .runtime import Runtime
from .store import StoreError

Channel = Literal["CN_OTP", "CN_NTC", "CN_MKT"]
READ = ToolAnnotations(
    readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=True
)
PREPARE = ToolAnnotations(
    readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=True
)
WRITE = ToolAnnotations(
    readOnlyHint=False, destructiveHint=True, idempotentHint=False, openWorldHint=True
)


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class QualificationDocument(RequestModel):
    target: Literal[
        "business",
        "operator",
        "responsible",
        "legal",
        "powerOfAttorney",
        "otherMaterials",
    ]
    certificate_type: Literal[0, 1, 2, 3, 4, 6, 7, 9] | None = None
    side: Literal["front", "back"] | None = None
    index: int | None = Field(default=None, ge=0, le=4)
    replace: bool = False


class SignatureRequest(RequestModel):
    content: str
    purpose: Literal[1, 2]
    qualification_id: int = Field(gt=0)
    sub_account: list[str] = Field(min_length=1)
    channel_type: list[Channel] = Field(min_length=1)
    source: Literal[1, 2, 3]
    description: str | None = None
    domain: str | None = None
    scene: str | None = None
    project_name: str | None = None
    app_icp: dict | None = None
    trademark: dict | None = None


class TemplateRequest(RequestModel):
    name: str
    content: str
    channel_type: Channel
    signature: list[str] = Field(min_length=1)
    sub_account: list[str] = Field(min_length=1)
    template_param: list[str] = Field(default_factory=list)
    project: str | None = None
    description: str | None = None
    short_url_config: dict | None = None


class SendRequest(RequestModel):
    sub_account: str
    signature: str
    template_id: str
    mobile: list[str] = Field(min_length=1, max_length=200)
    template_params: dict[str, str]
    dedupe_policy: Literal["reject", "keep-first"] = "reject"


class BatchRequest(RequestModel):
    file_id: str
    sub_account: str
    task_name: str
    signature: str
    template_id: str
    scheduled: bool = False
    send_time: str | None = None


class BatchLaunchRequest(RequestModel):
    sub_account: str
    task_id: str
    file_sha256: str
    total_count: int = Field(ge=1)
    valid_count: int = Field(ge=1)
    invalid_count: int = Field(ge=0)
    dup_count: int = Field(ge=0)


def build_server(runtime: Runtime):
    mcp = MCPServer(
        "Volcengine SMS",
        version=__version__,
        instructions=(
            "国内短信：先查询消息组，RE:0001 时引导用户在 https://console.volcengine.com/sms 完成开通。"
            "资质通过独立工具完成：查询要求、创建草稿、上传材料、确认信息、校验、预览及提交。"
            "证件、个人字段、验证码由宿主通过受控文件渠道提供，只向工具传 fileId；不得在聊天中索取原文。"
            "HTTP 文件接口与本地受限目录导入是宿主集成渠道，不要求网页。OCR 结果交客户私密核对后再保存。"
            "先选择已审核资质、签名和模板。申请及发送必须先 prepare，展示当前预览并取得用户确认，"
            "再 execute_sms_operation；operationId 仅绑定预览，不代表用户授权，客户端必须实施确认。"
            "普通群发使用 batch_csv 文件引用，创建任务后单独确认启动。特殊通知群发不在支持范围内。"
            "API 接受、任务完成和短信送达分别判断。outcome_unknown 不得自动重发。"
            "申请提交后查询审核状态，审核通过后才继续后续任务。工具不能代替客户确认或同意服务协议。"
        ),
    )

    async def invoke(ctx, method, *args):
        def run():
            owner, credentials = runtime.caller(ctx)
            result = method(*args, owner, credentials)
            return runtime.safe(result, credentials)

        try:
            result = await asyncio.to_thread(run)
        except (
            CliError,
            StoreError,
            AuthenticationError,
            QualificationUploadError,
            ValueError,
        ) as exc:
            raise ToolError(str(exc)) from None
        if result.get("success") is False:
            raise ToolError(json.dumps(result, ensure_ascii=False))
        return result

    async def query(ctx, command, **options):
        return await invoke(ctx, runtime.query, command, options)

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_message_groups(
        ctx: Context, name: str | None = None
    ) -> dict[str, Any]:
        """查询当前调用者的消息组；只有 RE:0001 表示未开通短信服务。"""
        return await query(ctx, "list-message-groups", name=name)

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_message_group(ctx: Context, sub_account: str) -> dict[str, Any]:
        """查询指定消息组状态及允许发送的短信类型。"""
        return await query(ctx, "message-group-detail", sub_account=sub_account)

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_qualifications(
        ctx: Context,
        qualification_id: int | None = None,
        material_name: str | None = None,
        status: list[int] | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        """查询资质及审核结果，仅返回客户可见的安全字段。"""
        return await query(
            ctx,
            "list-qualifications",
            id=qualification_id,
            material_name=material_name,
            status=status,
            page=page,
            page_size=page_size,
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_signatures(
        ctx: Context,
        signature: str | None = None,
        sub_account: list[str] | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        """查询短信签名和审核状态。"""
        return await query(
            ctx,
            "list-signatures",
            signature=signature,
            sub_account=sub_account,
            page=page,
            page_size=page_size,
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_templates(
        ctx: Context,
        template_id: str | None = None,
        sub_account: list[str] | None = None,
        signature: list[str] | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        """查询模板、变量和审核状态。"""
        return await query(
            ctx,
            "list-templates",
            template_id=template_id,
            sub_account=sub_account,
            signature=signature,
            page=page,
            page_size=page_size,
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_template(
        ctx: Context, template_id: str, signature: str, sub_account: str
    ) -> dict[str, Any]:
        """读取指定签名、消息组下模板的正文和变量，正文不含签名前缀。contentRedacted=true 表示正文已脱敏或截断，不能据此声称获得完整原文。实际发送前仍需 prepare_send 校验资源和生成预览；消息组行业映射为空不构成单条发送的独立门禁。"""
        return await invoke(
            ctx, runtime.template_detail, template_id, signature, sub_account
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def match_template(
        ctx: Context,
        content: str,
        signature: str,
        sub_account: str,
        channel_type: Channel,
    ) -> dict[str, Any]:
        """按完整内容、签名、消息组及短信类型精确匹配已审核模板。"""
        return await query(
            ctx,
            "match-template",
            content=content,
            signature=signature,
            sub_account=sub_account,
            channel_type=channel_type,
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_signature(
        ctx: Context, request: SignatureRequest
    ) -> dict[str, Any]:
        """校验并预览签名申请。展示预览并取得客户确认后才能执行 operationId。"""
        return await invoke(ctx, runtime.prepare, "signature", request.model_dump())

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_template(
        ctx: Context, request: TemplateRequest
    ) -> dict[str, Any]:
        """校验并预览模板申请。展示预览并取得客户确认后才能执行 operationId。"""
        return await invoke(ctx, runtime.prepare, "template", request.model_dump())

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_send(ctx: Context, request: SendRequest) -> dict[str, Any]:
        """重新校验资源与精确变量，生成脱敏发送预览。此步骤不发送短信。"""
        return await invoke(ctx, runtime.prepare, "send", request.model_dump())

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def execute_sms_operation(ctx: Context, operation_id: str) -> dict[str, Any]:
        """执行已预览且用户已明确确认的短信操作，可能产生费用。客户端必须确认相同预览；禁止自动确认、修改字段或重试未知结果。"""
        return await invoke(ctx, runtime.execute, operation_id)

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_sms_operation_result(
        ctx: Context, operation_id: str
    ) -> dict[str, Any]:
        """只读查询执行记录，不会重发。连接中断后优先查询此记录。"""
        return await invoke(ctx, runtime.operation_result, operation_id)

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_send_status(
        ctx: Context,
        sub_account: str,
        message_id: str,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        """通过 Message ID 查询公开发送日志和回执；提交成功不等于送达。"""
        return await query(
            ctx,
            "send-status",
            sub_account=sub_account,
            message_id=message_id,
            page=page,
            page_size=page_size,
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def analyze_delivery(
        ctx: Context,
        start: str,
        end: str,
        sub_account: str | None = None,
        channel_type: Channel | None = None,
        signature: str | None = None,
        template_id: str | None = None,
        mobile: str | None = None,
        bucket: Literal["total", "hour", "day"] = "day",
        include_logs: bool = False,
        dimension: Literal["subAccount", "signature", "template", "time"] = "time",
        page_size: int = 100,
        max_pages: int = 10,
    ) -> dict[str, Any]:
        """按明确时间范围分析提交和送达情况。日志需要显式消息组，输出说明统计口径与截断情况。"""
        return await query(
            ctx,
            "analytics",
            start=start,
            end=end,
            sub_account=sub_account,
            channel_type=channel_type,
            signature=signature,
            template_id=template_id,
            mobile=mobile,
            bucket=bucket,
            include_logs=include_logs,
            dimension=dimension,
            page_size=page_size,
            max_pages=max_pages,
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_qualification_requirements(ctx: Context) -> dict[str, Any]:
        """查询当前账号的资质材料要求和私密 JSON 文件字段规范，不创建申请。"""
        result = await invoke(ctx, runtime.qualification_requirements)
        result["privateInputSchemas"] = {
            "business": BusinessData.model_json_schema(),
            "person": PersonData.model_json_schema(),
        }
        return result

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def create_qualification_draft(
        ctx: Context, name: str, purpose: Literal[1, 2]
    ) -> dict[str, Any]:
        """创建资质草稿：name 为 1 至 20 字，purpose 1 自用、2 他用；不提交线上申请，不依赖网页。草稿有效期以返回值为准。"""
        return await invoke(ctx, runtime.create_qualification_draft, name, purpose)

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def update_qualification_base(
        ctx: Context, draft_id: str, name: str, purpose: Literal[1, 2]
    ) -> dict[str, Any]:
        """修改资质名称或自用/他用用途，使原申请预览失效。"""
        return await invoke(
            ctx,
            runtime.change_qualification,
            draft_id,
            lambda draft: draft.set_base(name, purpose),
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def import_input_file(
        ctx: Context,
        relative_path: str,
        kind: Literal[
            "qualification_image",
            "qualification_data",
            "verification_code",
            "batch_csv",
        ],
        content_type: str,
    ) -> dict[str, Any]:
        """仅限 stdio：导入客户明确提供且已放入配置目录的文件，返回 fileId。禁止读取原文进入聊天。图片 JPEG/PNG，单张不超过 2 MB；CSV 不超过 50 MB。HTTP 客户端应由宿主通过鉴权的 POST /files 上传。"""
        if ctx.headers is not None:
            raise ToolError("HTTP 模式不允许读取服务器本地目录；请使用鉴权文件上传接口")
        try:
            owner, _credentials = runtime.caller(ctx)
            return await asyncio.to_thread(
                runtime.inputs.import_local, relative_path, kind, content_type, owner
            )
        except (StoreError, QualificationUploadError, AuthenticationError) as error:
            raise ToolError(str(error)) from None

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def export_qualification_review(
        ctx: Context, file_id: str, relative_path: str
    ) -> dict[str, Any]:
        """仅限 stdio：将 OCR 核对数据导出到材料目录内的全新文件，交客户私密查看。禁止把导出内容读入聊天。HTTP 宿主使用鉴权的 GET /files/{fileId}。"""
        if ctx.headers is not None:
            raise ToolError("HTTP 宿主请通过鉴权文件接口获取私密核对数据")
        try:
            owner, _credentials = runtime.caller(ctx)
            return await asyncio.to_thread(
                runtime.inputs.export_local, file_id, relative_path, owner
            )
        except (StoreError, AuthenticationError) as error:
            raise ToolError(str(error)) from None

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def upload_qualification_document(
        ctx: Context, draft_id: str, file_id: str, document: QualificationDocument
    ) -> dict[str, Any]:
        """将 qualification_image 文件上传到短信材料服务并关联草稿。营业证件指定类型；居民身份证指定类型 0 和 front/back；其他附件指定从 0 开始的连续 index。变更材料后重新确认和校验，不提交资质。"""
        return await invoke(
            ctx,
            runtime.upload_qualification_document,
            draft_id,
            file_id,
            document.model_dump(),
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def recognize_qualification_document(
        ctx: Context,
        draft_id: str,
        target: Literal["business", "operator", "responsible", "legal"],
    ) -> dict[str, Any]:
        """识别已上传的营业证件或居民身份证正反面。返回私密核对文件 ID；OCR 不自动替客户确认或提交。"""
        return await invoke(
            ctx, runtime.recognize_qualification_document, draft_id, target
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def update_qualification_information(
        ctx: Context,
        draft_id: str,
        target: Literal["business", "operator", "responsible", "legal"],
        file_id: str,
    ) -> dict[str, Any]:
        """保存客户已核对的 qualification_data JSON 文件，字段由 get_qualification_requirements 描述。修改后旧校验和预览失效，不在参数中接收原始个人字段。"""
        return await invoke(
            ctx, runtime.update_qualification_information, draft_id, target, file_id
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def set_qualification_responsible(
        ctx: Context, draft_id: str, same_operator: bool
    ) -> dict[str, Any]:
        """设置责任人是否与经办人相同；相同时复用已保存的经办人材料和校验。"""
        return await invoke(
            ctx,
            runtime.change_qualification,
            draft_id,
            lambda draft: draft.set_responsible_mode(same_operator),
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def clear_qualification_legal(ctx: Context, draft_id: str) -> dict[str, Any]:
        """移除可选的法人补充材料；营业证件上的法人姓名仍保留。"""
        return await invoke(
            ctx,
            runtime.change_qualification,
            draft_id,
            lambda draft: draft.clear_optional_legal(),
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def check_qualification_information(
        ctx: Context,
        draft_id: str,
        target: Literal["business", "operator", "responsible", "legal"],
    ) -> dict[str, Any]:
        """校验已保存的企业或人员信息，只返回脱敏状态；内部票据不暴露给模型。"""
        return await invoke(
            ctx,
            runtime.change_qualification,
            draft_id,
            lambda draft: draft.check_information(target),
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_qualification_verification_code(
        ctx: Context, draft_id: str, role: Literal["operator", "responsible"]
    ) -> dict[str, Any]:
        """预览向指定人员手机号发送验证码；展示脱敏号码并取得客户确认后使用 execute_sms_operation。"""
        return await invoke(ctx, runtime.prepare_qualification, draft_id, role)

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def verify_qualification_code(
        ctx: Context,
        draft_id: str,
        role: Literal["operator", "responsible"],
        file_id: str,
        request_id: str,
    ) -> dict[str, Any]:
        """验证客户通过私密渠道提供的 verification_code JSON 文件。request_id 为本次操作 UUID；服务端暂存副本在验证调用后删除，验证码不回显。"""
        return await invoke(
            ctx, runtime.verify_qualification_code, draft_id, role, file_id, request_id
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_qualification_application(
        ctx: Context, draft_id: str
    ) -> dict[str, Any]:
        """在材料和必要校验齐备后生成资质申请预览；客户确认当前预览后使用 execute_sms_operation 提交。"""
        return await invoke(ctx, runtime.prepare_qualification, draft_id, None)

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_qualification_draft(ctx: Context, draft_id: str) -> dict[str, Any]:
        """查询草稿缺少的材料、校验进展或提交结果；申请成功后用 list_qualifications 查询审核。"""
        return await invoke(ctx, runtime.qualification_status, draft_id)

    @mcp.tool(annotations=WRITE, structured_output=True)
    async def cancel_qualification_draft(ctx: Context, draft_id: str) -> dict[str, Any]:
        """放弃尚未提交的草稿并清除草稿材料，不撤销已提交或结果未知的申请。"""
        return await invoke(ctx, runtime.cancel_qualification, draft_id)

    @mcp.tool(annotations=READ, structured_output=True)
    async def check_batch_file(
        ctx: Context, file_id: str, sub_account: str, signature: str, template_id: str
    ) -> dict[str, Any]:
        """校验 batch_csv 文件的号码、重复项及选定模板变量，返回统计与文件指纹，不创建或启动群发任务。"""
        return await invoke(
            ctx, runtime.check_batch_file, file_id, sub_account, signature, template_id
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_batch_csv_template(
        ctx: Context, sub_account: str, template_id: str
    ) -> dict[str, Any]:
        """读取选定普通群发模板要求的 CSV 表头和示例。"""
        return await query(
            ctx,
            "batch-template-demo",
            sub_account=sub_account,
            template_id=template_id,
            force_update=False,
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_batch_task(ctx: Context, request: BatchRequest) -> dict[str, Any]:
        """校验已上传的 CSV 和已审核的普通通知/营销模板，预览群发任务；不支持验证码群发。"""
        return await invoke(ctx, runtime.prepare_batch, request.model_dump())

    @mcp.tool(annotations=READ, structured_output=True)
    async def get_batch_task(
        ctx: Context, sub_account: str, task_id: str
    ) -> dict[str, Any]:
        """查询普通群发任务。处理完成不等于每个号码都已送达。"""
        return await query(
            ctx, "batch-detail", sub_account=sub_account, task_id=task_id
        )

    @mcp.tool(annotations=READ, structured_output=True)
    async def list_batch_tasks(
        ctx: Context,
        sub_account: str,
        task_name: str | None = None,
        signature: str | None = None,
        template_id: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        """查询普通群发任务列表；已知 taskId 时优先查询详情。"""
        return await query(
            ctx,
            "batch-list",
            sub_account=sub_account,
            task_name=task_name,
            signature=signature,
            template_id=template_id,
            page=page,
            page_size=page_size,
        )

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_batch_launch(
        ctx: Context, request: BatchLaunchRequest
    ) -> dict[str, Any]:
        """生成普通群发启动预览。文件与内容摘要、人数取自创建结果。需客户明确确认启动该任务。"""
        return await invoke(ctx, runtime.prepare, "batch_launch", request.model_dump())

    @mcp.tool(annotations=PREPARE, structured_output=True)
    async def prepare_batch_cancel(
        ctx: Context, sub_account: str, task_id: str
    ) -> dict[str, Any]:
        """读取最新任务并预览取消操作；执行时再次校验是否仍可取消。"""
        return await invoke(
            ctx,
            runtime.prepare_cancel,
            {"sub_account": sub_account, "task_id": task_id},
        )

    return mcp


def main():
    parser = argparse.ArgumentParser(description="Volcengine SMS MCP server")
    parser.add_argument(
        "-t", "--transport", choices=["stdio", "streamable-http"], default="stdio"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    settings = Settings.from_env()
    runtime = Runtime(settings)
    mcp = build_server(runtime)
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    else:
        import uvicorn
        from .web import create_app

        settings.validate_http()
        uvicorn.run(create_app(runtime, mcp), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
