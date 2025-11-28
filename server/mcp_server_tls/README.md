# TLS MCP Server

The official MCP Server for the logging service can accurately convert natural language into log analysis statements, enabling efficient log analysis. It is easy to use, quick to get started, and suitable for scenarios such as operations troubleshooting and data analysis, unlocking the unlimited potential of the logging service for you.

| Version | v0.1.0 |
| :-: | :-: |
| Description | A new experience of natural language-driven log analysis |
| Category | Cloud Basics - Storage |
| Tags | Logs, Observability, Data Flywheel |

## Tools

### Tool 1: search_logs_v2_tool

This tool allows you to search logs using various query types, including full-text search, key-value search, and SQL queries. It provides flexible time range filtering and limit options to customize search results, with a default time range of 15 minutes.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["query"],
    "properties": {
      "query": {
        "type": "string",
        "description": "Log query statement"
      },
      "topic_id": {
        "type": "string",
        "description": "Optional log topic ID, defaults to the topic_id set in the environment variable, if not set, this parameter is required"
      },
      "start_time": {
        "type": "integer",
        "description": "Query start time, Unix timestamp (seconds/milliseconds)"
      },
      "end_time": {
        "type": "integer",
        "description": "Query end time, Unix timestamp (seconds/milliseconds)"
      },
      "limit": {
        "type": "integer",
        "description": "Maximum number of logs to return, default value is 10"
      }
    }
  },
  "name": "search_logs_v2",
  "description": "Query logs within a specified log topic and time range based on a log query statement"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112195)

```json
{
  "result_status": "complete",
  "hit_count": 1,
  "list_over": false,
  "analysis": false,
  "count": 1,
  "limit": 10,
  "context": "",
  "logs": [
    {
      "__container_ip__": "127.0.0.1",
      "__container_name__": "tls container name",
      "__content__": "log content",
      "__context_flow__": "",
      "__image_name__": "image name",
      "__namespace__": "namespace",
      "__package_offset__": "package offset",
      "__path__": "your log path",
      "__pod_name__": "tls pod name",
      "__pod_uid__": "tls pod uid",
      "__source__": "your ip",
      "__tag____client_ip__": "client ip",
      "__tag____receive_time__": "log receive time",
      "__time__": 1745029622660
    }
  ],
  "analysis_result": {
    "analysis_schema": [],
    "analysis_type": {},
    "analysis_data": []
  },
  "elapsed_millisecond": 666
}
```

- Example of the most easily triggered prompt:

Use the search_logs_v2_tool to help me query the top 10 logs with the query "__content__: error"

### Tool 2: text2sql

Converts user input queries into TLS-defined SQL query statements. If the query is ambiguous, further clarification may be requested.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["question"],
    "properties": {
      "question": {
        "type": "string",
        "description": "User input query language"
      },
      "topic_id": {
        "type": "string",
        "description": "Optional log topic ID, defaults to the topic_id set in the environment variable, if not set, this parameter is required"
      },
      "session_id": {
        "type": "string",
        "description": "Optional session ID for TLS Copilot"
      },
    }
  },
  "name": "text2sql",
  "description": "Converts user input queries into TLS-defined SQL query statements"
}
```

`Output`

```json
{
    "answer": "AI-generated response, including reasoning process",
    "Suggestions": ["AI-generated suggestions, such as clarifications for ambiguous queries"],
    "session_id": "Session ID returned by the server for the current TLS Copilot session"
}
```

- Example of the most easily triggered prompt:

Use the text2sql tool to generate an SQL query to count logs where the "__content__" field contains "error"

### Tool 3: describe_project_tool

Retrieves project information for a specified project ID under the current permissions.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "Optional log project ID, defaults to the project_id set in the environment variable, if not set, this parameter is required"
      },
    }
  },
  "name": "describe_project_tool",
  "description": "Retrieves project information for a specified project ID under the current permissions"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112178)

```json
{
    "project_name": "your project_name",
    "project_id": "your project id",
    "description": "your project description",
    "create_time": "2025-04-18 18:00:00",
    "inner_net_domain": "https://tls-cn-beijing.ivolces.com",
    "topic_count": 1,
    "iam_project_name": "default",
    "tags": null,
    "public_net_domain": "https://tls-cn-beijing.volces.com",
    "cs_account_channel": ""
}
```

- Example of the most easily triggered prompt:

Use the describe_project_tool to find the project name for project_id xxx

### Tool 4: describe_projects_tool

Retrieves information for multiple projects under the current permissions.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {}
  },
  "name": "describe_projects_tool",
  "description": "Retrieves information for multiple projects under the current permissions"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112179)

```json
{
    "total": 1,
    "projects": [
        "project_name": "your project_name",
        "project_id": "your project id",
        "description": "your project description",
        "create_time": "2025-04-18 18:00:00",
        "inner_net_domain": "https://tls-cn-beijing.ivolces.com",
        "topic_count": 1,
        "iam_project_name": "default",
        "tags": null,
        "public_net_domain": "https://tls-cn-beijing.volces.com",
        "cs_account_channel": ""
    ]
}
```

- Example of the most easily triggered prompt:

Use the describe_projects_tool to find the names of the first 10 projects

### Tool 5: describe_topic_tool

Retrieves topic information for a specified topic ID under the current permissions.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "Optional log topic ID, defaults to the topic_id set in the environment variable, if not set, this parameter is required"
      },
    }
  },
  "name": "describe_topic_tool",
  "description": "Retrieves topic information for a specified topic ID under the current permissions"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112184)

```json
{
  "topic_name": "your topic name",
  "topic_id": "your topic id",
  "project_id": "your project id",
  "ttl": 30,
  "create_time": "2022-06-22 16:05:27",
  "modify_time": "2025-03-10 17:19:54",
  "shard_count": 6,
  "description": "",
  "auto_split": false,
  "max_split_shard": 0,
  "enable_tracking": false,
  "time_key": "",
  "time_format": "",
  "tags": null,
  "log_public_ip": true,
  "enable_hot_ttl": false,
  "hot_ttl": 0,
  "cold_ttl": 0,
  "archive_ttl": 0
}
```

- Example of the most easily triggered prompt:

Use the describe_topic_tool to find the shard count for the current topic

### Tool 6: describe_topics_tool

Retrieves information for multiple topics under a specified project ID within the current permissions.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "Optional log project ID, defaults to the project_id set in the environment variable, if not set, this parameter is required"
      },
    }
  },
  "name": "describe_topics_tool",
  "description": "Retrieves information for multiple topics under a specified project ID within the current permissions"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112185)

```json
{
  "total": 1,
  "topics": [
    {
        "topic_name": "your topic name",
        "topic_id": "your topic id",
        "project_id": "your project id",
        "ttl": 30,
        "create_time": "2022-06-22 16:05:27",
        "modify_time": "2025-03-10 17:19:54",
        "shard_count": 6,
        "description": "",
        "auto_split": false,
        "max_split_shard": 0,
        "enable_tracking": false,
        "time_key": "",
        "time_format": "",
        "tags": null,
        "log_public_ip": true,
        "enable_hot_ttl": false,
        "hot_ttl": 0,
        "cold_ttl": 0,
        "archive_ttl": 0
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_topics_tool to find the shard count for the first 10 topics under the current project

### Tool 7: put_logs_v2_tool

Upload logs to the specified log topic.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["logs"],
    "properties": {
      "logs": {
        "type": "array",
        "description": "The logs field contains the log fields to be written, each item in the array is a log, and each item consists of multiple key-value pairs"
      },
      "log_time": {
        "type": "int",
        "description": "Log timestamp for writing to the log, defaults to current time",
      },
      "topic_id": {
        "type": "string",
        "description": "Optional log topic ID, defaults to the topic_id set in the environment variable, if not set, this parameter is required"
      },
      "source": {
        "type": "string",
        "description": "Log source, usually identified by machine IP",
      },
      "filename": {
        "type": "string",
        "description": "Log file name",
      },
      "hash_key": {
        "type": "string",
        "description": "HashKey of the log group, used to specify the partition (Shard) to which the current log group is to be written",
      },
      "compression": {
        "type": "string",
        "description": "Compression format of the request body, defaults to lz4, optional zlib",
      },
    }
  },
  "name": "put_logs_v2_tool",
  "description": "Call the PutLogs interface to upload logs to the specified log topic. If you need to use searchLogs to query the logs, please set up the index first"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112191)

```json
{
    "request_id": "your_request_id"
}
```

- Example of the most easily triggered prompt:

Use the put_logs_v2_tool to help me write the following logs as [{"user": "peter", "age": 18}, {"user": "marry", "age": 16}]

### Tool 8: create_alarm_notify_group_tool

Create an alarm notification group for configuring alert recipients and notification methods.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["alarm_notify_group_name", "notify_type", "receivers"],
    "properties": {
      "alarm_notify_group_name": {
        "type": "string",
        "description": "Alarm notification group name"
      },
      "notify_type": {
        "type": "array",
        "description": "Notification types, supports 'Trigger' and 'Recovery'",
        "items": {
          "type": "string"
        }
      },
      "receivers": {
        "type": "array",
        "description": "List of receiver information",
        "items": {
          "type": "object",
          "properties": {
            "receiver_type": {"type": "string", "description": "Receiver type, e.g., 'User'"},
            "receiver_names": {"type": "array", "description": "List of receiver names"},
            "receiver_channels": {"type": "array", "description": "Notification channels, e.g., ['Email', 'Sms', 'Phone']"},
            "start_time": {"type": "string", "description": "Notification start time"},
            "end_time": {"type": "string", "description": "Notification end time"},
            "webhook": {"type": "string", "description": "Webhook URL"}
          }
        }
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM project name"
      }
    }
  },
  "name": "create_alarm_notify_group_tool",
  "description": "Create an alarm notification group"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112220)

```json
{
  "alarm_notify_group_id": "Alarm notification group ID"
}
```

- Example of the most easily triggered prompt:

Use the create_alarm_notify_group_tool to create an alarm notification group named "ops-team" with email notification recipients

### Tool 9: describe_alarm_notify_groups_tool

Query alarm notification group list with various filtering conditions and pagination support.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "alarm_notify_group_name": {
        "type": "string",
        "description": "Alarm notification group name filter"
      },
      "alarm_notify_group_id": {
        "type": "string",
        "description": "Alarm notification group ID filter"
      },
      "receiver_name": {
        "type": "string",
        "description": "Receiver name filter"
      },
      "page_number": {
        "type": "integer",
        "description": "Page number, defaults to 1"
      },
      "page_size": {
        "type": "integer",
        "description": "Number per page, defaults to 20, maximum 100"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM project name filter"
      }
    }
  },
  "name": "describe_alarm_notify_groups_tool",
  "description": "Query alarm notification group list"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112223)

```json
{
  "total": 10,
  "alarm_notify_groups": [
    {
      "alarm_notify_group_id": "Notification group ID",
      "alarm_notify_group_name": "Notification group name",
      "notify_type": ["Trigger", "Recovery"],
      "receivers": [],
      "create_time": "Creation time",
      "modify_time": "Modification time"
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_alarm_notify_groups_tool to query the first 10 alarm notification groups

### Tool 10: create_alarm_tool

Create an alarm policy for monitoring logs and triggering alerts.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["project_id", "alarm_name", "query_request", "request_cycle", "condition", "alarm_period", "alarm_notify_group"],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "Log project ID"
      },
      "alarm_name": {
        "type": "string",
        "description": "Alarm policy name"
      },
      "query_request": {
        "type": "array",
        "description": "Query request list",
        "items": {
          "type": "object",
          "properties": {
            "topic_id": {"type": "string", "description": "Log topic ID"},
            "query": {"type": "string", "description": "Query statement"},
            "number": {"type": "integer", "description": "Alert object sequence number"},
            "start_time_offset": {"type": "integer", "description": "Query start time offset (minutes)"},
            "end_time_offset": {"type": "integer", "description": "Query end time offset (minutes)"},
            "time_span_type": {"type": "string", "description": "Time type"},
            "truncated_time": {"type": "string", "description": "Time truncation"}
          }
        }
      },
      "request_cycle": {
        "type": "object",
        "description": "Request cycle configuration",
        "properties": {
          "cycle_type": {"type": "string", "description": "Cycle type: Period or Fixed"},
          "time": {"type": "integer", "description": "Cycle time (minutes)"},
          "cron_tab": {"type": "string", "description": "Cron expression"}
        }
      },
      "condition": {
        "type": "string",
        "description": "Alarm trigger condition"
      },
      "alarm_period": {
        "type": "integer",
        "description": "Alarm period (minutes)"
      },
      "alarm_notify_group": {
        "type": "array",
        "description": "Alarm notification group ID list",
        "items": {"type": "string"}
      },
      "status": {"type": "boolean", "description": "Whether to enable alarm"},
      "trigger_period": {"type": "integer", "description": "Trigger period"},
      "user_define_msg": {"type": "string", "description": "Custom message"},
      "severity": {"type": "string", "description": "Alarm severity level"},
      "alarm_period_detail": {"type": "object", "description": "Detailed alarm period configuration"},
      "join_configurations": {"type": "array", "description": "Join configurations"},
      "trigger_conditions": {"type": "array", "description": "Trigger conditions"}
    }
  },
  "name": "create_alarm_tool",
  "description": "Create an alarm policy"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112216)

```json
{
  "alarm_id": "Alarm policy ID",
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the create_alarm_tool to create an alarm policy that triggers when the number of error logs exceeds 100

### Tool 11: describe_alarms_tool

Query alarm policy list with various filtering conditions and pagination support.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "Log project ID"
      },
      "alarm_name": {
        "type": "string",
        "description": "Alarm policy name filter"
      },
      "alarm_id": {
        "type": "string",
        "description": "Alarm policy ID filter"
      },
      "topic_name": {
        "type": "string",
        "description": "Topic name filter"
      },
      "topic_id": {
        "type": "string",
        "description": "Topic ID filter"
      },
      "status": {
        "type": "boolean",
        "description": "Alarm status filter"
      },
      "page_number": {
        "type": "integer",
        "description": "Page number, defaults to 1"
      },
      "page_size": {
        "type": "integer",
        "description": "Number per page, defaults to 20, maximum 100"
      }
    }
  },
  "name": "describe_alarms_tool",
  "description": "Query alarm policy list"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112219)

```json
{
  "total": 10,
  "alarms": [
    {
      "alarm_id": "Alarm policy ID",
      "alarm_name": "Alarm policy name",
      "project_id": "Project ID",
      "status": true,
      "severity": "Alarm severity level",
      "condition": "Trigger condition",
      "create_time": "Creation time",
      "modify_time": "Modification time"
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_alarms_tool to query all alarm policies under the current project

### Tool 12: create_download_task_tool

Create a download task for exporting log data based on specified conditions.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["query", "task_name", "start_time", "end_time", "format_type", "sort", "limit"],
    "properties": {
      "query": {
        "type": "string",
        "description": "Log query statement"
      },
      "task_name": {
        "type": "string",
        "description": "Download task name"
      },
      "start_time": {
        "type": "integer",
        "description": "Query start time, Unix timestamp (seconds/milliseconds)"
      },
      "end_time": {
        "type": "integer",
        "description": "Query end time, Unix timestamp (seconds/milliseconds)"
      },
      "format_type": {
        "type": "string",
        "description": "Export format: csv or json"
      },
      "sort": {
        "type": "string",
        "description": "Sort order"
      },
      "limit": {
        "type": "integer",
        "description": "Export log quantity limit"
      },
      "topic_id": {
        "type": "string",
        "description": "Optional log topic ID, defaults to the topic_id set in the environment variable"
      },
      "compression": {
        "type": "string",
        "description": "Compression format, defaults to gzip"
      }
    }
  },
  "name": "create_download_task_tool",
  "description": "Create a log download task"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/142119)

```json
{
  "task_id": "Task ID"
}
```

- Example of the most easily triggered prompt:

Use the create_download_task_tool to create a task for exporting logs containing errors in CSV format

### Tool 13: describe_download_tasks_tool

Query log download task list with pagination and task name filtering support.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "Optional log topic ID, defaults to the topic_id set in the environment variable"
      },
      "page_number": {
        "type": "integer",
        "description": "Page number, defaults to 1"
      },
      "page_size": {
        "type": "integer",
        "description": "Number per page, defaults to 20, maximum 100"
      },
      "task_name": {
        "type": "string",
        "description": "Task name filter, supports fuzzy search"
      }
    }
  },
  "name": "describe_download_tasks_tool",
  "description": "Query log download task list"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/142120)

```json
{
  "total": 10,
  "tasks": [
    {
      "task_id": "Task ID",
      "task_name": "Task name",
      "topic_id": "Topic ID",
      "query": "Query statement",
      "start_time": "Start time",
      "end_time": "End time",
      "format_type": "Format type",
      "status": "Task status",
      "create_time": "Creation time",
      "modify_time": "Modification time"
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_download_tasks_tool to query all download tasks for the current topic

### Tool 14: describe_download_url_tool

Get the download URL for a log download task.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["task_id"],
    "properties": {
      "task_id": {
        "type": "string",
        "description": "Download task ID"
      }
    }
  },
  "name": "describe_download_url_tool",
  "description": "Get log download URL"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/142122)

```json
{
  "download_url": "Download URL"
}
```

- Example of the most easily triggered prompt:

Use the describe_download_url_tool to get the download URL for task task-123

### Tool 15: create_host_group_tool

Create a host group for managing log collection hosts.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_name", "host_group_type"],
    "properties": {
      "host_group_name": {
        "type": "string",
        "description": "Host group name"
      },
      "host_group_type": {
        "type": "string",
        "description": "Host group type: 'IP' or 'Label'"
      },
      "host_ip_list": {
        "type": "array",
        "description": "List of host IP addresses, required when type is 'IP'"
      },
      "host_identifier": {
        "type": "string",
        "description": "Host identifier, required when type is 'Label'"
      },
      "auto_update": {
        "type": "boolean",
        "description": "Whether to enable automatic update, defaults to false"
      },
      "update_start_time": {
        "type": "string",
        "description": "Update start time, format HH:MM"
      },
      "update_end_time": {
        "type": "string",
        "description": "Update end time, format HH:MM"
      },
      "service_logging": {
        "type": "boolean",
        "description": "Whether to enable service logging, defaults to false"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM project name"
      }
    }
  },
  "name": "create_host_group_tool",
  "description": "Create a host group"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112206)

```json
{
  "host_group_id": "Host group ID"
}
```

- Example of the most easily triggered prompt:

Use the create_host_group_tool to create an IP-type host group named "Web Servers"

### Tool 16: describe_host_groups_tool

Query host group list with various filtering conditions and pagination support.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "Host group ID filter"
      },
      "host_group_name": {
        "type": "string",
        "description": "Host group name filter"
      },
      "page_number": {
        "type": "integer",
        "description": "Page number, defaults to 1"
      },
      "page_size": {
        "type": "integer",
        "description": "Number per page, defaults to 20, maximum 100"
      },
      "auto_update": {
        "type": "boolean",
        "description": "Auto update status filter"
      },
      "host_identifier": {
        "type": "string",
        "description": "Host identifier filter"
      },
      "service_logging": {
        "type": "boolean",
        "description": "Service logging status filter"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM project name filter"
      }
    }
  },
  "name": "describe_host_groups_tool",
  "description": "Query host group list"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112211)

```json
{
  "total": 10,
  "host_groups": [
    {
      "host_group_id": "Host group ID",
      "host_group_name": "Host group name",
      "host_group_type": "Host group type",
      "create_time": "Creation time",
      "modify_time": "Modification time",
      "host_count": "Host count"
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_host_groups_tool to query all host groups

### Tool 17: create_rule_tool

Create a log collection rule for configuring log collection paths and parsing methods.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_name"],
    "properties": {
      "rule_name": {
        "type": "string",
        "description": "Collection rule name"
      },
      "topic_id": {
        "type": "string",
        "description": "Log topic ID"
      },
      "paths": {
        "type": "array",
        "description": "Collection path list"
      },
      "log_type": {
        "type": "string",
        "description": "Log type, defaults to minimalist_log"
      },
      "extract_rule": {
        "type": "object",
        "description": "Log extraction rule configuration"
      },
      "exclude_paths": {
        "type": "array",
        "description": "Exclude path configuration"
      },
      "user_define_rule": {
        "type": "object",
        "description": "User-defined rule configuration"
      },
      "log_sample": {
        "type": "string",
        "description": "Log sample"
      },
      "input_type": {
        "type": "integer",
        "description": "Input type: 0 for host file, 1 for K8s stdout, 2 for K8s container file"
      },
      "container_rule": {
        "type": "object",
        "description": "Container collection rule"
      }
    }
  },
  "name": "create_rule_tool",
  "description": "Create a log collection rule"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112199)

```json
{
  "rule_id": "Rule ID"
}
```

- Example of the most easily triggered prompt:

Use the create_rule_tool to create a log collection rule with collection path /var/log/nginx/*.log

### Tool 18: create_index_tool

Create index configuration for a log topic, supporting full-text search and key-value indexing.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "Log topic ID"
      },
      "full_text": {
        "type": "object",
        "description": "Full-text search configuration",
        "properties": {
          "delimiter": {"type": "string", "description": "Word delimiter"},
          "case_sensitive": {"type": "boolean", "description": "Case sensitive"},
          "include_chinese": {"type": "boolean", "description": "Chinese support"}
        }
      },
      "key_value": {
        "type": "array",
        "description": "Key-value index configuration list",
        "items": {
          "type": "object",
          "properties": {
            "key": {"type": "string", "description": "Field name"},
            "value_type": {"type": "string", "description": "Data type"},
            "delimiter": {"type": "string", "description": "Word delimiter"},
            "case_sensitive": {"type": "boolean", "description": "Case sensitive"},
            "include_chinese": {"type": "boolean", "description": "Chinese support"},
            "sql_flag": {"type": "boolean", "description": "Enable SQL query"},
            "index_all": {"type": "boolean", "description": "Index all values"}
          }
        }
      },
      "user_inner_key_value": {
        "type": "array",
        "description": "User inner key-value index configuration"
      }
    }
  },
  "name": "create_index_tool",
  "description": "Create log topic index"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112187)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the create_index_tool to create full-text search and key-value index for the status field of a topic

### Tool 19: describe_index_tool

Query index configuration information for a log topic.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "Log topic ID"
      }
    }
  },
  "name": "describe_index_tool",
  "description": "Query log topic index configuration"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112190)

```json
{
  "topic_id": "Topic ID",
  "full_text": {"Full-text search configuration"},
  "key_value": [{"Key-value index configuration"}],
  "user_inner_key_value": [{"User inner key-value index"}],
  "create_time": "Creation time",
  "modify_time": "Modification time"
}
```

- Example of the most easily triggered prompt:

Use the describe_index_tool to query the index configuration of the current topic

### Tool 20: consume_logs_tool

Consume log data from a specified shard.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["shard_id", "cursor"],
    "properties": {
      "shard_id": {
        "type": "integer",
        "description": "Shard ID"
      },
      "cursor": {
        "type": "string",
        "description": "Consumer cursor position"
      },
      "topic_id": {
        "type": "string",
        "description": "Log topic ID"
      },
      "end_cursor": {
        "type": "string",
        "description": "End cursor position"
      },
      "log_group_count": {
        "type": "integer",
        "description": "Limit on the number of log groups to return"
      },
      "compression": {
        "type": "string",
        "description": "Compression format, supports lz4/zlib"
      },
      "consumer_group_name": {
        "type": "string",
        "description": "Consumer group name"
      },
      "consumer_name": {
        "type": "string",
        "description": "Consumer name"
      }
    }
  },
  "name": "consume_logs_tool",
  "description": "Consume logs from specified shard"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112194)

```json
{
  "log_groups": [{"Log group data"}],
  "count": "Number of log groups",
  "cursor": "Next cursor position"
}
```

- Example of the most easily triggered prompt:

Use the consume_logs_tool to consume logs from shard 0 at the specified cursor position

### Tool 21: describe_cursor_tool

Get the cursor position for a shard at a specified time point.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["shard_id", "from_time"],
    "properties": {
      "shard_id": {
        "type": "integer",
        "description": "Shard ID"
      },
      "from_time": {
        "type": "string",
        "description": "Time point, can be Unix timestamp (seconds) or 'begin'/'end'"
      },
      "topic_id": {
        "type": "string",
        "description": "Log topic ID"
      }
    }
  },
  "name": "describe_cursor_tool",
  "description": "Get shard cursor position"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112193)

```json
{
  "cursor": "Cursor position",
  "count": "Number of logs",
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the describe_cursor_tool to get the cursor at the beginning position of shard 0

### Tool 22: describe_log_context_tool

Get context log information for a specified log entry.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["context_flow", "package_offset", "source"],
    "properties": {
      "context_flow": {
        "type": "string",
        "description": "Log group ID"
      },
      "package_offset": {
        "type": "integer",
        "description": "Sequence number of the log in the log group"
      },
      "source": {
        "type": "string",
        "description": "Log source host IP"
      },
      "topic_id": {
        "type": "string",
        "description": "Log topic ID"
      },
      "prev_logs": {
        "type": "integer",
        "description": "Number of previous logs to include, defaults to 10"
      },
      "next_logs": {
        "type": "integer",
        "description": "Number of next logs to include, defaults to 10"
      }
    }
  },
  "name": "describe_log_context_tool",
  "description": "Get log context"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/125689)

```json
{
  "prev_logs": [{"Previous logs"}],
  "next_logs": [{"Next logs"}],
  "context_flow": "Log group ID"
}
```

- Example of the most easily triggered prompt:

Use the describe_log_context_tool to get the context logs 20 before and after the specified log

### Tool 23: create_project_tool

Create a new log project.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["project_name"],
    "properties": {
      "project_name": {
        "type": "string",
        "description": "Project name"
      },
      "region": {
        "type": "string",
        "description": "Region information"
      },
      "description": {
        "type": "string",
        "description": "Project description"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM project name"
      },
      "tags": {
        "type": "array",
        "description": "Project tag information"
      }
    }
  },
  "name": "create_project_tool",
  "description": "Create a log project"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112174)

```json
{
  "project_id": "Project ID",
  "project_name": "Project name",
  "region": "Region",
  "create_time": "Creation time",
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the create_project_tool to create a project named "Production Environment Logs"

### Tool 24: create_topic_tool

Create a new log topic.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["topic_name"],
    "properties": {
      "topic_name": {
        "type": "string",
        "description": "Topic name"
      },
      "project_id": {
        "type": "string",
        "description": "Project ID"
      },
      "ttl": {
        "type": "integer",
        "description": "Log retention time (days), defaults to 30"
      },
      "shard_count": {
        "type": "integer",
        "description": "Number of partitions, defaults to 2, range 1-10"
      },
      "description": {
        "type": "string",
        "description": "Topic description"
      },
      "auto_split": {
        "type": "boolean",
        "description": "Whether to enable automatic splitting, defaults to true"
      },
      "max_split_shard": {
        "type": "integer",
        "description": "Maximum number of partitions after splitting, defaults to 50"
      },
      "enable_tracking": {
        "type": "boolean",
        "description": "Whether to enable WebTracking, defaults to false"
      },
      "time_key": {
        "type": "string",
        "description": "Time field name"
      },
      "time_format": {
        "type": "string",
        "description": "Time field parsing format"
      },
      "tags": {
        "type": "array",
        "description": "Topic tags"
      },
      "log_public_ip": {
        "type": "boolean",
        "description": "Whether to record public IP, defaults to true"
      },
      "enable_hot_ttl": {
        "type": "boolean",
        "description": "Whether to enable hot/cold archiving, defaults to false"
      },
      "hot_ttl": {
        "type": "integer",
        "description": "Hot data retention time"
      },
      "cold_ttl": {
        "type": "integer",
        "description": "Cold data retention time"
      },
      "archive_ttl": {
        "type": "integer",
        "description": "Archive data retention time"
      }
    }
  },
  "name": "create_topic_tool",
  "description": "Create a log topic"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112180)

```json
{
  "topic_id": "Topic ID",
  "topic_name": "Topic name",
  "project_id": "Project ID",
  "ttl": "Retention time",
  "shard_count": "Number of partitions",
  "create_time": "Creation time",
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the create_topic_tool to create a topic named "Application Logs" with TTL of 90 days and 3 partitions

### Tool 25: delete_alarm_notify_group_tool

Delete a specified alarm notification group.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["alarm_notify_group_id"],
    "properties": {
      "alarm_notify_group_id": {
        "type": "string",
        "description": "Alarm notification group ID"
      }
    }
  },
  "name": "delete_alarm_notify_group_tool",
  "description": "Delete alarm notification group"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112221)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_alarm_notify_group_tool to delete the alarm notification group with ID notify-group-123

### Tool 26: delete_alarm_tool

Delete a specified alarm policy.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["alarm_id"],
    "properties": {
      "alarm_id": {
        "type": "string",
        "description": "Alarm policy ID"
      }
    }
  },
  "name": "delete_alarm_tool",
  "description": "Delete alarm policy"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112217)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_alarm_tool to delete the alarm policy with ID alarm-123

### Tool 27: delete_host_group_tool

Delete a specified host group.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "Host group ID"
      }
    }
  },
  "name": "delete_host_group_tool",
  "description": "Delete host group"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112208)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_host_group_tool to delete the host group with ID host-group-123

### Tool 28: describe_host_group_tool

Query detailed information of a specified host group.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "Host group ID"
      }
    }
  },
  "name": "describe_host_group_tool",
  "description": "Query host group details"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112210)

```json
{
  "host_group_id": "Host group ID",
  "host_group_name": "Host group name",
  "host_group_type": "Host group type",
  "host_ip_list": ["Host IP list"],
  "host_identifier": "Host identifier",
  "auto_update": "Whether auto update is enabled",
  "service_logging": "Whether service logging is enabled",
  "create_time": "Creation time",
  "modify_time": "Modification time"
}
```

- Example of the most easily triggered prompt:

Use the describe_host_group_tool to query details of the host group with ID host-group-123

### Tool 29: describe_hosts_tool

Query the list of hosts in a specified host group.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "Host group ID"
      },
      "ip": {
        "type": "string",
        "description": "Host IP filter"
      },
      "heartbeat_status": {
        "type": "integer",
        "description": "Heartbeat status filter"
      },
      "page_number": {
        "type": "integer",
        "description": "Page number, defaults to 1"
      },
      "page_size": {
        "type": "integer",
        "description": "Number per page, defaults to 20, maximum 100"
      }
    }
  },
  "name": "describe_hosts_tool",
  "description": "Query host list in host group"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112212)

```json
{
  "total": 10,
  "hosts": [
    {
      "ip": "Host IP",
      "heartbeat_status": "Heartbeat status",
      "last_heartbeat_time": "Last heartbeat time",
      "create_time": "Creation time",
      "modify_time": "Modification time"
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_hosts_tool to query all hosts in host group host-group-123

### Tool 30: describe_host_group_rules_tool

Query the list of log collection rules associated with a specified host group.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "Host group ID"
      },
      "page_number": {
        "type": "integer",
        "description": "Page number, defaults to 1"
      },
      "page_size": {
        "type": "integer",
        "description": "Number per page, defaults to 20, maximum 100"
      }
    }
  },
  "name": "describe_host_group_rules_tool",
  "description": "Query rules associated with host group"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112214)

```json
{
  "total": 5,
  "rules": [
    {
      "rule_id": "Rule ID",
      "rule_name": "Rule name",
      "topic_id": "Topic ID",
      "topic_name": "Topic name",
      "create_time": "Creation time",
      "modify_time": "Modification time"
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_host_group_rules_tool to query all rules associated with host group host-group-123

### Tool 31: delete_rule_tool

Delete a specified log collection rule.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "Rule ID"
      }
    }
  },
  "name": "delete_rule_tool",
  "description": "Delete log collection rule"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112200)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_rule_tool to delete the log collection rule with ID rule-123

### Tool 32: describe_rule_tool

Query detailed information of a specified log collection rule.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "Rule ID"
      }
    }
  },
  "name": "describe_rule_tool",
  "description": "Query log collection rule details"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112202)

```json
{
  "rule_id": "Rule ID",
  "rule_name": "Rule name",
  "project_id": "Project ID",
  "topic_id": "Topic ID",
  "paths": ["Collection path list"],
  "log_type": "Log type",
  "extract_rule": {"Extraction rule configuration"},
  "exclude_paths": ["Exclude path list"],
  "user_define_rule": {"User-defined rule"},
  "create_time": "Creation time",
  "modify_time": "Modification time"
}
```

- Example of the most easily triggered prompt:

Use the describe_rule_tool to query details of the rule with ID rule-123

### Tool 33: describe_rules_tool

Query log collection rule list with various filtering conditions and pagination support.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "Project ID"
      },
      "project_name": {
        "type": "string",
        "description": "Project name"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM project name"
      },
      "rule_id": {
        "type": "string",
        "description": "Rule ID filter"
      },
      "rule_name": {
        "type": "string",
        "description": "Rule name filter"
      },
      "topic_id": {
        "type": "string",
        "description": "Topic ID filter"
      },
      "topic_name": {
        "type": "string",
        "description": "Topic name filter"
      },
      "page_number": {
        "type": "integer",
        "description": "Page number, defaults to 1"
      },
      "page_size": {
        "type": "integer",
        "description": "Number per page, defaults to 20, maximum 100"
      },
      "log_type": {
        "type": "string",
        "description": "Log type filter"
      },
      "pause": {
        "type": "integer",
        "description": "Pause status filter"
      }
    }
  },
  "name": "describe_rules_tool",
  "description": "Query log collection rule list"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112203)

```json
{
  "total": 20,
  "rules": [
    {
      "rule_id": "Rule ID",
      "rule_name": "Rule name",
      "project_id": "Project ID",
      "topic_id": "Topic ID",
      "topic_name": "Topic name",
      "log_type": "Log type",
      "pause": "Pause status",
      "create_time": "Creation time",
      "modify_time": "Modification time"
    }
  ]
}
```

- Example of the most easily triggered prompt:

Use the describe_rules_tool to query all log collection rules under the current project

### Tool 34: apply_rule_to_host_groups_tool

Apply a log collection rule to specified host groups.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id", "host_group_ids"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "Rule ID"
      },
      "host_group_ids": {
        "type": "array",
        "description": "List of host group IDs",
        "items": {
          "type": "string"
        }
      }
    }
  },
  "name": "apply_rule_to_host_groups_tool",
  "description": "Apply rule to host groups"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112204)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the apply_rule_to_host_groups_tool to apply rule rule-123 to host groups host-group-1 and host-group-2

### Tool 35: delete_rule_from_host_groups_tool

Delete a log collection rule from specified host groups.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id", "host_group_ids"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "Rule ID"
      },
      "host_group_ids": {
        "type": "array",
        "description": "List of host group IDs",
        "items": {
          "type": "string"
        }
      }
    }
  },
  "name": "delete_rule_from_host_groups_tool",
  "description": "Delete rule from host groups"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112205)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_rule_from_host_groups_tool to delete rule rule-123 from host groups

### Tool 36: delete_index_tool

Delete index configuration for a specified log topic.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["topic_id"],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "Log topic ID"
      }
    }
  },
  "name": "delete_index_tool",
  "description": "Delete log topic index"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112188)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_index_tool to delete the index configuration of topic topic-123

### Tool 37: delete_project_tool

Delete a specified log project.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["project_id"],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "Project ID"
      }
    }
  },
  "name": "delete_project_tool",
  "description": "Delete log project"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112176)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_project_tool to delete the log project with ID project-123

### Tool 38: delete_topic_tool

Delete a specified log topic.

- Input parameters required for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["topic_id"],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "Topic ID"
      }
    }
  },
  "name": "delete_topic_tool",
  "description": "Delete log topic"
}
```

`Output`
    - [Reference Documentation](https://www.volcengine.com/docs/6470/112182)

```json
{
  "request_id": "Request ID"
}
```

- Example of the most easily triggered prompt:

Use the delete_topic_tool to delete the log topic with ID topic-123

## Supported Platforms

Can be used with cline, cursor, Claude desktop, or other terminals supporting MCP server calls.

## Service Activation Link

[Activate TLS Service](https://console.volcengine.com/tls). Users who have not activated the service will be redirected to the activation page. If already activated, they will be redirected to the homepage.

## Authentication Method

API Key ([Signature Mechanism](https://www.volcengine.com/docs/6470/112168))

## Installation and Deployment

### System Dependencies

- Install Python 3.10 or higher
- Install uv

```
mv .env_example .env
```

Set relevant environment variables in the `.env` file.

For local deployment, set `PROJECT_ID`, `TOPIC_ID`, `ACCOUNT_ID`, etc., as default parameters for the tools.

For server-based deployment, set `DEPLOY_MODE=remote` and only configure `REGION` and `ENDPOINT`.

## Installation

### Run Locally

#### 1. Launching via local code

```json
{
    "mcpServers": {
        "tls": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/src/mcp_server_tls",
                "run",
                "main.py"
            ]
        }
    }
}
```

#### 2. Launch via remote repository

```json
{
    "mcpServers": {
        "tls": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_tls",
                "mcp-server-tls"
            ],
            "env": {
                "AK": "your ak",
                "SK": "your sk",
                "REGION": "your region",
                "ENDPOINT": "your endpoint",
                "ACCOUNT_ID": "your account id",
                "PROJECT_ID": "your project id",
                "TOPIC_ID": "your topic id"
            }
        }
    }
}
```

### Remote startup

#### Deploying remote services

##### 1. Local direct startup

Set `DEPLOY_MODE=remote`

```shell
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER run mcp-server-tls -t sse
```

or

```shell
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER run mcp-server-tls -t streamable-http
```

> We suggest that using streamable-http

##### 2. Started by DOCKER

We also provide DOCKERFILE to facilitate your deployment, which has not been pushed to the open source repository, so you can manually package it first.

Example of docker compose startup.

```
services:
  mcp:
    image: your-image:your-version
    container_name: mcp_server_tls
    restart: always
    ports:
      - "80:8000"
    environment:
      MCP_DEPLOY_MODE: remote
      TRANSPORT_TYPE: streamable-http
      MCP_SERVER_HOST: 0.0.0.0
      MCP_SERVER_PORT: 8000
```

#### call

|transport-type| call link example |
| :-: | :-: |
| sse | http://127.0.0.1:8000/sse |
| streamable-http | http://127.0.0.1:8000/mcp |

The caller should put the authentication information in the authorization header after encoding it in base64 in the following format

```json
{
    "AccessKeyId": "your ak",
    "SecretAccessKey": "your sk",
    "SessionToken": "your token",
    "Region": "your region",
    "Endpoint": "your endpoint"
}
```

`Region` and `Endpoint` is not necessary, default region is `cn-beijing`, endpoint is `https://tls-cn-beijing.volces.com`

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).