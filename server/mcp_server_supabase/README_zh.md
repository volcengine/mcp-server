# MCP Server: Supabase
> 在 MCP 客户端中直接管理 AIDAP Supabase 项目、Postgres 数据库、Edge Functions 和 Storage。

[English](./README.md) | 简体中文

| 项目 | 详情 |
| ---- | ---- |
| 版本 | v0.1.0 |
| 描述 | 面向 AIDAP Supabase 的 MCP Server，为 AI 助手提供项目、数据库、Edge Functions 和存储管理能力。 |
| 分类 | 数据库 |
| 标签 | Supabase, PostgreSQL, AIDAP, Edge Functions, Storage |
| 文档 | [火山引擎 AIDAP Supabase](https://www.volcengine.com/docs/87275/2105900) |

## 核心能力

### 1. 项目与分支管理
- `list_projects`
  列出当前账号下可用的 AIDAP Supabase 项目。
- `get_project`
  获取指定项目详情，支持传入工作空间 ID 或分支 ID。
- `create_project`
  在 AIDAP 中创建新的 Supabase 项目。
- `pause_project`
  暂停项目。
- `restore_project`
  恢复已暂停项目。
- `get_project_url`
  获取当前工作空间或分支对应的项目访问地址。
- `get_publishable_keys`
  获取项目的 publishable key 和 service role key。
- `list_branches`
  列出项目下的开发分支。
- `create_branch`
  创建开发分支。
- `delete_branch`
  删除开发分支。
- `reset_branch`
  将分支重置到 AIDAP 当前支持的最新状态。

### 2. 数据库开发
- `execute_sql`
  直接执行 Postgres SQL。
- `list_tables`
  按 schema 列出数据表。
- `list_migrations`
  查看 `supabase_migrations.schema_migrations` 中记录的迁移历史。
- `list_extensions`
  列出已安装的 PostgreSQL 扩展。
- `apply_migration`
  执行 SQL 并写入迁移记录。
- `generate_typescript_types`
  基于数据库 schema 生成 TypeScript 类型定义。

### 3. Edge Functions
- `list_edge_functions`
  列出当前项目中的 Edge Functions。
- `get_edge_function`
  获取函数源码和元数据。
- `deploy_edge_function`
  使用 Node.js 或 Python 运行时部署或更新函数。
- `delete_edge_function`
  按名称删除函数。

### 4. Storage
- `list_storage_buckets`
  列出项目中的存储桶。
- `create_storage_bucket`
  创建存储桶，支持配置公开访问、文件大小限制和 MIME 类型限制。
- `delete_storage_bucket`
  删除存储桶。
- `get_storage_config`
  获取当前工作空间端点暴露的存储配置。
- `update_storage_config`
  在当前端点支持时更新存储配置。

## 兼容性说明

- 官方 Supabase MCP Server 主要基于 Supabase Management API 实现。AIDAP 没有同等的 Management API，所以这里是通过 AIDAP 的 workspace API 和 Supabase 工作空间端点来实现兼容能力。
- 在 AIDAP 里，`workspace` 对应 Supabase 的 `project`。为了兼容 MCP 侧常见命名，工具参数仍然使用 `project_id`。
- 大多数项目级工具里的 `project_id` 同时支持传入工作空间 ID 或分支 ID。传入 `br-xxx` 这类分支 ID 时，服务端会自动解析其所属 workspace。
- 未显式传入 `project_id` 时，服务端会优先使用 `DEFAULT_PROJECT_ID` 或 `DEFAULT_WORKSPACE_ID`。
- `reset_branch` 为兼容接口保留了 `migration_version` 参数，但当前 AIDAP API 会忽略它。
- `update_storage_config` 在部分 AIDAP 工作空间端点上可能返回 `supported: false`，表示当前端点暂不支持该能力。

## 接入指南

### 1. 环境依赖
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

### 2. 获取凭证
从[火山引擎访问密钥控制台](https://console.volcengine.com/iam/keymanage/)获取 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY`。

### 3. 环境变量

| 变量名 | 必需 | 说明 |
| ------ | ---- | ---- |
| `VOLCENGINE_ACCESS_KEY` | 是 | 火山引擎 Access Key ID |
| `VOLCENGINE_SECRET_KEY` | 是 | 火山引擎 Secret Access Key |
| `VOLCENGINE_REGION` | 否 | 区域，默认 `cn-beijing` |
| `DEFAULT_PROJECT_ID` | 否 | 未传 `project_id` 时使用的默认项目 ID |
| `DEFAULT_WORKSPACE_ID` | 否 | 与 `DEFAULT_PROJECT_ID` 作用相同 |
| `READ_ONLY` | 否 | 设置为 `true` 后禁止写操作 |
| `SUPABASE_ENDPOINT_SCHEME` | 否 | 工作空间端点协议，默认 `http` |
| `SUPABASE_PROJECT_SLUG` | 否 | Edge Functions 使用的项目 slug，默认 `default` |

## 快速部署

### 方式一：使用 `uvx`

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_supabase",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk",
        "VOLCENGINE_REGION": "cn-beijing"
      }
    }
  }
}
```

### 方式二：本地源码运行

```bash
cd /absolute/path/to/mcp-server/server/mcp_server_supabase
uv sync
```

```json
{
  "mcpServers": {
    "supabase": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-server/server/mcp_server_supabase",
        "run",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk",
        "VOLCENGINE_REGION": "cn-beijing",
        "DEFAULT_PROJECT_ID": "ws-xxxxxxxx"
      }
    }
  }
}
```

### 方式三：使用 `python3`

```json
{
  "mcpServers": {
    "supabase": {
      "command": "python3",
      "args": [
        "-m",
        "mcp_server_supabase.server"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk",
        "VOLCENGINE_REGION": "cn-beijing"
      }
    }
  }
}
```

## Prompt 示例

- `列出我所有的 Supabase 项目`
- `查看项目 ws-xxxx 下的所有分支`
- `执行 SQL: select * from public.users limit 10`
- `为 public,auth schema 生成 TypeScript 类型`
- `部署一个名为 webhook-handler 的 Edge Function`
- `列出项目 ws-xxxx 下的所有存储桶`

## 补充说明

- 大多数 MCP 桌面客户端默认使用 `stdio`，上面的配置方式最通用。
- 设置 `READ_ONLY=true` 后，所有写入类工具都会被拦截。
- 当端点解析或 API Key 获取依赖分支，而你又没有显式指定分支时，服务端会自动使用默认分支。

## License

volcengine/mcp-server 采用 [MIT 许可证](https://github.com/volcengine/mcp-server/blob/main/LICENSE) 授权。
