import logging
import os
from dataclasses import dataclass

from mcp_server_na.common.client import NAClient

logger = logging.getLogger(__name__)


@dataclass
class NetworkAdvisorConfig:
    """Configuration for Storage NetworkAdvisor MCP Server.

    Required environment variables:
        VOLCENGINE_ACCESS_KEY: The access key for authentication
        VOLCENGINE_SECRET_KEY: The secret key for authentication
        VOLCENGINE_REGION:     The region of the service
    """
    access_key: str
    secret_key: str
    region: str
    host: str


def validate_local_required_vars():
    """
    Validate that all required environment variables are set.

    Raises:
    ValueError: If any required environment variable is missing.
    """
    missing_vars = []
    for var in ["VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY", "VOLCENGINE_REGION", "VOLCENGINE_ENDPOINT"]:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


def load_config() -> NetworkAdvisorConfig:
    validate_local_required_vars()

    config = NetworkAdvisorConfig(
        access_key=os.getenv("VOLCENGINE_ACCESS_KEY", ""),
        secret_key=os.getenv("VOLCENGINE_SECRET_KEY", ""),
        region=os.getenv("VOLCENGINE_REGION", ""),
        host=os.getenv("VOLCENGINE_ENDPOINT", ""),
    )
    logger.info("Success to Loaded configuration")

    return config


NA_CONFIG = load_config()
