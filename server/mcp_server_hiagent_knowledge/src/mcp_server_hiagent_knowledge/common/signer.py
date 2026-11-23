"""HiAgent OpenAPI AK/SK V4 signing."""

from __future__ import annotations

import datetime as _dt
import hashlib
import hmac
import json
from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import parse_qsl, quote, urlsplit


ALGORITHM = "HMAC-SHA256"


@dataclass(frozen=True)
class SignedRequest:
    """Signed HTTP request parts."""

    url: str
    headers: dict[str, str]
    body: bytes


def _hash_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _hmac_sha256(key: bytes | str, message: str) -> bytes:
    if isinstance(key, str):
        key = key.encode("utf-8")
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()


def _normalize_query(params: Mapping[str, str]) -> str:
    pairs: list[tuple[str, str]] = []
    for key, value in params.items():
        pairs.append((quote(str(key), safe="-_.~"), quote(str(value), safe="-_.~")))
    return "&".join(f"{key}={value}" for key, value in sorted(pairs))


def _normalize_uri(path: str) -> str:
    return quote(path or "/", safe="/-_.~")


def _canonical_headers(headers: Mapping[str, str], signed_headers: list[str]) -> str:
    values = {key.lower(): " ".join(str(value).strip().split()) for key, value in headers.items()}
    return "".join(f"{key}:{values[key]}\n" for key in signed_headers)


def _signed_header_names(headers: Mapping[str, str]) -> list[str]:
    selected: list[str] = []
    for key in headers:
        lowered = key.lower()
        if lowered in {"content-type", "content-md5", "host"} or lowered.startswith("x-"):
            selected.append(lowered)
    return sorted(set(selected))


def _signing_key(secret_access_key: str, date: str, region: str, service: str) -> bytes:
    k_date = _hmac_sha256(secret_access_key, date)
    k_region = _hmac_sha256(k_date, region)
    k_service = _hmac_sha256(k_region, service)
    return _hmac_sha256(k_service, "request")


def sign_openapi_request(
    *,
    top_host: str,
    action: str,
    version: str,
    account_id: str,
    access_key_id: str,
    secret_access_key: str,
    region: str,
    service: str,
    body: Mapping[str, object] | None = None,
    now: _dt.datetime | None = None,
) -> SignedRequest:
    """Build a signed POST request for HiAgent OpenAPI."""

    payload = json.dumps(body or {}, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    timestamp = (now or _dt.datetime.now(_dt.timezone.utc)).strftime("%Y%m%dT%H%M%SZ")
    date = timestamp[:8]
    query = {
        "Action": action,
        "Version": version,
        "X-Account-Id": account_id,
    }
    parsed = urlsplit(top_host)
    path = parsed.path or "/"
    host = parsed.netloc
    if not parsed.scheme or not host:
        raise ValueError("HIAGENT_TOP_HOST must include scheme and host")

    base_query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    canonical_query = _normalize_query({**base_query, **query})
    url = f"{parsed.scheme}://{host}{path}?{canonical_query}"

    headers = {
        "Content-Type": "application/json",
        "Host": host,
        "X-Date": timestamp,
        "X-Content-Sha256": _hash_hex(payload),
    }
    signed_headers = _signed_header_names(headers)
    canonical_request = "\n".join(
        [
            "POST",
            _normalize_uri(path),
            canonical_query,
            _canonical_headers(headers, signed_headers),
            ";".join(signed_headers),
            headers["X-Content-Sha256"],
        ]
    )
    credential_scope = f"{date}/{region}/{service}/request"
    string_to_sign = "\n".join(
        [ALGORITHM, timestamp, credential_scope, _hash_hex(canonical_request.encode("utf-8"))]
    )
    signature = hmac.new(
        _signing_key(secret_access_key, date, region, service),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    headers["Authorization"] = (
        f"{ALGORITHM} Credential={access_key_id}/{credential_scope}, "
        f"SignedHeaders={';'.join(signed_headers)}, "
        f"Signature={signature}"
    )

    return SignedRequest(url=url, headers=headers, body=payload)
