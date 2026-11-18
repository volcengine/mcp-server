"""国内短信补充查询契约；只允许明确列出的只读 Action。"""

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .models import ApiModel, Channel, Text

Page = Annotated[int, Field(ge=1)]
PageSize = Annotated[int, Field(ge=1, le=100)]
ResourceId = Annotated[int, Field(gt=0)]


class MessageGroupsQuery(ApiModel):
    page_index: Page = Field(1, alias="pageIndex")
    page_size: PageSize = Field(20, alias="pageSize")
    sub_account_name: str | None = Field(None, alias="subAccountName")
    sub_account: str | None = Field(None, alias="subAccount")
    project: str | None = None
    all_status: bool | None = Field(None, alias="allStatus")


class SignatureQualificationsQuery(ApiModel):
    purpose: Literal[0, 1, 2] | None = None


class SignatureDetailsQuery(ApiModel):
    signature: str | None = Field(None, alias="Signature")
    exact_match: bool | None = Field(None, alias="ExactMatch")
    project_name: str | None = Field(None, alias="ProjectName")
    sub_accounts: list[str] | None = Field(None, alias="SubAccounts")
    channel_types: list[Channel] | None = Field(None, alias="ChannelTypes")
    industries: list[str] | None = Field(None, alias="Industries")
    statuses: list[int] | None = Field(None, alias="Statuses")
    page: Page = Field(1, alias="Page")
    page_size: PageSize = Field(20, alias="PageSize")


class BatchTemplatesQuery(ApiModel):
    template_id: str | None = Field(None, alias="TemplateId")
    signatures: list[str] | None = Field(None, alias="Signatures")
    sub_accounts: list[str] | None = Field(None, alias="SubAccounts")
    page: Page = Field(1, alias="Page")
    page_size: PageSize = Field(20, alias="PageSize")


class TrafficLinksQuery(ApiModel):
    id: ResourceId | None = None
    link: str | None = None
    jump_link: str | None = Field(None, alias="jumpLink")
    use_volc_link: bool | None = Field(None, alias="useVolcLink")


class TrafficPhonesQuery(ApiModel):
    id: ResourceId | None = None
    number: str | None = None


class RelatedTemplatesQuery(ApiModel):
    signature: str | None = None
    number: str | None = None
    link: str | None = None
    jump_link: str | None = Field(None, alias="jumpLink")

    @model_validator(mode="after")
    def require_filter(self):
        if not any((self.signature, self.number, self.link, self.jump_link)):
            raise ValueError("关联模板查询至少需要签名、号码或链接之一")
        return self


class TrafficContentQuery(ApiModel):
    content: Text = Field(repr=False, description="已填完变量的实际正文")
    use_volc_link: bool | None = Field(None, alias="useVolcLink")


class ThirdTemplatesQuery(ApiModel):
    second_template_id: Text = Field(alias="secondTemplateId")
    phone_id: ResourceId | None = Field(None, alias="phoneId")
    link_id: ResourceId | None = Field(None, alias="linkId")
    sub_content_id: ResourceId | None = Field(None, alias="subContentId")


class ReportStatusQuery(ApiModel):
    signature: Text = Field(alias="Signature")
    channel_type: Channel = Field(alias="ChannelType")
    industry: Text = Field(alias="Industry")
    sub_account: str | None = Field(None, alias="SubAccount")
    template_id: str | None = Field(None, alias="TemplateId")
    content: str | None = Field(None, alias="Content", repr=False)
    carrier: Literal["中国移动", "中国联通", "中国电信"] | None = Field(None, alias="Carrier")


class BatchContentQuery(ApiModel):
    sub_account: Text = Field(alias="subAccount")
    signature: Text
    template_id: Text = Field(alias="templateId")
    content: str | None = Field(None, repr=False)


class MessageGroupsRequest(ApiModel):
    action: Literal["GetSubAccountListForAgent"]
    params: MessageGroupsQuery


class SignatureQualificationsRequest(ApiModel):
    action: Literal["GetApplySignatureBind"]
    params: SignatureQualificationsQuery


class SignatureDetailsRequest(ApiModel):
    action: Literal["ListSignaturesForAgent"]
    params: SignatureDetailsQuery


class BatchTemplatesRequest(ApiModel):
    action: Literal["ListBatchTemplatesForAgent"]
    params: BatchTemplatesQuery


class TrafficLinksRequest(ApiModel):
    action: Literal["GetTobTrafficDrivingLinkListForAgent"]
    params: TrafficLinksQuery


class TrafficPhonesRequest(ApiModel):
    action: Literal["GetTobTrafficDrivingPhoneListForAgent"]
    params: TrafficPhonesQuery


class RelatedTemplatesRequest(ApiModel):
    action: Literal["ListRelationTemplateForAgent"]
    params: RelatedTemplatesQuery


class TrafficContentRequest(ApiModel):
    action: Literal["CheckTrafficDrivingExist"]
    params: TrafficContentQuery


class ThirdTemplatesRequest(ApiModel):
    action: Literal["ListThirdTemplate"]
    params: ThirdTemplatesQuery


class ReportStatusRequest(ApiModel):
    action: Literal["AgentGetSignatureTemplateReportStatus"]
    params: ReportStatusQuery


class BatchContentRequest(ApiModel):
    action: Literal["ValidateBatchTaskContentForAgent"]
    params: BatchContentQuery


class MessageGroupDetailQuery(ApiModel):
    sub_account: Text = Field(alias="subAccount")


class MessageGroupDetailRequest(ApiModel):
    action: Literal["GetSubAccountDetail"]
    params: MessageGroupDetailQuery


ResourceQuery = Annotated[
    MessageGroupsRequest | MessageGroupDetailRequest
    | SignatureQualificationsRequest
    | SignatureDetailsRequest
    | BatchTemplatesRequest
    | TrafficLinksRequest
    | TrafficPhonesRequest
    | RelatedTemplatesRequest
    | TrafficContentRequest
    | ThirdTemplatesRequest
    | ReportStatusRequest
    | BatchContentRequest,
    Field(discriminator="action"),
]


class BatchTaskReference(ApiModel):
    sub_account: Text = Field(alias="subAccount")
    task_id: Text = Field(alias="taskId")


class BatchTaskListQuery(ApiModel):
    sub_account: str | None = Field(None, alias="subAccount")
    task_name: str | None = Field(None, alias="taskName")
    signature: str | None = None
    template_id: str | None = Field(None, alias="templateId")
    page: Page = Field(1, alias="pageIndex")
    page_size: PageSize = Field(20, alias="pageSize")


class BatchTaskDetailRequest(ApiModel):
    action: Literal["GetBatchTaskDetail"]
    params: BatchTaskReference


class BatchTaskListRequest(ApiModel):
    action: Literal["GetBatchTaskList"]
    params: BatchTaskListQuery


BatchTaskQuery = Annotated[
    BatchTaskDetailRequest | BatchTaskListRequest, Field(discriminator="action")
]
