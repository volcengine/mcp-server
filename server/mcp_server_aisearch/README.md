# AI搜索引擎 MCP Server

## 版本信息

v0.0.1

## 产品描述

火山引擎AI搜索引擎，为企业客户提供高效的知识库检索能力，支持文本和图片输入，可在各类业务场景中快速构建智能检索系统；AI 搜索引擎产品正在公测，集成前请在官网申请公测名额 https://www.volcengine.com/public_beta_invite?source=AI_Search（链接文本：公测申请| AI搜索引擎）。申请成功并开通服务后可开始配置集成。

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

根据用户输入的文本或图片查询对应数据集，返回原始搜索结果。该工具不能在不提供datasetId参数的情况下使用。

#### 调试所需的输入参数:

输入：

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["application_id","dataset_id"],
    "properties": {
      "application_id": {
        "description": "要搜索的应用ID",
        "type": "string"
      },
      "dataset_id": {
        "description": "要搜索的数据集ID",
        "type": "string"
      },
      "text": {
        "description": "搜索查询文本。必须提供文本或image_url之一。",
        "type": "string"
      },
      "image_url": {
        "description": "要搜索的图片URL。必须提供文本或image_url之一。",
        "type": "string"
      },
      "filter": {
        "description": "搜索结果的过滤条件。支持must、must_not、range操作符以及and、or逻辑操作符。格式：{\"op\": \"must\", \"field\": \"status\", \"conds\": [1,2]}。- op (必需)：操作符类型，支持\"must\"、\"must_not\"、\"range\"、\"and\"、\"or\"。- field (must、must_not、range必需)：应用过滤条件的字段。- conds (must、must_not必需)：过滤值列表。- conds (and、or必需)：嵌套的过滤条件。留空或设置为None表示不应用过滤。默认为None。",
        "type": "object",
        "properties": {
          "op": {
            "description": "指定过滤逻辑的算子类型，决定过滤条件如何生效。支持\"must\"、\"must_not\"、\"range\"、\"and\"、\"or\"。",
            "type": "string",
            "enum": ["must", "must_not", "range", "and", "or"],
            "required": true
          },
          "field": {
            "description": "指定需要应用过滤条件的目标字段（如数据的 \"状态字段 status\"\"时间字段 create_time\" 等 ）。当 op 为 must 、 must_not 、 range 时， 必须填写 field ，明确对哪个字段做过滤。当 op 为 and 、 or 时， 无需填写 field （这两类算子用于组合多组过滤条件，字段由嵌套的子条件定义 ）。",
            "type": "string",
            "example": "status"
          },
          "conds": {
            "description": "根据 op 类型，提供过滤所需的 \"值\" 或 \"嵌套条件\"。当 op 为 must / must_not 时， conds 需填 具体值的集合 （如 [1, 2] ），表示 field 字段需匹配（或排除）这些值。当 op 为 and / or 时， conds 需填 嵌套的过滤条件集合 （如 [{\"op\": \"must\", \"field\": ...}, {\"op\": \"range\", ...}] ），表示需组合多组过滤规则， and 要求全满足， or 要求满足任意一组。",
            "type": "array",
            "items": {
              "type": ["integer", "string"]
            }
          },
          "gte": {
            "description": "筛选 field 字段值 大于等于 该值的数据（如 price ≥ 100）。仅在 op=range 时生效。",
            "type": "number",
            "example": 100.0
          },
          "gt": {
            "description": "筛选 field 字段值 严格大于 该值的数据（如 price ＞ 100）。仅在 op=range 时生效。",
            "type": "number",
            "example": 100.0
          },
          "lte": {
            "description": "筛选 field 字段值 小于等于 该值的数据（如 price ≤ 500）。仅在 op=range 时生效。",
            "type": "number",
            "example": 500.0
          },
          "lt": {
            "description": "筛选 field 字段值 严格小于 该值的数据（如 price ＜ 500）。仅在 op=range 时生效。",
            "type": "number",
            "example": 500.0
          }
        }
      },
      "page_number": {
        "description": "要检索的结果页码。默认为1。",
        "type": "integer"
      },
      "page_size": {
        "description": "每页结果的数量。默认为10。",
        "type": "integer"
      }
    }
  },
  "name": "search",
  "description": "根据用户输入的文本或图片查询知识库文档，返回未经LLM处理的原始搜索结果。"
}
```

输出：

- 包含搜索结果的字典。

#### 最容易被唤起的 Prompt示例

在{applicationId}应用中的{datasetId}数据集中查找相关物品

### Tool 2: chat_search

#### 类型

saas

#### 详细描述

使用AI能力执行基于对话的搜索，根据领域知识回答用户问题。此接口适用于对话式搜索场景。如果需要非对话式搜索，应使用搜索接口。

#### 调试所需的输入参数:

输入：

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["application_id", "session_id"],
    "properties": {
      "application_id": {
        "description": "要搜索的应用ID",
        "type": "string"
      },
      "session_id": {
        "description": "对话会话的唯一标识符。",
        "type": "string"
      },
      "text": {
        "description": "搜索查询文本。必须提供文本或image_url之一。",
        "type": "string"
      },
      "image_url": {
        "description": "要搜索的图片URL。必须提供文本或image_url之一。",
        "type": "string"
      },
      "search_limit": {
        "description": "返回的最大搜索结果数。默认为10。",
        "type": "integer"
      },
      "dataset_ids": {
        "description": "要搜索的数据集ID列表。",
        "type": "array",
        "items": {
          "type": "string"
        }
      },
      "filters": {
        "description": "搜索结果的过滤条件，按数据集应用。格式：{\"dataset_id\": {\"op\": \"must\", \"field\": \"status\", \"conds\": [1,2]}}。- op (必需)：操作符类型，支持\"must\"、\"must_not\"、\"range\"、\"and\"、\"or\"。- field (must、must_not、range必需)：应用过滤条件的字段。- conds (must、must_not必需)：过滤值列表。- conds (and、or必需)：嵌套的过滤条件。留空或设置为None表示不应用过滤。默认为None。",
        "type": "object",
        "additionalProperties": {
          "type": "object",
          "properties": {
            "op": {
              "description": "指定过滤逻辑的算子类型，决定过滤条件如何生效。支持\"must\"、\"must_not\"、\"range\"、\"and\"、\"or\"。",
              "type": "string",
              "enum": ["must", "must_not", "range", "and", "or"],
              "required": true
            },
            "field": {
              "description": "指定需要应用过滤条件的目标字段（如数据的 \"状态字段 status\"\"时间字段 create_time\" 等 ）。当 op 为 must 、 must_not 、 range 时， 必须填写 field ，明确对哪个字段做过滤。当 op 为 and 、 or 时， 无需填写 field （这两类算子用于组合多组过滤条件，字段由嵌套的子条件定义 ）。",
              "type": "string",
              "example": "status"
            },
            "conds": {
              "description": "根据 op 类型，提供过滤所需的 \"值\" 或 \"嵌套条件\"。当 op 为 must / must_not 时， conds 需填 具体值的集合 （如 [1, 2] ），表示 field 字段需匹配（或排除）这些值。当 op 为 and / or 时， conds 需填 嵌套的过滤条件集合 （如 [{\"op\": \"must\", \"field\": ...}, {\"op\": \"range\", ...}] ），表示需组合多组过滤规则， and 要求全满足， or 要求满足任意一组。",
              "type": "array",
              "items": {
                "type": ["integer", "string"]
              }
            },
            "gte": {
              "description": "筛选 field 字段值 大于等于 该值的数据（如 price ≥ 100）。仅在 op=range 时生效。",
              "type": "number",
              "example": 100.0
            },
            "gt": {
              "description": "筛选 field 字段值 严格大于 该值的数据（如 price ＞ 100）。仅在 op=range 时生效。",
              "type": "number",
              "example": 100.0
            },
            "lte": {
              "description": "筛选 field 字段值 小于等于 该值的数据（如 price ≤ 500）。仅在 op=range 时生效。",
              "type": "number",
              "example": 500.0
            },
            "lt": {
              "description": "筛选 field 字段值 严格小于 该值的数据（如 price ＜ 500）。仅在 op=range 时生效。",
              "type": "number",
              "example": 500.0
            }
          }
        }
      }
    }
  },
  "name": "chat_search",
  "description": "使用AI能力执行基于对话的搜索，根据领域知识回答用户问题。"
}
```

输出：

- 包含对话结果和相关物品数据的字典。

#### 最容易被唤起的 Prompt示例

通过对话的形式，在{applicationId}应用中搜索和{query}相关的物品

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
cd mcp-server/server/mcp_server_aisearch
uv run mcp-server-aisearch

# 使用sse/streamable-http模式启动(默认为stdio)
uv run mcp-server-aisearch -t sse
uv run mcp-server-aisearch -t streamable-http
```

## 部署

### UVX

```json
{
  "mcpServers": {
    "mcp-server-aisearch": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_aisearch",
        "mcp-server-aisearch"
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