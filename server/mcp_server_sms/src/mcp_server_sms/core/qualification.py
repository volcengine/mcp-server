# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
# Licensed under the Apache License, Version 2.0.
"""Qualification business rules independent of MCP, HTTP and user interfaces."""

from __future__ import annotations
import datetime
from copy import deepcopy
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, ValidationError
import re
import time
from .qualification_upload import ocr_business_certificate_image
from typing import Any, Dict, Mapping
from .qualification_upload import (
    BUSINESS_CHECK_SKIP_TICKET,
    MAX_IMAGE_BYTES,
    QualificationUploadError,
    check_mobile_verification_code,
    check_signature_qualification_information,
    create_signature_qualification,
    get_account_identity,
    get_account_ident_rank,
    normalize_check_status,
    ocr_identity_document_images,
    send_mobile_verification_code,
    upload_qualification_file_bytes,
)

MAX_JSON_BYTES = 64 * 1024
PERSON_FILE_TYPES = {"operator": (8, 9), "responsible": (10, 11), "legal": (18, 19)}
LEGAL_CERTIFICATE_TYPES = frozenset({0, 1, 2, 3, 4, 9})
LEGAL_DOCUMENT_FILE_TYPES = {1: 12, 2: 13, 3: 14, 4: 15, 9: 6}
PERSON_LABELS = {"operator": "经办人", "responsible": "责任人", "legal": "法人"}


class PrivateData(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class BusinessData(PrivateData):
    businessCertificateType: Literal[1, 4, 6, 7]
    businessCertificateName: str = Field(min_length=1, max_length=256)
    unifiedSocialCreditIdentifier: str = Field(min_length=1, max_length=64)
    legalPersonName: str = Field(min_length=1, max_length=256)
    businessCertificateValidityPeriodStart: str
    businessCertificateValidityPeriodEnd: str


class PersonData(PrivateData):
    certificateType: Literal[0, 1, 2, 3, 4, 9] = 0
    personName: str = ""
    personIDCard: str = ""
    personMobile: str = ""


def new_state(client):
    rank = get_account_ident_rank(client)
    identity = get_account_identity(client)
    return {
        "rank": rank,
        "accountBusinessName": identity["businessName"],
        "userType": identity["userType"],
        "mobileVerificationRequired": identity["userType"] == "smb",
        "revision": 0,
        "materialName": "",
        "purpose": 1,
        "authorizee": "",
        "sameOperator": None,
        "sections": {},
        "pending": {},
        "checks": {},
        "mobileVerifications": {},
        "done": False,
        "result": None,
    }


def requirements(state):
    return {
        "accountRules": state["rank"],
        "accountBusinessName": state["accountBusinessName"],
        "mobileVerificationRequired": state["mobileVerificationRequired"],
        "imageTypes": ["image/jpeg", "image/png"],
        "maxImageBytes": MAX_IMAGE_BYTES,
        "legalPersonOptional": True,
    }


def public_state(state):
    if state["done"]:
        return {"status": "finished", "result": state["result"]}
    sections = state["sections"]
    checks = {
        role: _public_check(state, role) for role in ("business", *PERSON_FILE_TYPES)
    }
    if state["sameOperator"] is True:
        checks["responsible"] = dict(checks["operator"])
    missing = []
    if not state["materialName"]:
        missing.append("base_information")
    for role in ("business", "operator"):
        if role not in sections:
            missing.append(role + "_information")
    if state["sameOperator"] is None:
        missing.append("responsible_mode")
    elif not state["sameOperator"] and "responsible" not in sections:
        missing.append("responsible_information")
    for role in ("business", "operator", "responsible"):
        if not checks[role]["canContinue"]:
            missing.append(role + "_check")
    legal = sections.get("legal")
    if (
        legal
        and legal["certificateType"] == 0
        and legal["personIDCard"]
        and not checks["legal"]["matched"]
    ):
        missing.append("legal_check")
    verified = {
        role: _mobile_verified(state, role) for role in ("operator", "responsible")
    }
    missing.extend(
        role + "_mobile_verification" for role, passed in verified.items() if not passed
    )
    if state["purpose"] == 2:
        if not state["authorizee"]:
            missing.append("account_business_name")
        if state["rank"]["needOtherUseCheck"] and "powerOfAttorney" not in sections:
            missing.append("power_of_attorney")
    if state["pending"]:
        missing.append("confirm_uploaded_information")
    return {
        "status": "draft",
        "revision": state["revision"],
        "materialName": state["materialName"],
        "purpose": state["purpose"],
        "sameOperator": state["sameOperator"],
        "savedSections": list(sections),
        "pendingSections": list(state["pending"]),
        "checks": checks,
        "mobileVerifications": verified,
        "missing": missing,
        "readyForPreview": not missing,
    }


class QualificationDraft:
    """Serialized business operations; the caller owns persistence and authorization."""

    def __init__(self, client, state):
        self.client, self.state = client, state

    def set_base(self, name, purpose):
        name = _text(name, maximum=20)
        if purpose not in (1, 2):
            raise ValueError("资质用途必须为自用或他用")
        state = self.state
        state.update(
            materialName=name,
            purpose=purpose,
            authorizee=state["accountBusinessName"] if purpose == 2 else "",
        )
        if purpose == 1:
            for target in ("powerOfAttorney", "otherMaterials"):
                state["sections"].pop(target, None)
                state["pending"].pop(target, None)
        state["revision"] += 1

    def upload_document(
        self,
        content,
        content_type,
        target,
        certificate_type=None,
        side=None,
        index=None,
        replace=False,
    ):
        state = self.state
        if target == "business":
            valid = (
                certificate_type in (1, 4, 6, 7)
                and side is None
                and index is None
                and not replace
            )
        elif target in PERSON_FILE_TYPES:
            if target == "legal" and certificate_type in LEGAL_DOCUMENT_FILE_TYPES:
                valid = side is None and index in (0, 1)
            else:
                valid = (
                    certificate_type == 0
                    and side in ("front", "back")
                    and index is None
                    and not replace
                )
        elif target == "powerOfAttorney":
            valid = (
                state["purpose"] == 2
                and state["rank"]["needOtherUseCheck"]
                and certificate_type is None
                and side is None
                and index is None
                and not replace
            )
        elif target == "otherMaterials":
            valid = (
                state["purpose"] == 2
                and certificate_type is None
                and side is None
                and index in range(5)
            )
        else:
            valid = False
        if not valid:
            raise ValueError("材料类型、证件类型或图片位置与当前申请不匹配")
        if target == "otherMaterials":
            documents = [] if replace else state["sections"].get(target, [])
            if index > len(documents):
                raise ValueError("材料序号必须连续")
        elif target == "legal" and certificate_type in LEGAL_DOCUMENT_FILE_TYPES:
            pending = state["pending"].get("legal", {})
            documents = (
                []
                if replace or pending.get("certificateType") != certificate_type
                else pending.get("documents", [])
            )
            if index > len(documents):
                raise ValueError("材料序号必须连续")
        uploaded = upload_qualification_file_bytes(self.client, content, content_type)
        if target == "powerOfAttorney":
            state["sections"][target] = uploaded
        elif target == "otherMaterials":
            existing = [] if replace else state["sections"].get(target, [])
            materials = list(existing)
            if index == len(materials):
                materials.append(uploaded)
            else:
                materials[index] = uploaded
            state["sections"][target] = materials
        elif target == "business":
            state["pending"][target] = {**uploaded, "certificateType": certificate_type}
        else:
            pending = state["pending"].setdefault(target, {})
            if pending and pending.get("certificateType") != certificate_type:
                pending.clear()
            pending["certificateType"] = certificate_type
            if certificate_type == 0:
                pending.setdefault("imageUris", {})[side] = uploaded["imageUri"]
                pending.setdefault("imageSuffixes", {})[side] = uploaded["imageSuffix"]
            else:
                documents = [] if replace else pending.get("documents", [])
                if index == len(documents):
                    documents.append(uploaded)
                else:
                    documents[index] = uploaded
                pending["documents"] = documents
        state["checks"].pop(target, None)
        state["mobileVerifications"].pop(target, None)
        state["revision"] += 1
        return {"uploaded": True, "target": target}

    def recognize_document(self, target):
        pending = self.state["pending"].get(target)
        if not pending:
            raise ValueError("请先上传需要识别的材料")
        if target == "business":
            result = ocr_business_certificate_image(
                self.client, pending["imageUri"], pending["certificateType"]
            )
        elif (
            target in PERSON_FILE_TYPES
            and pending["certificateType"] == 0
            and _has_identity_image_pair(pending)
        ):
            result = ocr_identity_document_images(
                self.client,
                pending["imageUris"]["front"],
                pending["imageUris"]["back"],
                image_suffixes=pending["imageSuffixes"],
            )["person"]
        else:
            raise ValueError("当前证件不支持 OCR，或身份证正反面尚未齐全")
        # Raw OCR results travel through the private file exchange, never a tool result.
        return result

    def set_information(self, target, document):
        model = BusinessData if target == "business" else PersonData
        if target not in ("business", *PERSON_FILE_TYPES):
            raise ValueError("不支持的信息类型")
        try:
            values = model.model_validate(document).model_dump()
        except ValidationError as error:
            fields = [
                ".".join(map(str, item["loc"]))
                for item in error.errors(include_input=False)
            ]
            raise ValueError("材料字段格式不正确：" + ", ".join(fields)) from None
        state = self.state
        sections = state["sections"]
        pending = state["pending"].get(target)
        existing = sections.get(target)
        if target == "business":
            start = _date(values["businessCertificateValidityPeriodStart"])
            end = _date(values["businessCertificateValidityPeriodEnd"])
            if end < start:
                raise ValueError("营业证件有效期结束时间早于开始时间")
            source = pending if pending is not None else existing
            if state["rank"]["needBusinessCertificateImage"] and not (
                source and source.get("imageUri")
            ):
                raise ValueError("当前账号要求提供营业证件图片")
            if source and source.get("imageUri"):
                source_type = source.get(
                    "certificateType", source.get("businessCertificateType")
                )
                if source_type != values["businessCertificateType"]:
                    raise ValueError("营业证件类型已变化，请重新上传对应图片")
                values.update(
                    imageUri=source["imageUri"], imageSuffix=source["imageSuffix"]
                )
            legal = sections.get("legal")
            if legal and legal["personName"] != values["legalPersonName"]:
                sections.pop("legal", None)
                state["pending"].pop("legal", None)
                state["checks"].pop("legal", None)
        else:
            certificate_type = values["certificateType"]
            if target != "legal" and certificate_type != 0:
                raise ValueError("经办人和责任人仅支持居民身份证")
            if target == "responsible" and state["sameOperator"] is True:
                raise ValueError("当前责任人复用经办人，请先切换为不同人员")
            values["personName"] = (
                _legal_person_name(sections.get("business"), values["personName"])
                if target == "legal"
                else _text(values["personName"])
            )
            values["personIDCard"] = (
                _id_card(values["personIDCard"], required=target != "legal")
                if certificate_type == 0
                else _optional_text(values["personIDCard"], maximum=64)
            )
            values["personMobile"] = _mobile(
                values["personMobile"],
                required=_person_requirement(state["rank"], target, "mobile"),
            )
            source = pending if pending is not None else existing
            if source and source.get("certificateType") != certificate_type:
                source = None
            if certificate_type == 0:
                if (
                    source
                    and source.get("imageUris")
                    and not _has_identity_image_pair(source)
                ):
                    raise ValueError("身份证图片需要同时提供正反面")
                if _person_requirement(
                    state["rank"], target, "image"
                ) and not _has_identity_image_pair(source):
                    raise ValueError("当前账号要求提供该人员的身份证正反面")
                if _has_identity_image_pair(source):
                    values.update(
                        imageUris=dict(source["imageUris"]),
                        imageSuffixes=dict(source["imageSuffixes"]),
                    )
            elif source and source.get("documents"):
                values["documents"] = deepcopy(source["documents"])
            state["mobileVerifications"].pop(target, None)
        sections[target] = values
        state["pending"].pop(target, None)
        state["checks"].pop(target, None)
        if target == "operator" and state["sameOperator"] is True:
            sections.pop("responsible", None)
            state["checks"].pop("responsible", None)
        state["revision"] += 1

    def clear_optional_legal(self):
        for key in ("sections", "pending", "checks"):
            self.state[key].pop("legal", None)
        self.state["revision"] += 1

    def set_responsible_mode(self, same_operator):
        state = self.state
        operator = state["sections"].get("operator")
        if not operator:
            raise ValueError("请先保存经办人信息")
        if same_operator:
            if _person_requirement(
                state["rank"], "responsible", "image"
            ) and not _has_identity_image_pair(operator):
                raise ValueError("复用责任人前需要补齐经办人身份证图片")
            if (
                _person_requirement(state["rank"], "responsible", "mobile")
                and not operator["personMobile"]
            ):
                raise ValueError("复用责任人前需要补齐经办人手机号")
            for key in ("sections", "pending", "checks", "mobileVerifications"):
                state[key].pop("responsible", None)
        state["sameOperator"] = same_operator
        state["revision"] += 1

    def check_information(self, target):
        state = self.state
        if target in state["pending"]:
            raise ValueError("请先确认新上传材料对应的信息")
        result = check_signature_qualification_information(
            self.client, target, _verification_params(state, target)
        )
        state["checks"][target] = result
        if target in ("operator", "responsible"):
            state["mobileVerifications"].pop(target, None)
        state["revision"] += 1
        return {"target": target, "check": _public_check(state, target)}

    def code_recipient(self, role):
        state = self.state
        if (
            role not in ("operator", "responsible")
            or not state["mobileVerificationRequired"]
            or (role == "responsible" and state["sameOperator"] is True)
        ):
            raise ValueError("当前人员无需独立进行手机号验证码校验")
        person = state["sections"].get(role)
        check = state["checks"].get(role)
        if (
            not person
            or not person["personMobile"]
            or not check
            or not check["matched"]
        ):
            raise ValueError("请先完成该人员的信息校验并提供手机号")
        return person["personMobile"]

    def send_code(self, role):
        mobile = self.code_recipient(role)
        previous = self.state["mobileVerifications"].get(role)
        if previous and time.time() - previous.get("sentAt", 0) < 60:
            raise ValueError("验证码发送间隔至少为 60 秒")
        message_id = send_mobile_verification_code(self.client, mobile, role)
        self.state["mobileVerifications"][role] = {
            "mobile": mobile,
            "messageId": message_id,
            "verified": False,
            "sentAt": time.time(),
        }
        self.state["revision"] += 1
        return {"status": "verification_code_sent"}

    def verify_code(self, role, code):
        mobile = self.code_recipient(role)
        verification = self.state["mobileVerifications"].get(role)
        if not verification or verification["mobile"] != mobile:
            raise ValueError("请先获取当前手机号的验证码")
        check_mobile_verification_code(self.client, mobile, code, role)
        verification["verified"] = True
        self.state["revision"] += 1
        return {"status": "mobile_verified"}

    def preview(self):
        status = public_state(self.state)
        if not status.get("readyForPreview"):
            raise ValueError(
                "申请信息或校验尚未完成：" + ", ".join(status.get("missing", []))
            )
        return _preview(self.state)

    def submit(self, expected_revision):
        if self.state["revision"] != expected_revision:
            raise ValueError("材料已变化，请重新生成并确认预览")
        self.preview()
        try:
            result = create_signature_qualification(
                self.client, _submission_payload(self.state)
            )
        except QualificationUploadError as error:
            if error.outcome_unknown:
                self.state.update(
                    done=True,
                    result={
                        "status": "qualification_submission_outcome_unknown",
                        "outcomeUnknown": True,
                        "requestId": error.request_id,
                        "logId": error.log_id,
                    },
                )
            raise
        self.state.update(done=True, result={**result, "revision": expected_revision})
        return result


def _text(value: Any, *, maximum: int = 256) -> str:
    if not isinstance(value, str):
        raise ValueError("文本字段需要字符串")
    if not value or value.isspace() or len(value) > maximum:
        raise ValueError("文本字段不能为空或超过允许长度")
    return value


def _optional_text(value: Any, *, maximum: int = 256) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError
    if len(value) > maximum:
        raise ValueError
    return value


def _date(value: Any) -> str:
    value = _text(value, maximum=10)
    try:
        parsed = datetime.date.fromisoformat(value)
    except ValueError:
        raise ValueError("有效期需要 YYYY-MM-DD 格式") from None
    if parsed.isoformat() != value:
        raise ValueError("有效期需要 YYYY-MM-DD 格式")
    return value


def _id_card(value: Any, *, required: bool = True) -> str:
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise ValueError
    if not value and (not required):
        return ""
    if not re.fullmatch("[0-9]{17}[0-9X]", value):
        raise ValueError
    return value


def _mobile(value: Any, *, required: bool) -> str:
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise ValueError
    if value and (not re.fullmatch("1[3-9][0-9]{9}", value)):
        raise ValueError
    if required and (not value):
        raise ValueError
    return value


def _person_requirement(rank: Mapping[str, Any], role: str, kind: str) -> bool:
    """Return the deterministic fields required before a role can be saved."""
    if kind not in ("image", "mobile"):
        raise ValueError
    if role == "legal":
        return False
    if role not in ("operator", "responsible"):
        raise ValueError
    prefix = "Operator" if role == "operator" else "Responsible"
    if kind == "image":
        return bool(rank.get("need" + prefix + "Image"))
    return bool(rank.get(role + "ThreeElement") or rank.get("need" + prefix + "Mobile"))


def _legal_person_name(business: Any, submitted: Any) -> str:
    """Keep the business certificate as the sole source of the legal name."""
    if not isinstance(business, Mapping):
        raise QualificationUploadError(
            "business_info_required", "请先保存营业证件信息。"
        )
    expected = _text(business.get("legalPersonName"))
    try:
        actual = _text(submitted)
    except ValueError as error:
        raise QualificationUploadError(
            "legal_name_mismatch", "法人姓名必须与营业证件一致。"
        ) from error
    if actual != expected:
        raise QualificationUploadError(
            "legal_name_mismatch", "法人姓名必须与营业证件一致。"
        )
    return expected


def _public_check(state: Mapping[str, Any], target: str) -> Dict[str, Any]:
    check = state.get("checks", {}).get(target)
    if not isinstance(check, Mapping):
        return {"attempted": False, "matched": False, "canContinue": False}
    return {
        "attempted": True,
        "matched": bool(check.get("matched")),
        "canContinue": bool(check.get("canContinue")),
        "status": normalize_check_status(check.get("status")),
        "forceSkip": check.get("ticket") == BUSINESS_CHECK_SKIP_TICKET,
    }


def _verification_params(state: Mapping[str, Any], target: str) -> Dict[str, Any]:
    sections = state["sections"]
    if target == "business":
        business = sections.get("business")
        if not isinstance(business, Mapping):
            raise QualificationUploadError(
                "qualification_check_required", "请先保存营业证件信息。"
            )
        return {
            "businessCertificateName": business["businessCertificateName"],
            "unifiedSocialCreditIdentifier": business["unifiedSocialCreditIdentifier"],
            "legalPersonName": business["legalPersonName"],
        }
    if target not in ("legal", "operator", "responsible"):
        raise QualificationUploadError(
            "qualification_check_invalid", "不支持当前信息校验。"
        )
    if target == "responsible" and state.get("sameOperator") is True:
        raise QualificationUploadError(
            "qualification_check_not_needed", "责任人与经办人相同，无需重复校验。"
        )
    person = sections.get(target)
    if not isinstance(person, Mapping):
        raise QualificationUploadError(
            "qualification_check_required",
            "请先保存{}信息。".format(PERSON_LABELS[target]),
        )
    mobile_required = target != "legal" and bool(
        state["rank"].get(target + "ThreeElement")
    )
    return {
        "personName": person["personName"],
        "personIDCard": person["personIDCard"],
        "personMobile": person["personMobile"] if mobile_required else "",
    }


def _has_identity_image_pair(section: Any) -> bool:
    if not isinstance(section, Mapping):
        return False
    image_uris = section.get("imageUris")
    return isinstance(image_uris, Mapping) and bool(
        image_uris.get("front") and image_uris.get("back")
    )


def _mobile_verification_needed(state: Mapping[str, Any], role: str) -> bool:
    if not state.get("mobileVerificationRequired"):
        return False
    person = state.get("sections", {}).get(role)
    return isinstance(person, Mapping) and bool(person.get("personMobile"))


def _mobile_verified(state: Mapping[str, Any], role: str) -> bool:
    if role == "responsible" and state.get("sameOperator") is True:
        role = "operator"
    if not _mobile_verification_needed(state, role):
        return True
    person = state.get("sections", {}).get(role)
    verification = state.get("mobileVerifications", {}).get(role)
    return bool(
        isinstance(person, Mapping)
        and isinstance(verification, Mapping)
        and (verification.get("verified") is True)
        and (verification.get("mobile") == person.get("personMobile"))
    )


def _person_payload(section: Mapping[str, Any], role: str) -> Dict[str, Any]:
    front_type, back_type = PERSON_FILE_TYPES[role]
    certificate_type = int(section.get("certificateType") or 0)
    payload = {
        "certificateType": certificate_type,
        "personCertificate": [],
        "personName": section["personName"],
        "personIDCard": section["personIDCard"],
        "personMobile": section["personMobile"],
    }
    uris = section.get("imageUris")
    suffixes = section.get("imageSuffixes")
    if isinstance(uris, Mapping) and isinstance(suffixes, Mapping):
        payload["personCertificate"] = [
            {
                "fileType": front_type,
                "fileContent": uris["front"],
                "fileSuffix": suffixes["front"],
            },
            {
                "fileType": back_type,
                "fileContent": uris["back"],
                "fileSuffix": suffixes["back"],
            },
        ]
    documents = section.get("documents")
    if (
        role == "legal"
        and certificate_type in LEGAL_DOCUMENT_FILE_TYPES
        and isinstance(documents, list)
    ):
        payload["personCertificate"] = [
            {
                "fileType": LEGAL_DOCUMENT_FILE_TYPES[certificate_type],
                "fileContent": item["imageUri"],
                "fileSuffix": item["imageSuffix"],
            }
            for item in documents
            if isinstance(item, Mapping)
            and item.get("imageUri")
            and item.get("imageSuffix")
        ]
    return payload


def _submission_payload(state: Mapping[str, Any]) -> Dict[str, Any]:
    sections = state["sections"]
    business = sections["business"]
    checks = state["checks"]
    operator_ticket = checks["operator"]["ticket"]
    responsible_ticket = (
        operator_ticket
        if state.get("sameOperator") is True
        else checks["responsible"]["ticket"]
    )
    payload: Dict[str, Any] = {
        "id": 0,
        "purpose": state["purpose"],
        "materialName": state["materialName"],
        "businessInfo": {
            "businessCertificateType": business["businessCertificateType"],
            "businessCertificate": {},
            "businessCertificateName": business["businessCertificateName"],
            "unifiedSocialCreditIdentifier": business["unifiedSocialCreditIdentifier"],
            "businessCertificateValidityPeriodStart": business[
                "businessCertificateValidityPeriodStart"
            ],
            "businessCertificateValidityPeriodEnd": business[
                "businessCertificateValidityPeriodEnd"
            ],
            "legalPersonName": business["legalPersonName"],
        },
        "operatorPerson": _person_payload(sections["operator"], "operator"),
        "responsiblePersonInfo": _person_payload(
            sections["operator"]
            if state.get("sameOperator") is True
            else sections["responsible"],
            "responsible",
        ),
        "powerOfAttorney": [],
        "otherMaterials": [],
        "effectSignatures": [],
        "from": "vconsole",
        "sameOperator": state.get("sameOperator") is True,
        "businessCheckTicket": checks["business"]["ticket"],
        "operatorCheckTicket": operator_ticket,
        "responsibleCheckTicket": responsible_ticket,
    }
    legal = sections.get("legal")
    if isinstance(legal, Mapping):
        payload["legalPerson"] = _person_payload(legal, "legal")
        legal_check = checks.get("legal")
        if isinstance(legal_check, Mapping) and legal_check.get("ticket"):
            payload["legalCheckTicket"] = legal_check["ticket"]
    if business.get("imageUri"):
        payload["businessInfo"]["businessCertificate"] = {
            "fileType": business["businessCertificateType"],
            "fileContent": business["imageUri"],
            "fileSuffix": business["imageSuffix"],
        }
    other_materials = sections.get("otherMaterials")
    if isinstance(other_materials, list):
        payload["otherMaterials"] = [
            {
                "fileType": 6,
                "fileContent": item["imageUri"],
                "fileSuffix": item["imageSuffix"],
            }
            for item in other_materials
            if isinstance(item, Mapping)
            and item.get("imageUri")
            and item.get("imageSuffix")
        ]
    rank = state["rank"]
    if state["purpose"] == 2:
        payload["authorizer"] = business["businessCertificateName"]
        payload["authorizee"] = state["authorizee"]
    if state["purpose"] == 2 and rank.get("needOtherUseCheck"):
        power = sections["powerOfAttorney"]
        payload["powerOfAttorney"] = [
            {
                "fileType": 5,
                "fileContent": power["imageUri"],
                "fileSuffix": power["imageSuffix"],
            }
        ]
    return payload


def _preview(state: Mapping[str, Any]) -> Dict[str, Any]:
    sections = state["sections"]
    business = sections["business"]
    people = {}
    for role in PERSON_FILE_TYPES:
        if role == "responsible" and state.get("sameOperator") is True:
            person = sections.get("operator")
        else:
            person = sections.get(role)
        if isinstance(person, Mapping):
            people[role] = {
                "label": PERSON_LABELS[role],
                "personName": person["personName"],
                "personIDCard": person["personIDCard"],
                "personMobile": person["personMobile"],
                "reusedFromOperator": bool(
                    role == "responsible" and state.get("sameOperator") is True
                ),
            }
    return {
        "revision": state["revision"],
        "materialName": state["materialName"],
        "purpose": "他用" if state["purpose"] == 2 else "自用",
        "powerOfAttorney": "已提供" if "powerOfAttorney" in sections else "无需提供",
        "authorization": {
            "authorizer": business["businessCertificateName"],
            "authorizee": state["authorizee"],
            "otherMaterialCount": len(sections.get("otherMaterials") or []),
        }
        if state["purpose"] == 2
        else None,
        "business": {
            key: business[key]
            for key in (
                "businessCertificateName",
                "unifiedSocialCreditIdentifier",
                "legalPersonName",
                "businessCertificateValidityPeriodStart",
                "businessCertificateValidityPeriodEnd",
            )
        },
        "people": people,
        "checks": {
            "business": "通过"
            if state["checks"]["business"]["matched"]
            else "未通过自动校验，将转人工审核",
            "legal": "通过"
            if state.get("checks", {}).get("legal", {}).get("matched")
            else "无需校验",
            "operator": "通过",
            "responsible": "同经办人，复用经办人校验"
            if state.get("sameOperator") is True
            else "通过",
        },
    }
