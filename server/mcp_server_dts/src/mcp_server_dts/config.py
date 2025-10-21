import os
import logging
import json
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class DtsConfig:
    """Configuration for DTS MCP Server."""
    region: str
    access_key_id: str
    access_key_secret: str
    endpoint: str

def load_config(config_path: str = None) -> DtsConfig:
    """Load configuration from file."""
    if config_path:
        try:
            with open(config_path) as f:
                config_data = json.load(f)
                env_vars = config_data.get('env', {})

                return DtsConfig(
                    region=env_vars.get("VOLCENGINE_REGION", os.getenv("VOLCENGINE_REGION"), "cn-beijing"),
                    access_key_id=env_vars.get("VOLCENGINE_ACCESS_KEY", os.environ["VOLCENGINE_ACCESS_KEY"]),
                    secret=env_vars.get("VOLCENGINE_SECRET_KEY", os.environ["VOLCENGINE_SECRET_KEY"]),
                    endpoint=env_vars.get("VOLCENGINE_ENDPOINT", os.environ["VOLCENGINE_ENDPOINT"])
                )
        except Exception as e:
            logger.warning(f"Failed to load config file, fallback to env vars: {str(e)}")          
            
    required_vars= [ "VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY", "VOLCENGINE_ENDPOINT"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
                raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    return DtsConfig(
                    region=os.getenv("VOLCENGINE_REGION", "cn-beijing"),
                    access_key_id=os.environ["VOLCENGINE_ACCESS_KEY"],
                    access_key_secret=os.environ["VOLCENGINE_SECRET_KEY"],
                    endpoint=os.environ["VOLCENGINE_ENDPOINT"]
                )
