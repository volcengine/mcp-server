# EMR MCP Server 

## 版本信息
v0.1.0

## 产品描述

EMR MCP Server is a Model Context Protocol server that provides MCP clients (such as Claude Desktop) with the ability to interact with the Volcengine EMR service. 

## 分类
火山引擎 E-MapReduce（简称“EMR”）

## 功能
- 查询EMR on Serverless 作业实例信息
- 查询EMR on ECS集群信息
- 查询EMR on VKE集群信息

## 可用工具
由于部分接口涉及大量输入参数和返回内容，某些非常规内容会为大型语言模型（LLM）带来过重的上下文负担。为避免不必要的令牌浪费，EMR MCP服务器仅提供常见内容的查询服务。

- `list_serverless_jobs`: [查询EMR on Serverless 作业实例信息](https://www.volcengine.com/docs/6491/1263265)
- `list_emr_on_ecs_clusters`: [查询EMR on ECS集群信息](https://www.volcengine.com/docs/6491/1208305)
- `list_emr_on_vke_clusters`: [查询EMR on VKE集群信息](https://www.volcengine.com/docs/6491/1230115)

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
Start the server:

#### UV
```bash
cd mcp-server/server/mcp_server_emr
uv run mcp-server-emr

# 使用 streamable-http 模式启动(默认为stdio)
uv run mcp-server-emr -t streamable-http
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
| `MCP_SERVER_HOST` | MCP server监听主机 | `0.0.0.0` |
| `MCP_SERVER_PORT` | MCP server监听端口 | `8000` |
| `STREAMABLE_HTTP_PATH` | Streamable HTTP路径 | `/mcp` |
| `STATLESS_HTTP` | 是否启用无状态HTTP | `true` |



例如，在启动服务器前设置这些环境变量:

```bash
export VOLCENGINE_ACCESS_KEY={ak}
export VOLCENGINE_SECRET_KEY={sk}
export VOLCENGINE_REGION={region}
export MCP_SERVER_HOST=0.0.0.0
export MCP_SERVER_PORT=8000
export STREAMABLE_HTTP_PATH=/mcp
export STATLESS_HTTP=true
```

### uvx 启动

```json
{
  "mcpServers": {
    "mcp-server-emr": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_emr",
        "mcp-server-emr"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key-id",
        "VOLCENGINE_SECRET_KEY": "your-access-key-secret",
        "VOLCENGINE_REGION": "cn-beijing",
        "MCP_SERVER_HOST": "0.0.0.0",
        "MCP_SERVER_PORT": "8000",
        "STREAMABLE_HTTP_PATH": "/mcp",
        "STATLESS_HTTP": "true"
      }
    }
  }
}
```

# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
