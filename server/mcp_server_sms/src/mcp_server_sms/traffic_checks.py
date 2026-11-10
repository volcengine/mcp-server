"""引流表单在提交前校验，受理后只读核对资源 ID。"""

import re
from urllib.parse import urlsplit

from anyio import move_on_after

from .client import failure
from .observability import observe_call
from .operations import RegisterLinksRequest, TrafficRegistration
from .protocol import SmsAPIError

_NUMBER_PATTERNS = {
    1: (re.compile(r"1[3-9][0-9]{9}"), "手机号"),
    2: (re.compile(r"400[0-9]{7}"), "400 号码"),
    3: (re.compile(r"700[0-9]+"), "700 号码"),
    4: (re.compile(r"800[0-9]{7}"), "800 号码"),
    5: (re.compile(r"9[56][0-9]{3}"), "95 或 96 号码"),
    6: (re.compile(r"12[0-9]{3}"), "12 号码"),
    7: (re.compile(r"[0-9]{10,12}"), "固定电话"),
}
_READBACK_SECONDS = 12
_URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")


def _link_identity(value: str):
    parsed = urlsplit(value if _URL_SCHEME.match(value) else "//" + value)
    if (
        not parsed.hostname or parsed.scheme not in ("", "http", "https")
        or parsed.username is not None or any(character.isspace() for character in value)
    ):
        raise ValueError
    # URL 路径与查询参数区分大小写。只让解析器识别协议、主机和端口，不修改原值。
    return parsed.scheme, parsed.hostname, parsed.port, parsed.path, parsed.query, parsed.fragment


def _matches_link(candidate: str | None, identity: tuple) -> bool:
    if not isinstance(candidate, str):
        return False
    try:
        return _link_identity(candidate) == identity
    except ValueError:
        return False


def validate_traffic_form(request: TrafficRegistration) -> None:
    """validate_traffic_form 按资源类型验证格式和本次表单内的重复项。"""
    seen = set()
    for index, row in enumerate(request.params.data, 1):
        if isinstance(request, RegisterLinksRequest):
            raw = row.jump_link if row.use_volc_link else row.link
            try:
                parsed = _link_identity(raw)
            except ValueError:
                raise SmsAPIError(failure(
                    request.action, "invalid_traffic_link", f"第 {index} 行链接格式不正确"
                )) from None
            if not row.use_volc_link and row.protocol != (parsed[0] or "缺省"):
                raise SmsAPIError(failure(
                    request.action, "traffic_protocol_mismatch", f"第 {index} 行协议与文案链接不一致"
                ))
            identity = (row.use_volc_link, parsed)
        else:
            pattern, label = _NUMBER_PATTERNS[row.number_type]
            if pattern.fullmatch(row.number) is None:
                raise SmsAPIError(failure(
                    request.action, "invalid_traffic_number", f"第 {index} 行请输入正确的{label}"
                ))
            identity = row.number
        if identity in seen:
            raise SmsAPIError(failure(
                request.action, "duplicate_traffic_resource", f"第 {index} 行与本次录入的其他资源重复"
            ))
        seen.add(identity)


async def read_back_traffic(call, request: TrafficRegistration) -> dict:
    """read_back_traffic 保留成功写入，只为精确匹配的资源补充 ID。"""
    ids = []
    is_link = isinstance(request, RegisterLinksRequest)
    action = "GetTobTrafficDrivingLinkListForAgent" if is_link else "GetTobTrafficDrivingPhoneListForAgent"
    with observe_call("form", "traffic", path="read_back") as observation:
        with move_on_after(_READBACK_SECONDS):
            for row in request.params.data:
                if is_link:
                    field, value = ("jumpLink", row.jump_link) if row.use_volc_link else ("link", row.link)
                    filters = {field: value, "useVolcLink": row.use_volc_link}
                    identity = _link_identity(value)
                else:
                    field, value = "number", row.number
                    filters = {field: value}
                try:
                    result = (await call(action, filters))["result"]
                except SmsAPIError:
                    continue
                records = result.get("list", result.get("List")) if isinstance(result, dict) else None
                if not isinstance(records, list):
                    continue
                matches = [
                    item for item in records
                    if isinstance(item, dict) and (
                        _matches_link(item.get(field), identity)
                        and item.get("useVolcLink", row.use_volc_link) is row.use_volc_link
                        if is_link else item.get(field) == value
                    )
                ]
                if len(matches) == 1 and type(matches[0].get("id")) is int and matches[0]["id"] > 0:
                    ids.append(matches[0]["id"])
        count = len(request.params.data)
        verified = len(ids) == count
        observation.result_class = "success" if verified else "partial"
        return {"resourceIds": ids, "submittedRecordCount": count, "verified": verified}
