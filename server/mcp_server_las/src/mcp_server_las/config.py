import os
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)
DEFAULT_DATASET = 'ds_public'

@dataclass
class LASConfig:
    """Configuration for LAS MCP Server."""

    endpoint: str
    region: str
    access_key_id: str
    access_key_secret: str
    session_token: str
    dataset_id: str



def load_config() -> LASConfig:
    """Load configuration from environment variables."""
    required_vars = [
        "VOLCENGINE_ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY",
    ]

    # Check if all required environment variables are set
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Load configuration from environment variables
    return LASConfig(
        endpoint=os.getenv("VOLCENGINE_ENDPOINT", "https://las-cn-beijing.volces.com"),
        region=os.getenv("REGION", "cn-beijing"),
        access_key_id=os.environ["VOLCENGINE_ACCESS_KEY"],
        access_key_secret=os.environ["VOLCENGINE_SECRET_KEY"],
        session_token='',
        dataset_id=os.getenv("LAS_DATASET_ID", ""),
    )

def load_config_by_sts(ak, sk, session_token) -> LASConfig:
    """Load configuration from environment variables."""
    return LASConfig(
        endpoint=os.getenv("VOLCENGINE_ENDPOINT", "https://las-cn-beijing.volces.com"),
        region=os.getenv("REGION", "cn-beijing"),
        access_key_id=ak,
        access_key_secret=sk,
        session_token=session_token,
        dataset_id=os.getenv("LAS_DATASET_ID", DEFAULT_DATASET),
    )
