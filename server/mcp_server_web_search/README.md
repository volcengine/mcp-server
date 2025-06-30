# Web Search MCP Server 

## 版本信息
v1.0

## 产品描述

Web Search MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供面向AI的、实时的、增强检索的搜索引擎结果，支持返回结构化数据，协助提升LLM回答的准确性和时效性。
目前本产品仅在柔佛地域提供服务。

## 分类
网络

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: web_search

#### 类型

SaaS

#### 详细描述

该工具允许您便捷查询搜索引擎并获取结果。

#### 调试所需的输入参数:

输入：

```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["query_word"],
    "properties": {
        "query_word": {
          "description": "待查询的关键字",
          "type": "string"
        }
    }
  },
  "name": "web_search",
  "description": "查询搜索引擎并获取结果。"
}
```

输出：

- 返回搜索引擎搜索结果。

#### 最容易被唤起的Prompt示例

```
查一下明天上海到北京的航班有哪些。
```


## 可适配平台

python，cursor

## 服务开通链接 (整体产品)

<https://www.volcengine.com/docs/84296/1554657>

## 鉴权方式

从火山引擎管理控制台获取鉴权Token。

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量       | 描述                     | 必填  | 默认值 |
|------------|------------------------|-----|-----|
| `ENDPOINT` | Web_Search实例访问Endpoint | 否   | -   |
| `TOKEN`    | Web_Search实例鉴权Token    | 是   | -   |

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
- 同步依赖项并更新uv.lock:
  ```bash
  uv sync
  ```
- 构建mcp server:
  ```bash
  uv build
  ```

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-web-search*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-web-search": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_web_search",
        "mcp-server-web-search"
      ],
      "env": {
        "ENDPOINT": "web search instance endpoint",
        "TOKEN": "web search instance token"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
