# RDS MySQL MCP Server
> 火山引擎 RDS MySQL 版是由火山引擎提供的完全兼容开源 MySQL 的关系型数据库服务，支持实例管理、账号管理、数据库管理、备份恢复、白名单、透明数据加密、数据迁移、数据同步、读写分离、安全审计、高可用、版本升级、备份恢复等关键特性。

---


| 项目 | 详情 |
| ---- | ---- |
| 版本 | v1.0.0 |
| 描述 | 火山引擎 RDS MySQL 版即开即用、稳定可靠的关系型数据库服务 |
| 分类 | 数据库 |
| 标签 | MySQL, RDS, 关系型数据库, 数据库 |

---

## Tools

### 1. `list_rds_mysql_instances`
- **详细描述**：查看用户的 RDS MySQL 实例列表，支持分页查询。
- **触发示例**：`"列出我的 RDS MySQL 实例"`

### 2. `describe_rds_mysql_detail`
- **详细描述**：根据指定 RDS MySQL 实例 ID 查看实例详情。
- **触发示例**：`"查看实例 ID 为 mysql - 123456 的详细信息"`

### 3. `list_rds_mysql_instance_engine_minor_versions`
- **详细描述**：查询指定 RDS MySQL 实例可升级的内核小版本。
- **触发示例**：`"查看实例 mysql - 123456 可升级的内核版本"`

### 4. `list_rds_mysql_instance_accounts`
- **详细描述**：查看指定 RDS MySQL 实例的数据库账号列表，支持分页查询。
- **触发示例**：`"列出实例 mysql - 123456 的所有数据库账号"`

### 5. `list_rds_mysql_instance_databases`
- **详细描述**：查看指定 RDS MySQL 实例的数据库列表，支持分页查询。
- **触发示例**：`"列出实例 mysql - 123456 的所有数据库"`

### 6. `list_rds_mysql_instance_parameters`
- **详细描述**：查询指定 RDS MySQL 实例的参数配置。
- **触发示例**：`"查看实例 mysql - 123456 的参数配置"`

### 7. `list_rds_mysql_parameter_templates`
- **详细描述**：查询 MySQL 实例的参数模板列表，支持分页查询。
- **触发示例**：`"列出可用的 MySQL 参数模板"`

### 8. `describe_rds_mysql_parameter_template`
- **详细描述**：根据参数模版 ID 查询指定的参数模板详情。
- **触发示例**：`"查看参数模板 mysql - template - 123 的详细信息"`

### 9. `modify_rds_mysql_instance_alias`
- **详细描述**：修改 RDS MySQL 实例名称。
- **触发示例**：`"将实例 mysql - 123456 的名称改为生产数据库"`

### 10. `modify_rds_mysql_account_description`
- **详细描述**：修改 RDS MySQL 实例的数据库账号的描述信息。
- **触发示例**：`"将账号 admin 的描述改为管理员账号"`

---

## 服务开通链接
[点击前往火山引擎 RDS MySQL 服务开通页面](https://console.volcengine.com/db/rds-mysql)

---

## 鉴权方式
在火山引擎管理控制台获取访问密钥 ID、秘密访问密钥和区域，采用 API Key 鉴权。需要在配置文件中设置 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY`。

---

## 部署
火山引擎RDS MySQL 服务接入地址：https://www.volcengine.com/docs/6313/170639
```json
{
  "mcpServers": {
    "rds_mysql": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_rds_mysql",
        "mcp-server-rds-mysql"
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

