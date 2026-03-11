# Metrics MCP Server ![Product Logo](./logo.svg)

Volcengine Metrics Service is a comprehensive metrics management and monitoring system that provides extensive metrics collection, storage, querying, and visualization capabilities. Metrics MCP Server offers functions such as metrics querying, dashboard management, and data analysis, facilitating natural language-driven metrics management and analysis experience in operation troubleshooting, data analysis, and other scenarios.

<table>
  <tr>
    <td>Version</td>
    <td>v0.1.0</td>
  </tr>
  <tr>
    <td>Description</td>
    <td>Natural language-driven query and management of Volcengine Metrics data</td>
  </tr>
  <tr>
    <td>Category</td>
    <td>Observability</td>
  </tr>
  <tr>
    <td>Tags</td>
    <td>Metrics, Monitoring, Observability</td>
  </tr>
</table>

## Tools

This MCP Server product provides the following Tools (functions/capabilities):

### Tool 1: metrics_list_workspace

#### Detailed Description

Query all workspace instances information under the current account in the specified region.

#### Input parameters required for debugging:

Input:

```json
{
    "name": "metrics_list_workspace",
    "description": "Query all Metrics workspace instances information in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "page_number": {
                "default": 1,
                "description": "Page number for pagination",
                "type": "integer"
            },
            "page_size": {
                "default": 10,
                "description": "Page size for pagination",
                "type": "integer"
            },
            "name": {
                "description": "Workspace name for filtering",
                "type": "string"
            }
        },
        "required": [
	    "region"
	]
    }
}
```

Output:

- List of workspaces with metadata

#### Example Prompt most likely to trigger

Please list all workspace instances information in the cn-beijing region.

### Tool 2: metrics_get_workspace_info

#### Detailed Description

Query details of a specific workspace under the current account in the specified region.

#### Input parameters required for debugging:

Input:

```json
{
    "name": "metrics_get_workspace_info",
    "description": "Query details of a specific workspace in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace_id": {
                "description": "Workspace ID",
                "type": "string"
            }
        },
        "required": [
            "region",
            "workspace_id"
        ]
    }
}
```

Output:

- Workspace details information

#### Example Prompt most likely to trigger

Please get workspace information with ID "test-workspace-id" in the cn-beijing region.

### Tool 3: metrics_list_query_clusters

#### Detailed Description

Query all query clusters information under the current account in the specified region.

#### Input parameters required for debugging:

Input:

```json
{
    "name": "metrics_list_query_clusters",
    "description": "Query all query clusters information under the current account in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "page_number": {
                "default": 1,
                "description": "Page number for pagination",
                "type": "integer"
            },
            "page_size": {
                "default": 10,
                "description": "Page size for pagination",
                "type": "integer"
            },
            "name": {
                "description": "Query cluster name for filtering",
                "type": "string"
            }
        },
        "required": [
            "region"
        ]
    }
}
```

Output:

- List of query clusters with metadata

#### Example Prompt most likely to trigger

Please list all query clusters in the cn-beijing region.

### Tool 4: metrics_get_query_cluster

#### Detailed Description

Query details of a specific query cluster under the current account in the specified region.

#### Input parameters required for debugging:

Input:

```json
{
    "name": "metrics_get_query_cluster",
    "description": "Query details of a specific query cluster in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "cluster_id": {
                "description": "Query cluster ID",
                "type": "string"
            }
        },
        "required": [
            "region",
            "cluster_id"
        ]
    }
}
```

Output:

- Query cluster details information

#### Example Prompt most likely to trigger

Please get query cluster information with ID "test-cluster-id" in the cn-beijing region.

### Tool 5: metrics_list_preagg

#### Detailed Description

Query all preaggregation rules in the specified workspace under the current account in the specified region.

#### Input parameters required for debugging:

Input:

```json
{
    "name": "metrics_list_preagg",
    "description": "Query all preaggregation rules in the specified workspace under the current account in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace_name": {
                "description": "Workspace name",
                "type": "string"
            },
            "page_number": {
                "default": 1,
                "description": "Page number for pagination",
                "type": "integer"
            },
            "page_size": {
                "default": 10,
                "description": "Page size for pagination",
                "type": "integer"
            },
            "only_show_mine": {
                "default": true,
                "description": "Whether to only show rules created by current user",
                "type": "boolean"
            }
        },
        "required": [
            "region",
            "workspace_name"
        ]
    }
}
```

Output:

- List of preaggregation rules with metadata

#### Example Prompt most likely to trigger

Please get all preaggregation rules in workspace named "test_workspace_name" in the cn-beijing region.

### Tool 6: metrics_influx_query

#### Detailed Description

Query InfluxDB metrics data from the specified workspace under the current account in the specified region.

#### Input parameters required for debugging:

Input:

```json
{
    "name": "metrics_influx_query",
    "description": "Query InfluxDB metrics data from the specified workspace under the current account in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace": {
                "description": "Workspace name",
                "type": "string"
            },
            "queries": {
                "description": "List of InfluxQL query strings",
                "type": "array",
                "items": {"type": "string"}
            },
            "epoch": {
                "description": "Timestamp precision (s/ms/us/ns)",
                "type": "string"
            }
        },
        "required": [
            "region",
            "workspace",
            "queries"
        ]
    }
}
```

Output:

- Query data results

#### Example Prompt most likely to trigger

Please query CPU usage in the last 30 minutes using InfluxQL in workspace named "test_workspace_name" in the cn-beijing region.

### Tool 7: metrics_query

#### Detailed Description

Query Metrics/OpenTSDB metrics data from the specified workspace under the current account in the specified region.

#### Input parameters required for debugging:

Input:

```json
{
    "name": "metrics_query",
    "description": "Query Metrics/OpenTSDB metrics data from the specified workspace under the current account in the specified region",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "Target region(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace": {
                "description": "Workspace name",
                "type": "string"
            },
            "queries": {
                "description": "List of query configuration details",
                "type": "array",
                "items": {"type": "object"}
            },
            "start": {
                "default": "10m-ago",
                "description": "Query start time",
                "type": "string"
            },
            "end": {
                "default": "now",
                "description": "Query end time",
                "type": "string"
            }
        },
        "required": [
            "region",
            "workspace",
            "queries"
        ]
    }
}
```

Output:

- Metrics query results

#### Example Prompt most likely to trigger

Please query CPU usage metrics in the last 30 minutes using Metrics/OpenTSDB protocol in workspace named "test_workspace_name" in the cn-beijing region.

## Compatible Platforms

Ark, Trae, Cursor, Claude Desktop or other terminals that support MCP Server calls.

## Service Activation Link (Overall Product)

https://console.volcengine.com/cloud-monitor/metrics

## Authentication Method

API Key ([Signature Mechanism](https://www.volcengine.com/docs/6731/942192))

## Installation and Deployment

### System Dependencies

- Install Python 3.10 or higher
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
    "mcp_server_metrics": {
      "command": "uv",
      "env": {
        "VOLCENGINE_ACCESS_KEY":"Your Volcengine access key",
        "VOLCENGINE_SECRET_KEY":"Your Volcengine secret key"
      },
      "args": [
        "--directory",
        "/<your local path to mcp-servers>/server/mcp_server_metrics",
        "run",
        "mcp-server-metrics"
      ]
    }
  }
}
```

UVX

```json
{
  "mcpServers": {
    "mcp_server_metrics": {
      "command": "uvx",
      "env": {
        "VOLCENGINE_ACCESS_KEY":"Your Volcengine access key",
        "VOLCENGINE_SECRET_KEY":"Your Volcengine secret key"
      },
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_metrics",
        "mcp-server-metrics"
      ]
    }
  }
}
```

# License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)