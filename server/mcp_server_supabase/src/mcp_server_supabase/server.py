"""Supabase MCP Server - Refactored Version"""

import argparse
import logging
import os
from mcp.server.fastmcp import FastMCP

from .config import READ_ONLY
from .platform import AidapClient
from .tools import EdgeFunctionTools, StorageTools, DatabaseTools, WorkspaceTools

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

mcp = FastMCP("Supabase MCP Server (AIDAP)", port=int(os.getenv("PORT", "8000")))

aidap_client = AidapClient()
default_project_id = os.getenv("DEFAULT_PROJECT_ID") or os.getenv("DEFAULT_WORKSPACE_ID")

edge_tools = EdgeFunctionTools(aidap_client, default_project_id)
storage_tools = StorageTools(aidap_client, default_project_id)
database_tools = DatabaseTools(aidap_client, default_project_id)
workspace_tools = WorkspaceTools(aidap_client, default_project_id)


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
    project_id: str = None
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
        function_name, source_code, verify_jwt, runtime, import_map, project_id
    )


@mcp.tool()
async def delete_edge_function(function_name: str, project_id: str = None) -> str:
    """Deletes an Edge Function."""
    return await edge_tools.delete_edge_function(function_name, project_id)


@mcp.tool()
async def list_storage_buckets(project_id: str = None) -> str:
    """Lists all storage buckets in a project."""
    return await storage_tools.list_storage_buckets(project_id)


@mcp.tool()
async def create_storage_bucket(
    bucket_name: str,
    public: bool = False,
    file_size_limit: int = None,
    allowed_mime_types: str = None,
    project_id: str = None
) -> str:
    """Creates a new storage bucket."""
    return await storage_tools.create_storage_bucket(
        bucket_name, public, file_size_limit, allowed_mime_types, project_id
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
    import json
    parsed_config = json.loads(config)
    return await storage_tools.update_storage_config(parsed_config, project_id)


@mcp.tool()
async def execute_sql(query: str, project_id: str = None) -> str:
    """Executes raw SQL in the Postgres database."""
    return await database_tools.execute_sql(query, project_id)


@mcp.tool()
async def list_tables(schemas: str = "public", project_id: str = None) -> str:
    """Lists all tables in one or more schemas."""
    schema_list = [s.strip() for s in schemas.split(",")]
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
    schema_list = [s.strip() for s in schemas.split(",") if s.strip()]
    return await database_tools.generate_typescript_types(schema_list, project_id)


@mcp.tool()
async def list_workspaces() -> str:
    """Lists all available workspaces."""
    return await workspace_tools.list_workspaces()


@mcp.tool()
async def get_workspace(project_id: str) -> str:
    """Gets details for a specific project."""
    return await workspace_tools.get_workspace(project_id)


@mcp.tool()
async def create_workspace(
    project_name: str,
    engine_version: str = "Supabase_1_24",
    engine_type: str = "Supabase"
) -> str:
    """Creates a new project."""
    return await workspace_tools.create_workspace(project_name, engine_version, engine_type)


@mcp.tool()
async def start_workspace(project_id: str = None) -> str:
    """Starts a project."""
    return await workspace_tools.start_workspace(project_id)


@mcp.tool()
async def stop_workspace(project_id: str = None) -> str:
    """Stops a project."""
    return await workspace_tools.stop_workspace(project_id)


@mcp.tool()
async def get_workspace_endpoints(project_id: str = None) -> str:
    """Gets API endpoint URL for a project."""
    return await workspace_tools.get_workspace_endpoints(project_id)


@mcp.tool()
async def get_workspace_api_keys(project_id: str = None, reveal: bool = False) -> str:
    """Gets API keys for a project."""
    return await workspace_tools.get_workspace_api_keys(project_id, reveal)


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
    engine_type: str = "Supabase"
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


def main():
    parser = argparse.ArgumentParser(description="Supabase MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    
    logger.info(f"Starting Supabase MCP Server on port {args.port}")
    logger.info(f"Read-only mode: {READ_ONLY}")
    if default_project_id:
        logger.info(f"Default project ID: {default_project_id}")
    
    mcp.run()


if __name__ == "__main__":
    main()
