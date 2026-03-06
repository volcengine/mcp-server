# MCP Server: Supabase
> Manage AIDAP Supabase projects, Postgres schema, Edge Functions, and Storage directly from any MCP client.

English | [简体中文](./README_zh.md)

| Item | Details |
| ---- | ------- |
| Version | v0.1.0 |
| Description | An MCP server for AIDAP Supabase that exposes project, database, Edge Functions, and Storage operations to AI assistants. |
| Category | Database |
| Tags | Supabase, PostgreSQL, AIDAP, Edge Functions, Storage |
| Docs | [Volcengine AIDAP Supabase](https://www.volcengine.com/docs/87275/2105900) |

## Core Capabilities

### 1. Project and Branch Management
- `list_projects`
  List all available AIDAP Supabase projects.
- `get_project`
  Get details for a specific project. You can pass either a workspace ID or a branch ID.
- `create_project`
  Create a new Supabase project in AIDAP.
- `pause_project`
  Pause a project.
- `restore_project`
  Resume a paused project.
- `get_project_url`
  Get the project API endpoint resolved from the current workspace or branch.
- `get_publishable_keys`
  Get publishable and service role keys for a project.
- `list_branches`
  List development branches under a project.
- `create_branch`
  Create a new development branch.
- `delete_branch`
  Delete a development branch.
- `reset_branch`
  Reset a branch to the latest state supported by AIDAP.

### 2. Database Development
- `execute_sql`
  Execute raw SQL against the target Postgres database.
- `list_tables`
  List tables from one or more schemas.
- `list_migrations`
  List migration history stored in `supabase_migrations.schema_migrations`.
- `list_extensions`
  List installed PostgreSQL extensions.
- `apply_migration`
  Execute SQL and record the migration metadata.
- `generate_typescript_types`
  Generate TypeScript definitions from database schemas.

### 3. Edge Functions
- `list_edge_functions`
  List all deployed Edge Functions.
- `get_edge_function`
  Get function source code and metadata.
- `deploy_edge_function`
  Deploy or update a function with Node.js or Python runtime.
- `delete_edge_function`
  Delete a function by name.

### 4. Storage
- `list_storage_buckets`
  List storage buckets in the target project.
- `create_storage_bucket`
  Create a storage bucket with optional public access, size limit, and MIME type restrictions.
- `delete_storage_bucket`
  Delete a storage bucket.
- `get_storage_config`
  Fetch storage service configuration from the workspace endpoint.
- `update_storage_config`
  Update storage configuration when the current AIDAP endpoint supports it.

## Compatibility Notes

- The official Supabase MCP server is built around the Supabase Management API. AIDAP does not provide the same Management API, so this server maps compatible operations onto AIDAP workspace APIs and Supabase workspace endpoints.
- In AIDAP, `workspace` is the equivalent of a Supabase `project`. Tool parameters keep the name `project_id` for MCP compatibility.
- For most project-scoped tools, `project_id` accepts either a workspace ID or a branch ID. If a branch ID such as `br-xxx` is passed, the server resolves the parent workspace automatically.
- When `project_id` is omitted, the server uses `DEFAULT_PROJECT_ID` or `DEFAULT_WORKSPACE_ID` if configured.
- `reset_branch` accepts `migration_version` for compatibility, but the current AIDAP API ignores that field.
- `update_storage_config` may return `supported: false` if the current AIDAP workspace endpoint does not expose that capability.

## Integration Guide

### 1. Requirements
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

### 2. Credentials
Get `VOLCENGINE_ACCESS_KEY` and `VOLCENGINE_SECRET_KEY` from the [Volcengine Access Key Console](https://console.volcengine.com/iam/keymanage/).

### 3. Environment Variables

| Variable | Required | Description |
| -------- | -------- | ----------- |
| `VOLCENGINE_ACCESS_KEY` | Yes | Volcengine access key ID |
| `VOLCENGINE_SECRET_KEY` | Yes | Volcengine secret access key |
| `VOLCENGINE_REGION` | No | Region code, default `cn-beijing` |
| `DEFAULT_PROJECT_ID` | No | Default project ID used when `project_id` is omitted |
| `DEFAULT_WORKSPACE_ID` | No | Same purpose as `DEFAULT_PROJECT_ID` |
| `READ_ONLY` | No | Set to `true` to block write operations |
| `SUPABASE_ENDPOINT_SCHEME` | No | Endpoint scheme for workspace API URLs, default `http` |
| `SUPABASE_PROJECT_SLUG` | No | Edge Functions project slug, default `default` |

## Quick Deployment

### Method 1: Run with `uvx`

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_supabase",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk",
        "VOLCENGINE_REGION": "cn-beijing"
      }
    }
  }
}
```

### Method 2: Run from local source with `uv`

```bash
cd /absolute/path/to/mcp-server/server/mcp_server_supabase
uv sync
```

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server/server/mcp_server_supabase",
        "run",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk",
        "VOLCENGINE_REGION": "cn-beijing",
        "DEFAULT_PROJECT_ID": "ws-xxxxxxxx"
      }
    }
  }
}
```

### Method 3: Run with `python3`

```json
{
  "mcpServers": {
    "supabase": {
      "command": "python3",
      "args": [
        "-m",
        "mcp_server_supabase.server"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk",
        "VOLCENGINE_REGION": "cn-beijing"
      }
    }
  }
}
```

## Prompt Examples

- `List all my Supabase projects`
- `Show all branches for project ws-xxxx`
- `Execute SQL: select * from public.users limit 10`
- `Generate TypeScript types for schemas public,auth`
- `Deploy an Edge Function named webhook-handler`
- `List all storage buckets in project ws-xxxx`

## Notes

- Most MCP desktop clients use `stdio`, so the JSON examples above are the recommended setup.
- Write tools are disabled when `READ_ONLY=true`.
- The server uses the default branch automatically when the target endpoint or key needs a branch and none is provided explicitly.

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
