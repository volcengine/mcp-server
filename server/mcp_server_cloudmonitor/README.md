# CloudMonitor MCP Server

CloudMonitor MCP Server Provide capabilities such as query metric data。

|             |                                                                               |
|-------------|-------------------------------------------------------------------------------|
| Version     | v0.1.0                                                                        |
| Description | CloudMonitor MCP Server Help you query and manage monitoring data more easily |
| Category    | CloudNative-Observability                                                     |
| Label       | Observability、Query Metric                                                    |

## Features

- Query MetricData


## Tools

This MCP Server product provides the following Tools:
- `get_metric_data`: [get_metric_data](https://www.volcengine.com/docs/6408/105542)
- `list_o11y_agent_vpc_endpoints`: [list_o11y_agent_vpc_endpoints](https://www.volcengine.com/docs/6408/1986343)
- `update_o11y_agent_ecs_process_config`: [update_o11y_agent_ecs_process_config](https://www.volcengine.com/docs/6408/1986344)
- `list_o11y_agent_ecs_process_configs`: [list_o11y_agent_ecs_process_configs](https://www.volcengine.com/docs/6408/1986345)
- `get_o11y_agent_ecs_auto_install`: [get_o11y_agent_ecs_auto_install](https://www.volcengine.com/docs/6408/1986339)
- `update_o11y_agent_ecs_auto_install`: [update_o11y_agent_ecs_auto_install](https://www.volcengine.com/docs/6408/1986338)
- `create_o11y_agent_ecs_deploy_task`: [create_o11y_agent_ecs_deploy_task](https://www.volcengine.com/docs/6408/1986340)
- `perform_o11y_agent_ecs_deploy_task`: [perform_o11y_agent_ecs_deploy_task](https://www.volcengine.com/docs/6408/1986341)
- `list_o11y_agent_ecs_instances`: [list_o11y_agent_ecs_instances](https://www.volcengine.com/docs/6408/1986342)
- `list_o11y_agent_ecs_instance_metadata`: [list_o11y_agent_ecs_instance_metadata](https://www.volcengine.com/docs/6408/1990483)

### Tool 1: get_metric_data

#### Type

SaaS

#### Detail

Query the metric data of the specified cloud product

#### The input parameters required for debugging

Input：

```json
{
    "name": "get_metric_data",
    "description": "Query the specified metric data of the cloud product",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "request": {
                "type": "object",
                "description": "The request body of the metric query includes the start and end times of the query, the namespace, metric information, etc",
                "properties": {
                    "StartTime": {
                        "description": "Query the start time in the format of RFC3339 or Unix timestamp",
                        "type": "number"
                    },
                    "EndTime": {
                        "description": "Query the end time in the format of RFC3339 or Unix timestamp",
                        "type": "number"
                    },
                    "Namespace": {
                        "description": "The cloud product namespace to which the metric belongs",
                        "type": "string"
                    },
                    "SubNamespace": {
                        "description": "The cloud product subnamespace to which the metric belongs",
                        "type": "string"
                    },
                    "MetricName": {
                        "description": "The Name of metric",
                        "type": "string"
                    },
                    "Period": {
                        "description": "Aggregation time period",
                        "type": "string"
                    },
                    "Instances": {
                        "description": "Instances information",
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": "object",
                                "Dimensions": {
                                    "description": "The specific dimension information under the instance",
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

output：

- Return the index data of the query

#### The most easily evoked Prompt example

```
Query the CpuTotal metric data of the Instance i-cnlfk3hz2nf95hjlz under the Instance subnamespace of the VCM_ECS product in the cn-beijing area in the recent 5 minutes.
```

### Tool 2: list_o11y_agent_vpc_endpoints

#### Type

SaaS

#### Detail

Query the vpc endpoints related to the O11yAgent collection plug-in

#### The input parameters required for debugging

Input：

```json
{
    "name": "list_o11y_agent_vpc_endpoints",
    "description": "Query the vpc endpoints related to the O11yAgent collection plug-in",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": []
    }
}
```

output：

- Return all vpc endpoints related to the O11yAgent collection plug-in

#### The most easily evoked Prompt example

```
Please help me search for the terminal nodes related to the O11yAgent collection plugin-in the cn beijing region.
```

### Tool 3: update_o11y_agent_ecs_process_config

#### Type

SaaS

#### Detail

Update the process monitoring config of the specified ecs instance

#### The input parameters required for debugging

Input：

```json
{
    "name": "update_o11y_agent_ecs_process_config",
    "description": "Update the process monitoring config of the specified ecs instance",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instance_id": {
                "default": "",
                "description": "target instance",
                "type": "string"
            },
            "processes": {
                "default": "",
                "description": "target monitoring processes",
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

output：

- Return the instance id that was successfully modified 

#### The most easily evoked Prompt example

```
Please modify the custom process monitoring configuration for the i-cnlfk3hz2nf95hjlz instance in the cn beijing region to nginx and Java.
```

### Tool 4: list_o11y_agent_ecs_process_configs

#### Type

SaaS

#### Detail

Query the process monitoring config of the specified ecs instance

#### The input parameters required for debugging

Input：

```json
{
    "name": "list_o11y_agent_ecs_process_configs",
    "description": "Query the process monitoring config of the specified ecs instance",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instance_id": {
                "default": "",
                "description": "target instance",
                "type": "string"
            }
        },
        "required": [
            "instance_id"
        ]
    }
}
```

output：

- Return the monitoring processes of the instance

#### The most easily evoked Prompt example

```
Please help me check the custom process monitoring configuration for the i-cnlfk3hz2nf95hjlz instance in the cn beijing region.
```

### Tool 5: get_o11y_agent_ecs_auto_install

#### Type

SaaS

#### Detail

Query if enable to auto install O11yAgent collection plug-in

#### The input parameters required for debugging

Input：

```json
{
    "name": "get_o11y_agent_ecs_auto_install",
    "description": "Query if enable to auto install O11yAgent collection plug-in",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": [
        ]
    }
}
```

output：

- Return the result of the query

#### The most easily evoked Prompt example

```
Please help me check if the automatic installation of O11yAgent collection plugin-in is enabled in the cn beijing region.
```

### Tool 6: update_o11y_agent_ecs_auto_install

#### Type

SaaS

#### Detail

Update the O11yAgent collection plug-in's auto install config

#### The input parameters required for debugging

Input：

```json
{
    "name": "update_o11y_agent_ecs_auto_install",
    "description": "Update the O11yAgent collection plug-in's auto install config",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "enable": {
                "default": "true",
                "description": "whether to enable auto install",
                "type": "bool"
            }
        },
        "required": [
            "enable"
        ]
    }
}
```

output：

- Empty

#### The most easily evoked Prompt example

```
Please help me enable the automatic installation of O11yAgent collection plugin-in for the cn beijing region.
```

### Tool 7: create_o11y_agent_ecs_deploy_task

#### Type

SaaS

#### Detail

Create O11yAgent collection plug-in's deployment task

#### The input parameters required for debugging

Input：

```json
{
    "name": "create_o11y_agent_ecs_deploy_task",
    "description": "Create O11yAgent collection plug-in's deployment task",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "task_type": {
                "default": "",
                "description": "target task type(e.g. upgrade, install)",
                "type": "string"
            },
            "instance_ids": {
                "default": "",
                "description": "target instance ids",
                "type": "list"
            },
            "select_all": {
                "default": "false",
                "description": "whether to change all instances",
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

output：

- Empty

#### The most easily evoked Prompt example

```
Please help me upgrade the O11yAgent collection plugin-in version for all instances in the cn beijing region.
```

### Tool 8: perform_o11y_agent_ecs_deploy_task

#### Type

SaaS

#### Detail

Perform operations on the deployment task of the O11yAgent collection plug-in

#### The input parameters required for debugging

Input：

```json
{
    "name": "perform_o11y_agent_ecs_deploy_task",
    "description": "Perform operations on the deployment task of the O11yAgent collection plug-in",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "task_type": {
                "default": "",
                "description": "target task type(e.g. upgrade, install)",
                "type": "string"
            },
            "action": {
                "default": "finish",
                "description": "action(e.g. finish)",
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

output：

- Empty

#### The most easily evoked Prompt example

```
Please help me complete the upgrade and deployment task of the O11yAgent collection plugin-in the cn-beijing region.
```

### Tool 9: list_o11y_agent_ecs_instances

#### Type

SaaS

#### Detail

Query the O11yAgent collection plug-in's info of the specified instances

#### The input parameters required for debugging

Input：

```json
{
    "name": "list_o11y_agent_ecs_instances",
    "description": "Query the O11yAgent collection plug-in's info of the specified instances",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
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

output：

- Return the O11yAgent collection plug-in's info of the query

#### The most easily evoked Prompt example

```
Please help me query the information about the O11yAgent collection plugin-in for the instance i-cnlfk3hz2nf95hjlz in the cn-beijing region.
```

### Tool 10: list_o11y_agent_ecs_instance_metadata

#### Type

SaaS

#### Detail

Query the O11yAgent collection plug-in's metadata of the specified instances

#### The input parameters required for debugging

Input：

```json
{
    "name": "list_o11y_agent_ecs_instance_metadata",
    "description": "Query the O11yAgent collection plug-in's metadata of the instance",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
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

output：

- Return the O11yAgent collection plug-in's metadata of the query

#### The most easily evoked Prompt example

```
Please help me query the metadata of the O11yAgent collection plugin-in for the instance i-cnlfk3hz2nf95hjlz in the cn-beijing region.
```

## Adaptable platform  

sse: Ark，Python, Cline
stdio: Python, Cline, Trae
streamable-http: Python, Cline, Trae

## Service activation link (overall product) 

<https://console.volcengine.com/cloud-monitor>

## Authentication  

OAuth 2.0

## Configuration on different platforms

### Ark

#### exploration center

1. View the details of the MCP Server
At the Large Model Ecosystem Square, select the appropriate CloudMonitor MCP Server and view the details
2. Select the platform on which the MCP Server is about to run
Check the platforms that the current MCP Server has adapted to and select the appropriate ones
3. Check and compare the available Tools 
Carefully review the functional descriptions of the available Tools and the required input parameters, and try to run the corresponding functions.
4. Obtain the exclusive URL or code sample 
Check the login status of the account and the activation of the service, and generate a unique URL
5. Use it on the corresponding Client's platform 
Click the quick jump button to go to the experience center of the Ark platform for the experience of the corresponding MCP Server

### UVX

Please obtain the environment variables in advance VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY。

Start using the stdio mode in the local mode,

stdio mode:

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

The remote mode is started using the streamable-http mode,

streamable-http mode:
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
