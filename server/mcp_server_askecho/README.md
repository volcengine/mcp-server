# 联网问答Agent MCP Server

## 版本信息

v0.1.0

## 产品描述

整合豆包大模型及联网能力，为企业客户提供端到端的联网搜索及智能体服务，在通用问答、新闻、知识百科、出行等各类业务场景中，帮助客户快速构建专属chatbot

## 分类

搜索工具

## 标签

- 人工智能与机器学习
- 联网搜索

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: chat_completion

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
      "query"
    ],
    "properties": {
      "query": {
        "description": "搜索问题",
        "type": "string"
      }
    }
  },
  "name": "chat_completion",
  "description": "联网问答智能体会话"
}
```

输出：

- 大模型基于联网搜索给出的总结回复

#### 最容易被唤起的 Prompt示例

今天的热点新闻

## 可适配平台

Trae，Cursor，Python

## 服务开通链接 (整体产品)

登录火山控制台，开通【联网agent lite版】，具体流程参考：https://www.volcengine.com/docs/85508/1512748

## 鉴权方式

火山引擎的AKSK鉴权体系

## 安装部署

### 前置准备

- Python 3.13+
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
cd mcp-server/server/mcp_server_askecho
uv run mcp-server-askecho

# 使用sse模式启动(默认为stdio)
uv run mcp-server-askecho -t sse
```

## 部署

### UVX

```json
{
  "mcpServers": {
    "mcp-server-askecho": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_askecho",
        "mcp-server-askecho"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key",
        "VOLCENGINE_SECRET_KEY": "your-secret-key",
        "ASKECHO_BOT_ID": "your-bot-id"
      }
    }
  }
}
```

# License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)