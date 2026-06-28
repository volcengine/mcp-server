# APMPlus MCP Server

The MCP Server officially launched by the Application Performance Monitoring service can accurately convert natural language into observable analysis statements. It efficiently analyzes observable data including metrics, traces, and logs, helping you comprehensively ensure the entire lifecycle of your applications and improve the efficiency of troubleshooting and problem-solving.

| Version |                                              v0.2.0                                               |
| :-: |:-------------------------------------------------------------------------------------------------:|
| Description | The APMPlus MCP Server helps you comprehensively ensure the entire lifecycle of your applications |
| Category |                                           Observability                                           |
| Tags |                   Observability, Traces, Metrics, Logs, Performance Monitoring                    |

## Tools
This MCP Server product provides the following Tools (capabilities):
### 1. apmplus_server_list_alert_rule
Query the alert rules from APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `region`: [str, optional] Region ID. Defaults to cn-beijing.
  - `keyword`: [str, optional] Search keyword. Defaults to "".
  - `page_number`: [int, optional] Page number for pagination. Defaults to 1.
  - `page_size`: [int, optional] Page size for pagination. Defaults to 10.

### 2. apmplus_server_list_notify_group
Query the notification group information from APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `region`: [str, optional] Region ID. Defaults to cn-beijing.
  - `keyword`: [str, optional] Search keyword. Defaults to "".
  - `page_number`: [int, optional] Page number for pagination. Defaults to 1.
  - `page_size`: [int, optional] Page size for pagination. Defaults to 10.

### 3. apmplus_server_query_metrics
Query the metrics from APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `region`: [str, optional] Region ID. Defaults to cn-beijing.
  - `query`: [str] Metric expression, in PromQL format
  - `start_time`: [int] Start time, in seconds
  - `end_time`: [int] End time, in seconds

### 4. apmplus_server_get_trace_detail
Get trace detail information from APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `trace_id`: [str, optional] Trace ID.
  - `suggest_time`: [int, optional] Suggest time in seconds.
  - `region`: [str, optional] Region ID. Defaults to cn-beijing.

### 5. apmplus_server_list_span
Get a list of trace span from APMPlus - Server Monitoring in a specified region.
- Parameters:
  - `start_time`: [int] Start time in seconds, example: 1693536000
  - `end_time`: [int] End time in seconds, example: 1693546000
  - `filters`: [list[dict], optional] Filter expression.
                                    Each dict contains:
                                  - 'Op' (str): in, not_in
                                  - 'Key' (str): Filter key
                                  - 'Values' (list[str]): Filter values
  - `order`: [str, optional] Order direction. Defaults to DESC.
  - `order_by`: [str, optional] Order by field. Defaults to "".
  - `offset`: [int, optional] Offset for pagination. Defaults to 0.
  - `limit`: [int, optional] Limit for pagination. Defaults to 10.
  - `min_call_cost_millisecond`: [int, optional] Minimum call cost in milliseconds. Defaults to 0.
  - `max_call_cost_millisecond`: [int, optional] Maximum call cost in milliseconds. Defaults to 0.
  - `project_name`: [str, optional] The project name.
  - `tag_filters`: [list[dict], optional] List of tag filters. Each dict contains:
                                             - 'Key' (str): Tag key
                                             - 'Value' (list[str]): Tag value
                                             Max 10 tag pairs.
                                             Empty value means no restriction on tag value.
  - `region`: [str, optional] Region ID. Defaults to cn-beijing.

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