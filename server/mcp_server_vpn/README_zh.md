# VPN连接 MCP  

## 版本信息  
v1.0.0  

## 产品描述  
VPN MCP Server 是一个 Model Context Protocol 服务器，为 MCP 客户端（如 Cursor、Claude Desktop 等）提供与火山引擎 VPN 服务交互的能力。
通过自然语言即可对 VPN 网关、IPsec 连接、SSL VPN 等资源进行全链路管理，支持VPN网关、IPsec 连接、用户网关、SSL服务端等资源的查询操作，帮助用户高效管理云上网络连接。  

## 分类  
网络  

## 功能

- 查询 VPN 网关详情  
- 查询 IPsec 连接详情 / 列表  
- 查询 VPN 网关路由  
- 查询 SSL VPN 证书与服务端信息 

## Tools  
本 MCP Server 产品提供以下 Tools (工具 / 能力)：
> 下列 **inputSchema** 仅列出常用字段，其他可选过滤条件保持与官方 OpenAPI 一致。所有工具均为 **实例** 类型，调用方式一致：向 MCP 客户端发出自然语言指令或直接构造 JSON 请求。

| 工具                                        | 说明                 | 文档                                                                                           |
| ----------------------------------------- |--------------------| -------------------------------------------------------------------------------------------- |
| `describe_vpn_gateway_attributes`         | 查询指定 VPN 网关详情      | [https://www.volcengine.com/docs/6455/108332](https://www.volcengine.com/docs/6455/108332)   |
| `describe_vpn_gateways`                   | 按条件查询 VPN 网关列表     | [https://www.volcengine.com/docs/6455/108331](https://www.volcengine.com/docs/6455/108331)   |
| `describe_vpn_connection_attributes`      | 查询指定 IPsec 连接详情    | [https://www.volcengine.com/docs/6455/108350](https://www.volcengine.com/docs/6455/108350)   |
| `describe_vpn_connections`                | 按条件查询 IPsec 连接列表   | [https://www.volcengine.com/docs/6455/108353](https://www.volcengine.com/docs/6455/108353)   |
| `describe_vpn_gateway_route_attributes`   | 查询指定 VPN 网关路由条目    | [https://www.volcengine.com/docs/6455/108357](https://www.volcengine.com/docs/6455/108357)   |
| `describe_vpn_gateway_routes`             | 按条件查询 VPN 网关路由条目列表 | [https://www.volcengine.com/docs/6455/108358](https://www.volcengine.com/docs/6455/108358)   |
| `describe_customer_gateways`              | 查询用户网关列表           | [https://www.volcengine.com/docs/6455/108346](https://www.volcengine.com/docs/6455/108346)   |
| `describe_ssl_vpn_client_cert_attributes` | 查询指定 SSL 客户端证书详情   | [https://www.volcengine.com/docs/6455/1119965](https://www.volcengine.com/docs/6455/1119965) |
| `describe_ssl_vpn_client_certs`           | 查询 SSL 客户端证书列表     | [https://www.volcengine.com/docs/6455/1119966](https://www.volcengine.com/docs/6455/1119966) |
| `describe_ssl_vpn_servers`                | 查询 SSL 服务端列表       | [https://www.volcengine.com/docs/6455/1119961](https://www.volcengine.com/docs/6455/1119961) |


### Tool 1: describe_vpn_gateway_attributes
#### 详细描述
查询指定 VPN 网关的详细信息（名称、公网 IP、带宽、计费类型、状态等）。


#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["vpn_gateway_id"],
    "properties": {
      "vpn_gateway_id": {
        "description": "VPN 网关 ID，例如 vgw-xxxxxxxx",
        "type": "string"
      },
      "region": {
        "description": "资源所在 Region（可选，缺省时使用 VOLCENGINE_REGION）",
        "type": "string"
      }
    }
  },
  "name": "describe_vpn_gateway_attributes",
  "description": "查询指定 VPN 网关详情"
}
```
#### 输出
* 返回 VPN 网关的详细属性.

#### Prompt 示例
```text
查询 VPN 网关 vgw-xxxxxxxx 的详细信息。
```


### Tool 2: describe_vpn_gateways

#### 详细描述

按条件查询 VPN 网关列表，支持 Region、状态、ID 过滤。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region":        { "type": "string",  "description": "资源所在 Region（可选）" },
      "vpn_gateway_ids": { "type": "array", "items": { "type": "string" }, "description": "VPN 网关 ID 列表（可选）" },
      "status":        { "type": "string",  "description": "网关状态，例如 Available/Creating" }
    }
  },
  "name": "describe_vpn_gateways",
  "description": "查询 VPN 网关列表"
}
```

#### 输出

* 返回符合条件的 VPN 网关列表。

#### Prompt 示例

```
列出 cn-beijing 地域状态为 Available 的全部 VPN 网关。
```


### Tool 3: describe_vpn_connection_attributes

#### 详细描述

查询指定 IPsec 连接的详细信息（隧道配置、加密算法、状态等）。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["vpn_connection_id"],
    "properties": {
      "vpn_connection_id": {
        "description": "IPsec 连接 ID，例如 vgc-xxxxxxxx",
        "type": "string"
      },
      "region": { "type": "string", "description": "资源所在 Region（可选）" }
    }
  },
  "name": "describe_vpn_connection_attributes",
  "description": "查询指定 IPsec 连接详情"
}
```

#### 输出

* 返回 IPsec 连接的详细属性（JSON）。

#### Prompt 示例

```
查看 IPsec 连接 vgc-xxxxxxxx 的详细配置。
```


### Tool 4: describe_vpn_connections

#### 详细描述

按条件查询 IPsec 连接列表，支持网关、状态、名称过滤。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region":         { "type": "string",  "description": "资源所在 Region（可选）" },
      "vpn_gateway_id": { "type": "string",  "description": "所属 VPN 网关 ID（可选）" },
      "status":         { "type": "string",  "description": "连接状态，如 Available" }
    }
  },
  "name": "describe_vpn_connections",
  "description": "查询 IPsec 连接列表"
}
```

#### 输出

* 返回符合条件的 IPsec 连接列表。

#### Prompt 示例

```
列出网关 vgw-xxxxxxxx 下所有 Available 状态的 IPsec 连接。
```


### Tool 5: describe_vpn_gateway_route_attributes

#### 详细描述

查询指定 VPN 网关路由条目详情（目的网段、下一跳、优先级等）。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["vpn_gateway_route_id"],
    "properties": {
      "vpn_gateway_route_id": {
        "description": "VPN 网关路由条目 ID，例如 vgr-xxxxxxxx",
        "type": "string"
      },
      "region": { "type": "string", "description": "资源所在 Region（可选）" }
    }
  },
  "name": "describe_vpn_gateway_route_attributes",
  "description": "查询指定 VPN 网关路由条目详情"
}
```

#### 输出

* 返回路由条目的详细信息（JSON）。

#### Prompt 示例

```
查询路由条目 vgr-xxxxxxxx 的详细信息。
```


### Tool 6: describe_vpn_gateway_routes

#### 详细描述

按条件查询 VPN 网关路由条目列表，支持目的网段、状态过滤。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region":        { "type": "string",  "description": "资源所在 Region（可选）" },
      "vpn_gateway_id":{ "type": "string",  "description": "所属 VPN 网关 ID（可选）" },
      "destination_cidr_block": { "type": "string", "description": "目的网段 CIDR（可选）" },
      "status":        { "type": "string",  "description": "路由状态，如 Available" },
    }
  },
  "name": "describe_vpn_gateway_routes",
  "description": "查询 VPN 网关路由条目列表"
}
```

#### 输出

* 返回符合条件的路由条目列表。

#### Prompt 示例

```
列出网关 vgw-xxxxxxxx 中目的网段为 10.0.0.0/16 的全部路由条目。
```


### Tool 7: describe_customer_gateways

#### 详细描述

查询用户网关（CGW）列表，支持 ID、状态过滤。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string",  "description": "资源所在 Region（可选）" },
      "customer_gateway_ids": {
        "type": "array",
        "items": { "type": "string" },
        "description": "用户网关 ID 列表（可选）"
      },
      "status": { "type": "string",  "description": "状态，例如 Available" }
    }
  },
  "name": "describe_customer_gateways",
  "description": "查询用户网关列表"
}
```

#### 输出

* 返回用户网关列表。

#### Prompt 示例

```
列出所有 Available 状态的用户网关。
```


### Tool 8: describe_ssl_vpn_client_cert_attributes

#### 详细描述

查询指定 SSL VPN 客户端证书详情（状态、过期时间、绑定服务器等）。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["ssl_vpn_client_cert_id"],
    "properties": {
      "ssl_vpn_client_cert_id": {
        "description": "SSL 客户端证书 ID，例如 vsc-xxxxxxxx",
        "type": "string"
      },
      "region": { "type": "string", "description": "资源所在 Region（可选）" }
    }
  },
  "name": "describe_ssl_vpn_client_cert_attributes",
  "description": "查询指定 SSL 客户端证书详情"
}
```

#### 输出

* 返回 SSL 客户端证书详细信息（JSON）。

#### Prompt 示例

```
查看 SSL 客户端证书 vsc-xxxxxxxx 的详情。
```


### Tool 9: describe_ssl_vpn_client_certs

#### 详细描述

按条件查询 SSL VPN 客户端证书列表，可按服务器、状态过滤。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string", "description": "资源所在 Region（可选）" },
      "ssl_vpn_server_id": { "type": "string", "description": "所属 SSL VPN 服务器 ID（可选）" },
      "ssl_vpn_client_cert_ids": {
        "type": "array",
        "items": { "type": "string" },
        "description": "证书 ID 列表（可选）"
      }
    }
  },
  "name": "describe_ssl_vpn_client_certs",
  "description": "查询 SSL 客户端证书列表"
}
```

#### 输出

* 返回 SSL 客户端证书列表。

#### Prompt 示例

```
列出SSL服务端 vsc-xxxxxxxx 下的所有 SSL 客户端证书。
```


### Tool 10: describe_ssl_vpn_servers

#### 详细描述

查询 SSL VPN 服务器列表，支持网关、ID 过滤。

#### 输入

```json
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "region": { "type": "string", "description": "资源所在 Region（可选）" },
      "vpn_gateway_id": { "type": "string", "description": "所属 VPN 网关 ID（可选）" },
      "ssl_vpn_server_ids": {
        "type": "array",
        "items": { "type": "string" },
        "description": "服务器 ID 列表（可选）"
      }
    }
  },
  "name": "describe_ssl_vpn_servers",
  "description": "查询 SSL VPN 服务器列表"
}
```

#### 输出

* 返回 SSL VPN 服务器列表。

#### Prompt 示例

```
列出网关 vgw-xxxxxxxx 下的全部 SSL VPN 服务器。
```


## 可适配平台

Python、Cursor、Claude Desktop、任意支持 MCP 协议的客户端

## 服务开通链接 (整体产品)

[https://console.volcengine.com/vpn/](https://console.volcengine.com/vpn/)

## 鉴权方式

使用火山引擎 AccessKey / SecretKey 进行 HMAC 签名。

1. 登录火山引擎控制台 → 访问密钥 → 创建 AccessKey / SecretKey。
2. 启动 MCP Server 前，通过环境变量注入凭证。

### 环境变量

| 环境变量                    | 描述                    | 必填 | 默认值                      |
| ----------------------- | --------------------- |----|--------------------------|
| `VOLCENGINE_ENDPOINT`   | 火山引擎 OpenAPI Endpoint | 否  | `open.volcengineapi.com` |
| `VOLCENGINE_REGION`     | 火山引擎 Region           | 是  | -                        |
| `VOLCENGINE_ACCESS_KEY` | AccessKey ID          | 是  | -                        |
| `VOLCENGINE_SECRET_KEY` | Secret AccessKey      | 是  | -                        |

## 安装部署

### 系统依赖

* Python 3.11 或更高版本
* UV 包管理器

安装 UV：

* **Linux/macOS**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
* **Windows**

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 同步依赖并构建

```bash
uv sync   # 生成 / 更新 uv.lock
uv build  # 可选，编译依赖
```

### Using uv（推荐）

无需额外安装，直接使用 `uvx` 运行 *mcp-server-vpn*。

#### 本地运行示例

```bash
export VOLCENGINE_ACCESS_KEY=<your_ak>
export VOLCENGINE_SECRET_KEY=<your_sk>
export VOLCENGINE_REGION=cn-beijing
export VOLCENGINE_ENDPOINT=open.volcengineapi.com
export PORT=8000
uv run mcp-server-vpn
```

#### 客户端配置示例

将以下内容添加到 MCP 客户端的 settings 文件：

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

volcengine/mcp-server 遵循 [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)。

