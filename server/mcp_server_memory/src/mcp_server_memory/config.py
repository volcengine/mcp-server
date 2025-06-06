import os
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class MemoryConfig:
    """Configuration for Viking Knowledge Base MCP Server."""
    ak: str
    sk: str
    project: Optional[str] = None
    region: str = "cn-north-1"


def load_config() -> MemoryConfig:
    """Load configuration from environment variables."""
    required_vars = [
        "VOLCENGINE_ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY",
        "MEMORY_PROJECT",
        "MEMORY_REGION",
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
        project=os.environ.get("MEMORY_PROJECT","default"),
        region=os.environ.get("MEMORY_REGION", "cn-north-1")
    )


config = load_config()
