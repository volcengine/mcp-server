# RDS PostgreSQL MCP Server
> Volcengine RDS PostgreSQL is a relational database service provided by Volcengine that is fully compatible with open - source PostgreSQL. It supports key features such as instance management, database management, account management, Schema management, connection management, parameter management, backup and recovery, log management, event management, and data security.

---

| Item | Details |
| ---- | ---- |
| Version | v1.0.0 |
| Description | Volcengine RDS PostgreSQL is a ready - to - use and reliable relational database service. |
| Category | Database |
| Tags | PostgreSQL, RDS, Relational Database, Database |

---

## Tools

### 1. `describe_db_instances`
- **Detailed Description**: View the list of a user's RDS PostgreSQL instances, supporting pagination queries.
- **Trigger Example**: `"List my RDS PostgreSQL instances"`

### 2. `describe_db_instance_detail`
- **Detailed Description**: View the details of a specified RDS PostgreSQL instance by its ID.
- **Trigger Example**: `"View the details of the instance with ID postgres-123456"`

### 3. `describe_databases`
- **Detailed Description**: Get the list of databases for a specified RDS PostgreSQL instance.
- **Trigger Example**: `"Get the database list of the postgres-123456 instance"`

### 4. `describe_db_accounts`
- **Detailed Description**: Get the list of accounts for a specified RDS PostgreSQL instance.
- **Trigger Example**: `"Get the account list of the postgres-123456 instance"`

### 5. `describe_schemas`
- **Detailed Description**: Get the list of schemas for a specified RDS PostgreSQL instance.
- **Trigger Example**: `"Get the schema list of the postgres-123456 instance"`

### 6. `describe_db_instance_parameters`
- **Detailed Description**: Get the list of parameters for a specified RDS PostgreSQL instance.
- **Trigger Example**: `"Get the parameter list of the postgres-123456 instance"`

### 7. `describe_allow_lists`
- **Detailed Description**: Get the list of allow lists in a specified region for RDS PostgreSQL.
- **Trigger Example**: `"Get the allow list in the cn-beijing region"`

### 8. `describe_allow_list_detail`
- **Detailed Description**: Get the details of an RDS PostgreSQL allow list.
- **Trigger Example**: `"Get the details of the allow list acl-123456"`

### 9. `describe_backups`
- **Detailed Description**: Get the list of backups for a specified RDS PostgreSQL instance.
- **Trigger Example**: `"Get the backup list of the postgres-123456 instance"`

### 10. `describe_backup_policy`
- **Detailed Description**: Get the backup policy for a specified RDS PostgreSQL instance.
- **Trigger Example**: `"Get the backup policy of the postgres-123456 instance"`

### 11. `create_db_instance`
- **Detailed Description**: Create an RDS PostgreSQL instance.
- **Trigger Example**: `"Create an RDS PostgreSQL instance"`

### 12. `create_database`
- **Detailed Description**: Create an RDS PostgreSQL database.
- **Trigger Example**: `"Create a database named testdb in the postgres-123456 instance"`

### 13. `create_db_account`
- **Detailed Description**: Create an RDS PostgreSQL database account.
- **Trigger Example**: `"Create a database account named testuser in the postgres-123456 instance"`

### 14. `create_schema`
- **Detailed Description**: Create an RDS PostgreSQL database Schema.
- **Trigger Example**: `"Create a schema named testschema in the testdb database of the postgres-123456 instance"`

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