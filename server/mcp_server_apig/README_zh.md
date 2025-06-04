# APIG MCP Server 

## 版本信息
v0.2.0

## 产品描述

APIG MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎APIG服务交互的能力。可以基于自然语言对云端实例资源进行全链路管理，支持实例、服务、留有的查询操作，实现APIG资源的高效管理。

## 分类
容器与中间件

## 功能

- 查询实例信息
- 查询服务信息
- 查询路由信息
- 简单实例操作

## 可用工具
由于部分接口的入参和返回内容较多，一些不常用的内容会对大模型造成过长的上下文负担，为了避免不必要的token浪费，APIG MCP Server仅提供常见内容的查询。

- `list_gateways`: 查询网关实例列表
- 

## 使用指南

### 前置准备
- Python 3.12+
- UV

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 安装
克隆仓库:
```bash
git clone git@github.com:volcengine/mcp-server.git
```

### 使用方法
启动服务器:

#### UV
```bash
cd mcp-server/server/mcp_server_apig
uv run mcp-server-apig

# 使用sse模式启动(默认为stdio)
uv run mcp-server-apig -t sse
```

使用客户端与服务器交互:
```
Trae | Cursor ｜ Claude Desktop | Cline | ...
```

## 配置

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量 | 描述 | 默认值 |
|----------|------|--------|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号ACCESSKEY | - |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号SECRETKEY | - |
| `VOLCENGINE_REGION` | 火山引擎资源region | - |
| `VOLCENGINE_ENDPOINT` | 火山引擎endpoint | - |
| `MCP_SERVER_PORT` | MCP server监听端口 | `8000` |

例如，在启动服务器前设置这些环境变量:

```bash
export VOLCENGINE_ACCESS_KEY={ak}
export VOLCENGINE_SECRET_KEY={sk}
export VOLCENGINE_REGION={region}
export VOLCENGINE_ENDPOINT={endpoint}
export MCP_SERVER_PORT=8000
```

### uvx 启动
```json
{
    "mcpServers": {
        "mcp-server-apig": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_apig",
            "mcp-server-apig"
          ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "",
                "VOLCENGINE_SECRET_KEY": "",
                "VOLCENGINE_REGION": "",
                "VOLCENGINE_ENDPOINT": "",
                "MCP_SERVER_PORT": ""
            }
        }
    }
}
```

## 示例
### Cursor


# 证书
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
