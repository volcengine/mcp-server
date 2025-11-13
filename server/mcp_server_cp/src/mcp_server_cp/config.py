import os

from dataclasses import dataclass


@dataclass
class CodePipelineConfig:
    """Configuration for CodePipeline MCP Server."""

    volcengine_endpoint: str
    volcengine_ak: str
    volcengine_sk: str
    volcengine_region: str
    session_token: str


def load_config() -> CodePipelineConfig:
    """Load configuration from environment variables."""
    return CodePipelineConfig(
        volcengine_endpoint=os.environ["VOLCENGINE_ENDPOINT"],
        volcengine_ak=os.environ["VOLCENGINE_ACCESS_KEY"],
        volcengine_sk=os.environ["VOLCENGINE_SECRET_KEY"],
        volcengine_region=os.environ.get("VOLCENGINE_REGION", "cn-beijing"),
        session_token="",
    )