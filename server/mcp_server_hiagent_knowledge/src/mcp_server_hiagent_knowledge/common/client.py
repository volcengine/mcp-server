"""Minimal HiAgent OpenAPI client."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass

from mcp_server_hiagent_knowledge.common.config import HiAgentConfig
from mcp_server_hiagent_knowledge.common.signer import sign_openapi_request
from mcp_server_hiagent_knowledge.common.tools._common import (
    OPENAPI_VERSION as DEFAULT_OPENAPI_VERSION,
)


@dataclass(frozen=True)
class OpenAPIError(Exception):
    """Error raised when HiAgent Platform API reports a failure."""

    status_code: int
    message: str

    def __str__(self) -> str:
        return f"HiAgent OpenAPI request failed: {self.status_code} {self.message}"


def _parse_response(raw: bytes, status_code: int) -> dict[str, object]:
    if not raw:
        if status_code >= 400:
            raise OpenAPIError(status_code, "")
        return {}

    decoded = raw.decode("utf-8")
    try:
        payload = json.loads(decoded)
    except json.JSONDecodeError:
        if status_code >= 400:
            raise OpenAPIError(status_code, decoded) from None
        raise

    metadata = payload.get("ResponseMetadata")
    if isinstance(metadata, dict):
        error = metadata.get("Error")
        if isinstance(error, dict):
            code = str(error.get("Code", "UnknownError"))
            message = str(error.get("Message", ""))
            raise OpenAPIError(status_code, f"{code}: {message}")
    if status_code >= 400:
        raise OpenAPIError(status_code, decoded)
    return payload


class HiAgentOpenAPIClient:
    """Small signed client for HiAgent OpenAPI requests."""

    def __init__(self, config: HiAgentConfig) -> None:
        self._config = config

    @property
    def is_configured(self) -> bool:
        return self._config.is_configured

    def call(
        self,
        *,
        action: str,
        body: Mapping[str, object] | None = None,
        version: str = DEFAULT_OPENAPI_VERSION,
        service: str | None = None,
        timeout_seconds: float = 30,
    ) -> dict[str, object]:
        """Call a HiAgent OpenAPI action with AK/SK V4 signing."""

        if not self._config.is_configured:
            raise ValueError(
                "HIAGENT_TOP_HOST, HIAGENT_ACCOUNT_ID, "
                "HIAGENT_ACCESS_KEY_ID, and HIAGENT_SECRET_ACCESS_KEY are required"
            )

        signed = sign_openapi_request(
            top_host=self._config.top_host,
            action=action,
            version=version,
            account_id=self._config.account_id,
            access_key_id=self._config.access_key_id,
            secret_access_key=self._config.secret_access_key,
            region=self._config.region,
            service=service or self._config.service,
            body=body,
        )
        request = urllib.request.Request(
            signed.url,
            data=signed.body,
            headers=signed.headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            try:
                return _parse_response(exc.read(), exc.code)
            except OpenAPIError as error:
                raise error from exc

        return _parse_response(raw, 200)
