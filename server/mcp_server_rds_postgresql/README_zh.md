# RDS PostgreSQL MCP Server
> 火山引擎 RDS PostgreSQL 版是由火山引擎提供的完全兼容开源 PostgreSQL 的关系型数据库服务，支持实例管理、数据库管理、账号管理、Schema管理、连接管理、参数管理、备份恢复、日志管理、事件管理、数据安全等关键特性。

---


| 项目 | 详情 |
| ---- | ---- |
| 版本 | v1.0.0 |
| 描述 | 火山引擎 RDS PostgreSQL 版即开即用、稳定可靠的关系型数据库服务 |
| 分类 | 数据库 |
| 标签 | PostgreSQL, RDS, 关系型数据库, 数据库 |

---

## Tools

### 1. `describe_db_instances`
- **详细描述**：查看用户的 RDS PostgreSQL 实例列表，支持分页查询。
- **触发示例**：`"列出我的 RDS PostgreSQL 实例"`

### 2. `describe_db_instance_detail`
- **详细描述**：根据指定 RDS PostgreSQL 实例 ID 查看实例详情。
- **触发示例**：`"查看实例ID 为 postgres-123456 的详细信息"`

### 3. `describe_databases`
- **详细描述**：获取指定RDS PostgreSQL实例的数据库列表。
- **触发示例**：`"获取 postgres-123456 实例的数据库列表"`

### 4. `describe_db_accounts`
- **详细描述**：获取指定RDS PostgreSQL实例的账号列表。
- **触发示例**：`"获取 postgres-123456 实例的账号列表"`

### 5. `describe_schemas`
- **详细描述**：获取指定RDS PostgreSQL实例的schema列表。
- **触发示例**：`"获取 postgres-123456 实例的 schema 列表"`

### 6. `describe_db_instance_parameters`
- **详细描述**：获取指定RDS PostgreSQL实例参数列表。
- **触发示例**：`"获取 postgres-123456 实例的参数列表"`

### 7. `describe_allow_lists`
- **详细描述**：获取RDS PostgreSQL指定地域下的白名单列表。
- **触发示例**：`"获取 cn-beijing 地域下的白名单列表"`

### 8. `describe_allow_list_detail`
- **详细描述**：获取RDS PostgreSQL白名单详情。
- **触发示例**：`"获取白名单 acl-123456 的详情"`

### 9. `describe_backups`
- **详细描述**：获取指定RDS PostgreSQL实例备份列表。
- **触发示例**：`"获取 postgres-123456 实例的备份列表"`

### 10. `describe_backup_policy`
- **详细描述**：获取指定RDS PostgreSQL实例备份策略。
- **触发示例**：`"获取 postgres-123456 实例的备份策略"`

### 11. `create_db_instance`
- **详细描述**：创建RDS PostgreSQL实例。
- **触发示例**：`"创建一个 RDS PostgreSQL 实例"`

### 12. `create_database`
- **详细描述**：创建RDS PostgreSQL数据库。
- **触发示例**：`"在 postgres-123456 实例中创建一个数据库为 testdb"`

### 13. `create_db_account`
- **详细描述**：创建RDS PostgreSQL数据库账号。
- **触发示例**：`"在 postgres-123456 实例中创建一个账号为 testuser 的数据库账号"`

### 14. `create_schema`
- **详细描述**：创建RDS PostgreSQL数据库Schema。
- **触发示例**：`"在 postgres-123456 实例的 testdb 数据库中创建一个 schema 为 testschema"`

---

## 服务开通链接
[点击前往火山引擎 RDS PostgreSQL 服务开通页面](https://console.volcengine.com/db/rds-pg)

---

## 鉴权方式
在火山引擎管理控制台获取访问密钥 ID、秘密访问密钥和区域，采用 API Key 鉴权。需要在配置文件中设置 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY`。

---

## 部署
火山引擎RDS PostgreSQL 服务接入地址：https://www.volcengine.com/docs/6438/69237
```json
{
  "mcpServers": {
    "rds_postgresql": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_rds_postgresql",
        "mcp-server-rds-postgresql"
      ],
      "transportType": "stdio",
      "env": {
        "VOLCENGINE_ENDPOINT": "火山引擎endpoint",
        "VOLCENGINE_REGION": "火山引擎资源region",
        "VOLCENGINE_ACCESS_KEY": "火山引擎账号ACCESSKEY",
        "VOLCENGINE_SECRET_KEY": "火山引擎账号SECRETKEY",
        "MCP_SERVER_PORT": "MCP server监听端口"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).


