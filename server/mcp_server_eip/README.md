# EIP MCP Server 

## 版本信息
v1.0

## 产品描述

EIP MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎EIP服务交互的能力。可以基于自然语言对云端资源进行管理，一期仅支持查询公网IP、带宽包实例等操作。
## 分类
网络

## 功能

- 查看一个指定公网IP的详细信息
- 查询满足指定条件的公网IP
- 查询满足指定条件的共享带宽包

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

业务数据查询
- `describe_eip_address_attributes`: [查看指定公网IP的详情](https://www.volcengine.com/docs/6402/71040)
- `describe_eip_addresses`: [查询满足指定条件的公网IP](https://www.volcengine.com/docs/6402/71035)
- `describe_bandwidth_packages`: [查询满足指定条件的共享带宽包](https://www.volcengine.com/docs/6623/100685)

## 可适配平台

可以使用 Cline、Cursor、Claude Desktop 等支持 MCP Server 调用的客户端。

## 服务开通链接 (整体产品)

<https://www.volcengine.com/docs/6402>

## 鉴权方式

从火山引擎管理控制台获取账号 AccessKey 和 SecretKey。

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                    | 描述                         | 必填 | 默认值 |
|-------------------------|----------------------------|----|-----|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 ACCESS KEY          | 是  | -   |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 SECRET KEY          | 是  | -   |
| `VOLCENGINE_REGION`     | 火山引擎 Region名称（如cn-beijing) | 是  | -   |
| `VOLCENGINE_ENDPOINT`   | 火山引擎 OpenAPI Endpoint      | 是  | -   |

## 安装部署

### 系统依赖

- 安装 Python 3.11 或者更高版本
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
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-EIP*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-eip": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_eip",
        "mcp-server-eip"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your access-key",
        "VOLCENGINE_SECRET_KEY": "your secret-key",
        "VOLCENGINE_REGION": "volcengine region",
        "VOLCENGINE_ENDPOINT": "volcengine endpoint"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
