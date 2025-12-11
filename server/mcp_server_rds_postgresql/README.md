# RDS PostgreSQL MCP Server
> Volcengine RDS PostgreSQL is a relational database service provided by Volcengine that is fully compatible with open - source PostgreSQL. It supports key features such as instance management, database management, account management, Schema management, connection management, parameter management, backup and recovery, log management, event management, and data security.

---

| Item | Details                                                                                   |
| ---- |-------------------------------------------------------------------------------------------|
| Version | v1.1.0                                                                                    |
| Description | Volcengine RDS PostgreSQL is a ready - to - use and reliable relational database service. |
| Category | Database                                                                                  |
| Tags | PostgreSQL, RDS, Relational Database, Database                                            |

---

## Tools

### 1. `describe_wal_log_backups`
- **Detailed Description**: Call the DescribeWALLogBackups API to get the list of WAL log backups for a specified instance.
- **Trigger Example**: `Get the WAL log backup list for instance postgres-123456`


### 2. `describe_db_instance_ssl`
- **Detailed Description**: Call the DescribeDBInstanceSSL API to query the SSL settings of a specified instance.
- **Trigger Example**: `Query the SSL configuration of instance postgres-123456`


### 3. `describe_tasks`
- **Detailed Description**: Call the DescribeTasks API to query tasks.
- **Trigger Example**: `View the recent tasks of instance postgres-123456`


### 4. `describe_db_engine_version_parameters`
- **Detailed Description**: Call the DescribeDBEngineVersionParameters API to query the list of parameters that can be set by users for a specified database engine version.
- **Trigger Example**: `Query the list of parameters supported by PostgreSQL 14`


### 5. `describe_planned_events`
- **Detailed Description**: Call the DescribePlannedEvents API to query maintenance events in the current region.
- **Trigger Example**: `View the database maintenance events in the current region`


### 6. `get_backup_download_link`
- **Detailed Description**: Call the GetBackupDownloadLink API to obtain the download link for a backup.
- **Trigger Example**: `Get the download link for backup ID backup-789012`


### 7. `clone_database`
- **Detailed Description**: Call the CloneDatabase API to clone an existing database.
- **Trigger Example**: `Clone the mydb database in instance postgres-123456`


### 8. `describe_slots`
- **Detailed Description**: Call the DescribeSlots API to query the replication slot list.
- **Trigger Example**: `Query replication slot information for instance postgres-123456`


### 9. `describe_allow_list_detail`
- **Detailed Description**: Call the DescribeAllowListDetail API to view the allowlist details.
- **Trigger Example**: `View the details of allowlist with ID allowlist-345678`


### 10. `describe_allow_lists`
- **Detailed Description**: Call the DescribeAllowLists API to view the allowlist list in the specified region.
- **Trigger Example**: `List all allowlists in the current region`


### 11. `revoke_db_account_privilege`
- **Detailed Description**: Call the RevokeDBAccountPrivilege API to revoke all privileges from a database account.
- **Trigger Example**: `Revoke all privileges from account user1 in instance postgres-123456`


### 12. `modify_db_endpoint_name`
- **Detailed Description**: Call the ModifyDBEndpointName API to modify the connection endpoint name.
- **Trigger Example**: `Rename the connection endpoint endpoint-789012 of instance postgres-123456 to main-endpoint`


### 13. `describe_detached_backups`
- **Detailed Description**: Call the DescribeDetachedBackups API to query backups of deleted instances.
- **Trigger Example**: `Query the backup list of deleted instances`


### 14. `describe_backup_policy`
- **Detailed Description**: Call the DescribeBackupPolicy API to query the backup policy.
- **Trigger Example**: `View the backup policy of instance postgres-123456`


### 15. `describe_backups`
- **Detailed Description**: Call the DescribeBackups API to query the backup list.
- **Trigger Example**: `List all backups for instance postgres-123456`


### 16. `modify_db_instance_name`
- **Detailed Description**: Call the ModifyDBInstanceName API to modify the instance name.
- **Trigger Example**: `Rename instance postgres-123456 to my-postgres-instance`


### 17. `describe_db_instance_parameters`
- **Detailed Description**: Call the DescribeDBInstanceParameters API to query the instance parameter configuration.
- **Trigger Example**: `View the current parameter configuration of instance postgres-123456`


### 18. `modify_db_instance_parameters`
- **Detailed Description**: Call the ModifyDBInstanceParameters API to modify instance parameters.
- **Trigger Example**: `Modify the max_connections parameter of instance postgres-123456 to 500`


### 19. `modify_db_instance_charge_type`
- **Detailed Description**: Call the ModifyDBInstanceChargeType API to modify the instance billing type.
- **Trigger Example**: `Change the billing type of instance postgres-123456 to monthly subscription`


### 20. `describe_db_instance_price_difference`
- **Detailed Description**: Call the DescribeDBInstancePriceDifference API to query the price difference for instance. 
- **Trigger Example**: `Query the price difference for upgrading the specification of instance postgres-123456`


### 21. `modify_db_endpoint_dns`
- **Detailed Description**: Call the ModifyDBEndpointDNS API to modify the resolution method of the private network address for the instance.
- **Trigger Example**: `Modify the private network DNS resolution method of instance postgres-123456`


### 22. `remove_tags_from_resource`
- **Detailed Description**: Call the RemoveTagsFromResource API to unbind tags from the instance.
- **Trigger Example**: `Unbind the tag env=test from instance postgres-123456`


### 23. `add_tags_to_resource`
- **Detailed Description**: Call the AddTagsToResource API to bind tags to the instance.
- **Trigger Example**: `Add the tag env=prod to instance postgres-123456`


### 24. `describe_db_instance_price_detail`
- **Detailed Description**: Call the DescribeDBInstancePriceDetail API to query the detailed price for instance.
- **Trigger Example**: `Query the detailed price for creating a PostgreSQL instance`


### 25. `create_db_endpoint`
- **Detailed Description**: Call the CreateDBEndpoint API to create a connection endpoint for the specified instance.
- **Trigger Example**: `Create a new connection endpoint for instance postgres-123456`


### 26. `describe_db_instance_detail`
- **Detailed Description**: Call the DescribeDBInstanceDetail API to query detailed information about the instance.
- **Trigger Example**: `View detailed information for instance postgres-123456`


### 27. `modify_db_instance_spec`
- **Detailed Description**: Call the ModifyDBInstanceSpec API to modify the instance configuration.
- **Trigger Example**: `Upgrade the specification of instance postgres-123456 to 4 cores 16G`


### 28. `restore_to_new_instance`
- **Detailed Description**: Call the RestoreToNewInstance API to restore to a new instance.
- **Trigger Example**: `Restore from backup backup-789012 to a new instance`


### 29. `create_db_instance`
- **Detailed Description**: Call the CreateDBInstance API to create an instance.
- **Trigger Example**: `Create a PostgreSQL 14 version instance`


### 30. `describe_db_instances`
- **Detailed Description**: Call the DescribeDBInstances API to query the instance list.
- **Trigger Example**: `List all PostgreSQL instances in the current region`


### 31. `describe_db_instance_specs`
- **Detailed Description**: Call the DescribeDBInstanceSpecs API to query the available instance specifications for sale.
- **Trigger Example**: `Query available PostgreSQL instance specifications`


### 32. `describe_recoverable_time`
- **Detailed Description**: Call the DescribeRecoverableTime API to query the recoverable time range for instance backups.
- **Trigger Example**: `Query the recoverable time range for instance postgres-123456`


### 33. `modify_db_endpoint_address`
- **Detailed Description**: Call the ModifyDBEndpointAddress API to modify the port and prefix of the private network connection address for the instance.
- **Trigger Example**: `Modify the private network connection port of instance postgres-123456 to 5433`


### 34. `describe_failover_logs`
- **Detailed Description**: Call the DescribeFailoverLogs API to query the primary-standby switchover logs for the instance.
- **Trigger Example**: `View the primary-standby switchover history for instance postgres-123456`


### 35. `reset_db_account`
- **Detailed Description**: Call the ResetDBAccount API to reset the password of the account.
- **Trigger Example**: `Reset the password for account user1 in instance postgres-123456`


### 36. `modify_db_account_privilege`
- **Detailed Description**: Call the ModifyDBAccountPrivilege API to modify the database account privileges.
- **Trigger Example**: `Add read-write privileges on database mydb to account user1 in instance postgres-123456`


### 37. `create_schema`
- **Detailed Description**: Call the CreateSchema API to create a Schema.
- **Trigger Example**: `Create schema1 in database mydb of instance postgres-123456`


### 38. `modify_schema_owner`
- **Detailed Description**: Call the ModifySchemaOwner API to modify the owner of a Schema.
- **Trigger Example**: `Change the owner of schema1 in database mydb of instance postgres-123456 to user2`


### 39. `describe_schemas`
- **Detailed Description**: Call the DescribeSchemas API to query the Schema list.
- **Trigger Example**: `List all schemas in database mydb of instance postgres-123456`


### 40. `modify_database_owner`
- **Detailed Description**: Call the ModifyDatabaseOwner API to modify the database Owner.
- **Trigger Example**: `Change the owner of database mydb in instance postgres-123456 to user2`


### 41. `create_database`
- **Detailed Description**: Call the CreateDatabase API to create a database.
- **Trigger Example**: `Create a new database newdb in instance postgres-123456`


### 42. `describe_databases`
- **Detailed Description**: Call the DescribeDatabases API to query the database list.
- **Trigger Example**: `List all databases in instance postgres-123456`


### 43. `create_db_account`
- **Detailed Description**: Call the CreateDBAccount API to create an account.
- **Trigger Example**: `Create a new account user3 in instance postgres-123456`


### 44. `describe_db_accounts`
- **Detailed Description**: Call the DescribeDBAccounts API to query the account list.
- **Trigger Example**: `List all accounts in instance postgres-123456`

---

## Service Activation Link
[Click to go to the Volcengine RDS PostgreSQL service activation page](https://console.volcengine.com/db/rds-pg)

---

## Authentication Method
Obtain the access key ID, secret access key, and region from the Volcengine Management Console, and use API Key authentication. You need to set `VOLCENGINE_ACCESS_KEY` and `VOLCENGINE_SECRET_KEY` in the configuration file.

---

## Deployment
Volcengine RDS PostgreSQL service access address: https://www.volcengine.com/docs/6438/69237
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
        "VOLCENGINE_ENDPOINT": "Volcengine endpoint",
        "VOLCENGINE_REGION": "Volcengine resource region",
        "VOLCENGINE_ACCESS_KEY": "Volcengine account ACCESSKEY",
        "VOLCENGINE_SECRET_KEY": "Volcengine account SECRETKEY",
        "MCP_SERVER_PORT": "MCP server listening port"
      }
    }
  }
}
```

## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).