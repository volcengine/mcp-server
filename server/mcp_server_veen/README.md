# VEEN MCP Server

> Volcengine Edge Computing Node MCP Server

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

### Tool 1: get_cloud_server

Get details of the cloud server by the specific ID.

### Tool 2: start_instances

Start the edge computing node instance by the specific ID.

### Tool 3: get_instance

Get details of the edge computing node instance by the specific ID.

### Tool 4: list_instances

List the edge computing node instances.

### Tool 5: get_image

Get details of the container image by the specific ID.

### Tool 6: list_instance_internal_ips

List all internal IP addresses of the specific edge computing node.

### Tool 7: list_instance_types

List all the available spec types of the specific edge computing node.

### Tool 8: create_cloud_server

Create edge computing node.

### Tool 9: set_instance_name

Set the display name of the specific edge computing node instance.

### Tool 10: enable_instances_i_pv6

Enable IP v6 for the specific edge computing node instance.

### Tool 11: list_instance_internal_ips

List all internal IP addresses of the specific edge computing node instance.

### Tool 12: list_cloud_servers

List all edge computing node.

### Tool 13: list_instance_types

List all instance types of the specific edge computing node.

### Tool 14: list_available_resource_info

List all available resource info of the specific instance type.

### Tool 15: create_instance

Create edge computing node instance.

### Tool 16: list_images

List all images of the specific instance type.

### Tool 17: get_image

Get image details.

### Tool 18: get_veen_instance_usage

Get the usage of the specific instance type.

### Tool 19: list_vpc_instances

List all virtual private cloud instances.

## Compatible Platforms

- Python
- Node.js

## Service Activation Link

You need to activate the VEEN service in your Volcengine account.

https://console.volcengine.com/edge/veen

## Authentication Method

AK&amp;SK

### Get AK&amp;SK

Obtain Access Key ID and Secret Access Key from [Access control in Volcengine Console](https://console.volcengine.com/iam/identitymanage/user).

Note: the Access Key ID and Secret Access Key must have permissions for the OpenAPIs (available tools).

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

![Configuration sample in Cline](./assets/cline_mcp_add.jpg)

```json
{
  "mcpServers": {
    "mcp-server-veen": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_veen/python",
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

> P.S. Please replace `Your Volcengine AK` and `Your Volcengine SK` above with your own Access Key ID and Secret Access Key.

## Node.js - MCP Server

### Dependencies

- [Node.js](https://nodejs.org/en/download) 22.14.1 or higher

### Deployment and configuration

```json
{
  "mcpServers": {
    "mcp-server-veen": {
      "command": "node",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_veen/nodejs",
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

> P.S. Please replace `Your Volcengine AK` and `Your Volcengine SK` above with your own Access Key ID and Secret Access Key.

### Using a client

Use a client to interact with the server.

- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- 方舟

Also support [Cline](https://cline.bot/).

## Usage Examples

- List all stopped edge instances.

## License

[MIT](../../LICENSE)
