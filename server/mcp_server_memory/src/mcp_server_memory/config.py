import os
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class MemoryConfig:
    """Configuration for Viking Memory MCP Server."""
    ak: str
    sk: str
    user_id: str
    project: Optional[str] = None
    region: str = "cn-north-1"
    collection_name: str = 'public_test_collection'


def load_config() -> MemoryConfig:
    """Load configuration from environment variables."""
    required_vars = [
        "VOLCENGINE_ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY",
        "MEMORY_PROJECT",
        "MEMORY_REGION",
        "MEMORY_COLLECTION_NAME"
    ]

    # Check if all required environment variables are set
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        # raise ValueError(error_msg)

    # Load configuration from environment variables
    return MemoryConfig(
        ak=os.environ.get("VOLCENGINE_ACCESS_KEY"),
        sk=os.environ.get("VOLCENGINE_SECRET_KEY"),
        user_id=os.environ.get("MEMORY_USER_ID"),
        project=os.environ.get("MEMORY_PROJECT","default"),
        region=os.environ.get("MEMORY_REGION", "cn-north-1"),
        collection_name=os.environ.get("MEMORY_COLLECTION_NAME", "public_test_collection")
    )


config = load_config()
