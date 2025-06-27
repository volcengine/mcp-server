# VikingDB MCP Server 

## 产品描述

VikingDB MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎向量库VikingDB服务交互的能力。可以允许您从您的向量库中查询结果。

## 分类
其他

## 功能

- 在向量库中查询结果

## 使用指南

### 前置准备
- Python 3.10+
- UV
- API credentials (AK/SK)

### 安装
克隆仓库:
```bash
git clone git@github.com:volcengine/mcp-server.git
```

### 使用方法
启动服务器:

#### UV
```bash
cd mcp-server/server/mcp_server_vikingdb
uv run mcp-server-vikingdb

# 使用sse模式启动(默认为stdio)
uv run mcp-server-vikingdb -t sse
```

使用客户端与服务器交互:
```
Trae | Cursor ｜ Claude Desktop | Cline | ...
```

## 配置

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                       | 描述                       | 默认值 |
|----------------------------|--------------------------|-------|
| `VOLCENGINE_ACCESS_KEY`    | 火山引擎账号ACCESSKEY          | - |
| `VOLCENGINE_SECRET_KEY`    | 火山引擎账号SECRETKEY          | - |
| `VIKING_DB_COLLECTION_NAME`| 要查询的vikingdb的colletion名称 | - |
| `VIKING_DB_INDEX_NAME`     | 要查询的colletion的index名称    | - |
| `VIKING_DB_REGION`         | vikingdb区域，默认值           | cn-north-1 |
| `PORT`                     | MCP server监听端口           | `8000` |


## 可用工具

VikingDB MCP Server 仅提供查询结果的功能。

- `search_vikingdb`: [在指定collection和index中搜索结果](https://www.volcengine.com/docs/84313/1580544)

```python
search_vikingdb(
    query="How to reset my password?",
    limit=3,
    collection_name=None,
    index_name=None,
)
```

Parameters:
- `query` (必须): 查询字符串
- `limit` (可选): 返回的结果条数 (default: 3)
- `collection_name` (可选): 要搜索的vikingdb的colletion名称。如果未提供，则使用全局配置的colletion名称
- `index_name` (可选):要搜索的集合的 vikingdb 索引名称。如果未提供，则使用全局配置的索引名称



### uvx 启动
```json
{
  "mcpServers": {
    "vikingdb": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vikingdb",
          "mcp-server-vikingdb"
        ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VIKING_DB_COLLECTION_NAME": "your-vikingdb-collection-name",
        "VIKING_DB_INDEX_NAME": "your-vikingdb-index-name", 
        "VIKING_DB_REGION": "your-vikingdb-collection-region"
      }
    }
  }
}
```

## 证书
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
