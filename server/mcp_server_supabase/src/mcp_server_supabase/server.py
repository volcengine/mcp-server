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
default_workspace_id = os.getenv("DEFAULT_WORKSPACE_ID")

edge_tools = EdgeFunctionTools(aidap_client, default_workspace_id)
storage_tools = StorageTools(aidap_client, default_workspace_id)
database_tools = DatabaseTools(aidap_client, default_workspace_id)
workspace_tools = WorkspaceTools(aidap_client, default_workspace_id)


@mcp.tool()
async def list_edge_functions(workspace_id: str = None) -> str:
    """Lists all Edge Functions in a workspace."""
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
    workspace_id: str = None
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
        workspace_id: The workspace ID (optional)
    """
    return await edge_tools.deploy_edge_function(
        function_name, source_code, verify_jwt, runtime, import_map, workspace_id
    )


@mcp.tool()
async def delete_edge_function(function_name: str, workspace_id: str = None) -> str:
    """Deletes an Edge Function."""
    return await edge_tools.delete_edge_function(function_name, workspace_id)


@mcp.tool()
async def invoke_edge_function(
    function_name: str,
    payload: str = None,
    method: str = "POST",
    workspace_id: str = None
) -> str:
    """Invokes an Edge Function."""
    return await edge_tools.invoke_edge_function(function_name, payload, method, workspace_id)


@mcp.tool()
async def list_storage_buckets(workspace_id: str = None) -> str:
    """Lists all storage buckets in a workspace."""
    return await storage_tools.list_storage_buckets(workspace_id)


@mcp.tool()
async def create_storage_bucket(
    bucket_name: str,
    public: bool = False,
    file_size_limit: int = None,
    allowed_mime_types: str = None,
    workspace_id: str = None
) -> str:
    """Creates a new storage bucket."""
    return await storage_tools.create_storage_bucket(
        bucket_name, public, file_size_limit, allowed_mime_types, workspace_id
    )


@mcp.tool()
async def delete_storage_bucket(bucket_name: str, workspace_id: str = None) -> str:
    """Deletes a storage bucket."""
    return await storage_tools.delete_storage_bucket(bucket_name, workspace_id)


@mcp.tool()
async def get_storage_config(workspace_id: str = None) -> str:
    """Gets the storage configuration for a workspace."""
    return await storage_tools.get_storage_config(workspace_id)


@mcp.tool()
async def update_storage_config(config: str, workspace_id: str = None) -> str:
    """Updates the storage configuration for a workspace."""
    import json
    parsed_config = json.loads(config)
    return await storage_tools.update_storage_config(parsed_config, workspace_id)


@mcp.tool()
async def execute_sql(query: str, workspace_id: str = None) -> str:
    """Executes raw SQL in the Postgres database."""
    return await database_tools.execute_sql(query, workspace_id)


@mcp.tool()
async def list_tables(schemas: str = "public", workspace_id: str = None) -> str:
    """Lists all tables in one or more schemas."""
    schema_list = [s.strip() for s in schemas.split(",")]
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
    schema_list = [s.strip() for s in schemas.split(",") if s.strip()]
    return await database_tools.generate_typescript_types(schema_list, workspace_id)


@mcp.tool()
async def list_workspaces() -> str:
    """Lists all available workspaces."""
    return await workspace_tools.list_workspaces()


@mcp.tool()
async def get_workspace(workspace_id: str) -> str:
    """Gets details for a specific workspace."""
    return await workspace_tools.get_workspace(workspace_id)


@mcp.tool()
async def create_workspace(
    workspace_name: str,
    engine_version: str = "Supabase_1_24",
    engine_type: str = "Supabase"
) -> str:
    """Creates a new workspace."""
    return await workspace_tools.create_workspace(workspace_name, engine_version, engine_type)


@mcp.tool()
async def start_workspace(workspace_id: str = None) -> str:
    """Starts a workspace."""
    return await workspace_tools.start_workspace(workspace_id)


@mcp.tool()
async def stop_workspace(workspace_id: str = None) -> str:
    """Stops a workspace."""
    return await workspace_tools.stop_workspace(workspace_id)


@mcp.tool()
async def get_workspace_endpoints(workspace_id: str = None) -> str:
    """Gets API endpoint URL for a workspace."""
    return await workspace_tools.get_workspace_endpoints(workspace_id)


@mcp.tool()
async def get_workspace_api_keys(workspace_id: str = None) -> str:
    """Gets API keys for a workspace."""
    return await workspace_tools.get_workspace_api_keys(workspace_id)


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
    """Resets migrations of a development branch. Any untracked data or schema changes will be lost."""
    return await workspace_tools.reset_branch(branch_id, migration_version, workspace_id)


def main():
    parser = argparse.ArgumentParser(description="Supabase MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    args = parser.parse_args()
    
    logger.info(f"Starting Supabase MCP Server on port {args.port}")
    logger.info(f"Read-only mode: {READ_ONLY}")
    if default_workspace_id:
        logger.info(f"Default workspace ID: {default_workspace_id}")
    
    mcp.run()


if __name__ == "__main__":
    main()
