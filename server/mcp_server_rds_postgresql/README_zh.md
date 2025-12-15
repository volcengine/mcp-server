# RDS PostgreSQL MCP Server
> 火山引擎 RDS PostgreSQL 版是由火山引擎提供的完全兼容开源 PostgreSQL 的关系型数据库服务，支持实例管理、数据库管理、账号管理、Schema管理、连接管理、参数管理、备份恢复、日志管理、事件管理、数据安全等关键特性。

---


| 项目 | 详情                                      |
| ---- |-----------------------------------------|
| 版本 | v1.1.0                                  |
| 描述 | 火山引擎 RDS PostgreSQL 版即开即用、稳定可靠的关系型数据库服务 |
| 分类 | 数据库                                     |
| 标签 | PostgreSQL, RDS, 关系型数据库, 数据库            |

---

## Tools

### 1. `describe_wal_log_backups`
- **详细描述**: 调用 DescribeWALLogBackups 接口获取指定实例已备份的 WAL 日志列表。
- **触发示例**: `获取实例postgres-123456的WAL日志备份列表`


### 2. `describe_db_instance_ssl`
- **详细描述**: 调用 DescribeDBInstanceSSL 接口查询指定实例的 SSL 设置。
- **触发示例**: `查询实例postgres-123456的SSL配置`


### 3. `describe_tasks`
- **详细描述**: 调用 DescribeTasks 接口查询任务。
- **触发示例**: `查看实例postgres-123456的最近任务`


### 4. `describe_db_engine_version_parameters`
- **详细描述**: 调用 DescribeDBEngineVersionParameters 接口查询指定数据库引擎版本支持用户设置的参数列表。
- **触发示例**: `查询PostgreSQL 14版本支持的参数列表`


### 5. `describe_planned_events`
- **详细描述**: 调用 DescribePlannedEvents 接口查询当前地域下的运维事件。
- **触发示例**: `查看当前地域的数据库运维事件`


### 6. `get_backup_download_link`
- **详细描述**: 调用 GetBackupDownloadLink 接口获取备份的下载链接。
- **触发示例**: `获取备份ID为backup-789012的下载链接`


### 7. `clone_database`
- **详细描述**: 调用 CloneDatabase 接口克隆已有数据库。
- **触发示例**: `克隆实例postgres-123456中的mydb数据库`


### 8. `describe_slots`
- **详细描述**: 调用 DescribeSlots 接口查询复制槽列表。
- **触发示例**: `查询实例postgres-123456的复制槽信息`


### 9. `describe_allow_list_detail`
- **详细描述**: 调用 DescribeAllowListDetail 接口查看白名单详情。
- **触发示例**: `查看白名单ID为allowlist-345678的详细信息`


### 10. `describe_allow_lists`
- **详细描述**: 调用 DescribeAllowLists 接口查看指定地域下的白名单列表。
- **触发示例**: `列出当前地域的所有白名单`


### 11. `revoke_db_account_privilege`
- **详细描述**: 调用 RevokeDBAccountPrivilege 接口清空对数据库账号的授权。

- **触发示例**: `清空实例postgres-123456中账号user1的所有权限`


### 12. `modify_db_endpoint_name`
- **详细描述**: 调用 ModifyDBEndpointName 接口修改连接终端名称。
- **触发示例**: `将实例postgres-123456的连接终端endpoint-789012改名为main-endpoint`


### 13. `describe_detached_backups`
- **详细描述**: 调用 DescribeDetachedBackups 接口查询已删除实例备份。
- **触发示例**: `查询已删除实例的备份列表`


### 14. `describe_backup_policy`
- **详细描述**: 调用 DescribeBackupPolicy 接口查询备份策略。
- **触发示例**: `查看实例postgres-123456的备份策略`


### 15. `describe_backups`
- **详细描述**: 调用 DescribeBackups 接口查询备份列表。
- **触发示例**: `列出实例postgres-123456的所有备份`


### 16. `modify_db_instance_name`
- **详细描述**: 调用 ModifyDBInstanceName 接口修改实例名称。
- **触发示例**: `将实例postgres-123456改名为my-postgres-instance`


### 17. `describe_db_instance_parameters`
- **详细描述**: 调用 DescribeDBInstanceParameters 接口查询实例的参数配置。
- **触发示例**: `查看实例postgres-123456的当前参数配置`


### 18. `modify_db_instance_parameters`
- **详细描述**: 调用 ModifyDBInstanceParameters 接口修改实例参数。
- **触发示例**: `修改实例postgres-123456的max_connections参数为500`


### 19. `modify_db_instance_charge_type`
- **详细描述**: 调用 ModifyDBInstanceChargeType 接口修改实例计费类型。
- **触发示例**: `将实例postgres-123456的计费类型改为包年包月`


### 20. `describe_db_instance_price_difference`
- **详细描述**: 调用 DescribeDBInstancePriceDifference 接口查询实例差价。
- **触发示例**: `查询实例postgres-123456升级规格的差价`


### 21. `modify_db_endpoint_dns`
- **详细描述**: 调用 ModifyDBEndpointDNS 接口修改实例私网地址的解析方式。
- **触发示例**: `修改实例postgres-123456的私网DNS解析方式`


### 22. `remove_tags_from_resource`
- **详细描述**: 调用 RemoveTagsFromResource 接口为实例解绑标签。
- **触发示例**: `为实例postgres-123456解绑标签env=test`


### 23. `add_tags_to_resource`
- **详细描述**: 调用 AddTagsToResource 接口为实例绑定标签。
- **触发示例**: `为实例postgres-123456添加标签env=prod`


### 24. `describe_db_instance_price_detail`
- **详细描述**: 调用 DescribeDBInstancePriceDetail 接口查询实例价格详情。
- **触发示例**: `查询创建PostgreSQL实例的详细价格`


### 25. `create_db_endpoint`
- **详细描述**: 调用 CreateDBEndpoint 接口为指定实例创建连接终端。
- **触发示例**: `为实例postgres-123456创建一个新的连接终端`


### 26. `describe_db_instance_detail`
- **详细描述**: 调用 DescribeDBInstanceDetail 接口查询实例详细信息。
- **触发示例**: `查看实例postgres-123456的详细信息`


### 27. `modify_db_instance_spec`
- **详细描述**: 调用 ModifyDBInstanceSpec 接口修改实例配置。
- **触发示例**: `将实例postgres-123456的规格升级为4核16G`


### 28. `restore_to_new_instance`
- **详细描述**: 调用 RestoreToNewInstance 接口恢复到新实例。
- **触发示例**: `从备份backup-789012恢复到新实例`


### 29. `create_db_instance`
- **详细描述**: 调用 CreateDBInstance 接口创建实例。
- **触发示例**: `创建一个PostgreSQL 14版本的实例`


### 30. `describe_db_instances`
- **详细描述**: 调用 DescribeDBInstances 接口查询实例列表。
- **触发示例**: `列出当前地域的所有PostgreSQL实例`


### 31. `describe_db_instance_specs`
- **详细描述**: 调用 DescribeDBInstanceSpecs 接口查询可售卖的实例规格。
- **触发示例**: `查询可用的PostgreSQL实例规格`


### 32. `describe_recoverable_time`
- **详细描述**: 调用 DescribeRecoverableTime 接口查询实例备份可恢复的时间范围。
- **触发示例**: `查询实例postgres-123456的可恢复时间范围`


### 33. `modify_db_endpoint_address`
- **详细描述**: 调用 ModifyDBEndpointAddress 接口修改实例私网连接地址的端口和前缀。
- **触发示例**: `修改实例postgres-123456的私网连接端口为5433`


### 34. `describe_failover_logs`
- **详细描述**: 调用 DescribeFailoverLogs 接口查询实例主备切换日志。
- **触发示例**: `查看实例postgres-123456的主备切换历史`


### 35. `reset_db_account`
- **详细描述**: 调用 ResetDBAccount 接口重置账号的密码。
- **触发示例**: `重置实例postgres-123456中账号user1的密码`


### 36. `modify_db_account_privilege`
- **详细描述**: 调用 ModifyDBAccountPrivilege 接口修改数据库账号权限。
- **触发示例**: `为实例postgres-123456的账号user1添加对mydb数据库的读写权限`


### 37. `create_schema`
- **详细描述**: 调用 CreateSchema 接口创建 Schema。
- **触发示例**: `在实例postgres-123456的mydb数据库中创建schema1`


### 38. `modify_schema_owner`
- **详细描述**: 调用 ModifySchemaOwner 接口修改 Schema 的 owner。
- **触发示例**: `将实例postgres-123456中mydb数据库的schema1的所有者改为user2`


### 39. `describe_schemas`
- **详细描述**: 调用 DescribeSchemas 接口查询 Schema 列表。
- **触发示例**: `列出实例postgres-123456中mydb数据库的所有schema`


### 40. `modify_database_owner`
- **详细描述**: 调用 ModifyDatabaseOwner 接口修改数据库 Owner。
- **触发示例**: `将实例postgres-123456中mydb数据库的所有者改为user2`


### 41. `create_database`
- **详细描述**: 调用 CreateDatabase 接口创建数据库。
- **触发示例**: `在实例postgres-123456中创建新数据库newdb`


### 42. `describe_databases`
- **详细描述**: 调用 DescribeDatabases 接口查询数据库列表。
- **触发示例**: `列出实例postgres-123456的所有数据库`


### 43. `create_db_account`
- **详细描述**: 调用 CreateDBAccount 接口创建账号。
- **触发示例**: `在实例postgres-123456中创建新账号user3`


### 44. `describe_db_accounts`
- **详细描述**: 调用 DescribeDBAccounts 接口查询账号列表。
- **触发示例**: `列出实例postgres-123456的所有账号`

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


