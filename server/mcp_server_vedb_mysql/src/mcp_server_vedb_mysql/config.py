import os
import logging
import json  # 新增导入
from dataclasses import dataclass
from pathlib import Path  # 新增导入

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
                    region=env_vars.get("REGION", os.getenv("REGION", "cn-beijing")),
                    access_key_id=env_vars.get("VOLC_ACCESSKEY", os.environ["VOLC_ACCESSKEY"]),
                    access_key_secret=env_vars.get("VOLC_SECRETKEY", os.environ["VOLC_SECRETKEY"]),
                    account_id=env_vars.get("ACCOUNT_ID", os.getenv("ACCOUNT_ID", "")),
                    endpoint=env_vars.get("ENDPOINT", os.getenv("ENDPOINT", "")),
                    zone=env_vars.get("ZONE", os.getenv("ZONE", ""))
                )
        except Exception as e:
            logger.warning(f"Failed to load config file, fallback to env vars: {str(e)}")
    
    # 从环境变量加载
    required_vars = ["VOLC_ACCESSKEY", "VOLC_SECRETKEY", "REGION"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
    return VedbMysqlConfig(
        region=os.getenv("REGION", "cn-beijing"),
        access_key_id=os.environ["VOLC_ACCESSKEY"],
        access_key_secret=os.environ["VOLC_SECRETKEY"],
        account_id=os.getenv("ACCOUNT_ID", ""),
        endpoint=os.getenv("ENDPOINT", ""),
        zone=os.getenv("ZONE", "")
    )
