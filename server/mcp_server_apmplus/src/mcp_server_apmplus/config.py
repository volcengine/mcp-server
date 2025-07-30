import base64
import json
import logging
import os
from dataclasses import dataclass

from volcenginesdkcore.signv4 import SignerV4

logger = logging.getLogger(__name__)

ENV_VOLCENGINE_ENDPOINT = "VOLCENGINE_ENDPOINT"
ENV_VOLCENGINE_REGION = "VOLCENGINE_REGION"
ENV_VOLCENGINE_ACCESS_KEY = "VOLCENGINE_ACCESS_KEY"
ENV_VOLCENGINE_SECRET_KEY = "VOLCENGINE_SECRET_KEY"
ENV_VOLCENGINE_SESSION_TOKEN = "VOLCENGINE_SESSION_TOKEN"

ENV_MCP_SERVER_NAME = "MCP_SERVER_NAME"
ENV_MCP_SERVER_MODE = "MCP_SERVER_MODE"
ENV_MCP_SERVER_PORT = "MCP_SERVER_PORT"
ENV_MCP_SERVER_HOST = "MCP_SERVER_HOST"

DEFAULT_ENDPOINT = "https://open.volcengineapi.com"


@dataclass
class ApmplusConfig:
    """Configuration for Storage APMPlus MCP Server.

    Required environment variables:
        VOLCENGINE_ACCESS_KEY: The Access key ID for authentication
        VOLCENGINE_SECRET_KEY: Access key secret for authentication
    """

    endpoint: str
    access_key: str
    secret_key: str
    session_token: str

    def is_valid(self) -> bool:
        """Check if the configuration is valid."""
        if self.access_key == "" and self.secret_key == "" and self.session_token == "":
            return False
        return True

    def append_authorization(
        self, path, method, headers, body, post_params, query, region, service
    ):
        SignerV4.sign(
            path,
            method,
            headers,
            body,
            post_params,
            query,
            self.access_key,
            self.secret_key,
            region,
            service,
            self.session_token,
        )


def validate_required_vars():
    """
    Validate that all required environment variables are set.

    Raises:
    ValueError: If any required environment variable is missing.
    """
    missing_vars = []
    for var in [ENV_VOLCENGINE_ACCESS_KEY, ENV_VOLCENGINE_SECRET_KEY]:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


def load_config() -> ApmplusConfig:
    # validate_required_vars()  # 不强校验AKSK，允许通过authorization参数传入
    config = ApmplusConfig(
        access_key=os.getenv(ENV_VOLCENGINE_ACCESS_KEY, ""),
        secret_key=os.getenv(ENV_VOLCENGINE_SECRET_KEY, ""),
        session_token=os.getenv(ENV_VOLCENGINE_SESSION_TOKEN, ""),
        endpoint=os.getenv(ENV_VOLCENGINE_ENDPOINT, DEFAULT_ENDPOINT),
    )
    logger.info(f"Loaded configuration")

    return config


def parse_authorization(authorization: str) -> ApmplusConfig:
    b = base64.standard_b64decode(authorization)
    auth_obj = json.loads(b.decode("utf-8"))
    return ApmplusConfig(
        access_key=auth_obj["AccessKeyId"],
        secret_key=auth_obj["SecretAccessKey"],
        session_token=auth_obj["SessionToken"],
        endpoint=os.getenv(ENV_VOLCENGINE_ENDPOINT, DEFAULT_ENDPOINT),
    )
