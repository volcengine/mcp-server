# Supabase MCP Server

English | [简体中文](README_zh.md)

> MCP server for Volcengine Supabase workspaces. It exposes workspace, branch, database, Edge Functions, storage, and TypeScript type generation capabilities through MCP.

| Item | Details |
| ---- | ---- |
| Version | v0.1.0 |
| Description | MCP server built on top of Volcengine Supabase workspaces |
| Category | Database / Developer Tools |
| Tags | Supabase, PostgreSQL, Edge Functions, Storage, Volcengine |

## Tools

### `account`

| Tool | Description |
| ---- | ---- |
| `list_workspaces` | List all available Supabase workspaces in the current account |
| `get_workspace` | Get workspace details |
| `create_workspace` | Create a new Supabase workspace |
| `pause_workspace` | Pause a workspace |
| `restore_workspace` | Resume a paused workspace |
### `docs`

No tools are currently exposed.

### `database`

| Tool | Description |
| ---- | ---- |
| `execute_sql` | Execute raw SQL against the Postgres database |
| `list_tables` | List tables in one or more schemas |
| `list_migrations` | List records from `supabase_migrations.schema_migrations` |
| `list_extensions` | List installed PostgreSQL extensions |
| `apply_migration` | Run migration SQL and record it in `supabase_migrations.schema_migrations` |

### `debugging`

No tools are currently exposed.

### `development`

| Tool | Description |
| ---- | ---- |
| `get_workspace_url` | Get the API endpoint for a workspace |
| `get_publishable_keys` | Get publishable, anon, and service role keys |
| `generate_typescript_types` | Generate TypeScript definitions from schema metadata |

### `functions`

| Tool | Description |
| ---- | ---- |
| `list_edge_functions` | List Edge Functions in a workspace |
| `get_edge_function` | Get the source code and configuration of an Edge Function |
| `deploy_edge_function` | Create or update an Edge Function |
| `delete_edge_function` | Delete an Edge Function |

### `branching`

| Tool | Description |
| ---- | ---- |
| `list_branches` | List branches under a workspace |
| `create_branch` | Create a development branch |
| `delete_branch` | Delete a development branch |
| `restore_branch` | Restore branch data to a specified point in time and return the restored branch ID |

### `storage`

| Tool | Description |
| ---- | ---- |
| `list_storage_buckets` | List storage buckets |
| `create_storage_bucket` | Create a new storage bucket |
| `delete_storage_bucket` | Delete a storage bucket |
| `get_storage_config` | Get storage configuration |

## Authentication

- Local deployment: use `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY`, and optional `VOLCENGINE_SESSION_TOKEN`

Static AK/SK can be obtained from the [Volcengine API Access Key console](https://console.volcengine.com/iam/keymanage/).

## Environment Variables

| Name | Required | Default | Description |
| ---- | ---- | ---- | ---- |
| `VOLCENGINE_ACCESS_KEY` | Yes | - | Volcengine access key for local static authentication |
| `VOLCENGINE_SECRET_KEY` | Yes | - | Volcengine secret key for local static authentication |
| `VOLCENGINE_SESSION_TOKEN` | No | - | Optional session token used with temporary local credentials |
| `VOLCENGINE_REGION` | No | `cn-beijing` | Region used for the Volcengine API |
| `WORKSPACE_REF` | No | - | Startup-level hard scope. When set, `account` tools are hidden and workspace-scoped calls are forced to this target |
| `FEATURES` | No | `account,database,debugging,development,docs,functions,branching` | Official feature groups. `storage` is disabled by default |
| `DISABLED_TOOLS` | No | - | Comma-separated denylist applied after all other policy filters |
| `READ_ONLY` | No | `false` | Startup-level read-only switch; when enabled, mutating tools are hidden |
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

### Build a Docker image for local testing

```bash
docker build -t volcengine/mcp-server-supabase:latest server/mcp_server_supabase
```

### Build and publish a multi-platform image

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t <your-registry>/mcp-server-supabase:latest \
  --push \
  server/mcp_server_supabase
```

Use the multi-platform build when sharing the image with other companies or teams on different host architectures.

### Run in Docker

```bash
docker run --rm -p 8000:8000 \
  -e VOLCENGINE_ACCESS_KEY=<your-access-key> \
  -e VOLCENGINE_SECRET_KEY=<your-secret-key> \
  -e VOLCENGINE_REGION=cn-beijing \
  -e WORKSPACE_REF=ws-xxxxxxxx \
  -e FEATURES=database,functions \
  volcengine/mcp-server-supabase:latest
```

The container defaults to `streamable-http` on `0.0.0.0:8000` and serves MCP at `http://<host>:8000/mcp`. Override the transport by appending arguments such as `--transport sse`.

### AI tool integration with local source

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
        "WORKSPACE_REF": "ws-xxxxxxxx",
        "FEATURES": "database,functions"
      }
    }
  }
}
```

### AI tool integration with `uvx`

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
        "WORKSPACE_REF": "ws-xxxxxxxx",
        "FEATURES": "database,functions"
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

The package exposes `mcp-server-supabase`, `mcp-server-supabase-sse`, and `mcp-server-supabase-streamable`. The examples above use `mcp-server-supabase`.

## Usage Notes

- `WORKSPACE_REF` applies a hard workspace scope for the server instance and removes `workspace_id` from visible tool schemas.
- When `WORKSPACE_REF` is active, `account` tools are hidden and any explicit `workspace_id` outside the scope is rejected.
- `FEATURES` accepts only the official groups: `account`, `docs`, `database`, `debugging`, `development`, `functions`, `storage`, and `branching`.
- If `FEATURES` is not set, the default enabled groups are `account`, `database`, `debugging`, `development`, `docs`, `functions`, and `branching`. `storage` stays disabled by default.
- `READ_ONLY=true` hides all mutating tools for the server instance.
- `DISABLED_TOOLS` takes tool names such as `execute_sql,deploy_edge_function` and removes them after the rest of the policy has been resolved.
- `workspace_id` and `workspace_ref` accept workspace IDs only. Branch IDs such as `br-xxxx` are rejected.
- `get_publishable_keys` resolves the default branch automatically when needed.
- `restore_branch` supports optional `time` and `source_branch_id` arguments and returns `backup_branch_id`.
- `deploy_edge_function` currently supports `native-node20/v1`, `native-python3.9/v1`, `native-python3.10/v1`, and `native-python3.12/v1`.
- `--transport sse` serves the MCP SSE endpoint at `MCP_SSE_PATH` and the message endpoint at `MCP_MESSAGE_PATH`.
- `--transport streamable-http` serves the MCP HTTP endpoint at `STREAMABLE_HTTP_PATH`.
- For remote deployments, `streamable-http` is usually the better default; `sse` remains available for clients that still require it.

## Policy Precedence

### Tool filtering order at startup

1. `features` selects the base tool set
2. `workspace_ref` removes `account` tools and scopes the server to one workspace
3. `read_only` removes all mutating tools
4. `disabled_tools` removes specific tool names last

## Integration Modes

### AI tools

This server works with Cursor, Claude Desktop, Cline, Trae, and any other MCP client that supports `stdio`, `sse`, or `streamable-http`.

- Local integrations usually use `stdio`
- Configure `command`, `args`, and `env` in the client
- Local source mode usually injects static AK/SK through `env`
- The two `mcpServers` JSON examples above follow this pattern

### Custom AI agents

If your agent runtime can spawn a local MCP process, you can keep using `stdio`. If your agent runs on a server, in containers, or in a multi-instance environment, `streamable-http` or `sse` is usually the better integration path.

- `stdio`: have the agent spawn `mcp-server-supabase` as a child process
- `streamable-http`: connect to `http://<host>:<port>/mcp`
- `sse`: connect to `http://<host>:<port>/sse` and post messages to `http://<host>:<port>/messages/`
- Tool visibility and workspace scope are fixed when the server starts through env vars or CLI flags

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
