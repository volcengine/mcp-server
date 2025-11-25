# EMR MCP Server 

## Version
v0.1.0

## Overview

EMR MCP Server is a Model Context Protocol server that provides MCP clients (such as Claude Desktop) with the ability to interact with the Volcengine EMR service. 

## Category
EMR

## Features
- Query serverless jobs information
- Query emr on ecs clusters information
- Query emr on vke clusters information

## Available Tools
Since some interfaces have a lot of input parameters and return content, some uncommon content will cause too much context burden on llm. In order to avoid unnecessary token waste, EMR MCP Server only provides queries for common content.

- `list_serverless_jobs`: [query serverless jobs](https://www.volcengine.com/docs/6491/1263265)
- `list_emr_on_ecs_clusters`: [query emr on ecs clusters](https://www.volcengine.com/docs/6491/1208305)
- `list_emr_on_vke_clusters`: [query emr on vke clusters](https://www.volcengine.com/docs/6491/1230115)

## Usage Guide

### Prerequisites
- Python 3.12+
- UV

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation
Clone the repository:
```bash
git clone git@github.com:volcengine/mcp-server.git
```

### Usage
Start the server:

#### UV
```bash
cd mcp-server/server/mcp_server_emr
uv run mcp-server-emr

# Start with streamable-http mode (default is stdio)
uv run mcp-server-emr -t streamable-http
```

Use a client to interact with the server:
```
Trae | Cursor ｜ Claude Desktop | Cline | ...
```

## Configuration

### Environment Variables
The following environment variables are available for configuring the MCP server:

| Environment Variable | Description | Default Value |
|----------|------|--------|
| `VOLCENGINE_ACCESS_KEY` | Volcengine account ACCESSKEY | - |
| `VOLCENGINE_SECRET_KEY` | Volcengine account SECRETKEY | - |
| `VOLCENGINE_REGION` | Volcengine account REGION | - |
| `MCP_SERVER_HOST` | MCP server listening host | `0.0.0.0` |
| `MCP_SERVER_PORT` | MCP server listening port | `8000` |
| `STREAMABLE_HTTP_PATH` | Streamable HTTP path | `/mcp` |
| `STATLESS_HTTP` | Whether to enable stateless HTTP | `true` |


For example, set these environment variables before starting the server:

```bash
export VOLCENGINE_ACCESS_KEY={ak}
export VOLCENGINE_SECRET_KEY={sk}
export VOLCENGINE_REGION={region}
export MCP_SERVER_HOST=0.0.0.0
export MCP_SERVER_PORT=8000
export STREAMABLE_HTTP_PATH=/mcp
export STATLESS_HTTP=true
```

### Run with uvx

```json
{
  "mcpServers": {
    "mcp-server-emr": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_emr",
        "mcp-server-emr"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key-id",
        "VOLCENGINE_SECRET_KEY": "your-access-key-secret",
        "VOLCENGINE_REGION": "cn-beijing",
        "MCP_SERVER_HOST": "0.0.0.0",
        "MCP_SERVER_PORT": "8000",
        "STREAMABLE_HTTP_PATH": "/mcp",
        "STATLESS_HTTP": "true"
      }
    }
  }
}
```

# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
