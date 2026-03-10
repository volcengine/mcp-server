from typing import Optional
from ..platform import AidapClient, SupabaseClient
from ..utils import resolve_workspace_id


class BaseTools:
    def __init__(self, aidap_client: AidapClient):
        self.aidap = aidap_client

    def _resolve_workspace_id(self, workspace_id: Optional[str]) -> str:
        resolved_workspace_id = resolve_workspace_id(workspace_id)
        if not resolved_workspace_id:
            raise ValueError("workspace_id is required")
        return resolved_workspace_id

    async def _get_client(self, workspace_id: str) -> SupabaseClient:
        import logging
        logger = logging.getLogger(__name__)

        endpoint = await self.aidap.get_endpoint(workspace_id)
        logger.info(f"[DEBUG] Got endpoint for {workspace_id}: {endpoint}")
        if not endpoint:
            raise ValueError(f"Could not get endpoint for workspace {workspace_id}")

        api_key = await self.aidap.get_api_key(workspace_id, "service_role")
        logger.info(f"[DEBUG] Got API key for {workspace_id}: {'yes' if api_key else 'no'}")
        if not api_key:
            raise ValueError(f"Could not get API key for workspace {workspace_id}")

        return SupabaseClient(endpoint, api_key)
