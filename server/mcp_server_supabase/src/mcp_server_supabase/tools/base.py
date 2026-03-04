from typing import Optional
from ..platform import AidapClient, SupabaseClient


class BaseTools:
    """Base class for all tool classes"""

    def __init__(self, aidap_client: AidapClient, workspace_id: Optional[str] = None):
        self.aidap = aidap_client
        self.default_workspace_id = workspace_id

    def _get_workspace_id(self, workspace_id: Optional[str]) -> str:
        """Get workspace ID from parameter or default"""
        result = workspace_id or self.default_workspace_id
        if not result:
            raise ValueError(
                "workspace_id is required: not provided as parameter and no default workspace_id configured. "
                "Please provide workspace_id or set DEFAULT_WORKSPACE_ID environment variable."
            )
        return result

    async def _get_client(self, workspace_id: str) -> SupabaseClient:
        """Get Supabase client for workspace"""
        import logging
        logger = logging.getLogger(__name__)

        endpoint = await self.aidap.get_endpoint(workspace_id)
        logger.info(f"[DEBUG] Got endpoint for {workspace_id}: {endpoint}")
        if not endpoint:
            raise ValueError(f"Could not get endpoint for workspace {workspace_id}")

        api_key = await self.aidap.get_api_key(workspace_id, "service_role")
        logger.info(f"[DEBUG] Got API key for {workspace_id}: {api_key[:20] if api_key else None}...")
        if not api_key:
            raise ValueError(f"Could not get API key for workspace {workspace_id}")

        return SupabaseClient(endpoint, api_key)
