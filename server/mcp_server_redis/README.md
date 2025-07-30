# Redis MCP Server
> Volcengine Redis is a fully managed in-memory caching service provided by Volcengine that is fully compatible with open-source Redis. It supports key features such as instance management, account and permission management, connection management, parameter configuration, backup and restore, monitoring and alerting, log analysis, data security, high availability, and scalability.

---

| Item | Details                                                                                   |
| ---- |-------------------------------------------------------------------------------------------|
| Version | v1.0.0                                                                                    |
| Description | Volcengine Redis is a fully managed, high-performance in-memory database service that is compatible with open-source Redis. |
| Category | Database                                                                                  |
| Tags | Redis, NoSQL, Cache, KV Database, Database                                                |

---

## Available Tools

### 1. `describe_regions`
- **Detailed Description**: Query the list of available regional resources for Redis Database.
- **Trigger Example**: `View the list of currently available Redis regions`

### 2. `describe_zones`
- **Detailed Description**: Query the list of available zone resources for Redis Database in a specified region.
- **Trigger Example**: `"Query the list of available zones under region cn-beijing"`

### 3. `describe_vpcs`
- **Detailed Description**: Query VPCs that meet specified conditions.
- **Trigger Example**: `"Query the VPC list under the current account, display up to 10"`

### 4. `describe_subnets`
- **Detailed Description**: Query subnets that meet specified conditions.
- **Trigger Example**: `"View subnet information under VPC ID vpc-rs22ruc4sgzkvxxxxxxxxxx"`

### 5. `describe_db_instances`
- **Detailed Description**: View the user's Redis instance list, supports pagination query.
- **Trigger Example**: `"List my 5 most recently created Redis instances"`

### 6. `describe_db_instance_detail`
- **Detailed Description**: View instance details based on specified Redis instance ID.
- **Trigger Example**: `"View detailed information for instance ID redis-cnlf57snuxxxxxxxx"`

### 7. `describe_db_instance_specs`
- **Detailed Description**: Query the list of instance specifications supported by Redis.
- **Trigger Example**: `"View the instance specifications table supported by Redis"`

### 8. `describe_slow_logs`
- **Detailed Description**: Query slow log details of the target Redis instance within specified time.
- **Trigger Example**: `"View slow log information for instance redis-cnlf57snuxxxxxxxx in the last half hour"`

### 9. `describe_hot_keys`
- **Detailed Description**: Query hot key details of the target Redis instance within specified time period.
- **Trigger Example**: `"View hot key information for instance redis-cnlf57snuxxxxxxxx in the last half hour"`

### 10. `describe_big_keys`
- **Detailed Description**: Query big key details of the target Redis instance within specified time period.
- **Trigger Example**: `"View big key information for instance redis-cnlf57snuxxxxxxxx in the last half hour"`

### 11. `describe_backups`
- **Detailed Description**: Query the backup set list of the target Redis instance.
- **Trigger Example**: `"View backup information for instance redis-cnlf57snuxxxxxxxx"`

### 12. `describe_db_instance_params`
- **Detailed Description**: Query the list of parameters supported by the target Redis instance.
- **Trigger Example**: `"View parameter list for instance redis-cnlf57snuxxxxxxxx"`

### 13. `describe_parameter_groups`
- **Detailed Description**: Query basic information of parameter templates under current account and region.
- **Trigger Example**: `"View available parameter templates"`

### 14. `describe_parameter_group_detail`
- **Detailed Description**: Query detailed information of the target parameter list.
- **Trigger Example**: `"Detailed information of parameter template DefaultParamGroupId-5.0"`

### 15. `describe_allow_lists`
- **Detailed Description**: Query the IP whitelist in specified region under current account.
- **Trigger Example**: `"View my whitelist"`

### 16. `describe_allow_list_detail`
- **Detailed Description**: Query detailed information of target whitelist, including IP addresses and bound instance details.
- **Trigger Example**: `"View detailed information of whitelist acl-cnlf114hwh3qtxxxxxx"`

### 17. `list_db_account`
- **Detailed Description**: Query account information in Redis instance, including account name, role, etc.
- **Trigger Example**: `"Help me check the account information for instance redis-cnlf57snuxxxxxxxx"`

### 18. `create_db_instance`
- **Detailed Description**: Create Redis instance.
- **Trigger Example**: `"Help me create a 1GB master-slave instance named redis-mcp-server in cn-beijing region"`

### 19. `modify_db_instance_params`
- **Detailed Description**: Modify parameter configuration of target Redis instance.
- **Trigger Example**: `"Turn on the AOF switch for instance redis-cnlf57snuxxxxxxxx"`

### 20. `create_db_account`
- **Detailed Description**: Create account for target Redis instance.
- **Trigger Example**: `"Create an account named mcptest for instance redis-cnlf57snuxxxxxxxx with read-write permissions"`

### 21. `create_allow_list`
- **Detailed Description**: Create a new IP whitelist.
- **Trigger Example**: `"Create a whitelist named mcptest with network segments 127.0.0.1,192.168.1.0/24"`

### 22. `associate_allow_list`
- **Detailed Description**: Bind target Redis instance to specified IP whitelist.
- **Trigger Example**: `"Associate whitelist acl-cnlf61xhhfrgxxxxx with single instance redis-cnlf57snuxxxxxxxx"`

### 23. `disassociate_allow_list`
- **Detailed Description**: Create a new IP whitelist.
- **Trigger Example**: `"Unbind instance redis-cnlf57snuxxxxxxxx from whitelist acl-cnlf61xhhfrgxxxxx"`

---

## Service Activation Link
[Click to go to the Volcengine Redis service activation page](https://console.volcengine.com/db/redis)

---

## Authentication Method
Obtain the access key ID, secret access key, and region from the Volcengine Management Console, and use API Key authentication. 
You need to set `VOLCENGINE_ACCESS_KEY` and `VOLCENGINE_SECRET_KEY` in the configuration file.

---

## Deployment
Volcengine Redis service access address: https://www.volcengine.com/docs/6293/65743
```json
{
  "mcpServers": {
    "redis": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_redis",
        "mcp-server-redis"
      ],
      "env": {
        "VOLCENGINE_REGION": "Volcengine resource region",
        "VOLCENGINE_ACCESS_KEY": "Volcengine account ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY": "Volcengine account SECRET_KEY"
      }
    }
  }
}
```
Currently, the supported regions: ["cn-beijing", "cn-guangzhou", "cn-shanghai", "cn-hongkong", "ap-southeast-1", "ap-southeast-3"]

## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).