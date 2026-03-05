"""Workspace management tools for Supabase MCP Server"""

import asyncio
import json
import logging
import inspect
from typing import Optional

from ..utils import read_only_check

logger = logging.getLogger(__name__)


class WorkspaceTools:
    """Tools for managing workspaces"""

    def __init__(self, aidap_client, default_workspace_id: Optional[str] = None):
        self.aidap_client = aidap_client
        self.default_workspace_id = default_workspace_id

    def _resolve_workspace_id(self, workspace_id: Optional[str] = None) -> Optional[str]:
        return workspace_id or self.default_workspace_id

    def _error_detail(self, code: str, message: str, retriable: bool = False) -> dict:
        return {
            "code": code,
            "message": message,
            "retriable": retriable,
        }

    def _mask_key(self, value: Optional[str], reveal: bool) -> Optional[str]:
        if value is None:
            return None
        if reveal:
            return value
        if len(value) <= 12:
            return "*" * len(value)
        return f"{value[:6]}...{value[-4:]}"

    async def list_workspaces(self) -> str:
        """Lists all available workspaces.

        Returns:
            JSON string containing list of workspaces
        """
        try:
            from volcenginesdkaidap.models import DescribeWorkspacesRequest, FilterForDescribeWorkspacesInput

            parameters = inspect.signature(FilterForDescribeWorkspacesInput).parameters
            filter_kwargs = {
                "name": "DBEngineVersion",
                "value": "Supabase_1_24",
            }
            if "mode" in parameters:
                filter_kwargs["mode"] = "Exact"
            filters = [FilterForDescribeWorkspacesInput(**filter_kwargs)]

            request = DescribeWorkspacesRequest(filters=filters)
            response = self.aidap_client.client.describe_workspaces(request)

            if hasattr(response, 'workspaces') and response.workspaces:
                workspaces = []
                for ws in response.workspaces:
                    workspace_info = {
                        "workspace_id": getattr(ws, 'workspace_id', None),
                        "workspace_name": getattr(ws, 'workspace_name', None),
                        "status": getattr(ws, 'status', None),
                        "region": getattr(ws, 'region', None),
                    }
                    workspaces.append(workspace_info)

                return json.dumps({
                    "success": True,
                    "workspaces": workspaces,
                    "count": len(workspaces)
                }, indent=2)

            return json.dumps({
                "success": True,
                "workspaces": [],
                "count": 0
            }, indent=2)

        except Exception as e:
            logger.error(f"Error listing workspaces: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)

    async def get_workspace(self, workspace_id: str) -> str:
        """Gets details for a specific workspace.

        Args:
            workspace_id: The workspace ID

        Returns:
            JSON string containing workspace details
        """
        try:
            # 使用正确的 API 方法名
            from volcenginesdkaidap.models import DescribeWorkspaceDetailRequest

            request = DescribeWorkspaceDetailRequest(workspace_id=workspace_id)
            response = self.aidap_client.client.describe_workspace_detail(request)

            if hasattr(response, 'workspace'):
                ws = response.workspace
                workspace_info = {
                    "workspace_id": getattr(ws, 'workspace_id', None),
                    "workspace_name": getattr(ws, 'workspace_name', None),
                    "status": getattr(ws, 'status', None),
                    "region": getattr(ws, 'region', None),
                    "created_at": getattr(ws, 'created_at', None),
                    "updated_at": getattr(ws, 'updated_at', None),
                }

                return json.dumps({
                    "success": True,
                    "workspace": workspace_info
                }, indent=2)

            return json.dumps({
                "success": False,
                "error": "Workspace not found"
            }, indent=2)

        except Exception as e:
            logger.error(f"Error getting workspace: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)

    @read_only_check
    async def create_workspace(
        self,
        workspace_name: str,
        engine_version: str = "Supabase_1_24",
        engine_type: str = "Supabase",
    ) -> str:
        if not workspace_name or not workspace_name.strip():
            return json.dumps({"success": False, "error": "workspace_name is required"}, indent=2)
        result = await self.aidap_client.create_workspace(
            workspace_name=workspace_name.strip(),
            engine_type=engine_type,
            engine_version=engine_version
        )
        return json.dumps(result, indent=2)

    @read_only_check
    async def start_workspace(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)
        result = await self.aidap_client.start_workspace(ws_id)
        return json.dumps(result, indent=2)

    @read_only_check
    async def stop_workspace(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)
        result = await self.aidap_client.stop_workspace(ws_id)
        return json.dumps(result, indent=2)

    @read_only_check
    async def create_branch(
        self,
        name: str = "develop",
        workspace_id: Optional[str] = None,
    ) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)

        result = await self.aidap_client.create_branch(ws_id, name)
        return json.dumps(result, indent=2)

    async def list_branches(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)
        try:
            branches = await self.aidap_client.list_branches(ws_id)
            return json.dumps({"success": True, "branches": branches}, indent=2)
        except Exception as e:
            logger.error(f"Error listing branches: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    @read_only_check
    async def delete_branch(self, branch_id: str, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({
                "success": False,
                "error": "workspace_id is required",
                "error_detail": self._error_detail("MissingWorkspaceId", "workspace_id is required", False),
            }, indent=2)
        if not branch_id or not branch_id.strip():
            return json.dumps({
                "success": False,
                "error": "branch_id is required",
                "error_detail": self._error_detail("MissingBranchId", "branch_id is required", False),
            }, indent=2)
        normalized_branch_id = branch_id.strip()

        try:
            branches = await self.aidap_client.list_branches(ws_id)
            exists = any(b.get("branch_id") == normalized_branch_id for b in branches)
            if not exists:
                return json.dumps({
                    "success": False,
                    "error": f"Branch '{normalized_branch_id}' not found in workspace '{ws_id}'",
                    "error_detail": self._error_detail(
                        "BranchNotFound",
                        f"Branch '{normalized_branch_id}' not found in workspace '{ws_id}'",
                        False
                    ),
                }, indent=2)
        except Exception as e:
            logger.error(f"Error checking branch before delete: {e}")
            return json.dumps({
                "success": False,
                "error": str(e),
                "error_detail": self._error_detail("ListBranchesFailed", str(e), True),
            }, indent=2)

        result = await self.aidap_client.delete_branch(ws_id, normalized_branch_id)
        if not result.get("success"):
            error_text = result.get("error", "delete branch failed")
            return json.dumps({
                "success": False,
                "error": error_text,
                "error_detail": self._error_detail(
                    result.get("code", "DeleteBranchFailed"),
                    error_text,
                    bool(result.get("retriable", False))
                ),
            }, indent=2)

        max_confirm_attempts = 20
        last_list_error: Optional[str] = None
        for _ in range(max_confirm_attempts):
            await asyncio.sleep(1)
            try:
                branches = await self.aidap_client.list_branches(ws_id)
                exists = any(b.get("branch_id") == normalized_branch_id for b in branches)
                if not exists:
                    return json.dumps({"success": True, "branch_id": normalized_branch_id}, indent=2)
            except Exception as e:
                last_list_error = str(e)

        if last_list_error:
            return json.dumps({
                "success": False,
                "error": f"Delete requested for branch '{normalized_branch_id}' but verification failed: {last_list_error}",
                "error_detail": self._error_detail(
                    "DeleteBranchVerifyFailed",
                    f"Delete requested for branch '{normalized_branch_id}' but verification failed: {last_list_error}",
                    True
                ),
            }, indent=2)
        return json.dumps({
            "success": False,
            "error": f"Delete requested for branch '{normalized_branch_id}' but branch still exists",
            "error_detail": self._error_detail(
                "BranchStillExists",
                f"Delete requested for branch '{normalized_branch_id}' but branch still exists",
                True
            ),
        }, indent=2)

    async def get_workspace_endpoints(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)

        endpoint = await self.aidap_client.get_endpoint(ws_id)
        if not endpoint:
            return json.dumps({
                "success": False,
                "error": f"Could not get endpoint for workspace {ws_id}"
            }, indent=2)

        return json.dumps({
            "success": True,
            "workspace_id": ws_id,
            "project_url": endpoint,
            "api_url": endpoint
        }, indent=2)

    async def get_workspace_api_keys(self, workspace_id: Optional[str] = None, reveal: bool = False) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)

        try:
            keys = await self.aidap_client.get_api_keys(ws_id)
            publishable_key = None
            anon_key = None
            service_role_key = None
            masked_keys = []
            for key in keys:
                key_type = (key.get("type") or "").lower()
                value = key.get("key")
                if key_type == "public":
                    publishable_key = value
                    anon_key = value
                if key_type == "service":
                    service_role_key = value
                masked_keys.append({
                    **key,
                    "key": self._mask_key(value, reveal),
                })
            return json.dumps({
                "success": True,
                "workspace_id": ws_id,
                "reveal": reveal,
                "publishable_key": self._mask_key(publishable_key, reveal),
                "anon_key": self._mask_key(anon_key, reveal),
                "service_role_key": self._mask_key(service_role_key, reveal),
                "keys": masked_keys
            }, indent=2)
        except Exception as e:
            logger.error(f"Error getting api keys: {e}")
            return json.dumps({"success": False, "error": str(e)}, indent=2)

    @read_only_check
    async def reset_branch(
        self,
        branch_id: str,
        migration_version: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> str:
        """Resets migrations of a development branch.

        Args:
            branch_id: Branch ID to reset
            migration_version: Target migration version (official schema field, not supported by current AIDAP SDK)
            workspace_id: The workspace ID (optional)

        Returns:
            JSON string containing operation result
        """
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return json.dumps({
                "success": False,
                "error": "workspace_id is required"
            }, indent=2)

        try:
            result = await self.aidap_client.reset_branch(ws_id, branch_id)
            if not isinstance(result, dict):
                result = {"success": bool(result)}
            if migration_version:
                result["warning"] = "migration_version is ignored because current AIDAP reset_branch API does not support version-targeted reset"
            return json.dumps(result, indent=2)
        except Exception as e:
            logger.error(f"Error resetting branch: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
