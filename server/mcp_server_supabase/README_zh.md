# Supabase MCP Server (Python 版本)

> 将 Supabase/AIDAP 项目连接到 Cursor、Claude、Windsurf 等 AI 助手

[English](./README.md) | 简体中文

## 功能特性

通过 [Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP)，AI 助手可以直接与你的 Supabase/AIDAP 项目交互。

### 支持的功能

- ✅ **工作空间管理** - 列出、创建、启动/停止工作空间，管理设置
- ✅ **数据库管理** - 列出表、执行 SQL、应用迁移、管理数据库和账户 ✨ 增强
- ✅ **Edge Functions** - 部署、获取代码、调用和管理 Edge Functions ✨ 增强
- ✅ **调试工具** - 获取多服务日志和性能/安全建议 ✨ 新增
- ✅ **开发工具** - 生成 TypeScript 类型、获取 API URL 和密钥 ✨ 新增
- ✅ **存储管理** - 管理存储桶和对象
- ✅ **分支管理** - 创建、删除、重置、恢复分支
- ✅ **AIDAP 集成** - 火山引擎工作空间管理（workspace = project）

## 快速开始

### 前置要求

⚠️ **重要**: 此 MCP server 依赖内部的 volcengine-python-sdk（包含 AIDAP 模块），需要先安装：

```bash
# 克隆 SDK 仓库
git clone https://code.byted.org/iaasng/volcengine-python-sdk.git -b aidap-Python-2025-10-01-online-2306-2026_02_27_11_45_12

# 安装 SDK
cd volcengine-python-sdk
pip install -e .
```

### 本地安装运行

安装完 volcengine-python-sdk 后：

```bash
# 安装 mcp-server-supabase
cd /path/to/mcp-server/server/mcp_server_supabase
pip install -e .

# 运行服务器
python -m mcp_server_supabase.server
```

### MCP 客户端配置

在 MCP 客户端（如 Claude Desktop、Cursor、Windsurf）中配置：

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
        "VOLCENGINE_REGION": "cn-beijing"
      }
    }
  }
}
```


## 环境变量配置

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `VOLCENGINE_ACCESS_KEY` | ✅ | 火山引擎访问密钥 |
| `VOLCENGINE_SECRET_KEY` | ✅ | 火山引擎私密密钥 |
| `VOLCENGINE_REGION` | ⭕ | 区域（默认：cn-beijing） |
| `READ_ONLY` | ⭕ | 只读模式（设置为 "true" 启用） |


## 🎯 自动默认分支解析

**新功能！** 现在大部分工具的 `branch_id` 参数都是可选的。如果不提供 `branch_id`，系统会自动使用工作空间的默认分支。

### 工作原理

1. **自动获取**：首次调用时，系统自动查询工作空间的默认分支
2. **智能缓存**：默认分支 ID 会被缓存，避免重复 API 调用
3. **自动刷新**：当设置新的默认分支时，缓存会自动清除

### 使用示例

```python
# 之前：必须提供 branch_id
execute_sql(workspace_id="xxx", branch_id="br-xxx", query="SELECT * FROM users")

# 现在：branch_id 可选，自动使用默认分支
execute_sql(workspace_id="xxx", query="SELECT * FROM users")
```

### 缓存管理

如果需要手动清除缓存（例如更改了默认分支）：

```python
# 清除特定工作空间的缓存
clear_default_branch_cache(workspace_id="xxx")

# 清除所有缓存
clear_default_branch_cache()
```


## 可用工具（54 个）

### 数据库操作（8 个）
- `list_tables` - 列出数据库表
- `execute_sql` - 执行 SQL 查询
- `list_extensions` - 列出数据库扩展
- `list_migrations` - 列出迁移历史 ✨ 新增
- `apply_migration` - 应用数据库迁移并记录到 schema_migrations ✨ 新增
- `list_databases` - 列出所有数据库
- `create_database` - 创建新数据库
- `drop_database` - 删除数据库

### Edge Functions（6 个）
- `list_edge_functions` - 列出 Edge Functions
- `get_edge_function` - 获取 Edge Function 源代码 ✨ 新增
- `deploy_edge_function` - 部署或更新 Edge Function ✨ 新增
- `delete_edge_function` - 删除 Edge Function ✨ 新增
- `invoke_edge_function` - 调用 Edge Function
- `get_edge_function_logs` - 获取函数日志

### 调试工具（2 个）
- `get_logs` - 获取服务日志 (postgres/api/auth/storage/realtime/functions) ✨ 新增
- `get_advisors` - 获取性能和安全建议 (检查缺失索引、未使用索引、缺失主键等) ✨ 新增

### 开发工具（3 个）
- `generate_typescript_types` - 根据数据库 schema 生成 TypeScript 类型定义 ✨ 新增
- `get_project_url` - 获取项目 API URL（别名：get_workspace_endpoints）
- `get_publishable_keys` - 获取可发布的 API 密钥（别名：get_workspace_api_keys）

### 存储管理（8 个）
- `list_storage_buckets` - 列出存储桶
- `create_storage_bucket` - 创建存储桶
- `delete_storage_bucket` - 删除存储桶
- `list_storage_objects` - 列出存储对象
- `delete_storage_object` - 删除存储对象
- `get_storage_object_info` - 获取对象元数据
- `get_storage_config` - 获取存储配置 ✨ 新增
- `update_storage_config` - 更新存储配置（需要付费计划） ✨ 新增

### 工作空间管理（12 个）
- `list_workspaces` - 列出所有工作空间
- `get_workspace` - 获取工作空间详情
- `create_workspace` - 创建新工作空间
- `delete_workspace` - 删除工作空间
- `start_workspace` - 启动工作空间
- `stop_workspace` - 停止工作空间
- `get_workspace_endpoints` - 获取工作空间端点
- `get_workspace_api_keys` - 获取 API 密钥
- `modify_workspace_name` - 修改工作空间名称
- `modify_workspace_settings` - 修改工作空间设置
- `modify_workspace_deletion_protection` - 修改删除保护策略
- `reset_workspace_password` - 重置管理员密码
- `get_workspace_usage_stats` - 获取使用统计

### 数据库账户管理（4 个）
- `list_db_accounts` - 列出数据库账户
- `create_db_account` - 创建数据库账户
- `delete_db_account` - 删除数据库账户
- `reset_db_account_password` - 重置账户密码

### 分支管理（10 个）
- `list_branches` - 列出所有分支
- `get_branch_detail` - 获取分支详情
- `create_branch` - 创建新分支
- `delete_branch` - 删除分支
- `reset_branch` - 重置分支
- `restart_branch` - 重启分支
- `restore_branch` - 恢复分支
- `set_default_branch` - 设置默认分支
- `list_restorable_branches` - 列出可恢复的分支
- `clear_default_branch_cache` - 清除默认分支缓存 ✨ 新增

## 使用示例

配置完成后，在 AI 助手中可以这样使用：

```
"帮我查看数据库中的所有表"
"执行 SQL: SELECT * FROM users LIMIT 10"
"生成数据库的 TypeScript 类型定义"
"部署一个新的 Edge Function"
"查看最近的 API 日志"
"列出所有组织和项目"
"列出所有 AIDAP 工作空间"
"获取工作空间的 API 密钥"
```

## 安全建议

⚠️ 连接 LLM 到数据源存在固有风险，请遵循以下最佳实践：

1. **不要连接生产环境** - 使用开发项目，避免暴露真实数据
2. **启用只读模式** - 设置 `READ_ONLY=true` 限制写操作
3. **项目范围限制** - 设置 `SUPABASE_PROJECT_REF` 限制访问范围
4. **审查工具调用** - 始终在 MCP 客户端中审查并批准工具调用

## 本地开发

```bash
# 克隆仓库
git clone https://github.com/volcengine/mcp-server.git
cd mcp-server/server/mcp_server_supabase

# 安装依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/
ruff check src/
```

## 项目结构

```
mcp_server_supabase/
├── pyproject.toml          # 项目配置
├── README.md               # 英文文档
├── README_zh.md            # 中文文档
└── src/
    └── mcp_server_supabase/
        ├── __init__.py
        └── server.py       # 主入口（FastMCP 实现）
```

## 常见问题

### Q: 如何获取 Supabase Access Token？

A: 访问 [Supabase Dashboard](https://supabase.com/dashboard/account/tokens) 生成个人访问令牌。

### Q: 如何获取 AIDAP 密钥？

A: 登录火山引擎控制台，在 [访问控制](https://console.volcengine.com/iam/keymanage/) 页面创建 Access Key。

### Q: AIDAP 中的 workspace 和 Supabase 的 project 有什么区别？

A: 在 AIDAP 中，workspace 就是 Supabase 的 project。两者是等价的概念，只是名称不同。

### Q: 只读模式有什么限制？

A: 只读模式下，只能执行 SELECT、WITH、EXPLAIN 查询，无法执行 INSERT、UPDATE、DELETE、CREATE 等写操作。

### Q: 如何更新到最新版本？

A: 使用 `uvx` 会自动使用最新版本，无需手动更新。

## 相关资源

- [Model Context Protocol 文档](https://modelcontextprotocol.io/introduction)
- [Supabase 文档](https://supabase.com/docs)
- [AIDAP 文档](https://www.volcengine.com/docs/6431/1181698)
- [火山引擎 MCP Server 仓库](https://github.com/volcengine/mcp-server)

## 许可证

Apache 2.0 - 详见 [LICENSE](../../LICENSE) 文件
