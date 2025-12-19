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
    # Accept either VOLCENGINE_ACCESS_KEY or VOLC_ACCESSKEY (and similarly for secret key)
    access_key = os.environ.get("VOLCENGINE_ACCESS_KEY") or os.environ.get("VOLC_ACCESSKEY")
    secret_key = os.environ.get("VOLCENGINE_SECRET_KEY") or os.environ.get("VOLC_SECRETKEY")

    # Check if we have at least one variant of the required variables
    if not access_key:
        error_msg = "Missing required environment variable: VOLCENGINE_ACCESS_KEY or VOLC_ACCESSKEY"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    if not secret_key:
        error_msg = "Missing required environment variable: VOLCENGINE_SECRET_KEY or VOLC_SECRETKEY"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Load configuration from environment variables
    return LASConfig(
        endpoint=os.getenv("VOLCENGINE_ENDPOINT", "https://las-cn-beijing.volces.com"),
        region=os.getenv("REGION", "cn-beijing"),
        access_key_id=access_key,
        access_key_secret=secret_key,
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
