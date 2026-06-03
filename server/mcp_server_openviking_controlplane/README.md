# OpenViking Control Plane — MCP Server + CLI

MCP server **and** CLI for the OpenViking control plane (topapi · `top` cluster) —
manage OV libraries (`Collection`). Both front-ends share one core (`client.py`), so
a tool added once is available from MCP and the CLI alike.

Covers the 6 core control-plane Actions:

| Action | MCP tool | CLI command |
|---|---|---|
| `ListOpenVikingCollections` | `list_collections` | `ov-cp list` |
| `CreateOpenVikingCollection` | `create_collection` ⚠️ | `ov-cp create` |
| `GetOpenVikingCollection` | `get_collection` | `ov-cp get <rid>` |
| `DeleteOpenVikingCollection` | `delete_collection` ⚠️ | `ov-cp delete <rid>` |
| `GetOpenVikingUsage` | `get_usage` | `ov-cp usage <rid>` |
| `GetOpenVikingCollectionUserAccess` | `get_collection_api_key` | `ov-cp api-key <rid>` |

## Authentication (development phase)

Signing is **not** implemented yet. During development you supply the request headers
yourself (copy them from the browser DevTools — "Copy request headers"). The tool
replays them on every request. Auth is pluggable (`common/auth.py` → `ManualHeadersAuth`);
a dedicated API key / AK-SK signer can be swapped in later without touching the rest.

### Configuration

| Setting | Env var | CLI flag | Default |
|---|---|---|---|
| Gateway host | `VIKING_HOST` | `--host` | (or `Host` header) |
| Scheme | `VIKING_SCHEMA` | `--schema` | `https` |
| Default project | `OPENVIKING_PROJECT` | `--project` | `default` |
| Auth headers (file) | `VIKING_HEADERS_FILE` | `--headers-file` / `-H` | — |
| Auth headers (inline) | `VIKING_HEADERS` | `--header 'K: V'` (repeatable) | — |

The headers file may be a JSON object **or** a raw `Key: Value` block (HTTP/2
pseudo-headers like `:authority` are skipped). If `Host` is among the headers, you may
omit `VIKING_HOST`.

## CLI usage

```bash
uv sync                      # or: pip install -e .

# read-only
uv run ov-cp --headers-file headers.txt --host vikingdb-stg.cn-beijing.volcengineapi.com list
uv run ov-cp -H headers.txt get   <ResourceID>
uv run ov-cp -H headers.txt usage <ResourceID>
uv run ov-cp -H headers.txt api-key <ResourceID>

# create (consumes paid quota; max 20 libraries/account)
uv run ov-cp -H headers.txt create \
  --name my_kb --source volcengine \
  --vlm-model doubao-vision-... --vlm-api-key-id <id> \
  --emb-model doubao-embedding-... --emb-api-key-id <id>

# delete (irreversible)
uv run ov-cp -H headers.txt delete <ResourceID> --yes
```

`ov-cp --help` works without any config.

## MCP usage (stdio / uvx)

The server defaults to **stdio** transport, so it can be launched as a subprocess by
any MCP client. Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "openviking-controlplane": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_openviking_controlplane",
        "mcp-server-openviking-controlplane"
      ],
      "env": {
        "VIKING_HOST": "vikingdb-stg.cn-beijing.volcengineapi.com",
        "VIKING_HEADERS_FILE": "/absolute/path/to/headers.txt"
      }
    }
  }
}
```

For local development point it at your checkout instead:

```json
{
  "mcpServers": {
    "openviking-controlplane": {
      "command": "uv",
      "args": ["run", "--directory", "/abs/path/server/mcp_server_openviking_controlplane",
               "mcp-server-openviking-controlplane"],
      "env": { "VIKING_HOST": "...", "VIKING_HEADERS_FILE": "/abs/path/headers.txt" }
    }
  }
}
```

Run with SSE instead via `mcp-server-openviking-controlplane --transport sse`.

> ⚠️ `create_collection` / `delete_collection` create/destroy **billable** resources and
> are exposed as MCP tools; their descriptions instruct the model to confirm with you
> first. Rely on your client's tool-permission prompt as the final gate.
