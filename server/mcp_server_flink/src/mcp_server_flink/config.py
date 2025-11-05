import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@dataclass
class FlinkConfig:
    """Configuration for Serverless Flink MCP Server.

    Required environment variables:
        VOLCENGINE_ACCESS_KEY: The Access key ID for authentication
        VOLCENGINE_SECRET_KEY: Access key secret for authentication
        VOLCENGINE_REGION:  The region of the Serverless Flink
        VOLCENGINE_SERVICE: The service of the Serverless Flink
        VOLCENGINE_PROJECT_NAME: The project name of the Serverless Flink
        DEPLOY_MODE: The deployment mode
    """
    access_key: str
    secret_key: str
    region: str
    service: str
    project_name: str
    deploy_mode: str

    def is_valid(self) -> bool:
        """Check if the configuration is valid."""
        if self.access_key == "" and self.secret_key == "":
            return False
        return True


def load_config() -> FlinkConfig:
    config = FlinkConfig(
        access_key=os.getenv("VOLCENGINE_ACCESS_KEY", ""),
        secret_key=os.getenv("VOLCENGINE_SECRET_KEY", ""),
        region=os.getenv("VOLCENGINE_REGION", ""),
        service=os.getenv("VOLCENGINE_SERVICE", "flink"),
        project_name=os.getenv("VOLCENGINE_PROJECT_NAME", ""),
        deploy_mode=os.getenv("DEPLOY_MODE", "local")
    )
    logger.info(
        f"Loaded configuration, region: {config.region}, service: {config.service}, project name: {config.project_name}, deploy mode: {config.deploy_mode}")

    return config


load_dotenv()

DEFAULT_FLINK_CONFIG = load_config()
DEFAULT_DIRECTORY_NAME = "数据开发文件夹"
