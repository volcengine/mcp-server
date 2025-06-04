# VEEN Edge MCP Server


## Version Information

v0.1

## Product Description

### Short Description

Apply, configure, and query for edge computing nodes, including virtual machines, images, bare metal, and corresponding network configurations.

### Long Description

Based on edge nodes covering all provinces and operators in China, the Volcengine Edge Computing Node product provides users with compute, network, and storage resources at their nearest location. It helps users quickly deploy business applications to the edge layer. The edge computing node product provides different levels of computing services to meet the diverse needs of users in different scenarios. It includes edge computing nodes, edge containers, edge hosting, and edge functions.

## Category

CDN与边缘

## Tags

Edge Computing, Virtual Machine, Image, Storage

## Tools

This MCP Server product provides the following Tools (capabilities):

### Tool 1: start_cloud_server

Start the cloud server by the specific ID.

### Tool 2: get_cloud_server

Get details of the cloud server by the specific ID.

### Tool 3: start_instances

Start the edge computing node instance by the specific ID.

### Tool 4: get_instance

Get details of the edge computing node instance by the specific ID.

### Tool 5: list_instances

List the edge computing node instances.

### Tool 6: get_image

Get details of the container image by the specific ID.

### Tool 7: list_instance_internal_ips

List all internal IP addresses of the specific edge computing node.

### Tool 8: list_instance_types

List all the available spec types of the specific edge computing node.

## Compatible Platforms

Python

## Service Activation Link

https://console.volcengine.com/edge/veen

## Authentication Method

AK&amp;SK

## Installation

### Using uv

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed.
We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run.

```bash
cd mcp-server/server/mcp_server_veen
uv run mcp-server-veen

# Start with sse mode (default is stdio)
uv run mcp-server-veen -t sse
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
    "mcp-server-veen": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_veen",
        "mcp-server-veen"
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
