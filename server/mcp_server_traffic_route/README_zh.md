# TrafficRoute MCP Server

## 版本信息

v0.1

## 产品描述

### 短描述

支持对各种类型的 DNS 节点链路进行配置。

### 长描述

TrafficRoute 用于配置 DNS 链路规则，以确保终端请求能够正确快捷到达对应的服务节点。

## 分类

企业应用

## 标签

DNS，Domain

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: list_zones

获取在 TrafficRoute 上的解析域名列表。

### Tool 2: create_zone

添加域名配置。

### Tool 3: list_records

获取域名的全部解析记录列表。

## 可适配平台

- Python
- Node.js

## 鉴权方式

AK&amp;SK

### 获取 AK&amp;SK

从[火山引擎控制台](https://console.volcengine.com/iam/identitymanage/user)获取 Access Key ID 和 Secret Access Key。

注意：此 Access Key ID 和 Secret Access Key 须具有相关 OpenAPIs 访问权限。

### 环境变量配置

| 变量名 | 值 |
| ---------- | ---------- |
| `VOLCENGINE_ACCESS_KEY` | 账户对应的火山引擎 Access Key ID |
| `VOLCENGINE_SECRET_KEY` | 账户对应的火山引擎 Secret Access Key |

## Python 版 MCP server

### 依赖项

运行 MCP server 的设备需要安装以下依赖项。

- Python 3.11 或更高版本
- [`uv`](https://docs.astral.sh/uv/) &amp; [`uvx`](https://docs.astral.sh/uv/guides/tools/)
- 对于 Windows 操作系统，还需要参考 [PyCryptodome 文档](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#windows-from-sources) 配置该库编译环境，否则 MCP 服务无法正常启动。

### 部署与配置

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

## Node.js 版 MCP server

### 依赖项

运行 MCP server 的设备需要安装以下依赖项。

- Node.js 22.14.1 或更高版本

### 部署与配置

```json
{
  "mcpServers": {
    "mcp-server-traffic-route": {
      "command": "node",
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

## 使用客户端

支持通过以下客户端与 MCP Server 交互，具体配置可查阅该客户端文档。

- Cline
- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- 方舟

## 许可

[MIT](../../LICENSE)
