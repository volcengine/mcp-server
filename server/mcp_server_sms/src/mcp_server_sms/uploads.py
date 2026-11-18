"""短信材料的浏览器直传授权与确认，以及原有服务端文件上传。"""

import csv
import hashlib
import hmac
import io
import json
import re
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from http.cookiejar import CookieJar
from pathlib import PurePath
from time import time
from urllib.parse import quote, urlencode, urlsplit

import httpx
from anyio import CapacityLimiter, WouldBlock
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials as ImageCredentials
from pydantic import ValidationError

from .auth import Credentials
from .client import SmsClient, _RejectCookies, failure
from .configuration import FORM_CONFIG
from .observability import observe_call
from .upload_models import (
    ApplyUploadResponse,
    CommitUploadResponse,
    MaterialToken,
    MaterialUploadConfirmation,
    MaterialUploadContext,
    MaterialUploadMetadata,
    RecipientsUploadConfirmation,
    RecipientsUploadContext,
    RecipientsUploadMetadata,
    SmsRequestError,
)

# 来自短信生产材料上传契约，与客户或部署账号无关；不是浏览器可覆盖的地址。
IMAGEX = FORM_CONFIG["materialUpload"]
# 使用当前服务的固定上传入口，配置首项为实际上传目标；不使用动态 UploadHosts。
# 来源：https://www.volcengine.com/docs/508/1537728

_MIME = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "pdf": "application/pdf",
    "zip": "application/zip",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
_MATERIAL_TYPES = {
    "business": {"png", "jpg", "jpeg"},
    "identity": {"png", "jpg", "jpeg"},
    "authorization": {"png", "jpg", "jpeg"},
    "other": {"png", "jpg", "jpeg", "gif", "doc", "docx", "zip"},
    "app": {"png", "jpg", "jpeg", "pdf", "zip"},
    "trademark": {"png", "jpg", "jpeg", "pdf", "zip"},
}


def upload_error(action, code, message, *, unknown=False):
    return SmsRequestError(failure(action, code, message, outcome_unknown=unknown))




def _check_recipient_columns(columns: list[str]) -> list[str]:
    """统一校验名单模板的列定义，保留原有列名及顺序。"""
    if (
        not columns or columns[0] != "phone"
        or not all(isinstance(column, str) and column for column in columns)
        or len(set(columns)) != len(columns)
    ):
        raise upload_error("ValidateRecipients", "invalid_csv_template", "名单模板表头不完整或包含重复列")
    return columns


def recipient_columns(demo: str) -> list[str]:
    """recipient_columns 读取实际名单模板，要求首列为 phone 且变量列唯一。"""
    try:
        columns = next(csv.reader(io.StringIO(demo.removeprefix("\ufeff")), strict=True))
    except (ValueError, csv.Error, StopIteration):
        raise upload_error("ValidateRecipients", "invalid_csv_template", "短信 API 返回的名单模板表头不完整") from None
    return _check_recipient_columns(columns)


def recipient_rows(data: bytes, expected: list[str]):
    """recipient_rows 按模板逐行读取，不改写原始号码或变量。"""
    try:
        rows = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True)
        if next(rows) != expected:
            raise ValueError("headers")
        count = 0
        for count, row in enumerate(rows, 1):
            if len(row) != len(expected) or re.fullmatch(r"1[3-9][0-9]{9}", row[0]) is None:
                raise ValueError("row")
            yield count + 1, row[0], dict(zip(expected[1:], row[1:], strict=True))
        if count == 0:
            raise ValueError("empty")
    except (ValueError, UnicodeError, csv.Error, StopIteration):
        raise upload_error(
            "ValidateRecipients",
            "invalid_csv",
            "名单格式不符合模板，请使用下载的 UTF-8 CSV 示例并检查号码和列数",
        ) from None


def validate_recipients(data: bytes, columns: list[str]) -> dict:
    """按照已核对的 CSV 列定义校验原文件，只统计重复号码，不修改或去重文件。"""
    count, phones, samples = 0, set(), []
    for _, phone, params in recipient_rows(data, columns):
        count += 1
        phones.add(phone)
        if len(samples) < 3:
            samples.append({"phone": phone[:3] + "****" + phone[-4:], "params": params})
    return {
        "columns": columns,
        "totalCount": count,
        "dupCount": count - len(phones),
        "samples": samples,
    }


class FileUploader:
    """FileUploader 复用短信凭据边界，只访问短信平台返回的上传位置。"""

    def __init__(self, api: SmsClient, *, transport: httpx.AsyncBaseTransport | None = None):
        self.api = api
        self._slots = CapacityLimiter(FORM_CONFIG["maxConcurrentUploads"])
        self.http = httpx.AsyncClient(
            transport=transport,
            timeout=60,
            follow_redirects=False,
            cookies=CookieJar(policy=_RejectCookies()),
        )

    async def __aenter__(self):
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.http.__aexit__(*args)



    async def _exchange(
        self,
        action,
        method,
        url,
        *,
        content=b"",
        headers=None,
        json_result=True,
        response_model=None,
    ):
        with observe_call("api", action) as observation:
            try:
                response = await self.http.request(method, url, content=content, headers=headers)
                if not response.is_success:
                    raise upload_error(
                        action,
                        "upload_http_error",
                        "文件上传服务未确认成功，请核对结果",
                        unknown=True,
                    )
                payload = response.json() if json_result else {}
                if not isinstance(payload, dict):
                    raise upload_error(
                        action, "invalid_upload_response", "上传响应格式不完整", unknown=True
                    )
                metadata = payload.get("ResponseMetadata", {})
                if not isinstance(metadata, dict) or metadata.get("Error"):
                    raise upload_error(
                        action, "upload_api_error", "文件上传服务返回错误，请核对结果", unknown=True
                    )
                if response_model is not None:
                    response_model.model_validate(payload)
            except (httpx.HTTPError, ValueError):
                result = failure(
                    action,
                    "upload_outcome_unknown",
                    "上传结果待确认，请勿自动重试",
                    outcome_unknown=True,
                )
                observation.record(result)
                raise SmsRequestError(result) from None
            except SmsRequestError as exc:
                observation.record(exc.result)
                raise
            observation.record({"success": True, "request_id": response.headers.get("x-tt-logid")})
            return payload

    async def _imagex(
        self, action, method, token: MaterialToken, params, body=None, *, response_model
    ):
        query = {
            "Action": action,
            "Version": "2018-08-01",
            "ServiceId": IMAGEX["serviceId"],
            **params,
        }
        encoded = (
            json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode()
            if body is not None
            else b""
        )
        request = AWSRequest(
            method=method,
            url=IMAGEX["endpoint"] + "?" + urlencode(query),
            data=encoded,
            headers={
                "Content-Type": "application/json"
                if method == "POST"
                else "application/x-www-form-urlencoded; charset=utf-8",
                "X-Amz-Content-Sha256": hashlib.sha256(encoded).hexdigest(),
                "X-Vod-Upload-AppID": IMAGEX["appId"],
                "X-Vod-Upload-UserID": IMAGEX["userId"],
            },
        )
        SigV4Auth(
            ImageCredentials(
                token.access_key.get_secret_value(),
                token.secret_key.get_secret_value(),
                token.session_token.get_secret_value(),
            ),
            "ImageX",
            IMAGEX["region"],
        ).add_auth(request)
        payload = await self._exchange(
            action,
            method,
            request.url,
            content=encoded,
            headers=dict(request.headers),
            response_model=response_model,
        )
        return payload["Result"]

    async def prepare_recipients(
        self, request: RecipientsUploadMetadata, credentials: Credentials
    ) -> dict:
        """prepare_recipients 申请账号专属的 TOS Key，向表单只返回该对象的 PUT 能力。"""
        if PurePath(request.name).suffix.lower() != ".csv":
            raise upload_error("prepare_recipients_upload", "invalid_file_type", "请选择 CSV 名单")
        authorized = await self.api.call("GetUploadTosURL", {"suffix": "csv"}, credentials)
        if not authorized["success"]:
            raise SmsRequestError(authorized)
        result = authorized["result"]
        _check_tos_url(result["url"])
        context = RecipientsUploadContext(
            **request.model_dump(), file=result["file"],
            expires_at=int(time()) + FORM_CONFIG["recipientsUpload"]["confirmationTtlSeconds"],
        )
        receipt = RecipientsUploadConfirmation(
            context=context, signature=_upload_signature(context, credentials, "recipients")
        )
        return {
            "upload": {"url": result["url"], "method": "PUT", "headers": {}},
            "confirmation": receipt.model_dump(),
        }

    @asynccontextmanager
    async def read_recipients(
        self, receipt: RecipientsUploadConfirmation, credentials: Credentials
    ):
        """read_recipients 验证账号票据，按短信服务返回的地址有界回读并核对原文件摘要。"""
        context = receipt.context
        if not hmac.compare_digest(
            receipt.signature, _upload_signature(context, credentials, "recipients")
        ):
            raise upload_error(
                "ReadRecipients", "upload_authorization_changed",
                "名单授权无效或登录已更新，请重新选择文件上传",
            )
        if int(time()) >= context.expires_at:
            raise upload_error("ReadRecipients", "upload_expired", "名单核对凭证已过期，请重新上传")
        try:
            self._slots.acquire_nowait()
        except WouldBlock:
            raise upload_error("ReadRecipients", "upload_busy", "当前文件核对较多，请稍后重试") from None
        try:
            authorized = await self.api.call(
                "GetFilePublicTosURL", {"fileName": context.file, "duration": 300}, credentials
            )
            if not authorized["success"]:
                raise SmsRequestError(authorized)
            if authorized["result"]["fileName"] != context.file:
                raise upload_error("ReadRecipients", "invalid_file_reference", "名单文件身份不一致")
            url = authorized["result"]["url"]
            _check_tos_url(url)
            # 槽位覆盖读取、统计和引流检查的整个消费期，避免缓冲返回后失去并发上限。
            yield await self._read_recipient_bytes(url, context)
        finally:
            self._slots.release()

    async def _read_recipient_bytes(self, url: str, context: RecipientsUploadContext) -> bytes:
        with observe_call("api", "ReadRecipients") as observation:
            try:
                async with self.http.stream("GET", url, headers={"Accept-Encoding": "identity"}) as response:
                    if not response.is_success:
                        raise upload_error(
                            "ReadRecipients", "upload_read_failed", "名单尚未能读取，请重新选择上传"
                        )
                    # 下载的是已校验摘要的原文件，禁止先解压再做大小检查造成内存放大。
                    if response.headers.get("content-encoding", "identity").lower() != "identity":
                        raise upload_error(
                            "ReadRecipients", "unexpected_content_encoding",
                            "名单响应包含不支持的压缩编码，请重新上传原始 CSV",
                        )
                    data = bytearray()
                    async for chunk in response.aiter_raw(chunk_size=65536):
                        if len(data) + len(chunk) > context.size:
                            raise upload_error(
                                "ReadRecipients", "invalid_file_size", "上传的名单大小与所选文件不一致"
                            )
                        data.extend(chunk)
                    if len(data) != context.size or hashlib.sha256(data).hexdigest() != context.sha256:
                        raise upload_error(
                            "ReadRecipients", "file_content_changed", "上传的名单与所选文件不一致，请重新上传"
                        )
            except httpx.HTTPError:
                error = upload_error("ReadRecipients", "upload_read_failed", "名单读取未完成，请稍后重试")
                observation.record(error.result)
                raise error from None
            except SmsRequestError as exc:
                observation.record(exc.result)
                raise
            observation.record({"success": True, "request_id": response.headers.get("x-tt-logid")})
            return bytes(data)

    @asynccontextmanager
    async def validated_recipients(
        self, receipt: RecipientsUploadConfirmation, credentials: Credentials, columns: list[str]
    ) -> AsyncIterator[tuple[bytes, dict]]:
        """validated_recipients 复用页面列定义，一次有界回读供名单统计和正文检查使用。"""
        columns = _check_recipient_columns(columns)
        async with self.read_recipients(receipt, credentials) as data:
            context = receipt.context
            counts = validate_recipients(data, columns)
            yield data, {
                "file": context.file, "name": context.name, **counts,
                "receipt": receipt.model_dump(),
            }

    async def prepare_material(
        self, request: MaterialUploadMetadata, credentials: Credentials
    ) -> dict:
        """prepare_material 申请单文件上传能力，原始凭据不离开服务端。"""
        suffix = PurePath(request.name).suffix[1:].lower()
        if suffix not in _MATERIAL_TYPES[request.category]:
            raise upload_error(
                "prepare_material_upload", "invalid_file_type", "此材料不支持所选文件类型"
            )
        try:
            self._slots.acquire_nowait()
        except WouldBlock:
            raise upload_error(
                "prepare_material_upload", "upload_busy", "当前上传较多，请稍后重新选择文件"
            ) from None
        try:
            token = await self.api.material_credentials(credentials)
            target = await self._apply_material(suffix, token)
            context = MaterialUploadContext(
                name=request.name, suffix=suffix, uri=target["uri"],
                session_key=target["session_key"],
                expires_at=int(time()) + IMAGEX["confirmationTtlSeconds"],
            )
            confirmation = MaterialUploadConfirmation(
                context=context, signature=_upload_signature(context, credentials, "material")
            )
            return {
                "upload": {
                    "url": target["url"], "method": "PUT",
                    "headers": {**target["headers"], "Content-CRC32": request.crc32},
                },
                "confirmation": confirmation.model_dump(),
            }
        except ValidationError:
            raise upload_error(
                "prepare_material_upload", "invalid_upload_address", "材料上传会话不完整"
            ) from None
        finally:
            self._slots.release()

    async def complete_material(
        self, request: MaterialUploadConfirmation, credentials: Credentials
    ) -> dict:
        """complete_material 按当前凭据核对短期票据，再向 ImageX 确认实际上传结果。"""
        context = request.context
        if not hmac.compare_digest(request.signature, _upload_signature(context, credentials, "material")):
            raise upload_error(
                "complete_material_upload", "upload_authorization_changed",
                "上传授权无效或登录已更新，请重新选择文件上传",
            )
        if int(time()) >= context.expires_at:
            raise upload_error(
                "complete_material_upload", "upload_expired", "上传授权已过期，请重新选择文件上传"
            )
        token = await self.api.material_credentials(credentials)
        reference = await self._commit_material(context.uri, context.session_key, token)
        return {"fileContent": reference, "fileSuffix": context.suffix, "name": context.name}

    async def _apply_material(self, suffix: str, token: MaterialToken) -> dict:
        params = {
            "NeedFallback": "true", "UploadNum": "1",
            "uid": IMAGEX["userId"], "appid": IMAGEX["appId"],
        }
        if _MIME[suffix] not in {"image/png", "image/jpeg", "image/gif"}:
            params["FileExtension"] = "." + suffix
        applied = await self._imagex(
            "ApplyImageUpload", "GET", token, params, response_model=ApplyUploadResponse
        )
        try:
            address = applied["UploadAddress"]
            stores = address["StoreInfos"]
            if len(stores) != 1:
                raise ValueError("address")
            uri, authorization = stores[0]["StoreUri"], stores[0]["Auth"]
            bucket, separator, key = uri.partition("/")
            session_key = address["SessionKey"]
            if not bucket or not separator or not key or not authorization or not session_key:
                raise ValueError("store")
        except (KeyError, IndexError, TypeError, ValueError, AttributeError):
            raise upload_error(
                "ApplyImageUpload", "invalid_upload_address", "材料上传会话不完整"
            ) from None
        return {
            "uri": uri, "session_key": session_key,
            "url": "https://" + IMAGEX["uploadHosts"][0] + "/" + quote(uri, safe="/"),
            "headers": {
                "Authorization": authorization,
                "Specified-Content-Type": _MIME[suffix],
            },
        }


    async def _commit_material(self, uri: str, session_key: str, token: MaterialToken) -> str:
        committed = await self._imagex(
            "CommitImageUpload", "POST", token, {"SkipMeta": "true"},
            {
                "SessionKey": session_key, "SuccessOids": [uri],
                "Functions": [], "PostProcess": [], "DecryptKeys": [],
            },
            response_model=CommitUploadResponse,
        )
        try:
            results = committed["Results"]
            if len(results) != 1 or results[0]["UriStatus"] != 2000 or results[0]["Uri"] != uri:
                raise ValueError("commit")
            return results[0]["Uri"]
        except (KeyError, IndexError, TypeError, ValueError, ValidationError):
            raise upload_error(
                "CommitImageUpload", "upload_not_confirmed", "材料上传提交结果待确认", unknown=True
            ) from None


def _upload_signature(
    context: MaterialUploadContext | RecipientsUploadContext,
    credentials: Credentials, purpose: str,
) -> str:
    # 与已有开通确认相同，按当前登录凭据绑定；跨实例无草稿，凭据刷新后需重新上传。
    payload = json.dumps({
        "context": context.model_dump(), "accessKey": credentials.access_key,
        "sessionToken": credentials.session_token,
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    prefix = ("sms-" + purpose + "-upload\0").encode()
    return hmac.digest(credentials.secret_key.encode(), prefix + payload, "sha256").hex()


def _check_tos_url(url: str) -> None:
    """_check_tos_url 保留既有 TOS 受信域名边界，不允许重定向或调用方任意 URL。"""
    try:
        parsed = urlsplit(url)
        valid = (
            parsed.scheme == "https" and parsed.hostname
            and parsed.hostname.endswith(".volces.com") and not parsed.username
            and not parsed.password and not parsed.fragment and parsed.port in (None, 443)
        )
    except ValueError:
        valid = False
    if not valid:
        raise upload_error("RecipientsUpload", "invalid_upload_url", "短信服务返回的名单地址无效")
