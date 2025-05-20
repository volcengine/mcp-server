# TrafficRoute MCP Server

## 版本信息

v0.1

## 产品描述

### 短描述

TrafficRoute 用于配置 DNS 规则，以确保终端请求能够正确快捷到达对应的服务节点。

### 长描述

TrafficRoute 用于配置 DNS 规则，以确保终端请求能够正确快捷到达对应的服务节点。

## 分类

企业应用

## 标签

DNS，Domain

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: list-zones

获取在 TrafficRoute 上的解析域名列表。

### Tool 2: create-zone

添加域名。
添加完毕后，后续可以通过 `create-record` 工具来添加解析。

### Tool 3: create-record

给指定域名增加解析记录。

### Tool 4: list-records

获取域名的全部解析记录列表。

## 可适配平台

Python

## 鉴权方式

AK&amp;SK

## 安装

### 使用 uv

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed.
We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run.

```bash
cd mcp-server/server/mcp_server_traffic_route
uv run mcp-server-traffic-route

# Start with sse mode (default is stdio)
uv run mcp-server-traffic-route -t sse
```

### 使用客户端

支持通过以下客户端与 MCP Server 交互，具体配置可查阅该客户端文档。

- 方舟
- Trae
- Cursor

## 部署

### UVX

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
        "VOLC_ACCESSKEY": "<Your-Volcengine-AK>",
        "VOLC_SECRETKEY": "<Your-Volcengine-SK>"
      }
    }
  }
}
```

## 许可

MIT
