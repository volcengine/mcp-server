# Web Scraper MCP Server 

## 版本信息
v1.0

## 产品描述

Web Scraper MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供面向AI的、实时的、增强检索的搜索引擎结果，支持返回结构化数据，协助提升LLM回答的准确性和时效性。
目前本产品仅在火山柔佛地域提供服务。

## 分类
网络

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: webscraper_serp

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
  "name": "webscraper_serp",
  "description": "查询搜索引擎并获取结果。"
}
```

输出：

- 返回搜索引擎搜索结果。

#### 最容易被唤起的Prompt示例

```
WebScraper帮我查一下明天上海的天气
```


## 可适配平台

Trae，python，cursor


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
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-vortexip-webscraper*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-vortexip-webscraper": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vortexip_webscraper",
        "mcp-server-vortexip-webscraper"
      ],
      "env": {
        "ENDPOINT": "web scraper instance endpoint",
        "TOKEN": "web scraper instance token"
      }
    }
  }
}
```

以下环境变量用于配置MCP服务器:

| 环境变量       | 描述                      | 必填  | 默认值 |
|------------|-------------------------|-----|-----|
| `ENDPOINT` | Web Scraper实例接入Endpoint | 是   | -   |
| `TOKEN`    | Web Scraper实例鉴权Token    | 是   | -   |


## 如何获取 ENDPOINT 和 TOKEN

### Web Scraper 服务介绍

[产品动态](https://www.volcengine.com/docs/84296/1554657)。目前产品处于邀测阶段，如遇权限问题请提工单或联系产品经理开白。

### 获取 ENDPOINT
账号开白后，登录[火山引擎控制台](https://console.volcengine.com/eip/region:eip+ap-southeast-1/vortexips/serpCreate)， 
按下图所示，创建公网接入模式的SERP实例。

<img src="https://lf3-beecdn.bytetos.com/obj/ies-fe-bee-upload/bee_prod/biz_950/tos_3f5039f428034541456c70fe4709b185.png" width="600" height="250">

实例服务接入点地址，即为对应的ENDPOINT，创建完成后可以直接复制。


<img src="https://lf3-beecdn.bytetos.com/obj/ies-fe-bee-upload/bee_prod/biz_950/tos_9d9048982dc210b81007085763471aa1.png" width="600" height="200">

### 获取 TOKEN
创建SERP实例完成后，在[火山引擎控制台](https://console.volcengine.com/eip/region:eip+ap-southeast-1/vortexips?)， 
按下图所示，创建API Key。

<img src="https://lf3-beecdn.bytetos.com/obj/ies-fe-bee-upload/bee_prod/biz_950/tos_7ea16a5d86207c5e37c2543c3087e46f.png" width="600" height="150">

API Key，即为对应的TOKEN，创建完成后可以直接复制。

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
