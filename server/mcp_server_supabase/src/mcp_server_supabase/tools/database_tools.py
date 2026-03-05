from typing import Optional, List
import logging
from .base import BaseTools
from ..utils import handle_errors, read_only_check

logger = logging.getLogger(__name__)


class DatabaseTools(BaseTools):
    """使用 REST API 方式执行 SQL"""
    @handle_errors
    async def execute_sql(self, query: str, workspace_id: Optional[str] = None) -> List[dict]:
        if not query or not query.strip():
            raise ValueError("SQL query cannot be empty")

        ws_id = self._get_workspace_id(workspace_id)
        logger.info(
            "Executing SQL query",
            extra={"workspace_id": ws_id, "query_length": len(query)}
        )

        client = await self._get_client(ws_id)
        result = await client.call_api("/pg/query", method="POST", json_data={"query": query})

        logger.debug(f"SQL query returned {len(result) if isinstance(result, list) else 'N/A'} rows")
        return result
    
    @handle_errors
    async def list_tables(self, schemas: List[str] = None, workspace_id: Optional[str] = None) -> List[dict]:
        if schemas is None:
            schemas = ["public"]

        # 验证 schema 名称，防止 SQL 注入
        for schema in schemas:
            if not schema.replace('_', '').isalnum():
                raise ValueError(f"Invalid schema name: {schema}")

        schema_list = "', '".join(schemas)
        query = f"""
        SELECT
            schemaname as schema,
            tablename as name
        FROM pg_tables
        WHERE schemaname IN ('{schema_list}')
        ORDER BY schemaname, tablename
        """

        return await self.execute_sql(query, workspace_id)
    
    @handle_errors
    async def list_migrations(self, workspace_id: Optional[str] = None) -> List[dict]:
        query = """
        SELECT version, name
        FROM supabase_migrations.schema_migrations
        ORDER BY version DESC
        """
        try:
            return await self.execute_sql(query, workspace_id)
        except Exception as e:
            logger.warning(f"Failed to list migrations: {e}")
            return []

    @handle_errors
    async def list_extensions(self, workspace_id: Optional[str] = None) -> List[dict]:
        query = """
        SELECT
            e.extname AS name,
            n.nspname AS schema,
            e.extversion AS version
        FROM pg_extension e
        JOIN pg_namespace n ON n.oid = e.extnamespace
        ORDER BY e.extname
        """
        return await self.execute_sql(query, workspace_id)
    
    @handle_errors
    @read_only_check
    async def apply_migration(self, name: str, query: str, workspace_id: Optional[str] = None) -> dict:
        await self.execute_sql(query, workspace_id)
        return {"success": True, "message": f"Migration {name} applied successfully"}
