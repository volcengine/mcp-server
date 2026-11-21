# HQD Multi-Source Search MCP Server

## Version Information

v0.1

## Product Description

### Short Description

Query enterprise data from HQD (High-Quality Dataset) multi-source search service, covering basic info, risk, operations, IP, and litigation data.

### Long Description

HQD Multi-Source Search MCP Server is a thin proxy that connects to the remote HQD MCP service deployed on Volcengine. It provides unified access to 5 enterprise data sources through a two-phase interaction pattern: metadata discovery (`describe_datasource`) followed by data retrieval (`query_datasource`). All queries are forwarded to the remote endpoint — no local data processing is performed.

## Category

Data Intelligence

## Tags

Enterprise Data, Multi-Source Search, HQD

## Tools

This MCP Server product provides the following Tools (capabilities):

### Tool 1: describe_datasource

Get metadata for data sources including dimensions, metrics, and filters. Agents should call this first to understand available data structures before querying.

### Tool 2: query_datasource

Query data from a specific datasource with filtering, aggregation, and pagination. Supports filter operators: `eq`, `like`, `in`, `not_in`, `between`, `range`, `keyword`.

## Compatible Platforms

- Python

## Authentication Method

Bearer Token

### Obtaining Auth Token

Contact the HQD service administrator to obtain an authentication token.

### Environment Variable Configuration

| Variable Name | Value |
| ---------- | ---------- |
| `HQD_AUTH_TOKEN` | Auth token for the remote HQD MCP endpoint |
| `HQD_MCP_ENDPOINT` | Remote HQD MCP endpoint (optional, has default) |

## Python MCP Server

### Dependencies

The device running MCP server needs to install the following dependencies:

- [Python](https://www.python.org/downloads/) 3.10 or higher.
- [`uv`](https://docs.astral.sh/uv/) & [`uvx`](https://docs.astral.sh/uv/guides/tools/).

### Deployment and Configuration

```json
{
  "mcpServers": {
    "mcp-server-hqd": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_hqd",
        "mcp-server-hqd"
      ],
      "env": {
        "HQD_AUTH_TOKEN": "Your HQD Auth Token"
      }
    }
  }
}
```

> Note: Please replace `Your HQD Auth Token` above with the authentication token provided by the HQD service administrator.

## Using Clients

The following clients are supported for interacting with MCP Server. For specific configurations, please refer to the client documentation:

- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- Ark

Supports [Cline](https://cline.bot/) plugin

## Available Datasources

| ID | Name |
|----|------|
| `enterprise_basic_wide` | Enterprise Basic Information |
| `enterprise_risk_wide` | Enterprise Risk Information |
| `enterprise_operation_wide` | Enterprise Operations Information |
| `enterprise_ip_wide` | Enterprise Intellectual Property |
| `enterprise_litigation` | Enterprise Litigation Information |

## Conversation Initiation Example

- List all available data sources.
- Query the basic information of the enterprise named "ByteDance".
- Search for enterprises with registered capital over 10 million in Beijing.

## License

[MIT](../../LICENSE)
