import os
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class AISearchEngineConfig:
    """Configuration for AI Search Engine MCP Server."""
    ak: str
    sk: str
    region: str = "cn-beijing"



def validate_local_required_config():
    """
    Validate that all required environment variables are set.

    Raises:
    ValueError: If any required environment variable is missing.
    """
    required_vars = [
        "VOLCENGINE_ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY"
    ]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        #raise ValueError(error_msg)

def load_config() -> AISearchEngineConfig:
    """Load configuration from environment variables."""
    validate_local_required_config()
    config = AISearchEngineConfig(
        ak=os.environ["VOLCENGINE_ACCESS_KEY"],
        sk=os.environ["VOLCENGINE_SECRET_KEY"],
        region=os.environ.get("AI_SEARCH_ENGINE_REGION", "cn-beijing")
    )
    logger.info("Success to Loaded configuration")

    return config

config = load_config()