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

### 1. `create_vedb_mysql_instance`
- **Description**: Creates a new instance.
- **Trigger example**: `"Create a new vedbm instance using the parameters of my other instance as reference, and tell me the MySQL connection string."`

### 2. `list_vedb_mysql_instances`
- **Description**: Retrieves the list of a user’s veDB MySQL instances, including each instance ID and basic information.
- **Trigger example**: `"List my vedbm instances."`

### 3. `describe_vedb_mysql_detail`
- **Description**: Gets detailed information about a specified instance.
- **Trigger example**: `"Show the details of instance ID vedbm-hylviolixpvu."`

### 4. `list_vedb_mysql_instance_databases`
- **Description**: Retrieves the list of databases within a specified instance, including permission information.
- **Trigger example**: `"Show the database list in instance vedbm-hylviolixpvu."`

### 5. `list_vedb_mysql_instance_accounts`
- **Description**: Retrieves account information within a specified instance, including permission details.
- **Trigger example**: `"Show the account list in instance vedbm-hylviolixpvu."`

### 6. `modify_vedb_mysql_instance_alias`
- **Description**: Updates the alias of a specified instance.
- **Trigger example**: `"Change the alias of instance vedbm-hylviolixpvu to Production Database."`

### 7. `create_vedb_mysql_allowlist`
- **Description**: Creates a veDB MySQL network allowlist (whitelist).
- **Trigger example**: `"Create a veDB MySQL network allowlist only for my ECS instances."`

### 8. `bind_allowlist_to_vedb_mysql_instances`
- **Description**: Binds a veDB MySQL network allowlist to one or more instances.
- **Trigger example**: `"Bind the allowlist created in the previous step to my veDB MySQL instance."`

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
