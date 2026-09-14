"""Request-scoped V4 SMS client; no CLI, login process, or credential fallback."""

import datetime
import time
from typing import Any, Callable

from .action_contracts import ACTION_REGISTRY
from .api_protocol import (
    ResolvedCredentials,
    RequestNotSentError,
    TransportResponse,
    _error_envelope,
    _urllib_transport,
    build_signed_request,
    emit_json as emit_json,
    normalize_response,
)


class SmsApiClient:
    def __init__(
        self,
        credentials: ResolvedCredentials,
        *,
        timeout: float = 15,
        transport: Callable[..., TransportResponse] = _urllib_transport,
    ):
        self.credentials = credentials
        self._timeout = timeout
        self._transport = transport

    def call(
        self, action: str, params: Any, *, preserve_presigned_url: bool = False
    ) -> dict:
        spec = ACTION_REGISTRY[action]
        credentials = self.credentials
        secrets = tuple(
            filter(
                None,
                (
                    credentials.access_key,
                    credentials.secret_key,
                    credentials.session_token,
                ),
            )
        )
        for attempt in range(3 if spec.read_only else 1):
            signed = build_signed_request(
                spec,
                params,
                credentials.access_key,
                credentials.secret_key,
                datetime.datetime.now(datetime.timezone.utc),
                action=action,
                session_token=credentials.session_token,
            )
            try:
                response = self._transport(signed.to_urllib_request(), self._timeout)
                result = normalize_response(
                    action,
                    spec,
                    response,
                    secrets,
                    preserve_presigned_url=preserve_presigned_url,
                )
            except RequestNotSentError:
                result = _error_envelope(
                    action, "network_error", "请求尚未发出", retryable=spec.read_only
                )
            except Exception:
                # Once dispatch started, an unexpected transport failure cannot prove
                # a mutation was not accepted. Never replay it.
                result = _error_envelope(
                    action,
                    "network_error" if spec.read_only else "outcome_unknown",
                    "请求结果暂时无法确认",
                    retryable=spec.read_only,
                    outcome_unknown=not spec.read_only,
                )
            if (
                spec.read_only
                and attempt < 2
                and (result.get("error") or {}).get("retryable")
            ):
                time.sleep(0.5 * 2**attempt)
                continue
            return result
        raise RuntimeError("Unreachable retry state")
