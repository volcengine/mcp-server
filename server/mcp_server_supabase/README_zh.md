# Supabase MCP Server

[English](README.md) | 简体中文

> 面向 AIDAP workspace 的 Supabase MCP Server，通过 MCP 暴露工作区、分支、数据库、Edge Functions、Storage 和 TypeScript 类型生成能力。

| 项目 | 详情 |
| ---- | ---- |
| 版本 | v0.1.0 |
| 描述 | 基于 AIDAP workspace 的 Supabase MCP Server |
| 分类 | 数据库 / 开发工具 |
| 标签 | Supabase, PostgreSQL, Edge Functions, Storage, AIDAP |

## 工具列表

### `account`

| 工具 | 说明 |
| ---- | ---- |
| `list_workspaces` | 列出当前账号下可访问的 Supabase workspace |
| `get_workspace` | 查询 workspace 详情，也支持直接传 branch ID |
| `create_workspace` | 创建新的 Supabase workspace |
| `pause_workspace` | 暂停 workspace |
| `restore_workspace` | 恢复已暂停的 workspace |

### `docs`

当前没有暴露工具。

### `database`

| 工具 | 说明 |
| ---- | ---- |
| `execute_sql` | 在 Postgres 数据库上执行原始 SQL |
| `list_tables` | 列出一个或多个 schema 下的表 |
| `list_migrations` | 查询 `supabase_migrations.schema_migrations` 中的迁移记录 |
| `list_extensions` | 列出已安装的 PostgreSQL 扩展 |
| `apply_migration` | 执行迁移 SQL，并写入 `supabase_migrations.schema_migrations` |

### `debugging`

当前没有暴露工具。

### `development`

| 工具 | 说明 |
| ---- | ---- |
| `get_workspace_url` | 获取 workspace 或 branch 的 API 地址 |
| `get_publishable_keys` | 获取 publishable、anon、service_role 等密钥 |
| `generate_typescript_types` | 根据 schema 元数据生成 TypeScript 类型定义 |

### `functions`

| 工具 | 说明 |
| ---- | ---- |
| `list_edge_functions` | 列出 workspace 或 branch 下的 Edge Functions |
| `get_edge_function` | 获取 Edge Function 的代码和配置 |
| `deploy_edge_function` | 创建或更新 Edge Function |
| `delete_edge_function` | 删除 Edge Function |

### `branching`

| 工具 | 说明 |
| ---- | ---- |
| `list_branches` | 列出 workspace 下的分支 |
| `create_branch` | 创建开发分支 |
| `delete_branch` | 删除开发分支 |
| `reset_branch` | 将分支重置到初始状态 |

### `storage`

| 工具 | 说明 |
| ---- | ---- |
| `list_storage_buckets` | 列出存储桶 |
| `create_storage_bucket` | 创建新的存储桶 |
| `delete_storage_bucket` | 删除存储桶 |
| `get_storage_config` | 获取 Storage 配置 |

## 鉴权方式

使用火山引擎 AK/SK 鉴权。可在[火山引擎 API 访问密钥控制台](https://console.volcengine.com/iam/keymanage/)获取凭证。

## 环境变量

| 变量名 | 必需 | 默认值 | 说明 |
| ---- | ---- | ---- | ---- |
| `VOLCENGINE_ACCESS_KEY` | 是 | - | 火山引擎 Access Key |
| `VOLCENGINE_SECRET_KEY` | 是 | - | 火山引擎 Secret Key |
| `VOLCENGINE_REGION` | 否 | `cn-beijing` | AIDAP API 所在地域 |
| `WORKSPACE_REF` | 否 | - | 连接级 workspace scope，设置后会隐藏 `account` 组工具，并强制所有 workspace-scoped 调用只能访问这个目标 |
| `FEATURES` | 否 | `account,database,debugging,development,docs,functions,branching` | 官方 feature groups，`storage` 默认关闭 |
| `ENABLED_TOOLS` | 否 | - | 逗号分隔的工具白名单，作用在 `features` 过滤之后 |
| `DISABLED_TOOLS` | 否 | - | 逗号分隔的工具黑名单，优先级高于 `ENABLED_TOOLS` |
| `READ_ONLY` | 否 | `false` | 设为 `true` 后会禁止所有写操作工具 |
| `SUPABASE_WORKSPACE_SLUG` | 否 | `default` | Edge Functions API 使用的项目 slug |
| `SUPABASE_ENDPOINT_SCHEME` | 否 | `http` | 生成 workspace URL 时使用的协议 |
| `MCP_SERVER_HOST` | 否 | `0.0.0.0` | `sse` 和 `streamable-http` 使用的监听地址 |
| `MCP_SERVER_PORT` | 否 | `8000` | 网络传输优先使用的端口变量 |
| `PORT` | 否 | `8000` | 兼容保留的端口变量 |
| `MCP_MOUNT_PATH` | 否 | `/` | HTTP 传输的基础挂载路径 |
| `MCP_SSE_PATH` | 否 | `/sse` | SSE 连接路径 |
| `MCP_MESSAGE_PATH` | 否 | `/messages/` | SSE 消息投递路径 |
| `STREAMABLE_HTTP_PATH` | 否 | `/mcp` | Streamable HTTP 路径 |

## 部署

### 在本地代码仓库中运行

```bash
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase
```

### 显式指定 transport 启动

```bash
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase --transport stdio
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase --transport sse --host 0.0.0.0 --port 8000
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase --transport streamable-http --host 0.0.0.0 --port 8000
```

### 独立网络启动入口

```bash
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase-sse
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase-streamable
```

### 使用本地源码配置 MCP Client

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase",
        "run",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "<your-access-key>",
        "VOLCENGINE_SECRET_KEY": "<your-secret-key>",
        "VOLCENGINE_REGION": "cn-beijing",
        "WORKSPACE_REF": "ws-xxxxxxxx",
        "FEATURES": "database,functions"
      }
    }
  }
}
```

### 使用 `uvx` 配置 MCP Client

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_supabase",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "<your-access-key>",
        "VOLCENGINE_SECRET_KEY": "<your-secret-key>",
        "VOLCENGINE_REGION": "cn-beijing",
        "WORKSPACE_REF": "ws-xxxxxxxx",
        "FEATURES": "database,functions"
      }
    }
  }
}
```

### 直接使用 Python 入口启动

```bash
python3 -m mcp_server_supabase.server --port 8000
python3 -m mcp_server_supabase.server --transport sse --host 0.0.0.0 --port 8000
```

这个包同时暴露了 `mcp-server-supabase`、`supabase-aidap`、`mcp-server-supabase-sse` 和 `mcp-server-supabase-streamable` 四个入口，示例统一使用 `mcp-server-supabase`。

## 使用说明

- `WORKSPACE_REF` 会把连接 hard-scope 到单个目标，并在 tool schema 中移除 `workspace_id`。
- `WORKSPACE_REF` 生效时，`account` 组工具不会暴露，且显式传入其他 `workspace_id` 会被拒绝。
- `FEATURES` 只接受官方 8 个分组：`account`、`docs`、`database`、`debugging`、`development`、`functions`、`storage`、`branching`。
- 如果没有设置 `FEATURES`，默认启用 `account`、`database`、`debugging`、`development`、`docs`、`functions`、`branching`，`storage` 默认关闭。
- `ENABLED_TOOLS` 和 `DISABLED_TOOLS` 会在 feature 过滤之后继续收窄工具集，且 `DISABLED_TOOLS` 优先。
- 如果传入的是 `br-xxxx` 这样的 branch ID，服务会自动解析所属 workspace。
- `get_publishable_keys` 在需要时会自动解析默认分支。
- `reset_branch` 虽然接收 `migration_version` 参数，但当前 AIDAP API 会忽略这个值，只执行分支重置。
- `deploy_edge_function` 当前支持 `native-node20/v1`、`native-python3.9/v1`、`native-python3.10/v1`、`native-python3.12/v1`。
- `--transport sse` 会在 `MCP_SSE_PATH` 暴露 SSE 连接地址，并在 `MCP_MESSAGE_PATH` 暴露消息投递地址。
- `--transport streamable-http` 会在 `STREAMABLE_HTTP_PATH` 暴露 MCP HTTP 地址。
- 远程部署通常更推荐 `streamable-http`，但为了兼容仍保留 `sse`。

## 可适配客户端

- Cursor
- Claude Desktop
- Cline
- Trae
- 所有支持 `stdio`、`sse` 或 `streamable-http` 的 MCP Client

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
