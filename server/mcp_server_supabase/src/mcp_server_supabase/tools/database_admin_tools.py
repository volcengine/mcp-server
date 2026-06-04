import logging
from typing import Optional

from .base import BaseTools
from ..utils import to_json

logger = logging.getLogger(__name__)


class DatabaseAdminTools(BaseTools):
    async def list_databases(
        self,
        workspace_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            databases = await self.aidap.describe_databases(ws_id, branch_id=branch_id, search=search)
            return to_json({
                "success": True,
                "workspace_id": ws_id,
                "databases": databases,
                "count": len(databases),
            })
        except Exception as e:
            logger.error(f"Error listing databases: {e}")
            return to_json({"success": False, "error": str(e)})

    async def create_database(
        self,
        database_name: str,
        owner: Optional[str] = None,
        description: Optional[str] = None,
        branch_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> str:
        if not database_name or not database_name.strip():
            return to_json({"success": False, "error": "database_name is required"})
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
        except ValueError as e:
            return to_json({"success": False, "error": str(e)})
        result = await self.aidap.create_database(
            ws_id,
            database_name=database_name.strip(),
            branch_id=branch_id,
            database_owner=owner,
            database_desc=description,
        )
        return to_json(result if isinstance(result, dict) else {"success": bool(result)})

    async def list_db_accounts(
        self,
        workspace_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        search: Optional[str] = None,
    ) -> str:
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            accounts = await self.aidap.describe_db_accounts(ws_id, branch_id=branch_id, search=search)
            return to_json({
                "success": True,
                "workspace_id": ws_id,
                "accounts": accounts,
                "count": len(accounts),
            })
        except Exception as e:
            logger.error(f"Error listing db accounts: {e}")
            return to_json({"success": False, "error": str(e)})

    async def create_db_account(
        self,
        account_name: str,
        account_password: str,
        description: Optional[str] = None,
        branch_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> str:
        if not account_name or not account_name.strip():
            return to_json({"success": False, "error": "account_name is required"})
        if not account_password:
            return to_json({"success": False, "error": "account_password is required"})
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
        except ValueError as e:
            return to_json({"success": False, "error": str(e)})
        result = await self.aidap.create_db_account(
            ws_id,
            account_name=account_name.strip(),
            account_password=account_password,
            branch_id=branch_id,
            account_desc=description,
        )
        return to_json(result if isinstance(result, dict) else {"success": bool(result)})

    async def get_db_account_connection(
        self,
        account_name: str,
        database_name: str,
        compute_id: Optional[str] = None,
        branch_id: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> str:
        if not account_name or not account_name.strip():
            return to_json({"success": False, "error": "account_name is required"})
        if not database_name or not database_name.strip():
            return to_json({"success": False, "error": "database_name is required"})
        try:
            ws_id = self._resolve_workspace_id(workspace_id)
            connection = await self.aidap.describe_db_account_connection(
                ws_id,
                account_name=account_name.strip(),
                database_name=database_name.strip(),
                branch_id=branch_id,
                compute_id=compute_id,
            )
            return to_json({"success": True, "workspace_id": ws_id, "connection": connection})
        except Exception as e:
            logger.error(f"Error getting db account connection: {e}")
            return to_json({"success": False, "error": str(e)})
