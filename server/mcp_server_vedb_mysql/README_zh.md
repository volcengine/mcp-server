# veDB MySQL MCP Server
> 云数据库 veDB MySQL 版采用计算存储分离架构，100%兼容MySQL，最多支持 200TiB 的超大容量结构化数据存储，单个数据库集群最多可扩展至 16 个计算节点。支持实例管理、账号管理、数据库管理、备份恢复、白名单、数据迁移、数据同步、读写分离、安全审计、高可用、版本升级、备份恢复等关键特性。

---


| 项目 | 详情 |
| ---- | ---- |
| 描述 | 火山引擎 veDB MySQL 版即开即用、稳定可靠的关系型数据库服务 |
| 分类 | 数据库 |
| 标签 | MySQL, RDS, 关系型数据库, 数据库 |

---

## 工具列表


### 实例管理

| 工具名称 | 作用 |
|---------|------|
| `list_vedb_mysql_instances` | 获取用户所有VeDB MySQL实例列表，包括实例ID和基本信息 |
| `describe_vedb_mysql_detail` | 获取特定VeDB MySQL实例的详细信息 |
| `modify_vedb_mysql_instance_alias` | 修改特定VeDB MySQL实例的别名 |
| `create_vedb_mysql_instance` | 创建VeDB MySQL实例 |
| `switch_instance_deletion_protection` | 开启或关闭实例删除保护功能 |
| `describe_db_instance_version` | 查询目标实例的版本 |
| `add_tags_to_resource` | 为一个或多个实例绑定标签 |
| `remove_tags_from_resource` | 为一个或多个实例解绑标签 |
| `modify_db_instance_spec` | 修改指定实例的节点配置 |
| `restart_db_instance` | 重启实例 |
| `change_master` | 切换主节点 |
| `delete_db_instance` | 删除实例 |
| `modify_db_node_config` | 设置指定节点在主备切换时被选为主节点的优先级 |

### 数据库和账号管理

| 工具名称 | 作用 |
|---------|------|
| `list_vedb_mysql_instance_databases` | 获取特定VeDB MySQL实例中创建的数据库列表，包括权限信息 |
| `list_vedb_mysql_instance_accounts` | 获取单个VeDB MySQL实例中的账户列表及其权限详情 |
| `modify_db_account_description` | 修改mysqld账号的描述信息 |
| `modify_database_description` | 修改mysqld数据库的描述信息 |
| `reset_account_priv` | 将高权限账号的权限重置到初始状态 |
| `revoke_db_account_privilege` | 为账号撤销对数据库的权限 |
| `grant_db_account_privilege` | 为账号赋予指定数据库的权限 |
| `reset_account_passwd` | 修改数据库账号密码 |
| `create_db_account` | 创建管理数据库的账号 |
| `create_database` | 为实例创建数据库 |
| `delete_db_account` | 删除数据库账号 |
| `delete_database` | 删除实例的数据库 |

### 备份和恢复

| 工具名称 | 作用 |
|---------|------|
| `restore_table` | 将实例的历史数据库和表恢复至原实例中 |
| `modify_backup_policy` | 修改指定实例的数据备份策略 |
| `restore_to_new_instance` | 将已有实例的备份数据恢复至一个新的实例中 |
| `create_backup` | 为指定实例创建数据备份 |
| `delete_backup` | 删除指定实例的手动备份文件 |
| `describe_backup_policy` | 查询指定实例的数据备份策略 |
| `describe_backups` | 查询指定实例的备份文件列表信息 |
| `describe_recoverable_time` | 查询实例备份可恢复的时间范围 |

### 连接终端管理

| 工具名称 | 作用 |
|---------|------|
| `modify_db_endpoint_address` | 修改连接地址端口或前缀 |
| `modify_db_endpoint_dns` | 修改私网地址的解析方式 |
| `describe_db_endpoint` | 查询指定实例连接终端的详细信息 |
| `delete_db_endpoint` | 删除连接终端 |
| `create_db_endpoint` | 创建连接终端 |
| `modify_db_endpoint` | 修改连接终端 |
| `create_db_endpoint_public_address` | 为指定的实例创建公网连接地址，即开启实例的公网访问功能 |
| `delete_db_endpoint_public_address` | 删除指定实例的公网连接地址，即关闭公网访问功能 |

### 任务和事件管理

| 工具名称 | 作用 |
|---------|------|
| `cancel_schedule_events` | 取消待执行的计划内事件 |
| `describe_schedule_events` | 查看当前账号下的计划内事件 |
| `modify_schedule_events` | 修改待执行事件的执行时间 |
| `modify_db_instance_maintenance_window` | 修改实例的可维护时间段 |

### 参数管理

| 工具名称 | 作用 |
|---------|------|
| `save_as_parameter_template` | 将指定实例的参数配置保存为参数模板 |
| `create_parameter_template` | 创建参数模板 |
| `apply_parameter_template` | 应用参数模板 |
| `describe_parameter_templates` | 查询参数模板列表 |
| `list_parameter_change_history` | 查询实例参数修改历史 |
| `delete_parameter_template` | 删除参数模板 |
| `describe_parameter_template_detail` | 查询参数模板详情 |
| `describe_db_instance_parameters` | 查询目标实例的参数列表 |
| `modify_db_instance_parameters` | 修改实例mysqld数据面参数 |
| `describe_modifiable_parameters` | 查询可修改的参数列表 |

### 信息查询

| 工具名称 | 作用 |
|---------|------|
| `create_vedb_mysql_allowlist` | 为VeDB MySQL创建网络白名单 |
| `bind_allowlist_to_vedb_mysql_instances` | 将网络白名单绑定到VeDB MySQL实例 |
| `describe_instance_allow_lists` | 查询实例绑定的白名单信息 |
| `modify_allow_list` | 修改目标白名单设置，例如白名单名称、IP白名单地址等 |
| `describe_allow_list_detail` | 查询目标白名单的详细信息，例如IP地址和绑定的实例详情 |
| `delete_allow_list` | 删除目标白名单 |
| `describe_allow_lists` | 查询当前账号下指定地域内的所有IP白名单信息 |
| `disassociate_allow_list` | 将目标实例从指定IP白名单中解绑 |
| `describe_storage_payable_price` | 查询存储价格 |
| `describe_availability_zones` | 查询当前地域下实例支持的可用区资源 |
| `describe_db_instance_specs` | 查询指定可用区支持的节点规格信息 |
| `describe_db_instance_price_detail` | 查询指定配置实例的价格详情 |
| `describe_regions` | 查询实例可用的地域资源 |

---

## 服务开通链接
[点击前往火山引擎veDB MySQL服务开通页面](https://console.volcengine.com/db/vedb-mysql)

---

## 鉴权方式
在火山引擎管理控制台获取访问密钥 ID、秘密访问密钥和区域，采用 API Key 鉴权。需要在配置文件中设置 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY`。

---

## 部署
火山引擎veDB MySQL服务接入地址: <https://www.volcengine.com/docs/6357/66583>
```json
{
  "mcpServers": {
    "vedb_mysql": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vedb_mysql",
        "mcp-server-vedbm"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "VOLCENGINE_REGION": "<VOLCENGINE_REGION>",
        "MCP_SERVER_PORT": "<PORT>",
        "VOLCENGINE_ENDPOINT": "<ENDPOINT>"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
