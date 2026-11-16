"""单条短信预览、资源复核和确认票据。"""

import hashlib
import hmac
import json
import math
import re
from collections.abc import Mapping
from typing import Annotated, Any

from pydantic import Field

from .auth import Credentials
from .client import failure
from .models import SmsSendRequest
from .protocol import SmsAPIError

SendConfirmation = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
_VARIABLE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
_CHANNELS = {"CN_OTP", "CN_NTC", "CN_MKT"}


def _reject(code: str, message: str, action: str = "ListSecondTemplate"):
    raise SmsAPIError(failure(action, code, message))


def _rows(envelope: Mapping[str, Any], action: str) -> list[Mapping[str, Any]]:
    result = envelope.get("result")
    if not isinstance(result, Mapping):
        _reject("invalid_response", "模板查询未返回有效结果", action)
    values = next(
        (result[key] for key in ("List", "list", "Items", "items") if key in result),
        None,
    )
    if not isinstance(values, list):
        _reject("invalid_response", "模板查询未返回资源列表", action)
    return [value for value in values if isinstance(value, Mapping)]


def _value(item: Mapping[str, Any], *names: str) -> Any:
    return next((item[name] for name in names if name in item), None)


def _relationship(item: Mapping[str, Any], *names: str) -> list[str] | None:
    value = _value(item, *names)
    if value is None:
        return None
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    if isinstance(value, list) and all(isinstance(part, str) for part in value):
        return value
    _reject("invalid_response", "模板适用范围格式无效")


def _supports(item: Mapping[str, Any], expected: str, *names: str) -> bool:
    values = _relationship(item, *names)
    return values is None or expected in values or "All" in values or "*" in values


def _parameter_names(value: Any) -> list[str]:
    if not isinstance(value, list):
        _reject("invalid_response", "模板变量元数据不完整")
    names = []
    for item in value:
        if isinstance(item, str):
            name = item
        elif isinstance(item, Mapping):
            name = _value(item, "name", "Name", "ParamName")
        else:
            name = None
        if not isinstance(name, str) or not name:
            _reject("invalid_response", "模板变量元数据不完整")
        names.append(name)
    return names


def _content_body(content: str, signature: str) -> str:
    prefix = f"【{signature}】"
    return content[len(prefix):] if content.startswith(prefix) else content


def _mask_mobile(value: str) -> str:
    return f"{value[:3]}****{value[-4:]}"


def _segments(content: str, signature: str) -> int:
    length = len(f"【{signature}】{content}")
    return 1 if length <= 70 else math.ceil(length / 67)


async def prepare_sms_send(call, request: SmsSendRequest, credentials: Credentials) -> dict[str, Any]:
    """重新读取模板和消息组，生成可展示的单条发送预览。"""
    envelope = await call("ListSecondTemplate", {
        "templateId": request.template_id,
        "signatures": request.signature,
        "subAccounts": [request.sub_account],
    })
    records = [
        item for item in _rows(envelope, "ListSecondTemplate")
        if _value(item, "TemplateId", "templateId") == request.template_id
        and _supports(item, request.signature, "Signatures", "signatures")
        and _supports(item, request.sub_account, "SubAccounts", "subAccounts")
    ]
    if not records:
        _reject(
            "template_preview_unavailable",
            "查询未取得该模板、签名和消息组的预览信息",
        )

    views: dict[str, dict[str, Any]] = {}
    explicit_group = False
    for item in records:
        content = _value(item, "TemplateContent", "Content", "content")
        params = _value(item, "TemplateParams", "templateParams")
        channel = _value(item, "ChannelType", "channelType")
        if params is None and isinstance(content, str) and _VARIABLE.search(content) is None:
            params = []
        if not isinstance(content, str) or channel not in _CHANNELS:
            _reject("invalid_response", "接口返回的模板正文、变量或短信类型不完整")
        names = _parameter_names(params)
        task_fields = _value(item, "TaskFields", "taskFields")
        if item.get("BatchOnly") is True or item.get("batchOnly") is True:
            _reject("batch_only_template", "该模板仅支持群发任务，不能发送单条短信")
        if task_fields not in (None, []):
            _reject("unsupported_task_fields", "该模板要求群发任务字段，不能发送单条短信")
        body = _content_body(content, request.signature)
        view = {
            "templateContent": body,
            "templateParams": names,
            "channelType": channel,
            "batchOnly": False,
            "taskFields": [],
        }
        key = json.dumps(view, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        views[key] = view
        groups = _relationship(item, "SubAccounts", "subAccounts")
        explicit_group = explicit_group or (
            groups is not None and request.sub_account in groups
        )

    if len(views) != 1:
        _reject(
            "ambiguous_template_preview",
            "查询到多种正文、变量或短信类型，请先核对模板记录",
        )
    if not explicit_group:
        groups = await call("GetSubAccountListForAgent", {
            "subAccount": request.sub_account,
            "pageIndex": 1,
            "pageSize": 100,
        })
        active = any(
            _value(item, "subAccountId", "SubAccountId") == request.sub_account
            and str(_value(item, "status", "Status")) == "1"
            for item in _rows(groups, "GetSubAccountListForAgent")
        )
        if not active:
            _reject(
                "message_group_unavailable",
                "所选消息组未出现在当前账号的启用列表中",
                "GetSubAccountListForAgent",
            )

    view = next(iter(views.values()))
    expected = view["templateParams"]
    if len(expected) != len(set(expected)):
        _reject("duplicate_template_variables", "模板变量元数据包含重复变量")
    if set(request.template_params) != set(expected):
        _reject("template_variables_mismatch", "变量值必须与模板变量逐一对应")
    content_variables = _VARIABLE.findall(view["templateContent"])
    if len(content_variables) != len(set(content_variables)) or set(content_variables) != set(expected):
        _reject("template_metadata_mismatch", "模板正文变量与变量元数据不一致")
    rendered = _VARIABLE.sub(
        lambda match: request.template_params[match.group(1)],
        view["templateContent"],
    )
    canonical = {
        "request": request.payload(),
        "resource": view,
        "renderedContentSha256": hashlib.sha256(rendered.encode()).hexdigest(),
        "accessKey": credentials.access_key,
        "sessionToken": credentials.session_token,
    }
    encoded = json.dumps(
        canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    confirmation = hmac.digest(
        credentials.secret_key.encode(), b"sms-send\0" + encoded, "sha256"
    ).hex()
    return {
        "maskedRecipient": _mask_mobile(request.mobiles[0]),
        "subAccount": request.sub_account,
        "signature": request.signature,
        "templateId": request.template_id,
        "channelType": view["channelType"],
        "variableNames": sorted(expected),
        "renderedContent": rendered,
        "estimatedSegments": _segments(rendered, request.signature),
        "confirmation": confirmation,
    }
