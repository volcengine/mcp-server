# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates.
# Licensed under the Apache License, Version 2.0.
# Adapted from byted-sms-sender at c7c49836dff727ca7a2ab297dc9d1ad62c5aec15.

from __future__ import annotations
import csv
import datetime
import hashlib
import hmac
import io
import json
import re
import socket
from dataclasses import dataclass
from functools import reduce
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)
from urllib import error, parse, request
from .action_contracts import (
    _SHORT_URL_CONFIG_FIELDS,
    ACTION_REGISTRY,
    COMMON_PAGE_FIELDS,
    TEMPLATE_DEMO_CSV_MEDIA_TYPES,
    TEMPLATE_FIELDS,
    TEMPLATE_PARAM_FIELDS,
    TEMPLATE_SCALAR_LIST_FIELDS,
    ActionSpec,
)

DEFAULT_ENDPOINT = "https://sms.volcengineapi.com"
DEFAULT_SERVICE = "volcSMS"
DEFAULT_REGION = "cn-north-1"
RETRYABLE_BUSINESS_ERROR_CODES = frozenset({"1015", "1999"})
Params = Union[Mapping[str, Any], Sequence[Tuple[str, Any]]]


@dataclass(frozen=True)
class SignedRequest:
    url: str
    method: str
    headers: Mapping[str, str]
    body: bytes
    canonical_query: str
    canonical_request: str
    string_to_sign: str
    authorization: str

    def to_urllib_request(self) -> request.Request:
        return request.Request(
            self.url,
            data=self.body if self.method != "GET" else None,
            headers=dict(self.headers),
            method=self.method,
        )


@dataclass(frozen=True)
class TransportResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes


class RequestNotSentError(OSError):
    """The transport failed before it could transmit the request."""


class ResponseLostError(OSError):
    """The request may have reached the service but no response was observed."""


@dataclass(frozen=True, repr=False)
class ResolvedCredentials:
    access_key: str
    secret_key: str
    session_token: str = ""


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _hmac(key: bytes, value: str) -> bytes:
    return hmac.new(key, value.encode("utf-8"), hashlib.sha256).digest()


def _query_items(params: Params) -> List[Tuple[str, str]]:
    source = params.items() if isinstance(params, Mapping) else params
    items: List[Tuple[str, str]] = []
    for key, value in source:
        values = value if isinstance(value, (list, tuple)) else (value,)
        for item in values:
            if item is None:
                continue
            if isinstance(item, bool):
                text = "true" if item else "false"
            else:
                text = str(item)
            items.append((str(key), text))
    return items


def _encode_query(items: Iterable[Tuple[str, str]]) -> str:
    encoded = [
        (parse.quote(key, safe="-_.~"), parse.quote(value, safe="-_.~"))
        for key, value in items
    ]
    encoded.sort()
    return "&".join(("{}={}".format(key, value) for key, value in encoded))


def _signing_key(secret_key: str, date: str, region: str, service: str) -> bytes:
    key_date = _hmac(secret_key.encode("utf-8"), date)
    key_region = _hmac(key_date, region)
    key_service = _hmac(key_region, service)
    return _hmac(key_service, "request")


def _compact_json(params: Params) -> bytes:
    if not isinstance(params, Mapping):
        raise ValueError("POST parameters must be a JSON object")
    return json.dumps(
        params, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def build_signed_request(
    spec: ActionSpec,
    params: Params,
    access_key: str,
    secret_key: str,
    now: datetime.datetime,
    *,
    action: Optional[str] = None,
    endpoint: str = DEFAULT_ENDPOINT,
    region: str = DEFAULT_REGION,
    service: str = DEFAULT_SERVICE,
    session_token: str = "",
) -> SignedRequest:
    """Build a V4-signed request and expose its canonical values for tests."""
    if action is None:
        matches = [name for name, value in ACTION_REGISTRY.items() if value is spec]
        if len(matches) != 1:
            raise ValueError("action is required for an unregistered ActionSpec")
        action = matches[0]
    parsed_endpoint = parse.urlsplit(endpoint.rstrip("/"))
    if parsed_endpoint.scheme != "https" or not parsed_endpoint.netloc:
        raise ValueError("VOLCENGINE_SMS_ENDPOINT must be an absolute HTTPS URL")
    path = parsed_endpoint.path or "/"
    path = parse.quote(parse.unquote(path), safe="/-_.~")
    method = spec.method.upper()
    if method == "GET":
        body = b""
        query_items = [("Action", action), ("Version", spec.version)]
        query_items.extend(_query_items(params))
    else:
        body = _compact_json(params)
        query_items = [("Action", action), ("Version", spec.version)]
    canonical_query = _encode_query(query_items)
    utc_now = now.astimezone(datetime.timezone.utc)
    x_date = utc_now.strftime("%Y%m%dT%H%M%SZ")
    short_date = x_date[:8]
    body_hash = _sha256(body)
    canonical_headers: Dict[str, str] = {
        "host": parsed_endpoint.netloc,
        "x-content-sha256": body_hash,
        "x-date": x_date,
    }
    if method != "GET":
        canonical_headers["content-type"] = "application/json"
    if session_token:
        canonical_headers["x-security-token"] = session_token
    signed_header_names = ";".join(sorted(canonical_headers))
    canonical_header_text = "".join(
        (
            "{}:{}\n".format(name, canonical_headers[name].strip())
            for name in sorted(canonical_headers)
        )
    )
    canonical_request = "\n".join(
        [
            method,
            path,
            canonical_query,
            canonical_header_text,
            signed_header_names,
            body_hash,
        ]
    )
    scope = "{}/{}/{}/request".format(short_date, region, service)
    string_to_sign = "\n".join(
        ["HMAC-SHA256", x_date, scope, _sha256(canonical_request.encode("utf-8"))]
    )
    signature = hmac.new(
        _signing_key(secret_key, short_date, region, service),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    authorization = (
        "HMAC-SHA256 Credential={}/{}, SignedHeaders={}, Signature={}".format(
            access_key, scope, signed_header_names, signature
        )
    )
    headers = {
        "Host": parsed_endpoint.netloc,
        "X-Date": x_date,
        "X-Content-Sha256": body_hash,
        "Authorization": authorization,
    }
    if method != "GET":
        headers["Content-Type"] = "application/json"
    if session_token:
        headers["X-Security-Token"] = session_token
    base_url = parse.urlunsplit(
        (parsed_endpoint.scheme, parsed_endpoint.netloc, path, "", "")
    )
    return SignedRequest(
        url="{}?{}".format(base_url, canonical_query),
        method=method,
        headers=headers,
        body=body,
        canonical_query=canonical_query,
        canonical_request=canonical_request,
        string_to_sign=string_to_sign,
        authorization=authorization,
    )


def _urllib_transport(req: request.Request, timeout: float) -> TransportResponse:
    class NoRedirect(request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    try:
        with request.build_opener(NoRedirect()).open(req, timeout=timeout) as response:
            return TransportResponse(
                int(response.getcode()), dict(response.headers.items()), response.read()
            )
    except error.HTTPError as exc:
        return TransportResponse(
            int(exc.code),
            dict(exc.headers.items()) if exc.headers else {},
            exc.read() if hasattr(exc, "read") else b"",
        )
    except (socket.timeout, TimeoutError) as exc:
        raise ResponseLostError(str(exc)) from exc
    except error.URLError as exc:
        raise ResponseLostError(str(exc.reason)) from exc
    except (ConnectionError, OSError) as exc:
        raise ResponseLostError(str(exc)) from exc


_PHONE_RE = re.compile("(?<!\\d)(?:\\+?86)?(1[3-9]\\d)(\\d{4})(\\d{4})(?!\\d)")
_URL_RE = re.compile("https?://[^\\s\\\"'<>]+")
_AUTH_RE = re.compile("(?i)\\bAuthorization\\s*[:=]\\s*[^\\r\\n]+")
_BEARER_RE = re.compile("(?i)\\bBearer\\s+[A-Za-z0-9._~+/\\-=]+")
_SENSITIVE_KEYS = {
    "authorization",
    "accesskey",
    "access_key",
    "secretkey",
    "secret_key",
    "ak",
    "sk",
    "token",
    "sessiontoken",
    "xsecuritytoken",
    "ticket",
    "businesscheckticket",
    "operatorcheckticket",
    "responsiblecheckticket",
    "legalcheckticket",
    "identitycard",
    "identitycardnumber",
    "uploadfilelist",
    "materialurl",
    "callbackurl",
}


def _sanitize_text(
    value: str, secrets: Sequence[str], *, strip_url_query: bool = True
) -> str:
    safe = reduce(
        lambda redacted, literal: (
            redacted.replace(literal, "[REDACTED]") if literal else redacted
        ),
        secrets,
        value,
    )
    safe = _AUTH_RE.sub("Authorization: [REDACTED]", safe)
    safe = _BEARER_RE.sub("Bearer [REDACTED]", safe)
    safe = _PHONE_RE.sub(
        lambda match: "{}****{}".format(match.group(1), match.group(3)), safe
    )

    def strip_url(match: re.Match) -> str:
        raw = match.group(0)
        parsed = parse.urlsplit(raw)
        return parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))

    if strip_url_query:
        safe = _URL_RE.sub(strip_url, safe)
    if len(safe) > 1024:
        safe = safe[:1021] + "..."
    return safe


# Identifiers and integrity hashes are protocol data, not free text. A run of
# digits inside a UUID/hash must not be mistaken for a phone number.
_OPAQUE_FIELDS = frozenset(
    {
        "id",
        "ids",
        "subaccount",
        "subaccounts",
        "subaccountid",
        "messageid",
        "messageids",
        "templateid",
        "templateids",
        "secondtemplateid",
        "flowid",
        "draftid",
        "reviewfileid",
        "sha256",
        "operationid",
        "fileid",
        "qualificationid",
        "identificationid",
        "signatureidentificationid",
        "applyid",
        "taskid",
        "requestid",
        "logid",
        "digest",
        "filesha256",
        "contentsha256",
        "templatesha256",
        "renderedsha256",
        "templatecontentsha256",
        "renderedcontentsha256",
        "filekeyfingerprint",
        "ticket",
        "businesscheckticket",
        "operatorcheckticket",
        "responsiblecheckticket",
        "legalcheckticket",
        "accesskeyid",
        "secretaccesskey",
        "sessiontoken",
    }
)


def sanitize_output(
    value: Any, *, secrets: Sequence[str] = (), field_name: str = ""
) -> Any:
    """Remove private fields and mask free text without rewriting identifiers."""
    if isinstance(value, Mapping):
        cleaned = {}
        for key, item in value.items():
            canonical = str(key).replace("-", "").replace("_", "").lower()
            if canonical in _SENSITIVE_KEYS or canonical in {
                "fileurl",
                "imageuri",
                "personidcard",
            }:
                continue
            cleaned[str(key)] = sanitize_output(
                item, secrets=secrets, field_name=str(key)
            )
        return cleaned
    if isinstance(value, (list, tuple)):
        return [
            sanitize_output(item, secrets=secrets, field_name=field_name)
            for item in value
        ]
    if isinstance(value, str):
        if field_name.replace("-", "").replace("_", "").lower() in _OPAQUE_FIELDS:
            return reduce(
                lambda redacted, literal: (
                    redacted.replace(literal, "[REDACTED]") if literal else redacted
                ),
                secrets,
                value,
            )
        return _sanitize_text(value, secrets)
    return value


def _filter_result(
    value: Any,
    allowed_fields: Optional[frozenset],
    secrets: Sequence[str],
    *,
    preserve_presigned_url: bool = False,
    field_name: str = "",
) -> Any:
    if allowed_fields is None:
        return sanitize_output(value, secrets=secrets, field_name=field_name)
    if isinstance(value, Mapping):
        output: Dict[str, Any] = {}
        for key, item in value.items():
            if key not in allowed_fields:
                continue
            if (
                preserve_presigned_url
                and str(key).lower() == "url"
                and isinstance(item, str)
            ):
                output[str(key)] = item
            else:
                output[str(key)] = _filter_result(
                    item,
                    allowed_fields,
                    secrets,
                    preserve_presigned_url=preserve_presigned_url,
                    field_name=str(key),
                )
        return output
    if isinstance(value, (list, tuple)):
        return [
            _filter_result(
                item,
                allowed_fields,
                secrets,
                preserve_presigned_url=preserve_presigned_url,
                field_name=field_name,
            )
            for item in value
        ]
    return sanitize_output(value, secrets=secrets, field_name=field_name)


def _filter_template_result(value: Any, secrets: Sequence[str]) -> Any:
    """Filter template results with allowlists scoped to each published path."""
    if not isinstance(value, Mapping):
        return {}

    def filter_nested(item: Any, allowed: Set[str]) -> Any:
        if isinstance(item, Mapping):
            return {
                str(key): sanitize_output(nested, secrets=secrets, field_name=str(key))
                for key, nested in item.items()
                if key in allowed
                and (not isinstance(nested, (Mapping, list, tuple, set)))
            }
        if isinstance(item, (list, tuple)):
            return [filter_nested(nested, allowed) for nested in item]
        return sanitize_output(item, secrets=secrets)

    def filter_item(item: Any) -> Any:
        if not isinstance(item, Mapping):
            return sanitize_output(item, secrets=secrets)
        output: Dict[str, Any] = {}
        for key, nested in item.items():
            if key not in TEMPLATE_FIELDS:
                continue
            if key in {"TemplateParams", "templateParams"}:
                output[str(key)] = filter_nested(nested, TEMPLATE_PARAM_FIELDS)
            elif key in {"ShortUrlConfig", "shortUrlConfig"}:
                output[str(key)] = filter_nested(nested, _SHORT_URL_CONFIG_FIELDS)
            elif key in TEMPLATE_SCALAR_LIST_FIELDS:
                values = nested if isinstance(nested, (list, tuple)) else ()
                output[str(key)] = [
                    sanitize_output(value, secrets=secrets, field_name=str(key))
                    for value in values
                    if not isinstance(value, (Mapping, list, tuple, set))
                ]
            elif isinstance(nested, (Mapping, list, tuple, set)):
                continue
            else:
                output[str(key)] = sanitize_output(
                    nested, secrets=secrets, field_name=str(key)
                )
        return output

    output: Dict[str, Any] = {}
    for key, item in value.items():
        if key in {"List", "list", "Items", "items"}:
            values = item if isinstance(item, (list, tuple)) else ()
            output[str(key)] = [
                filter_item(nested) for nested in values if isinstance(nested, Mapping)
            ]
        elif key in COMMON_PAGE_FIELDS and (
            not isinstance(item, (Mapping, list, tuple, set))
        ):
            output[str(key)] = sanitize_output(item, secrets=secrets)
        elif key in TEMPLATE_FIELDS:
            filtered = filter_item({key: item})
            if key in filtered:
                output[str(key)] = filtered[key]
    return output


def _filter_message_group_detail(value: Any, secrets: Sequence[str]) -> Any:
    """Filter GetSubAccountDetail with field allowlists scoped by JSON path."""
    if not isinstance(value, Mapping):
        return {}

    def is_scalar(item: Any) -> bool:
        return not isinstance(item, (Mapping, list, tuple, set))

    output: Dict[str, Any] = {}
    for key in ("subAccountId", "subAccountName", "status"):
        if key in value and is_scalar(value[key]):
            output[key] = sanitize_output(
                value[key], secrets=secrets, field_name=str(key)
            )
    mapping_key = "channelTypeToIndustryConfig"
    if mapping_key in value:
        raw_mappings = value[mapping_key]
        mappings = raw_mappings if isinstance(raw_mappings, (list, tuple)) else ()
        output[mapping_key] = [
            {
                key: sanitize_output(item[key], secrets=secrets)
                for key in ("channelType", "channelTypeCn", "industry", "industryCn")
                if key in item and is_scalar(item[key])
            }
            for item in mappings
            if isinstance(item, Mapping)
        ]
    return output


def _header(headers: Mapping[str, str], name: str) -> Optional[str]:
    lowered = name.lower()
    for key, value in headers.items():
        if key.lower() == lowered:
            return value
    return None


def _request_id(payload: Any, headers: Mapping[str, str]) -> Optional[str]:
    if isinstance(payload, Mapping):
        metadata = payload.get("ResponseMetadata")
        if isinstance(metadata, Mapping):
            value = metadata.get("RequestId") or metadata.get("RequestID")
            if value is not None:
                return str(value)
    return _header(headers, "X-Tt-Logid") or _header(headers, "X-Request-Id")


def _business_error_code(response: TransportResponse) -> str:
    try:
        payload = json.loads(response.body.decode("utf-8")) if response.body else {}
    except (UnicodeDecodeError, json.JSONDecodeError):
        return ""
    metadata = payload.get("ResponseMetadata") if isinstance(payload, Mapping) else None
    error_value = (
        metadata.get("Error")
        if isinstance(metadata, Mapping) and isinstance(metadata.get("Error"), Mapping)
        else None
    )
    return str(error_value.get("Code") or "") if error_value is not None else ""


def _filename_from_content_disposition(value: Optional[str]) -> str:
    if not value:
        return ""
    for part in value.split(";"):
        key, separator, raw = part.strip().partition("=")
        if not separator or key.lower() not in {"filename", "filename*"}:
            continue
        encoded = raw.strip().strip('"')
        if key.lower() == "filename*" and "''" in encoded:
            encoded = encoded.split("''", 1)[1]
        decoded = parse.unquote(encoded).replace("\\", "/").rsplit("/", 1)[-1]
        if decoded:
            return decoded
    return ""


def _error_envelope(
    action: str,
    code: str,
    message: str,
    *,
    request_id: Optional[str] = None,
    retryable: bool = False,
    outcome_unknown: bool = False,
    secrets: Sequence[str] = (),
    remediation: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    error_value: Dict[str, Any] = {
        "code": code,
        "message": _sanitize_text(message, secrets),
        "retryable": retryable,
        "outcome_unknown": outcome_unknown,
    }
    if remediation:
        error_value["remediation"] = sanitize_output(dict(remediation), secrets=secrets)
    return {
        "success": False,
        "action": action,
        "request_id": _sanitize_text(request_id, secrets) if request_id else None,
        "result": None,
        "error": error_value,
    }


def _invalid_success_response(
    action: str,
    spec: ActionSpec,
    message: str,
    *,
    request_id: Optional[str],
    secrets: Sequence[str],
) -> Dict[str, Any]:
    """Preserve an ambiguous write outcome when a 2xx body is unusable."""
    if spec.read_only:
        return _error_envelope(
            action, "invalid_response", message, request_id=request_id, secrets=secrets
        )
    return _error_envelope(
        action,
        "outcome_unknown",
        message,
        request_id=request_id,
        outcome_unknown=True,
        secrets=secrets,
    )


def _result_contract_error(spec: ActionSpec, result: Any) -> Optional[str]:
    """Return a structural response error without treating zero as missing."""
    if not spec.required_result_fields and (not spec.required_result_any):
        return None
    if not isinstance(result, Mapping):
        return "Service response Result must be a JSON object"
    missing = sorted(
        (field for field in spec.required_result_fields if field not in result)
    )
    if missing:
        return "Service response Result is missing required field(s): {}".format(
            ", ".join(missing)
        )
    if spec.required_result_any and (
        not any((field in result for field in spec.required_result_any))
    ):
        return "Service response Result contains none of the expected fields"
    return None


def _normalize_template_demo_csv(
    action: str, spec: ActionSpec, response: TransportResponse, secrets: Sequence[str]
) -> Dict[str, Any]:
    request_id = _request_id({}, response.headers)
    content_type = _header(response.headers, "Content-Type") or ""
    media_type = content_type.partition(";")[0].strip().lower()
    if not response.body:
        return _error_envelope(
            action,
            "invalid_response",
            "TemplateUploadDemo returned an empty response body",
            request_id=request_id,
            secrets=secrets,
        )
    if media_type not in TEMPLATE_DEMO_CSV_MEDIA_TYPES:
        return _error_envelope(
            action,
            "invalid_response",
            "TemplateUploadDemo response was not an expected CSV file",
            request_id=request_id,
            secrets=secrets,
        )
    try:
        value = response.body.decode("utf-8-sig")
    except UnicodeDecodeError:
        return _error_envelope(
            action,
            "invalid_response",
            "TemplateUploadDemo CSV was not valid UTF-8",
            request_id=request_id,
            secrets=secrets,
        )
    try:
        first_row = next(csv.reader(io.StringIO(value, newline=""), strict=True))
    except (csv.Error, StopIteration):
        first_row = []
    if not first_row or first_row[0] != "phone":
        return _error_envelope(
            action,
            "invalid_response",
            "TemplateUploadDemo CSV must use phone as its first column",
            request_id=request_id,
            secrets=secrets,
        )
    demo = {
        "fileName": _filename_from_content_disposition(
            _header(response.headers, "Content-Disposition")
        )
        or "TemplateUploadDemo.csv",
        "value": value,
        "contentType": content_type,
        "size": len(response.body),
    }
    return {
        "success": True,
        "action": action,
        "request_id": _sanitize_text(request_id, secrets) if request_id else None,
        "result": _filter_result(demo, spec.result_fields, secrets),
        "error": None,
    }


def emit_json(value: Any, *, secrets: Sequence[str] = ()) -> str:
    """Return stable JSON suitable for stdout/stderr without leaking secrets."""
    return json.dumps(
        sanitize_output(value, secrets=secrets),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def normalize_response(
    action: str,
    spec: ActionSpec,
    response: TransportResponse,
    secrets: Sequence[str],
    *,
    preserve_presigned_url: bool = False,
) -> Dict[str, Any]:
    if (
        action == "TemplateUploadDemo"
        and 200 <= response.status < 300
        and (not response.body)
    ):
        return _normalize_template_demo_csv(action, spec, response, secrets)
    try:
        payload = json.loads(response.body.decode("utf-8")) if response.body else {}
    except (UnicodeDecodeError, json.JSONDecodeError):
        if action == "TemplateUploadDemo" and 200 <= response.status < 300:
            return _normalize_template_demo_csv(action, spec, response, secrets)
        if 200 <= response.status < 300:
            return _invalid_success_response(
                action,
                spec,
                "Service response was not valid JSON",
                request_id=_request_id({}, response.headers),
                secrets=secrets,
            )
        return _error_envelope(
            action,
            "http_{}".format(response.status),
            "HTTP {} returned a non-JSON response".format(response.status),
            request_id=_request_id({}, response.headers),
            retryable=spec.read_only
            and (response.status == 429 or 500 <= response.status <= 599),
            secrets=secrets,
        )
    request_id = _request_id(payload, response.headers)
    metadata = payload.get("ResponseMetadata") if isinstance(payload, Mapping) else None
    business_error = (
        metadata.get("Error")
        if isinstance(metadata, Mapping) and isinstance(metadata.get("Error"), Mapping)
        else None
    )
    if business_error is not None:
        business_code = str(business_error.get("Code") or "service_error")
        return _error_envelope(
            action,
            business_code,
            "Service returned error {}".format(business_code),
            request_id=request_id,
            retryable=spec.read_only
            and (
                response.status == 429
                or 500 <= response.status <= 599
                or business_code in RETRYABLE_BUSINESS_ERROR_CODES
            ),
            secrets=secrets,
        )
    if response.status >= 500 and not spec.read_only:
        return _error_envelope(
            action,
            "outcome_unknown",
            "写请求结果暂时无法确认",
            request_id=request_id,
            outcome_unknown=True,
            secrets=secrets,
        )
    if not 200 <= response.status < 300:
        return _error_envelope(
            action,
            "http_{}".format(response.status),
            "HTTP {}".format(response.status),
            request_id=request_id,
            retryable=spec.read_only
            and (response.status == 429 or 500 <= response.status <= 599),
            secrets=secrets,
        )
    if not isinstance(payload, Mapping):
        return _invalid_success_response(
            action,
            spec,
            "Service response root must be a JSON object",
            request_id=request_id,
            secrets=secrets,
        )
    if action == "GetSubAccountDetail":
        result = _filter_message_group_detail(payload.get("Result"), secrets)
    elif action in {"ListSmsTemplateForAgent", "ListSecondTemplate"}:
        result = _filter_template_result(payload.get("Result"), secrets)
    else:
        result = _filter_result(
            payload.get("Result"),
            spec.result_fields,
            secrets,
            preserve_presigned_url=preserve_presigned_url,
        )
    contract_error = _result_contract_error(spec, result)
    if contract_error is not None:
        return _invalid_success_response(
            action, spec, contract_error, request_id=request_id, secrets=secrets
        )
    return {
        "success": True,
        "action": action,
        "request_id": _sanitize_text(request_id, secrets) if request_id else None,
        "result": result,
        "error": None,
    }
