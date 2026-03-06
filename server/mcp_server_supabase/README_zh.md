# Supabase MCP Server

面向 AIDAP 工作区的 Supabase MCP 服务。

## 概览

这个服务通过 MCP 暴露 Supabase 能力，并统一使用 AIDAP `workspace` 作为核心资源模型。

支持范围：

- 工作区生命周期管理
- 分支生命周期管理
- 数据库访问
- Edge Functions
- 存储管理
- TypeScript 类型生成

## 环境变量

| 变量名 | 必需 | 说明 |
| --- | --- | --- |
| `VOLCENGINE_ACCESS_KEY` | 是 | 火山引擎访问密钥 |
| `VOLCENGINE_SECRET_KEY` | 是 | 火山引擎私密密钥 |
| `VOLCENGINE_REGION` | 否 | 区域，默认 `cn-beijing` |
| `READ_ONLY` | 否 | 设为 `true` 时禁止写操作 |
| `DEFAULT_WORKSPACE_ID` | 否 | 未传 `workspace_id` 时使用的默认工作区 |
| `SUPABASE_WORKSPACE_SLUG` | 否 | Edge Functions 使用的 slug，默认 `default` |
| `SUPABASE_ENDPOINT_SCHEME` | 否 | `http` 或 `https`，默认 `http` |

## 启动

```bash
python -m mcp_server_supabase.server
```

## MCP 客户端配置示例

```json
{
  "mcpServers": {
    "supabase": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server_supabase.server"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "cn-beijing",
        "DEFAULT_WORKSPACE_ID": "ws-xxxxxxxx"
      }
    }
  }
}
```

## 工具列表

### 工作区

- `list_workspaces`
- `get_workspace`
- `create_workspace`
- `pause_workspace`
- `restore_workspace`
- `get_workspace_url`
- `get_publishable_keys`

### 分支

- `list_branches`
- `create_branch`
- `delete_branch`
- `reset_branch`

### 数据库

- `execute_sql`
- `list_tables`
- `list_migrations`
- `list_extensions`
- `apply_migration`
- `generate_typescript_types`

### Edge Functions

- `list_edge_functions`
- `get_edge_function`
- `deploy_edge_function`
- `delete_edge_function`

### 存储

- `list_storage_buckets`
- `create_storage_bucket`
- `delete_storage_bucket`
- `get_storage_config`
- `update_storage_config`

## 使用说明

- 所有 `workspace_id` 参数都可以直接传分支 ID。
- 未传 `workspace_id` 时，如果配置了 `DEFAULT_WORKSPACE_ID`，服务会自动使用它。
- `get_publishable_keys` 在需要时会自动解析默认分支。
