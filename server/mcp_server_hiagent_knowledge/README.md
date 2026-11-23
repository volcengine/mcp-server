# HiAgent Knowledge MCP Server

This MCP server exposes a **knowledge base (knowledge engine)** as MCP tools. Each tool is named after the user-facing **capability** it provides rather than a raw OpenAPI action. It provides knowledge base discovery and the full knowledge-engine tool set (semantic search, regex grep, document metadata/chunks, and Wiki search/read).

## Features

- List knowledge bases (datasets) in a workspace, and inspect a single dataset
- Search knowledge across datasets by relevance (`search_knowledge`)
- Match chunks by RE2 regex (`grep_knowledge_chunks`)
- Read documents' metadata in batch (`list_document_infos`) and a document's chunks in order (`list_document_chunks`)
- Search generated Wiki pages (`search_wiki`), read a page (`read_wiki_page`), and trace its sources — by page slug (`read_wiki_source_chunk`) or by a referenced source document's resource id (`read_wiki_source_doc`)
- Report MCP server and OpenAPI configuration state

### Capability-based tool naming

The HiAgent OpenAPI exposes the knowledge engine through a single action (`CallKnowledgeTool` in `v3.3.0`, the default for standalone AK/SK callers; `CallKnowledgeEngineTool` in `v3.1.0` / `v3.2.1`) whose `ToolName` field selects a sub-tool and whose request carries a same-named PascalCase parameter object. This server maps each `(ToolName, parameter object)` combination to its own capability-named MCP tool with a flat argument schema:

| MCP tool | OpenAPI action (`v3.3.0` / `v3.1.0`–`v3.2.1`) | `ToolName` | Parameter object | Capability |
|---|---|---|---|---|
| `search_knowledge` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `knowledge_search` | `KnowledgeSearch` | Relevance search across datasets |
| `grep_knowledge_chunks` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `grep_chunks` | `GrepChunks` | RE2 regex match over candidate chunks |
| `list_document_infos` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `list_doc_infos` | `ListDocInfos` | Documents' metadata, batched by dataset |
| `list_document_chunks` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `list_knowledge_chunks` | `ListKnowledgeChunks` | Sequential read of one document's chunks |
| `search_wiki` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `wiki_search` | `WikiSearch` | Search generated Wiki pages |
| `read_wiki_page` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `wiki_read_page` | `WikiReadPage` | Read a Wiki page by slug |
| `read_wiki_source_chunk` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `wiki_read_source_chunk` | `WikiReadSourceChunk` | Read a Wiki page's referenced source chunks, by page slug |
| `read_wiki_source_doc` | `CallKnowledgeTool` / `CallKnowledgeEngineTool` | `wiki_read_source_doc` (`v3.3.0`) / `list_knowledge_chunks` (`v3.1.0`–`v3.2.1`) | `WikiReadSourceDoc` (`v3.3.0`) / `ListKnowledgeChunks` (`v3.1.0`–`v3.2.1`) | Read one referenced source document's chunks in order, by resource id |

> Note: in HiAgent a *dataset* is a *knowledge base*, so `list_datasets` / `get_dataset` are the "list/inspect knowledge base" capabilities.

> Validation model: this server is a thin adapter. It only checks that the fields it must always send are present (dataset ids, a pattern/slug/queries where the capability requires one, plus `workspace_id` on `v3.1.0`/`v3.2.1`) and relies on argument types from the tool schema. Value ranges, enums and cross-field rules (e.g. `limit`/`overlap` bounds, `grep_type` scope rules) are owned by the backend service and are version-specific, so its `InvalidParameter.*` errors are passed through to the caller rather than duplicated here. On `v3.3.0` (`CallKnowledgeTool`), `workspace_id` is optional (omit/blank to authorize across the caller's visible datasets), and optional `user_info` (`{"UserID": ..., "UserChannel": "IAM"}`) may only name the TOP-authenticated IAM user itself (other users or channels such as `"Lark"` are rejected with 403). On `v3.1.0` / `v3.2.1` (`CallKnowledgeEngineTool`), `workspace_id` is required and `user_info` supports IAM or mappable Lark channels (other channels are treated as guest).

## Setup

### Prerequisites

- Python 3.11 or higher
- API credentials (AK/SK)

### Installation

Run directly from the repository with uvx (recommended):

```bash
uvx --from "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_hiagent_knowledge" mcp-server-hiagent-knowledge
```

Or with uv, from the compatibility path:

```bash
cd mcp-server/server/mcp_server_hiagent_knowledge
uv run mcp-server-hiagent-knowledge
```

### Configuration

The server requires the following environment variables:

- `HIAGENT_TOP_HOST`: HiAgent Platform API (volc-top) gateway address, including scheme and port
- `HIAGENT_ACCESS_KEY_ID`: Your HiAgent access key id
- `HIAGENT_SECRET_ACCESS_KEY`: Your HiAgent secret access key

Optional environment variables:

- `HIAGENT_VERSION`: HiAgent OpenAPI compatibility version to use. Defaults to the latest registered version (currently `v3.3.0`). Can also be set per-run with the `--hiagent-version` CLI flag, which takes precedence. Selects the version-specific contract under `versions/`; supported values: `v3.1.0`, `v3.2.1`, `v3.3.0`
- `HIAGENT_TOOLS`: Tool allowlist, a comma-separated list of exact tool names selecting the base tool set to expose; unset means all tools. Can also be set per-run with the `--tools` / `-t` CLI flag, which takes precedence
- `HIAGENT_DISABLED_TOOLS`: Tool denylist, comma-separated; subtracted from the allowlist (or from all tools when no allowlist is given). Can also be set per-run with the `--disabled-tools` CLI flag, which takes precedence
- `HIAGENT_ACCOUNT_ID`: Main account id sent as the `X-Account-Id` query parameter, defaults to `1000000000`
- `HIAGENT_REGION`: Region used in AK/SK V4 signing (not a network address), defaults to `cn-north-1`
- `FASTMCP_CHECK_FOR_UPDATES`: Set to `off` to skip FastMCP's startup update check, which otherwise makes an outbound request and can fail startup in restricted networks
- `MCP_SERVER_HOST`: Bind host for the FastMCP server, streamable-http only (default: `127.0.0.1`)
- `MCP_SERVER_PORT`: Bind port for the FastMCP server, streamable-http only (default: `8000`)
- `STREAMABLE_HTTP_PATH`: Streamable HTTP endpoint path (default: `/mcp`)

## Usage

### Running the Server

The server can be run with either stdio transport (for MCP integration, e.g. the HiAgent STDIO plugin) or streamable-http transport:

```bash
python -m mcp_server_hiagent_knowledge.main --transport stdio
```

Or:

```bash
python -m mcp_server_hiagent_knowledge.main --transport streamable-http
```

Select a specific HiAgent OpenAPI version explicitly with `--hiagent-version`
(overrides the `HIAGENT_VERSION` environment variable; defaults to the latest
registered version):

```bash
python -m mcp_server_hiagent_knowledge.main --hiagent-version v3.1.0
```

### Filtering the Exposed Tools

All tools are exposed by default. Two optional flags narrow the exposed tool set;
both take a comma-separated list of **exact tool names** (an unknown name exits
with an error), and `health_check` is always kept:

| Flag | Short | Environment variable | Description |
|---|---|---|---|
| `--tools` | `-t` | `HIAGENT_TOOLS` | Allowlist: selects the base tool set; unset means all tools |
| `--disabled-tools` | - | `HIAGENT_DISABLED_TOOLS` | Denylist: subtracted from the allowlist (or from all tools when no allowlist is given) |

Resolution order: `--tools` picks the base set (unset = all), then
`--disabled-tools` is subtracted from it. For each flag the precedence is
**CLI flag > environment variable > unset**; an empty or whitespace-only
environment value (e.g. `HIAGENT_TOOLS=`) is treated as unset (= all tools) and
does not narrow the set to just `health_check`. For example, to make the agent
reliably search the Wiki when a dataset mixes plain documents and generated Wiki
pages, expose only the Wiki tools:

```bash
python -m mcp_server_hiagent_knowledge.main \
  -t search_wiki,read_wiki_page,read_wiki_source_chunk,read_wiki_source_doc
```

### Available Tools

#### health_check

Report the MCP server and OpenAPI configuration state.

```python
health_check()
```

#### list_datasets

Discover the knowledge bases the calling identity can access, including own
datasets and visible shared ones, via `list_datasets` (unified discovery since
HiAgent v3.3.0). Standalone AK/SK callers dispatch it through
`CallKnowledgeTool`, which authorizes per the calling identity's own
knowledge-base ACL; the request body and wire version are unchanged.

```python
list_datasets(
    workspace_id="workspace_id",   # optional: omit to auto-discover
    user_id="iam_user_id",
    keyword="finance",
    limit=20,
)
```

- `workspace_id` (optional): scope discovery to one workspace (its own plus
  visible shared datasets). Omit it — or pass a blank value — to merge every
  HiAgent workspace the identity has joined plus its legacy personal space; each
  `DatasetID` appears once.
- `user_id` (optional): IAM user ID; the channel is fixed to IAM. When omitted,
  the backend resolves the IAM identity associated with the credentials.
- `keyword` (optional): name/description keyword, sent as `ListDatasets.Filter.Keyword`.
- `limit` (optional): page size, 1..100; the backend defaults to 100 when omitted.
- `cursor` (optional): previous `NextCursor`. Keep the same user, workspace, keyword
  and limit across pages; cursors are not interchangeable with other tools or
  parameter sets.
- `ids` (optional): dataset IDs; `[]` returns no items. Mutually exclusive with
  explicit `limit`/`cursor`.

The full OpenAPI response is preserved. `Result.ListDatasets` contains `Items`
(`DatasetID`, `Name`, `Description`, `WorkspaceID`, `Icon`, `IndexingTechnique`,
`IndexTypes`) and an optional `NextCursor`, with no `Total`. For a shared dataset,
`WorkspaceID` is the source workspace. The backend enforces permissions and
argument constraints; shared visibility never replaces the retrieval-time
permission check.

Migration: this server selects one contract per run; it does not detect the backend
version or retry with another contract, so set `HIAGENT_VERSION` (or
`--hiagent-version`) to the version your deployment serves. With `v3.1.0` or
`v3.2.1`, `list_datasets` keeps the original `ListDatasets` action: `workspace_id`
is required, paging uses `name`, `page_number` (default 1) and `page_size`
(default 20), and the response includes `Total`. The MCP tool name is `list_datasets`
in every version, so refresh the client's tool schema when the selected version
changes and configure tool allow/deny lists with the names that version exposes.

#### get_dataset

On `v3.3.0`, returns one visible dataset's summary (`DatasetID`, `Name`,
`Description`, `WorkspaceID`, `Icon`, `IndexingTechnique`, `IndexTypes`) via
`list_datasets` with an explicit `ids` filter (does not return default retrieval
parameters). On `v3.1.0` / `v3.2.1`, calls `GetDataset` with a required
`workspace_id` and returns full dataset details including default retrieval
parameters.

```python
get_dataset(
    dataset_id="dataset_id",
    workspace_id="workspace_id",   # optional on v3.3.0; required on v3.1.0/v3.2.1
)
```

Parameters:
- `dataset_id` (required): the id of the dataset to inspect.
- `workspace_id` (optional on `v3.3.0`; required on `v3.1.0`/`v3.2.1`): consuming workspace id to scope lookup to; omit/blank on `v3.3.0` to look up across the caller's joined and legacy personal spaces.

#### search_knowledge

Search knowledge across one or more datasets and return the chunks most relevant to your queries.

```python
search_knowledge(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    queries=["How to reset my password?"],
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): list of dataset ids to search, at least one.
- `queries` (required): list of natural-language query strings, at least one.

#### grep_knowledge_chunks

Match knowledge chunks by one RE2 regular expression. Use for exact tokens (error codes, identifiers, fixed phrases) when semantic search is insufficient. Narrows candidates first, then applies the pattern — not an exhaustive full-dataset scan.

```python
grep_knowledge_chunks(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    pattern="ERR\\d+",
    queries=["error code"],
    limit=10,
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): dataset ids to search, at least one.
- `pattern` (required): one RE2 regular expression (no backreferences/lookarounds).
- `queries` (optional): queries to narrow the candidate set.
- `limit` (optional): maximum number of matches.
- `grep_type` (optional): scan scope, `dataset_ids` (default) or `resource_ids`.
- `resource_ids` (optional): document/resource ids to restrict the scan to; required when `grep_type` is `resource_ids`.

#### list_document_infos

Get metadata for one or more documents, batched by dataset (title, type, size, status, segment count, timestamps). Metadata only — not document content.

```python
list_document_infos(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    resource_ids={"dataset_id": ["resource_id_1", "resource_id_2"]},
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): dataset ids involved, at least one.
- `resource_ids` (required): map of dataset id → list of document/resource ids to describe; keys must be within `dataset_ids`.

#### list_document_chunks

List the knowledge chunks of a single document/resource in reading order. Unlike `search_knowledge` (relevance-ranked for a query), this walks one resource sequentially — useful for browsing a document's full content.

```python
list_document_chunks(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    resource_id="resource_id",
    limit=50,
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): list of dataset ids the resource belongs to, at least one.
- `resource_id` (required): the document/resource whose chunks to list.
- `limit` (optional): maximum number of chunks per page.
- `cursor_segment_id` (optional): segment id to continue paging from (pass the last returned segment id).

#### search_wiki

Search generated Wiki pages for concepts and topic pages. Returns page candidates (with `Slug`) for navigation, not final evidence.

```python
search_wiki(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    queries=["reverse acquisition"],
    limit=5,
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): dataset ids to search, at least one.
- `queries` (required): natural-language query strings, at least one.
- `limit` (optional): maximum number of pages.

#### read_wiki_page

Read one generated Wiki page by slug (structure, summary, content). Wiki pages are generated navigation material, not final evidence.

```python
read_wiki_page(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    slug="concept/reverse-acquisition",
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): dataset ids the page belongs to, at least one.
- `slug` (required): the Wiki page slug (from `search_wiki`).

#### read_wiki_source_chunk

Read a Wiki page's referenced source chunks, resolved by the page slug — the final evidence for facts, numbers, quotations and code. To instead read one referenced source document's chunks in order by its resource id, use `read_wiki_source_doc`.

```python
read_wiki_source_chunk(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    slug="concept/reverse-acquisition",
    limit=5,
    overlap=2,
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): dataset ids the page belongs to, at least one.
- `slug` (required): the Wiki page slug whose sources to read.
- `limit` (optional): maximum number of source chunks per page.
- `overlap` (optional): number of adjacent segments to expand around each referenced chunk for more context (0 disables expansion).
- `cursor_segment_id` (optional): segment id to continue paging from.

#### read_wiki_source_doc

Read one referenced source document's chunks in reading order, by resource id. Companion to `read_wiki_source_chunk`: that resolves a page's referenced chunks by slug; this walks a single referenced source document (`resource_id`, e.g. from a Wiki page's `SourceRefs`) sequentially.

```python
read_wiki_source_doc(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    resource_id="resource_id",
    limit=50,
)
```

Parameters:
- `workspace_id` (required): the workspace id the datasets belong to.
- `dataset_ids` (required): dataset ids the resource belongs to, at least one.
- `resource_id` (required): the referenced source document/resource whose chunks to read.
- `limit` (optional): maximum number of chunks per page.
- `cursor_segment_id` (optional): segment id to continue paging from.

## MCP Integration

To add this server to your MCP configuration, add the following to your MCP settings file:

```json
{
  "mcpServers": {
    "hiagent-knowledge": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_hiagent_knowledge",
          "mcp-server-hiagent-knowledge"
        ],
      "env": {
        "HIAGENT_TOP_HOST": "http://your-top-host:30040",
        "HIAGENT_ACCESS_KEY_ID": "your-access-key",
        "HIAGENT_SECRET_ACCESS_KEY": "your-secret-key",
        "HIAGENT_ACCOUNT_ID": "1000000000",
        "HIAGENT_REGION": "cn-north-1",
        "FASTMCP_CHECK_FOR_UPDATES": "off"
      }
    }
  }
}
```

This uses the STDIO transport (the default), which the HiAgent MCP plugin launches locally and injects credentials into via its environment-variable table.

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your AK/SK credentials are correct
   - Check that you have the necessary permissions for the workspace and datasets

2. **Startup Failure in Restricted Networks**
   - Set `FASTMCP_CHECK_FOR_UPDATES=off` to skip FastMCP's outbound update check

3. **Empty or Denied Results**
   - Verify the `workspace_id` and `dataset_ids` are correct
   - Confirm `HIAGENT_TOP_HOST` points to the HiAgent Platform API (volc-top) gateway, not the web or Agent API address

### Logging

The server uses Python's logging module with INFO level by default. You can see detailed logs in the console when running the server.

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
