# MCP Server Product Name: VMP MCP Server ![Product Logo](./logo.svg)

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

### Tool 1: list_workspaces

#### Type
SaaS

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

### Tool 2: query_metrics

#### Type
SaaS

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
                "description": "Query time, in RFC3339 format or Unix timestamp, default is the current time.",
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

### Tool 3: query_range_metrics

#### Type
SaaS

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
                "description": "Query step, in duration format, optional. If not provided, it will be automatically calculated based on the query time range.",
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

### Tool 4: query_metric_names

#### Type
SaaS

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
                "description": "Series Selector, used to filter the matching metric range, following the standard Prometheus Vector Selector syntax, e.g.: {job=~\"kubelet\"}",
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

### Tool 5: query_metric_labels

#### Type
SaaS

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

### Deployment
UV
```json
{
  "mcpServers": {
    "mcp_server_vmp": {
      "command": "uv",
      "env": {
        "VOLC_ACCESSKEY":"Your Volcengine access key",
        "VOLC_SECRETKEY":"Your Volcengine secret key"
      },
      "args": [
        "--directory",
        "/<your local path to mcp-servers>/mcp_server_vmp/src/mcp_server_vmp",
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
        "VOLC_ACCESSKEY":"Your Volcengine access key",
        "VOLC_SECRETKEY":"Your Volcengine secret key"
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


