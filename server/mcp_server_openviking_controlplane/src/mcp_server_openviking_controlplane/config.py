import json
import logging
import os
from dataclasses import dataclass
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Control plane API version, carried as a query param on every Action call.
API_VERSION = "2025-06-09"


@dataclass
class ControlPlaneConfig:
    """Configuration for the OpenViking control plane MCP server / CLI."""

    host: str
    headers: Dict[str, str]
    schema: str = "https"
    project: str = "default"

    @property
    def base_url(self) -> str:
        return f"{self.schema}://{self.host}"


def parse_headers_blob(blob: str) -> Dict[str, str]:
    """Parse manually supplied headers.

    Accepts either a JSON object, or the raw ``Key: Value`` block you get from a
    browser's "Copy request headers" (HTTP/2 pseudo-headers like ``:authority``
    are skipped).
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


def build_config(
    host: Optional[str] = None,
    schema: Optional[str] = None,
    project: Optional[str] = None,
    headers: Optional[Dict[str, str]] = None,
    headers_file: Optional[str] = None,
) -> ControlPlaneConfig:
    """Build a config from explicit args first, then environment fallbacks.

    Header sources, in precedence order: explicit ``headers`` arg > ``headers_file``
    arg > ``VIKING_HEADERS_FILE`` env (path) > ``VIKING_HEADERS`` env (inline).
    """
    if headers:
        resolved_headers = dict(headers)
    elif headers_file:
        resolved_headers = _read_headers_file(headers_file)
    elif os.environ.get("VIKING_HEADERS_FILE"):
        resolved_headers = _read_headers_file(os.environ["VIKING_HEADERS_FILE"])
    elif os.environ.get("VIKING_HEADERS"):
        resolved_headers = parse_headers_blob(os.environ["VIKING_HEADERS"])
    else:
        resolved_headers = {}

    resolved_host = (
        host
        or os.environ.get("VIKING_HOST")
        or resolved_headers.get("Host")
        or resolved_headers.get("host")
    )

    if not resolved_headers:
        raise ValueError(
            "missing auth headers: set --headers-file / --header, or VIKING_HEADERS_FILE "
            "(path) / VIKING_HEADERS (inline JSON or raw 'Key: Value' lines)"
        )
    if not resolved_host:
        raise ValueError(
            "missing host: set --host or VIKING_HOST, or include a 'Host' header in the "
            "supplied headers"
        )

    return ControlPlaneConfig(
        host=resolved_host,
        headers=resolved_headers,
        schema=schema or os.environ.get("VIKING_SCHEMA", "https"),
        project=project or os.environ.get("OPENVIKING_PROJECT", "default"),
    )


_config: Optional[ControlPlaneConfig] = None


def get_config() -> ControlPlaneConfig:
    """Lazy, cached config built purely from the environment (used by the MCP server)."""
    global _config
    if _config is None:
        _config = build_config()
    return _config
