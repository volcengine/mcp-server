#  RDS MSSQL MCP Server

 > 火山引擎 RDS SQL Server 版是由火山引擎提供的完全兼容微软SQL Server的关系型数据库服务，支持实例管理、账号管理、数据库管理、备份恢复（含全量、增量、日志备份及时间点恢复）、跨地域备份、白名单、透明数据加密（TDE）、数据迁移、数据同步、读写分离、安全审计、高可用架构（HA/集群版）、版本升级、备份策略自定义、恢复到已有实例、对象存储备份数据上云等关键特性。

---

| 项目 | 详情                                      |
| ---- |-----------------------------------------|
| 版本 | v1.0.0                                  |
| 描述 | 火山引擎 RDS SQL Server 版即开即用、稳定可靠的关系型数据库服务 |
| 分类 | 数据库                                     |
| 标签 | SQL Server, MSSQL, RDS, 关系型数据库, 数据库     |


---

## 支持的Tools

### 1. `describe_db_instances`  
- **详细描述**: 查询云数据库SQL Server版实例列表，支持按付费类型、状态、版本等条件筛选及分页。  
- **触发示例**: `"列出我的运行中的云数据库SQL Server实例"`  

### 2. `describe_db_instance_detail`  
- **详细描述**: 根据指定实例ID查看该云数据库SQL Server版实例的详情信息。  
- **触发示例**: `"查看实例ID为mssql-123456的详细信息"`  

### 3. `describe_db_instance_parameters`  
- **详细描述**: 根据指定实例ID查询该实例的参数信息，支持模糊查询参数名。  
- **触发示例**: `"查询实例mssql-123456中参数名包含Agent的参数"`  

### 4. `describe_available_cross_region`  
- **详细描述**: 查看跨地域备份的目的地域，可指定实例ID查询该实例可用的目的地域，或指定发起地域查询可用目的地域。  
- **触发示例**: `"查看实例mssql-123456可用于跨地域备份的目的地域"`  

### 5. `describe_availability_zones`  
- **详细描述**: 查询指定地域或所有地域的云数据库SQL Server版可用区列表。  
- **触发示例**: `"查询地域cn-beijing的云数据库SQL Server可用区列表"`  

### 6. `describe_backup_detail`  
- **详细描述**: 根据指定实例ID和备份ID查询该备份文件的详细信息。  
- **触发示例**: `"查询实例mssql-123456中备份ID为4969fcce7764447081c709c5****的详细信息"`  

### 7. `describe_backups`  
- **详细描述**: 根据指定实例ID查看该实例的备份集列表，支持按备份类型、时间范围等筛选。  
- **触发示例**: `"查看实例mssql-123456的全量备份集列表"`  

### 8. `describe_cross_backup_policy`  
- **详细描述**: 根据指定实例ID查看该实例的跨地域备份策略。  
- **触发示例**: `"查看实例mssql-123456的跨地域备份策略"`  

### 9. `describe_db_instance_specs`  
- **详细描述**: 查询云数据库SQL Server版实例的规格代码，支持按版本、实例类型、可用区筛选。  
- **触发示例**: `"查询SQL Server 2019标准版在cn-beijing-a可用区的实例规格代码"`  

### 10. `describe_regions`  
- **详细描述**: 查看云数据库SQL Server版支持的地域列表。  
- **触发示例**: `"列出云数据库SQL Server支持的所有地域"`  

### 11. `describe_tos_restore_task_detail`  
- **详细描述**: 根据指定恢复任务ID查询云数据库SQL Server版实例备份数据上云的详细信息。  
- **触发示例**: `"查看恢复任务ID为490的备份数据上云详细信息"`  

### 12. `describe_tos_restore_tasks`  
- **详细描述**: 查询实例备份数据上云任务列表，支持按实例ID、时间范围等条件筛选。  
- **触发示例**: `"查询实例mssql-123456最近7天的备份数据上云任务列表"`  


### 13. `modify_backup_policy`  
- **详细描述**: 修改指定实例的备份策略，包括备份时间窗口、全量备份周期、数据备份保留天数及日志备份频率。  
- **触发示例**: `"修改实例mssql-123456的备份策略，备份时间19:00Z-20:00Z，全量周期周一和周三，保留7天"`  

### 14. `modify_cross_backup_policy`  
- **详细描述**: 修改指定实例的跨地域备份策略，可设置是否开启备份、目的地域及保留天数。  
- **触发示例**: `"修改实例mssql-123456的跨地域备份策略，开启备份到cn-shanghai并保留14天"`  

### 15. `modify_db_instance_name`  
- **详细描述**: 修改指定实例的名称，需符合命名规则。  
- **触发示例**: `"将实例mssql-123456的名称改为new-sql-instance"`  


### 16. `create_backup`  
- **详细描述**: 为指定实例创建备份集，支持实例级或指定数据库备份，当前仅支持全量备份。  
- **触发示例**: `"为实例mssql-123456创建全量备份"`  

### 17. `create_db_instance`  
- **详细描述**: 创建云数据库SQL Server版实例，需指定版本、类型、可用区、规格、存储等参数。  
- **触发示例**: `"创建一个SQL Server 2019标准版的高可用实例，节点规格rds.mssql.se.ha.d4.4c16g，存储空间100GiB"`  

### 18. `create_tos_restore`  
- **详细描述**: 将对象存储TOS上的备份文件恢复到指定云数据库SQL Server版实例，支持全量、差异或日志恢复。  
- **触发示例**: `"将TOS地址tos-cn-beijing.volces.com:backname:slow_query.log的备份文件全量恢复到实例mssql-123456"`  

### 19. `restore_to_existed_instance`  
- **详细描述**: 以数据库为单位，将源实例的备份数据恢复到已有目标实例，支持按备份集或时间点恢复。  
- **触发示例**: `"将源实例mssql-123456的备份集f569f53bf60a48d5b****中的数据库恢复到目标实例mssql-789012"`

---

## 服务开通链接
>  [点击前往火山引擎 SQL Server 服务开通页面](https://console.volcengine.com/db/sql-server)


---

## 鉴权方式
在火山引擎管理控制台获取访问密钥 ID、秘密访问密钥和区域，采用 API Key 鉴权。
需要在配置文件中设置 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY`。


---

## 部署
>  火山引擎 SQL Server 服务接入地址：https://www.volcengine.com/docs/6899
```json
{
  "mcpServers": {
    "rds_mssql": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_rds_mssql",
        "mcp-server-rds-mssql"
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


---

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
