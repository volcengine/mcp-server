"""Per-call credentials. HTTP never falls back to the server's environment."""

import base64
import binascii
import json
import os
from collections.abc import Mapping
from dataclasses import dataclass


class AuthenticationError(ValueError):
    pass


@dataclass(frozen=True, repr=False)
class Credentials:
    access_key: str
    secret_key: str
    session_token: str = ""

    @classmethod
    def from_headers(cls, headers: Mapping[str, str] | None):
        if headers is None:
            values = {
                "AccessKeyId": os.getenv("VOLCENGINE_ACCESS_KEY"),
                "SecretAccessKey": os.getenv("VOLCENGINE_SECRET_KEY"),
                "SessionToken": os.getenv("VOLCENGINE_SESSION_TOKEN", ""),
            }
        else:
            authorization = headers.get("authorization", "")
            scheme, separator, encoded = authorization.partition(" ")
            if not separator or scheme.lower() != "bearer" or len(encoded) > 16384:
                raise AuthenticationError("需要 Authorization: Bearer <Base64 JSON 短信凭据>")
            try:
                values = json.loads(base64.b64decode(encoded, validate=True))
            except (ValueError, UnicodeError, binascii.Error):
                raise AuthenticationError("短信调用凭据格式无效") from None
        if not isinstance(values, dict) or any(
            not isinstance(values.get(key), str) or not values[key]
            for key in ("AccessKeyId", "SecretAccessKey")
        ):
            raise AuthenticationError("需要完整的短信 AccessKeyId 和 SecretAccessKey")
        token = values.get("SessionToken", "")
        if not isinstance(token, str):
            raise AuthenticationError("SessionToken 必须是字符串")
        return cls(values["AccessKeyId"], values["SecretAccessKey"], token)
