# 边缘计算节点 MCP Server


## 版本信息

v0.1

## 产品描述

### 短描述

申请、配置、查阅在边缘计算节点，包括虚拟机、镜像、裸金属，及对应的网络配置。

### 长描述

基于覆盖全国各省市和运营商的边缘节点，火山引擎边缘计算节点产品为用户就近提供计算、网络、存储等资源，帮助用户将业务快速部署到边缘层。边缘计算节点提供不同粒度的算力服务，满足多样化场景中的用户需求。包含边缘计算节点、边缘容器、边缘托管和边缘函数等子产品。

## 分类

CDN与边缘

## 标签

边缘云，虚拟机，镜像，存储

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: start_cloud_server

根据边缘服务的 ID 启动边缘服务。

### Tool 2: get_cloud_server

根据边缘服务的 ID 获取边缘服务的详细信息。

### Tool 3: start_instances

根据边缘实例 ID 启动实例。

### Tool 4: get_instance

根据边缘实例 ID 获取实例详细信息。

### Tool 5: list_instances

列出指定的边缘服务或所有边缘服务下的边缘实例。

### Tool 6: get_image

获取容器镜像详情。

### Tool 7: list_instance_internal_ips

获取边缘实例的私网 IP 地址的列表。

### Tool 8: list_instance_types

获取边缘服务下可开通的实例规格。

## 可适配平台

Python

## 服务开通链接

https://console.volcengine.com/edge/veen

## 鉴权方式

AK&amp;SK

## 安装

### 使用 uv

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed.
We will use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run.

```bash
cd mcp-server/server/mcp_server_veen
uv run mcp-server-veen

# Start with sse mode (default is stdio)
uv run mcp-server-veen -t sse
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

## 许可

MIT
