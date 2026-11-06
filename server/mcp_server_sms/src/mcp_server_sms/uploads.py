"""MCP 表单上传：文件通过宿主工具通道进入，凭据始终留在服务端。"""

import base64
import binascii
import csv
import hashlib
import io
import json
import re
import zlib
from http.cookiejar import CookieJar
from pathlib import PurePath
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
    MAX_UPLOAD_BYTES,
    ApplyUploadResponse,
    CommitUploadResponse,
    FileUpload,
    MaterialToken,
    MaterialUpload,
    SmsRequestError,
    UploadedMaterial,
)

# 来自短信生产材料上传契约，与客户或部署账号无关；不是浏览器可覆盖的地址。
IMAGEX = FORM_CONFIG["materialUpload"]
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


def decode_file(request: FileUpload) -> tuple[bytes, str]:
    """校验大小与文件类别，原始文件字节不做转换。"""
    try:
        data = base64.b64decode(request.data, validate=True)
    except (ValueError, binascii.Error):
        raise upload_error(
            "upload_sms_file", "invalid_file", "文件编码无效，请重新选择文件"
        ) from None
    if not data or len(data) > MAX_UPLOAD_BYTES:
        raise upload_error("upload_sms_file", "invalid_file_size", "请选择不超过 10 MB 的非空文件")
    suffix = PurePath(request.name).suffix[1:].lower()
    allowed = _MATERIAL_TYPES[request.category] if isinstance(request, MaterialUpload) else {"csv"}
    if suffix not in allowed:
        raise upload_error("upload_sms_file", "invalid_file_type", "此材料不支持所选文件类型")
    return data, suffix


def validate_recipients(data: bytes, demo: str) -> dict:
    """按照上游 CSV 表头校验原文件，只统计重复号码，不修改或去重文件。"""
    try:
        expected = next(csv.reader(io.StringIO(demo), strict=True))
        rows = csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True)
        columns = next(rows)
        if not expected or expected[0] != "phone" or columns != expected:
            raise ValueError("headers")
        count, phones, samples = 0, set(), []
        for row in rows:
            if len(row) != len(columns) or re.fullmatch(r"1[3-9][0-9]{9}", row[0]) is None:
                raise ValueError("row")
            count += 1
            phones.add(row[0])
            if len(samples) < 3:
                samples.append(
                    {
                        "phone": row[0][:3] + "****" + row[0][-4:],
                        "params": dict(zip(columns[1:], row[1:], strict=True)),
                    }
                )
        if count == 0:
            raise ValueError("empty")
    except (ValueError, UnicodeError, csv.Error, StopIteration):
        raise upload_error(
            "upload_sms_file",
            "invalid_csv",
            "名单格式不符合模板，请使用下载的 UTF-8 CSV 示例并检查号码和列数",
        ) from None
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

    async def upload(self, request: FileUpload, credentials: Credentials) -> dict:
        # 文件请求不排队持有解码缓冲；满载时明确拒绝，取消或失败都会归还槽位。
        try:
            self._slots.acquire_nowait()
        except WouldBlock:
            raise upload_error(
                "upload_sms_file", "upload_busy", "当前上传较多，请稍后重新选择文件"
            ) from None
        try:
            return await self._upload(request, credentials)
        finally:
            self._slots.release()

    async def _upload(self, request: FileUpload, credentials: Credentials) -> dict:
        data, suffix = decode_file(request)
        if isinstance(request, MaterialUpload):
            token = await self.api.material_credentials(credentials)
            reference = await self._material(data, suffix, token)
            return {"fileContent": reference, "fileSuffix": suffix, "name": request.name}
        demo = await self.api.call(
            "TemplateUploadDemoForAgent",
            {
                "subAccount": request.sub_account,
                "templateId": request.template_id,
            },
            credentials,
        )
        if not demo["success"]:
            raise SmsRequestError(demo)
        counts = validate_recipients(data, demo["result"]["value"])
        authorized = await self.api.call("GetUploadTosURL", {"suffix": "csv"}, credentials)
        if not authorized["success"]:
            raise SmsRequestError(authorized)
        url = authorized["result"]["url"]
        parsed = urlsplit(url)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or not parsed.hostname.endswith(".volces.com")
            or parsed.username
            or parsed.password
            or parsed.fragment
            or parsed.port not in (None, 443)
        ):
            raise upload_error(
                "UploadRecipients", "invalid_upload_url", "短信服务返回的名单上传地址无效"
            )
        await self._exchange("UploadRecipients", "PUT", url, content=data, json_result=False)
        return {"file": authorized["result"]["file"], "name": request.name, **counts}

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

    async def _material(self, data: bytes, suffix: str, token: MaterialToken) -> str:
        params = {
            "NeedFallback": "true",
            "UploadNum": "1",
            "uid": IMAGEX["userId"],
            "appid": IMAGEX["appId"],
        }
        if _MIME[suffix] not in {"image/png", "image/jpeg", "image/gif"}:
            params["FileExtension"] = "." + suffix
        applied = await self._imagex(
            "ApplyImageUpload", "GET", token, params, response_model=ApplyUploadResponse
        )
        try:
            address = applied["UploadAddress"]
            host = address["UploadHosts"][0]
            stores = address["StoreInfos"]
            if len(stores) != 1 or not isinstance(host, str):
                raise ValueError("address")
            parsed = urlsplit("https://" + host)
            if (
                parsed.hostname != host
                or parsed.port is not None
                or parsed.path
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError("host")
            uri, authorization = stores[0]["StoreUri"], stores[0]["Auth"]
            bucket, separator, key = uri.partition("/")
            session_key = address["SessionKey"]
            if not bucket or not separator or not key or not authorization or not session_key:
                raise ValueError("store")
            upload_headers = address.get("UploadHeader", {})
            if not isinstance(upload_headers, dict) or any(
                not isinstance(v, str) for v in upload_headers.values()
            ):
                raise ValueError("headers")
        except (KeyError, IndexError, TypeError, ValueError, AttributeError):
            raise upload_error(
                "ApplyImageUpload", "invalid_upload_address", "材料上传地址不完整"
            ) from None
        url = (
            "https://" + host + "/upload/v1/" + quote(bucket, safe="") + "/" + quote(key, safe="/")
        )
        await self._exchange(
            "UploadMaterial",
            "POST",
            url,
            content=data,
            headers={
                "Authorization": authorization,
                "X-Upload-Content-CRC32": f"{zlib.crc32(data) & 0xFFFFFFFF:08x}",
                "Specified-Content-Type": _MIME[suffix],
                **upload_headers,
            },
            response_model=UploadedMaterial,
        )
        committed = await self._imagex(
            "CommitImageUpload",
            "POST",
            token,
            {"SkipMeta": "true"},
            {
                "SessionKey": session_key,
                "SuccessOids": [uri],
                "Functions": [],
                "PostProcess": [],
                "DecryptKeys": [],
            },
            response_model=CommitUploadResponse,
        )
        try:
            results = committed["Results"]
            if (
                len(results) != 1
                or results[0]["UriStatus"] != 2000
                or not isinstance(results[0]["Uri"], str)
                or not results[0]["Uri"]
            ):
                raise ValueError("commit")
            return results[0]["Uri"]
        except (KeyError, IndexError, TypeError, ValueError, ValidationError):
            raise upload_error(
                "CommitImageUpload", "upload_not_confirmed", "材料上传提交结果待确认", unknown=True
            ) from None
