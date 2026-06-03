# OpenViking 控制面 — MCP Server + CLI

OpenViking 控制面（topapi · `top` 集群）的 MCP Server **与** CLI —— 用于管理 OV 库
（`Collection`）。两个前端共用同一套核心（`client.py`），新增一个能力即可同时被 MCP
和 CLI 使用。

覆盖 6 个核心控制面 Action：

| Action | MCP tool | CLI 命令 |
|---|---|---|
| `ListOpenVikingCollections` | `list_collections` | `ov-cp list` |
| `CreateOpenVikingCollection` | `create_collection` ⚠️ | `ov-cp create` |
| `GetOpenVikingCollection` | `get_collection` | `ov-cp get <rid>` |
| `DeleteOpenVikingCollection` | `delete_collection` ⚠️ | `ov-cp delete <rid>` |
| `GetOpenVikingUsage` | `get_usage` | `ov-cp usage <rid>` |
| `GetOpenVikingCollectionUserAccess` | `get_collection_api_key` | `ov-cp api-key <rid>` |

## 鉴权（开发阶段）

目前**不实现签名**。开发阶段由你手动提供请求 header（从浏览器 DevTools「Copy request
headers」复制即可），工具每次请求原样回放。鉴权是可插拔的（`common/auth.py` →
`ManualHeadersAuth`），后续接入独立 API Key / AK-SK 签名时只需替换这一处。

### 配置

| 项 | 环境变量 | CLI 参数 | 默认 |
|---|---|---|---|
| 网关 host | `VIKING_HOST` | `--host` | （可由 `Host` header 兜底） |
| 协议 | `VIKING_SCHEMA` | `--schema` | `https` |
| 默认 project | `OPENVIKING_PROJECT` | `--project` | `default` |
| 鉴权 header（文件） | `VIKING_HEADERS_FILE` | `--headers-file` / `-H` | — |
| 鉴权 header（内联） | `VIKING_HEADERS` | `--header 'K: V'`（可重复） | — |

header 文件可以是 JSON 对象，也可以是原始 `Key: Value` 多行块（`:authority` 这类
HTTP/2 伪首部会被跳过）。若 header 中已含 `Host`，可省略 `VIKING_HOST`。

## CLI 用法

```bash
uv sync                      # 或：pip install -e .

# 只读
uv run ov-cp --headers-file headers.txt --host vikingdb-stg.cn-beijing.volcengineapi.com list
uv run ov-cp -H headers.txt get   <ResourceID>
uv run ov-cp -H headers.txt usage <ResourceID>
uv run ov-cp -H headers.txt api-key <ResourceID>

# 建库（消耗付费配额，单账号上限 20 个库）
uv run ov-cp -H headers.txt create \
  --name my_kb --source volcengine \
  --vlm-model doubao-vision-... --vlm-api-key-id <id> \
  --emb-model doubao-embedding-... --emb-api-key-id <id>

# 删库（不可逆）
uv run ov-cp -H headers.txt delete <ResourceID> --yes
```

`ov-cp --help` 不需要任何配置即可运行。

## MCP 用法（stdio / uvx）

Server 默认 **stdio** 传输，可被任意 MCP 客户端作为子进程拉起。`.mcp.json` 配置：

```json
{
  "mcpServers": {
    "openviking-controlplane": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_openviking_controlplane",
        "mcp-server-openviking-controlplane"
      ],
      "env": {
        "VIKING_HOST": "vikingdb-stg.cn-beijing.volcengineapi.com",
        "VIKING_HEADERS_FILE": "/absolute/path/to/headers.txt"
      }
    }
  }
}
```

本地开发可改指向你的代码检出：

```json
{
  "mcpServers": {
    "openviking-controlplane": {
      "command": "uv",
      "args": ["run", "--directory", "/abs/path/server/mcp_server_openviking_controlplane",
               "mcp-server-openviking-controlplane"],
      "env": { "VIKING_HOST": "...", "VIKING_HEADERS_FILE": "/abs/path/headers.txt" }
    }
  }
}
```

需要 SSE 时：`mcp-server-openviking-controlplane --transport sse`。

> ⚠️ `create_collection` / `delete_collection` 会创建/销毁**付费**资源，且已暴露为 MCP
> tool；其描述会要求模型先与你确认。最终拦截依赖客户端的工具授权弹窗。
