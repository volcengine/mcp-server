"""Request schemas for SMS APIs, without drafts or client interaction state."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

Channel = Literal["CN_OTP", "CN_NTC", "CN_MKT"]
BatchChannel = Literal["CN_NTC", "CN_MKT"]
Mobile = Annotated[str, Field(pattern=r"^1[3-9][0-9]{9}$")]
Text = Annotated[str, Field(min_length=1)]


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, hide_input_in_errors=True)

    def payload(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class MaterialFile(ApiModel):
    file_type: int = Field(alias="fileType", ge=0, le=19)
    file_content: str = Field(
        alias="fileContent", repr=False, description="短信材料接口接受的文件引用；不是 MCP fileId"
    )
    file_suffix: str | None = Field(None, alias="fileSuffix")


class BusinessInfo(ApiModel):
    business_certificate_type: Literal[1, 4, 6, 7] = Field(alias="businessCertificateType")
    business_certificate_name: Text = Field(alias="businessCertificateName")
    unified_social_credit_identifier: Text = Field(
        alias="unifiedSocialCreditIdentifier", repr=False
    )
    legal_person_name: Text = Field(alias="legalPersonName", repr=False)
    business_certificate: MaterialFile | None = Field(None, alias="businessCertificate")
    validity_start: str = Field(alias="businessCertificateValidityPeriodStart")
    validity_end: str = Field(alias="businessCertificateValidityPeriodEnd")


class PersonInfo(ApiModel):
    certificate_type: Literal[0, 1, 2, 3, 4, 9] = Field(alias="certificateType")
    person_name: str = Field(alias="personName", repr=False)
    person_id_card: str = Field(alias="personIDCard", repr=False)
    person_mobile: str | None = Field(None, alias="personMobile", repr=False)
    person_certificate: list[MaterialFile] | None = Field(
        None, alias="personCertificate", repr=False
    )


class QualificationApplication(ApiModel):
    purpose: Literal[1, 2]
    material_name: str = Field(alias="materialName", min_length=1, max_length=20)
    business_info: BusinessInfo = Field(alias="businessInfo")
    operator_person: PersonInfo = Field(alias="operatorPerson")
    responsible_person_info: PersonInfo = Field(alias="responsiblePersonInfo")
    same_operator: bool = Field(alias="sameOperator")
    business_check_ticket: str | None = Field(None, alias="businessCheckTicket", repr=False)
    operator_check_ticket: str | None = Field(None, alias="operatorCheckTicket", repr=False)
    responsible_check_ticket: str | None = Field(None, alias="responsibleCheckTicket", repr=False)
    legal_person: PersonInfo | None = Field(None, alias="legalPerson")
    legal_check_ticket: str | None = Field(None, alias="legalCheckTicket", repr=False)
    power_of_attorney: list[MaterialFile] | None = Field(None, alias="powerOfAttorney")
    other_materials: list[MaterialFile] | None = Field(None, alias="otherMaterials")
    effect_signatures: list[str] | None = Field(None, alias="effectSignatures")
    authorizer: str | None = None
    authorizee: str | None = None


class AppIcp(ApiModel):
    app_icp_filling: str = Field(alias="appIcpFilling")


class Trademark(ApiModel):
    trademark_cn: str | None = Field(None, alias="trademarkCn")
    trademark_en: str | None = Field(None, alias="trademarkEn")
    trademark_number: str | None = Field(None, alias="trademarkNumber")


class SignatureApplication(ApiModel):
    content: Text
    purpose: Literal[1, 2]
    qualification_id: int = Field(alias="signatureIdentificationID", gt=0)
    source: int
    sub_accounts: list[str] | None = Field(None, alias="subAccounts")
    channel_types: list[Channel] | None = Field(None, alias="channelTypes")
    description: str | None = Field(None, alias="desc")
    domain: str | None = None
    scene: str | None = None
    project_name: str | None = Field(None, alias="projectName")
    app_icp: AppIcp | None = Field(None, alias="appIcp")
    trademark: Trademark | None = None


class TemplateParameter(ApiModel):
    name: Text


class ShortUrlConfig(ApiModel):
    is_enabled: str | None = Field(None, alias="isEnabled")
    belong: str | None = None
    is_need_click_details: str | None = Field(None, alias="isNeedClickDetails")
    ua_check_strategy: int | None = Field(None, alias="uaCheckStrategy")


class TemplateApplication(ApiModel):
    name: Text
    content: Text
    channel_type: Channel = Field(alias="channelType")
    area: Literal["cn"] = "cn"
    signatures: list[str] | None = None
    sub_accounts: list[str] | None = Field(None, alias="subAccounts")
    template_params: list[TemplateParameter] | None = Field(None, alias="templateParams")
    description: str | None = Field(None, alias="desc")
    project: str | None = None
    short_url_config: ShortUrlConfig | None = Field(None, alias="shortUrlConfig")


class BatchTask(ApiModel):
    sub_account: Text = Field(alias="subAccount")
    name: Text
    signature: Text
    template_id: Text = Field(alias="templateId")
    template_name: str = Field(alias="templateName")
    channel_type: BatchChannel = Field(alias="channelType")
    file_url: Text = Field(alias="fileUrl", description="GetUploadTosURL 返回的 file 对象 Key")
    scheduled: bool
    send_time: int = Field(
        alias="sendTime",
        ge=0,
        description="短信 API 的发送时间；立即发送传 0，定时发送使用 Unix 秒",
    )
    extra: dict | None = None
