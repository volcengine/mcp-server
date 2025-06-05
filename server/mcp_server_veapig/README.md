# APIG MCP Server 
APIG MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎APIG服务交互的能力。可以基于自然语言对云端实例资源进行全链路管理，支持实例、服务、路由的查询操作，实现APIG资源的高效管理。

| 版本 | v0.2.0                    | 
|----|---------------------------|
| 描述 | 基于 MCP 管理 APIG 资源，智能化流量管理 |
| 分类 | 容器与中间件                    |
| 标签 | API网关 AI网关                |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: list_gateways

#### 类型

SaaS

#### 详细描述

该工具允许您便捷查看火山引擎APIG的实例列表。

#### 调试所需的输入参数:

输入：

```json 
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {}
  },
  "name": "list_gateways",
  "description": "查询您账号下拥有的所有网关实例的列表。"
}
```

输出：

- 返回您账号下拥有的网关实例列表，包含实例名称、实例ID、创建时间等信息。

#### 最容易被唤起的 Prompt示例

```
列举火山引擎 APIG 的实例列表。
```

## 可适配平台

方舟，python，cursor

## 服务开通链接 (整体产品)

<https://console.volcengine.com/veapig>

## 鉴权方式

火山引擎，从 volcengine 管理控制台获取 volcengine 访问密钥 ID、秘密访问密钥和区域，请在.env文件中设置相关环境变量

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量             | 描述                     | 默认值 |
|------------------|------------------------|-----|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 ACCESS KEY      | -   |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 SECRET KEY      | -   |
| `VOLCENGINE_REGION`         | 火山引擎 TOS region        | -   |
| `TOS_ENDPOINT`   | 火山引擎 TOS Endpoint      | -   |
| `SECURITY_TOKEN` | 火山引擎 Security Token，可选 | -   |
| `TOS_BUCKETS`    | 指定访问的 TOS 桶，可选         | -   |

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

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-veapig*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-veapig": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/src/mcp_server_veapig",
        "run",
        "mcp-server-veapig"
      ]
    }
  }
}
```

## 在不同平台的配置

### 方舟

#### 体验中心

[示例如下]

1. 查看MCP Server 详情
   在大模型生态广场，选择合适的MCP Server，并查看详情
2. 选择MCP Server即将运行的平台
   检查当前MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的Tools
   仔细查看可用的Tools的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的URL或代码示例
   检查账号登录状态与服务开通情况，生成唯一URL
5. 去对应的Client的平台进行使用
   点击快捷跳转按钮，前往方舟平台的体验中心进行对应MCP Server的体验

## 产品截图/视频 - optional

### Cursor

## 部署

[示例如下]

### UVX

```json
{
  "mcpServers": {
    "mcp-server-veapig": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_veapig",
        "mcp-server-veapig"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your access-key-id",
        "VOLCENGINE_SECRET_KEY": "your access-key-secret",
        "VOLCENGINE_REGION": "veapig region",
        "TOS_ENDPOINT": "veapig endpoint",
        "SECURITY_TOKEN": "your security token",
        "TOS_BUCKET": "your specific bucket"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).


