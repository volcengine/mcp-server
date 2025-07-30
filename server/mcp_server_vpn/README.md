# VPN MCP

## Version  
v1.0.0  

## Product Description  
VPN  MCP  Server is a Model Context Protocol (MCP) server that allows MCP‑compatible clients (e.g., Cursor, Claude  Desktop) to interact with Volcengine’s VPN service.  
Using natural language, users can query and troubleshoot VPN Gateways, IPsec connections, Customer Gateways, SSL VPN servers, and related resources—streamlining cloud‑network operations.

## Category  
Networking

## Features  

- Retrieve VPN Gateway details  
- Retrieve IPsec Connection details / list  
- Retrieve VPN Gateway routes  
- Retrieve SSL  VPN certificates and server information  

## Tools  
The MCP  Server exposes the following Tools (capabilities):  
> **inputSchema** below lists common fields only; other optional filters follow the official OpenAPI.  
> All tools are **Instance‑type**; they can be invoked via natural‑language prompts or by sending JSON payloads.

| Tool | Description | Docs |
|------|-------------|------|
| `describe_vpn_gateway_attributes` | Get details of a specific VPN Gateway | <https://www.volcengine.com/docs/6455/108332> |
| `describe_vpn_gateways` | List VPN Gateways with filters | <https://www.volcengine.com/docs/6455/108331> |
| `describe_vpn_connection_attributes` | Get details of a specific IPsec Connection | <https://www.volcengine.com/docs/6455/108350> |
| `describe_vpn_connections` | List IPsec Connections with filters | <https://www.volcengine.com/docs/6455/108353> |
| `describe_vpn_gateway_route_attributes` | Get details of a VPN Gateway route entry | <https://www.volcengine.com/docs/6455/108357> |
| `describe_vpn_gateway_routes` | List VPN Gateway route entries | <https://www.volcengine.com/docs/6455/108358> |
| `describe_customer_gateways` | List Customer Gateways | <https://www.volcengine.com/docs/6455/108346> |
| `describe_ssl_vpn_client_cert_attributes` | Get details of a specific SSL client cert | <https://www.volcengine.com/docs/6455/1119965> |
| `describe_ssl_vpn_client_certs` | List SSL client certificates | <https://www.volcengine.com/docs/6455/1119966> |
| `describe_ssl_vpn_servers` | List SSL VPN servers | <https://www.volcengine.com/docs/6455/1119961> |

---

### Tool  1: describe_vpn_gateway_attributes  
#### Description
Fetch detailed information of a VPN Gateway (name, public  IP, bandwidth, billing, status, etc.).

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["vpn_gateway_id"],
    "properties": {
      "vpn_gateway_id": {
        "description": "VPN Gateway ID, e.g., vgw-xxxxxxxx",
        "type": "string"
      },
      "region": {
        "description": "Region (optional, defaults to VOLCENGINE_REGION)",
        "type": "string"
      }
    }
  },
  "name": "describe_vpn_gateway_attributes",
  "description": "Get VPN Gateway details"
}
````

#### Output
* JSON with full gateway attributes.

#### Prompt Example

```
Show details of VPN Gateway vgw-xxxxxxxx.
```

---

### Tool  2: describe\_vpn\_gateways

#### Description 
List VPN Gateways by Region, status, IDs, etc.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region":        { "type": "string",  "description": "Region (optional)" },
      "vpn_gateway_ids": { "type": "array", "items": { "type": "string" }, "description": "Gateway ID list (optional)" },
      "status":        { "type": "string",  "description": "Status, e.g., Available/Creating" }
    }
  },
  "name": "describe_vpn_gateways",
  "description": "List VPN Gateways"
}
```

####  Output
* List of matching VPN Gateways.

####  Prompt Example

```
List all Available VPN Gateways in cn‑beijing.
```

---

### Tool  3: describe\_vpn\_connection\_attributes

#### Description
Get details of an IPsec Connection (tunnel config, crypto, status, etc.).

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["vpn_connection_id"],
    "properties": {
      "vpn_connection_id": {
        "description": "IPsec Connection ID, e.g., vgc-xxxxxxxx",
        "type": "string"
      },
      "region": { "type": "string", "description": "Region (optional)" }
    }
  },
  "name": "describe_vpn_connection_attributes",
  "description": "Get IPsec Connection details"
}
```

#### Output
JSON with connection attributes.

#### Prompt Example

```
Show configuration of IPsec connection vgc-xxxxxxxx.
```

---

### Tool  4: describe_vpn_connections

#### Description
* List IPsec Connections by gateway, status, name.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region":         { "type": "string",  "description": "Region (optional)" },
      "vpn_gateway_id": { "type": "string",  "description": "VPN Gateway ID (optional)" },
      "status":         { "type": "string",  "description": "Status, e.g., Available" }
    }
  },
  "name": "describe_vpn_connections",
  "description": "List IPsec Connections"
}
```

#### Output
* List of matching IPsec Connections.

#### Prompt Example

```
List all Available IPsec connections under gateway vgw‑xxxxxxxx.
```

---

### Tool  5: describe\_vpn\_gateway\_route\_attributes

#### Description 
Get details of a VPN Gateway route entry.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["vpn_gateway_route_id"],
    "properties": {
      "vpn_gateway_route_id": {
        "description": "Route entry ID, e.g., vgr-xxxxxxxx",
        "type": "string"
      },
      "region": { "type": "string", "description": "Region (optional)" }
    }
  },
  "name": "describe_vpn_gateway_route_attributes",
  "description": "Get route entry details"
}
```

#### Output
* JSON with route details.

#### Prompt Example

```
Show route vgr‑xxxxxxxx details.
```

---

### Tool  6: describe\_vpn\_gateway\_routes

#### Description
* List VPN Gateway routes by CIDR, status, etc.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region":              { "type": "string",  "description": "Region (optional)" },
      "vpn_gateway_id":      { "type": "string",  "description": "Gateway ID (optional)" },
      "destination_cidr_block": { "type": "string", "description": "Destination CIDR (optional)" },
      "status":              { "type": "string",  "description": "Route status, e.g., Available" }
    }
  },
  "name": "describe_vpn_gateway_routes",
  "description": "List VPN Gateway routes"
}
```

#### Output 
* List of matching routes.

#### Prompt Example

```
List all routes to 10.0.0.0/16 under gateway vgw‑xxxxxxxx.
```

---

### Tool  7: describe\_customer\_gateways

#### Description
* List Customer Gateways (CGW) with filters.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string", "description": "Region (optional)" },
      "customer_gateway_ids": {
        "type": "array",
        "items": { "type": "string" },
        "description": "CGW ID list (optional)"
      },
      "status": { "type": "string", "description": "Status, e.g., Available" }
    }
  },
  "name": "describe_customer_gateways",
  "description": "List Customer Gateways"
}
```

#### Output
* List of Customer Gateways.

#### Prompt Example

```
Show all Available Customer Gateways.
```

---

### Tool  8: describe\_ssl\_vpn\_client\_cert\_attributes

#### Description
* Get details of an SSL client certificate.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["ssl_vpn_client_cert_id"],
    "properties": {
      "ssl_vpn_client_cert_id": {
        "description": "SSL client cert ID, e.g., vsc-xxxxxxxx",
        "type": "string"
      },
      "region": { "type": "string", "description": "Region (optional)" }
    }
  },
  "name": "describe_ssl_vpn_client_cert_attributes",
  "description": "Get SSL client cert details"
}
```

#### Output
* JSON with certificate details.

#### Prompt Example

```
Show details of SSL client certificate vsc‑xxxxxxxx.
```

---

### Tool  9: describe\_ssl\_vpn\_client\_certs

#### Description
* List SSL client certificates by server, status.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string", "description": "Region (optional)" },
      "ssl_vpn_server_id": { "type": "string", "description": "SSL VPN server ID (optional)" },
      "ssl_vpn_client_cert_ids": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Cert ID list (optional)"
      }
    }
  },
  "name": "describe_ssl_vpn_client_certs",
  "description": "List SSL client certs"
}
```

#### Output
* List of SSL client certs.

#### Prompt Example

```
List all SSL certs under server vsc-xxxxxxxx.
```

---

### Tool  10: describe\_ssl\_vpn\_servers

#### Description
* List SSL VPN servers by gateway, IDs.

#### Input

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string", "description": "Region (optional)" },
      "vpn_gateway_id": { "type": "string", "description": "Gateway ID (optional)" },
      "ssl_vpn_server_ids": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Server ID list (optional)"
      }
    }
  },
  "name": "describe_ssl_vpn_servers",
  "description": "List SSL VPN servers"
}
```

#### Output
* List of SSL VPN servers.

#### Prompt Example

```
List all SSL VPN servers under gateway vgw‑xxxxxxxx.
```

---

## Supported Platforms

Python, Cursor, Claude  Desktop, and any MCP‑compatible client

## Service Console

[https://console.volcengine.com/vpn/](https://console.volcengine.com/vpn/)

## Authentication

Volcengine AccessKey / SecretKey with HMAC signature.

1. Obtain credentials in the Volcengine console → Access Keys.
2. Set environment variables before running the server.

### Environment Variables

| Variable                | Description      | Required | Default                  |
| ----------------------- | ---------------- | -------- | ------------------------ |
| `VOLCENGINE_ENDPOINT`   | OpenAPI endpoint | No       | `open.volcengineapi.com` |
| `VOLCENGINE_REGION`     | Resource region  | Yes      | —                        |
| `VOLCENGINE_ACCESS_KEY` | AccessKey ID     | Yes      | —                        |
| `VOLCENGINE_SECRET_KEY` | Secret AccessKey | Yes      | —                        |

## Installation & Deployment

### Prerequisites

* Python 3.11+
* UV package manager

Install UV:

* **Linux/macOS**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
* **Windows**

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Sync dependencies & build

```bash
uv sync   # generate / update uv.lock
uv build  # optional, compile deps
```

### Running with uv (recommended)

```bash
export VOLCENGINE_ACCESS_KEY=<your_ak>
export VOLCENGINE_SECRET_KEY=<your_sk>
export VOLCENGINE_REGION=cn-beijing
export VOLCENGINE_ENDPOINT=open.volcengineapi.com
export PORT=8000
uv run mcp-server-vpn    # default stdio transport
```

### Client settings example

```json
{
  "mcpServers": {
    "mcp-server-vpn": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vpn",
        "mcp-server-vpn"
      ],
      "env": {
        "VOLCENGINE_ENDPOINT": "open.volcengineapi.com",
        "VOLCENGINE_REGION": "cn-beijing",
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

## License

volcengine/mcp-server is released under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).

