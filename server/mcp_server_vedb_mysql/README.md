# veDB MySQL MCP Server
> The veDB MySQL cloud database adopts a compute-storage–separated architecture, is 100 % MySQL-compatible, and supports up to 200 TiB of large-scale structured data storage. A single cluster can scale out to as many as 16 compute nodes. Key features include instance management, account management, database management, backup and restore, allowlist, data migration, data synchronization, read/write splitting, security auditing, high availability, version upgrades, and backup & recovery.

[中文介绍](README_zh.md)

---
| Item | Details |
| ---- | ---- |
| Description | Volcano Engine veDB MySQL is an out-of-the-box, stable and reliable relational database service |
| Category | Database |
| Tags | MySQL, RDS, Relational Database, Database |

---

## Tools

| Tool Name | Description | Trigger Example |
|----------|-------------|---------------|
| **Parameter Management Tools** | |
| `save_as_parameter_template` | Save parameter configuration of specified instance as a parameter template | Save current parameter configuration of instance vedbm-**** as a new parameter template named custom_template |
| `create_parameter_template` | Create parameter template | Create a MySQL 8.0 parameter template named new_template containing parameter max_connections=1000 |
| `list_parameter_templates` | Query parameter template list | Query all parameter templates for MySQL 8.0 version |
| `describe_parameter_template_detail` | Query parameter template details | Query detailed configuration of parameter template vedbmpt-**** |
| `describe_db_parameters` | Query MySQL parameter list of the instance | Query all kernel parameters of instance vedbm-instanceid |
| **Database and Account Management Tools** | |
| `list_vedb_mysql_instance_databases` | Retrieve list of databases created in a specific VeDB MySQL instance, including privilege information | Query all database lists and privilege details in the instance |
| `list_vedb_mysql_instance_accounts` | Retrieve list of accounts in a single VeDB MySQL instance with their privilege details | Query all account lists and privilege details in the instance |
| `modify_db_account_description` | Modify description information of a MySQL account within the instance | Modify description of account user1 to "development account" under vedbm-instanceid |
| `modify_database_description` | Modify description information of a MySQL database within the instance | Modify description of database test_db to "test database" under vedbm-instanceid |
| `create_db_account` | Create MySQL account within the instance | Create new ordinary account test_mcp with password Password123 in instance vedbm-instanceid |
| `create_database` | Create MySQL database within the instance | Create database test_db under vedbm-instanceid |
| **Backup and Recovery Tools** | |
| `restore_to_new_instance` | Restore backup data from existing instance to a new instance | Create a new instance using backup data from instance vedbm-**** (backup ID: snap-**-**), specification: vedb.mysql.x4.large, node count: 2, VPC and subnet same as original instance |
| `create_backup` | Create data backup for specified instance | Create a manual full backup for instance vedbm-instanceid |
| `get_backup_policy` | Query data backup policy for specified instance | Query current data backup policy of instance vedbm-**** |
| `list_backups` | Query backup list for specified instance | Query all successfully completed snapshots of instance vedbm-instanceid |
| `get_recoverable_time` | Query recoverable time range for instance backups | Query recoverable time range for instance vedbm-instanceid |
| **Instance Management Tools** | |
| `list_vedb_mysql_instances` | Retrieve list of all VeDB MySQL instances for the user, including instance IDs and basic information | Query all instance lists |
| `describe_vedb_mysql_detail` | Retrieve detailed information about a specific VeDB MySQL instance | Query detailed information of specified instance |
| `modify_vedb_mysql_instance_alias` | Modify alias of a specific VeDB MySQL instance | Modify instance alias |
| `create_vedb_mysql_instance` | Create VeDB MySQL instance | Create new database instance |
| `add_tags_to_resource` | Bind tags to one or more instances | Add tag test=mcp to instance vedbm-instanceid |
| `remove_tags_from_resource` | Unbind tags from one or more instances | Remove tag test from instance vedbm-instanceid |
| `change_master` | Switch primary node | Switch instance primary node to vedbm-xxxx-1 |
| **Network and Allowlist Management Tools** | |
| `create_vedb_mysql_allowlist` | Create network allowlist for VeDB MySQL | Create an IP allowlist named test_whitelist allowing IP address 192.168.1.0/24 to access |
| `bind_allowlist_to_vedb_mysql_instances` | Bind network allowlist to VeDB MySQL instances | Bind allowlist to specified instance |
| `list_bound_allow_lists` | Query allowlist information bound to the instance | Query all currently bound allowlist information for instance vedbm-**** |
| `get_db_endpoint` | Query detailed information of specified instance connection endpoints | Query all connection endpoint details for instance vedbm-**** |
| `create_db_endpoint` | Create connection endpoint | Create new connection endpoint in the instance |
| `list_allow_lists` | Query all IP allowlists | Query all allowlist lists in Beijing region |
| `describe_allow_list_detail` | Query detailed information of target allowlist | Query detailed information and bound instances of the allowlist |
| **Information Query Tools** | |
| `list_availability_zones` | Query availability zones supported by instances in current region | Query all availability zone information supported in Beijing region |
| `list_available_db_specs` | Query node specification information supported in specified availability zone | Query all available VeDB MySQL instance specifications in Beijing region |
| `list_region_names` | Query regions available for instances | Query all region lists supported by VeDB MySQL |

---

## Service Activation Link
[Click here to open the Volcano Engine veDB MySQL service page](https://console.volcengine.com/db/vedb-mysql)

---

## Authentication
Obtain your Access Key ID, Secret Access Key, and Region from the Volcano Engine console, and use API Key authentication.  
Set the following variables in your configuration file:

```
VOLCENGINE_ACCESS_KEY  = <Your Access Key ID>
VOLCENGINE_SECRET_KEY  = <Your Secret Access Key>
```

## Deploy
Volcano Engine veDB MySQL service access address: <https://www.volcengine.com/docs/6357/66583>
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
