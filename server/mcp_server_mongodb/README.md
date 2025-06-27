# Volc Mongo SDK MCP Server 
> 火山引擎 MongoDB 版是由火山引擎提供的完全兼容开源 MongoDB 数据库服务，支持实例管理、账号管理、数据库管理、备份恢复、白名单、透明数据加密、数据迁移、数据同步、读写分离、安全审计、高可用、版本升级、备份恢复等关键特性。
[https://www.volcengine.com/product/mongodb]


---

| 项目 | 详情                               |
| ---- |----------------------------------|
| 版本 | v1.0.0                           |
| 描述 | 火山引擎 MongoDB 版即开即用、稳定可靠的关系型数据库服务 |
| 分类 | 数据库                              |
| 标签 | MongoDB 关系型数据库, 数据库              |

---


## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### 1.describe_db_instances
- **详细描述**： 获取MongoDB实例列表和数量
### 2.describe_db_instance_detail
- **详细描述**： 返回MongoDB实例的详情信息
### 3.describe_backups_request
- **详细描述**： 获取MongoDB实例备份信息列表
### 4.describe_db_instance_parameters
- **详细描述**： 获取MongoDB实例参数列表
### 5.describe_slow_log
- **详细描述**： 获取MongoDB慢日志列表
### 6.describe_azs
- **详细描述**： 获取实例创建可用区
### 7.describe_allow_lists
- **详细描述**： 获取MongoDB实例白名单
### 8.describe_node_specs
- **详细描述**： 获取实例部署规格
### 9.create_db_instance
- **详细描述**： 创建mongoDB实例



## 可适配平台  
可以使用 cline, cursor, claude desktop 或支持MCP server调用的的其他终端


## 鉴权方式  
从 volcengine 管理控制台获取 volcengine 访问密钥 ID、秘密访问密钥和区域

## 安装部署  

### 系统依赖
- 安装 Python 3.10 或者更高版本
- 安装 uv 
  - 如果是linux系统 
  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  - 如果是window系统 
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- 同步依赖项并更uv.lock:
  ```bash
  uv sync
  ```
- 构建mcp server:
  ```bash
  uv build
  ```

### 使用 UVX

```json
{
    "mcpServers": {
        "mcp-server-mongodb": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_mongodb",
            "mcp-server-mongodb"
          ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your-access-key-id",
                "VOLCENGINE_SECRET_KEY": "your-access-key-secret",
                "VOLCENGINE_REGION": "VOLC_REGION"
            }
        }
    }
}
```

## 数据面 [MCP server](https://www.volcengine.com/mcp-marketplace/detail?name=MongoDB)

## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).


