import os
from dataclasses import dataclass
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

ENV_ASKECHO_BOT_ID = "ASKECHO_BOT_ID"
ENV_VOLCENGINE_ACCESS_KEY = "VOLCENGINE_ACCESS_KEY"
ENV_VOLCENGINE_SECRET_KEY = "VOLCENGINE_SECRET_KEY"


@dataclass
class AskEchoConfig:
    bot_id: str
    volcengine_ak: str
    volcengine_sk: str


def load_config() -> AskEchoConfig:
    """Load configuration from environment variables."""
    try:
        required_vars = [ENV_ASKECHO_BOT_ID, ENV_VOLCENGINE_ACCESS_KEY, ENV_VOLCENGINE_SECRET_KEY]
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        logger.info(f"Loaded configuration from environment")
        return AskEchoConfig(
            bot_id=os.environ.get(ENV_ASKECHO_BOT_ID),
            volcengine_ak=os.environ.get(ENV_VOLCENGINE_ACCESS_KEY),
            volcengine_sk=os.environ.get(ENV_VOLCENGINE_SECRET_KEY)
        )
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise
