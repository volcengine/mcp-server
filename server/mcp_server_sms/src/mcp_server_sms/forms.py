"""短信表单的 MCP Apps 资源与结果边界，不保存用户填写的数据。"""

import json
from importlib.resources import files
from typing import Literal

from mcp.server.apps import Apps, ResourceCsp
from mcp.types import CallToolResult, TextContent

FORM_URI = "ui://sms/forms.html"
FORM_META = {"ui": {"resourceUri": FORM_URI, "visibility": ["model", "app"]}}
APP_ONLY_META = {"ui": {"visibility": ["app"]}}
FormKind = Literal["qualification", "signature", "traffic", "batch"]

_FORM_HELP = {
    "qualification": "填写企业、人员及材料信息，完成校验后预览并确认提交资质申请。",
    "signature": "选择资质、填写签名来源及证明材料，预览后确认提交签名申请。",
    "traffic": "选择录入链接或联系号码，核对备案或归属信息后确认提交。",
    "batch": "选择消息组和模板、上传名单并预览；创建任务与确认启动分别执行。",
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


def open_form(kind: FormKind) -> dict:
    """open_form 只打开界面；不支持 UI 的客户端仍能获得所需步骤与工具信息。"""
    return {
        "success": True,
        "form": kind,
        "mode": "input",
        "message": _FORM_HELP[kind],
        "result": None,
    }


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
