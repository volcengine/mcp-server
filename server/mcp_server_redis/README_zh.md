# Redis MCP Server
> 火山引擎 Redis 是由火山引擎提供的全托管内存缓存服务，兼容开源 Redis。它支持实例管理、账号和权限管理、连接管理、参数配置、备份恢复、监控告警、日志分析、数据安全、高可用性和可扩展性等关键功能。

---


| 项目 | 详情                                      |
| ---- |-----------------------------------------|
| 版本 | v1.0.0                                  |
| 描述 | 火山引擎 Redis 是一款全托管的高性能内存数据库服务，兼容开源 Redis |
| 分类 | 数据库                                     |
| 标签 | Redis, NoSQL, 非关系型数据库, 缓存数据库，KV键值数据库    |

---

## 支持的Tools

### 1. `describe_regions`
- **详细描述**：查询缓存数据库 Redis 版可用的地域资源列表。
- **触发示例**：`查看当前redis可用的region列表表`

### 2. `describe_zones`
- **详细描述**：查询缓存数据库 Redis 版在指定地域下的可用区资源列表。
- **触发示例**：`"查询region cn-beijing下的可用区列表"`

### 3. `describe_vpcs`
- **详细描述**：查询满足指定条件的VPC。
- **触发示例**：`"查询当前账号下的vpc列表，最多展示10个"`

### 4. `describe_subnets`
- **详细描述**：查询满足指定条件的子网。
- **触发示例**：`"查看vpc id vpc-rs22ruc4sgzkvxxxxxxxxxx 下的子网网段信息"`

### 5. `describe_db_instances`
- **详细描述**：查看用户的 Redis 实例列表，支持分页查询。
- **触发示例**：`"列出我最近创建的5个redis实例"`

### 6. `describe_db_instance_detail`
- **详细描述**：根据指定 Redis 实例 ID 查看实例详情。
- **触发示例**：`"查看实例ID 为 redis-cnlf57snuxxxxxxxx 的详细信息"`

### 7. `describe_db_instance_specs`
- **详细描述**：查询 Redis 支持的实例规格列表。
- **触发示例**：`"查看redis支持的实例规格表"`

### 8. `describe_slow_logs`
- **详细描述**：查询目标 Redis 实例在指定时间内的慢日志详情。
- **触发示例**：`"查看实例 redis-cnlf57snuxxxxxxxx 半个小时内的慢日志信息"`

### 9. `describe_hot_keys`
- **详细描述**：查询目标 Redis 实例在指定时间段内的热 Key 详情。
- **触发示例**：`"查看实例 redis-cnlf57snuxxxxxxxx 半个小时内的热Key信息"`

### 10. `describe_big_keys`
- **详细描述**：查询目标 Redis 实例在指定时间段内的大 Key 详情。
- **触发示例**：`"查看实例 redis-cnlf57snuxxxxxxxx 半个小时内的大Key信息"`

### 11. `describe_backups`
- **详细描述**：查询目标 Redis 实例的备份集列表。
- **触发示例**：`"查看实例 redis-cnlf57snuxxxxxxxx 的备份信息"`

### 12. `describe_db_instance_params`
- **详细描述**：查询目标 Redis 实例支持的参数列表。
- **触发示例**：`"查看实例 redis-cnlf57snu3tt8vyja 的参数列表"`

### 13. `describe_parameter_groups`
- **详细描述**：查询当前账号和地域下的参数模板的基本信息。
- **触发示例**：`"查看有哪些可用的参数模板"`

### 14. `describe_parameter_group_detail`
- **详细描述**：查询目标参数列表的详细信息。
- **触发示例**：`"参数模板 DefaultParamGroupId-5.0 的详细信息"`

### 15. `describe_allow_lists`
- **详细描述**：查询当前账号下在指定地域的 IP 白名单列表。
- **触发示例**：`"查看我的白名单列表"`

### 16. `describe_allow_list_detail`
- **详细描述**：查询目标白名单的详细信息，包括 IP 地址和绑定的实例详情。
- **触发示例**：`"查看白名单 acl-cnlf114hwh3qtxxxxxx 的详细信息"`

### 17. `list_db_account`
- **详细描述**：查询 Redis 实例中的账号信息，包括账号名称、账号角色等。
- **触发示例**：`"帮我查看下实例 redis-cnlf57snuxxxxxxxx 的账号信息"`

### 18. `create_db_instance`
- **详细描述**：创建 Redis 实例。
- **触发示例**：`"帮我在cn-beijing region创建一个名字为redis-mcp-server的1GB的主备实例"`

### 19. `modify_db_instance_params`
- **详细描述**：修改目标 Redis 实例的参数配置。
- **触发示例**：`"打开实例 redis-cnlf57snuxxxxxxxx 的aof开关"`

### 20. `create_db_account`
- **详细描述**：为目标 Redis 实例创建账号。
- **触发示例**：`"为实例 redis-cnlf57snuxxxxxxxx创建一个名为mcptest的账号，并授予读写权限"`

### 21. `create_allow_list`
- **详细描述**：创建一个新的 IP 白名单。
- **触发示例**：`"创建一个名为mcptest的白名单，网段为127.0.0.1,192.168.1.0/24"`

### 22. `associate_allow_list`
- **详细描述**：将目标 Redis 实例绑定到指定 IP 白名单。
- **触发示例**：`"将白名单 acl-cnlf61xhhfrgxxxxx 关联单实例redis-cnlf57snuxxxxxxxx"`

### 23. `disassociate_allow_list`
- **详细描述**：创建一个新的 IP 白名单。
- **触发示例**：`"将实例redis-cnlf57snuxxxxxxxx从白名单 acl-cnlf61xhhfrgxxxxx 解绑"`

---

## 服务开通链接
[点击前往火山引擎 Redis 服务开通页面](https://console.volcengine.com/db/redis)

---

## 鉴权方式
在火山引擎管理控制台获取访问密钥 ID、秘密访问密钥和区域，采用 API Key 鉴权。
需要在配置文件中设置 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY`。

---

## 部署
火山引擎Redis 服务接入地址：https://www.volcengine.com/docs/6293/65743
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
      "--transport": "stdio",
      "env": {
        "VOLCENGINE_REGION": "火山引擎资源region",
        "VOLCENGINE_ACCESS_KEY": "火山引擎账号ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY": "火山引擎账号SECRET_KEY",
        "MCP_SERVER_PORT": "MCP server监听端口"
      }
    }
  }
}
```
当前支持的Region: ["cn-beijing", "cn-guangzhou", "cn-shanghai", "cn-hongkong", "ap-southeast-1", "ap-southeast-3"]

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).


