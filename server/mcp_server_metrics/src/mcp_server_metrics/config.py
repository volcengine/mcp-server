import base64
import json
import logging
import os
from dataclasses import dataclass

from volcenginesdkcore.signv4 import SignerV4

logger = logging.getLogger(__name__)

VOLCENGINE_ACCESS_KEY = "VOLCENGINE_ACCESS_KEY"
VOLCENGINE_SECRET_KEY = "VOLCENGINE_SECRET_KEY"
VOLCENGINE_SESSION_TOKEN = "VOLCENGINE_SESSION_TOKEN"
VOLCENGINE_REGION = "VOLCENGINE_REGION"
VOLCENGINE_ENDPOINT = "VOLCENGINE_ENDPOINT"
METRICS_WORKSPACE_NAME = "METRICS_WORKSPACE_NAME"

MCP_SERVER_NAME = "MCP_SERVER_NAME"
MCP_SERVER_MODE = "MCP_SERVER_MODE"
MCP_SERVER_PORT = "MCP_SERVER_PORT"
MCP_SERVER_HOST = "MCP_SERVER_HOST"

DEFAULT_REGION = "cn-beijing"


@dataclass
class MetricsConfig:
    """Configuration for Metrics MCP Server.

    Required environment variables:
        VOLCENGINE_ACCESS_KEY: The Access key ID for authentication
        VOLCENGINE_SECRET_KEY: Access key secret for authentication
        VOLCENGINE_REGION: The region of the Metrics service
        METRICS_WORKSPACE_NAME: The workspace name of the Metrics service
    """

    access_key: str
    secret_key: str
    session_token: str
    region: str
    endpoint: str
    workspace_name: str

    def is_valid(self) -> bool:
        """Check if the configuration is valid."""
        if self.access_key == "" and self.secret_key == "" and self.session_token == "":
            return False
        return True

    def get_endpoint(self, region: str) -> str:
        """Get endpoint based on region."""
        return f"https://metrics.{region}.volcengineapi.com"

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
    for var in [VOLCENGINE_ACCESS_KEY, VOLCENGINE_SECRET_KEY]:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


def load_config() -> MetricsConfig:
    region = os.getenv(VOLCENGINE_REGION, DEFAULT_REGION)
    endpoint = f"https://metrics.{region}.volcengineapi.com"

    config = MetricsConfig(
        access_key=os.getenv(VOLCENGINE_ACCESS_KEY, ""),
        secret_key=os.getenv(VOLCENGINE_SECRET_KEY, ""),
        session_token=os.getenv(VOLCENGINE_SESSION_TOKEN, ""),
        region=region,
        endpoint=endpoint,
        workspace_name=os.getenv(METRICS_WORKSPACE_NAME, ""),
    )
    logger.info(f"Loaded configuration")

    return config


def parse_authorization(authorization: str) -> MetricsConfig:
    b = base64.standard_b64decode(authorization)
    auth_obj = json.loads(b.decode("utf-8"))

    access_key = auth_obj.get("AccessKeyId") or auth_obj.get("access_key_id") or ""
    secret_key = auth_obj.get("SecretAccessKey") or auth_obj.get("secret_access_key") or ""
    session_token = auth_obj.get("SessionToken") or auth_obj.get("session_token") or ""
    region = os.getenv(VOLCENGINE_REGION, DEFAULT_REGION)
    endpoint = f"https://metrics.{region}.volcengineapi.com"

    workspace_name = os.getenv(METRICS_WORKSPACE_NAME, "")
    
    return MetricsConfig(
        access_key=access_key,
        secret_key=secret_key,
        session_token=session_token,
        endpoint=endpoint,
        region=region,
        workspace_name=workspace_name,
    )
