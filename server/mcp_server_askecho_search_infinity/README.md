# 联网搜索API MCP Server
## 版本信息
v0.2.0
## 产品描述
火山引擎联网搜索API，提供豆包搜索 Custom 版网页与基础图片搜索能力，帮助大模型获取更准确、更新鲜的外部信息。
## 分类
火山引擎云原生
## 标签
- 搜索工具
- 知识获取

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### Tool 1: web_search

#### 类型
saas
#### 详细描述
根据用户输入问题，返回联网搜索结果，支持网页与基础图片搜索。
#### 调试所需的输入参数:
输入：
```json
{
    "inputSchema": {
        "type": "object",
        "required": [
            "Query"
        ],
        "properties": {
            "Query": {
                "description": "用户搜索 query，1~100 个字符",
                "type": "string"
            },
            "Count": {
                "description": "返回条数；web 默认 10 条、最多 50 条，image 默认且最多 5 条",
                "type": "number"
            },
            "SearchType": {
                "description": "搜索类型，仅支持 web 或 image，默认 web",
                "type": "string"
            },
            "TimeRange": {
                "description": "web 搜索时间范围，可选 OneDay/OneWeek/OneMonth/OneYear 或 YYYY-MM-DD..YYYY-MM-DD",
                "type": "string"
            },
            "AuthLevel": {
                "description": "权威等级过滤，0 为默认，1 为非常权威",
                "type": "number"
            },
            "NeedContent": {
                "description": "是否返回网页正文，仅支持 web",
                "type": "boolean"
            },
            "NeedUrl": {
                "description": "是否返回网页 URL，仅支持 web",
                "type": "boolean"
            },
            "Sites": {
                "description": "仅搜索指定站点，以 | 分隔，最多 20 个，仅支持 web",
                "type": "string"
            },
            "BlockHosts": {
                "description": "排除指定站点，以 | 分隔，最多 5 个，仅支持 web",
                "type": "string"
            },
            "Industry": {
                "description": "行业搜索，可选 finance、game 或 gov，仅支持 web",
                "type": "string"
            },
            "QueryRewrite": {
                "description": "是否启用查询改写",
                "type": "boolean"
            },
            "ContentFormats": {
                "description": "网页正文格式，可选 text 或 markdown，仅支持 web",
                "type": "string"
            }
        }
    },
    "name": "web_search",
    "description": "联网搜索 API 调用"
}
```
输出：
```json
联网搜索结果，结构参考官方 API 文档 https://www.volcengine.com/docs/87772/2272953
```

#### 最容易被唤起的 Prompt示例
联网搜索北京周边游攻略
## 可适配平台
Claude Code, Codex, Trae，Cursor等支持MCP协议的AI工具
## 服务开通链接 (整体产品)
登录火山控制台，开通【联网搜索API】，服务开通链接：https://console.volcengine.com/search-infinity/web-search

API Key 创建链接：https://console.volcengine.com/search-infinity/api-key
## 鉴权方式
- API Key鉴权
- 火山引擎的AKSK鉴权体系
## 安装部署
### 前置准备
- Python 3.12 / 3.13
- UV
  **Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
### 安装
克隆仓库:
```bash
git clone git@github.com:volcengine/mcp-server.git
```
### 使用方法
启动服务器:
**UV**
```bash
cd mcp-server/server/mcp_server_askecho_search_infinity
uv run mcp-server-askecho-search-infinity
# 使用sse/streamable-http模式启动(默认为stdio)
uv run mcp-server-askecho-search-infinity -t sse
uv run mcp-server-askecho-search-infinity -t streamable-http
```
## 部署
### UVX
鉴权信息，火山引擎 AK/SK 与 `ASK_ECHO_SEARCH_INFINITY_API_KEY` 二选一即可

#### 推荐：从 PyPI 或已配置的火山镜像源安装

该方式不依赖 GitHub，`>=0.2.0` 会自动使用可获取的最新发布版本。

```json
{
  "mcpServers": {
    "mcp-server-askecho-search-infinity": {
      "command": "uvx",
      "args": [
        "--from",
        "mcp-server-askecho-search-infinity>=0.2.0",
        "mcp-server-askecho-search-infinity"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "",
        "VOLCENGINE_SECRET_KEY": "",
        "ASK_ECHO_SEARCH_INFINITY_API_KEY": ""
      }
    }
  }
}
```

#### 备用：从 GitHub 源码安装

```json
{
  "mcpServers": {
    "mcp-server-askecho-search-infinity": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_askecho_search_infinity",
        "mcp-server-askecho-search-infinity"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "",
        "VOLCENGINE_SECRET_KEY": "",
        "ASK_ECHO_SEARCH_INFINITY_API_KEY": ""
      }
    }
  }
}
```
## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)
