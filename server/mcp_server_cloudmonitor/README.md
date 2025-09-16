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
