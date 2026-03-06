"""Workspace management tools for Supabase MCP Server"""

import asyncio
import json
import logging
import inspect
from typing import Any, Optional

from ..utils import read_only_check

logger = logging.getLogger(__name__)


class WorkspaceTools:
    """Tools for managing workspaces"""

    def __init__(self, aidap_client, default_workspace_id: Optional[str] = None):
        self.aidap_client = aidap_client
        self.default_workspace_id = default_workspace_id

    def _resolve_workspace_id(self, workspace_id: Optional[str] = None) -> Optional[str]:
        return workspace_id or self.default_workspace_id

    def _to_json(self, payload: dict) -> str:
        return json.dumps(payload, indent=2, ensure_ascii=False)

    def _compact(self, payload: dict) -> dict:
        return {k: v for k, v in payload.items() if v is not None}

    def _pick(self, source: Any, *field_names: str) -> Any:
        source_dict = source.to_dict() if hasattr(source, "to_dict") else source if isinstance(source, dict) else {}
        for field_name in field_names:
            value = None
            if isinstance(source, dict):
                value = source.get(field_name)
            else:
                value = getattr(source, field_name, None)
            if value is None and isinstance(source_dict, dict):
                value = source_dict.get(field_name)
            if isinstance(value, str):
                value = value.strip()
                if not value:
                    value = None
            if value is not None:
                return value
        return None

    def _workspace_view(self, source: Any) -> dict:
        workspace_id = self._pick(source, "workspace_id")
        workspace_name = self._pick(source, "workspace_name")
        project_name = self._pick(source, "project_name")
        payload = {
            "workspace_id": workspace_id,
            "workspace_name": workspace_name,
            "project_name": project_name or workspace_name,
            "status": self._pick(source, "workspace_status", "status"),
            "region": self._pick(source, "region_id", "region"),
            "created_at": self._pick(source, "create_time", "created_at"),
            "updated_at": self._pick(source, "update_time", "updated_at"),
            "engine_type": self._pick(source, "engine_type"),
            "engine_version": self._pick(source, "engine_version"),
            "deletion_protection_status": self._pick(source, "deletion_protection_status"),
        }
        return self._compact(payload)

    def _project_view(self, source: Any) -> dict:
        workspace_payload = self._workspace_view(source)
        project_name = workspace_payload.get("project_name") or workspace_payload.get("workspace_name")
        payload = {
            "project_id": workspace_payload.get("workspace_id"),
            "project_name": project_name,
            "workspace_id": workspace_payload.get("workspace_id"),
            "workspace_name": workspace_payload.get("workspace_name"),
            "status": workspace_payload.get("status"),
            "region": workspace_payload.get("region"),
            "created_at": workspace_payload.get("created_at"),
            "updated_at": workspace_payload.get("updated_at"),
            "engine_type": workspace_payload.get("engine_type"),
            "engine_version": workspace_payload.get("engine_version"),
            "deletion_protection_status": workspace_payload.get("deletion_protection_status"),
        }
        return self._compact(payload)

    def _with_project_alias(self, payload: dict, project_id: Optional[str] = None, project_name: Optional[str] = None) -> dict:
        result = dict(payload)
        workspace_id = result.get("workspace_id") or project_id
        workspace_name = result.get("workspace_name") or project_name
        if workspace_id:
            result["workspace_id"] = workspace_id
            result["project_id"] = workspace_id
        if workspace_name:
            result["workspace_name"] = workspace_name
            result["project_name"] = workspace_name
        return result

    def _describe_workspaces_response(self):
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
        return self.aidap_client.client.describe_workspaces(request)

    def _describe_workspace_detail_response(self, workspace_id: str):
        from volcenginesdkaidap.models import DescribeWorkspaceDetailRequest

        request = DescribeWorkspaceDetailRequest(workspace_id=workspace_id)
        return self.aidap_client.client.describe_workspace_detail(request)

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
        try:
            response = self._describe_workspaces_response()
            raw_workspaces = list(getattr(response, "workspaces", []) or [])
            workspaces = [self._workspace_view(ws) for ws in raw_workspaces]
            return self._to_json({
                "success": True,
                "workspaces": workspaces,
                "count": len(workspaces)
            })

        except Exception as e:
            logger.error(f"Error listing workspaces: {e}")
            return self._to_json({
                "success": False,
                "error": str(e)
            })

    async def get_workspace(self, workspace_id: str) -> str:
        try:
            response = self._describe_workspace_detail_response(workspace_id)
            ws = getattr(response, "workspace", None)
            if ws is not None:
                workspace_info = self._workspace_view(ws)
                return self._to_json({
                    "success": True,
                    "workspace": workspace_info
                })

            return self._to_json({
                "success": False,
                "error": "Workspace not found"
            })

        except Exception as e:
            logger.error(f"Error getting workspace: {e}")
            return self._to_json({
                "success": False,
                "error": str(e)
            })

    async def list_projects(self) -> str:
        try:
            response = self._describe_workspaces_response()
            raw_workspaces = list(getattr(response, "workspaces", []) or [])
            projects = [self._project_view(ws) for ws in raw_workspaces]
            return self._to_json({
                "success": True,
                "projects": projects,
                "count": len(projects)
            })
        except Exception as e:
            logger.error(f"Error listing projects: {e}")
            return self._to_json({
                "success": False,
                "error": str(e)
            })

    async def get_project(self, project_id: str) -> str:
        try:
            response = self._describe_workspace_detail_response(project_id)
            ws = getattr(response, "workspace", None)
            if ws is not None:
                project_info = self._project_view(ws)
                return self._to_json({
                    "success": True,
                    "project": project_info
                })
            return self._to_json({
                "success": False,
                "error": "Project not found"
            })
        except Exception as e:
            logger.error(f"Error getting project: {e}")
            return self._to_json({
                "success": False,
                "error": str(e)
            })

    @read_only_check
    async def create_workspace(
        self,
        workspace_name: str,
        engine_version: str = "Supabase_1_24",
        engine_type: str = "Supabase",
    ) -> str:
        if not workspace_name or not workspace_name.strip():
            return self._to_json({"success": False, "error": "workspace_name is required"})
        result = await self.aidap_client.create_workspace(
            workspace_name=workspace_name.strip(),
            engine_type=engine_type,
            engine_version=engine_version
        )
        return self._to_json(result)

    @read_only_check
    async def create_project(
        self,
        project_name: str,
        engine_version: str = "Supabase_1_24",
        engine_type: str = "Supabase",
    ) -> str:
        if not project_name or not project_name.strip():
            return self._to_json({"success": False, "error": "project_name is required"})
        result = await self.aidap_client.create_workspace(
            workspace_name=project_name.strip(),
            engine_type=engine_type,
            engine_version=engine_version
        )
        if not isinstance(result, dict):
            return self._to_json({"success": False, "error": "Unexpected create project response"})
        if result.get("success"):
            mapped = {
                "success": True,
                "project_id": result.get("workspace_id"),
                "project_name": result.get("workspace_name") or project_name.strip(),
                "workspace_id": result.get("workspace_id"),
                "workspace_name": result.get("workspace_name") or project_name.strip(),
                "engine_type": result.get("engine_type"),
                "engine_version": result.get("engine_version"),
            }
            return self._to_json(self._compact(mapped))
        return self._to_json(result)

    @read_only_check
    async def start_workspace(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "workspace_id is required"})
        result = await self.aidap_client.start_workspace(ws_id)
        return self._to_json(result)

    @read_only_check
    async def stop_workspace(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "workspace_id is required"})
        result = await self.aidap_client.stop_workspace(ws_id)
        return self._to_json(result)

    @read_only_check
    async def restore_project(self, project_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(project_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "project_id is required"})
        result = await self.aidap_client.start_workspace(ws_id)
        if isinstance(result, dict):
            result = self._with_project_alias(result, ws_id)
        return self._to_json(result)

    @read_only_check
    async def pause_project(self, project_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(project_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "project_id is required"})
        result = await self.aidap_client.stop_workspace(ws_id)
        if isinstance(result, dict):
            result = self._with_project_alias(result, ws_id)
        return self._to_json(result)

    @read_only_check
    async def create_branch(
        self,
        name: str = "develop",
        workspace_id: Optional[str] = None,
    ) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "workspace_id is required"})

        result = await self.aidap_client.create_branch(ws_id, name)
        return self._to_json(result)

    async def list_branches(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "workspace_id is required"})
        try:
            branches = await self.aidap_client.list_branches(ws_id)
            return self._to_json({"success": True, "branches": branches})
        except Exception as e:
            logger.error(f"Error listing branches: {e}")
            return self._to_json({"success": False, "error": str(e)})

    @read_only_check
    async def delete_branch(self, branch_id: str, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({
                "success": False,
                "error": "workspace_id is required",
                "error_detail": self._error_detail("MissingWorkspaceId", "workspace_id is required", False),
            })
        if not branch_id or not branch_id.strip():
            return self._to_json({
                "success": False,
                "error": "branch_id is required",
                "error_detail": self._error_detail("MissingBranchId", "branch_id is required", False),
            })
        normalized_branch_id = branch_id.strip()

        try:
            branches = await self.aidap_client.list_branches(ws_id)
            exists = any(b.get("branch_id") == normalized_branch_id for b in branches)
            if not exists:
                return self._to_json({
                    "success": False,
                    "error": f"Branch '{normalized_branch_id}' not found in workspace '{ws_id}'",
                    "error_detail": self._error_detail(
                        "BranchNotFound",
                        f"Branch '{normalized_branch_id}' not found in workspace '{ws_id}'",
                        False
                    ),
                })
        except Exception as e:
            logger.error(f"Error checking branch before delete: {e}")
            return self._to_json({
                "success": False,
                "error": str(e),
                "error_detail": self._error_detail("ListBranchesFailed", str(e), True),
            })

        result = await self.aidap_client.delete_branch(ws_id, normalized_branch_id)
        if not result.get("success"):
            error_text = result.get("error", "delete branch failed")
            return self._to_json({
                "success": False,
                "error": error_text,
                "error_detail": self._error_detail(
                    result.get("code", "DeleteBranchFailed"),
                    error_text,
                    bool(result.get("retriable", False))
                ),
            })

        max_confirm_attempts = 20
        last_list_error: Optional[str] = None
        for _ in range(max_confirm_attempts):
            await asyncio.sleep(1)
            try:
                branches = await self.aidap_client.list_branches(ws_id)
                exists = any(b.get("branch_id") == normalized_branch_id for b in branches)
                if not exists:
                    return self._to_json({"success": True, "branch_id": normalized_branch_id})
            except Exception as e:
                last_list_error = str(e)

        if last_list_error:
            return self._to_json({
                "success": False,
                "error": f"Delete requested for branch '{normalized_branch_id}' but verification failed: {last_list_error}",
                "error_detail": self._error_detail(
                    "DeleteBranchVerifyFailed",
                    f"Delete requested for branch '{normalized_branch_id}' but verification failed: {last_list_error}",
                    True
                ),
            })
        return self._to_json({
            "success": False,
            "error": f"Delete requested for branch '{normalized_branch_id}' but branch still exists",
            "error_detail": self._error_detail(
                "BranchStillExists",
                f"Delete requested for branch '{normalized_branch_id}' but branch still exists",
                True
            ),
        })

    async def get_workspace_endpoints(self, workspace_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "workspace_id is required"})

        endpoint = await self.aidap_client.get_endpoint(ws_id)
        if not endpoint:
            return self._to_json({
                "success": False,
                "error": f"Could not get endpoint for workspace {ws_id}"
            })

        return self._to_json({
            "success": True,
            "workspace_id": ws_id,
            "project_url": endpoint,
            "api_url": endpoint
        })

    async def get_project_url(self, project_id: Optional[str] = None) -> str:
        ws_id = self._resolve_workspace_id(project_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "project_id is required"})

        endpoint = await self.aidap_client.get_endpoint(ws_id)
        if not endpoint:
            return self._to_json({
                "success": False,
                "error": f"Could not get endpoint for project {ws_id}"
            })

        return self._to_json({
            "success": True,
            "project_id": ws_id,
            "workspace_id": ws_id,
            "project_url": endpoint,
            "api_url": endpoint
        })

    async def _get_api_keys_payload(self, workspace_id: str, reveal: bool = False) -> dict:
        keys = await self.aidap_client.get_api_keys(workspace_id)
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
        return {
            "success": True,
            "workspace_id": workspace_id,
            "reveal": reveal,
            "publishable_key": self._mask_key(publishable_key, reveal),
            "anon_key": self._mask_key(anon_key, reveal),
            "service_role_key": self._mask_key(service_role_key, reveal),
            "keys": masked_keys
        }

    async def get_workspace_api_keys(self, workspace_id: Optional[str] = None, reveal: bool = False) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "workspace_id is required"})

        try:
            payload = await self._get_api_keys_payload(ws_id, reveal)
            return self._to_json(payload)
        except Exception as e:
            logger.error(f"Error getting api keys: {e}")
            return self._to_json({"success": False, "error": str(e)})

    async def get_publishable_keys(self, project_id: Optional[str] = None, reveal: bool = False) -> str:
        ws_id = self._resolve_workspace_id(project_id)
        if not ws_id:
            return self._to_json({"success": False, "error": "project_id is required"})

        try:
            payload = await self._get_api_keys_payload(ws_id, reveal)
            payload = self._with_project_alias(payload, ws_id)
            return self._to_json(payload)
        except Exception as e:
            logger.error(f"Error getting publishable keys: {e}")
            return self._to_json({"success": False, "error": str(e)})

    @read_only_check
    async def reset_branch(
        self,
        branch_id: str,
        migration_version: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> str:
        ws_id = self._resolve_workspace_id(workspace_id)
        if not ws_id:
            return self._to_json({
                "success": False,
                "error": "workspace_id is required"
            })

        try:
            result = await self.aidap_client.reset_branch(ws_id, branch_id)
            if not isinstance(result, dict):
                result = {"success": bool(result)}
            if migration_version:
                result["warning"] = "migration_version is ignored because current AIDAP reset_branch API does not support version-targeted reset"
            return self._to_json(result)
        except Exception as e:
            logger.error(f"Error resetting branch: {e}")
            return self._to_json({
                "success": False,
                "error": str(e)
            })
