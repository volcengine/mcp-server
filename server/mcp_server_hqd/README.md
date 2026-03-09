# HQD Multi-Source Search MCP Server

MCP server for HQD (High-Quality Dataset) multi-source enterprise data search. This server acts as a proxy to the remote HQD MCP service, providing unified access to enterprise data sources.

## Features

- Proxy to remote HQD MCP service — no local data processing
- 2 MCP tools: `describe_datasource` (metadata discovery) + `query_datasource` (data retrieval)
- 5 enterprise data sources: basic info, risk, operations, IP, litigation
- YAML-driven datasource metadata, filter/aggregation/pagination support

## Setup

### Prerequisites

- Python >= 3.10

### Installation

```bash
pip install -e .
```

### Configuration

```bash
cp .env_example .env
# Edit .env if you need to change the remote endpoint
```

| Variable | Default | Description |
|----------|---------|-------------|
| `HQD_MCP_ENDPOINT` | `https://sd6k08f59gqcea6qe13vg.apigateway-cn-beijing.volceapi.com/mcp` | Remote HQD MCP endpoint |
| `HQD_AUTH_TOKEN` | (empty) | Auth token sent as `Authorization: Bearer <token>` to the remote endpoint |
| `PORT` | `8000` | Local server port |

## Usage

### Running

```bash
# STDIO mode (for Claude Desktop / Cursor / Trae)
mcp-server-hqd --transport stdio

# SSE mode
mcp-server-hqd --transport sse
```

### MCP Integration

```json
{
  "mcpServers": {
    "hqd": {
      "command": "mcp-server-hqd",
      "args": ["--transport", "stdio"]
    }
  }
}
```

### Available Tools

#### `describe_datasource`

Get metadata for data sources including dimensions, metrics, and filters.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `datasource_id` | string | `"all"` | Datasource ID, or `"all"` for summary list |
| `locale` | string | `"zh-CN"` | Response language |

#### `query_datasource`

Query data from a specific datasource with filtering, aggregation, and pagination.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `datasource_id` | string | required | Target datasource ID |
| `filters` | string | `null` | Filter string: `field:op:value;...` |
| `select_fields` | string | `null` | Fields to return, comma-separated |
| `aggregation` | string | `null` | Aggregation: `field:func,...` |
| `group_by` | string | `null` | Group-by fields, comma-separated |
| `sort_field` | string | `null` | Sort field |
| `sort_order` | string | `"desc"` | Sort direction (`asc`/`desc`) |
| `page` | int | `1` | Page number |
| `page_size` | int | `10` | Page size (max 50) |

### Available Datasources

| ID | Name |
|----|------|
| `enterprise_basic_wide` | 企业基本信息宽表 |
| `enterprise_risk_wide` | 企业风险信息宽表 |
| `enterprise_operation_wide` | 企业经营信息宽表 |
| `enterprise_ip_wide` | 企业知识产权宽表 |
| `enterprise_litigation` | 企业诉讼信息 |
