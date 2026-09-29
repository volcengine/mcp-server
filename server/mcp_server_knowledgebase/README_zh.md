# Viking Knowledge Base MCP Server

[English](README.md)

## 产品介绍

Viking Knowledge Base MCP Server 让 Claude Desktop、Cursor、Cline、Trae
等 MCP 客户端能够与火山引擎 Viking 知识库交互，支持管理和查看知识库及
文档，并从知识库中检索相关知识切片。

## 功能

- 通过 URL 向知识库添加文档
- 获取文档信息和处理状态
- 使用游标分页获取文档列表
- 获取知识库信息和构建状态
- 获取已配置 Project 下的知识库列表
- 在知识库中检索，并支持可选的文档过滤条件
- 支持 Viking API Key 或火山引擎 AK/SK 鉴权
- 支持 stdio 和无状态 Streamable HTTP 传输

## 前置条件

- Python 3.10 或更高版本
- Viking 知识库 API Key，或火山引擎 AK/SK 凭证

## 安装

从 PyPI 安装：

```bash
pip install mcp-server-knowledgebase
```

也可以使用 `uv` 将其安装为持久可用的命令行工具：

```bash
uv tool install mcp-server-knowledgebase
```

本地开发时，克隆仓库并以 editable 模式安装当前软件包：

```bash
git clone https://github.com/volcengine/mcp-server.git
cd mcp-server/server/mcp_server_knowledgebase
uv pip install -e .
```

## 配置

### 鉴权

至少配置一种鉴权方式：

- API Key：设置 `VIKING_API_KEY`，请求使用
  `Authorization: Bearer <VIKING_API_KEY>`。
- AK/SK：同时设置 `VOLCENGINE_ACCESS_KEY` 和
  `VOLCENGINE_SECRET_KEY`，请求使用火山引擎 SignerV4 鉴权。

同时配置两种方式时，优先使用 `VIKING_API_KEY`。未配置 API Key 时，
Access Key 和 Secret Key 必须成对配置。

### 环境变量

| 环境变量 | 描述 | 默认值 |
|---|---|---|
| `VIKING_API_KEY` | Viking 知识库 API Key；配置后优先使用 | - |
| `VOLCENGINE_ACCESS_KEY` | 火山引擎 Access Key | - |
| `VOLCENGINE_SECRET_KEY` | 火山引擎 Secret Key | - |
| `KNOWLEDGE_BASE_PROJECT` | Viking 知识库所属 Project | `default` |
| `KNOWLEDGE_BASE_REGION` | AK/SK 签名使用的火山引擎地域 | `cn-north-1` |
| `KNOWLEDGE_BASE_TIMEOUT` | 上游请求超时时间，单位为秒 | `30` |
| `MCP_SERVER_HOST` | Streamable HTTP 监听地址 | `127.0.0.1` |
| `MCP_SERVER_PORT` | Streamable HTTP 端口；未设置时读取 `PORT` | `8000` |
| `STREAMABLE_HTTP_PATH` | Streamable HTTP 端点路径 | `/mcp` |

## 启动服务器

使用默认的 stdio 传输方式启动：

```bash
mcp-server-knowledgebase
```

无需持久安装即可直接运行已发布的软件包：

```bash
uvx --from mcp-server-knowledgebase mcp-server-knowledgebase
```

也可以在源码目录中直接运行模块：

```bash
python -m mcp_server_knowledgebase.server --transport stdio
```

使用无状态 Streamable HTTP 启动：

```bash
mcp-server-knowledgebase --transport streamable-http
```

默认端点为 `http://127.0.0.1:8000/mcp`。仅在可信网关后部署时设置
`MCP_SERVER_HOST=0.0.0.0`。

### MCP 协议与部署安全

服务器使用 MCP Python SDK 2.x，支持 `2026-07-28` 协议修订版，包括无状态
`server/discover` 协商。SDK 同时兼容基于旧版握手的客户端。由于 HTTP+SSE
已被 `2026-07-28` 规范弃用，本服务器不再提供该传输方式。

Streamable HTTP 不会自动把已配置的 Viking API Key 或火山引擎 AK/SK
转换成 MCP 调用方鉴权。远程部署时必须使用认证网关或兼容 MCP 的 OAuth，
并且不要向调用方暴露服务凭证。

## 可用工具

- [`add_doc`](https://www.volcengine.com/docs/84313/1254624)：通过 URL 添加文档
- [`get_doc`](https://www.volcengine.com/docs/84313/1254615)：获取文档信息和处理状态
- [`list_docs`](https://docs.volcengine.com/docs/84313/2477871?lang=zh)：使用游标分页获取文档列表
- [`get_collection`](https://www.volcengine.com/docs/84313/1254602)：获取知识库信息
- [`list_collections`](https://www.volcengine.com/docs/84313/1254596)：获取已配置 Project 下的知识库列表
- [`search_knowledge`](https://www.volcengine.com/docs/84313/1350012)：在知识库中检索知识

### `add_doc`

通过 URL 向知识库添加支持的文档。

```python
add_doc(
    collection_name="product_docs",
    add_type="url",
    doc_id="product_guide_2026",
    doc_name="Product Guide",
    doc_type="pdf",
    url="https://example.com/product-guide.pdf",
)
```

参数：

- `collection_name`（必填）：目标知识库名称。
- `add_type`（必填）：目前仅支持 `"url"`。
- `doc_id`（必填）：仅包含英文字母、数字和下划线的唯一 ID，必须以英文字母
  开头，长度为 1–128 个字符。
- `doc_name`（必填）：文档名称，长度为 1–256 个字符。
- `doc_type`（必填）：可选值为 `xlsx`、`csv`、`jsonl`、`txt`、`doc`、
  `docx`、`pdf`、`markdown`、`faq.xlsx` 或 `pptx`。
- `url`（必填）：可访问的文档 URL。

返回示例：

```json
{
  "collection_name": "product_docs",
  "doc_id": "product_guide_2026",
  "resource_id": "kb-example"
}
```

### `get_doc`

获取文档元数据和处理状态。

```python
get_doc(
    collection_name="product_docs",
    resource_id="kb-example",
    doc_id="product_guide_2026",
)
```

参数：

- `collection_name`（可选）：文档所属的知识库。
- `resource_id`（可选）：知识库 ID。与 `collection_name` 至少提供一个；同时提供时优先使用 `resource_id`。
- `doc_id`（必填）：文档 ID。

返回示例：

```json
{
  "collection_name": "product_docs",
  "doc_id": "product_guide_2026",
  "doc_name": "Product Guide",
  "doc_type": "pdf",
  "add_type": "url",
  "create_time": 1788220800,
  "update_time": 1788220860,
  "point_num": 53,
  "status": {
    "process_status": 0,
    "failed_code": null
  },
  "title": "Product Guide",
  "doc_summary": "Product setup and account management instructions.",
  "brief_summary": "An introduction to the product.",
  "meta": {
    "category": "product",
    "version": "2026"
  },
  "video_outline": {
    "title": "Product walkthrough",
    "summary": "A walkthrough of the product.",
    "chapters": [
      {
        "title": "Account settings",
        "content": "Open Account Settings.",
        "start_time": "00:00:10",
        "end_time": "00:00:30",
        "element_content": {
          "text": "Account Settings"
        }
      }
    ]
  },
  "audio_outline": {
    "title": "Product introduction",
    "summary": "An introduction to account management.",
    "chapters": [
      {
        "title": "Resetting your password",
        "content": "Select Reset Password.",
        "start_time": 10.0,
        "end_time": 30.0,
        "element_content": {
          "text": "Reset Password"
        }
      }
    ]
  }
}
```

`process_status` 状态值：`0` 表示处理完成，`1` 表示处理失败，`2` 或 `3`
表示排队中，`5` 表示删除中，`6` 表示处理中。Viking 未返回的字段为 `null`。

返回字段还包括 `title`（文档标题）、`doc_summary`（文档摘要）、
`brief_summary`（简短摘要）、`meta`（元数据）、`video_outline`（视频大纲）和
`audio_outline`（音频大纲）。大纲包含 `title`、`summary` 和 `chapters`；章节包含
`title`、`content`、`start_time`、`end_time` 和 `element_content`。

### `list_docs`

使用游标分页获取知识库中的文档列表。

```python
list_docs(
    collection_name="product_docs",
    resource_id="kb-example",
    limit=2,
    next_token=None,
)
```

参数：

- `collection_name`（可选）：要获取文档列表的知识库。
- `resource_id`（可选）：知识库 ID。与 `collection_name` 至少提供一个；同时提供时优先使用 `resource_id`。
- `limit`（可选）：单次返回的文档数量，范围为 1–100，默认值为 `50`。
- `next_token`（可选）：上一次调用返回的不透明游标。首次请求不传；返回值中的
  游标为空表示文档已全部返回。

返回示例：

```json
{
  "collection_name": "product_docs",
  "total_num": 3,
  "count": 1,
  "doc_list": [
    {
      "doc_id": "product_guide_2026",
      "doc_name": "Product Guide",
      "doc_type": "pdf",
      "create_time": 1788220800,
      "update_time": 1788220860,
      "point_num": 53,
      "status": {
        "process_status": 0,
        "failed_code": null
      },
      "brief_summary": "An introduction to the product.",
      "title": "Product Guide"
    }
  ],
  "has_more": true,
  "next_token": "opaque-cursor-for-next-page"
}
```

Viking 未提供 `total_num` 时，该字段为 `null`。

### `get_collection`

获取知识库信息和构建状态。

```python
get_collection(
    collection_name="product_docs",
    resource_id="kb-example",
)
```

参数：

- `collection_name`（可选）：知识库名称。
- `resource_id`（可选）：知识库 ID。与 `collection_name` 至少提供一个；同时提供时优先使用 `resource_id`。

返回示例：

```json
{
  "collection_name": "product_docs",
  "description": "Product manuals and release notes",
  "status": 1,
  "resource_id": "kb-example",
  "doc_num": 3,
  "create_time": 1788220800,
  "update_time": 1788220860
}
```

知识库状态值：`-1` 表示待构建，`0` 表示构建中，`1` 表示构建完成，`2`
表示构建失败，`3` 表示变更中。

### `list_collections`

获取全局配置 Project 下的所有知识库。

```python
list_collections()
```

此工具没有参数。

返回示例：

```json
{
  "collection_list": [
    {
      "collection_name": "product_docs",
      "description": "Product manuals and release notes",
      "resource_id": "kb-example-1",
      "create_time": 1788220800,
      "update_time": 1788220860
    },
    {
      "collection_name": "support_faq",
      "description": "Frequently asked support questions",
      "resource_id": "kb-example-2",
      "create_time": 1788220800,
      "update_time": 1788220860
    }
  ],
  "total_num": 2
}
```

### `search_knowledge`

在知识库中检索相关切片。可选的文档过滤条件可以包含或排除匹配的文档字段值。

```python
search_knowledge(
    query="How do I reset my password?",
    collection_name="support_faq",
    resource_id="kb-example",
    limit=10,
    doc_filter={
        "op": "must",
        "field": "doc_id",
        "conds": ["account_guide"],
    },
)
```

参数：

- `query`（必填）：检索问题，长度为 1–8000 个字符。
- `collection_name`（可选）：要检索的知识库。
- `resource_id`（可选）：知识库 ID。与 `collection_name` 至少提供一个；同时提供时优先使用 `resource_id`。
- `limit`（可选）：返回的最大切片数量，范围为 1–100，默认值为 `10`。
- `doc_filter`（可选）：包含以下字段的对象：
  - `op`：`"must"` 表示包含匹配结果，`"must_not"` 表示排除匹配结果。
  - `field`：要过滤的文档字段，例如 `"doc_id"`。
  - `conds`：用于匹配的非空值列表。

返回示例：

```json
{
  "result_list": [
    {
      "id": "chunk_001",
      "content": "Open Account Settings and select Reset Password.",
      "doc_id": "account_guide",
      "doc_name": "Account Guide",
      "title": "Account Guide",
      "doc_type": "pdf",
      "score": 0.85,
      "rerank_score": 0.92,
      "chunk_title": "Resetting your password",
      "audio_start_time": null,
      "audio_end_time": null,
      "video_start_time": null,
      "video_end_time": null,
      "chunk_attachment": [
        {
          "uuid": "image_1",
          "caption": "Account Settings",
          "type": "image"
        }
      ]
    }
  ]
}
```

Viking 未提供文档元数据时，`doc_id` 和 `doc_name` 为 `null`。非空的
`doc_id` 可以直接传给 `get_doc`。

切片还包括 `title`（文档标题）、`doc_type`（文档类型）、`score`（检索得分）、
`rerank_score`（重排得分）、`chunk_title`（切片标题）、`audio_start_time`、
`audio_end_time`、`video_start_time`、`video_end_time`（音视频起止时间）和
`chunk_attachment`（附件列表）。附件包含 `uuid`、`caption` 和 `type`。

`image`、`doc-image` 和 `table` 类型附件的图片链接通过 MCP `ResourceLink`
返回，包含 `uri`、`name`、`description` 和 `mimeType`（`image/*`），
URL 不包含在 `chunk_attachment` 中。

图片链接内容块示例：

```json
{
  "type": "resource_link",
  "uri": "https://example.com/account-settings.png",
  "name": "image_1",
  "description": "Account Settings",
  "mimeType": "image/*"
}
```

## MCP 客户端配置

下面是使用 `uvx` 和 Viking API Key 的 stdio 配置示例：

```json
{
  "mcpServers": {
    "knowledgebase": {
      "command": "uvx",
      "args": [
        "--from",
        "mcp-server-knowledgebase>=0.2.2",
        "mcp-server-knowledgebase"
      ],
      "env": {
        "VIKING_API_KEY": "your-viking-api-key",
        "KNOWLEDGE_BASE_PROJECT": "your-project-name",
        "KNOWLEDGE_BASE_REGION": "cn-north-1"
      }
    }
  }
}
```

也可以改为同时配置 `VOLCENGINE_ACCESS_KEY` 和
`VOLCENGINE_SECRET_KEY`。三种凭证均存在时，优先使用 `VIKING_API_KEY`。

## 故障排查

1. 鉴权错误
   - 检查 API Key 或 AK/SK 凭证。
   - 使用 AK/SK 时，必须同时配置两个值。
   - 检查凭证是否有权访问已配置的 Project 和知识库。
2. 连接超时
   - 检查到火山引擎 API 的网络连接。
   - 必要时调整 `KNOWLEDGE_BASE_TIMEOUT`。
3. 返回结果为空
   - 检查 Project 和知识库名称。
   - 检索时尝试扩大问题范围或移除文档过滤条件。
   - 获取文档列表时，只能继续使用上一次调用原样返回的 `next_token`。

## 许可证

本项目使用 [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)。
