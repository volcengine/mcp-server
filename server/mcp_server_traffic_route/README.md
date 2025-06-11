# TrafficRoute MCP Server

## Version Information

v0.1

## Product Description

###  Short Description

Support for configuring DNS routing rules to ensure that requests from clients reach the desired service nodes.

### Long Description

The DNS routing service that allows users to configure DNS routing rules to ensure that requests from clients reach the desired service nodes.

## Category

Enterprise Applications

## Tags

DNS，Domain

## Tools

This MCP Server product provides the following Tools (capabilities):

### Tool 1: list_zones

List DNS on TrafficRoute.

### Tool 2: create_zone

Add a domain configuration.

### Tool 3: list_records

Get all records of the specific DNS.

## Compatible Platforms

Python

## Authentication Method

AK&amp;SK

### Get AK&amp;SK

Obtain AccessKey and SecretKey from [Access control in Volcengine Console](https://console.volcengine.com/iam/identitymanage/user).

Note: AccessKey and SecretKey must have permissions for the OpenAPIs (available tools).

### Environment Variable Configuration

| Variable Name | Value |
| ---------- | ---------- |
| `VOLCENGINE_ACCESS_KEY` | Volcengine AccessKey |
| `VOLCENGINE_SECRET_KEY` | Volcengine SecretKey |

## Python - MCP Server

### Dependencies

Require following dependencies to run MCP server.

- Python 3.11 or higher.
- [`uv`](https://docs.astral.sh/uv/) and [`uvx`](https://docs.astral.sh/uv/guides/tools/) packages for running the server.
- For Windows OS user, please refer to [PyCryptodome documentation](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#windows-from-sources) to configure the compilation environment of this library, otherwise the MCP service will not start normally.

### Deployment and configuration

```json
{
  "mcpServers": {
    "mcp-server-traffic-route": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_traffic_route/python",
        "mcp-server-traffic-route"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

## Node.js - MCP Server

### Dependencies

Require following dependencies to run MCP server.

- Node.js 22.14.1 or higher

### Deployment and configuration

```json
{
  "mcpServers": {
    "mcp-server-traffic-route": {
      "command": "node",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_traffic_route/nodejs",
        "mcp-server-traffic-route"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

### Using a client

Use a client to interact with the server.

- Cline
- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- 方舟

## License

[MIT](../../LICENSE)
