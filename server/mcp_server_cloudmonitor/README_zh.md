# CloudMonitor MCP Server

CloudMonitor MCP Server 提供创建、更新、发布函数和添加触发器的能力。

| |                                    |
|------|------------------------------------|
| 版本 | v0.0.1                             |
| 描述 | CloudMonitor MCP Server 帮助你更轻松查询、管理监控数据 |
| 分类 | 云原生-可观测                            |
| 标签 | 可观测、指标查询                           |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: get_metric_data

#### 类型

SaaS

#### 详细描述

查询指定云产品的指标数据

#### 调试所需的输入参数，

输入：

```json
{
    "name": "get_metric_data",
    "description": "查询云产品的指定指标的数据",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "request": {
                "type": "object",
                "description": "指标查询的请求体，包含查询的起止、截止时间，命名空间，指标信息等",
                "properties": {
                    "StartTime": {
                        "description": "查询起始时间，格式为RFC3339 或 Unix 时间戳",
                        "type": "number"
                    },
                    "EndTime": {
                        "description": "查询截止时间，格式为RFC3339 或 Unix 时间戳",
                        "type": "number"
                    },
                    "Namespace": {
                        "description": "指标所属的云产品命名空间",
                        "type": "string"
                    },
                    "SubNamespace": {
                        "description": "指标所属的云产品命名子空间",
                        "type": "string"
                    },
                    "MetricName": {
                        "description": "查询的指标",
                        "type": "string"
                    },
                    "Period": {
                        "description": "聚合时间周期",
                        "type": "string"
                    },
                    "Instances": {
                        "description": "查询的实例信息",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": "object",
                                "Dimensions": {
                                    "description": "查询实例下具体的维度信息",
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "Name": {
                                                "type": "string"
                                            },
                                            "Value": {
                                                "type": "string"
                                            }
                                        },
                                        "required": [
                                            "Name",
                                            "Value"
                                        ]
                                    }
                                }
                            }
                        }
                    }
                },
                "required": [
                    "StartTime",
                    "EndTime",
                    "Namespace",
                    "SubNamespace",
                    "MetricName"
                ]
            }
        },
        "required": [
            "workspaceId",
            "query",
            "start",
            "end"
        ]
    }
}
```

输出：

- 返回查询的指标数据

#### 最容易被唤起的 Prompt示例

```
查询最近5分钟，cn-beijing区域下VCM_ECS产品的Instance子命名空间下，实例为i-cnlfk3hz2nf95hjlz的CpuTotal指标数据。
```

## 可适配平台  

sse: 方舟，Python, Cline
stdio: Python, Cline, Trae
streamable-http: Python, Cline, Trae

## 服务开通链接 (整体产品)  

<https://console.volcengine.com/cloud-monitor>

## 鉴权方式  

OAuth 2.0

## 在不同平台的配置

### 方舟

#### 体验中心

1. 查看 MCP Server 详情
在大模型生态广场，选择合适的 CloudMonitor MCP Server，并查看详情
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

local方式 使用stdio模式启动:

stdio方式

```json
{
  "mcpServers": {
    "mcp-server-cloudmonitor-stdio": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cloudmonitor",
        "mcp-server-cloudmonitor-stdio"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your volcengine access key",
        "VOLCENGINE_SECRET_KEY": "your volcengine secret key"
      }
    }
  }
}
```

remote方式 使用streamable-http模式启动:

streamable-http方式

```json
{
  "mcpServers": {
    "mcp-server-cloudmonitor-streamable": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cloudmonitor",
        "mcp-server-cloudmonitor-streamable"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your volcengine access key",
        "VOLCENGINE_SECRET_KEY": "your volcengine secret key"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the MIT License.
