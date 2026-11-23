"""HiAgent application compatibility registry; versions own contract deltas."""
from importlib import import_module
from types import ModuleType

VERSION_PACKAGES = {
    "v3.1.0": "v3_1_0",
    "v3.2.1": "v3_2_1",
    "v3.3.0": "v3_3_0",
}
SUPPORTED_VERSIONS = tuple(VERSION_PACKAGES)

def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.lstrip("v").split("."))

DEFAULT_VERSION = max(SUPPORTED_VERSIONS, key=_version_key)

def load_version_module(version: str) -> ModuleType:
    package = VERSION_PACKAGES.get(version)
    if package is None:
        raise ValueError(f"unsupported HIAGENT_VERSION {version!r}; supported versions: {', '.join(SUPPORTED_VERSIONS)}")
    return import_module(f"mcp_server_hiagent_knowledge.versions.{package}")
