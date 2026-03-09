"""HTTP client for the remote HQD MCP server (streamable-http transport)."""

import json
import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class HqdRemoteClient:
    """Stateful client that communicates with the remote HQD MCP server."""

    def __init__(self, endpoint: str):
        self._endpoint = endpoint
        self._session_id: Optional[str] = None
        self._http = requests.Session()
        self._http.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        })
        self._req_id = 0

    def _next_id(self) -> int:
        self._req_id += 1
        return self._req_id

    def _parse_sse_response(self, text: str) -> Dict[str, Any]:
        """Parse SSE event stream and extract the JSON-RPC data."""
        for line in text.strip().splitlines():
            if line.startswith("data: "):
                return json.loads(line[6:])
        # Fallback: try parsing the whole text as JSON
        return json.loads(text)

    def _send(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the remote MCP server."""
        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params or {},
        }

        headers = {}
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id

        resp = self._http.post(self._endpoint, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        # Capture session ID from response headers
        sid = resp.headers.get("mcp-session-id")
        if sid:
            self._session_id = sid

        return self._parse_sse_response(resp.text)

    def initialize(self) -> None:
        """Initialize the MCP session with the remote server."""
        result = self._send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp-server-hqd-proxy", "version": "0.1.0"},
        })
        server_info = result.get("result", {}).get("serverInfo", {})
        logger.info(
            f"Connected to remote HQD MCP: {server_info.get('name')} "
            f"v{server_info.get('version')}, session={self._session_id}"
        )

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the remote MCP server and return the text result."""
        if not self._session_id:
            self.initialize()

        result = self._send("tools/call", {
            "name": tool_name,
            "arguments": arguments,
        })

        # Extract text content from MCP response
        rpc_result = result.get("result", {})
        contents = rpc_result.get("content", [])
        for item in contents:
            if item.get("type") == "text":
                return item["text"]

        # Fallback
        return json.dumps(rpc_result, ensure_ascii=False, indent=2)
