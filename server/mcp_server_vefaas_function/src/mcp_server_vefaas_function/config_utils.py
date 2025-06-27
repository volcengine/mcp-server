from __future__ import annotations

"""Utility helpers for configuring environment variables **before** starting the MCP server.

IMPORTANT: This module **must not** import ``vefaas_server``; otherwise the MCP instance
would be created *before* the environment variables are set.
"""

import os
from typing import Any

__all__ = ["set_mcp_config_env"]

def set_mcp_config_env(mode: str, **kwargs: Any) -> None:
    """Write environment variables according to the running mode.

    Args:
        mode: Running mode. One of ``streamable``, ``sse``, or ``stdio``.
        **kwargs: Extra key‐value pairs that will be written into environment
            variables named ``FASTMCP_<KEY>`` (upper-case).
    """

    # Mode-specific default settings
    if mode == "streamable":
        # Enable JSON response & stateless HTTP by default
        os.environ["FASTMCP_JSON_RESPONSE"] = "true"
        os.environ["FASTMCP_STATELESS_HTTP"] = "true"

    # Write remaining key-value pairs
    for key, value in kwargs.items():
        env_key = f"FASTMCP_{key.upper()}"
        os.environ[env_key] = str(value)
