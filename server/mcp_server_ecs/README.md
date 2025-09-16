# ECS MCP Server 


## Version
v0.2.0

## Overview

ECS MCP Server is a Model Context Protocol server that provides MCP clients (such as Claude Desktop) with the ability to interact with the Volcengine ECS service. It enables full-chain management of cloud instance resources based on natural language, supporting query operations for instances, images, regions, availability zones, available resources, and system events, thereby achieving efficient management of ECS resources.

## Category
ECS

## Features

- Query instance information
- Query event information 
- Query region information
- Simple instance operations

## Available Tools
Since some interfaces have a lot of input parameters and return content, some uncommon content will cause too much context burden on llm. In order to avoid unnecessary token waste, ECS MCP Server only provides queries for common content.

- `describe_instances`: [query instance list](https://www.volcengine.com/docs/6396/70466)
- `describe_images`: [query image list](https://www.volcengine.com/docs/6396/70808)
- `describe_instance_types`: [query instance type list](https://www.volcengine.com/docs/6396/92769)
- `describe_available_resource`: [query available resources](https://www.volcengine.com/docs/6396/76279)
- `describe_system_events`: [query system events](https://www.volcengine.com/docs/6396/129399)
- `describe_regions`: [query region list](https://www.volcengine.com/docs/6396/1053194)
- `describe_zones`: [query availability zone list](https://www.volcengine.com/docs/6396/120518)
- `start_instances`: [start instances](https://www.volcengine.com/docs/6396/101068)
- `renew_instance`: [renew instance](https://www.volcengine.com/docs/6396/76276)

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
cd mcp-server/server/mcp_server_ecs
uv run mcp-server-ecs

# Start with streamable-http mode (default is stdio)
uv run mcp-server-ecs -t streamable-http
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
| `VOLCENGINE_REGION` | Volcengine resource region | - 
| `VOLCENGINE_ENDPOINT` | Volcengine endpoint | - |
| `MCP_SERVER_PORT` | MCP server listening port | `8000` |

For example, set these environment variables before starting the server:

```bash
export VOLCENGINE_ACCESS_KEY={ak}
export VOLCENGINE_SECRET_KEY={sk}
export VOLCENGINE_REGION={region}
export VOLCENGINE_ENDPOINT={endpoint}
export MCP_SERVER_PORT=8000
```

### Run with uvx
```json
{
    "mcpServers": {
        "mcp-server-ecs": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_ecs",
            "mcp-server-ecs"
          ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "",
                "VOLCENGINE_SECRET_KEY": "",
                "VOLCENGINE_REGION": "",
                "VOLCENGINE_ENDPOINT": "",
                "MCP_SERVER_PORT": ""
            }
        }
    }
}
```

## Examples
### Cursor
![Image](https://lf3-beecdn.bytetos.com/obj/ies-fe-bee-upload/bee_prod/biz_950/tos_333f0ad0f93c311bae4259ce2ab9022c.jpg)
![Image](https://lf3-beecdn.bytetos.com/obj/ies-fe-bee-upload/bee_prod/biz_950/tos_49abb4af5fb42f55052558867daff3d6.jpg)


# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
