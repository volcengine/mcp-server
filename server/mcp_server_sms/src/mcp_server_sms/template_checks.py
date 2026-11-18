"""模板申请校验、当前账号限制和固定引流预检。"""

import hmac
import json
import re
from collections import Counter
from time import time

from .auth import Credentials
from .client import failure
from .configuration import FORM_CONFIG
from .models import TemplateApplication
from .observability import observe_call
from .protocol import SmsAPIError

_VARIABLE = re.compile(r"\$\{([^{}]*)\}")
_VARIABLE_NAME = re.compile(r"[A-Za-z0-9_]+")
_OTP_CONTENT = re.compile(r"验证码|code\s|code\s+is|注册码|校验码|动态码|动态密码")
_MARKETING_UNSUBSCRIBE = "拒收请回复R"
_MAX_TEMPLATE_VARIABLES = 20
_MAX_TRAFFIC = {2: 1, 3: 2, 4: 1}


def _reject(code: str, message: str, action: str = "ApplySmsTemplateV2ForAgent"):
    raise SmsAPIError(failure(action, code, message))


def template_variables(content: str) -> list[str]:
    """template_variables 按短信原生占位符语法提取变量，不改写正文或变量名。"""
    names = [match[1] for match in _VARIABLE.finditer(content)]
    if "${" in _VARIABLE.sub("", content) or any(_VARIABLE_NAME.fullmatch(name) is None for name in names):
        raise SmsAPIError(failure(
            "ApplySmsTemplateV2ForAgent", "invalid_template_variables", "请使用完整的 ${变量名}，名称仅含英文、数字或下划线"
        ))
    return names


def validate_template_application(request: TemplateApplication) -> None:
    """validate_template_application 对齐模板原生规则，不改写或截断正文。"""
    with observe_call("form", "template", path="validate") as observation:
        try:
            for value, maximum in ((request.name, 50), (request.description or "", 300)):
                try:
                    units = len(value.encode("utf-16-le")) // 2
                except UnicodeEncodeError:
                    _reject("invalid_template_text", "模板名称或用途包含无法编码的字符")
                if units > maximum:
                    _reject("invalid_template_length", "模板名称最多 50 字符，用途最多 300 字符")
            if len(request.name.encode("utf-8")) > 100:
                _reject("invalid_template_length", "模板名称不能超过 100 个字节")
            names = template_variables(request.content)
            if any(name.lower() == "volc_sms_url_token" for name in names):
                _reject("invalid_template_variables", "不能使用保留变量名 volc_sms_url_token")
            definitions = request.template_params or []
            declared = {item.name: item.param_type for item in definitions}
            if not request.signatures or any(not item for item in request.signatures):
                raise SmsAPIError(failure("ApplySmsTemplateV2ForAgent", "signature_required", "请至少选择一个短信签名"))
            if len(declared) != len(definitions) or set(names) != set(declared):
                raise SmsAPIError(failure(
                    "ApplySmsTemplateV2ForAgent", "invalid_template_variables", "正文变量与变量设置必须一一对应，不能重复定义"
                ))
            if request.channel_type == "CN_OTP" and (
                len(names) != 1 or set(declared.values()) != {1} or request.template_traffic_driving
            ):
                raise SmsAPIError(failure(
                    "ApplySmsTemplateV2ForAgent", "invalid_otp_template", "验证码模板需且只能有一个普通变量，不支持引流绑定"
                ))
            if request.channel_type == "CN_OTP" and _OTP_CONTENT.search(request.content) is None:
                _reject("invalid_otp_template", "验证码正文需要包含验证码、注册码、校验码、动态码、动态密码或 code")
            if request.channel_type != "CN_OTP":
                matches = list(_VARIABLE.finditer(request.content))
                if any(left.end() == right.start() for left, right in zip(matches, matches[1:])):
                    _reject("invalid_template_variables", "通知和营销模板不支持相邻占位符，请保留分隔内容")
                if len(matches) > _MAX_TEMPLATE_VARIABLES:
                    _reject(
                        "invalid_template_variables",
                        f"每个通知或营销模板最多包含 {_MAX_TEMPLATE_VARIABLES} 个变量占位符",
                    )
            if request.channel_type == "CN_MKT" and not request.content.endswith(_MARKETING_UNSUBSCRIBE):
                _reject(
                    "invalid_marketing_unsubscribe",
                    f"营销模板末尾必须为“{_MARKETING_UNSUBSCRIBE}”",
                )
            if request.short_url_config and request.short_url_config.is_enabled == "1" and request.channel_type != "CN_MKT":
                raise SmsAPIError(failure("ApplySmsTemplateV2ForAgent", "invalid_short_link", "平台短链只适用于营销模板"))
            traffic_names = {name for name, kind in declared.items() if kind in (2, 3)}
            groups = request.template_traffic_driving or []
            if traffic_names and not groups:
                raise SmsAPIError(failure("ApplySmsTemplateV2ForAgent", "traffic_binding_required", "请为链接或电话号码变量选择已报备资源"))
            for group in groups:
                if len({item.name for item in group}) != len(group) or {item.name for item in group} != traffic_names:
                    raise SmsAPIError(failure("ApplySmsTemplateV2ForAgent", "invalid_traffic_binding", "每组引流绑定需完整覆盖对应变量且不重复"))
                if any(declared[item.name] != item.param_type for item in group):
                    raise SmsAPIError(failure("ApplySmsTemplateV2ForAgent", "invalid_traffic_binding", "引流绑定类型与变量类型不一致"))
            counts = Counter(declared.values())
            if any(counts[kind] > maximum for kind, maximum in _MAX_TRAFFIC.items()):
                _reject("too_many_traffic_params", "包含固定内容在内，最多 1 个链接、2 个联系号码和 1 个链接 Path")
        except SmsAPIError as exc:
            observation.record(exc.result)
            raise
        observation.record({"success": True})


async def _resolve_traffic(call, body: dict) -> None:
    """显式 ID 必须属于本次账号，补齐原始绑定内容，不修改正文。"""
    resources = {}
    use_volc_link = body.get("shortUrlConfig", {}).get("isEnabled") == "1"
    for group in body.get("templateTrafficDriving", []):
        for item in group:
            kind, resource_id = item["paramType"], item["id"]
            key = (kind, resource_id)
            action = "GetTobTrafficDrivingLinkListForAgent" if kind == 2 else "GetTobTrafficDrivingPhoneListForAgent"
            if key not in resources:
                params = {"id": resource_id, **({"useVolcLink": use_volc_link} if kind == 2 else {})}
                envelope = await call(action, params)
                result = envelope.get("result")
                rows = result.get("list") if isinstance(result, dict) else None
                if not isinstance(rows, list):
                    _reject("invalid_response", "引流查询未返回资源列表", action)
                matches = [row for row in rows if isinstance(row, dict) and type(row.get("id")) is int and row["id"] == resource_id]
                if len(matches) != 1:
                    _reject("invalid_traffic_binding", "所选引流资源不存在或不属于当前账号", action)
                resources[key] = matches[0]
            resource = resources[key]
            if kind == 2 and type(resource.get("useVolcLink")) is not bool:
                _reject("invalid_response", "链接资源缺少短链类型，无法确定绑定内容", action)
            if kind == 2 and resource["useVolcLink"] != use_volc_link:
                _reject("invalid_traffic_binding", "所选链接与当前平台短链设置不一致，请重新选择", action)
            field = ("jumpLink" if resource["useVolcLink"] else "link") if kind == 2 else "number"
            original = resource.get(field)
            if not isinstance(original, str) or not original:
                _reject("invalid_response", "所选引流资源缺少可绑定的原始内容", action)
            permitted = [original]
            if kind == 2 and resource.get("jumpLink"):
                permitted.append(resource["jumpLink"])
            if item.get("content") and item["content"] not in permitted:
                _reject("invalid_traffic_binding", "引流 content 与所选资源 id 不一致，请重新核对", action)
            if not item.get("content"):
                item["content"] = original


async def prepare_template_application(
    call, request: TemplateApplication, credentials: Credentials, *, expires_at: int | None = None
) -> dict:
    """预览和提交均调用同一只读前检，确认绑定参数、账号及核对结果。"""
    with observe_call("form", "template", path="prepare") as observation:
        try:
            validate_template_application(request)
            envelope = await call("ListAllSmsProduct", {})
            account = envelope.get("result")
            if not isinstance(account, dict) or not isinstance(account.get("userType"), str):
                _reject("invalid_response", "账号类型或身份信息不完整，请先核实", "ListAllSmsProduct")
            definitions = request.template_params or []
            if request.channel_type == "CN_MKT" and definitions:
                if type(account.get("mktParam")) is not int:
                    _reject("invalid_response", "账号查询未提供有效的营销变量配置，请先核实", "ListAllSmsProduct")
                if account["mktParam"] != 1:
                    _reject("template_account_restricted", "当前账号未允许营销模板使用变量")
            if account["userType"] == "smb" and request.channel_type == "CN_NTC" and definitions:
                _reject("template_account_restricted", "因短信行业风险管控，小微账号暂不支持带变量的通知模板")
            body = request.payload()
            await _resolve_traffic(call, body)
            envelope = await call("CheckTrafficDrivingExist", {
                "content": body["content"],
                "useVolcLink": body.get("shortUrlConfig", {}).get("isEnabled") == "1",
            })
            result = envelope.get("result")
            fixed = result.get("list") if isinstance(result, dict) else None
            if not isinstance(fixed, list):
                _reject("invalid_response", "固定引流查询未返回资源列表，请先核实", "CheckTrafficDrivingExist")
            for item in fixed:
                if (not isinstance(item, dict) or type(item.get("paramType")) is not int
                        or item["paramType"] not in (2, 3) or type(item.get("isExist")) is not bool):
                    _reject("invalid_response", "固定引流查询结果不完整，请先核实", "CheckTrafficDrivingExist")
                if not item["isExist"]:
                    _reject("fixed_traffic_missing", "正文中的固定链接或联系号码尚未录入引流信息库，请先录入")
                if (type(item.get("id")) is not int or item["id"] <= 0
                        or not isinstance(item.get("content"), str) or not item["content"]):
                    _reject("invalid_response", "固定引流查询缺少资源 ID 或原始内容，请先核实", "CheckTrafficDrivingExist")
            counts = Counter([item.param_type for item in definitions] + [item["paramType"] for item in fixed])
            if any(counts[kind] > maximum for kind, maximum in _MAX_TRAFFIC.items()):
                _reject("too_many_traffic_params", "包含固定内容在内，最多 1 个链接、2 个联系号码和 1 个链接 Path")
            if request.channel_type == "CN_OTP" and fixed:
                _reject("invalid_otp_template", "验证码模板不支持固定链接或联系号码")
            warnings = []
            if account["userType"] == "smb" and any(item["paramType"] == 2 for item in fixed):
                warnings.append("小微账号带固定链接有审核拒绝风险；引流资源已录入不代表模板审核通过")
            if account["userType"] == "smb" and request.channel_type == "CN_MKT":
                warnings.append("小微账号营销模板可能受准入限制，是否开放以服务端结果为准；明确受限后停止原样重试")
            view = {
                "request": body,
                "account": {key: account[key] for key in ("businessName", "userType", "mktParam") if key in account},
                "fixedTraffic": fixed, "warnings": warnings,
            }
            if expires_at is None:
                expires_at = int(time()) + FORM_CONFIG["previewConfirmationTtlSeconds"]
            encoded = json.dumps({
                "view": view, "accessKey": credentials.access_key, "sessionToken": credentials.session_token,
                "expiresAt": expires_at,
            }, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            signature = hmac.digest(
                credentials.secret_key.encode(), b"sms-template\0" + encoded, "sha256"
            ).hex()
            view["confirmation"] = {"expires_at": expires_at, "signature": signature}
        except SmsAPIError as exc:
            observation.record(exc.result)
            raise
        observation.record({"success": True})
        return view


def template_apply_payload(view: dict) -> dict:
    """按 ApplySmsTemplateV2ForAgent 契约移除核对字段并补齐固定引流结构。"""
    body = {**view["request"]}
    body["templateTrafficDriving"] = [
        [{"name": item["name"], "paramType": item["paramType"], "id": item["id"]} for item in group]
        for group in body.get("templateTrafficDriving", [])
    ]
    body["fixTrafficDriving"] = [
        {"paramType": item["paramType"], "id": item["id"], "content": item["content"]}
        for item in view["fixedTraffic"]
    ]
    return body
