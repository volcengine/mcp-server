"""SMS HTTP boundary: official V4 signing, one request, structured outcomes."""

import json
from dataclasses import dataclass
from http.cookiejar import CookieJar, DefaultCookiePolicy
from typing import Any, Literal

import httpx
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials as SigningCredentials

from .auth import Credentials

API_HOST = "sms.volcengineapi.com"
API_VERSION = "2026-01-01"
API_REGION = "cn-north-1"
API_SERVICE = "volcSMS"


@dataclass(frozen=True)
class Action:
    method: Literal["GET", "POST"]
    write: bool = False
    result_format: Literal["json", "csv", "id"] = "json"
    required_any: tuple[str, ...] = ()
    required_all: tuple[str, ...] = ()
    opaque_result_fields: tuple[str, ...] = ()


# Only named tools can select an action; callers cannot supply arbitrary APIs.
ACTIONS = {
    "ListSubAccountForAgent": Action("POST"),
    "GetSubAccountDetail": Action("GET"),
    "ListAllSmsProduct": Action("GET"),
    "GetAccountIdentRankForAgent": Action("GET"),
    "GetSignatureIdentificationList": Action("POST"),
    "GetOCRLicenseForAgent": Action("POST"),
    "ThreeElementEnterpriseCheckForAgent": Action("POST"),
    "ThreeElementPersonCheckForAgent": Action("POST"),
    "SendSmsVerifyCodeByMobile": Action("POST", True, required_any=("messageId",)),
    "CheckSmsVerifyCodeByMobile": Action("POST", True, required_any=("status",)),
    "ApplySignatureIdentificationForAgent": Action("POST", True, "id"),
    "ListSignatureForAgent": Action("POST"),
    "ApplySmsSignatureV2": Action("POST", True, required_any=("applyId", "status")),
    "ListSmsTemplateForAgent": Action("POST"),
    "ListSecondTemplate": Action("GET"),
    "ApplySmsTemplateV2": Action("POST", True, required_any=("templateId", "status")),
    "SendSmsForAgent": Action("POST", True, required_any=("MessageId", "MessageIds")),
    "ListSmsSendLogForAgent": Action("POST"),
    "ListTotalSendCountStatForAgent": Action("POST"),
    "GetUploadTosURL": Action(
        "GET", True, required_all=("file", "url"), opaque_result_fields=("url",)
    ),
    "TemplateUploadDemo": Action("POST", result_format="csv"),
    "SetBatchTask": Action("POST", True, required_any=("taskId",)),
    "GetBatchTaskDetail": Action("GET"),
    "GetBatchTaskList": Action("GET"),
    "ConsentBatchTask": Action("POST", True),
    "DeleteBatchTask": Action("POST", True),
}

_CREDENTIAL_FIELDS = frozenset(
    {
        "accesskeyid",
        "accesskey",
        "secretaccesskey",
        "secretkey",
        "sessiontoken",
        "securitytoken",
        "authorization",
        "cookie",
        "set-cookie",
    }
)

# These status codes explicitly reject the request. Unstructured timeout,
# conflict and gateway-specific responses remain uncertain for mutations.
_REJECTED_HTTP_STATUSES = frozenset({400, 401, 403, 404, 405, 413, 415, 422, 429})


class _RejectCookies(DefaultCookiePolicy):
    """Connection pooling must not introduce cross-caller cookie state."""

    def set_ok(self, cookie, request):
        return False


def safe_result(
    value: Any, credentials: Credentials, *, opaque_fields: tuple[str, ...] = ()
) -> Any:
    """Redact credentials while preserving declared top-level API references."""
    if isinstance(value, dict):
        return {
            key: item if key in opaque_fields else safe_result(item, credentials)
            for key, item in value.items()
            if key.lower() not in _CREDENTIAL_FIELDS
        }
    if isinstance(value, list):
        return [safe_result(item, credentials) for item in value]
    if isinstance(value, str):
        for secret in (credentials.access_key, credentials.secret_key, credentials.session_token):
            if secret:
                value = value.replace(secret, "[REDACTED]")
    return value


def failure(action, code, message, request_id=None, *, outcome_unknown=False, http_status=None):
    error = {"code": code, "message": message, "outcome_unknown": outcome_unknown}
    if http_status is not None:
        error["http_status"] = http_status
    return {
        "success": False,
        "action": action,
        "request_id": request_id,
        "result": None,
        "error": error,
    }


class SmsClient:
    def __init__(self, *, transport: httpx.AsyncBaseTransport | None = None, timeout: float = 15):
        self._http = httpx.AsyncClient(
            transport=transport,
            timeout=timeout,
            follow_redirects=False,
            cookies=CookieJar(policy=_RejectCookies()),
        )

    async def __aenter__(self):
        await self._http.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._http.__aexit__(exc_type, exc_value, traceback)

    async def call(self, action: str, params: dict, credentials: Credentials) -> dict:
        spec = ACTIONS[action]
        wire = {key: value for key, value in params.items() if value is not None}
        request = Request()
        request.schema = "https"
        request.set_host(API_HOST)
        request.set_path("/")
        request.set_method(spec.method)
        request.set_headers({"Accept": "application/json", "Content-Type": "application/json"})
        query = {"Action": action, "Version": API_VERSION}
        if spec.method == "GET":
            query.update(
                {
                    key: str(value).lower() if isinstance(value, bool) else str(value)
                    for key, value in wire.items()
                }
            )
        else:
            request.set_body(json.dumps(wire, ensure_ascii=False, separators=(",", ":")))
        request.set_query(query)
        SignerV4.sign(
            request,
            SigningCredentials(
                credentials.access_key,
                credentials.secret_key,
                API_SERVICE,
                API_REGION,
                credentials.session_token,
            ),
        )
        try:
            response = await self._http.request(
                spec.method,
                request.build(),
                headers=request.headers,
                content=request.body.encode("utf-8") if request.body else None,
            )
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout):
            return failure(action, "connection_failed", "未建立 API 连接，请检查网络")
        except httpx.HTTPError:
            return failure(
                action,
                "outcome_unknown" if spec.write else "transport_error",
                "请求结果暂时无法确认；写操作不要自动重试",
                outcome_unknown=spec.write,
            )
        return self.decode(action, response, credentials)

    @staticmethod
    def decode(action: str, response: httpx.Response, credentials: Credentials) -> dict:
        spec = ACTIONS[action]
        request_id = response.headers.get("x-tt-logid") or response.headers.get("x-request-id")
        request_id = safe_result(request_id, credentials)
        try:
            payload = response.json()
        except ValueError:
            content_type = response.headers.get("content-type", "").split(";", 1)[0]
            if (
                spec.result_format == "csv"
                and response.is_success
                and content_type
                in {
                    "text/csv",
                    "application/csv",
                    "application/octet-stream",
                    "application/vnd.ms-excel",
                    "text/comma-separated-values",
                }
            ):
                try:
                    result = {
                        "content": response.content.decode("utf-8-sig"),
                        "contentType": "text/csv",
                    }
                except UnicodeError:
                    return failure(
                        action,
                        "invalid_response",
                        "CSV 响应不是 UTF-8",
                        request_id,
                        http_status=response.status_code,
                    )
                return {
                    "success": True,
                    "action": action,
                    "request_id": request_id,
                    "result": safe_result(result, credentials),
                    "error": None,
                }
            payload = None
        metadata = payload.get("ResponseMetadata", {}) if isinstance(payload, dict) else {}
        if isinstance(metadata, dict):
            request_id = metadata.get("RequestId") or request_id
        else:
            metadata = {}
        request_id = safe_result(request_id, credentials)
        if response.status_code >= 500 and spec.write:
            return failure(
                action,
                "outcome_unknown",
                "服务端异常，不能确认写入结果",
                request_id,
                outcome_unknown=True,
                http_status=response.status_code,
            )
        api_error = metadata.get("Error")
        if isinstance(api_error, dict):
            # API error messages can echo identity documents, codes or auth input.
            # Preserve the public error code and RequestId, never echo raw input.
            code = safe_result(str(api_error.get("Code") or "api_error"), credentials)
            return failure(
                action,
                code,
                "短信 API 返回错误，请结合错误码和 RequestId 排查",
                request_id,
                http_status=response.status_code,
            )
        if response.status_code in _REJECTED_HTTP_STATUSES:
            return failure(
                action,
                f"http_{response.status_code}",
                "短信 API 拒绝了请求",
                request_id,
                http_status=response.status_code,
            )
        if not response.is_success or not isinstance(payload, dict) or "Result" not in payload:
            return failure(
                action,
                "outcome_unknown" if spec.write else "invalid_response",
                "未收到可确认的短信 API 响应",
                request_id,
                outcome_unknown=spec.write,
                http_status=response.status_code,
            )
        result = payload["Result"]
        valid = True
        if spec.result_format == "id":
            valid = type(result) is int and result > 0
        elif spec.required_any:
            valid = isinstance(result, dict) and any(
                key in result
                and result[key] is not None
                and result[key] != ""
                and result[key] != []
                for key in spec.required_any
            )
        if spec.required_all:
            valid = (
                valid
                and isinstance(result, dict)
                and all(
                    isinstance(result.get(key), str) and bool(result[key])
                    for key in spec.required_all
                )
            )
        if not valid:
            return failure(
                action,
                "outcome_unknown" if spec.write else "invalid_response",
                "接口响应缺少必要结果，不能确认操作完成",
                request_id,
                outcome_unknown=spec.write,
                http_status=response.status_code,
            )
        return {
            "success": True,
            "action": action,
            "request_id": request_id,
            # A signed upload URL is an operational capability, not a display
            # string. Editing its query parameters would invalidate the signature.
            "result": safe_result(result, credentials, opaque_fields=spec.opaque_result_fields),
            "error": None,
        }
