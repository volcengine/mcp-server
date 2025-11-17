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

| 工具名称 | 作用 | 触发示例 |
|---------|------|----------|
| **参数管理工具** |
| save_as_parameter_template | 将指定实例的参数配置保存为参数模板 | 将实例vedbm-****的当前参数配置保存为新的参数模板，模板名称为custom_template |
| create_parameter_template | 创建参数模板 | 创建一个名为new_template的MySQL 8.0参数模板，包含参数max_connections=1000 |
| list_parameter_templates | 查询参数模板列表 | 查询所有MySQL 8.0版本的参数模板 |
| describe_parameter_template_detail | 查询参数模板详情 | 查询参数模板vedbmpt-****的详细配置 |
| describe_db_parameters | 查询实例的mysql参数列表 | 查询实例vedbm-instanceid的所有内核参数 |
| **数据库和账号管理工具** |
| list_vedb_mysql_instance_databases | 获取特定VeDB MySQL实例中创建的数据库列表，包括权限信息 | 查询实例中的所有数据库列表及权限详情 |
| list_vedb_mysql_instance_accounts | 获取单个VeDB MySQL实例中的账户列表及其权限详情 | 查询实例中的所有账号列表及权限详情 |
| modify_db_account_description | 修改实例内某个mysql账号的描述信息 | vedbm-instanceid下修改账号user1的描述信息为开发账号 |
| modify_database_description | 修改实例内某个mysql数据库的描述信息 | vedbm-instanceid下修改数据库test_db的描述信息为测试数据库 |
| create_db_account | 在实例内创建mysql账号 | 在实例vedbm-instanceid内创建普通新账号test_mcp，密码为Password123 |
| create_database | 在实例内创建mysql数据库 | vedbm-instanceid下创建数据库test_db |
| **备份和恢复工具** |
| restore_to_new_instance | 将已有实例的备份数据恢复至一个新的实例中 | 使用实例vedbm-****的备份数据（备份ID：snap-**-**）创建一个新实例，规格为vedb.mysql.x4.large，节点数为2，VPC和子网与原实例保持一致 |
| create_backup | 为指定实例创建数据备份 | 为实例vedbm-instanceid创建一个手动全量备份 |
| get_backup_policy | 查询指定实例的数据备份策略 | 查询实例vedbm-****当前的数据备份策略 |
| list_backups | 查询指定实例的备份列表 | 查询实例vedbm-instanceid的所有成功完成的快照 |
| get_recoverable_time | 查询实例备份可恢复的时间范围 | 查询实例vedbm-instanceid可恢复的时间范围 |
| **实例管理工具** |
| list_vedb_mysql_instances | 获取用户所有VeDB MySQL实例列表，包括实例ID和基本信息 | 查询所有实例列表 |
| describe_vedb_mysql_detail | 获取特定VeDB MySQL实例的详细信息 | 查询指定实例的详细信息 |
| modify_vedb_mysql_instance_alias | 修改特定VeDB MySQL实例的别名 | 修改实例别名 |
| create_vedb_mysql_instance | 创建VeDB MySQL实例 | 创建新的数据库实例 |
| add_tags_to_resource | 为一个或多个实例绑定标签 | 为实例vedbm-instanceid添加标签test=mcp |
| remove_tags_from_resource | 为一个或多个实例解绑标签 | 为实例vedbm-instanceid移除标签test |
| change_master | 切换主节点 | 切换实例主节点到vedbm-xxxx-1 |
| **网络和白名单管理工具** |
| create_vedb_mysql_allowlist | 为VeDB MySQL创建网络白名单 | 创建一个名为test_whitelist的IP白名单，允许IP地址192.168.1.0/24访问 |
| bind_allowlist_to_vedb_mysql_instances | 将网络白名单绑定到VeDB MySQL实例 | 将白名单绑定到指定实例 |
| list_bound_allow_lists | 查询实例绑定的白名单信息 | 查询实例vedbm-****当前绑定的所有白名单信息 |
| get_db_endpoint | 查询指定实例连接终端的详细信息 | 查询实例vedbm-****的所有连接终端详细信息 |
| create_db_endpoint | 创建连接终端 | 在实例中创建新的连接终端 |
| list_allow_lists | 查询所有IP白名单 | 查询北京地域下的所有白名单列表 |
| describe_allow_list_detail | 查询目标白名单的详细信息 | 查询白名单的详细信息和绑定实例 |
| **信息查询工具** |
| list_availability_zones | 查询当前地域下实例支持的可用区 | 查询北京地域下支持的所有可用区信息 |
| list_available_db_specs | 查询指定可用区支持的节点规格信息 | 查询北京地域下可用的所有veDB MySQL实例规格 |
| list_region_names | 查询实例可用的地域 | 查询veDB MySQL支持的所有地域列表 |

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
        "VOLCENGINE_ACCESS_KEY": "<your-access-key>",
        "VOLCENGINE_SECRET_KEY": "<your-secret-key>",
        "VOLCENGINE_REGION": "cn-beijing",
        "MCP_SERVER_PORT": "8000"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
