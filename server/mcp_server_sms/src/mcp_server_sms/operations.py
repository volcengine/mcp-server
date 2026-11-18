"""引流录入的类型化请求；服务开通由专用页面流程负责。"""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .models import ApiModel, Text


class TrafficLink(ApiModel):
    use_volc_link: bool = Field(alias="useVolcLink", strict=True)
    protocol: Literal["http", "https", "缺省"] | None = None
    link: str | None = None
    link_domain_icp: str | None = Field(None, alias="linkDomainIcp")
    link_domain_icp_body: str | None = Field(None, alias="linkDomainIcpBody")
    link_domain: str | None = Field(None, alias="linkDomain")
    link_path: str | None = Field(None, alias="linkPath")
    jump_link: str | None = Field(None, alias="jumpLink")
    jump_link_domain_icp: str | None = Field(None, alias="jumpLinkDomainIcp")
    jump_link_domain_icp_body: str | None = Field(None, alias="jumpLinkDomainIcpBody")
    jump_link_domain: str | None = Field(None, alias="jumpLinkDomain")
    jump_link_path: str | None = Field(None, alias="jumpLinkPath")

    @model_validator(mode="after")
    def require_link(self):
        required = (
            (self.jump_link, self.jump_link_domain_icp, self.jump_link_domain_icp_body)
            if self.use_volc_link
            else (self.protocol, self.link, self.link_domain_icp, self.link_domain_icp_body)
        )
        if not all(required):
            raise ValueError("需要完整的链接和域名备案信息")
        return self


class TrafficPhone(ApiModel):
    number_type: Literal[1, 2, 3, 4, 5, 6, 7] = Field(alias="numberType")
    number: Text = Field(repr=False)
    company: str | None = None
    number_province: str | None = Field(None, alias="numberProvince")
    number_city: str | None = Field(None, alias="numberCity")
    number_person: str | None = Field(None, alias="numberPerson", repr=False)
    person_type: Literal[0, 1] | None = Field(None, alias="personType")
    person_id: str | None = Field(None, alias="personId", repr=False)

    @model_validator(mode="after")
    def validate_identity_kind(self):
        if self.number_type == 1 and self.company:
            raise ValueError("手机号不填写所属企业")
        if self.number_type != 1 and any((self.number_person, self.person_type, self.person_id)):
            raise ValueError("非手机号不填写个人证件信息")
        return self


class TrafficLinks(ApiModel):
    data: Annotated[list[TrafficLink], Field(min_length=1, max_length=10)]


class TrafficPhones(ApiModel):
    data: Annotated[list[TrafficPhone], Field(min_length=1, max_length=100)]


class RegisterLinksRequest(ApiModel):
    action: Literal["BulkCreateTobTrafficDrivingLinkForAgent"]
    params: TrafficLinks


class RegisterPhonesRequest(ApiModel):
    action: Literal["BulkCreateTobTrafficDrivingPhoneForAgent"]
    params: TrafficPhones


TrafficRegistration = Annotated[
    RegisterLinksRequest | RegisterPhonesRequest, Field(discriminator="action")
]
