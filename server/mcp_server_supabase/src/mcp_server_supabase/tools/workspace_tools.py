"""Workspace management tools for Supabase MCP Server"""

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
    async def create_branch(
        self,
        name: str = "develop",
        workspace_id: Optional[str] = None,
    ) -> str:
        ws_id = workspace_id or self.default_workspace_id
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)

        result = await self.aidap_client.create_branch(ws_id, name)
        return json.dumps(result, indent=2)

    async def list_branches(self, workspace_id: Optional[str] = None) -> str:
        ws_id = workspace_id or self.default_workspace_id
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)

        branches = await self.aidap_client.list_branches(ws_id)
        return json.dumps({"branches": branches}, indent=2)

    @read_only_check
    async def delete_branch(self, branch_id: str, workspace_id: Optional[str] = None) -> str:
        ws_id = workspace_id or self.default_workspace_id
        if not ws_id:
            return json.dumps({"success": False, "error": "workspace_id is required"}, indent=2)

        result = await self.aidap_client.delete_branch(ws_id, branch_id)
        return json.dumps(result, indent=2)

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
        ws_id = workspace_id or self.default_workspace_id
        if not ws_id:
            return json.dumps({
                "success": False,
                "error": "workspace_id is required"
            }, indent=2)

        if migration_version:
            return json.dumps({
                "success": False,
                "error": "migration_version is not supported by current AIDAP reset_branch API"
            }, indent=2)

        try:
            success = await self.aidap_client.reset_branch(ws_id, branch_id)
            return json.dumps({
                "success": success
            }, indent=2)
        except Exception as e:
            logger.error(f"Error resetting branch: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            }, indent=2)
