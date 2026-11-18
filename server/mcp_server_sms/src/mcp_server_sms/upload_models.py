"""表单上传的有界输入与内部凭据契约；文件内容不会进入普通工具结果。"""

from typing import Annotated, Literal

from pydantic import Field, SecretStr

from .configuration import FORM_CONFIG
from .models import ApiModel, Text
from .responses import ApiResult

MAX_UPLOAD_BYTES = FORM_CONFIG["maxUploadBytes"]
MAX_UPLOAD_ENCODED_LENGTH = ((MAX_UPLOAD_BYTES + 2) // 3) * 4
MaterialCategory = Literal["identity", "business", "authorization", "other", "app", "trademark"]


class FileContent(ApiModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    data: Annotated[str, Field(min_length=1, max_length=MAX_UPLOAD_ENCODED_LENGTH)] = Field(
        repr=False, description="原始文件字节的 Base64 编码；不接受本地路径或 URL"
    )




class MaterialUploadMetadata(ApiModel):
    """MaterialUploadMetadata 仅传输原文件元信息，不携带文件内容。"""

    name: Annotated[str, Field(min_length=1, max_length=255)]
    category: MaterialCategory
    size: Annotated[int, Field(strict=True, gt=0, le=MAX_UPLOAD_BYTES)]
    crc32: Annotated[str, Field(pattern=r"^[0-9a-f]{8}$")]


class MaterialUploadContext(ApiModel):
    """MaterialUploadContext 绑定一次已申请的上传会话，由凭据签名后交给表单。"""

    name: Annotated[str, Field(min_length=1, max_length=255)]
    suffix: Annotated[str, Field(min_length=1, max_length=5)]
    uri: Annotated[str, Field(min_length=1, max_length=4096)] = Field(repr=False)
    session_key: Annotated[str, Field(min_length=1, max_length=8192)] = Field(repr=False)
    expires_at: Annotated[int, Field(strict=True, gt=0)]


class MaterialUploadConfirmation(ApiModel):
    """MaterialUploadConfirmation 验证当前登录凭据与上传会话，避免跨账号或篡改后确认。"""

    context: MaterialUploadContext = Field(repr=False)
    signature: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")] = Field(repr=False)


class RecipientsUploadMetadata(ApiModel):
    """RecipientsUploadMetadata 以大小和摘要绑定所选名单，正文不进入工具参数。"""

    name: Annotated[str, Field(min_length=1, max_length=255)]
    size: Annotated[int, Field(strict=True, gt=0, le=MAX_UPLOAD_BYTES)]
    sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
    sub_account: Text
    template_id: Text


class RecipientsUploadContext(RecipientsUploadMetadata):
    """RecipientsUploadContext 只接受本次账号申请的文件 Key，不接受调用方提供下载地址。"""

    file: Annotated[str, Field(min_length=1, max_length=4096)] = Field(repr=False)
    expires_at: Annotated[int, Field(strict=True, gt=0)]


class RecipientsUploadConfirmation(ApiModel):
    context: RecipientsUploadContext = Field(repr=False)
    signature: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")] = Field(repr=False)






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
    """SmsRequestError 保留调用边界返回的原始失败结果。"""

    def __init__(self, result: dict):
        self.result = result
        super().__init__(result["error"]["message"])
