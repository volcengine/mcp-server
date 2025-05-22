# APMPlus MCP Server

The MCP Server officially launched by the Application Performance Monitoring service can accurately convert natural language into observable analysis statements. It efficiently analyzes observable data including metrics, traces, and logs, helping you comprehensively ensure the entire lifecycle of your applications and improve the efficiency of troubleshooting and problem-solving.

| Version | v0.1.0 |
| :-: |:----------------:|
| Description | The APMPlus MCP Server helps you comprehensively ensure the entire lifecycle of your applications |
| Category | Observability |
| Tags | Observability, Traces, Metrics, Logs, Performance Monitoring |

## Tools
This MCP Server product provides the following Tools (capabilities):
### 1. apmplus_server_list_alert_rule
Query the alert rules for APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `region_id`: [str] Region ID
  - `keyword`: [str] Search keyword
  - `page_number`: [int] Page number for pagination
  - `page_size`: [int] Page size for pagination

### 2. apmplus_server_list_notify_group
Query the notification group information for APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `region_id`: [str] Region ID
  - `keyword`: [str] Search keyword
  - `page_number`: [int] Page number for pagination
  - `page_size`: [int] Page size for pagination

### 3. apmplus_server_query_metrics
Query the metrics for APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `region_id`: [str] Region ID
  - `query`: [str] Metric expression, in PromQL format
  - `start_time`: [int] Start time, in seconds
  - `end_time`: [int] End time, in seconds

## Compatible Platforms
You can use cline, cursor, claude desktop, or other terminals that support MCP server calls.

## Service Activation Link
https://console.volcengine.com/apmplus-server

## Installation and Deployment
Obtain your AK/SK from [volcengine](https://www.volcengine.com/docs/6291/65568), then add the AK/SK to the MCP server configuration, or configure them in the `.env` file in your working directory with the following format:
```shell
VOLCENGINE_ACCESS_KEY=your_volcengine_ak
VOLCENGINE_SECRET_KEY=your_volcengine_sk

## Using uv
Add the following configuration to your MCP settings file:
```json
{
  "mcpServers": {
    "mcp-server-apmplus": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_apmplus",
        "mcp-server-apmplus"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```
Or clone the repository locally and start it from the local code repository:
```json
{
  "mcpServers": {
    "mcp-server-apmplus": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/src/mcp_server_apmplus",
        "run",
        "server.py"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```

## License
[MIT](https://github.com/volcengine/mcp-server/blob/main/LICENSE)