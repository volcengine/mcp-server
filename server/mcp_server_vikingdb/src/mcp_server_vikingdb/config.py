import os
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class VikingdbConfig:
    """Configuration for Vikingdb MCP Server."""
    ak: str
    sk: str
    vikingdb_collection_name: str
    vikingdb_index_name: str
    region: str = "cn-north-1"

def load_config() -> VikingdbConfig:
    """Load configuration from environment variables."""
    required_vars = [
        "VOLCENGINE_ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY",
        "VIKING_DB_COLLECTION_NAME",
        "VIKING_DB_INDEX_NAME",
        "VIKING_DB_REGION"
    ]

    # Check if all required environment variables are set
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Load configuration from environment variables
    return VikingdbConfig(
        ak=os.environ["VOLCENGINE_ACCESS_KEY"],
        sk=os.environ["VOLCENGINE_SECRET_KEY"],
        vikingdb_collection_name=os.environ["VIKING_DB_COLLECTION_NAME"],
        vikingdb_index_name=os.environ["VIKING_DB_INDEX_NAME"],
        region=os.environ.get("VIKING_DB_REGION", "cn-north-1")
    )


config = load_config()
