from dataclasses import dataclass
from typing import Awaitable, Callable

from mcp.server.fastmcp import FastMCP

from .runtime import SupabaseRuntime


ToolBuilder = Callable[[SupabaseRuntime], Callable[..., Awaitable[str]]]


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    feature: str
    scoped: bool
    mutating: bool
    build: ToolBuilder


def _build_list_edge_functions(runtime: SupabaseRuntime):
    edge_tools = runtime.edge_tools

    async def list_edge_functions(workspace_id: str = None) -> str:
        """Lists all Edge Functions in a workspace."""
        return await edge_tools.list_edge_functions(workspace_id)

    return list_edge_functions


def _build_get_edge_function(runtime: SupabaseRuntime):
    edge_tools = runtime.edge_tools

    async def get_edge_function(function_name: str, workspace_id: str = None) -> str:
        """Retrieves the source code and configuration for an Edge Function."""
        return await edge_tools.get_edge_function(function_name, workspace_id)

    return get_edge_function


def _build_deploy_edge_function(runtime: SupabaseRuntime):
    edge_tools = runtime.edge_tools

    async def deploy_edge_function(
        function_name: str,
        source_code: str,
        verify_jwt: bool = True,
        runtime: str = "native-node20/v1",
        import_map: str = None,
        workspace_id: str = None,
    ) -> str:
        """Deploys a new Edge Function or updates an existing one.

        Args:
            function_name: Name of the function to deploy
            source_code: Source code for the function
            verify_jwt: Whether to verify JWT tokens
            runtime: Runtime environment
            import_map: Optional import map JSON for dependencies
            workspace_id: The workspace ID
        """
        return await edge_tools.deploy_edge_function(
            function_name,
            source_code,
            verify_jwt,
            runtime,
            import_map,
            workspace_id,
        )

    return deploy_edge_function


def _build_delete_edge_function(runtime: SupabaseRuntime):
    edge_tools = runtime.edge_tools

    async def delete_edge_function(function_name: str, workspace_id: str = None) -> str:
        """Deletes an Edge Function."""
        return await edge_tools.delete_edge_function(function_name, workspace_id)

    return delete_edge_function


def _build_list_storage_buckets(runtime: SupabaseRuntime):
    storage_tools = runtime.storage_tools

    async def list_storage_buckets(workspace_id: str = None) -> str:
        """Lists all storage buckets in a workspace."""
        return await storage_tools.list_storage_buckets(workspace_id)

    return list_storage_buckets


def _build_create_storage_bucket(runtime: SupabaseRuntime):
    storage_tools = runtime.storage_tools

    async def create_storage_bucket(
        bucket_name: str,
        public: bool = False,
        file_size_limit: int = None,
        allowed_mime_types: str | list[str] = None,
        workspace_id: str = None,
    ) -> str:
        """Creates a new storage bucket."""
        return await storage_tools.create_storage_bucket(
            bucket_name,
            public,
            file_size_limit,
            allowed_mime_types,
            workspace_id,
        )

    return create_storage_bucket


def _build_delete_storage_bucket(runtime: SupabaseRuntime):
    storage_tools = runtime.storage_tools

    async def delete_storage_bucket(bucket_name: str, workspace_id: str = None) -> str:
        """Deletes a storage bucket."""
        return await storage_tools.delete_storage_bucket(bucket_name, workspace_id)

    return delete_storage_bucket


def _build_get_storage_config(runtime: SupabaseRuntime):
    storage_tools = runtime.storage_tools

    async def get_storage_config(workspace_id: str = None) -> str:
        """Gets the storage configuration for a workspace."""
        return await storage_tools.get_storage_config(workspace_id)

    return get_storage_config


def _build_execute_sql(runtime: SupabaseRuntime):
    database_tools = runtime.database_tools

    async def execute_sql(query: str, workspace_id: str = None) -> str:
        """Executes raw SQL in the Postgres database."""
        return await database_tools.execute_sql(query, workspace_id)

    return execute_sql


def _build_list_tables(runtime: SupabaseRuntime):
    database_tools = runtime.database_tools

    async def list_tables(schemas: str = "public", workspace_id: str = None) -> str:
        """Lists all tables in one or more schemas."""
        schema_list = [schema.strip() for schema in schemas.split(",")]
        return await database_tools.list_tables(schema_list, workspace_id)

    return list_tables


def _build_list_migrations(runtime: SupabaseRuntime):
    database_tools = runtime.database_tools

    async def list_migrations(workspace_id: str = None) -> str:
        """Lists all migrations in the database."""
        return await database_tools.list_migrations(workspace_id)

    return list_migrations


def _build_list_extensions(runtime: SupabaseRuntime):
    database_tools = runtime.database_tools

    async def list_extensions(workspace_id: str = None) -> str:
        """Lists all PostgreSQL extensions in the database."""
        return await database_tools.list_extensions(workspace_id)

    return list_extensions


def _build_apply_migration(runtime: SupabaseRuntime):
    database_tools = runtime.database_tools

    async def apply_migration(name: str, query: str, workspace_id: str = None) -> str:
        """Applies a migration to the database."""
        return await database_tools.apply_migration(name, query, workspace_id)

    return apply_migration


def _build_generate_typescript_types(runtime: SupabaseRuntime):
    database_tools = runtime.database_tools

    async def generate_typescript_types(schemas: str = "public", workspace_id: str = None) -> str:
        """Generates TypeScript definitions from database schema."""
        schema_list = [schema.strip() for schema in schemas.split(",") if schema.strip()]
        return await database_tools.generate_typescript_types(schema_list, workspace_id)

    return generate_typescript_types


def _build_list_workspaces(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def list_workspaces() -> str:
        """Lists all available workspaces."""
        return await workspace_tools.list_workspaces()

    return list_workspaces


def _build_get_workspace(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def get_workspace(workspace_id: str) -> str:
        """Gets details for a specific workspace."""
        return await workspace_tools.get_workspace(workspace_id)

    return get_workspace


def _build_create_workspace(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def create_workspace(
        workspace_name: str,
        engine_version: str = "Supabase_1_24",
        engine_type: str = "Supabase",
    ) -> str:
        """Creates a new workspace."""
        return await workspace_tools.create_workspace(workspace_name, engine_version, engine_type)

    return create_workspace


def _build_pause_workspace(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def pause_workspace(workspace_id: str = None) -> str:
        """Pauses a workspace."""
        return await workspace_tools.pause_workspace(workspace_id)

    return pause_workspace


def _build_restore_workspace(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def restore_workspace(workspace_id: str = None) -> str:
        """Restores a workspace."""
        return await workspace_tools.restore_workspace(workspace_id)

    return restore_workspace


def _build_get_workspace_url(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def get_workspace_url(workspace_id: str = None) -> str:
        """Gets API endpoint URL for a workspace."""
        return await workspace_tools.get_workspace_url(workspace_id)

    return get_workspace_url


def _build_get_publishable_keys(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def get_publishable_keys(workspace_id: str = None, reveal: bool = False) -> str:
        """Gets API keys for a workspace."""
        return await workspace_tools.get_publishable_keys(workspace_id, reveal)

    return get_publishable_keys


def _build_list_branches(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def list_branches(workspace_id: str = None) -> str:
        """Lists all development branches of a workspace."""
        return await workspace_tools.list_branches(workspace_id)

    return list_branches


def _build_create_branch(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def create_branch(name: str = "develop", workspace_id: str = None) -> str:
        """Creates a development branch."""
        return await workspace_tools.create_branch(name, workspace_id)

    return create_branch


def _build_delete_branch(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def delete_branch(branch_id: str, workspace_id: str = None) -> str:
        """Deletes a development branch."""
        return await workspace_tools.delete_branch(branch_id, workspace_id)

    return delete_branch


def _build_restore_branch(runtime: SupabaseRuntime):
    workspace_tools = runtime.workspace_tools

    async def restore_branch(
        branch_id: str,
        source_branch_id: str = None,
        time: str = None,
        workspace_id: str = None,
    ) -> str:
        """Restores branch data to a specified point in time and returns the restored branch ID."""
        return await workspace_tools.restore_branch(branch_id, source_branch_id, time, workspace_id)

    return restore_branch


TOOL_DEFINITIONS = (
    ToolDefinition("list_workspaces", "account", False, False, _build_list_workspaces),
    ToolDefinition("get_workspace", "account", True, False, _build_get_workspace),
    ToolDefinition("create_workspace", "account", False, True, _build_create_workspace),
    ToolDefinition("pause_workspace", "account", True, True, _build_pause_workspace),
    ToolDefinition("restore_workspace", "account", True, True, _build_restore_workspace),
    ToolDefinition("execute_sql", "database", True, True, _build_execute_sql),
    ToolDefinition("list_tables", "database", True, False, _build_list_tables),
    ToolDefinition("list_migrations", "database", True, False, _build_list_migrations),
    ToolDefinition("list_extensions", "database", True, False, _build_list_extensions),
    ToolDefinition("apply_migration", "database", True, True, _build_apply_migration),
    ToolDefinition("get_workspace_url", "development", True, False, _build_get_workspace_url),
    ToolDefinition("get_publishable_keys", "development", True, False, _build_get_publishable_keys),
    ToolDefinition("generate_typescript_types", "development", True, False, _build_generate_typescript_types),
    ToolDefinition("list_edge_functions", "functions", True, False, _build_list_edge_functions),
    ToolDefinition("get_edge_function", "functions", True, False, _build_get_edge_function),
    ToolDefinition("deploy_edge_function", "functions", True, True, _build_deploy_edge_function),
    ToolDefinition("delete_edge_function", "functions", True, True, _build_delete_edge_function),
    ToolDefinition("list_storage_buckets", "storage", True, False, _build_list_storage_buckets),
    ToolDefinition("create_storage_bucket", "storage", True, True, _build_create_storage_bucket),
    ToolDefinition("delete_storage_bucket", "storage", True, True, _build_delete_storage_bucket),
    ToolDefinition("get_storage_config", "storage", True, False, _build_get_storage_config),
    ToolDefinition("list_branches", "branching", True, False, _build_list_branches),
    ToolDefinition("create_branch", "branching", True, True, _build_create_branch),
    ToolDefinition("delete_branch", "branching", True, True, _build_delete_branch),
    ToolDefinition("restore_branch", "branching", True, True, _build_restore_branch),
)


def register_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    for tool_definition in TOOL_DEFINITIONS:
        mcp.tool()(tool_definition.build(runtime))
