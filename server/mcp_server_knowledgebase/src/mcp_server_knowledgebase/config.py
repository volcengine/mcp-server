import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class KnowledgeBaseConfig:
    """Configuration for Viking Knowledge Base MCP Server."""

    ak: Optional[str] = None
    sk: Optional[str] = None
    project: Optional[str] = None
    region: str = "cn-north-1"
    api_key: Optional[str] = None


def _credential_from_env(name: str) -> Optional[str]:
    value = os.environ.get(name)
    if value is None:
        return None
    return value.strip() or None


def load_config() -> KnowledgeBaseConfig:
    """Load configuration from environment variables."""
    ak = _credential_from_env("VOLCENGINE_ACCESS_KEY")
    sk = _credential_from_env("VOLCENGINE_SECRET_KEY")
    api_key = _credential_from_env("VIKING_API_KEY")

    if not api_key and bool(ak) != bool(sk):
        error_msg = (
            "VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY must be configured together"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    if not api_key and not (ak and sk):
        error_msg = (
            "Configure an authentication method: VIKING_API_KEY or "
            "VOLCENGINE_ACCESS_KEY with VOLCENGINE_SECRET_KEY"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    return KnowledgeBaseConfig(
        ak=ak,
        sk=sk,
        api_key=api_key,
        project=os.getenv("KNOWLEDGE_BASE_PROJECT", "").strip() or "default",
        region=os.environ.get("KNOWLEDGE_BASE_REGION", "cn-north-1"),
    )


config = load_config()
