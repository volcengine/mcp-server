# 融合信息搜索 MCP Server
## 版本信息
v0.1.0
## 产品描述
依托字节强大的搜索能力，提供适配大模型数据结构的联网搜索内容，助力提升大模型知识获取、时效性及回答准确性。
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
根据用户输入问题，提供基于联网搜索的大模型总结后回复内容
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
                "description": "用户搜索 query，1~100 个字符 (过长会截断)，不支持多词搜索",
                "type": "string"
            },
            "Count": {
                "description": "返回条数，最多50条，不传默认10条",
                "type": "number"
            }
        }
    },
    "name": "web_search",
    "description": "联网搜索能力调用"
}
```
输出：
```json
联网搜索结果，结构参考文档的响应体部分 https://www.volcengine.com/docs/85508/1650263
```

#### 最容易被唤起的 Prompt示例
联网搜索北京周边游攻略
## 可适配平台
Trae，Cursor，Python
## 服务开通链接 (整体产品)
登录火山控制台，开通【融合信息检索】，服务开通链接：https://console.volcengine.com/ask-echo/web-search
## 鉴权方式
- API Key鉴权
- 火山引擎的AKSK鉴权体系
## 安装部署
### 前置准备
- Python 3.12+
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
鉴权信息，火山引擎AK SK,与ASK_ECHO_SEARCH_INFINITY_API_KEY接入二选一即可
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