import logging
import os
from dataclasses import dataclass
from typing import List, Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
LOCAL_DEPLOY_MODE = "local"
REMOTE_DEPLOY_MODE = "remote"


@dataclass
class TosConfig:
    """Configuration for Storage TOS MCP Server.

    Required environment variables:
        VOLCENGINE_ACCESS_KEY: The Access key ID for authentication
        VOLCENGINE_SECRET_KEY: Access key secret for authentication
        TOS_ENDPOINT:   The TOS service endpoint
        VOLCENGINE_REGION:         The region of the TOS service
        DEPLOY_MODE:    The deployment mode
        TOS_BUCKETS:    The bucket list to use for the TOS service
        MAX_OBJECT_SIZE: The maximum size of an object in bytes
    """
    access_key: str
    secret_key: str
    region: str
    endpoint: str
    security_token: str
    deploy_mode: str
    max_object_size: int
    buckets: List[str]


def validate_local_required_vars():
    """
    Validate that all required environment variables are set.

    Raises:
    ValueError: If any required environment variable is missing.
    """
    missing_vars = []
    for var in ["VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY", "TOS_ENDPOINT"]:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


def validate_remote_required_vars():
    """
    Validate that all required environment variables are set.

    Raises:
    ValueError: If any required environment variable is missing.
    """
    missing_vars = []
    for var in ["TOS_ENDPOINT"]:
        if var not in os.environ:
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


def load_config() -> TosConfig:
    deploy_mode = os.getenv("DEPLOY_MODE", LOCAL_DEPLOY_MODE)
    if deploy_mode == LOCAL_DEPLOY_MODE:
        validate_local_required_vars()
    else:
        validate_remote_required_vars()

    config = TosConfig(
        access_key=os.getenv("VOLCENGINE_ACCESS_KEY", ""),
        secret_key=os.getenv("VOLCENGINE_SECRET_KEY", ""),
        region=os.getenv("VOLCENGINE_REGION", ""),
        endpoint=os.environ["TOS_ENDPOINT"],
        security_token=os.getenv("SECURITY_TOKEN", ""),
        deploy_mode=deploy_mode,
        buckets=os.getenv("TOS_BUCKETS", "").split(","),
        max_object_size=int(os.getenv("MAX_OBJECT_SIZE", "262144")),
    )
    logger.info(f"Loaded configuration, endpoint: {config.endpoint}, region: {config.region} buckets: {config.buckets}")

    return config


load_dotenv()

TOS_CONFIG = load_config()
