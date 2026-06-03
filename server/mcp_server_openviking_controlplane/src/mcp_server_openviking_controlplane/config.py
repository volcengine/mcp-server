import json
import logging
import os
from dataclasses import dataclass
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Console control-plane proxy endpoint. The browser hits:
#   {schema}://{host}{PATH_PREFIX}/{service}/{region}/{api_version}/{Action}
# e.g. https://console.volcengine.com/api/top/vikingdb/cn-beijing/2025-06-09/ListOpenVikingCollections
# (Action/Version live in the path, not the query string; auth is cookie-based.)
PATH_PREFIX = "/api/top"
DEFAULT_HOST = "console.volcengine.com"
DEFAULT_SCHEMA = "https"
DEFAULT_REGION = "cn-beijing"
DEFAULT_SERVICE = "vikingdb"
DEFAULT_API_VERSION = "2025-06-09"
DEFAULT_PROJECT = "default"


@dataclass
class ControlPlaneConfig:
    """Configuration for the OpenViking control plane MCP server / CLI."""

    headers: Dict[str, str]
    host: str = DEFAULT_HOST
    schema: str = DEFAULT_SCHEMA
    region: str = DEFAULT_REGION
    service: str = DEFAULT_SERVICE
    api_version: str = DEFAULT_API_VERSION
    project: str = DEFAULT_PROJECT

    @property
    def base_url(self) -> str:
        return f"{self.schema}://{self.host}"

    def action_path(self, action: str) -> str:
        return f"{PATH_PREFIX}/{self.service}/{self.region}/{self.api_version}/{action}"


def parse_headers_blob(blob: str) -> Dict[str, str]:
    """Parse manually supplied headers.

    Accepts either a JSON object, or the raw ``Key: Value`` block you get from a
    browser's "Copy request headers" (HTTP/2 pseudo-headers like ``:authority``
    are skipped). Values may contain ``:`` (e.g. Cookie / URLs) — only the first
    colon on each line splits key from value.
    """
    blob = (blob or "").strip()
    if not blob:
        return {}

    if blob.startswith("{"):
        try:
            obj = json.loads(blob)
        except json.JSONDecodeError as e:
            raise ValueError(f"headers look like JSON but failed to parse: {e}")
        return {str(k): str(v) for k, v in obj.items()}

    headers: Dict[str, str] = {}
    for line in blob.splitlines():
        line = line.strip()
        if not line or line.startswith(":") or ":" not in line:
            continue  # skip blanks, HTTP/2 pseudo-headers, and non-header lines
        key, _, value = line.partition(":")
        key = key.strip()
        if key:
            headers[key] = value.strip()
    return headers


def _read_headers_file(path: str) -> Dict[str, str]:
    try:
        with open(os.path.expanduser(path), "r", encoding="utf-8") as f:
            return parse_headers_blob(f.read())
    except OSError as e:
        raise ValueError(f"failed to read headers file {path!r}: {e}")


def _resolve_headers(
    headers: Optional[Dict[str, str]], headers_file: Optional[str]
) -> Dict[str, str]:
    """Header sources, in precedence order: explicit dict > file arg >
    ``VIKING_HEADERS_FILE`` env (path) > ``VIKING_HEADERS`` env (inline)."""
    if headers:
        return dict(headers)
    if headers_file:
        return _read_headers_file(headers_file)
    if os.environ.get("VIKING_HEADERS_FILE"):
        return _read_headers_file(os.environ["VIKING_HEADERS_FILE"])
    if os.environ.get("VIKING_HEADERS"):
        return parse_headers_blob(os.environ["VIKING_HEADERS"])
    return {}


def build_config(
    host: Optional[str] = None,
    schema: Optional[str] = None,
    region: Optional[str] = None,
    service: Optional[str] = None,
    api_version: Optional[str] = None,
    project: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    headers_file: Optional[str] = None,
) -> ControlPlaneConfig:
    """Build a config from explicit args first, then environment fallbacks, then
    package defaults (the console-proxy values)."""
    resolved_headers = _resolve_headers(headers, headers_file)
    if not resolved_headers:
        raise ValueError(
            "missing auth headers: set --headers-file / --header, or VIKING_HEADERS_FILE "
            "(path) / VIKING_HEADERS (inline JSON or raw 'Key: Value' lines)"
        )

    return ControlPlaneConfig(
        headers=resolved_headers,
        host=host or os.environ.get("VIKING_HOST", DEFAULT_HOST),
        schema=schema or os.environ.get("VIKING_SCHEMA", DEFAULT_SCHEMA),
        region=region or os.environ.get("VIKING_REGION", DEFAULT_REGION),
        service=service or os.environ.get("VIKING_API_SERVICE", DEFAULT_SERVICE),
        api_version=api_version or os.environ.get("VIKING_API_VERSION", DEFAULT_API_VERSION),
        project=project or os.environ.get("OPENVIKING_PROJECT", DEFAULT_PROJECT),
    )


_config: Optional[ControlPlaneConfig] = None


def get_config() -> ControlPlaneConfig:
    """Lazy, cached config built purely from the environment (used by the MCP server)."""
    global _config
    if _config is None:
        _config = build_config()
    return _config
