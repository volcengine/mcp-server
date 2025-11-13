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


### Instance Management

| Tool Name | Description |
|-----------|-------------|
| `list_vedb_mysql_instances` | Retrieve a list of all VeDB MySQL instances for the user, including instance IDs and basic information |
| `describe_vedb_mysql_detail` | Retrieve detailed information about a specific VeDB MySQL instance |
| `modify_vedb_mysql_instance_alias` | Modify a specific VeDB MySQL instance's alias |
| `create_vedb_mysql_instance` | Create a VeDB MySQL instance |
| `switch_instance_deletion_protection` | Enable or disable instance deletion protection |
| `describe_db_instance_version` | Query the version of the target instance |
| `add_tags_to_resource` | Bind tags to one or more instances |
| `remove_tags_from_resource` | Unbind tags from one or more instances |
| `modify_db_instance_spec` | Modify node configuration of the specified instance |
| `restart_db_instance` | Restart the instance |
| `change_master` | Switch the primary node |
| `delete_db_instance` | Delete the instance |
| `modify_db_node_config` | Set the priority of a specified node to be elected as primary during failover |

### Database and Account Management

| Tool Name | Description |
|-----------|-------------|
| `list_vedb_mysql_instance_databases` | Retrieve a list of databases created in a specific VeDB MySQL instance, including privilege information |
| `list_vedb_mysql_instance_accounts` | Obtain a list of accounts in a single VeDB MySQL instance, with their privilege details |
| `modify_db_account_description` | Modify the description information of a mysqld account |
| `modify_database_description` | Modify the description information of a mysqld database |
| `reset_account_priv` | Reset high-privilege account permissions to initial state |
| `revoke_db_account_privilege` | Revoke database privileges from an account |
| `grant_db_account_privilege` | Grant database privileges to an account |
| `reset_account_passwd` | Modify database account password |
| `create_db_account` | Create database management account |
| `create_database` | Create database for the instance |
| `delete_db_account` | Delete database account |
| `delete_database` | Delete database from the instance |

### Backup and Recovery

| Tool Name | Description |
|-----------|-------------|
| `restore_table` | Restore historical databases and tables to the original instance |
| `modify_backup_policy` | Modify data backup policy for the specified instance |
| `restore_to_new_instance` | Restore backup data from an existing instance to a new instance |
| `create_backup` | Create data backup for the specified instance |
| `delete_backup` | Delete manually created backup files for the specified instance |
| `describe_backup_policy` | Query data backup policy for the specified instance |
| `describe_backups` | Query backup file list information for the specified instance |
| `describe_recoverable_time` | Query the recoverable time range for instance backups |

### Connection Endpoint Management

| Tool Name | Description |
|-----------|-------------|
| `modify_db_endpoint_address` | Modify connection address port or prefix |
| `modify_db_endpoint_dns` | Modify resolution method of private network addresses |
| `describe_db_endpoint` | Query detailed information of specified instance connection endpoints |
| `delete_db_endpoint` | Delete connection endpoint |
| `create_db_endpoint` | Create connection endpoint |
| `modify_db_endpoint` | Modify connection endpoint |
| `create_db_endpoint_public_address` | Create public network connection address for the specified instance, enabling public network access |
| `delete_db_endpoint_public_address` | Delete public network connection address for the specified instance, disabling public network access |

### Task and Event Management

| Tool Name | Description |
|-----------|-------------|
| `cancel_schedule_events` | Cancel pending scheduled events |
| `describe_schedule_events` | View scheduled events under the current account |
| `modify_schedule_events` | Modify execution time of pending events |
| `modify_db_instance_maintenance_window` | Modify the maintenance window of the instance |

### Parameter Management

| Tool Name | Description |
|-----------|-------------|
| `save_as_parameter_template` | Save parameter configuration of specified instance as a parameter template |
| `create_parameter_template` | Create parameter template |
| `apply_parameter_template` | Apply parameter template |
| `describe_parameter_templates` | Query parameter template list |
| `list_parameter_change_history` | Query instance parameter modification history |
| `delete_parameter_template` | Delete parameter template |
| `describe_parameter_template_detail` | Query parameter template details |
| `describe_db_instance_parameters` | Query parameter list of target instance |
| `modify_db_instance_parameters` | Modify mysqld data plane parameters of the instance |
| `describe_modifiable_parameters` | Query list of modifiable parameters |

### Information Query

| Tool Name | Description |
|-----------|-------------|
| `create_vedb_mysql_allowlist` | Create a Network AllowList for VeDB MySQL |
| `bind_allowlist_to_vedb_mysql_instances` | Bind a Network AllowList to VeDB MySQL instances |
| `describe_instance_allow_lists` | Query allowlist information bound to the instance |
| `modify_allow_list` | Modify target allowlist settings, such as allowlist name, IP allowlist addresses, etc. |
| `describe_allow_list_detail` | Query detailed information of target allowlist, such as IP addresses and bound instance details |
| `delete_allow_list` | Delete target allowlist |
| `describe_allow_lists` | Query all IP allowlist information in the specified region under the current account |
| `disassociate_allow_list` | Unbind target instance from specified IP allowlist |
| `describe_storage_payable_price` | Query storage pricing |
| `describe_availability_zones` | Query available zone resources supported by instances in the current region |
| `describe_db_instance_specs` | Query node specifications supported in the specified availability zone |
| `describe_db_instance_price_detail` | Query price details for specified configuration instances |
| `describe_regions` | Query available region resources for instances |

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
