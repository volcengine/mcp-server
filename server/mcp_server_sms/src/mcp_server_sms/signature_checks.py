"""签名表单在提交前复核已确认的资质主体和名称风险。"""

from pydantic import Field

from .client import failure
from .models import ApiModel, SignatureApplication, Text
from .observability import observe_call
from .protocol import SmsAPIError


class SignatureFormConfirmation(ApiModel):
    business_name: Text = Field(alias="businessCertificateName")
    accept_name_risk: bool = Field(alias="acceptNameRisk", strict=True)


async def check_signature_confirmation(call, request: SignatureApplication, confirmation):
    """check_signature_confirmation 校验当前资质及客户刚核对的主体名称。"""
    action = "ApplySmsSignatureV2"
    if not 2 <= len(request.content) <= 25:
        raise SmsAPIError(failure(action, "invalid_signature", "签名内容须为 2 至 25 个字符"))
    if request.source == 3 and not (request.trademark and request.trademark.trademark_number):
        raise SmsAPIError(failure(action, "trademark_number_required", "请填写商标注册号"))
    result = await call("GetSignatureIdentificationList", {
        "id": request.qualification_id, "status": [3], "pageIndex": 1, "pageSize": 100,
    })
    listing = result["result"]
    rows = listing.get("list", listing.get("List")) if isinstance(listing, dict) else None
    matches = [
        row for row in rows
        if isinstance(row, dict) and type(row.get("id")) is int
        and row["id"] == request.qualification_id and row.get("auditStatus") == 3
        and row.get("usable") is True
    ] if isinstance(rows, list) else []
    if len(matches) != 1:
        raise SmsAPIError(failure(action, "qualification_unavailable", "所选资质不可用，请重新核对"))
    row = matches[0]
    info = row.get("businessInfo")
    name = (info.get("businessCertificateName") if isinstance(info, dict) else None) or row.get(
        "businessCertificateName"
    )
    if name != confirmation.business_name or row.get("purpose") != request.purpose:
        raise SmsAPIError(failure(action, "qualification_changed", "关联资质已变化，请重新核对"))
    name_risk = request.content not in name
    with observe_call(
        "form", "signature", path="name_risk" if name_risk else "name_matched"
    ) as observation:
        if name_risk and not confirmation.accept_name_risk:
            error = failure(action, "signature_name_risk", "请明确确认签名名称风险后提交")
            observation.record(error)
            raise SmsAPIError(error)
        observation.record(result)
