# 企业服务 MCP Server

企业服务全新推出的 MCP Server，具备商标查询等功能，支持通过自然语言交互轻松查询商标信息，申请人信息，需求信息。

| 版本 |            v0.1.0            |
| :--: | :--------------------------: |
| 描述 | 通过自然语言高效查询商标信息 |
| 分类 |           企业应用           |
| 标签 |           企业服务           |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool1: search_trademark

- 详细描述：查询商标局中记录的商标信息，常用于注册前评估意向商标的状态。支持商标名称，注册号和申请人独立搜索，且必填其一
- 触发示例：调用 search_trademark 获取相关数据

### Tool2: search_trademark_info

- 详细描述：根据商标注册号查询商标的详情
- 触发示例：调用 search_trademark_info 获取相关数据

### Tool3: list_trademarks

- 详细描述：获取当前账户提交的商标列表
- 触发示例：调用 list_trademarks 获取相关数据

### Tool4: get_trademark

- 详细描述：获取当前账户的商标详情
- 触发示例：调用 get_trademark 获取相关数据

### Tool5: list_applicants

- 详细描述：获取商标申请人列表
- 触发示例：调用 list_applicants 获取相关数据

### Tool6: get_applicant

- 详细描述：获取商标申请人详情
- 触发示例：调用 get_applicant 获取相关数据

### Tool7: list_requirements

- 详细描述：获取商标需求列表
- 触发示例：调用 list_requirements 获取相关数据

### Tool8: get_requirement

- 详细描述：获取商标需求详情
- 触发示例：调用 get_requirement 获取相关数据

### Tool9: list_barrier_trademarks

- 详细描述：获取障碍商标列表
- 触发示例：调用 list_barrier_trademarks 获取相关数据

## 最容易被唤起的 Prompt 示例

### search_trademark

我想查询下【火山引擎】商标的状态

### list_trademarks

我想查询下我的商标列表

## 可适配平台

可以使用 cline, cursor, claude desktop 或支持 MCP server 调用的的其他终端

## 服务开通链接 (整体产品)

<https://console.volcengine.com/enterprise/overview>

## 鉴权方式

从 volcengine 管理控制台获取 volcengine 访问密钥 ID、秘密访问密钥

## 安装

### 环境要求

- Python 3.13+
- 火山引擎账号及 AccessKey/SecretKey

## 部署

### 在 MCP Client 中集成

```json
{
  "mcpServers": {
    "mcp-server-enterprise": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_enterprise",
        "mcp-server-enterprise"
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
