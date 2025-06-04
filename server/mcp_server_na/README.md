# NetworkAdvisor MCP Server 

## 版本信息
v1.0

## 产品描述

NetworkAdvisor MCP Server 是一个模型上下文协议(Model Context Protocol)服务器，为MCP客户端(如Claude Desktop)提供与火山引擎云网络智能中心（NetworkAdvisor）服务交互的能力。可以基于自然语言对云网络资源发起一键诊断以及查询诊断结果。

## 分类
网络

## 功能

- 创建云网络实例诊断
- 查询云网络实例诊断结果

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: create_diagnosis_instance

#### 类型

SaaS

#### 详细描述

该工具允许您创建云网络实例诊断任务。

#### 调试所需的输入参数:

输入：

```json 
{
  "inputSchema": {
    "type": "object",
    "required": [
      "region",
      "resource_type",
      "resource_id"
    ],
    "properties": {
      "region": {
        "description": "资源所在Region",
        "type": "string"
      },
      "resource_type": {
        "description": "实例类型，如EIP、NAT、CLB",
        "type": "string"
      },
      "resource_id": {
        "description": "实例资源ID",
        "type": "string"
      }
    }
  },
  "name": "create_diagnosis_instance",
  "description": "创建实例诊断任务"
}
```

输出：

- 返回云网络实例诊断任务ID。

#### 最容易被唤起的Prompt示例

```
对cn-beijing云网络实例进行诊断，实例ID是eip-××××××，资源类型EIP
```

### Tool 2: describe_diagnosis_instance_detail

#### 类型

SaaS

#### 详细描述

该工具允许您查询云网络实例诊断任务的结果。

#### 调试所需的输入参数:

输入：

```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["diagnosis_instance_id"],
    "properties": {
        "diagnosis_instance_id": {
          "description": "实例诊断任务ID",
          "type": "string"
        }
    }
  },
  "name": "describe_diagnosis_instance_detail",
  "description": "查询一个实例诊断任务报告详情"
}
```

输出：

- 返回云网络实例诊断报告的详情。

#### 最容易被唤起的Prompt示例

```
查询火山引擎云网络实例诊断报告，任务ID为di-××××××。
```

## 可适配平台

python，cursor

## 服务开通链接 (整体产品)

<https://console.volcengine.com/netadvisor/diagnosis>

## 鉴权方式

从火山引擎管理控制台获取账号 AccessKey 和 SecretKey。

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量                    | 描述                    | 必填 | 默认值 |
|-------------------------|-----------------------|----|-----|
| `VOLCENGINE_ENDPOINT`   | 火山引擎 OpenAPI Endpoint | 是  | -   |
| `VOLCENGINE_REGION`     | 火山引擎 Region           | 是  | -   |
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 ACCESS KEY     | 是  | -   |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 SECRET KEY     | 是  | -   |

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
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-na*.

#### 本地配置

添加以下配置到你的 mcp settings 文件中

```json
{
  "mcpServers": {
    "mcp-server-na": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_na",
        "mcp-server-na"
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
