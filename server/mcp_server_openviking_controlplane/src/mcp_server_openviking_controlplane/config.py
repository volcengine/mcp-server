import logging
import os
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

# The control-plane TopAPI is compiled into the OpenViking data-plane cluster.
# Each Action is served at:  {endpoint}/api/openviking/{Action}
#   - Action/Version live in the path; there is NO ?Action=&Version= query.
#   - Auth is an Ark AgentPlan ApiKey replayed as: Authorization: Bearer <key>.
ACTION_PATH_PREFIX = "/api/openviking"

# Reserved public data-plane gateway (not open to traffic yet). The trailing
# /openviking base is the same prefix the data-plane APIs use, so the full URL
# is {endpoint}/api/openviking/{Action}. Override via VIKING_ENDPOINT / --endpoint
# while testing — e.g. a kubectl port-forward to the data pod: http://localhost:18080
DEFAULT_ENDPOINT = "https://api.vikingdb.cn-beijing.volces.com/openviking"
DEFAULT_PROJECT = "default"

# Model names for AgentPlan collections. The backend's prefix check only accepts
# these names for VLM / Embedding respectively, so they double as fixed defaults.
DEFAULT_VLM_MODEL = "doubao-seed-2.0-lite"
DEFAULT_EMBEDDING_MODEL = "doubao-embedding-vision"


@dataclass
class ControlPlaneConfig:
    """Configuration for the OpenViking control plane MCP server / CLI."""

    api_key: str
    endpoint: str = DEFAULT_ENDPOINT
    project: str = DEFAULT_PROJECT

    @property
    def base_url(self) -> str:
        return self.endpoint.rstrip("/")

    def action_path(self, action: str) -> str:
        return f"{ACTION_PATH_PREFIX}/{action}"


def build_config(
    endpoint: Optional[str] = None,
    project: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ControlPlaneConfig:
    """Build a config from explicit args first, then environment fallbacks, then
    package defaults."""
    resolved_key = api_key or os.environ.get("VIKING_API_KEY")
    if not resolved_key:
        raise ValueError(
            "missing AgentPlan API key: set --api-key or the VIKING_API_KEY env var "
            "(the Ark AgentPlan ApiKey sent as 'Authorization: Bearer <key>')"
        )
    return ControlPlaneConfig(
        api_key=resolved_key,
        endpoint=endpoint or os.environ.get("VIKING_ENDPOINT", DEFAULT_ENDPOINT),
        project=project or os.environ.get("OPENVIKING_PROJECT", DEFAULT_PROJECT),
    )


_config: Optional[ControlPlaneConfig] = None


def get_config() -> ControlPlaneConfig:
    """Lazy, cached config built purely from the environment (used by the MCP server)."""
    global _config
    if _config is None:
        _config = build_config()
    return _config
