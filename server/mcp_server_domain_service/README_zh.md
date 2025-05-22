
# 域名服务 MCP Server

域名服务全新推出的 MCP Server，具备高效的域名注册功能，支持通过自然语言交互轻松查询各类域名价格，一键完成域名注册操作，大幅简化域名获取流程，显著提升域名注册效率与便捷性。

| 版本 | v0.1.0 |
| :-: | :-: |
| 描述 | 通过自然语言高效查询并注册域名 |
| 分类 | 企业应用 |
| 标签 | 域名 |


## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### Tool1: check_fee
 - 详细描述：查询域名价格，能否注册以及是否包含限制词等信息。
 - 触发示例：调用 check_fee 获取相关数据
### Tool2: get_domain
 - 详细描述：获取指定域名的详细信息。
 - 触发示例：调用 get_domain 获取相关数据
### Tool3: get_async_task
 - 详细描述：查询火山引擎域名服务中异步任务的执行状态。操作包括域名注册，域名续费等。
 - 触发示例：调用 get_async_task 获取相关数据
### Tool4: get_template
 - 详细描述：获取一个域名信息模板的详情。
 - 触发示例：调用 get_template 获取相关数据
### Tool5: list_domains
 - 详细描述：查询您在火山引擎域名服务托管的域名的详细信息。
 - 触发示例：调用 list_domains 获取相关数据
### Tool6: list_templates
 - 详细描述：获取当前账号下的域名信息模板列表以及列表中每个信息模板的详细信息。您可以指定一个或者多个条件对返回的域名列表进行过滤。
 - 触发示例：调用 list_templates 获取相关数据
### Tool7: register_domain
 - 详细描述：注册一个域名。该操作会生成一个异步任务。您可以使用 get_async_task 查询该任务的状态。
 - 触发示例：调用 register_domain 获取相关数据


## 最容易被唤起的 Prompt示例
### check_fee
我想查询下 volcengine.com 域名的价格

### list_domains
我想查询下我的域名列表

### register_domain
我想申请一个 xxx.com 的域名


## 可适配平台  
可以使用 cline, cursor, claude desktop 或支持MCP server调用的的其他终端

## 服务开通链接 (整体产品)
<https://console.volcengine.com/domain-service>


## 鉴权方式
从 volcengine 管理控制台获取 volcengine 访问密钥 ID、秘密访问密钥

## 安装

### 环境要求

- Python 3.13+
- 火山引擎账号及AccessKey/SecretKey


## 部署
### 在 MCP Client 中集成

```json
{
  "mcpServers": {
    "mcp-server-domain-service": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_domain_service",
        "mcp-server-domain-service"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

## License
MIT