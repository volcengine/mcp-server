# AISearch Engine MCP Server

## 版本信息

v0.0.1

## 产品描述

整合火山引擎AISearch服务，为企业客户提供高效的知识库检索能力，支持文本和图片输入，可在各类业务场景中快速构建智能检索系统

## 分类

搜索工具

## 标签
- 人工智能与机器学习
- 知识库检索
- 多模态搜索

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: search

#### 类型

saas

#### 详细描述

根据用户输入的文本或图片查询知识库文档，返回未经LLM处理的原始搜索结果

#### 调试所需的输入参数:

输入：

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "text": {
        "description": "搜索查询文本，与image_url二选一",
        "type": "string"
      },
      "image_url": {
        "description": "搜索图片URL，与text二选一",
        "type": "string"
      },
      "filter": {
        "description": "搜索结果过滤条件，支持must、must_not、range操作符及and、or逻辑运算符",
        "type": "object"
      },
      "page_number": {
        "description": "结果页码，默认为1",
        "type": "integer"
      },
      "page_size": {
        "description": "每页结果数量，默认为10",
        "type": "integer"
      },
      "dataset_id": {
        "description": "要搜索的数据集ID",
        "type": "string"
      }
    }
  },
  "name": "search",
  "description": "知识库原始检索"
}
```

输出：

- 原始搜索结果字典

#### 最容易被唤起的 Prompt示例

在{applicationId}应用中的{datasetId}数据集中推荐一个物品

### Tool 2: chat_search

#### 类型

saas

#### 详细描述

使用AI能力执行基于对话的搜索，根据领域知识回答用户问题

#### 调试所需的输入参数:

输入：

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["session_id"],
    "properties": {
      "session_id": {
        "description": "对话会话唯一标识符",
        "type": "string"
      },
      "text": {
        "description": "搜索查询文本，与image_url二选一",
        "type": "string"
      },
      "image_url": {
        "description": "搜索图片URL，与text二选一",
        "type": "string"
      },
      "search_limit": {
        "description": "返回的最大搜索结果数量，默认为10",
        "type": "integer"
      },
      "dataset_ids": {
        "description": "要搜索的数据集ID列表",
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "filters": {
        "description": "搜索结果过滤条件，按数据集应用",
        "type": "object"
      }
    }
  },
  "name": "chat_search",
  "description": "AI对话式搜索"
}
```

输出：

- AI基于搜索结果生成的回答内容

#### 最容易被唤起的 Prompt示例

通过对话的形式，在{applicationId}应用中推荐一个物品

## 可适配平台

Trae，Cursor，Python

## 服务开通链接 (整体产品)

登录火山控制台，开通【AI搜索】服务。具体版本功能范围、开通具体流程参考：https://www.volcengine.com/docs/85296/1544945

## 鉴权方式

- 火山引擎的AKSK鉴权体系

## 安装部署

### 前置准备

- Python 3.13+
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

**UV**

```bash
cd mcp-server/server/mcp_server_aisearch_engine
uv run mcp-server-aisearch-engine

# 使用sse/streamable-http模式启动(默认为stdio)
uv run mcp-server-aisearch-engine -t sse
uv run mcp-server-aisearch-engine -t streamable-http
```

## 部署

### UVX

```json
{
  "mcpServers": {
    "mcp-server-aisearch-engine": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_aisearch_engine",
        "mcp-server-aisearch-engine"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "你的火山引擎AK",
        "VOLCENGINE_SECRET_KEY": "你的火山引擎SK"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)