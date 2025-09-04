# DBW MCP Server

> 火山引擎数据库工作台 (Database Workbench，简称DBW），是一款面向多类型数据库生命周期管理的统一云管平台。DBW是集数据库图形用户界面（GUI）、故障排查、审计于一体的数据库SaaS产品，提供全方位观测分析、智能风险检核和自治运维等web终端管理能力。为用户提供稳定、安全及高效的数据库管理云服务。

---


| 项目 | 详情             |
|----|----------------|
| 版本 | v1.0.0         |
| 描述 | 火山引擎数据库工作台 DBW |
| 分类 | 数据库            |
| 标签 | 数据库, 数据库生态工具   |

---

## Tools

### 1. `nl2sql`
- **详细描述**：根据自然语言问题生成SQL语句
- **触发示例**：`"查询所有用户的用户名"`

---

## 服务开通链接
[点击前往火山引擎 DBW 服务开通页面](https://console.volcengine.com/db/dbw)

---

## 鉴权方式
在火山引擎管理控制台获取访问密钥 ID、秘密访问密钥和区域，采用 API Key 鉴权。需要在环境变量中设置 `VOLCENGINE_ACCESS_KEY` 、 `VOLCENGINE_SECRET_KEY` 和 `VOLCENGINE_REGION`。

---

## 部署

火山引擎环境信息：https://www.volcengine.com/docs/6956/152603

### 系统依赖

- 安装 Python 3.10 或者更高版本
- 安装 uv

### 启动方式

需要在env环境变量中配置必选的 VOLCENGINE_REGION、VOLCENGINE_ACCESS_KEY、VOLCENGINE_SECRET_KEY 鉴权信息。

另外，DBW MCP Server还支持在环境变量中配置可选的 VOLCENGINE_INSTANCE_ID、VOLCENGINE_INSTANCE_TYPE 和 VOLCENGINE_DATABASE，从而允许用户固定使用同一个火山引擎数据库实例进行MCP Server工具调用。

```json
{
    "mcpServers": {
        "mcp-server-dbw": {
            "command": "uvx", 
            "args": [
                "--from",
                "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_dbw",
                "mcp-server-dbw"
            ],
            "env": {
                "VOLCENGINE_REGION": "<VOLCENGINE_REGION>",
                "VOLCENGINE_ACCESS_KEY": "<VOLCENGINE_ACCESS_KEY>",
                "VOLCENGINE_SECRET_KEY": "<VOLCENGINE_SECRET_KEY>",
                "VOLCENGINE_INSTANCE_ID": "<VOLCENGINE_INSTANCE_ID>",
                "VOLCENGINE_INSTANCE_TYPE": "<VOLCENGINE_INSTANCE_TYPE>",
                "VOLCENGINE_DATABASE": "<VOLCENGINE_DATABASE>"
            }
        }
    }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
