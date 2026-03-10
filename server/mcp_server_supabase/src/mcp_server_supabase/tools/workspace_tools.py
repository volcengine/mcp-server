import asyncio
import inspect
import logging
from typing import Any, Optional

from .base import BaseTools
from ..utils import compact_dict, pick_value, to_json

logger = logging.getLogger(__name__)


class WorkspaceTools(BaseTools):
    _filter_supports_mode: bool | None = None

    @classmethod
    def _supports_workspace_filter_mode(cls) -> bool:
        if cls._filter_supports_mode is None:
            from volcenginesdkaidap.models import FilterForDescribeWorkspacesInput

            cls._filter_supports_mode = "mode" in inspect.signature(FilterForDescribeWorkspacesInput).parameters
        return cls._filter_supports_mode

    def _resolve_workspace_or_response(
        self,
        workspace_id: Optional[str],
        detailed: bool = False,
    ) -> tuple[str | None, str | None]:
        try:
            return self._resolve_workspace_id(workspace_id), None
        except ValueError:
            return None, self._workspace_required_response(detailed)

    def _workspace_required_response(self, detailed: bool = False) -> str:
        payload = {
            "success": False,
            "error": "workspace_id is required",
        }
        if detailed:
            payload["error_detail"] = self._error_detail("MissingWorkspaceId", "workspace_id is required", False)
        return to_json(payload)

    def _workspace_view(self, source: Any) -> dict:
        payload = {
            "workspace_id": pick_value(source, "workspace_id"),
            "workspace_name": pick_value(source, "workspace_name"),
            "status": pick_value(source, "workspace_status", "status"),
            "region": pick_value(source, "region_id", "region"),
            "created_at": pick_value(source, "create_time", "created_at"),
            "updated_at": pick_value(source, "update_time", "updated_at"),
            "engine_type": pick_value(source, "engine_type"),
            "engine_version": pick_value(source, "engine_version"),
            "deletion_protection_status": pick_value(source, "deletion_protection_status"),
        }
        return compact_dict(payload)

    def _branch_view(self, branch: dict, workspace_payload: Optional[dict] = None) -> dict:
        workspace_payload = workspace_payload or {}
        payload = {
            "branch_id": branch.get("branch_id"),
            "branch_name": branch.get("branch_name") or branch.get("name"),
            "status": branch.get("status") or workspace_payload.get("status"),
            "default": branch.get("default"),
            "parent_id": branch.get("parent_id"),
            "workspace_id": workspace_payload.get("workspace_id") or branch.get("workspace_id"),
            "workspace_name": workspace_payload.get("workspace_name"),
            "created_at": branch.get("created_at") or workspace_payload.get("created_at"),
            "updated_at": branch.get("updated_at") or workspace_payload.get("updated_at"),
            "engine_type": workspace_payload.get("engine_type"),
            "engine_version": workspace_payload.get("engine_version"),
            "deletion_protection_status": workspace_payload.get("deletion_protection_status"),
            "target_type": "branch",
        }
        return compact_dict(payload)

    def _describe_workspaces_response(self):
        from volcenginesdkaidap.models import DescribeWorkspacesRequest, FilterForDescribeWorkspacesInput

        filter_kwargs = {
            "name": "DBEngineVersion",
            "value": "Supabase_1_24",
        }
        if self._supports_workspace_filter_mode():
            filter_kwargs["mode"] = "Exact"
        filters = [FilterForDescribeWorkspacesInput(**filter_kwargs)]
        request = DescribeWorkspacesRequest(filters=filters)
        return self.aidap.client.describe_workspaces(request)

    def _find_workspace_source(self, workspace_id: str) -> Optional[Any]:
        response = self._describe_workspaces_response()
        for workspace in list(getattr(response, "workspaces", []) or []):
            if pick_value(workspace, "workspace_id") == workspace_id:
                return workspace
        return None

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
            workspaces = [self._workspace_view(workspace) for workspace in raw_workspaces]
            return to_json({
                "success": True,
                "workspaces": workspaces,
                "count": len(workspaces),
            })
        except Exception as e:
            logger.error(f"Error listing workspaces: {e}")
            return to_json({
                "success": False,
                "error": str(e),
            })

    async def get_workspace(self, workspace_id: str) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            workspace_source = self._find_workspace_source(ws_id)
            if workspace_source is None:
                return to_json({
                    "success": False,
                    "error": "Workspace not found",
                })
            workspace_info = self._workspace_view(workspace_source)
            return to_json({
                "success": True,
                "workspace": workspace_info,
            })
        except Exception as e:
            logger.error(f"Error getting workspace: {e}")
            return to_json({
                "success": False,
                "error": str(e),
            })

    async def create_workspace(
        self,
        workspace_name: str,
        engine_version: str = "Supabase_1_24",
        engine_type: str = "Supabase",
    ) -> str:
        if not workspace_name or not workspace_name.strip():
            return to_json({"success": False, "error": "workspace_name is required"})
        result = await self.aidap.create_workspace(
            workspace_name=workspace_name.strip(),
            engine_type=engine_type,
            engine_version=engine_version,
        )
        if not isinstance(result, dict):
            return to_json({"success": False, "error": "Unexpected create workspace response"})
        if result.get("success"):
            mapped = {
                "success": True,
                "workspace_id": result.get("workspace_id"),
                "workspace_name": result.get("workspace_name") or workspace_name.strip(),
                "engine_type": result.get("engine_type"),
                "engine_version": result.get("engine_version"),
            }
            return to_json(compact_dict(mapped))
        return to_json(result)

    async def restore_workspace(self, workspace_id: Optional[str] = None) -> str:
        ws_id, error_response = self._resolve_workspace_or_response(workspace_id)
        if error_response:
            return error_response
        result = await self.aidap.start_workspace(ws_id)
        return to_json(result if isinstance(result, dict) else {"success": bool(result), "workspace_id": ws_id})

    async def pause_workspace(self, workspace_id: Optional[str] = None) -> str:
        ws_id, error_response = self._resolve_workspace_or_response(workspace_id)
        if error_response:
            return error_response
        result = await self.aidap.stop_workspace(ws_id)
        return to_json(result if isinstance(result, dict) else {"success": bool(result), "workspace_id": ws_id})

    async def create_branch(
        self,
        name: str = "develop",
        workspace_id: Optional[str] = None,
    ) -> str:
        ws_id, error_response = self._resolve_workspace_or_response(workspace_id)
        if error_response:
            return error_response

        result = await self.aidap.create_branch(ws_id, name)
        if result.get("success") and result.get("branch_id"):
            branch_payload = self._branch_view(result, {"workspace_id": ws_id})
            branch_payload["branch_name"] = branch_payload.get("branch_name") or name
            response_payload = {
                "success": True,
                **branch_payload,
            }
            endpoint = await self.aidap.get_endpoint(ws_id, branch_id=result["branch_id"])
            if endpoint:
                response_payload["workspace_url"] = endpoint
                response_payload["api_url"] = endpoint
            return to_json(compact_dict(response_payload))
        return to_json(result)

    async def list_branches(self, workspace_id: Optional[str] = None) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            workspace_source = self._find_workspace_source(ws_id)
            workspace_payload = self._workspace_view(workspace_source) if workspace_source is not None else {"workspace_id": ws_id}
            branches = await self.aidap.list_branches(ws_id)
            normalized_branches = [self._branch_view(branch, workspace_payload) for branch in branches]
            return to_json({"success": True, "branches": normalized_branches})
        except Exception as e:
            logger.error(f"Error listing branches: {e}")
            return to_json({"success": False, "error": str(e)})

    async def delete_branch(self, branch_id: str, workspace_id: Optional[str] = None) -> str:
        ws_id, error_response = self._resolve_workspace_or_response(workspace_id, detailed=True)
        if error_response:
            return error_response
        if not branch_id or not branch_id.strip():
            return to_json({
                "success": False,
                "error": "branch_id is required",
                "error_detail": self._error_detail("MissingBranchId", "branch_id is required", False),
            })
        normalized_branch_id = branch_id.strip()

        try:
            branches = await self.aidap.list_branches(ws_id)
            exists = any(branch.get("branch_id") == normalized_branch_id for branch in branches)
            if not exists:
                return to_json({
                    "success": False,
                    "error": f"Branch '{normalized_branch_id}' not found in workspace '{ws_id}'",
                    "error_detail": self._error_detail(
                        "BranchNotFound",
                        f"Branch '{normalized_branch_id}' not found in workspace '{ws_id}'",
                        False,
                    ),
                })
        except Exception as e:
            logger.error(f"Error checking branch before delete: {e}")
            return to_json({
                "success": False,
                "error": str(e),
                "error_detail": self._error_detail("ListBranchesFailed", str(e), True),
            })

        result = await self.aidap.delete_branch(ws_id, normalized_branch_id)
        if not result.get("success"):
            error_text = result.get("error", "delete branch failed")
            return to_json({
                "success": False,
                "error": error_text,
                "error_detail": self._error_detail(
                    result.get("code", "DeleteBranchFailed"),
                    error_text,
                    bool(result.get("retriable", False)),
                ),
            })

        max_confirm_attempts = 20
        last_list_error: Optional[str] = None
        for _ in range(max_confirm_attempts):
            await asyncio.sleep(1)
            try:
                branches = await self.aidap.list_branches(ws_id)
                exists = any(branch.get("branch_id") == normalized_branch_id for branch in branches)
                if not exists:
                    return to_json({"success": True, "branch_id": normalized_branch_id, "workspace_id": ws_id})
            except Exception as e:
                last_list_error = str(e)

        if last_list_error:
            return to_json({
                "success": False,
                "error": f"Delete requested for branch '{normalized_branch_id}' but verification failed: {last_list_error}",
                "error_detail": self._error_detail(
                    "DeleteBranchVerifyFailed",
                    f"Delete requested for branch '{normalized_branch_id}' but verification failed: {last_list_error}",
                    True,
                ),
            })
        return to_json({
            "success": False,
            "error": f"Delete requested for branch '{normalized_branch_id}' but branch still exists",
            "error_detail": self._error_detail(
                "BranchStillExists",
                f"Delete requested for branch '{normalized_branch_id}' but branch still exists",
                True,
            ),
        })

    async def get_workspace_url(self, workspace_id: Optional[str] = None) -> str:
        ws_id, error_response = self._resolve_workspace_or_response(workspace_id)
        if error_response:
            return error_response

        endpoint = await self.aidap.get_endpoint(ws_id)
        if not endpoint:
            return to_json({
                "success": False,
                "error": f"Could not get endpoint for workspace {ws_id}",
            })

        payload = {
            "success": True,
            "workspace_id": ws_id,
            "workspace_url": endpoint,
            "api_url": endpoint,
        }
        return to_json(payload)

    async def _get_api_keys_payload(self, workspace_id: str, reveal: bool = False) -> dict:
        resolved_branch_id = await self.aidap.get_default_branch_id(workspace_id)
        if not resolved_branch_id:
            raise RuntimeError(f"Could not resolve default branch for workspace {workspace_id}")
        keys = await self.aidap.get_api_keys(workspace_id, branch_id=resolved_branch_id)
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
        payload = {
            "success": True,
            "workspace_id": workspace_id,
            "reveal": reveal,
            "publishable_key": self._mask_key(publishable_key, reveal),
            "anon_key": self._mask_key(anon_key, reveal),
            "service_role_key": self._mask_key(service_role_key, reveal),
            "keys": masked_keys,
        }
        if resolved_branch_id:
            payload["branch_id"] = resolved_branch_id
            payload["target_type"] = "branch"
        return payload

    async def get_publishable_keys(self, workspace_id: Optional[str] = None, reveal: bool = False) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            payload = await self._get_api_keys_payload(ws_id, reveal=reveal)
            return to_json(payload)
        except Exception as e:
            logger.error(f"Error getting publishable keys: {e}")
            return to_json({"success": False, "error": str(e)})

    async def restore_branch(
        self,
        branch_id: str,
        workspace_id: Optional[str] = None,
    ) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            result = await self.aidap.restore_branch(ws_id, branch_id)
            if not isinstance(result, dict):
                result = {"success": bool(result)}
            if result.get("success"):
                result.setdefault("workspace_id", ws_id)
                result.setdefault("branch_id", branch_id)
            return to_json(result)
        except Exception as e:
            logger.error(f"Error restoring branch: {e}")
            return to_json({
                "success": False,
                "error": str(e),
            })
