"""SMS HTTP boundary: official V4 signing, one request, structured outcomes."""

import json
from dataclasses import dataclass
from http.cookiejar import CookieJar, DefaultCookiePolicy
from typing import Any, Literal

import httpx
from pydantic import BaseModel, ValidationError
from volcengine.auth.SignerV4 import SignerV4
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials as SigningCredentials

from .auth import Credentials
from .observability import observe_call
from .responses import (
    ActivationResult,
    BatchContentChecked,
    BatchTaskCreated,
    BatchTemplateDemo,
    ConfirmedProtocols,
)
from .upload_models import MaterialAuthorization, MaterialToken, SmsRequestError

API_HOST = "sms.volcengineapi.com"
API_VERSION = "2026-01-01"
API_REGION = "cn-north-1"
API_SERVICE = "volcSMS"


@dataclass(frozen=True)
class Action:
    method: Literal["GET", "POST"]
    result_format: Literal["json", "csv", "id", "ack"] = "json"
    required_any: tuple[str, ...] = ()
    required_all: tuple[str, ...] = ()
    opaque_result_fields: tuple[str, ...] = ()
    private_result_fields: frozenset[str] = frozenset()
    result_model: type[BaseModel] | None = None
    timeout: float | None = None
    expose_result: bool = True
    public_result_fields: frozenset[str] | None = None


_RESOURCE_PRIVATE_FIELDS = frozenset({
    "operatorperson", "responsiblepersoninfo", "legalperson", "powerofattorney",
    "othermaterials", "businesscertificate", "legalpersonname", "authfilelist",
    "appicpfilelist", "trademarkfilelist", "fileurl", "filecontent",
    "numberperson", "persontype", "personid",
})

# 群发查询只公开任务摘要。文件 Key、下载能力和内部扩展字段留在短信服务。
_BATCH_TASK_FIELDS = frozenset({
    "taskId", "subAccount", "taskName", "signature", "templateId", "templateName",
    "channelType", "scheduled", "sendTime", "status", "totalCount", "dupCount",
    "sendContent", "msgCount", "okCount", "failCount", "receiptSuccessCount",
    "receiptFailCount", "noReceiptCount", "createdAt", "updatedAt", "taskType",
    "sendTimeStamp", "createdAtStamp", "updatedAtStamp",
})
_PAGE_FIELDS = frozenset({"List", "list", "Items", "items", "Total", "total", "Page", "page", "PageSize", "pageSize"})


# Only named tools can select an action; callers cannot supply arbitrary APIs.
ACTIONS = {
    "GetSubAccountListForAgent": Action("POST", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "GetSubAccountDetail": Action("GET", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "ListAllSmsProduct": Action("GET"),
    "GetAccountIdentRankForAgent": Action("GET"),
    "GetSignatureIdentificationList": Action("POST", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "GetApplySignatureBind": Action("GET"),
    "GetOCRLicenseForAgent": Action("POST"),
    "ThreeElementEnterpriseCheckForAgent": Action("POST"),
    "ThreeElementPersonCheckForAgent": Action("POST"),
    "SendSmsVerifyCodeByMobile": Action("POST", required_any=("messageId",)),
    "CheckSmsVerifyCodeByMobile": Action("POST", required_any=("status",)),
    "ApplySignatureIdentificationForAgent": Action("POST", "id"),
    "ListSignaturesForAgent": Action("POST", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "ApplySmsSignatureV2": Action(
        "POST", required_any=("applyId", "status"),
    ),
    "ListSmsTemplateForAgent": Action("POST", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "ListBatchTemplatesForAgent": Action("POST", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "ListSecondTemplate": Action("GET", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "ApplySmsTemplateV2ForAgent": Action(
        "POST", required_any=("templateId", "status"),
    ),
    "SendSmsForAgent": Action(
        "POST", required_any=("MessageId", "MessageIds"),
    ),
    "ListSmsSendLogForAgent": Action("POST", private_result_fields=frozenset({"mobile", "content"})),
    "GetTotalSendCountStatV4ForAgent": Action("POST"),
    "GetUploadTosURL": Action(
        "GET", required_all=("file", "url"), opaque_result_fields=("url",)
    ),
    "GetFilePublicTosURL": Action(
        "GET", required_all=("fileName", "url"), opaque_result_fields=("url",)
    ),
    # 仅上传组件消费原始凭据；没有任何公开业务工具允许选择这个 Action。
    "GetMUploadParam": Action("GET", result_model=MaterialAuthorization, expose_result=False),
    "TemplateUploadDemoForAgent": Action(
        "POST", result_format="csv", result_model=BatchTemplateDemo
    ),
    "SetBatchTaskForAgent": Action(
        "POST", result_model=BatchTaskCreated, timeout=60,
    ),
    "GetBatchTaskDetail": Action("GET", public_result_fields=_BATCH_TASK_FIELDS),
    "GetBatchTaskList": Action("GET", public_result_fields=_BATCH_TASK_FIELDS | _PAGE_FIELDS),
    "ConsentBatchTask": Action("POST", result_format="ack"),
    "DeleteBatchTask": Action("POST", result_format="ack"),
    "ValidateBatchTaskContentForAgent": Action("POST", result_model=BatchContentChecked),
    "CheckTrafficDrivingExist": Action("GET", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "ListThirdTemplate": Action("GET", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "AgentGetSignatureTemplateReportStatus": Action(
        "GET", private_result_fields=_RESOURCE_PRIVATE_FIELDS | {"content"}
    ),
    "GetTobTrafficDrivingLinkListForAgent": Action("GET"),
    "GetTobTrafficDrivingPhoneListForAgent": Action("GET", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "ListRelationTemplateForAgent": Action("GET", private_result_fields=_RESOURCE_PRIVATE_FIELDS),
    "BulkCreateTobTrafficDrivingLinkForAgent": Action(
        "POST"
    ),
    "BulkCreateTobTrafficDrivingPhoneForAgent": Action(
        "POST", private_result_fields=_RESOURCE_PRIVATE_FIELDS,
    ),
    "ConfirmProtocolDocument": Action(
        "POST", result_model=ConfirmedProtocols,
    ),
    "ActivateSmsProductInOneStep": Action(
        "POST", result_model=ActivationResult,
    ),
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


class _RejectCookies(DefaultCookiePolicy):
    """Connection pooling must not introduce cross-caller cookie state."""

    def set_ok(self, cookie, request):
        return False


def safe_result(
    value: Any, credentials: Credentials, *, opaque_fields: tuple[str, ...] = (),
    private_fields: frozenset[str] = frozenset(),
    public_fields: frozenset[str] | None = None,
) -> Any:
    """Redact credentials while preserving declared top-level API references."""
    if isinstance(value, dict):
        return {
            key: item if key in opaque_fields else safe_result(
                item, credentials, private_fields=private_fields, public_fields=public_fields
            )
            for key, item in value.items()
            if key.lower() not in _CREDENTIAL_FIELDS | private_fields
            and (public_fields is None or key in public_fields)
        }
    if isinstance(value, list):
        return [safe_result(item, credentials, private_fields=private_fields, public_fields=public_fields) for item in value]
    if isinstance(value, str):
        for secret in (credentials.access_key, credentials.secret_key, credentials.session_token):
            if secret:
                value = value.replace(secret, "[REDACTED]")
    return value


def failure(
    action, code, message, request_id=None, *, outcome_unknown=False, http_status=None,
    backend_response=None, source=None,
):
    error = {"code": code, "message": message}
    if outcome_unknown is not None:
        error["outcome_unknown"] = outcome_unknown
    if http_status is not None:
        error["http_status"] = http_status
    if backend_response is not None:
        error["backend_response"] = backend_response
    if source is not None:
        error["source"] = source
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
        with observe_call("api", action) as observation:
            result = await self._call(action, params, credentials)
            observation.record(result)
            return result

    async def _call(self, action: str, params: dict, credentials: Credentials) -> dict:
        response = await self._request(action, params, credentials)
        if isinstance(response, dict):
            return response
        return self.decode(action, response, credentials, params=params)

    async def material_credentials(self, credentials: Credentials) -> MaterialToken:
        """material_credentials 在服务端提取材料上传 STS，普通 call 始终脱敏。"""
        action = "GetMUploadParam"
        with observe_call("api", action) as observation:
            response = await self._request(action, {}, credentials)
            result = response if isinstance(response, dict) else self.decode(action, response, credentials)
            observation.record(result)
            if not result["success"]:
                raise SmsRequestError(result)
            return MaterialAuthorization.model_validate(response.json()["Result"]).token

    async def _request(
        self, action: str, params: dict, credentials: Credentials,
    ) -> httpx.Response | dict:
        """复用官方短信签名及请求隔离；原始响应仅在包内解码边界消费。"""
        spec = ACTIONS[action]
        wire = {key: value for key, value in params.items() if value is not None}
        request = Request()
        request.schema = "https"
        request.set_host(API_HOST)
        request.set_path("/")
        request.set_method(spec.method)
        request.set_headers({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Request-Source": "mcp",
        })
        query = {"Action": action, "Version": API_VERSION}
        if spec.method == "GET":
            for key, value in wire.items():
                if isinstance(value, list):
                    query[key] = [str(item).lower() if isinstance(item, bool) else str(item) for item in value]
                else:
                    query[key] = str(value).lower() if isinstance(value, bool) else str(value)
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
                request.build(doseq=True),
                headers=request.headers,
                content=request.body.encode("utf-8") if request.body else None,
                **({"timeout": spec.timeout} if spec.timeout is not None else {}),
            )
        except httpx.HTTPError as exc:
            return failure(
                action, type(exc).__name__, str(exc), outcome_unknown=None, source="transport"
            )
        return response

    @staticmethod
    def decode(
        action: str, response: httpx.Response, credentials: Credentials,
        *, params: dict | None = None,
    ) -> dict:
        spec = ACTIONS[action]
        request_id = response.headers.get("x-tt-logid") or response.headers.get("x-request-id")
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
                        "value": response.content.decode("utf-8-sig"),
                        "contentType": "text/csv",
                        "size": len(response.content),
                    }
                except UnicodeError:
                    return failure(
                        action,
                        "invalid_response",
                        "CSV 响应不是 UTF-8",
                        request_id,
                        http_status=response.status_code,
                    )
                payload = {"Result": result}
            else:
                payload = None
        metadata = payload.get("ResponseMetadata", {}) if isinstance(payload, dict) else {}
        if isinstance(metadata, dict):
            request_id = metadata.get("RequestId", request_id)
        else:
            metadata = {}
        api_error = metadata.get("Error")
        if isinstance(api_error, dict):
            # 后端错误原样交给调用方；HTTP 状态和错误码不代表业务最终结果。
            return failure(
                action,
                api_error.get("Code"),
                api_error.get("Message"),
                request_id,
                outcome_unknown=None,
                http_status=response.status_code,
                backend_response=payload,
            )
        if response.is_error:
            return failure(
                action,
                f"http_{response.status_code}",
                response.text,
                request_id,
                outcome_unknown=None,
                http_status=response.status_code,
                backend_response=payload if payload is not None else response.text,
            )
        # 仅两个任务状态变更接口使用 TOP 的空结果回执。SuccessResponse(nil) 会省略
        # Result；必须核对本次 Action、Version、RequestId 且无错误，不能仅凭 HTTP 200。
        acknowledgement = (
            spec.result_format == "ack"
            and isinstance(metadata.get("RequestId"), str)
            and bool(metadata["RequestId"])
            and metadata.get("Action") == action
            and metadata.get("Version") == API_VERSION
            and metadata.get("Error") is None
        )
        if not response.is_success or not isinstance(payload, dict) or (
            "Result" not in payload and not acknowledgement
        ):
            return failure(
                action,
                "invalid_response",
                "未收到可确认的短信 API 响应",
                request_id,
                outcome_unknown=None,
                http_status=response.status_code,
                backend_response=payload if payload is not None else response.text,
            )
        result = payload.get("Result")
        valid = True
        if spec.result_format == "ack":
            valid = acknowledgement and result is None
        elif spec.result_format == "id":
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
        if spec.result_model is not None:
            try:
                spec.result_model.model_validate(result, context=params)
            except ValidationError:
                valid = False
        if not valid:
            return failure(
                action,
                "invalid_response",
                "接口响应缺少必要结果，不能确认操作完成",
                request_id,
                outcome_unknown=None,
                http_status=response.status_code,
                backend_response=payload,
            )
        return {
            "success": True,
            "action": action,
            "request_id": request_id,
            # A signed upload URL is an operational capability, not a display
            # string. Editing its query parameters would invalidate the signature.
            "result": safe_result(
                result, credentials, opaque_fields=spec.opaque_result_fields,
                private_fields=spec.private_result_fields,
                public_fields=spec.public_result_fields,
            ) if spec.expose_result else None,
            "error": None,
        }
