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

#### 调试所需的输入参数

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

### Tool 2: list_o11y_agent_vpc_endpoints

#### 类型

SaaS

#### 详细描述

查询与O11yAgent采集插件相关的终端节点

#### 调试所需的输入参数

输入：

```json
{
    "name": "list_o11y_agent_vpc_endpoints",
    "description": "查询与O11yAgent采集插件相关的终端节点",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": []
    }
}
```

输出：

- 返回与O11yAgent采集插件相关的所有终端节点

#### 最容易被唤起的 Prompt示例

```
请帮我查询cn-beijing地域下与O11yAgent采集插件相关的终端节点。
```

### Tool 3: update_o11y_agent_ecs_process_config

#### 类型

SaaS

#### 详细描述

更新指定ecs实例的进程监控配置

#### 调试所需的输入参数

输入：

```json
{
    "name": "update_o11y_agent_ecs_process_config",
    "description": "更新指定ecs实例的进程监控配置",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instance_id": {
                "default": "",
                "description": "目标实例",
                "type": "string"
            },
            "processes": {
                "default": "",
                "description": "目标监控进程",
                "type": "list"
            }
        },
        "required": [
            "instance_id",
            "processes"
        ]
    }
}
```

输出：

- 返回已成功修改的实例id

#### 最容易被唤起的 Prompt示例

```
请修改cn-beijing地域下i-cnlfk3hz2nf95hjlz实例的自定义进程监控配置为nginx,java。
```

### Tool 4: list_o11y_agent_ecs_process_configs

#### 类型

SaaS

#### 详细描述

查询指定ecs实例的监控进程配置

#### 调试所需的输入参数

输入：

```json
{
    "name": "list_o11y_agent_ecs_process_configs",
    "description": "查询指定ecs实例的监控进程配置",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instance_id": {
                "default": "",
                "description": "目标实例",
                "type": "string"
            }
        },
        "required": [
            "instance_id"
        ]
    }
}
```

输出：

- 返回实例的监控进程

#### 最容易被唤起的 Prompt示例

```
请帮我查询cn-beijing地域下i-cnlfk3hz2nf95hjlz实例的自定义进程监控配置。
```

### Tool 5: get_o11y_agent_ecs_auto_install

#### 类型

SaaS

#### 详细描述

查询是否启用自动安装O11yAgent采集插件

#### 调试所需的输入参数

输入：

```json
{
    "name": "get_o11y_agent_ecs_auto_install",
    "description": "查询是否启用自动安装O11yAgent采集插件",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": [
        ]
    }
}
```

输出：

- 返回查询结果

#### 最容易被唤起的 Prompt示例

```
请帮我查询cn-beijing地域是否启用自动安装O11yAgent采集插件。
```

### Tool 6: update_o11y_agent_ecs_auto_install

#### 类型

SaaS

#### 详细描述

更新O11yAgent采集插件的自动安装配置

#### 调试所需的输入参数

输入：

```json
{
    "name": "update_o11y_agent_ecs_auto_install",
    "description": "更新O11yAgent采集插件的自动安装配置",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "enable": {
                "default": "true",
                "description": "是否启用自动安装",
                "type": "bool"
            }
        },
        "required": [
            "enable"
        ]
    }
}
```

输出：

- 空

#### 最容易被唤起的 Prompt示例

```
请帮我开启cn-beijing地域的自动安装O11yAgent采集插件。
```

### Tool 7: create_o11y_agent_ecs_deploy_task

#### 类型

SaaS

#### 详细描述

创建O11yAgent采集插件的部署任务

#### 调试所需的输入参数

输入：

```json
{
    "name": "create_o11y_agent_ecs_deploy_task",
    "description": "创建O11yAgent采集插件的部署任务",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "task_type": {
                "default": "",
                "description": "目标任务类型(e.g. upgrade, install)",
                "type": "string"
            },
            "instance_ids": {
                "default": "",
                "description": "目标实例Id集合",
                "type": "list"
            },
            "select_all": {
                "default": "false",
                "description": "是否变更所有实例",
                "type": "bool"
            }
        },
        "required": [
            "task_type",
            "instance_ids",
            "select_all"
        ]
    }
}
```

输出：

- 空

#### 最容易被唤起的 Prompt示例

```
请帮我升级cn-beijing地域下所有实例的O11yAgent采集插件版本。
```

### Tool 8: perform_o11y_agent_ecs_deploy_task

#### 类型

SaaS

#### 详细描述

对O11yAgent采集插件的部署任务执行操作

#### 调试所需的输入参数

输入：

```json
{
    "name": "perform_o11y_agent_ecs_deploy_task",
    "description": "对O11yAgent采集插件的部署任务执行操作",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "task_type": {
                "default": "",
                "description": "目标任务类型(e.g. upgrade, install)",
                "type": "string"
            },
            "action": {
                "default": "finish",
                "description": "操作(e.g. finish)",
                "type": "string"
            }
        },
        "required": [
            "task_type",
            "action"
        ]
    }
}
```

输出：

- 空

#### 最容易被唤起的 Prompt示例

```
请帮我结束cn-beijing地域下O11yAgent采集插件的升级部署任务。
```

### Tool 9: list_o11y_agent_ecs_instances

#### 类型

SaaS

#### 详细描述

查询O11yAgent采集插件中指定实例的信息

#### 调试所需的输入参数

输入：

```json
{
    "name": "list_o11y_agent_ecs_instances",
    "description": "查询O11yAgent采集插件中指定实例的信息",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instance_ids": {
                "default": "",
                "description": "需要查询的实例id集合",
                "type": "list"
            }
        },
        "required": [
            "instance_ids"
        ]
    }
}
```

输出：

- 返回O11yAgent采集插件的查询信息

#### 最容易被唤起的 Prompt示例

```
请帮我查询cn-beijing地域下实例i-cnlfk3hz2nf95hjlz的O11yAgent采集插件的信息。
```

### Tool 10: list_o11y_agent_ecs_instance_metadata

#### 类型

SaaS

#### 详细描述

查询指定实例的O11yAgent采集插件的元数据

#### 调试所需的输入参数

输入：

```json
{
    "name": "list_o11y_agent_ecs_instance_metadata",
    "description": "查询指定实例的O11yAgent采集插件的元数据",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instance_ids": {
                "default": "",
                "description": "instance ids to be queried",
                "type": "list"
            }
        },
        "required": [
            "instance_ids"
        ]
    }
}
```

输出：

- 返回O11yAgent采集插件的查询元数据

#### 最容易被唤起的 Prompt示例

```
请帮我查询cn-beijing地域下实例i-cnlfk3hz2nf95hjlz的O11yAgent采集插件的元数据。
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
