# Supabase MCP Server

Supabase MCP server for AIDAP workspaces.

## Overview

This server exposes Supabase capabilities through MCP and uses AIDAP workspaces as the primary resource model.

Supported areas:

- workspace lifecycle
- branch lifecycle
- database access
- Edge Functions
- storage
- TypeScript type generation

## Environment Variables

| Name | Required | Description |
| --- | --- | --- |
| `VOLCENGINE_ACCESS_KEY` | Yes | Volcengine access key |
| `VOLCENGINE_SECRET_KEY` | Yes | Volcengine secret key |
| `VOLCENGINE_REGION` | No | Region, default `cn-beijing` |
| `READ_ONLY` | No | Set to `true` to block write operations |
| `DEFAULT_WORKSPACE_ID` | No | Default workspace used when `workspace_id` is omitted |
| `SUPABASE_WORKSPACE_SLUG` | No | Edge Functions slug, default `default` |
| `SUPABASE_ENDPOINT_SCHEME` | No | `http` or `https`, default `http` |

## Run

```bash
python -m mcp_server_supabase.server
```

## MCP Client Example

```json
{
  "mcpServers": {
    "supabase": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server_supabase.server"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "cn-beijing",
        "DEFAULT_WORKSPACE_ID": "ws-xxxxxxxx"
      }
    }
  }
}
```

## Tools

### Workspace

- `list_workspaces`
- `get_workspace`
- `create_workspace`
- `pause_workspace`
- `restore_workspace`
- `get_workspace_url`
- `get_publishable_keys`

### Branch

- `list_branches`
- `create_branch`
- `delete_branch`
- `reset_branch`

### Database

- `execute_sql`
- `list_tables`
- `list_migrations`
- `list_extensions`
- `apply_migration`
- `generate_typescript_types`

### Edge Functions

- `list_edge_functions`
- `get_edge_function`
- `deploy_edge_function`
- `delete_edge_function`

### Storage

- `list_storage_buckets`
- `create_storage_bucket`
- `delete_storage_bucket`
- `get_storage_config`
- `update_storage_config`

## Usage Notes

- Any `workspace_id` parameter can also accept a branch ID.
- When `workspace_id` is omitted, the server uses `DEFAULT_WORKSPACE_ID` if configured.
- `get_publishable_keys` resolves the default branch automatically when needed.
