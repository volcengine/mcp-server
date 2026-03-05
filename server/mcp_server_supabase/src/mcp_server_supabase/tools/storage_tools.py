from typing import Optional, List, Dict, Any
import logging
from .base import BaseTools
from ..utils import handle_errors, read_only_check
from ..models import StorageConfig

logger = logging.getLogger(__name__)


class StorageTools(BaseTools):
    @handle_errors
    async def list_storage_buckets(self, workspace_id: Optional[str] = None) -> List[dict]:
        ws_id = self._get_workspace_id(workspace_id)
        logger.info(f"Listing storage buckets for workspace {ws_id}")

        client = await self._get_client(ws_id)
        result = await client.call_api("/storage/v1/bucket")

        logger.info(f"Found {len(result)} storage buckets")
        return result
    
    @handle_errors
    @read_only_check
    async def create_storage_bucket(
        self,
        bucket_name: str,
        public: bool = False,
        file_size_limit: Optional[int] = None,
        allowed_mime_types: Optional[str] = None,
        workspace_id: Optional[str] = None
    ) -> dict:
        if not bucket_name or not bucket_name.strip():
            raise ValueError("Bucket name cannot be empty")

        ws_id = self._get_workspace_id(workspace_id)
        logger.info(
            f"Creating storage bucket '{bucket_name}'",
            extra={"workspace_id": ws_id, "public": public}
        )

        client = await self._get_client(ws_id)

        data = {
            "name": bucket_name,
            "public": public
        }
        if file_size_limit:
            data["file_size_limit"] = file_size_limit
        if allowed_mime_types:
            data["allowed_mime_types"] = allowed_mime_types.split(",")
        
        return await client.call_api("/storage/v1/bucket", method="POST", json_data=data)
    
    @handle_errors
    @read_only_check
    async def delete_storage_bucket(self, bucket_name: str, workspace_id: Optional[str] = None) -> dict:
        if not bucket_name or not bucket_name.strip():
            raise ValueError("Bucket name cannot be empty")
        ws_id = self._get_workspace_id(workspace_id)
        client = await self._get_client(ws_id)
        response = await client.call_api(f"/storage/v1/bucket/{bucket_name}", method="DELETE")
        if isinstance(response, dict) and "error" in response:
            raise ValueError(response["error"])
        return {"success": True, "message": "Bucket deleted successfully"}
    
    @handle_errors
    async def get_storage_config(self, workspace_id: Optional[str] = None) -> StorageConfig:
        ws_id = self._get_workspace_id(workspace_id)
        client = await self._get_client(ws_id)
        result = await client.call_api("/storage/v1/config")
        return StorageConfig(**result)

    @handle_errors
    @read_only_check
    async def update_storage_config(
        self,
        config: Dict[str, Any],
        workspace_id: Optional[str] = None,
    ) -> dict:
        if not isinstance(config, dict) or not config:
            raise ValueError("config must be a non-empty object")

        ws_id = self._get_workspace_id(workspace_id)
        client = await self._get_client(ws_id)
        await client.call_api("/storage/v1/config", method="PUT", json_data=config)
        return {"success": True}
