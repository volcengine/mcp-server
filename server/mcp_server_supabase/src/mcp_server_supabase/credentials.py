import base64
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


VEFAAS_IAM_CREDENTIAL_PATH = "/var/run/secrets/iam/credential"
AUTHORIZATION_ENV_NAMES = ("authorization", "AUTHORIZATION")
STATIC_ACCESS_KEY_ENV_NAMES = ("VOLCENGINE_ACCESS_KEY", "VOLC_ACCESSKEY")
STATIC_SECRET_KEY_ENV_NAMES = ("VOLCENGINE_SECRET_KEY", "VOLC_SECRETKEY")
STATIC_SESSION_TOKEN_ENV_NAMES = ("VOLCENGINE_SESSION_TOKEN",)


@dataclass(frozen=True, slots=True)
class VolcengineCredentials:
    access_key: str
    secret_key: str
    session_token: str
    source: str
    cacheable: bool


def _get_env_value(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return ""


def _normalize_iso8601(value: str) -> str:
    return value.replace("Z", "+00:00") if value.endswith("Z") else value


def _validate_sts_time_window(payload: dict[str, Any]) -> None:
    current_time = payload.get("CurrentTime")
    expired_time = payload.get("ExpiredTime")
    if not current_time or not expired_time:
        return
    current_dt = datetime.fromisoformat(_normalize_iso8601(str(current_time)))
    expired_dt = datetime.fromisoformat(_normalize_iso8601(str(expired_time)))
    if current_dt > expired_dt:
        raise ValueError("STS token is expired")


def _parse_authorization_payload(raw_value: str, source: str, cacheable: bool) -> VolcengineCredentials:
    token = raw_value.split(" ", 1)[1] if " " in raw_value else raw_value
    decoded_bytes = base64.b64decode(token)
    payload = json.loads(decoded_bytes.decode("utf-8"))
    _validate_sts_time_window(payload)
    access_key = str(payload.get("AccessKeyId") or "").strip()
    secret_key = str(payload.get("SecretAccessKey") or "").strip()
    session_token = str(payload.get("SessionToken") or "").strip()
    if not access_key or not secret_key:
        raise ValueError("AccessKeyId or SecretAccessKey missing in authorization payload")
    return VolcengineCredentials(
        access_key=access_key,
        secret_key=secret_key,
        session_token=session_token,
        source=source,
        cacheable=cacheable,
    )


def _get_request_authorization(context_getter: Callable[[], Any] | None) -> str:
    if context_getter is None:
        return ""
    try:
        context = context_getter()
    except Exception:
        return ""
    request_context = getattr(context, "request_context", None)
    if request_context is None:
        request_context = getattr(context, "_request_context", None)
    request = getattr(request_context, "request", None)
    if request is None:
        return ""
    return str(request.headers.get("authorization") or "").strip()


def _get_vefaas_iam_credentials() -> VolcengineCredentials | None:
    path = Path(VEFAAS_IAM_CREDENTIAL_PATH)
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    access_key = str(payload.get("access_key_id") or "").strip()
    secret_key = str(payload.get("secret_access_key") or "").strip()
    session_token = str(payload.get("session_token") or "").strip()
    if not access_key or not secret_key:
        return None
    return VolcengineCredentials(
        access_key=access_key,
        secret_key=secret_key,
        session_token=session_token,
        source="vefaas_iam",
        cacheable=True,
    )


def resolve_volcengine_credentials(context_getter: Callable[[], Any] | None = None) -> VolcengineCredentials:
    static_access_key = _get_env_value(*STATIC_ACCESS_KEY_ENV_NAMES)
    static_secret_key = _get_env_value(*STATIC_SECRET_KEY_ENV_NAMES)
    static_session_token = _get_env_value(*STATIC_SESSION_TOKEN_ENV_NAMES)
    if static_access_key and static_secret_key:
        return VolcengineCredentials(
            access_key=static_access_key,
            secret_key=static_secret_key,
            session_token=static_session_token,
            source="env",
            cacheable=True,
        )

    request_authorization = _get_request_authorization(context_getter)
    if request_authorization:
        return _parse_authorization_payload(
            request_authorization,
            source="request_authorization",
            cacheable=False,
        )

    env_authorization = _get_env_value(*AUTHORIZATION_ENV_NAMES)
    if env_authorization:
        return _parse_authorization_payload(
            env_authorization,
            source="env_authorization",
            cacheable=True,
        )

    vefaas_credentials = _get_vefaas_iam_credentials()
    if vefaas_credentials is not None:
        return vefaas_credentials

    raise ValueError(
        "Volcengine credentials are not configured. "
        "Set VOLCENGINE_ACCESS_KEY/VOLCENGINE_SECRET_KEY, provide authorization, or mount VeFaaS IAM credentials."
    )
