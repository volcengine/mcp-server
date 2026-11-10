"""表单上传的有界输入与内部凭据契约；文件内容不会进入普通工具结果。"""

from typing import Annotated, Literal

from pydantic import Field, SecretStr

from .configuration import FORM_CONFIG
from .models import ApiModel, Text
from .responses import ApiResult

MAX_UPLOAD_BYTES = FORM_CONFIG["maxUploadBytes"]
MAX_UPLOAD_ENCODED_LENGTH = ((MAX_UPLOAD_BYTES + 2) // 3) * 4


class FileContent(ApiModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    data: Annotated[str, Field(min_length=1, max_length=MAX_UPLOAD_ENCODED_LENGTH)] = Field(
        repr=False, description="原始文件字节的 Base64 编码；不接受本地路径或 URL"
    )


class MaterialUpload(FileContent):
    kind: Literal["material"]
    category: Literal["identity", "business", "authorization", "other", "app", "trademark"]


class RecipientsUpload(FileContent):
    kind: Literal["recipients"]
    sub_account: Text
    template_id: Text


FileUpload = Annotated[MaterialUpload | RecipientsUpload, Field(discriminator="kind")]


class MaterialToken(ApiResult):
    access_key: SecretStr = Field(alias="accessKeyId", repr=False, min_length=1)
    secret_key: SecretStr = Field(alias="secretAccessKey", repr=False, min_length=1)
    session_token: SecretStr = Field(alias="sessionToken", repr=False, min_length=1)


class MaterialAuthorization(ApiResult):
    token: MaterialToken = Field(repr=False)


class UploadStore(ApiResult):
    uri: Text = Field(alias="StoreUri")
    authorization: SecretStr = Field(alias="Auth", repr=False, min_length=1)


class UploadAddress(ApiResult):
    hosts: Annotated[list[Text], Field(min_length=1)] = Field(alias="UploadHosts")
    stores: Annotated[list[UploadStore], Field(min_length=1, max_length=1)] = Field(
        alias="StoreInfos"
    )
    session_key: SecretStr = Field(alias="SessionKey", repr=False, min_length=1)


class AppliedUpload(ApiResult):
    address: UploadAddress = Field(alias="UploadAddress")


class ApplyUploadResponse(ApiResult):
    result: AppliedUpload = Field(alias="Result")


class UploadedMaterial(ApiResult):
    code: Literal[2000]


class CommittedMaterial(ApiResult):
    uri: Text = Field(alias="Uri")
    status: Literal[2000] = Field(alias="UriStatus")


class CommittedUpload(ApiResult):
    results: Annotated[list[CommittedMaterial], Field(min_length=1, max_length=1)] = Field(
        alias="Results"
    )


class CommitUploadResponse(ApiResult):
    result: CommittedUpload = Field(alias="Result")


class SmsRequestError(Exception):
    """SmsRequestError 只保存已经脱敏的失败结果。"""

    def __init__(self, result: dict):
        self.result = result
        super().__init__(result["error"]["message"])
