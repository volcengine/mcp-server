# Viking Knowledge Base MCP Server

## 产品描述

Viking Knowledge Base MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎知识库KnowledgeBase服务交互的能力。知识库MCP Server支持获取用户账号下的所有知识库列表，并在指定的知识库中检索结果。同时支持您以url上传的方式将文档上传到您的知识库,也支持查看文档和知识库的状态信息。

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
cd mcp-server/server/mcp_server_knowledgebase
uv run mcp-server-knowledgebase

# 使用sse模式启动(默认为stdio)
uv run mcp-server-knowledgebase -t sse
```

使用客户端与服务器交互:
```
Trae | Cursor ｜ Claude Desktop | Cline | ...
```

## 配置

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                     | 描述              | 默认值 |
|--------------------------|-----------------|-------|
| `VOLCENGINE_ACCESS_KEY`  | 火山引擎账号ACCESSKEY | - |
| `VOLCENGINE_SECRET_KEY`  | 火山引擎账号SECRETKEY | - |
| `KNOWLEDGE_BASE_PROJECT` | 知识库所属项目         | - |
| `KNOWLEDGE_BASE_REGION`  | 知识库区域           | cn-north-1 |
| `PORT`                   | MCP server监听端口  | `8000` |


## 可用工具

Knowledge Base MCP Server 提供以下功能

- `add_doc`: [上传文档（目前仅支持url）](https://www.volcengine.com/docs/84313/1254624)
- `get_doc`: [获取指定文档的状态](https://www.volcengine.com/docs/84313/1254615)
- `get_collection`: [获取知识库的详细信息](https://www.volcengine.com/docs/84313/1254602)
- `list_colletions`: [获取指定账户和Project下的知识库列表](https://www.volcengine.com/docs/84313/1254596)
- `search_knowledge`: [在指定知识库中进行搜索](https://www.volcengine.com/docs/84313/1350012)

#### add_doc

```python
add_doc(
    collection_name="collection_name",
    add_type="url",
    doc_id="_mcp_server_auto_gen_doc_id_xxxxxxx",
    doc_name="doc_xxxx",
    doc_type="pdf",
    url="http://xxxxx.pdf"
)
```

Parameters:
- `collection_name` (必须): 要上传文档的知识库名称
- `add_type` (必须): 上传文档的添加类型, mcp server目前仅支持url
- `doc_id` (必须): url上传方式需要指定doc_id
- `doc_name` (必须): url 上传方式需要指定doc_name.
- `doc_type` (必须): 要添加的文档的类型。对于结构化文档，支持 xlsx、csv 和 jsonl；对于非结构化文档，我们支持 txt、doc、docx、pdf、markdown、faq.xlsx 和 pptx
- `url` (必须): 待添加文档的 URL

#### get_doc

```python
get_doc(
    collection_name="collection_name",
    doc_id="_mcp_server_auto_gen_doc_id_xxxxxxx",
)
```

Parameters:
- `collection_name` (必须): 要获取信息的文档所属的知识库
- `doc_id` (必须): 要获取信息的文档ID

#### get_collection

```python
get_collection(
    collection_name="collection_name",
)
```

Parameters:
- `collection_name` (必须): 要获取信息的知识库名称


#### list_collections

```python
list_collections()
```

#### search_knowledge

```python
search_knowledge(
    query="How to reset my password?",
    limit=3,
    collection_name=None
)
```

Parameters:
- `query` (必须): 搜索查询字符串
- `limit` (可选): 返回的最大结果数（默认值：3）
- `collection_name` (可选): 要搜索的知识库名称。如果未提供，LLM将根据您账号列表下的知识库描述选择自动选择要搜索的知识库


### uvx 启动
```json
{
  "mcpServers": {
    "knowledgebase": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_knowledgebase",
          "mcp-server-knowledgebase"
        ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key", 
        "KNOWLEDGE_BASE_PROJECT": "your-project-name",
        "KNOWLEDGE_BASE_REGION": "your-region"
      }
    }
  }
}
```

## 证书
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
