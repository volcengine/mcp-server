# veDB MySQL MCP Server
> 云数据库 veDB MySQL 版采用计算存储分离架构，100%兼容MySQL，最多支持 200TiB 的超大容量结构化数据存储，单个数据库集群最多可扩展至 16 个计算节点。支持实例管理、账号管理、数据库管理、备份恢复、白名单、数据迁移、数据同步、读写分离、安全审计、高可用、版本升级、备份恢复等关键特性。

---


| 项目 | 详情 |
| ---- | ---- |
| 描述 | 火山引擎 veDB MySQL 版即开即用、稳定可靠的关系型数据库服务 |
| 分类 | 数据库 |
| 标签 | MySQL, RDS, 关系型数据库, 数据库 |

---

## Tools

### 1. `create_vedb_mysql_instance`
- **详细描述**：创建一个新实例
- **触发示例**：`"创建一个新的vedbm实例，参数参考我的其他实例。并告诉我mysql连接串"`

### 2. `list_vedb_mysql_instances`
- **详细描述**：获取用户的veDB MySQL实例列表，包括实例ID，以及实例的基本信息
- **触发示例**：`"列出我的vedbm实例"`

### 3. `describe_vedb_mysql_detail`
- **详细描述**：获取指定实例的实例详情
- **触发示例**：`"查看实例ID为vedbm-hylviolixpvu的详细信息"`

### 4. `list_vedb_mysql_instance_databases`
- **详细描述**：获取指定实例中数据库列表，包括数据库的权限信息
- **触发示例**：`"查看实例vedbm-hylviolixpvu实例中的数据库列表"`

### 5. `list_vedb_mysql_instance_accounts`
- **详细描述**：获取指定实例中账号信息，包括账号的权限详情
- **触发示例**：`"查看实例vedbm-hylviolixpvu实例中的账号列表"`

### 6. `modify_vedb_mysql_instance_alias`
- **详细描述**：更新指定实例的别名
- **触发示例**：`"将实例vedbm-hylviolixpvu的别名改为生产数据库"`

### 7. `create_vedb_mysql_allowlist`
- **详细描述**：创建一个veDB MySQL网络白名单
- **触发示例**：`"创建一个仅用于我的ECS实例的veDB MySQL网络白名单"`

### 8. `bind_allowlist_to_vedb_mysql_instances`
- **详细描述**：将veDB MySQL网络白名单绑定到实例
- **触发示例**：`"绑定上一步创建的白名单 到我的veDB MySQL实例上"`

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
