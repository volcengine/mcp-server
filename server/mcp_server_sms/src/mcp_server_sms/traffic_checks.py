"""引流表单的本地格式及重复项校验。"""

import re
from urllib.parse import urlsplit

from .client import failure
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
