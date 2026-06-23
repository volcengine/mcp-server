# OpenViking Control Plane — MCP Server + CLI

MCP server **and** CLI for the OpenViking control plane (topapi) — manage OV
libraries (`Collection`). Both front-ends share one core (`client.py`), so a tool
added once is available from MCP and the CLI alike.

Covers the 6 core control-plane Actions:

| Action | MCP tool | CLI command |
|---|---|---|
| `ListOpenVikingCollections` | `list_collections` | `ov-cp list` |
| `CreateOpenVikingCollection` | `create_collection` ⚠️ | `ov-cp create` |
| `GetOpenVikingCollection` | `get_collection` | `ov-cp get <rid>` |
| `DeleteOpenVikingCollection` | `delete_collection` ⚠️ | `ov-cp delete <rid>` |
| `GetOpenVikingUsage` | `get_usage` | `ov-cp usage <rid>` |
| `GetOpenVikingCollectionUserAccess` | `get_collection_api_key` | `ov-cp api-key <rid>` |

## Endpoint

The control-plane TopAPI is compiled into the OpenViking **data-plane cluster**;
each Action is served by the data-plane gateway at:

```text
{endpoint}/api/openviking/{Action}
# default endpoint: https://api.vikingdb.cn-beijing.volces.com/openviking
# full URL e.g.: https://api.vikingdb.cn-beijing.volces.com/openviking/api/openviking/ListOpenVikingCollections
```

The Action lives in the **path** (no `?Action=&Version=` query). The request body
is the Action's params (e.g. `{"ResourceID": "..."}`).

> The default endpoint points at the **reserved** public data-plane gateway (not
> open to traffic yet). For local testing set `--endpoint` / `VIKING_ENDPOINT` to a
> `kubectl port-forward`, e.g. `http://localhost:18080`.

## Authentication

The only method: an **Ark AgentPlan ApiKey**, sent as an `Authorization: Bearer
<key>` header on every request (the backend's `authorizeControlPlaneByArk` reads
the key only from this header — it does **not** accept `X-API-Key`). Auth is
pluggable (`common/auth.py` → `BearerTokenAuth`); an AK/SK signer can be swapped in
later without touching the rest.

> ⚠️ Write actions like `create` require the account to have **AgentPlan deduction
> activated**, otherwise they return `ProductUnordered`. Read-only actions
> (list/get/usage/delete) are not gated.

### Configuration

| Setting | Env var | CLI flag | Default |
|---|---|---|---|
| Control-plane endpoint (base URL) | `VIKING_ENDPOINT` | `--endpoint` / `-e` | `https://api.vikingdb.cn-beijing.volces.com/openviking` |
| AgentPlan ApiKey | `AGENTPLAN_API_KEY` | `--api-key` / `-k` | — (required) |
| Default project | `OPENVIKING_PROJECT` | `--project` | `default` |

## CLI usage

```bash
uv sync                      # or: pip install -e .

# set the key once via env, then drop the per-command flag
export AGENTPLAN_API_KEY=ark-xxxxxxxx

# read-only
uv run ov-cp list
uv run ov-cp get   <ResourceID>
uv run ov-cp usage <ResourceID>
uv run ov-cp api-key <ResourceID>

# create (consumes paid quota; with source=agentplan only --name is needed —
#         model names default, and the model ApiKey falls back to the configured key)
uv run ov-cp create --name my_kb

# delete (irreversible)
uv run ov-cp delete <ResourceID> --yes
```

Flags override env. The endpoint defaults to the public gateway; override it only
for testing (e.g. against a port-forward) with `-e` / `VIKING_ENDPOINT` —
`uv run ov-cp -e http://localhost:18080 list`.
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
        "AGENTPLAN_API_KEY": "ark-xxxxxxxx"
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
      "env": {
        "AGENTPLAN_API_KEY": "ark-xxxxxxxx"
      }
    }
  }
}
```

Run with SSE instead via `mcp-server-openviking-controlplane --transport sse`.

## Agent skill

A Claude Code / agent skill that documents the `ov-cp` workflow lives at
[`skills/openviking-controlplane/SKILL.md`](skills/openviking-controlplane/SKILL.md).
Symlink or copy it into your agent's skills directory (e.g. `~/.claude/skills/`) to
let an agent drive the control plane.

> ⚠️ `create_collection` / `delete_collection` create/destroy **billable** resources and
> are exposed as MCP tools; their descriptions instruct the model to confirm with you
> first. Rely on your client's tool-permission prompt as the final gate.
