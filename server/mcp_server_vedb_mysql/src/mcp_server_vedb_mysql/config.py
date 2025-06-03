import os
import logging
import json
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class VedbMysqlConfig:
    """Configuration for Storage EBS MCP Server."""
    region: str
    zone: str
    access_key_id: str
    access_key_secret: str
    account_id: str
    endpoint: str



def load_config(config_path: str = None) -> VedbMysqlConfig:
    """Load configuration from config file or environment variables."""
    # 优先从config文件加载
    if config_path:
        try:
            with open(config_path) as f:
                config_data = json.load(f)
                env_vars = config_data.get('env', {})
                
                return VedbMysqlConfig(
                    region=env_vars.get("VOLCENGINE_REGION", os.getenv("VOLCENGINE_REGION", "cn-beijing")),
                    access_key_id=env_vars.get("VOLCENGINE_ACCESS_KEY", os.environ["VOLCENGINE_ACCESS_KEY"]),
                    access_key_secret=env_vars.get("VOLCENGINE_SECRET_KEY", os.environ["VOLCENGINE_SECRET_KEY"]),
                    account_id="",
                    endpoint=env_vars.get("VOLCENGINE_ENDPOINT", os.getenv("VOLCENGINE_ENDPOINT", "")),
                    zone=""
                )
        except Exception as e:
            logger.warning(f"Failed to load config file, fallback to env vars: {str(e)}")
    
    # 从环境变量加载
    required_vars = ["VOLCENGINE_ACCESS_KEY", "VOLCENGINE_SECRET_KEY", "VOLCENGINE_REGION"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
    return VedbMysqlConfig(
        region=os.getenv("VOLCENGINE_REGION", "cn-beijing"),
        access_key_id=os.environ["VOLCENGINE_ACCESS_KEY"],
        access_key_secret=os.environ["VOLCENGINE_SECRET_KEY"],
        account_id="",
        endpoint=os.getenv("VOLCENGINE_ENDPOINT", ""),
        zone=""
    )
