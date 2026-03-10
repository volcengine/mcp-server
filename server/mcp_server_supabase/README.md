# Supabase MCP Server

English | [简体中文](README_zh.md)

> Supabase MCP server for AIDAP workspaces. It exposes workspace, branch, database, Edge Functions, storage, and TypeScript type generation capabilities through MCP.

| Item | Details |
| ---- | ---- |
| Version | v0.1.0 |
| Description | Supabase MCP server built on top of AIDAP workspaces |
| Category | Database / Developer Tools |
| Tags | Supabase, PostgreSQL, Edge Functions, Storage, AIDAP |

## Tools

### Workspace and Branch

| Tool | Description |
| ---- | ---- |
| `list_workspaces` | List all available Supabase workspaces in the current account |
| `get_workspace` | Get workspace details; branch IDs are also accepted |
| `create_workspace` | Create a new Supabase workspace |
| `pause_workspace` | Pause a workspace |
| `restore_workspace` | Resume a paused workspace |
| `get_workspace_url` | Get the API endpoint for a workspace or branch |
| `get_publishable_keys` | Get publishable, anon, and service role keys |
| `list_branches` | List branches under a workspace |
| `create_branch` | Create a development branch |
| `delete_branch` | Delete a development branch |
| `reset_branch` | Reset a branch to its baseline state |

### Database

| Tool | Description |
| ---- | ---- |
| `execute_sql` | Execute raw SQL against the Postgres database |
| `list_tables` | List tables in one or more schemas |
| `list_migrations` | List records from `supabase_migrations.schema_migrations` |
| `list_extensions` | List installed PostgreSQL extensions |
| `apply_migration` | Run migration SQL and record it in `supabase_migrations.schema_migrations` |
| `generate_typescript_types` | Generate TypeScript definitions from schema metadata |

### Edge Functions

| Tool | Description |
| ---- | ---- |
| `list_edge_functions` | List Edge Functions in a workspace or branch |
| `get_edge_function` | Get the source code and configuration of an Edge Function |
| `deploy_edge_function` | Create or update an Edge Function |
| `delete_edge_function` | Delete an Edge Function |

### Storage

| Tool | Description |
| ---- | ---- |
| `list_storage_buckets` | List storage buckets |
| `create_storage_bucket` | Create a new storage bucket |
| `delete_storage_bucket` | Delete a storage bucket |
| `get_storage_config` | Get storage configuration |

## Authentication

Use Volcengine AK/SK authentication. Obtain your credentials from the [Volcengine API Access Key console](https://console.volcengine.com/iam/keymanage/).

## Environment Variables

| Name | Required | Default | Description |
| ---- | ---- | ---- | ---- |
| `VOLCENGINE_ACCESS_KEY` | Yes | - | Volcengine access key |
| `VOLCENGINE_SECRET_KEY` | Yes | - | Volcengine secret key |
| `VOLCENGINE_REGION` | No | `cn-beijing` | Region used for the AIDAP API |
| `DEFAULT_WORKSPACE_ID` | No | - | Default target used when `workspace_id` is omitted |
| `READ_ONLY` | No | `false` | Set to `true` to block all mutating tools |
| `SUPABASE_WORKSPACE_SLUG` | No | `default` | Project slug used by Edge Functions APIs |
| `SUPABASE_ENDPOINT_SCHEME` | No | `http` | Endpoint scheme used when building workspace URLs |
| `MCP_SERVER_HOST` | No | `0.0.0.0` | Host used by `sse` and `streamable-http` transports |
| `MCP_SERVER_PORT` | No | `8000` | Preferred port variable for network transports |
| `PORT` | No | `8000` | Backward-compatible port variable |
| `MCP_MOUNT_PATH` | No | `/` | Base mount path for HTTP transports |
| `MCP_SSE_PATH` | No | `/sse` | SSE endpoint path |
| `MCP_MESSAGE_PATH` | No | `/messages/` | SSE message POST path |
| `STREAMABLE_HTTP_PATH` | No | `/mcp` | Streamable HTTP endpoint path |

## Deployment

### Run from a local checkout

```bash
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase
```

### Run with an explicit transport

```bash
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase --transport stdio
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase --transport sse --host 0.0.0.0 --port 8000
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase --transport streamable-http --host 0.0.0.0 --port 8000
```

### Dedicated network entrypoints

```bash
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase-sse
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase-streamable
```

### MCP client config with local source

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase",
        "run",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "<your-access-key>",
        "VOLCENGINE_SECRET_KEY": "<your-secret-key>",
        "VOLCENGINE_REGION": "cn-beijing",
        "DEFAULT_WORKSPACE_ID": "ws-xxxxxxxx"
      }
    }
  }
}
```

### MCP client config with `uvx`

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_supabase",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "<your-access-key>",
        "VOLCENGINE_SECRET_KEY": "<your-secret-key>",
        "VOLCENGINE_REGION": "cn-beijing",
        "DEFAULT_WORKSPACE_ID": "ws-xxxxxxxx"
      }
    }
  }
}
```

### Direct Python entrypoint

```bash
python3 -m mcp_server_supabase.server --port 8000
python3 -m mcp_server_supabase.server --transport sse --host 0.0.0.0 --port 8000
```

The package exposes `mcp-server-supabase`, `supabase-aidap`, `mcp-server-supabase-sse`, and `mcp-server-supabase-streamable`. The examples above use `mcp-server-supabase`.

## Usage Notes

- If `workspace_id` is omitted, the server falls back to `DEFAULT_WORKSPACE_ID` when configured.
- If a branch ID such as `br-xxxx` is provided, the server resolves the corresponding workspace automatically.
- `get_publishable_keys` resolves the default branch automatically when needed.
- `reset_branch` accepts `migration_version`, but the current AIDAP API ignores that value and performs a branch reset only.
- `deploy_edge_function` currently supports `native-node20/v1`, `native-python3.9/v1`, `native-python3.10/v1`, and `native-python3.12/v1`.
- `--transport sse` serves the MCP SSE endpoint at `MCP_SSE_PATH` and the message endpoint at `MCP_MESSAGE_PATH`.
- `--transport streamable-http` serves the MCP HTTP endpoint at `STREAMABLE_HTTP_PATH`.
- For remote deployments, `streamable-http` is usually the better default; `sse` remains available for clients that still require it.

## Compatible Clients

- Cursor
- Claude Desktop
- Cline
- Trae
- Any MCP client that supports `stdio`, `sse`, or `streamable-http`

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
