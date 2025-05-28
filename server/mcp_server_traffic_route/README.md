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

## Installation

### Using uv

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed.
We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run.

```bash
cd mcp-server/server/mcp_server_traffic_route
uv run mcp-server-traffic-route

# Start with sse mode (default is stdio)
uv run mcp-server-traffic-route -t sse
```

### Using a client

Use a client to interact with the server:

- 方舟
- Trae
- Cursor

## Deployment

### Integration in MCP Client

```json
{
  "mcpServers": {
    "mcp-server-traffic-route": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_traffic_route",
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

## License

MIT
