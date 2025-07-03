# Viking Memory MCP Server

## 产品描述

Viking Memory MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎记忆库服务交互的能力。记忆库MCP Server支持您在对话过程中抽取用户记忆并上传到指定的记忆库，同事可以在对话过程中利用这些记忆。

## 分类
其他

## 功能

- 获取用户账号下的所有知识库列表
- 在指定的知识库中检索结果
- 以url上传的方式将文档上传到您的知识库
- 查看文档的处理状态
- 查看知识库的状态

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
cd mcp-server/server/mcp_server_vikingdb_memory
uv run mcp-server-vikingdb-memory

# 使用sse模式启动(默认为stdio)
uv run mcp-server-vikingdb-memory -t sse
```

使用客户端与服务器交互:
```
Trae | Cursor ｜ Claude Desktop | Cline | ...
```

## 配置

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                     | 描述              | 默认值        |
|--------------------------|-----------------|------------|
| `VOLCENGINE_ACCESS_KEY`  | 火山引擎账号ACCESSKEY | -          |
| `VOLCENGINE_SECRET_KEY`  | 火山引擎账号SECRETKEY | -          |
| `MEMORY_PROJECT` | 记忆库所属项目         | -          |
| `MEMORY_REGION`  | 记忆库区域           | cn-north-1 |
| `MEMORY_COLLECTION_NAME`  | 记忆库名称           | -          |
| `MEMORY_USER_ID`  | 记忆所属于的用户名       | -          |


## 可用工具

#### add_memories

添加记忆

```python
add_memories(
    text="some memory"
)
```

Parameters:
- `text` (必须): 需要记录的记忆

#### search_memory

检索记忆

```python
search_memory(
    query="query"
)
```

Parameters:
- `query` (必须): 查询内容


### uvx 启动
```json
{
  "mcpServers": {
    "mcp-server-vikingdb-memory": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vikingdb_memory",
        "mcp-server-vikingdb-memory"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "MEMORY_PROJECT": "default",
        "MEMORY_REGION": "cn-north-1",
        "MEMORY_COLLECTION_NAME": "your-memory-collection",
        "MEMORY_USER_ID": "your-user-id"
      }
    }
  }
}
```

## 证书
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
