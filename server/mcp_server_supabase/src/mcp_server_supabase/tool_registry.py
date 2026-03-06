from mcp.server.fastmcp import FastMCP

from .runtime import SupabaseRuntime


def register_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    _register_edge_tools(mcp, runtime)
    _register_storage_tools(mcp, runtime)
    _register_database_tools(mcp, runtime)
    _register_workspace_tools(mcp, runtime)


def _register_edge_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    edge_tools = runtime.edge_tools

    @mcp.tool()
    async def list_edge_functions(workspace_id: str = None) -> str:
        """Lists all Edge Functions in a workspace or branch."""
        return await edge_tools.list_edge_functions(workspace_id)

    @mcp.tool()
    async def get_edge_function(function_name: str, workspace_id: str = None) -> str:
        """Retrieves the source code and configuration for an Edge Function."""
        return await edge_tools.get_edge_function(function_name, workspace_id)

    @mcp.tool()
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
            workspace_id: The workspace ID or branch ID
        """
        return await edge_tools.deploy_edge_function(
            function_name,
            source_code,
            verify_jwt,
            runtime,
            import_map,
            workspace_id,
        )

    @mcp.tool()
    async def delete_edge_function(function_name: str, workspace_id: str = None) -> str:
        """Deletes an Edge Function."""
        return await edge_tools.delete_edge_function(function_name, workspace_id)


def _register_storage_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    storage_tools = runtime.storage_tools

    @mcp.tool()
    async def list_storage_buckets(workspace_id: str = None) -> str:
        """Lists all storage buckets in a workspace or branch."""
        return await storage_tools.list_storage_buckets(workspace_id)

    @mcp.tool()
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

    @mcp.tool()
    async def delete_storage_bucket(bucket_name: str, workspace_id: str = None) -> str:
        """Deletes a storage bucket."""
        return await storage_tools.delete_storage_bucket(bucket_name, workspace_id)

    @mcp.tool()
    async def get_storage_config(workspace_id: str = None) -> str:
        """Gets the storage configuration for a workspace or branch."""
        return await storage_tools.get_storage_config(workspace_id)

def _register_database_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    database_tools = runtime.database_tools

    @mcp.tool()
    async def execute_sql(query: str, workspace_id: str = None) -> str:
        """Executes raw SQL in the Postgres database."""
        return await database_tools.execute_sql(query, workspace_id)

    @mcp.tool()
    async def list_tables(schemas: str = "public", workspace_id: str = None) -> str:
        """Lists all tables in one or more schemas."""
        schema_list = [schema.strip() for schema in schemas.split(",")]
        return await database_tools.list_tables(schema_list, workspace_id)

    @mcp.tool()
    async def list_migrations(workspace_id: str = None) -> str:
        """Lists all migrations in the database."""
        return await database_tools.list_migrations(workspace_id)

    @mcp.tool()
    async def list_extensions(workspace_id: str = None) -> str:
        """Lists all PostgreSQL extensions in the database."""
        return await database_tools.list_extensions(workspace_id)

    @mcp.tool()
    async def apply_migration(name: str, query: str, workspace_id: str = None) -> str:
        """Applies a migration to the database."""
        return await database_tools.apply_migration(name, query, workspace_id)

    @mcp.tool()
    async def generate_typescript_types(schemas: str = "public", workspace_id: str = None) -> str:
        """Generates TypeScript definitions from database schema."""
        schema_list = [schema.strip() for schema in schemas.split(",") if schema.strip()]
        return await database_tools.generate_typescript_types(schema_list, workspace_id)


def _register_workspace_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    workspace_tools = runtime.workspace_tools

    @mcp.tool()
    async def list_workspaces() -> str:
        """Lists all available workspaces."""
        return await workspace_tools.list_workspaces()

    @mcp.tool()
    async def get_workspace(workspace_id: str) -> str:
        """Gets details for a specific workspace or branch target."""
        return await workspace_tools.get_workspace(workspace_id)

    @mcp.tool()
    async def create_workspace(
        workspace_name: str,
        engine_version: str = "Supabase_1_24",
        engine_type: str = "Supabase",
    ) -> str:
        """Creates a new workspace."""
        return await workspace_tools.create_workspace(workspace_name, engine_version, engine_type)

    @mcp.tool()
    async def pause_workspace(workspace_id: str = None) -> str:
        """Pauses a workspace."""
        return await workspace_tools.pause_workspace(workspace_id)

    @mcp.tool()
    async def restore_workspace(workspace_id: str = None) -> str:
        """Restores a workspace."""
        return await workspace_tools.restore_workspace(workspace_id)

    @mcp.tool()
    async def get_workspace_url(workspace_id: str = None) -> str:
        """Gets API endpoint URL for a workspace or branch."""
        return await workspace_tools.get_workspace_url(workspace_id)

    @mcp.tool()
    async def get_publishable_keys(workspace_id: str = None, reveal: bool = False) -> str:
        """Gets API keys for a workspace or branch."""
        return await workspace_tools.get_publishable_keys(workspace_id, reveal)

    @mcp.tool()
    async def list_branches(workspace_id: str = None) -> str:
        """Lists all development branches of a workspace."""
        return await workspace_tools.list_branches(workspace_id)

    @mcp.tool()
    async def create_branch(name: str = "develop", workspace_id: str = None) -> str:
        """Creates a development branch."""
        return await workspace_tools.create_branch(name, workspace_id)

    @mcp.tool()
    async def delete_branch(branch_id: str, workspace_id: str = None) -> str:
        """Deletes a development branch."""
        return await workspace_tools.delete_branch(branch_id, workspace_id)

    @mcp.tool()
    async def reset_branch(branch_id: str, migration_version: str = None, workspace_id: str = None) -> str:
        """Resets a development branch. Any untracked data or schema changes will be lost."""
        return await workspace_tools.reset_branch(branch_id, migration_version, workspace_id)
