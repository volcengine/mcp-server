"""Separate MCP caller identity from request-scoped SMS credentials."""

import base64
import json
import os
import threading

import httpx
import jwt

from .core.api_protocol import ResolvedCredentials


class AuthenticationError(ValueError):
    pass


def subject_identity(issuer: str, subject: str) -> str:
    return json.dumps([issuer, subject], separators=(",", ":"))


class Authenticator:
    def __init__(self, settings):
        self.settings = settings
        self._keys = None
        self._lock = threading.Lock()

    def owner(self, headers):
        value = headers.get("authorization", "")
        scheme, _, token = value.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise AuthenticationError("需要有效的 MCP 访问令牌")
        try:
            with self._lock:
                if self._keys is None:
                    metadata_url = (
                        self.settings.oidc_issuer.rstrip("/")
                        + "/.well-known/openid-configuration"
                    )
                    response = httpx.get(metadata_url, timeout=10)
                    response.raise_for_status()
                    metadata = response.json()
                    if metadata["issuer"] != self.settings.oidc_issuer or not metadata[
                        "jwks_uri"
                    ].startswith("https://"):
                        raise ValueError("Invalid issuer metadata")
                    self._keys = jwt.PyJWKClient(metadata["jwks_uri"], timeout=10)
            key = self._keys.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token,
                key.key,
                algorithms=["RS256", "ES256"],
                issuer=self.settings.oidc_issuer,
                audience=self.settings.token_audience,
                options={"require": ["exp", "iss", "aud", "sub"]},
            )
            if not isinstance(claims["sub"], str) or not claims["sub"]:
                raise ValueError("Missing subject")
            return subject_identity(claims["iss"], claims["sub"])
        except Exception as exc:
            raise AuthenticationError("MCP 访问令牌无效或暂时无法验证") from exc


def sms_credentials(headers=None):
    if headers is None:
        values = {
            "AccessKeyId": os.getenv("VOLCENGINE_ACCESS_KEY", ""),
            "SecretAccessKey": os.getenv("VOLCENGINE_SECRET_KEY", ""),
            "SessionToken": os.getenv("VOLCENGINE_SESSION_TOKEN", ""),
        }
    else:
        encoded = headers.get("x-volcengine-credentials", "")
        try:
            if len(encoded) > 16384:
                raise ValueError("oversized header")
            values = json.loads(base64.b64decode(encoded, validate=True))
            if not isinstance(values, dict):
                raise ValueError("invalid credential object")
        except Exception as exc:
            raise AuthenticationError("缺少或无法解析短信调用凭据") from exc
    if any(
        not isinstance(values.get(key), str) or not values[key]
        for key in ("AccessKeyId", "SecretAccessKey")
    ):
        raise AuthenticationError("短信调用凭据不完整")
    if not isinstance(values.get("SessionToken", ""), str):
        raise AuthenticationError("短信临时凭据格式无效")
    return ResolvedCredentials(
        values["AccessKeyId"], values["SecretAccessKey"], values.get("SessionToken", "")
    )
