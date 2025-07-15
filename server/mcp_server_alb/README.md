# Application Load Balancer MCP Server

## Version Information

v0.1

## Product Description

### Short Description

Retrieve information about Application Load Balancer instances, including associated listeners, backend server groups, certificates, and other related information.

### Long Description

Volcengine ALB supports multiple application layer protocols such as HTTP, HTTPS, HTTP/2, WebSocket, WebSocket Secure, and QUIC to meet the needs of different scenarios. Volcengine ALB can monitor the health status of backend servers and provide certificate management functionality.

## Category

CDN and Edge

## Tags

Application Load Balancer

## Tools

This MCP Server product provides the following Tools (capabilities):

### Tool 1: describe_acl_attributes

Retrieve detailed information about a specified access control policy group.

### Tool 2: describe_ca_certificates

Retrieve CA certificate list.

### Tool 3: describe_acls

Retrieve access control policy group list.

### Tool 4: describe_certificates

Retrieve server certificate list.

### Tool 5: describe_customized_cfgs

Retrieve personalized configuration list.

### Tool 6: describe_all_certificates

Retrieve all certificate list.

### Tool 7: describe_listener_attributes

Retrieve detailed information about a specified listener.

### Tool 8: describe_listeners

Retrieve listener list.

### Tool 9: describe_load_balancer_attributes

Retrieve detailed information about an Application Load Balancer instance.

### Tool 10: describe_customized_cfg_attributes

Retrieve detailed information about a specified personalized configuration.

### Tool 11: describe_health_check_templates

Retrieve health check template list.

### Tool 12: describe_listener_health

Retrieve health check information of backend servers associated with a specified listener.

### Tool 13: describe_load_balancers

Retrieve Application Load Balancer instance list.

### Tool 14: describe_server_group_attributes

Retrieve detailed information about a server group.

### Tool 15: describe_rules

Retrieve forwarding rule list for a specified listener.

### Tool 16: describe_zones

Retrieve availability zone list supported by ALB deployment.

### Tool 17: describe_server_groups

Retrieve server group list.

### Tool 18: describe_server_group_backend_servers

Retrieve backend server information of a server group.

## Compatible Platforms

- Python

## Service Activation Link

You need to activate the Application Load Balancer service for your Volcengine account first.

https://console.volcengine.com/alb

## Authentication Method

AK&SK

### Obtaining AK&SK

Get Access Key ID and Secret Access Key from the [Volcengine Console](https://console.volcengine.com/iam/identitymanage/user).

Note: This Access Key ID and Secret Access Key must have access permissions for relevant OpenAPIs.

### Environment Variable Configuration

| Variable Name | Value |
| ---------- | ---------- |
| `VOLCENGINE_ACCESS_KEY` | Volcengine account Access Key ID |
| `VOLCENGINE_SECRET_KEY` | Volcengine account Secret Access Key |

## Python MCP Server

### Dependencies

The device running MCP server needs to install the following dependencies:

- [Python](https://www.python.org/downloads/) 3.11 or higher.
- [`uv`](https://docs.astral.sh/uv/) & [`uvx`](https://docs.astral.sh/uv/guides/tools/).
- For Windows operating system, you also need to configure the library compilation environment by referring to the [PyCryptodome documentation](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#windows-from-sources).

### Deployment and Configuration

```json
{
  "mcpServers": {
    "mcp-server-alb": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_alb/python",
        "mcp-server-alb"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

> Note: Please replace `Your Volcengine AK` and `Your Volcengine SK` above with the Access Key ID and Secret Access Key corresponding to your Volcengine account respectively.

## Using Clients

The following clients are supported for interacting with MCP Server. For specific configurations, please refer to the client documentation:

- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- Ark

Supports [Cline](https://cline.bot/) plugin

## Conversation Initiation Example

- List all ALB instances.
- Get the ALB instance information and associated listener information with the private IP address 192.168.1.16.

## License

[MIT](../../LICENSE)
