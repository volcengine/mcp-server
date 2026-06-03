import json
import logging
from typing import Any, Dict, Optional

import requests

from mcp_server_openviking_controlplane.common.auth import AuthProvider, ManualHeadersAuth
from mcp_server_openviking_controlplane.config import ControlPlaneConfig, get_config

logger = logging.getLogger(__name__)

# Headers we never replay verbatim: requests recomputes them, or a stale value
# breaks the request. We always send a freshly serialized JSON body.
_DROP_HEADERS = {"content-length", "connection", "accept-encoding"}


class ControlPlaneError(RuntimeError):
    """Raised when the control plane returns an Error envelope or a non-200 status."""

    def __init__(self, code: str, message: str, request_id: str = ""):
        self.code = code
        self.message = message
        self.request_id = request_id
        suffix = f" (RequestId={request_id})" if request_id else ""
        super().__init__(f"[{code}] {message}{suffix}")


class ControlPlaneClient:
    """Shared core used by both the MCP tools (``server.py``) and the CLI (``cli.py``).

    One method per control-plane Action. Each builds the request body, attaches auth
    headers via the ``AuthProvider``, POSTs, and unwraps the TOP response envelope.
    """

    def __init__(
        self,
        config: ControlPlaneConfig,
        auth: Optional[AuthProvider] = None,
        timeout: int = 30,
    ):
        self.config = config
        self.auth = auth or ManualHeadersAuth(config.headers)
        self.timeout = timeout

    def _request(self, action: str, body: Dict[str, Any]) -> Dict[str, Any]:
        # Console proxy: Action/Version are in the path, not the query string.
        path = self.config.action_path(action)
        body_str = json.dumps(body)

        headers = {"Content-Type": "application/json"}
        headers.update(self.auth.auth_headers("POST", path, {}, body_str))
        headers = {k: v for k, v in headers.items() if k.lower() not in _DROP_HEADERS}

        url = f"{self.config.base_url}{path}"
        logger.debug("POST %s body=%s", url, body_str)
        rsp = requests.request(
            "POST", url, data=body_str, headers=headers, timeout=self.timeout
        )
        return self._unwrap(action, rsp)

    @staticmethod
    def _unwrap(action: str, rsp: requests.Response) -> Dict[str, Any]:
        try:
            payload = rsp.json()
        except ValueError:
            raise ControlPlaneError(
                "InvalidResponse",
                f"{action} returned non-JSON (HTTP {rsp.status_code}): {rsp.text[:500]}",
            )

        meta = payload.get("ResponseMetadata", {}) if isinstance(payload, dict) else {}
        error = meta.get("Error")
        if error:
            raise ControlPlaneError(
                error.get("Code", "Unknown"),
                error.get("Message", ""),
                meta.get("RequestId", ""),
            )
        if rsp.status_code != 200:
            raise ControlPlaneError(
                "HTTPError",
                f"{action} HTTP {rsp.status_code}: {rsp.text[:500]}",
                meta.get("RequestId", ""),
            )
        return payload.get("Result", {}) if isinstance(payload, dict) else {}

    # --- Actions (6 core) ---------------------------------------------------

    def list_collections(self, project: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        proj = project if project is not None else self.config.project
        if proj:
            body["Project"] = proj
        return self._request("ListOpenVikingCollections", body)

    def create_collection(
        self,
        name: str,
        source: str,
        vlm: Dict[str, Any],
        embedding: Dict[str, Any],
        version: str = "developer",
        project: Optional[str] = None,
        description: Optional[str] = None,
        openviking_version: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "Name": name,
            "Version": version,
            "Source": source,
            "VLM": vlm,
            "Embedding": embedding,
        }
        proj = project if project is not None else self.config.project
        if proj:
            body["Project"] = proj
        if description is not None:
            body["Description"] = description
        if openviking_version:
            body["OpenvikingVersion"] = openviking_version
        if extra:
            body.update(extra)  # Feishu / GitHub / Memory, etc.
        return self._request("CreateOpenVikingCollection", body)

    def get_collection(self, resource_id: str) -> Dict[str, Any]:
        return self._request("GetOpenVikingCollection", {"ResourceID": resource_id})

    def delete_collection(self, resource_id: str) -> Dict[str, Any]:
        return self._request("DeleteOpenVikingCollection", {"ResourceID": resource_id})

    def get_usage(self, resource_id: str) -> Dict[str, Any]:
        return self._request("GetOpenVikingUsage", {"ResourceID": resource_id})

    def get_user_access(self, resource_id: str) -> Dict[str, Any]:
        # Console action AccessOpenVikingApiKey returns the default user's PLAINTEXT
        # data-plane key: {"UserID", "Role", "ApiKey"}. (The doc's
        # GetOpenVikingCollectionUserAccess does not exist here; ListOpenVikingUser
        # only returns a masked key.)
        return self._request("AccessOpenVikingApiKey", {"ResourceID": resource_id})


_client: Optional[ControlPlaneClient] = None


def get_client() -> ControlPlaneClient:
    """Lazy singleton used by the MCP server (config resolved from the environment)."""
    global _client
    if _client is None:
        _client = ControlPlaneClient(get_config())
    return _client
