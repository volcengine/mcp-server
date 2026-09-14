"""Explicit configuration for the independently deployed MCP service."""

import os
from dataclasses import dataclass, field
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Settings:
    database_url: str = field(repr=False)
    encryption_key: str = field(repr=False)
    public_url: str = ""
    oidc_issuer: str = ""
    token_audience: str = ""
    input_root: str = ""
    flow_ttl: int = 1800
    operation_ttl: int = 86400

    def __post_init__(self):
        if not 60 <= self.flow_ttl <= self.operation_ttl:
            raise ValueError("TTL must satisfy 60 <= flow TTL <= operation TTL")
        if self.input_root and not os.path.isabs(self.input_root):
            raise ValueError("SMS_MCP_INPUT_ROOT must be an absolute directory path")

    @classmethod
    def from_env(cls):
        required = ("SMS_MCP_DATABASE_URL", "SMS_MCP_ENCRYPTION_KEY")
        missing = [key for key in required if not os.environ.get(key)]
        if missing:
            raise ValueError("Missing configuration: " + ", ".join(missing))
        return cls(
            database_url=os.environ[required[0]],
            encryption_key=os.environ[required[1]],
            public_url=os.getenv("SMS_MCP_PUBLIC_URL", ""),
            oidc_issuer=os.getenv("SMS_MCP_OIDC_ISSUER", ""),
            token_audience=os.getenv("SMS_MCP_TOKEN_AUDIENCE", ""),
            input_root=os.getenv("SMS_MCP_INPUT_ROOT", ""),
            flow_ttl=int(os.getenv("SMS_MCP_FLOW_TTL", "1800")),
            operation_ttl=int(os.getenv("SMS_MCP_OPERATION_TTL", "86400")),
        )

    def validate_http(self):
        for key in (
            "public_url",
            "oidc_issuer",
            "token_audience",
        ):
            if not getattr(self, key):
                raise ValueError(f"HTTP mode requires {key}")
        for value in (self.public_url, self.oidc_issuer):
            parsed = urlsplit(value)
            if (
                parsed.scheme != "https"
                or not parsed.netloc
                or parsed.query
                or parsed.fragment
                or parsed.username
            ):
                raise ValueError(
                    "Public URL and OIDC issuer must be HTTPS URLs without credentials/query/fragment"
                )
        if urlsplit(self.public_url).path not in ("", "/"):
            raise ValueError(
                "SMS_MCP_PUBLIC_URL must be an origin; mount this service at its root"
            )
        if not 60 <= self.flow_ttl <= self.operation_ttl:
            raise ValueError("TTL must satisfy 60 <= flow TTL <= operation TTL")
