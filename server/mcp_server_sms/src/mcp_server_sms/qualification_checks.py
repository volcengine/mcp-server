"""企业自动核验与资质人工审核的上游契约。"""

from .client import failure
from .observability import observe_call
from .protocol import SmsAPIError

ENTERPRISE_CHECK = "ThreeElementEnterpriseCheckForAgent"
MANUAL_REVIEW_TICKET = "force_skip_check"
_MISMATCH_STATUSES = (1, 2, 3, "1", "2", "3", "\x01", "\x02", "\x03")
_UNAVAILABLE_CODES = {"connection_failed", "transport_error", "1999", "SY:0500"}


async def check_enterprise(call, params: dict, *, offer_manual_review: bool) -> dict:
    """check_enterprise 区分匹配、不匹配、校验服务不可用和其他拒绝。"""
    try:
        envelope = await call(ENTERPRISE_CHECK, params)
    except SmsAPIError as exc:
        envelope = exc.result
    if not offer_manual_review:
        if not envelope["success"]:
            raise SmsAPIError(envelope)
        return envelope

    diagnostic = envelope["error"] or {}
    status = envelope["result"]
    status = status.get("status") if isinstance(status, dict) else None
    mismatch = envelope["success"] and type(status) in (int, str) and status in _MISMATCH_STATUSES
    unavailable = not envelope["success"] and (
        diagnostic.get("source") == "transport" or diagnostic.get("code") in _UNAVAILABLE_CODES
        or diagnostic.get("http_status", 0) >= 500
    )
    if mismatch or unavailable:
        with observe_call("form", "qualification", path="manual_review_available") as observation:
            observation.record(envelope)
        return {
            **envelope, "success": True, "error": None,
            "result": {
                "manualReview": True,
                "code": "enterprise_check_mismatch" if mismatch else diagnostic.get("code"),
                "requestId": envelope["request_id"],
                **({"failure": envelope} if not envelope["success"] else {}),
            },
        }
    if not envelope["success"]:
        raise SmsAPIError(envelope)
    if isinstance(envelope["result"], dict):
        return {**envelope, "result": {**envelope["result"], "manualReview": False}}
    return envelope


def enterprise_ticket(envelope: dict) -> str:
    """enterprise_ticket 只把可转人工的结果转换成原生票据，不接受客户端构造的票据。"""
    result = envelope["result"]
    if isinstance(result, dict):
        if result.get("manualReview") is True:
            return MANUAL_REVIEW_TICKET
        status, ticket = result.get("status"), result.get("ticket")
        if type(status) in (int, str) and status in (0, "0", "\x00") and isinstance(ticket, str) and ticket:
            return ticket
    raise SmsAPIError(failure(
        ENTERPRISE_CHECK, "invalid_response", "企业校验结果不完整，请重新核验",
        envelope["request_id"],
    ))
