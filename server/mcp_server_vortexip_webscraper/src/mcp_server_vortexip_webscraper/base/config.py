import logging
import os
from dataclasses import dataclass


logger = logging.getLogger(__name__)
LOCAL_DEPLOY_MODE = "local"


@dataclass
class WebScraperConfig:
    """Configuration for Web Scraper MCP Server.

    Required environment variables:
        ENDPOINT: The access endpoint
        TOKEN: The token for authentication
    """
    endpoint: str
    token: str


def load_config() -> WebScraperConfig:

    config = WebScraperConfig(
        endpoint=os.getenv("ENDPOINT", ""),
        token=os.getenv("TOKEN", ""),
    )
    logger.info(f"Success to loaded configuration")

    return config


WEB_SCRAPER_CONFIG = load_config()
