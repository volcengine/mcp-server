import logging
from typing import Any, Optional

from .base import BaseTools
from ..utils import compact_dict, pick_value, to_json

logger = logging.getLogger(__name__)


class ComputeTools(BaseTools):
    def _compute_view(self, source: Any) -> dict:
        payload = {
            "compute_id": pick_value(source, "compute_id"),
            "compute_name": pick_value(source, "compute_name"),
            "compute_role": pick_value(source, "compute_role"),
            "compute_status": pick_value(source, "compute_status"),
            "service_type": pick_value(source, "service_type"),
            "branch_id": pick_value(source, "branch_id"),
            "workspace_id": pick_value(source, "workspace_id"),
            "auto_scaling_limit_min_cu": pick_value(source, "auto_scaling_limit_min_cu"),
            "auto_scaling_limit_max_cu": pick_value(source, "auto_scaling_limit_max_cu"),
            "enable_analytic": pick_value(source, "enable_analytic"),
            "last_active_time": pick_value(source, "last_active_time"),
            "suspended_time": pick_value(source, "suspended_time"),
        }
        return compact_dict(payload)

    async def get_compute_settings(
        self,
        workspace_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        service_type: Optional[str] = None,
    ) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            computes = await self.aidap.describe_computes(
                ws_id, branch_id=branch_id, service_type=service_type
            )
            normalized = [self._compute_view(compute) for compute in computes]
            return to_json({
                "success": True,
                "workspace_id": ws_id,
                "computes": normalized,
                "count": len(normalized),
            })
        except Exception as e:
            logger.error(f"Error getting compute settings: {e}")
            return to_json({"success": False, "error": str(e)})

    async def modify_compute_settings(
        self,
        min_cu: float,
        max_cu: float,
        suspend_timeout_seconds: Optional[int] = None,
        service_type: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
        except ValueError as e:
            return to_json({"success": False, "error": str(e)})

        if min_cu is None or max_cu is None:
            return to_json({"success": False, "error": "min_cu and max_cu are required"})

        result = await self.aidap.modify_compute_settings(
            ws_id,
            min_cu=min_cu,
            max_cu=max_cu,
            suspend_timeout_seconds=suspend_timeout_seconds,
            service_type=service_type,
        )
        if isinstance(result, dict):
            return to_json(result)
        return to_json({"success": bool(result), "workspace_id": ws_id})
