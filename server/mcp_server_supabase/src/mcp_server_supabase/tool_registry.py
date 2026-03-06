import json

from mcp.server.fastmcp import FastMCP

from .runtime import SupabaseRuntime


def register_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    _register_edge_tools(mcp, runtime)
    _register_storage_tools(mcp, runtime)
    _register_database_tools(mcp, runtime)
    _register_project_tools(mcp, runtime)


def _register_edge_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    edge_tools = runtime.edge_tools

    @mcp.tool()
    async def list_edge_functions(project_id: str = None) -> str:
        """Lists all Edge Functions in a project."""
        return await edge_tools.list_edge_functions(project_id)

    @mcp.tool()
    async def get_edge_function(function_name: str, project_id: str = None) -> str:
        """Retrieves the source code and configuration for an Edge Function."""
        return await edge_tools.get_edge_function(function_name, project_id)

    @mcp.tool()
    async def deploy_edge_function(
        function_name: str,
        source_code: str,
        verify_jwt: bool = True,
        runtime: str = "native-node20/v1",
        import_map: str = None,
        project_id: str = None,
    ) -> str:
        """Deploys a new Edge Function or updates an existing one.

        Args:
            function_name: Name of the function to deploy
            source_code: Source code for the function
            verify_jwt: Whether to verify JWT tokens (default: True)
            runtime: Runtime environment (default: native-node20/v1)
                     Options: native-node20/v1, native-python3.9/v1,
                             native-python3.10/v1, native-python3.12/v1
            import_map: Optional import map JSON for dependencies
            project_id: The project ID (optional)
        """
        return await edge_tools.deploy_edge_function(
            function_name,
            source_code,
            verify_jwt,
            runtime,
            import_map,
            project_id,
        )

    @mcp.tool()
    async def delete_edge_function(function_name: str, project_id: str = None) -> str:
        """Deletes an Edge Function."""
        return await edge_tools.delete_edge_function(function_name, project_id)


def _register_storage_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    storage_tools = runtime.storage_tools

    @mcp.tool()
    async def list_storage_buckets(project_id: str = None) -> str:
        """Lists all storage buckets in a project."""
        return await storage_tools.list_storage_buckets(project_id)

    @mcp.tool()
    async def create_storage_bucket(
        bucket_name: str,
        public: bool = False,
        file_size_limit: int = None,
        allowed_mime_types: str | list[str] = None,
        project_id: str = None,
    ) -> str:
        """Creates a new storage bucket."""
        return await storage_tools.create_storage_bucket(
            bucket_name,
            public,
            file_size_limit,
            allowed_mime_types,
            project_id,
        )

    @mcp.tool()
    async def delete_storage_bucket(bucket_name: str, project_id: str = None) -> str:
        """Deletes a storage bucket."""
        return await storage_tools.delete_storage_bucket(bucket_name, project_id)

    @mcp.tool()
    async def get_storage_config(project_id: str = None) -> str:
        """Gets the storage configuration for a project."""
        return await storage_tools.get_storage_config(project_id)

    @mcp.tool()
    async def update_storage_config(config: str, project_id: str = None) -> str:
        """Updates the storage configuration for a project."""
        return await storage_tools.update_storage_config(json.loads(config), project_id)


def _register_database_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    database_tools = runtime.database_tools

    @mcp.tool()
    async def execute_sql(query: str, project_id: str = None) -> str:
        """Executes raw SQL in the Postgres database."""
        return await database_tools.execute_sql(query, project_id)

    @mcp.tool()
    async def list_tables(schemas: str = "public", project_id: str = None) -> str:
        """Lists all tables in one or more schemas."""
        schema_list = [schema.strip() for schema in schemas.split(",")]
        return await database_tools.list_tables(schema_list, project_id)

    @mcp.tool()
    async def list_migrations(project_id: str = None) -> str:
        """Lists all migrations in the database."""
        return await database_tools.list_migrations(project_id)

    @mcp.tool()
    async def list_extensions(project_id: str = None) -> str:
        """Lists all PostgreSQL extensions in the database."""
        return await database_tools.list_extensions(project_id)

    @mcp.tool()
    async def apply_migration(name: str, query: str, project_id: str = None) -> str:
        """Applies a migration to the database."""
        return await database_tools.apply_migration(name, query, project_id)

    @mcp.tool()
    async def generate_typescript_types(schemas: str = "public", project_id: str = None) -> str:
        """Generates TypeScript definitions from database schema."""
        schema_list = [schema.strip() for schema in schemas.split(",") if schema.strip()]
        return await database_tools.generate_typescript_types(schema_list, project_id)


def _register_project_tools(mcp: FastMCP, runtime: SupabaseRuntime) -> None:
    workspace_tools = runtime.workspace_tools

    @mcp.tool()
    async def list_projects() -> str:
        """Lists all available projects."""
        return await workspace_tools.list_projects()

    @mcp.tool()
    async def get_project(project_id: str) -> str:
        """Gets details for a specific project."""
        return await workspace_tools.get_project(project_id)

    @mcp.tool()
    async def create_project(
        project_name: str,
        engine_version: str = "Supabase_1_24",
        engine_type: str = "Supabase",
    ) -> str:
        """Creates a new project."""
        return await workspace_tools.create_project(project_name, engine_version, engine_type)

    @mcp.tool()
    async def pause_project(project_id: str = None) -> str:
        """Pauses a project."""
        return await workspace_tools.pause_project(project_id)

    @mcp.tool()
    async def restore_project(project_id: str = None) -> str:
        """Restores a project."""
        return await workspace_tools.restore_project(project_id)

    @mcp.tool()
    async def get_project_url(project_id: str = None) -> str:
        """Gets API endpoint URL for a project."""
        return await workspace_tools.get_project_url(project_id)

    @mcp.tool()
    async def get_publishable_keys(project_id: str = None, reveal: bool = False) -> str:
        """Gets API keys for a project."""
        return await workspace_tools.get_publishable_keys(project_id, reveal)

    @mcp.tool()
    async def list_branches(project_id: str = None) -> str:
        """Lists all development branches of a project."""
        return await workspace_tools.list_branches(project_id)

    @mcp.tool()
    async def create_branch(name: str = "develop", project_id: str = None) -> str:
        """Creates a development branch."""
        return await workspace_tools.create_branch(name, project_id)

    @mcp.tool()
    async def delete_branch(branch_id: str, project_id: str = None) -> str:
        """Deletes a development branch."""
        return await workspace_tools.delete_branch(branch_id, project_id)

    @mcp.tool()
    async def reset_branch(branch_id: str, migration_version: str = None, project_id: str = None) -> str:
        """Resets migrations of a development branch. Any untracked data or schema changes will be lost."""
        return await workspace_tools.reset_branch(branch_id, migration_version, project_id)
