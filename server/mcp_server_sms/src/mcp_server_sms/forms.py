"""短信表单的 MCP Apps 资源与结果边界，不保存用户填写的数据。"""

import json
from importlib.resources import files
from typing import Annotated, Any, Literal

from mcp.server.apps import Apps, ResourceCsp
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, TextContent

from .models import ApiModel
from .observability import observe_call

FORM_URI = "ui://sms/forms.html"
FORM_META = {"ui": {"resourceUri": FORM_URI, "visibility": ["model", "app"]}}
APP_ONLY_META = {"ui": {"visibility": ["app"]}}
FormKind = Literal["qualification", "signature", "traffic", "batch", "service"]
# 保留工具原有的结构化结果 Schema，同时用 CallToolResult 携带仅给表单的元数据。
FormToolResult = Annotated[CallToolResult, dict[str, Any]]


_FORM_HELP = {
    "qualification": "填写企业、人员及材料信息，完成校验后预览并确认提交资质申请。",
    "signature": "选择资质、填写签名来源及证明材料，预览后确认提交签名申请。",
    "traffic": "选择录入链接或联系号码，核对备案或归属信息后确认提交。",
    "batch": "选择消息组和模板、上传名单并预览；创建任务与确认启动分别执行。",
    "service": "核对国内短信服务状态，阅读协议和计费说明后按页面确认。",
}


def form_extension() -> Apps:
    """form_extension 注册离线打包的 HTML，宿主无需加载外部脚本或业务连接。"""
    extension = Apps()
    html = files("mcp_server_sms").joinpath("static/forms.html").read_text(encoding="utf-8")
    extension.add_html_resource(
        FORM_URI,
        html,
        name="sms_forms",
        title="短信业务表单",
        csp=ResourceCsp(
            connect_domains=[], resource_domains=[], frame_domains=[], base_uri_domains=[]
        ),
        prefers_border=True,
    )
    return extension


def open_form(
    kind: FormKind, request: ApiModel | None, prefill: ApiModel | None
) -> CallToolResult | None:
    """open_form 打开可编辑草稿，或让已授权的完整请求进入原业务路径。"""
    if request is not None and prefill is None:
        return None
    path = (
        "conflicting_arguments" if request is not None
        else "prefilled" if prefill is not None
        else "blank"
    )
    with observe_call("form", kind, path=path) as observation:
        if request is not None:
            raise ToolError("预填表单和提交是两个操作，prefill 与 request 不可同时传入。")
        summary = {
            "success": True,
            "form": kind,
            "mode": "input",
            "message": _FORM_HELP[kind],
            "result": None,
        }
        # 宿主已提供的草稿仅交给表单；普通结果不回显个人信息或附件。
        result = CallToolResult(
            content=[TextContent(type="text", text=json.dumps(summary, ensure_ascii=False))],
            structured_content=summary,
            meta={"sms/form": {"prefill": prefill.payload()}} if prefill is not None else None,
        )
        observation.record(summary)
        return result


def private_result(result: dict) -> CallToolResult:
    """private_result 将表单专用明细放在元数据，普通结果仅交接操作状态。"""
    summary = {
        "success": result["success"],
        "action": result.get("action"),
        "request_id": result.get("request_id"),
        "error": result.get("error"),
        "result": None,
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(summary, ensure_ascii=False))],
        structured_content=summary,
        is_error=not summary["success"],
        meta={"sms/form": result},
    )


def tool_result(result: dict, private: bool) -> CallToolResult:
    """tool_result 保留普通客户端结果格式，表单调用可显式选择私密明细。"""
    if private:
        return private_result(result)
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False))],
        structured_content=result,
    )
