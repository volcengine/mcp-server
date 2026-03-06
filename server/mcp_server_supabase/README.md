# Supabase MCP Server

**Supabase MCP Server** 是一款基于模型上下文协议（Model Context Protocol, MCP）的服务器，实现了对 AIDAP Supabase 服务的全链路智能化管理。通过自然语言指令，用户可以对项目、数据库、Edge Functions、存储等资源进行创建、查询、修改、删除等操作，从而大幅提升 Supabase 开发与运维的效率。

---

## 项目概览
| 项目 | 详情 |
| ---- | ---- |
| **版本** | v1.0.0 |
| **描述** | 基于 MCP 管理 AIDAP Supabase 资源，支持智能化数据库与应用开发 |
| **分类** | 数据库与应用开发 |
| **标签** | Supabase, PostgreSQL, Edge Functions, BaaS |

---

## 关键特性
- **自动默认分支解析**：`branch_id` 参数可选，系统会自动使用项目的默认分支。
- **完整工具集合**：提供高阶工具，覆盖数据库、Edge Functions、存储、项目与分支等核心能力。
- **安全与审计**：只读模式、凭证管理、细粒度日志查询与安全建议。
- **跨语言支持**：兼容 Python、Node.js、Go 等多语言客户端。

---

## 快速开始
### 系统依赖
- Python 3.10+
- 推荐使用 `uv` 包管理器

### 安装 `uv`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 本地开发（推荐）
在项目根目录执行：
```bash
uv sync
source .venv/bin/activate
mv .env_example .env   # 填写环境变量
```

### 运行方式
#### 方式一：使用 `uvx`（推荐）
在 MCP 客户端配置文件中添加：
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
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "cn-beijing"
      }
    }
  }
}
```
#### 方式二：本地直接运行
```json
{
  "mcpServers": {
    "supabase-dev": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/mcp-server/server/mcp_server_supabase",
        "run",
        "mcp-server-supabase"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "cn-beijing",
        "READ_ONLY": "true"
      }
    }
  }
}
```
#### 方式三：Python 直接执行
```json
{
  "mcpServers": {
    "supabase": {
      "command": "python",
      "args": ["-m", "mcp_server_supabase.server"],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "cn-beijing"
      }
    }
  }
}
```

---

## 配置说明
主要配置文件位于 `server/mcp_server_supabase/src/mcp_server_supabase/config/config.yaml`，常用字段：
- `transport`：`sse`、`StreamableHTTP`、`stdio`（默认 `sse`）
- `auth`：`oauth`、`none`
- `credential`：`env`（从环境变量读取 AK/SK）或 `token`
- `credential.env`：`VOLCENGINE_ACCESS_KEY`、`VOLCENGINE_SECRET_KEY`、`VOLCENGINE_REGION`

---

## 核心工具一览
> **注**：以下为常用工具示例，完整列表请参见文档章节 "Tools"。

### 数据库操作（8）
- `list_tables`
- `execute_sql`
- `list_extensions`
- `list_migrations`
- `apply_migration`
- `list_databases`
- `create_database`
- `drop_database`

### Edge Functions（5）
- `list_edge_functions`
- `get_edge_function`
- `deploy_edge_function`
- `delete_edge_function`
- `get_edge_function_logs`

### 存储管理（8）
- `list_storage_buckets`
- `create_storage_bucket`
- `delete_storage_bucket`
- `list_storage_objects`
- `delete_storage_object`
- `get_storage_object_info`
- `get_storage_config`
- `update_storage_config`

### 项目管理（11）
- `list_projects`
- `get_project`
- `create_project`
- `pause_project`
- `restore_project`
- `get_project_url`
- `get_publishable_keys`
- `list_branches`
- `create_branch`
- `delete_branch`
- `reset_branch`

---

## 常用 Prompt 示例
- **数据库**：`"列出我的数据库表"`、`"查询 users 表的所有数据"`
- **Edge Functions**：`"列出所有 Edge Functions"`、`"部署一个新的 Edge Function"`
- **存储**：`"列出所有存储桶"`、`"创建一个公开存储桶"`
- **项目**：`"列出我的所有项目"`、`"创建一个新的项目"`

---

## 文档与资源
- [火山引擎 AIDAP Supabase 官方文档](https://www.volcengine.com/docs/87275/2105900)
- [Model Context Protocol 介绍](https://modelcontextprotocol.io/introduction)
- [Supabase 官方文档](https://supabase.com/docs)

---

## License

本项目遵循 MIT 许可证：
[MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)
