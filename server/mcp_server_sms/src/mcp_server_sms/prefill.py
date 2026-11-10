"""宿主 Agent 的表单草稿，只接收可编辑字段，不接收校验或提交结果。"""

from collections.abc import Iterable
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .models import ApiModel, Text
from .upload_models import MAX_UPLOAD_ENCODED_LENGTH, FileContent

MaterialDrafts = Annotated[list[FileContent], Field(max_length=5)]


def _check_attachment_budget(files: Iterable[FileContent | None]) -> None:
    # 单次开表的附件总量沿用一次上传的预算；超过时由用户在表单内分次上传。
    if sum(len(file.data) for file in files if file is not None) > MAX_UPLOAD_ENCODED_LENGTH:
        raise ValueError("预填附件总量超过单次上传上限")


class BusinessPrefill(ApiModel):
    business_certificate_type: Literal[1, 4, 6, 7] | None = Field(
        None, alias="businessCertificateType"
    )
    business_certificate_name: str | None = Field(None, alias="businessCertificateName")
    unified_social_credit_identifier: str | None = Field(
        None, alias="unifiedSocialCreditIdentifier", repr=False
    )
    legal_person_name: str | None = Field(None, alias="legalPersonName", repr=False)
    validity_start: str | None = Field(None, alias="businessCertificateValidityPeriodStart")
    validity_end: str | None = Field(None, alias="businessCertificateValidityPeriodEnd")
    business_certificate: FileContent | None = Field(
        None, alias="businessCertificate", repr=False
    )


class IdentityImagesPrefill(ApiModel):
    front: FileContent | None = None
    back: FileContent | None = None


class LegalImagesPrefill(IdentityImagesPrefill):
    document: FileContent | None = None


class PersonPrefill(ApiModel):
    person_name: str | None = Field(None, alias="personName", repr=False)
    person_id_card: str | None = Field(None, alias="personIDCard", repr=False)
    person_mobile: str | None = Field(None, alias="personMobile", repr=False)
    person_certificate: IdentityImagesPrefill | None = Field(
        None, alias="personCertificate", repr=False
    )


class LegalPersonPrefill(PersonPrefill):
    certificate_type: Literal[0, 1, 2, 3, 4, 9] | None = Field(None, alias="certificateType")
    person_certificate: LegalImagesPrefill | None = Field(
        None, alias="personCertificate", repr=False
    )


class QualificationFormPrefill(ApiModel):
    purpose: Literal[1, 2] | None = None
    material_name: str | None = Field(None, alias="materialName", max_length=20)
    business_info: BusinessPrefill | None = Field(None, alias="businessInfo")
    operator_person: PersonPrefill | None = Field(None, alias="operatorPerson", repr=False)
    responsible_person: PersonPrefill | None = Field(None, alias="responsiblePersonInfo", repr=False)
    same_operator: bool | None = Field(None, alias="sameOperator", strict=True)
    include_legal: bool | None = Field(None, alias="includeLegal", strict=True)
    legal_person: LegalPersonPrefill | None = Field(None, alias="legalPerson", repr=False)
    power_of_attorney: Annotated[list[FileContent], Field(max_length=1)] | None = Field(
        None, alias="powerOfAttorney", repr=False
    )
    other_materials: MaterialDrafts | None = Field(None, alias="otherMaterials", repr=False)

    @model_validator(mode="after")
    def check_attachment_budget(self):
        attachments = [
            self.business_info.business_certificate if self.business_info else None,
            *(self.power_of_attorney or []),
            *(self.other_materials or []),
        ]
        for person in (self.operator_person, self.responsible_person, self.legal_person):
            if person and person.person_certificate:
                attachments.extend((person.person_certificate.front, person.person_certificate.back))
        if self.legal_person and self.legal_person.person_certificate:
            attachments.append(self.legal_person.person_certificate.document)
        _check_attachment_budget(attachments)
        return self


class AppIcpPrefill(ApiModel):
    app_icp_filling: str | None = Field(None, alias="appIcpFilling")
    app_icp_file_list: MaterialDrafts | None = Field(None, alias="appIcpFileList", repr=False)


class TrademarkPrefill(ApiModel):
    trademark_cn: str | None = Field(None, alias="trademarkCn")
    trademark_en: str | None = Field(None, alias="trademarkEn")
    trademark_number: str | None = Field(None, alias="trademarkNumber")
    trademark_file_list: MaterialDrafts | None = Field(None, alias="trademarkFileList", repr=False)


class SignatureFormPrefill(ApiModel):
    content: str | None = Field(None, max_length=25)
    source: Literal[1, 2, 3] | None = None
    qualification_id: Annotated[int, Field(gt=0)] | None = Field(
        None, alias="signatureIdentificationID"
    )
    sub_accounts: list[Text] | None = Field(None, alias="subAccounts")
    is_limit_sub_account: Literal[0, 1] | None = Field(None, alias="isLimitSubAccount")
    description: str | None = Field(None, alias="desc")
    project_name: str | None = Field(None, alias="projectName")
    app_icp: AppIcpPrefill | None = Field(None, alias="appIcp")
    trademark: TrademarkPrefill | None = None
    upload_file_list: MaterialDrafts | None = Field(None, alias="uploadFileList", repr=False)

    @model_validator(mode="after")
    def check_attachment_budget(self):
        _check_attachment_budget([
            *(self.upload_file_list or []),
            *((self.app_icp.app_icp_file_list or []) if self.app_icp else []),
            *((self.trademark.trademark_file_list or []) if self.trademark else []),
        ])
        return self


class TrafficLinkPrefill(ApiModel):
    use_volc_link: bool | None = Field(None, alias="useVolcLink", strict=True)
    protocol: Literal["http", "https", "缺省"] | None = None
    link: str | None = None
    link_domain_icp: str | None = Field(None, alias="linkDomainIcp")
    link_domain_icp_body: str | None = Field(None, alias="linkDomainIcpBody")
    jump_link: str | None = Field(None, alias="jumpLink")
    jump_link_domain_icp: str | None = Field(None, alias="jumpLinkDomainIcp")
    jump_link_domain_icp_body: str | None = Field(None, alias="jumpLinkDomainIcpBody")


class TrafficPhonePrefill(ApiModel):
    number_type: Literal[1, 2, 3, 4, 5, 6, 7] | None = Field(None, alias="numberType")
    number: str | None = Field(None, repr=False)
    company: str | None = None
    number_province: str | None = Field(None, alias="numberProvince")
    number_city: str | None = Field(None, alias="numberCity")
    number_person: str | None = Field(None, alias="numberPerson", repr=False)
    person_type: Literal[0, 1] | None = Field(None, alias="personType")
    person_id: str | None = Field(None, alias="personId", repr=False)


class TrafficLinksPrefill(ApiModel):
    kind: Literal["link"]
    data: Annotated[list[TrafficLinkPrefill], Field(min_length=1, max_length=10)] | None = None


class TrafficPhonesPrefill(ApiModel):
    kind: Literal["phone"]
    data: Annotated[list[TrafficPhonePrefill], Field(min_length=1, max_length=100)] | None = None


TrafficFormPrefill = Annotated[TrafficLinksPrefill | TrafficPhonesPrefill, Field(discriminator="kind")]


class BatchFormPrefill(ApiModel):
    sub_account: Text | None = Field(None, alias="subAccount", description="已核实的启用消息组 ID")
    signature: Text | None = Field(None, description="该消息组下已核实的签名")
    template_id: Text | None = Field(None, alias="templateId", description="已核实的群发模板 ID")
    name: str | None = Field(None, description="任务名称")
    content: str | None = Field(None, repr=False, description="模板支持的任务级正文")
    check_traffic: bool | None = Field(None, alias="checkTraffic", strict=True)
    scheduled: bool | None = Field(None, strict=True, description="是否定时发送")
    send_time: int | None = Field(
        None, alias="sendTime", ge=0, le=253402271999,
        description="定时发送使用 Unix 秒，页面显示北京时间；立即发送可传 0",
    )
    recipients_file: FileContent | None = Field(
        None, alias="recipientsFile", repr=False, description="客户已授权使用的 CSV，待用户确认上传"
    )

    @model_validator(mode="after")
    def validate_schedule(self):
        if self.scheduled is False and self.send_time not in (None, 0):
            raise ValueError("立即发送不能指定定时时间")
        return self
