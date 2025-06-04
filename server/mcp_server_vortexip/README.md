# VortexIP MCP Server 

## 版本信息
v1.0

## 产品描述

VortexIP MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎VortexIP服务交互的能力。可以基于自然语言对云端资源进行管理，支持查询VortexIP、WebScraper实例等操作。

## 分类
网络

## 功能

- 查询VortexIP实例信息
- 查询WebScraper实例信息

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: describe_vortex_ip_attributes

#### 类型

SaaS

#### 详细描述

该工具允许您便捷查询火山引擎VortexIP实例详细信息。

#### 调试所需的输入参数:

输入：

```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["vortex_id"],
    "properties": {
        "vortex_id": {
          "description": "VortexIP实例ID",
          "type": "string"
        }
    }
  },
  "name": "describe_vortex_ip_attributes",
  "description": "查询您账号下一个VortexIP实例的详细信息。"
}
```

输出：

- 返回您账号下的VortexIP实例详细信息。

#### 最容易被唤起的Prompt示例

```
查询火山引擎VortexIP实例的信息，实例ID为example。
```

### Tool 2: describe_web_scraper_attributes

#### 类型

SaaS

#### 详细描述

该工具允许您便捷查询火山引擎WebScraper实例详细信息。

#### 调试所需的输入参数:

输入：

```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["web_scraper_id"],
    "properties": {
        "web_scraper_id": {
          "description": "WebScraper实例ID",
          "type": "string"
        }
    }
  },
  "name": "describe_web_scraper_attributes",
  "description": "查询您账号下一个WebScraper实例的详细信息。"
}
```

输出：

- 返回您账号下的WebScraper实例详细信息。

#### 最容易被唤起的Prompt示例

```
查询火山引擎WebScraper实例的信息，实例ID为example。
```

## 可适配平台

python，cursor

## 服务开通链接 (整体产品)

<https://www.volcengine.com/docs/84296/1251483>

## 鉴权方式

从火山引擎管理控制台获取账号 AccessKey 和 SecretKey。

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                    | 描述                    | 必填  | 默认值 |
|-------------------------|-----------------------|-----|-----|
| `VOLCENGINE_ENDPOINT`   | 火山引擎 OpenAPI Endpoint | 否   | -   |
| `VOLCENGINE_REGION`     | 火山引擎 VortexIP Region  | 是   | -   |
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 ACCESS KEY     | 是   | -   |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 SECRET KEY     | 是   | -   |

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
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-vortexip*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-vortexip": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vortexip",
        "mcp-server-vortexip"
      ],
      "env": {
        "VOLCENGINE_ENDPOINT": "volcengine endpoint",
        "VOLCENGINE_REGION": "volcengine region",
        "VOLCENGINE_ACCESS_KEY": "your access-key",
        "VOLCENGINE_SECRET_KEY": "your secret-key"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
