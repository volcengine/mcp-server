# veFaaS MCP Server

veFaaS MCP Server 提供创建、更新、发布函数和添加触发器的能力。

| | |
|------|------|
| 版本 | v0.0.1 |
| 描述 | veFaaS MCP Server 祝你轻松管理函数和触发器生命周期|
| 分类 | 容器与中间件 |
| 标签 | FaaS，函数服务，函数，生命周期 |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: supported_runtimes

#### 类型

SaaS

#### 详细描述

列出 VeFaaS 函数支持的所有运行时环境，包括各种版本的 Python、Golang、Node.js 等，便于用户在创建函数时选择合适的运行环境。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    },
    "name": "supported_runtimes",
    "description": "列出 VeFaaS 函数支持的所有运行时环境"
}
```

输出：

- 返回支持的运行时环境列表，如 python3.8/v1, python3.9/v1, golang/v1 等

#### 最容易被唤起的 Prompt示例

```
列出所有支持的运行时
VeFaaS 支持哪些运行时环境？
```

### Tool 2: create_function

#### 类型

SaaS

#### 详细描述

创建新的 VeFaaS 函数，可指定名称、运行时环境、命令和镜像等参数。如未提供名称，将自动生成随机名称。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "properties": {
        "name": {
          "description": "函数名称，若不提供则自动生成",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        },
        "runtime": {
          "description": "运行时环境，如 python3.8/v1",
          "type": "string"
        },
        "command": {
          "description": "要执行的命令",
          "type": "string"
        },
        "image": {
          "description": "容器镜像地址",
          "type": "string"
        }
      }
    },
    "name": "create_function",
    "description": "创建新的 VeFaaS 函数"
}
```

输出：

- 返回函数创建成功信息，包含函数名和函数 ID

#### 最容易被唤起的 Prompt示例

```
创建一个 Python 函数
创建一个使用 Node.js 的 VeFaaS 函数
```

### Tool 3: update_function

#### 类型

SaaS

#### 详细描述

更新现有 VeFaaS 函数的代码或配置，可修改源代码、运行命令等。支持 zip、tos 或容器镜像方式更新。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["function_id", "source"],
      "properties": {
        "function_id": {
          "description": "要更新的函数 ID",
          "type": "string"
        },
        "source": {
          "description": "源代码或镜像地址",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        },
        "command": {
          "description": "要执行的命令",
          "type": "string"
        }
      }
    },
    "name": "update_function",
    "description": "更新 VeFaaS 函数的代码或配置"
}
```

输出：

- 返回函数更新成功信息

#### 最容易被唤起的 Prompt示例

```
更新函数代码
修改函数的运行命令
```

### Tool 4: release_function

#### 类型

SaaS

#### 详细描述

发布 VeFaaS 函数使其可用于生产环境，将函数的最新版本部署为生产版本，使函数可被外部调用。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["function_id"],
      "properties": {
        "function_id": {
          "description": "要发布的函数 ID",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "release_function",
    "description": "发布 VeFaaS 函数使其可用于生产环境"
}
```

输出：

- 返回函数发布成功信息

#### 最容易被唤起的 Prompt示例

```
发布函数到生产环境
部署函数使其可被调用
```

### Tool 5: delete_function

#### 类型

SaaS

#### 详细描述

删除指定的 VeFaaS 函数，操作不可逆，会永久移除该函数及其所有配置，释放相关资源。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["function_id"],
      "properties": {
        "function_id": {
          "description": "要删除的函数 ID",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "delete_function",
    "description": "删除指定的 VeFaaS 函数"
}
```

输出：

- 返回函数删除成功信息

#### 最容易被唤起的 Prompt示例

```
删除函数
移除不再需要的函数
```

### Tool 6: get_function_release_status

#### 类型

SaaS

#### 详细描述

检查 VeFaaS 函数的发布状态，查询函数当前是否已经发布、发布过程是否完成、是否存在错误等信息。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["function_id"],
      "properties": {
        "function_id": {
          "description": "要检查的函数 ID",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "get_function_release_status",
    "description": "检查 VeFaaS 函数的发布状态"
}
```

输出：

- 返回函数的发布状态信息，包括当前状态、错误信息等

#### 最容易被唤起的 Prompt示例

```
检查函数发布状态
函数是否已成功部署
```

### Tool 7: does_function_exist

#### 类型

SaaS

#### 详细描述

检查指定 ID 的 VeFaaS 函数是否存在，返回布尔值表示函数存在与否，用于验证函数 ID 是否有效。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["function_id"],
      "properties": {
        "function_id": {
          "description": "要检查的函数 ID",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "does_function_exist",
    "description": "检查指定 ID 的 VeFaaS 函数是否存在"
}
```

输出：

- 返回布尔值：true（函数存在）或 false（函数不存在）

#### 最容易被唤起的 Prompt示例

```
检查函数是否存在
验证函数 ID 是否有效
```

### Tool 8: get_latest_functions

#### 类型

SaaS

#### 详细描述

列出最新创建的 VeFaaS 函数，默认返回 5 个最新的函数信息，包括函数 ID、名称、运行时等详细信息。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "properties": {
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "get_latest_functions",
    "description": "列出最新创建的 VeFaaS 函数"
}
```

输出：

- 返回最新函数列表及详细信息

#### 最容易被唤起的 Prompt示例

```
列出所有函数
查看最近创建的函数
```

### Tool 9: create_zip_from_code

#### 类型

SaaS

#### 详细描述

将 Python 代码打包为 Base64 编码的 zip 文件，用于函数部署，自动创建包含 index.py 的 zip 包并进行编码。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["code"],
      "properties": {
        "code": {
          "description": "要打包的 Python 代码",
          "type": "string"
        }
      }
    },
    "name": "create_zip_from_code",
    "description": "将 Python 代码打包为 Base64 编码的 zip 文件"
}
```

输出：

- 返回 Base64 编码的 zip 文件内容

#### 最容易被唤起的 Prompt示例

```
将代码打包为 zip
把 Python 代码打包用于部署
```

### Tool 10: create_api_gateway_trigger

#### 类型

SaaS

#### 详细描述

为 VeFaaS 函数创建 API 网关触发器，使函数可通过 HTTP 请求调用，自动配置路由和上游服务连接。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["function_id", "api_gateway_id", "service_id"],
      "properties": {
        "function_id": {
          "description": "函数 ID",
          "type": "string"
        },
        "api_gateway_id": {
          "description": "API 网关 ID",
          "type": "string"
        },
        "service_id": {
          "description": "服务 ID",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "create_api_gateway_trigger",
    "description": "为 VeFaaS 函数创建 API 网关触发器"
}
```

输出：

- 返回创建的路由信息

#### 最容易被唤起的 Prompt示例

```
创建 API 网关触发器
为函数添加 HTTP 触发器
```

### Tool 11: list_api_gateways

#### 类型

SaaS

#### 详细描述

列出所有可用的 API 网关，显示网关 ID、名称、区域等信息，帮助用户选择合适的网关创建触发器。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "properties": {
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "list_api_gateways",
    "description": "列出所有可用的 API 网关"
}
```

输出：

- 返回 API 网关列表及详细信息

#### 最容易被唤起的 Prompt示例

```
列出所有 API 网关
查看可用的网关列表
```

### Tool 12: list_api_gateway_services

#### 类型

SaaS

#### 详细描述

列出指定 API 网关的所有服务，显示服务 ID、名称、协议等信息，帮助用户选择合适的服务创建触发器。

#### 调试所需的输入参数

输入：

```json
{
    "inputSchema": {
      "type": "object",
      "required": ["gateway_id"],
      "properties": {
        "gateway_id": {
          "description": "API 网关 ID",
          "type": "string"
        },
        "region": {
          "description": "区域，默认为 cn-beijing",
          "type": "string"
        }
      }
    },
    "name": "list_api_gateway_services",
    "description": "列出指定 API 网关的所有服务"
}
```

输出：

- 返回 API 网关服务列表及详细信息

#### 最容易被唤起的 Prompt示例

```
列出网关的所有服务
查看网关下的服务列表
```

## 可适配平台  

sse: 方舟，Python
stdio: Python, Cursor, Claude macOS App, Cline

## 服务开通链接 (整体产品)  

<https://console.volcengine.com/vefaas>

## 鉴权方式  

OAuth 2.0

## 在不同平台的配置

### 方舟

#### 体验中心

1. 查看 MCP Server 详情
在大模型生态广场，选择合适的 veFaaS MCP Server，并查看详情
2. 选择 MCP Server 即将运行的平台
检查当前 MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的 Tools
仔细查看可用的 Tools 的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的URL或代码示例
检查账号登录状态与服务开通情况，生成唯一URL
5. 去对应的Client的平台进行使用
点击快捷跳转按钮，前往方舟平台的体验中心进行对应MCP Server的体验

### UVX

请预先获取环境变量 VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY。

```json
{
  "mcpServers": {
    "vefaas": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vefaas_function",
        "mcp-server-vefaas-function"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "xxx",
        "VOLCENGINE_SECRET_KEY": "xxx"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the MIT License.
