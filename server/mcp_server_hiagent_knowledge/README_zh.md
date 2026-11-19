# HiAgent Knowledge MCP Server

## 产品描述

HiAgent Knowledge MCP Server 是一个模型上下文协议（Model Context Protocol）服务器，将**知识库（知识引擎）**能力封装为标准 MCP 工具，供 MCP 客户端（如 Claude Desktop、Cursor，以及 HiAgent 平台的 MCP 插件）使用。每个工具都按其对用户暴露的**能力**命名，而非直接照搬底层 OpenAPI 的 action 名。当前提供知识库发现（列知识库、查详情）与完整的知识引擎工具集（语义检索、正则匹配、文档元数据/切片、Wiki 检索/阅读）。

## 分类

其他

## 功能

- 列出指定 workspace 下的知识库列表，并查看单个知识库详情
- 在一个或多个知识库中按相关性检索知识片段（`search_knowledge`）
- 按 RE2 正则匹配切片（`grep_knowledge_chunks`）
- 批量读取文档元数据（`list_document_infos`）与按顺序读取文档切片（`list_document_chunks`）
- 搜索生成的 Wiki 页面（`search_wiki`）、读取 Wiki 页面（`read_wiki_page`），并溯源：按页面 slug 读引用切片（`read_wiki_source_chunk`）或按引用源文档的 resource_id 顺序读原文（`read_wiki_source_doc`）
- 查看 MCP Server 与 OpenAPI 的配置状态

### 面向能力的工具命名

HiAgent OpenAPI 通过单个 `CallKnowledgeEngineTool` action 暴露知识引擎：`ToolName` 字段选择子工具，请求体携带同名 PascalCase 参数对象。本 Server 把每个 `(ToolName, 参数对象)` 组合映射为一个面向能力命名、参数扁平的独立 MCP 工具：

| MCP 工具 | OpenAPI action | `ToolName` | 参数对象 | 能力 |
|---|---|---|---|---|
| `search_knowledge` | `CallKnowledgeEngineTool` | `knowledge_search` | `KnowledgeSearch` | 跨知识库按相关性检索 |
| `grep_knowledge_chunks` | `CallKnowledgeEngineTool` | `grep_chunks` | `GrepChunks` | 候选切片内 RE2 正则匹配 |
| `list_document_infos` | `CallKnowledgeEngineTool` | `list_doc_infos` | `ListDocInfos` | 按知识库批量查文档元数据 |
| `list_document_chunks` | `CallKnowledgeEngineTool` | `list_knowledge_chunks` | `ListKnowledgeChunks` | 顺序读取单个文档的分片 |
| `search_wiki` | `CallKnowledgeEngineTool` | `wiki_search` | `WikiSearch` | 搜索生成的 Wiki 页面 |
| `read_wiki_page` | `CallKnowledgeEngineTool` | `wiki_read_page` | `WikiReadPage` | 按 slug 读取 Wiki 页面 |
| `read_wiki_source_chunk` | `CallKnowledgeEngineTool` | `wiki_read_source_chunk` | `WikiReadSourceChunk` | 按页面 slug 读取 Wiki 引用的切片 |
| `read_wiki_source_doc` | `CallKnowledgeEngineTool` | `list_knowledge_chunks` | `ListKnowledgeChunks` | 按 resource_id 顺序读取某引用源文档的切片 |

> 说明：HiAgent 中 dataset 即知识库，故 `list_datasets` / `get_dataset` 是「列/查知识库」能力。逐子工具的参数、验证与返回结构清单见 [docs/knowledge-engine-subtools.md](../../docs/knowledge-engine-subtools.md)。

> 校验模型：本 Server 是薄适配层，只校验「必须发送的字段是否存在」（workspace/dataset ID、能力要求的 pattern/slug/queries 等）并依赖工具 schema 的参数类型；数值范围、枚举、跨字段规则（如 `limit`/`overlap` 的上下限、`grep_type` 的范围约束）由后端服务负责且随版本变化，因此其 `InvalidParameter.*` 报错会原样透传给调用方，不在本层重复校验。检索工具还接受可选的 `user_info`（`{"UserID": ..., "UserChannel": ...}`），原样透传为 OpenAPI 的 `UserInfo` 终端用户身份。仅当 `UserChannel="IAM"`（或可映射到 IAM 用户的 `"Lark"`）且 `UserID` 为租户内真实用户时，后端才据此做知识库/文档级权限过滤；其它渠道按游客处理。透传它可让检索遵循终端用户自身的访问权限。

## 使用指南

### 前置准备

- Python 3.11+
- UV
- API credentials (AK/SK)

### 安装

克隆仓库：

```bash
git clone git@github.com:volcengine/mcp-server.git
```

### 使用方法

启动服务器：

#### UV

```bash
cd mcp-server/server/mcp_server_hiagent_knowledge
uv run mcp-server-hiagent-knowledge

# 使用 streamable-http 模式启动（默认为 stdio）
uv run mcp-server-hiagent-knowledge --transport streamable-http

# 显式指定 HiAgent OpenAPI 版本（覆盖 HIAGENT_VERSION 环境变量；不填默认用最新）
uv run mcp-server-hiagent-knowledge --hiagent-version v3.1.0

# 只暴露部分工具（白名单，逗号分隔，-t 是 --tools 的简写）——
# 例如只保留 Wiki 相关工具，让模型稳定走 Wiki 检索
uv run mcp-server-hiagent-knowledge -t search_wiki,read_wiki_page,read_wiki_source_chunk,read_wiki_source_doc

# 屏蔽个别工具（黑名单，在白名单基础上再剔除；不给白名单时相当于从全部工具中剔除）
uv run mcp-server-hiagent-knowledge --disabled-tools grep_knowledge_chunks
```

#### 工具范围过滤

默认暴露全部工具。可用两个可选参数收窄暴露的工具集（都接受逗号分隔的**精确工具名**，未知名会直接报错退出；`health_check` 始终保留）：

| 参数 | 简写 | 环境变量 | 说明 |
|---|---|---|---|
| `--tools` | `-t` | `HIAGENT_TOOLS` | 白名单：选定基础工具集；不填表示全部工具 |
| `--disabled-tools` | - | `HIAGENT_DISABLED_TOOLS` | 黑名单：在白名单（或全部工具）基础上再剔除 |

生效顺序：先由 `--tools` 选出基础集（不填=全部），再用 `--disabled-tools` 从中剔除。每个参数的取值优先级为**命令行参数 > 同名环境变量 > 不设置**；环境变量取空值或纯空白（如 `HIAGENT_TOOLS=`）等同于不设置（=全部工具），不会把工具收窄到只剩 `health_check`。典型用法：知识库里同时挂了普通文档与生成的 Wiki，若希望模型稳定检索 Wiki，用 `-t` 只暴露 `search_wiki` / `read_wiki_page` / `read_wiki_source_chunk` / `read_wiki_source_doc` 即可。

使用客户端与服务器交互：

```
Trae | Cursor | Claude Desktop | Cline | HiAgent MCP 插件 | ...
```

## 配置

### 环境变量

以下环境变量可用于配置 MCP 服务器：

| 环境变量 | 描述 | 默认值 |
|---|---|---|
| `HIAGENT_TOP_HOST` | HiAgent Platform API（volc-top）网关地址，含 scheme 与端口 | - |
| `HIAGENT_ACCESS_KEY_ID` | HiAgent 账号 AccessKey ID | - |
| `HIAGENT_SECRET_ACCESS_KEY` | HiAgent 账号 SecretAccessKey | - |
| `HIAGENT_ACCOUNT_ID` | 作为 `X-Account-Id` 查询参数发送的主账号 ID | `1000000000` |
| `HIAGENT_VERSION` | 使用的 HiAgent OpenAPI 兼容版本，对应 `versions/` 下该版本的自有契约；不填默认使用最新已注册版本（当前为 `v3.3.0`）。也可用 `--hiagent-version` 命令行参数按次指定，且优先级更高；当前支持 `v3.1.0`、`v3.2.1`、`v3.3.0` | 最新（`v3.3.0`） |
| `HIAGENT_TOOLS` | 工具白名单，逗号分隔的精确工具名；选定暴露的基础工具集，不填表示全部。可用 `--tools`/`-t` 命令行参数按次指定，优先级更高 | - |
| `HIAGENT_DISABLED_TOOLS` | 工具黑名单，逗号分隔；在白名单（或全部工具）基础上再剔除。可用 `--disabled-tools` 命令行参数按次指定，优先级更高 | - |
| `HIAGENT_REGION` | 用于 AK/SK V4 签名的 Region（非网络地址） | `cn-north-1` |
| `FASTMCP_CHECK_FOR_UPDATES` | 设为 `off`，否则 FastMCP 启动时的联网版本检查在受限网络下可能导致启动失败 | - |
| `MCP_SERVER_HOST` | MCP server 绑定 host（streamable-http） | `127.0.0.1` |
| `MCP_SERVER_PORT` | MCP server 监听端口（streamable-http） | `8000` |

## 可用工具

HiAgent Knowledge MCP Server 提供以下功能：

- `health_check`: 返回 MCP server 与 OpenAPI 的配置状态
- `list_datasets`: 发现调用身份可访问的知识库（自有库与可见共享库）
- `get_dataset`: 获取单个知识库的详细信息
- `search_knowledge`: 在一个或多个知识库中按相关性检索知识片段
- `grep_knowledge_chunks`: 按 RE2 正则匹配知识切片
- `list_document_infos`: 按知识库批量获取文档元数据
- `list_document_chunks`: 按顺序列出单个文档/资源的知识分片
- `search_wiki`: 搜索生成的 Wiki 页面
- `read_wiki_page`: 按 slug 读取 Wiki 页面
- `read_wiki_source_chunk`: 读取 Wiki 页引用的原始文档切片
- `read_wiki_source_doc`: 按 resource_id 顺序读取某引用源文档的切片

#### health_check

```python
health_check()
```

#### list_datasets

发现调用身份可访问的知识库（自有库与可见共享库），通过
`list_datasets` 子工具调用（HiAgent v3.3.0 起统一发现）。独立 AK/SK 调用方经
`CallKnowledgeTool` 发起该发现，鉴权主体为调用身份本人；请求体与 wire 版本不变。

```python
list_datasets(
    workspace_id="workspace_id",   # 可选：不传则自动发现
    user_id="iam_user_id",
    keyword="财报",
    limit=20,
)
```

- `workspace_id`：可选。传则查该空间的自有及可见共享库；不传或传空白时，按调用身份
  合并其加入的 HiAgent 空间及旧个人空间可见的全部知识库，同一 `DatasetID` 只返回一次。
- `user_id`：可选 IAM 用户 ID，身份渠道固定为 IAM；不传则由服务端解析凭证对应用户。
- `keyword`：可选名称/描述关键词，对应 `ListDatasets.Filter.Keyword`。
- `limit`：可选，每页 1..100 条；不传时服务端默认 100。
- `cursor`：可选，上一页的 `NextCursor`。翻页时保持用户、Workspace、关键词及 limit 不变；
  不能复用其它工具或其它参数组合下的游标。
- `ids`：可选 ID 列表；`[]` 表示空结果，与显式 `limit`/`cursor` 互斥。

返回完整 OpenAPI 响应，结果位于 `Result.ListDatasets`：`Items` 含 `DatasetID`、
`Name`、`Description`、`WorkspaceID`、`Icon`、`IndexingTechnique`、`IndexTypes`，
`NextCursor` 仅在有下一页时返回，不包含 `Total`。共享库的 `WorkspaceID` 为源空间。
权限和参数值域由服务端校验；发现范围不替代检索时的权限校验。

迁移：本 Server 每次只使用一个契约，不探测后端版本，也不会在调用失败后改用其它契约，
因此请按实际部署的服务版本设置 `HIAGENT_VERSION`（或 `--hiagent-version`）。使用
`v3.1.0` 或 `v3.2.1` 时，`list_datasets` 仍为原 `ListDatasets` action：`workspace_id`
必填，分页用 `name`、`page_number`（默认 1）、`page_size`（默认 20），响应含 `Total`。
三个版本的 MCP 工具名都是 `list_datasets`，切换版本后需刷新客户端工具 schema，
工具白/黑名单也应填写对应版本实际暴露的名称。

#### get_dataset

`v3.3.0` 下经 `list_datasets` 的 `ids` 过滤读取，独立调用方不使用平台侧的
`GetDataset` action。

```python
get_dataset(
    workspace_id="workspace_id",
    dataset_id="dataset_id",
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_id` (必须): 要获取信息的知识库 ID

#### search_knowledge

```python
search_knowledge(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    queries=["如何重置密码？"],
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 要检索的知识库 ID 列表，至少 1 个
- `queries` (必须): 检索查询词列表，至少 1 个

#### grep_knowledge_chunks

按一条 RE2 正则匹配知识切片；用于错误码、标识符、固定短语等精确定位。先召回候选再匹配，不是全库扫描。

```python
grep_knowledge_chunks(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    pattern="ERR\\d+",
    queries=["错误码"],
    limit=10,
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 要检索的知识库 ID 列表，至少 1 个
- `pattern` (必须): 一条 RE2 正则（不支持反向引用/前后瞻）
- `queries` (可选): 用于缩小候选集的查询词
- `limit` (可选): 命中上限
- `grep_type` (可选): 扫描范围，`dataset_ids`（默认）或 `resource_ids`
- `resource_ids` (可选): 限定扫描的文档/资源 ID 列表；当 `grep_type` 为 `resource_ids` 时必填

#### list_document_infos

按知识库批量获取一个或多个文档的元数据（标题、类型、大小、状态、分段数、时间戳）。仅元数据，非文档内容。

```python
list_document_infos(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    resource_ids={"dataset_id": ["resource_id_1", "resource_id_2"]},
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 涉及的知识库 ID 列表，至少 1 个
- `resource_ids` (必须): 知识库 ID → 该库下文档/资源 ID 列表的映射；key 必须在 `dataset_ids` 内

#### list_document_chunks

按阅读顺序列出单个文档/资源的知识分片；与 `search_knowledge`（按查询相关性排序）不同，本工具顺序遍历一个资源，适合浏览文档全文。

```python
list_document_chunks(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    resource_id="resource_id",
    limit=50,
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 资源所属的知识库 ID 列表，至少 1 个
- `resource_id` (必须): 要列出分片的文档/资源 ID
- `limit` (可选): 每页返回的最大分片数
- `cursor_segment_id` (可选): 续页游标，传入上一页返回的最后一个 segment ID

#### search_wiki

搜索生成的 Wiki 页面，返回页面候选（含 `Slug`）用于导航，不作为最终证据。

```python
search_wiki(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    queries=["反向购买"],
    limit=5,
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 要检索的知识库 ID 列表，至少 1 个
- `queries` (必须): 检索查询词列表，至少 1 个
- `limit` (可选): 返回页面上限

#### read_wiki_page

按 slug 读取单个 Wiki 页面（结构、摘要、内容）。Wiki 页面是生成的导航材料，非最终证据。

```python
read_wiki_page(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    slug="concept/reverse-acquisition",
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 页面所属的知识库 ID 列表，至少 1 个
- `slug` (必须): Wiki 页面 slug（来自 `search_wiki`）

#### read_wiki_source_chunk

按页面 slug 读取 Wiki 页引用的切片——事实、数字、引文、代码的最终证据来源。若想按引用源文档的 resource_id 顺序读原文，改用 `read_wiki_source_doc`。

```python
read_wiki_source_chunk(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    slug="concept/reverse-acquisition",
    limit=5,
    overlap=2,
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 页面所属的知识库 ID 列表，至少 1 个
- `slug` (必须): 要读取来源的 Wiki 页面 slug
- `limit` (可选): 每页返回的最大源切片数
- `overlap` (可选): 每个引用切片前后各扩展的邻近分段数，用于补充上下文（0 表示不扩展）
- `cursor_segment_id` (可选): 续页游标

#### read_wiki_source_doc

按 resource_id 顺序读取某个被引用源文档的切片。与 `read_wiki_source_chunk` 互补：后者按页面 slug 读引用切片；本工具顺序遍历单个引用源文档（`resource_id`，如取自 Wiki 页面的 `SourceRefs`）。

```python
read_wiki_source_doc(
    workspace_id="workspace_id",
    dataset_ids=["dataset_id"],
    resource_id="resource_id",
    limit=50,
)
```

Parameters:
- `workspace_id` (必须): 知识库所属的 workspace ID
- `dataset_ids` (必须): 资源所属的知识库 ID 列表，至少 1 个
- `resource_id` (必须): 要读取的被引用源文档/资源 ID
- `limit` (可选): 每页返回的最大切片数
- `cursor_segment_id` (可选): 续页游标

### uvx 启动

```json
{
  "mcpServers": {
    "hiagent-knowledge": {
      "command": "uvx",
        "args": [
          "--from",
          "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_hiagent_knowledge",
          "mcp-server-hiagent-knowledge"
        ],
      "env": {
        "HIAGENT_TOP_HOST": "http://your-top-host:30040",
        "HIAGENT_ACCESS_KEY_ID": "your-access-key",
        "HIAGENT_SECRET_ACCESS_KEY": "your-secret-key",
        "HIAGENT_ACCOUNT_ID": "1000000000",
        "HIAGENT_REGION": "cn-north-1",
        "FASTMCP_CHECK_FOR_UPDATES": "off"
      }
    }
  }
}
```

## 证书

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
