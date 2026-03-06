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

### 工作区与分支

| 工具 | 说明 |
| ---- | ---- |
| `list_workspaces` | 列出当前账号下可访问的 Supabase workspace |
| `get_workspace` | 查询 workspace 详情，也支持直接传 branch ID |
| `create_workspace` | 创建新的 Supabase workspace |
| `pause_workspace` | 暂停 workspace |
| `restore_workspace` | 恢复已暂停的 workspace |
| `get_workspace_url` | 获取 workspace 或 branch 的 API 地址 |
| `get_publishable_keys` | 获取 publishable、anon、service_role 等密钥 |
| `list_branches` | 列出 workspace 下的分支 |
| `create_branch` | 创建开发分支 |
| `delete_branch` | 删除开发分支 |
| `reset_branch` | 将分支重置到初始状态 |

### 数据库

| 工具 | 说明 |
| ---- | ---- |
| `execute_sql` | 在 Postgres 数据库上执行原始 SQL |
| `list_tables` | 列出一个或多个 schema 下的表 |
| `list_migrations` | 查询 `supabase_migrations.schema_migrations` 中的迁移记录 |
| `list_extensions` | 列出已安装的 PostgreSQL 扩展 |
| `apply_migration` | 执行迁移 SQL，并写入 `supabase_migrations.schema_migrations` |
| `generate_typescript_types` | 根据 schema 元数据生成 TypeScript 类型定义 |

### Edge Functions

| 工具 | 说明 |
| ---- | ---- |
| `list_edge_functions` | 列出 workspace 或 branch 下的 Edge Functions |
| `get_edge_function` | 获取 Edge Function 的代码和配置 |
| `deploy_edge_function` | 创建或更新 Edge Function |
| `delete_edge_function` | 删除 Edge Function |

### Storage

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
| `DEFAULT_WORKSPACE_ID` | 否 | - | 未传 `workspace_id` 时使用的默认目标 |
| `READ_ONLY` | 否 | `false` | 设为 `true` 后会禁止所有写操作工具 |
| `SUPABASE_WORKSPACE_SLUG` | 否 | `default` | Edge Functions API 使用的项目 slug |
| `SUPABASE_ENDPOINT_SCHEME` | 否 | `http` | 生成 workspace URL 时使用的协议 |
| `PORT` | 否 | `8000` | 直接启动服务时监听的端口 |

## 部署

### 在本地代码仓库中运行

```bash
uv --directory /ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase run mcp-server-supabase
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
        "DEFAULT_WORKSPACE_ID": "ws-xxxxxxxx"
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
        "DEFAULT_WORKSPACE_ID": "ws-xxxxxxxx"
      }
    }
  }
}
```

### 直接使用 Python 入口启动

```bash
python3 -m mcp_server_supabase.server --port 8000
```

这个包同时暴露了 `mcp-server-supabase` 和 `supabase-aidap` 两个入口，示例统一使用 `mcp-server-supabase`。

## 使用说明

- 如果没有显式传入 `workspace_id`，且配置了 `DEFAULT_WORKSPACE_ID`，服务会自动使用这个默认目标。
- 如果传入的是 `br-xxxx` 这样的 branch ID，服务会自动解析所属 workspace。
- `get_publishable_keys` 在需要时会自动解析默认分支。
- `reset_branch` 虽然接收 `migration_version` 参数，但当前 AIDAP API 会忽略这个值，只执行分支重置。
- `deploy_edge_function` 当前支持 `native-node20/v1`、`native-python3.9/v1`、`native-python3.10/v1`、`native-python3.12/v1`。

## 可适配客户端

- Cursor
- Claude Desktop
- Cline
- Trae
- 所有支持 `stdio` 的 MCP Client

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
