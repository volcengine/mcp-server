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

- Python
- Node.js

## Service Activation Link

You need to activate the TrafficRoute DNS suite in your Volcengine account.

https://console.volcengine.com/TrafficRoute/

## Authentication Method

AK&amp;SK

### Get AK&amp;SK

Obtain Access Key ID and Secret Access Key from [Access control in Volcengine Console](https://console.volcengine.com/iam/identitymanage/user).

Note: The Access Key ID and Secret Access Key must have permissions for the OpenAPIs (available tools).

### Environment Variable Configuration

| Variable Name | Value |
| ---------- | ---------- |
| `VOLCENGINE_ACCESS_KEY` | Your Volcengine Access Key ID |
| `VOLCENGINE_SECRET_KEY` | Your Volcengine Secret Access Key |

## Python - MCP Server

### Dependencies

- [Python](https://www.python.org/downloads/) 3.11 or higher.
- [`uv`](https://docs.astral.sh/uv/) and [`uvx`](https://docs.astral.sh/uv/guides/tools/) packages for running the server.
- For Windows NT OS user, please refer to [PyCryptodome documentation](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#windows-from-sources) to configure the compilation environment of this library, otherwise the MCP server will not start normally.

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

> P.S. Please replace `Your Volcengine AK` and `Your Volcengine SK` above with your own Access Key ID and Secret Access Key.

## Node.js - MCP Server

### Dependencies

- [Node.js](https://nodejs.org/en/download) 22.14.1 or higher

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

> P.S. Please replace `Your Volcengine AK` and `Your Volcengine SK` above with your own Access Key ID and Secret Access Key.

### Using a client

Use a client to interact with the server.

- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- 方舟

Also support [Cline](https://cline.bot/).

## License

[MIT](../../LICENSE)
