# VMP MCP Server ![Product Logo](./logo.svg)

The Volcengine Managed Prometheus Service (VMP) is a new-generation cloud-native monitoring system that fully inherits and integrates with the open-source prometheus ecosystem. The VMP MCP Server provides functions such as prometheus workspace queries and metric queries, facilitating the natural-language-driven metrics query and analysis experience in scenarios like operational troubleshooting and data analysis.

<table>
  <tr>
    <td>Version</td>
    <td>v0.1.0</td>
  </tr>
  <tr>
    <td>Description</td>
    <td>Natural-language-driven query and analysis of prometheus metric data</td>
  </tr>
  <tr>
    <td>Category</td>
    <td>Observability</td>
  </tr>
  <tr>
    <td>Tags</td>
    <td>Prometheus, Monitoring, Observability</td>
  </tr>
</table>

## Tools
This MCP Server product provides the following Tools (capabilities):

### Tool 1: create_workspace

#### Detailed Description
Create a VMP workspace instance in the specified region.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "create_workspace",
    "description": "Create a VMP workspace instance in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "name": {
                "description": "Name of the workspace instance",
                "type": "string"
            },
            "description": {
                "description": "Description of the workspace instance",
                "type": "string"
            },
            "delete_protection_enabled": {
                "description": "Whether to enable deletion protection for the workspace instance",
                "type": "boolean"
            },
            "instance_type_id": {
                "description": "Type ID of the workspace instance",
                "type": "string"
            },
            "project_name": {
                "description": "Project name to which the workspace instance belongs",
                "type": "string"
            },
            "username": {
                "description": "Basic auth username for the workspace instance, must be set together with the password field",
                "type": "string"
            },
            "password": {
                "description": "Basic auth password for the workspace instance, must be set together with the username field",
                "type": "string"
            },
            "public_access_enabled": {
                "description": "Whether to enable public access for the workspace instance",
                "type": "boolean"
            }
        },
        "required": [
            "region",
            "name",
            "instance_type_id"
        ]
    }
}
```
Output:
- Workspace ID

#### Example Prompt most likely to trigger
Please create a VMP workspace instance named vmp-1234567890abcdef with type vmp.standard.15d in the cn-beijing region.

### Tool 2: update_workspace

#### Detailed Description
Update information for a VMP workspace instance in the specified region.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "update_workspace",
    "description": "Update information for a VMP workspace instance in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspaceId": {
                "description": "ID of the VMP workspace instance to update",
                "type": "string"
            },
            "name": {
                "description": "New name for the workspace instance",
                "type": "string"
            },
            "delete_protection_enabled": {
                "description": "Whether to enable deletion protection for the workspace instance",
                "type": "boolean"
            },
            "description": {
                "description": "New description for the workspace instance",
                "type": "string"
            },
            "name": {
                "description": "New name for the workspace instance",
                "type": "string"
            },
            "public_access_enabled": {
                "description": "Whether to enable public access for the workspace instance",
                "type": "boolean"
            },
            "search_latency_offset": {
                "description": "Search latency offset for the workspace instance, must be a time duration string (e.g. 1m, 1h)",
                "type": "string"
            },
            "username": {
                "description": "Basic auth username for the workspace instance, must be set together with the password field",
                "type": "string"
            },
            "password": {
                "description": "Basic auth password for the workspace instance, must be set together with the username field",
                "type": "string"
            },
            "active_series": {
                "description": "Maximum number of active time series for the workspace instance",
                "type": "integer"
            },
            "ingest_samples_per_second": {
                "description": "Maximum number of samples ingested per second for the workspace instance",
                "type": "integer"
            },
            "public_query_bandwidth": {
                "description": "Maximum public query bandwidth for the workspace instance, in Mbps",
                "type": "integer"
            },
            "public_write_bandwidth": {
                "description": "Maximum public write bandwidth for the workspace instance, in Mbps",
                "type": "integer"
            },
            "query_per_second": {
                "description": "Maximum number of public queries per second for the workspace instance",
                "type": "integer"
            },
            "scan_samples_per_second": {
                "description": "Maximum number of samples scanned per second for the workspace instance",
                "type": "integer"
            },
            "scan_series_per_second": {
                "description": "Maximum number of time series scanned per second for the workspace instance",
                "type": "integer"
            }
        },
        "required": [
            "workspaceId",
            "region"
        ]
    }
}
```
Output:
- Workspace ID

#### Example Prompt most likely to trigger
Please help adjust the query per second rate of the VMP workspace with ID vmp-1234567890abcdef to 200.

### Tool 3: list_workspaces

#### Detailed Description
Query all workspace information in the specified region under the current account.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "list_workspaces",
    "description": "Query all VMP workspace instances information in the specified region.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        }
    }
}
```
Output:
- Workspace list

#### Example Prompt most likely to trigger
Please list all VMP workspace instances in the cn-beijing region.

### Tool 4: delete_workspace

#### Detailed Description
Delete a specified workspace instance in the specified region under the current account.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "delete_workspace",
    "description": "Delete a specified VMP workspace instance in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspaceId": {
                "description": "ID of the VMP workspace instance to delete",
                "type": "string"
            }
        },
        "required": [
            "region",
            "workspaceId"
        ]
    }
}
```
Output:
- Workspace ID

#### Example Prompt most likely to trigger
Please delete the VMP workspace instance vmp-1234567890abcdef in the cn-beijing region.

### Tool 5: list_workspace_instance_types

#### Detailed Description
Query all VMP workspace instance types in the specified region.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "list_workspace_instance_types",
    "description": "Query all VMP workspace instance types in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instanceTypeId": {
                "description": "ID of the VMP workspace instance type to query",
                "type": "string"
            }
        }
    }
}
```
Output:
- Workspace type list

#### Example Prompt most likely to trigger
Please list all workspace types in the cn-beijing region.

### Tool 6: query_metrics

#### Detailed Description
Execute a specified PromQL instant query in the specified VMP workspace.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "query_metrics",
    "description": "Execute a specified PromQL query statement in the specified VMP workspace.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "The ID of the VMP workspace instance to query.",
                "type": "string"
            },
            "query": {
                "description": "PromQL query statement.",
                "type": "string"
            },
            "time": {
                "anyOf": [
                    {
                        "type": "string"
                    },
                    {
                        "type": "null"
                    }
                ],
                "default": null,
                "description": "Query time, in RFC3339 format or Unix timestamp, default is the current time."
            },
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": [
            "workspaceId",
            "query"
        ]
    }
}
```
Output:
- Metric query results

#### Example Prompt most likely to trigger
Query the CPU usage at the current time in the VMP workspace instance b73766b5-2e63-4143-bcd1-8a1ba3a94746 in the cn-beijing region.

### Tool 7: query_range_metrics

#### Detailed Description
Execute a specified PromQL query within a specified time range in the specified VMP workspace.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "query_range_metrics",
    "description": "Execute a specified PromQL query within a specified time range in the specified VMP workspace.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "The ID of the target VMP workspace instance.",
                "type": "string"
            },
            "query": {
                "description": "PromQL query statement.",
                "type": "string"
            },
            "start": {
                "description": "Query start time, in RFC3339 format or Unix timestamp.",
                "type": "string"
            },
            "end": {
                "description": "Query end time, in RFC3339 format or Unix timestamp.",
                "type": "string"
            },
            "step": {
                "anyOf": [
                    {
                        "type": "string"
                    },
                    {
                        "type": "null"
                    }
                ],
                "default": null,
                "description": "Query step, in duration format, optional. If not provided, it will be automatically calculated based on the query time range."
            },
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
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
Output:
- Metric query results

#### Example Prompt most likely to trigger
Query the top 3 pods in terms of CPU usage in the last hour in the VMP workspace instance b73766b5-2e63-4143-bcd1-8a1ba3a94746 in the cn-beijing region.

### Tool 8: query_metric_names

#### Detailed Description
Query the list of metric names that match the specified filter conditions in the specified VMP workspace.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "query_metric_names",
    "description": "Query the list of metric names that match the specified filter conditions in the specified VMP workspace.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "The ID of the target VMP workspace instance.",
                "type": "string"
            },
            "match": {
                "anyOf": [
                    {
                        "type": "string"
                    },
                    {
                        "type": "null"
                    }
                ],
                "default": null,
                "description": "Series Selector, used to filter the matching metric range, following the standard Prometheus Vector Selector syntax, e.g.: {job=~\"kubelet\"}"
            },
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": [
            "workspaceId"
        ]
    }
}
```
Output:
- List of matching metric names

#### Example Prompt most likely to trigger
What are the CPU related metrics in the VMP workspace b73766b5-2e63-4143-bcd1-8a1ba3a94746 ?

### Tool 9: query_metric_labels

#### Detailed Description
Query the list of all label names for a specified metric in the specified VMP workspace.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "query_metric_labels",
    "description": "Query the list of all label names for a specified metric in the specified VMP workspace.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "The ID of the target VMP workspace instance.",
                "type": "string"
            },
            "metricName": {
                "description": "The name of the metric to query.",
                "type": "string"
            },
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": [
            "workspaceId",
            "metricName"
        ]
    }
}
```
Output:
- List of metric label names

#### Example Prompt most likely to trigger
What are the labels of the container_cpu_usage_seconds_total metric in the VMP workspace b73766b5-2e63-4143-bcd1-8a1ba3a94746 ?

### Tool 10: query_series

#### Detailed Description
Query all time series under the specified label filter in the specified VMP workspace.

#### Input parameters required for debugging:
Input:
```json 
{
    "name": "query_series",
    "description": "Query all time series under the specified label filter in the specified VMP workspace",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "The ID of the target VMP workspace instance.",
                "type": "string"
            },
            "match": {
                "type": "string",
                "description": "Series Selector, used to filter the matching metric range, following the standard Prometheus Vector Selector syntax, e.g.: {job=~\"kubelet\"}"
            },
            "start": {
                "description": "Query start time, in RFC3339 or Unix timestamp format",
                "type": "string"
            },
            "end": {
                "description": "Query end time, in RFC3339 or Unix timestamp format",
                "type": "string"
            },
            "region": {
                "default": "cn-beijing",
                "description": "Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": [
            "workspaceId",
            "match"
        ]
    }
}
```
Output:
- List of metric label names

#### Example Prompt most likely to trigger
What are the series of the up metric in the VMP workspace b73766b5-2e63-4143-bcd1-8a1ba3a94746 ?

## Compatible Platforms
Ark, Trae, Cursor, Claude Desktop, or other terminals that support MCP Server calls.

## Service Activation Link (Entire Product)
https://console.volcengine.com/prometheus

## Authentication Method
API Key ([Signature Mechanism](https://www.volcengine.com/docs/6731/942192))

## Installation and Deployment
### System Dependencies
- Install Python 3.10 or higher.
- Install uv
  - MacOS/Linux
  ```text
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  - Windows
  ```text
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### Environment Variables
| Environment Variable Name | Description | Default Value | Acquisition Method |
| --- | --- | --- | --- |
| VOLCENGINE_ACCESS_KEY | Volcengine Account ACCESS KEY | - | [Volcengine Access Console](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_SECRET_KEY | Volcengine Account SECRET KEY | - | [Volcengine Access Console](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_REGION | Volcengine Region | cn-beijing | - |

### Deployment
UV
```json
{
  "mcpServers": {
    "mcp_server_vmp": {
      "command": "uv",
      "env": {
        "VOLCENGINE_ACCESS_KEY":"Your Volcengine access key",
        "VOLCENGINE_SECRET_KEY":"Your Volcengine secret key"
      },
      "args": [
        "--directory",
        "/<your local path to mcp-servers>/server/mcp_server_vmp",
        "run",
        "mcp-server-vmp"
      ]
    }
  }
}
```
UVX
```json
{
  "mcpServers": {
    "mcp_server_vmp": {
      "command": "uvx",
      "env": {
        "VOLCENGINE_ACCESS_KEY":"Your Volcengine access key",
        "VOLCENGINE_SECRET_KEY":"Your Volcengine secret key"
      },
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vmp",
        "mcp-server-vmp"
      ]
    }
  }
}
```

# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)


