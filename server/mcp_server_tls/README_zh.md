# TLS MCP Server

日志服务官方推出的 MCP Server，可以将自然语言精准转化为日志分析语句，高效分析日志。操作便捷，上手快，适用于运维排查、数据分析等场景，为你轻松解锁日志服务的无限可能

| 版本 | v0.1.0 |
| :-: | :-: |
| 描述 | 自然语言驱动日志分析新体验 |
| 分类 | 云基础-存储 |
| 标签 | 日志，可观测，数据飞轮 |

## Tools

### Tool 1: search_logs_v2_tool

该工具允许您使用多种查询类型搜索日志，包括全文检索、键值搜索和SQL查询。它提供灵活的时间范围过滤和限制选项来定制搜索结果,默认时间为15分钟。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["query"],
    "properties": {
      "query": {
        "type": "string",
        "description": "日志查询语句"
      },
      "topic_id": {
        "type": "string",
        "description": "可选的日志主题ID, 默认为环境变量中设置的topic_id,如果没有设置,则必传"
      },
      "start_time": {
        "type": "integer",
        "description": "查询起始时间，Unix 时间戳（秒/毫秒）"
      },
      "end_time": {
        "type": "integer",
        "description": "查询结束时间，Unix 时间戳（秒/毫秒）"
      },
      "limit": {
        "type": "integer",
        "description": "返回的最大日志条数，默认值为 10"
      }
    }
  },
  "name": "search_logs_v2",
  "description": "根据日志查询语句，在指定日志主题和时间范围内查询日志"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112195)

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

- 最容易被唤起的 Prompt示例

使用search_logs_v2_tool工具帮我查询下query为"__content__: error"的前十条日志

### Tool 2: text2sql

将用户输入的查询语言转为TLS定义的SQL查询语句,如果查询语言比较模糊,可能会有询问.

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["question"],
    "properties": {
      "question": {
        "type": "string",
        "description": "用户输入的查询语言"
      },
      "topic_id": {
        "type": "string",
        "description": "可选的日志主题ID, 默认为环境变量中设置的topic_id,如果没有设置,则必传"
      },
      "session_id": {
        "type": "string",
        "description": "可选的tls copilot的会话id"
      },
    }
  },
  "name": "text2sql",
  "description": "将用户输入的查询语言转为TLS定义的SQL查询语句"
}
```

`输出`

```json
{
    "answer": "ai给出的返回结果,包含推理过程",
    "Suggestions": ["ai返回的建议,比如查询字段不明确时,可能给出询问"],
    "session_id": "服务端返回的当前与tls copilot会话id"
}
```

- 最容易被唤起的 Prompt示例

使用text2sql工具生成一个sql,用于查询__content__字段中包含error的日志数量

### Tool 3: describe_project_tool

获取当前权限下指定项目id下的项目信息

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "可选的日志项目ID, 默认为环境变量中设置的project_id,如果没有设置,则必传"
      },
    }
  },
  "name": "describe_project_tool",
  "description": "获取当前权限下指定项目id下的项目信息"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112178)

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

- 最容易被唤起的 Prompt示例

使用describe_project_tool工具帮我查下project_id为xxx的项目名是什么

### Tool 4: describe_projects_tool

获取当前权限下的多个项目信息

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {}
  },
  "name": "describe_projects_tool",
  "description": "获取当前权限下的多个项目信息"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112179)

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

- 最容易被唤起的 Prompt示例

使用describe_projects_tool工具帮我查下前十个项目名是什么

### Tool 5: describe_topic_tool

获取当前权限下指定主题id的主题信息

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "可选的日志主题ID, 默认为环境变量中设置的topic_id,如果没有设置,则必传"
      },
    }
  },
  "name": "describe_topic_tool",
  "description": "获取当前权限下指定主题id的主题信息"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112184)

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

- 最容易被唤起的 Prompt示例

使用describe_topic_tool工具帮我查下当前主题的分片数量

### Tool 6: describe_topics_tool

获取当前权限下指定项目ID的主题信息

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "可选的日志项目ID, 默认为环境变量中设置的project_id,如果没有设置,则必传"
      },
    }
  },
  "name": "describe_topics_tool",
  "description": "获取当前权限下指定project_id下的多个主题信息"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112185)

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

- 最容易被唤起的 Prompt示例

使用describe_topics_tool工具帮我查下当前项目下前10个项目的分区数量.

### Tool 7: put_logs_v2_tool

上传日志到指定的日志主题中。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["logs"],
    "properties": {
      "logs": {
        "type": "array",
        "description": "logs字段为要写入的日志字段，数组中每个item即为一条日志，每个item由多个key-value键值对组成"
      },
      "log_time": {
        "type": "int",
        "description": "写入日志的日志时间戳，默认为当前时间",
      },
      "topic_id": {
        "type": "string",
        "description": "可选的日志主题ID, 默认为环境变量中设置的topic_id,如果没有设置,则必传"
      },
      "source": {
        "type": "string",
        "description": "日志来源，通常使用机器 IP 作为标识",
      },
      "filename": {
        "type": "string",
        "description": "日志文件名",
      },
      "hash_key": {
        "type": "string",
        "description": "日志组的 HashKey，用于指定当前日志组要写入的分区（Shard）",
      },
      "compression": {
        "type": "string",
        "description": "请求体的压缩格式，默认为lz4，可选zlib",
      },
    }
  },
  "name": "put_logs_v2_tool",
  "description": "调用 PutLogs 接口上传日志到指定的日志主题中，如需使用searchLogs查询日志，请先设置好索引"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112191)

```json
{
    "request_id": "your_request_id"
}
```

- 最容易被唤起的 Prompt示例

使用put_logs_v2_tool工具帮我写入以下日志如[{"user": "peter", "age": 18}, {"user": "marry", "age": 16}]

### Tool 8: create_alarm_notify_group_tool

创建告警通知组，用于配置告警接收人和通知方式。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["alarm_notify_group_name", "notify_type", "receivers"],
    "properties": {
      "alarm_notify_group_name": {
        "type": "string",
        "description": "告警通知组名称"
      },
      "notify_type": {
        "type": "array",
        "description": "通知类型，支持'Trigger'和'Recovery'",
        "items": {
          "type": "string"
        }
      },
      "receivers": {
        "type": "array",
        "description": "接收人信息列表",
        "items": {
          "type": "object",
          "properties": {
            "receiver_type": {"type": "string", "description": "接收人类型，如'User'"},
            "receiver_names": {"type": "array", "description": "接收人名称列表"},
            "receiver_channels": {"type": "array", "description": "通知渠道，如['Email', 'Sms', 'Phone']"},
            "start_time": {"type": "string", "description": "通知开始时间"},
            "end_time": {"type": "string", "description": "通知结束时间"},
            "webhook": {"type": "string", "description": "Webhook URL"}
          }
        }
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM项目名称"
      }
    }
  },
  "name": "create_alarm_notify_group_tool",
  "description": "创建告警通知组"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112220)

```json
{
  "alarm_notify_group_id": "告警通知组ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_alarm_notify_group_tool工具创建名为"运维团队"的告警通知组，接收人通过邮件通知

### Tool 9: describe_alarm_notify_groups_tool

查询告警通知组列表，支持多种过滤条件和分页。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "alarm_notify_group_name": {
        "type": "string",
        "description": "告警通知组名称过滤"
      },
      "alarm_notify_group_id": {
        "type": "string",
        "description": "告警通知组ID过滤"
      },
      "receiver_name": {
        "type": "string",
        "description": "接收人名称过滤"
      },
      "page_number": {
        "type": "integer",
        "description": "页码，默认为1"
      },
      "page_size": {
        "type": "integer",
        "description": "每页数量，默认为20，最大100"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM项目名称过滤"
      }
    }
  },
  "name": "describe_alarm_notify_groups_tool",
  "description": "查询告警通知组列表"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112223)

```json
{
  "total": 10,
  "alarm_notify_groups": [
    {
      "alarm_notify_group_id": "通知组ID",
      "alarm_notify_group_name": "通知组名称",
      "notify_type": ["Trigger", "Recovery"],
      "receivers": [],
      "create_time": "创建时间",
      "modify_time": "修改时间"
    }
  ]
}
```

- 最容易被唤起的 Prompt示例

使用describe_alarm_notify_groups_tool工具查询前10个告警通知组

### Tool 10: create_alarm_tool

创建告警策略，用于监控日志并触发告警。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["project_id", "alarm_name", "query_request", "request_cycle", "condition", "alarm_period", "alarm_notify_group"],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "日志项目ID"
      },
      "alarm_name": {
        "type": "string",
        "description": "告警策略名称"
      },
      "query_request": {
        "type": "array",
        "description": "查询请求列表",
        "items": {
          "type": "object",
          "properties": {
            "topic_id": {"type": "string", "description": "日志主题ID"},
            "query": {"type": "string", "description": "查询语句"},
            "number": {"type": "integer", "description": "告警对象序号"},
            "start_time_offset": {"type": "integer", "description": "查询起始时间偏移(分钟)"},
            "end_time_offset": {"type": "integer", "description": "查询结束时间偏移(分钟)"},
            "time_span_type": {"type": "string", "description": "时间类型"},
            "truncated_time": {"type": "string", "description": "时间截断"}
          }
        }
      },
      "request_cycle": {
        "type": "object",
        "description": "请求周期配置",
        "properties": {
          "cycle_type": {"type": "string", "description": "周期类型：Period或Fixed"},
          "time": {"type": "integer", "description": "周期时间(分钟)"},
          "cron_tab": {"type": "string", "description": "Cron表达式"}
        }
      },
      "condition": {
        "type": "string",
        "description": "告警触发条件"
      },
      "alarm_period": {
        "type": "integer",
        "description": "告警周期(分钟)"
      },
      "alarm_notify_group": {
        "type": "array",
        "description": "告警通知组ID列表",
        "items": {"type": "string"}
      },
      "status": {"type": "boolean", "description": "是否启用告警"},
      "trigger_period": {"type": "integer", "description": "触发周期"},
      "user_define_msg": {"type": "string", "description": "自定义消息"},
      "severity": {"type": "string", "description": "告警级别"},
      "alarm_period_detail": {"type": "object", "description": "告警周期详细配置"},
      "join_configurations": {"type": "array", "description": "关联配置"},
      "trigger_conditions": {"type": "array", "description": "触发条件"}
    }
  },
  "name": "create_alarm_tool",
  "description": "创建告警策略"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112216)

```json
{
  "alarm_id": "告警策略ID",
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_alarm_tool工具创建告警策略，当错误日志数量超过100时触发告警

### Tool 11: describe_alarms_tool

查询告警策略列表，支持多种过滤条件和分页。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "日志项目ID"
      },
      "alarm_name": {
        "type": "string",
        "description": "告警策略名称过滤"
      },
      "alarm_id": {
        "type": "string",
        "description": "告警策略ID过滤"
      },
      "topic_name": {
        "type": "string",
        "description": "主题名称过滤"
      },
      "topic_id": {
        "type": "string",
        "description": "主题ID过滤"
      },
      "status": {
        "type": "boolean",
        "description": "告警状态过滤"
      },
      "page_number": {
        "type": "integer",
        "description": "页码，默认为1"
      },
      "page_size": {
        "type": "integer",
        "description": "每页数量，默认为20，最大100"
      }
    }
  },
  "name": "describe_alarms_tool",
  "description": "查询告警策略列表"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112219)

```json
{
  "total": 10,
  "alarms": [
    {
      "alarm_id": "告警策略ID",
      "alarm_name": "告警策略名称",
      "project_id": "项目ID",
      "status": true,
      "severity": "告警级别",
      "condition": "触发条件",
      "create_time": "创建时间",
      "modify_time": "修改时间"
    }
  ]
}
```

- 最容易被唤起的 Prompt示例

使用describe_alarms_tool工具查询当前项目下的所有告警策略

### Tool 12: create_download_task_tool

创建日志下载任务，用于导出指定条件的日志数据。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["query", "task_name", "start_time", "end_time", "format_type", "sort", "limit"],
    "properties": {
      "query": {
        "type": "string",
        "description": "日志查询语句"
      },
      "task_name": {
        "type": "string",
        "description": "下载任务名称"
      },
      "start_time": {
        "type": "integer",
        "description": "查询起始时间，Unix时间戳（秒/毫秒）"
      },
      "end_time": {
        "type": "integer",
        "description": "查询结束时间，Unix时间戳（秒/毫秒）"
      },
      "format_type": {
        "type": "string",
        "description": "导出格式：csv或json"
      },
      "sort": {
        "type": "string",
        "description": "排序方式"
      },
      "limit": {
        "type": "integer",
        "description": "导出日志数量限制"
      },
      "topic_id": {
        "type": "string",
        "description": "可选的日志主题ID，默认为环境变量中设置的topic_id"
      },
      "compression": {
        "type": "string",
        "description": "压缩格式，默认为gzip"
      }
    }
  },
  "name": "create_download_task_tool",
  "description": "创建日志下载任务"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/142119)

```json
{
  "task_id": "任务ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_download_task_tool工具创建任务导出包含错误的日志，格式为CSV

### Tool 13: describe_download_tasks_tool

查询日志下载任务列表，支持分页和任务名称过滤。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "可选的日志主题ID，默认为环境变量中设置的topic_id"
      },
      "page_number": {
        "type": "integer",
        "description": "页码，默认为1"
      },
      "page_size": {
        "type": "integer",
        "description": "每页数量，默认为20，最大100"
      },
      "task_name": {
        "type": "string",
        "description": "任务名称过滤，支持模糊搜索"
      }
    }
  },
  "name": "describe_download_tasks_tool",
  "description": "查询日志下载任务列表"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/142120)

```json
{
  "total": 10,
  "tasks": [
    {
      "task_id": "任务ID",
      "task_name": "任务名称",
      "topic_id": "主题ID",
      "query": "查询语句",
      "start_time": "起始时间",
      "end_time": "结束时间",
      "format_type": "格式类型",
      "status": "任务状态",
      "create_time": "创建时间",
      "modify_time": "修改时间"
    }
  ]
}
```

- 最容易被唤起的 Prompt示例

使用describe_download_tasks_tool工具查询当前主题的所有下载任务

### Tool 14: describe_download_url_tool

获取日志下载任务的下载URL。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["task_id"],
    "properties": {
      "task_id": {
        "type": "string",
        "description": "下载任务ID"
      }
    }
  },
  "name": "describe_download_url_tool",
  "description": "获取日志下载URL"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/142122)

```json
{
  "download_url": "下载URL"
}
```

- 最容易被唤起的 Prompt示例

使用describe_download_url_tool工具获取任务task-123的下载URL

### Tool 15: create_host_group_tool

创建主机组，用于管理日志收集的主机。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_name", "host_group_type"],
    "properties": {
      "host_group_name": {
        "type": "string",
        "description": "主机组名称"
      },
      "host_group_type": {
        "type": "string",
        "description": "主机组类型：'IP'或'Label'"
      },
      "host_ip_list": {
        "type": "array",
        "description": "主机IP地址列表，当类型为'IP'时必填"
      },
      "host_identifier": {
        "type": "string",
        "description": "主机标识符，当类型为'Label'时必填"
      },
      "auto_update": {
        "type": "boolean",
        "description": "是否启用自动更新，默认为false"
      },
      "update_start_time": {
        "type": "string",
        "description": "更新开始时间，格式为HH:MM"
      },
      "update_end_time": {
        "type": "string",
        "description": "更新结束时间，格式为HH:MM"
      },
      "service_logging": {
        "type": "boolean",
        "description": "是否启用服务日志，默认为false"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM项目名称"
      }
    }
  },
  "name": "create_host_group_tool",
  "description": "创建主机组"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112206)

```json
{
  "host_group_id": "主机组ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_host_group_tool工具创建名为"Web服务器"的IP类型主机组

### Tool 16: describe_host_groups_tool

查询主机组列表，支持多种过滤条件和分页。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "主机组ID过滤"
      },
      "host_group_name": {
        "type": "string",
        "description": "主机组名称过滤"
      },
      "page_number": {
        "type": "integer",
        "description": "页码，默认为1"
      },
      "page_size": {
        "type": "integer",
        "description": "每页数量，默认为20，最大100"
      },
      "auto_update": {
        "type": "boolean",
        "description": "自动更新状态过滤"
      },
      "host_identifier": {
        "type": "string",
        "description": "主机标识符过滤"
      },
      "service_logging": {
        "type": "boolean",
        "description": "服务日志状态过滤"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM项目名称过滤"
      }
    }
  },
  "name": "describe_host_groups_tool",
  "description": "查询主机组列表"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112211)

```json
{
  "total": 10,
  "host_groups": [
    {
      "host_group_id": "主机组ID",
      "host_group_name": "主机组名称",
      "host_group_type": "主机组类型",
      "create_time": "创建时间",
      "modify_time": "修改时间",
      "host_count": "主机数量"
    }
  ]
}
```

- 最容易被唤起的 Prompt示例

使用describe_host_groups_tool工具查询所有主机组

### Tool 17: create_rule_tool

创建日志收集规则，配置日志收集路径和解析方式。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_name"],
    "properties": {
      "rule_name": {
        "type": "string",
        "description": "收集规则名称"
      },
      "topic_id": {
        "type": "string",
        "description": "日志主题ID"
      },
      "paths": {
        "type": "array",
        "description": "收集路径列表"
      },
      "log_type": {
        "type": "string",
        "description": "日志类型，默认为minimalist_log"
      },
      "extract_rule": {
        "type": "object",
        "description": "日志提取规则配置"
      },
      "exclude_paths": {
        "type": "array",
        "description": "排除路径配置"
      },
      "user_define_rule": {
        "type": "object",
        "description": "用户自定义规则配置"
      },
      "log_sample": {
        "type": "string",
        "description": "日志样例"
      },
      "input_type": {
        "type": "integer",
        "description": "输入类型：0主机文件，1K8s标准输出，2K8s容器文件"
      },
      "container_rule": {
        "type": "object",
        "description": "容器收集规则"
      }
    }
  },
  "name": "create_rule_tool",
  "description": "创建日志收集规则"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112199)

```json
{
  "rule_id": "规则ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_rule_tool工具创建收集路径为/var/log/nginx/*.log的日志收集规则

### Tool 18: create_index_tool

为日志主题创建索引配置，支持全文检索和键值索引。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "日志主题ID"
      },
      "full_text": {
        "type": "object",
        "description": "全文检索配置",
        "properties": {
          "delimiter": {"type": "string", "description": "分词符"},
          "case_sensitive": {"type": "boolean", "description": "是否区分大小写"},
          "include_chinese": {"type": "boolean", "description": "是否支持中文"}
        }
      },
      "key_value": {
        "type": "array",
        "description": "键值索引配置列表",
        "items": {
          "type": "object",
          "properties": {
            "key": {"type": "string", "description": "字段名称"},
            "value_type": {"type": "string", "description": "数据类型"},
            "delimiter": {"type": "string", "description": "分词符"},
            "case_sensitive": {"type": "boolean", "description": "是否区分大小写"},
            "include_chinese": {"type": "boolean", "description": "是否支持中文"},
            "sql_flag": {"type": "boolean", "description": "是否启用SQL查询"},
            "index_all": {"type": "boolean", "description": "是否索引所有值"}
          }
        }
      },
      "user_inner_key_value": {
        "type": "array",
        "description": "用户内部键值索引配置"
      }
    }
  },
  "name": "create_index_tool",
  "description": "创建日志主题索引"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112187)

```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_index_tool工具为主题创建全文检索和status字段的键值索引

### Tool 19: describe_index_tool

查询日志主题的索引配置信息。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "日志主题ID"
      }
    }
  },
  "name": "describe_index_tool",
  "description": "查询日志主题索引配置"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112190)

```json
{
  "topic_id": "主题ID",
  "full_text": {"全文检索配置"},
  "key_value": [{"键值索引配置"}],
  "user_inner_key_value": [{"用户内部键值索引"}],
  "create_time": "创建时间",
  "modify_time": "修改时间"
}
```

- 最容易被唤起的 Prompt示例

使用describe_index_tool工具查询当前主题的索引配置

### Tool 20: consume_logs_tool

从指定分片中消费日志数据。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["shard_id", "cursor"],
    "properties": {
      "shard_id": {
        "type": "integer",
        "description": "分片ID"
      },
      "cursor": {
        "type": "string",
        "description": "消费游标位置"
      },
      "topic_id": {
        "type": "string",
        "description": "日志主题ID"
      },
      "end_cursor": {
        "type": "string",
        "description": "结束游标位置"
      },
      "log_group_count": {
        "type": "integer",
        "description": "返回日志组数量限制"
      },
      "compression": {
        "type": "string",
        "description": "压缩格式，支持lz4/zlib"
      },
      "consumer_group_name": {
        "type": "string",
        "description": "消费组名称"
      },
      "consumer_name": {
        "type": "string",
        "description": "消费者名称"
      }
    }
  },
  "name": "consume_logs_tool",
  "description": "从指定分片消费日志"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112194)

```json
{
  "pb_message": [{"日志组数据"}],
  "x_tls_count": "日志组数量",
  "x_tls_cursor": "下一个游标位置"
}
```

- 最容易被唤起的 Prompt示例

使用consume_logs_tool工具从分片0的指定游标位置消费日志

### Tool 21: describe_cursor_tool

获取分片在指定时间点的游标位置。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["shard_id", "from_time"],
    "properties": {
      "shard_id": {
        "type": "integer",
        "description": "分片ID"
      },
      "from_time": {
        "type": "string",
        "description": "时间点，可以是Unix时间戳(秒)或'begin'/'end'"
      },
      "topic_id": {
        "type": "string",
        "description": "日志主题ID"
      }
    }
  },
  "name": "describe_cursor_tool",
  "description": "获取分片游标位置"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112193)

```json
{
  "cursor": "游标位置"
}
```

- 最容易被唤起的 Prompt示例

使用describe_cursor_tool工具获取分片0在开始位置的游标

### Tool 22: describe_log_context_tool

获取指定日志条目的上下文日志信息。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["context_flow", "package_offset", "source"],
    "properties": {
      "context_flow": {
        "type": "string",
        "description": "日志组ID"
      },
      "package_offset": {
        "type": "integer",
        "description": "日志在日志组中的序号"
      },
      "source": {
        "type": "string",
        "description": "日志来源主机IP"
      },
      "topic_id": {
        "type": "string",
        "description": "日志主题ID"
      },
      "prev_logs": {
        "type": "integer",
        "description": "包含的前置日志数量，默认为10"
      },
      "next_logs": {
        "type": "integer",
        "description": "包含的后置日志数量，默认为10"
      }
    }
  },
  "name": "describe_log_context_tool",
  "description": "获取日志上下文"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/125689)

```json
{
  "prev_over": true,
  "next_over": true,
  "log_context_infos": "日志上下文信息"
}
```

- 最容易被唤起的 Prompt示例

使用describe_log_context_tool工具获取指定日志前后20条的上下文日志

### Tool 23: create_project_tool

创建新的日志项目。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["project_name"],
    "properties": {
      "project_name": {
        "type": "string",
        "description": "项目名称"
      },
      "region": {
        "type": "string",
        "description": "区域信息"
      },
      "description": {
        "type": "string",
        "description": "项目描述"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM项目名称"
      },
      "tags": {
        "type": "array",
        "description": "项目标签信息"
      }
    }
  },
  "name": "create_project_tool",
  "description": "创建日志项目"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112174)

```json
{
  "project_id": "项目ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_project_tool工具创建名为"生产环境日志"的项目

### Tool 24: create_topic_tool

创建新的日志主题。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["topic_name"],
    "properties": {
      "topic_name": {
        "type": "string",
        "description": "主题名称"
      },
      "project_id": {
        "type": "string",
        "description": "项目ID"
      },
      "ttl": {
        "type": "integer",
        "description": "日志保存时间(天)，默认为30"
      },
      "shard_count": {
        "type": "integer",
        "description": "分区数量，默认为2，范围1-10"
      },
      "description": {
        "type": "string",
        "description": "主题描述"
      },
      "auto_split": {
        "type": "boolean",
        "description": "是否启用自动分裂，默认为true"
      },
      "max_split_shard": {
        "type": "integer",
        "description": "自动分裂最大分区数，默认为50"
      },
      "enable_tracking": {
        "type": "boolean",
        "description": "是否启用WebTracking，默认为false"
      },
      "time_key": {
        "type": "string",
        "description": "时间字段名称"
      },
      "time_format": {
        "type": "string",
        "description": "时间字段解析格式"
      },
      "tags": {
        "type": "array",
        "description": "主题标签"
      },
      "log_public_ip": {
        "type": "boolean",
        "description": "是否记录公网IP，默认为true"
      },
      "enable_hot_ttl": {
        "type": "boolean",
        "description": "是否启用冷热归档，默认为false"
      },
      "hot_ttl": {
        "type": "integer",
        "description": "热数据保存时间"
      },
      "cold_ttl": {
        "type": "integer",
        "description": "冷数据保存时间"
      },
      "archive_ttl": {
        "type": "integer",
        "description": "归档数据保存时间"
      }
    }
  },
  "name": "create_topic_tool",
  "description": "创建日志主题"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112180)

```json
{
  "topic_id": "主题ID"
}
```

- 最容易被唤起的 Prompt示例

使用create_topic_tool工具创建名为"应用日志"的主题，TTL为90天，分区数为3

### Tool 25: delete_alarm_notify_group_tool

删除指定的告警通知组。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["alarm_notify_group_id"],
    "properties": {
      "alarm_notify_group_id": {
        "type": "string",
        "description": "告警通知组ID"
      }
    }
  },
  "name": "delete_alarm_notify_group_tool",
  "description": "删除告警通知组"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112221)

```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_alarm_notify_group_tool工具删除ID为notify-group-123的告警通知组

### Tool 26: delete_alarm_tool

删除指定的告警策略。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["alarm_id"],
    "properties": {
      "alarm_id": {
        "type": "string",
        "description": "告警策略ID"
      }
    }
  },
  "name": "delete_alarm_tool",
  "description": "删除告警策略"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112217)

```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_alarm_tool工具删除ID为alarm-123的告警策略

### Tool 27: delete_host_group_tool

删除指定的主机组。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "主机组ID"
      }
    }
  },
  "name": "delete_host_group_tool",
  "description": "删除主机组"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112208)

```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_host_group_tool工具删除ID为host-group-123的主机组

### Tool 28: describe_host_group_tool

查询指定主机组的详细信息。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "主机组ID"
      }
    }
  },
  "name": "describe_host_group_tool",
  "description": "查询主机组详情"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112210)


```json
{
  "host_group_id": "主机组ID",
  "host_group_name": "主机组名称",
  "host_group_type": "主机组类型",
  "host_ip_list": ["主机IP列表"],
  "host_identifier": "主机标识符",
  "auto_update": "是否自动更新",
  "service_logging": "是否启用服务日志",
  "create_time": "创建时间",
  "modify_time": "修改时间"
}
```

- 最容易被唤起的 Prompt示例

使用describe_host_group_tool工具查询ID为host-group-123的主机组详情

### Tool 29: describe_hosts_tool

查询指定主机组中的主机列表。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "主机组ID"
      },
      "ip": {
        "type": "string",
        "description": "主机IP过滤"
      },
      "heartbeat_status": {
        "type": "integer",
        "description": "心跳状态过滤"
      },
      "page_number": {
        "type": "integer",
        "description": "页码，默认为1"
      },
      "page_size": {
        "type": "integer",
        "description": "每页数量，默认为20，最大100"
      }
    }
  },
  "name": "describe_hosts_tool",
  "description": "查询主机组中的主机列表"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112212)


```json
{
  "total": 10,
  "hosts": [
    {
      "ip": "主机IP",
      "heartbeat_status": "心跳状态",
      "last_heartbeat_time": "最后心跳时间",
      "create_time": "创建时间",
      "modify_time": "修改时间"
    }
  ]
}
```

- 最容易被唤起的 Prompt示例

使用describe_hosts_tool工具查询主机组host-group-123中的所有主机

### Tool 30: describe_host_group_rules_tool

查询指定主机组关联的日志收集规则列表。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["host_group_id"],
    "properties": {
      "host_group_id": {
        "type": "string",
        "description": "主机组ID"
      },
      "page_number": {
        "type": "integer",
        "description": "页码，默认为1"
      },
      "page_size": {
        "type": "integer",
        "description": "每页数量，默认为20，最大100"
      }
    }
  },
  "name": "describe_host_group_rules_tool",
  "description": "查询主机组关联的规则"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112214)


```json
{
  "total": 5,
  "rules": [
    {
      "rule_id": "规则ID",
      "rule_name": "规则名称",
      "topic_id": "主题ID",
      "topic_name": "主题名称",
      "create_time": "创建时间",
      "modify_time": "修改时间"
    }
  ]
}
```

- 最容易被唤起的 Prompt示例

使用describe_host_group_rules_tool工具查询主机组host-group-123关联的所有规则

### Tool 31: delete_rule_tool

删除指定的日志收集规则。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "规则ID"
      }
    }
  },
  "name": "delete_rule_tool",
  "description": "删除日志收集规则"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112200)


```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_rule_tool工具删除ID为rule-123的日志收集规则

### Tool 32: describe_rule_tool

查询指定日志收集规则的详细信息。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "规则ID"
      }
    }
  },
  "name": "describe_rule_tool",
  "description": "查询日志收集规则详情"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112202)



```json
{
  "rule_id": "规则ID",
  "rule_name": "规则名称",
  "project_id": "项目ID",
  "topic_id": "主题ID",
  "paths": ["收集路径列表"],
  "log_type": "日志类型",
  "extract_rule": {"提取规则配置"},
  "exclude_paths": ["排除路径列表"],
  "user_define_rule": {"用户自定义规则"},
  "create_time": "创建时间",
  "modify_time": "修改时间"
}
```

- 最容易被唤起的 Prompt示例

使用describe_rule_tool工具查询ID为rule-123的规则详情

### Tool 33: describe_rules_tool

查询日志收集规则列表，支持多种过滤条件和分页。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": [],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "项目ID"
      },
      "project_name": {
        "type": "string",
        "description": "项目名称"
      },
      "iam_project_name": {
        "type": "string",
        "description": "IAM项目名称"
      },
      "rule_id": {
        "type": "string",
        "description": "规则ID过滤"
      },
      "rule_name": {
        "type": "string",
        "description": "规则名称过滤"
      },
      "topic_id": {
        "type": "string",
        "description": "主题ID过滤"
      },
      "topic_name": {
        "type": "string",
        "description": "主题名称过滤"
      },
      "page_number": {
        "type": "integer",
        "description": "页码，默认为1"
      },
      "page_size": {
        "type": "integer",
        "description": "每页数量，默认为20，最大100"
      },
      "log_type": {
        "type": "string",
        "description": "日志类型过滤"
      },
      "pause": {
        "type": "integer",
        "description": "暂停状态过滤"
      }
    }
  },
  "name": "describe_rules_tool",
  "description": "查询日志收集规则列表"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112203)


```json
{
  "total": 20,
  "rules": [
    {
      "rule_id": "规则ID",
      "rule_name": "规则名称",
      "project_id": "项目ID",
      "topic_id": "主题ID",
      "topic_name": "主题名称",
      "log_type": "日志类型",
      "pause": "暂停状态",
      "create_time": "创建时间",
      "modify_time": "修改时间"
    }
  ]
}
```

- 最容易被唤起的 Prompt示例

使用describe_rules_tool工具查询当前项目下的所有日志收集规则

### Tool 34: apply_rule_to_host_groups_tool

将日志收集规则应用到指定的主机组。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id", "host_group_ids"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "规则ID"
      },
      "host_group_ids": {
        "type": "array",
        "description": "主机组ID列表",
        "items": {
          "type": "string"
        }
      }
    }
  },
  "name": "apply_rule_to_host_groups_tool",
  "description": "应用规则到主机组"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112204)


```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用apply_rule_to_host_groups_tool工具将规则rule-123应用到主机组host-group-1和host-group-2

### Tool 35: delete_rule_from_host_groups_tool

从指定的主机组中删除日志收集规则。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["rule_id", "host_group_ids"],
    "properties": {
      "rule_id": {
        "type": "string",
        "description": "规则ID"
      },
      "host_group_ids": {
        "type": "array",
        "description": "主机组ID列表",
        "items": {
          "type": "string"
        }
      }
    }
  },
  "name": "delete_rule_from_host_groups_tool",
  "description": "从主机组删除规则"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112205)


```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_rule_from_host_groups_tool工具从主机组中删除规则rule-123

### Tool 36: delete_index_tool

删除指定日志主题的索引配置。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["topic_id"],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "日志主题ID"
      }
    }
  },
  "name": "delete_index_tool",
  "description": "删除日志主题索引"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112188)


```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_index_tool工具删除主题topic-123的索引配置

### Tool 37: delete_project_tool

删除指定的日志项目。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["project_id"],
    "properties": {
      "project_id": {
        "type": "string",
        "description": "项目ID"
      }
    }
  },
  "name": "delete_project_tool",
  "description": "删除日志项目"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112176)


```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_project_tool工具删除ID为project-123的日志项目

### Tool 38: delete_topic_tool

删除指定的日志主题。

- 调试所需的输入参数:

`输入`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["topic_id"],
    "properties": {
      "topic_id": {
        "type": "string",
        "description": "主题ID"
      }
    }
  },
  "name": "delete_topic_tool",
  "description": "删除日志主题"
}
```

`输出`
    - [参考文档](https://www.volcengine.com/docs/6470/112182)


```json
{
  "request_id": "请求ID"
}
```

- 最容易被唤起的 Prompt示例

使用delete_topic_tool工具删除ID为topic-123的日志主题

## 可适配平台

可以使用cline、cursor、claude desktop或支持MCP server调用的其它终端

## 服务开通链接

[开通tls服务](https://console.volcengine.com/tls), 未开通的用户会自动重定向到开通页. 如果已经开通,则会跳转首页

## 鉴权方式

API Key ([签名机制](https://www.volcengine.com/docs/6470/112168))

## 安装部署

### 系统依赖

- 安装 Python 3.10 或者更高版本
- 安装 uv

```
mv .env_example .env
```

请在.env文件中设置相关环境变量

如果是本地部署,可以设置PROJECT_ID、TOPIC_ID、ACCOUNT_ID等,用于当作工具的默认参数

如果是Server化部署,需设置DEPLOY_MODE=remote,且仅设置REGION、ENDPOINT

## 安装

### 本地启动

#### 1. 通过本地代码启动

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

#### 2. 通过远端仓库启动

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

### 远端启动

#### 部署远端服务

##### 1. 本地直接启动

设置 `DEPLOY_MODE=remote`

```shell
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER run mcp-server-tls -t sse
```

or

```shell
uv --directory /ABSOLUTE/PATH/TO/PARENT/FOLDER run mcp-server-tls -t streamable-http
```

> 我们建议使用streamable-http

##### 2. 通过DOCKER启动

我们也提供了DOCKERFILE方便大家部署，暂时未推送到开源库，可以先手动打包

docker compose 启动示例:

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

#### 调用

|transport-type|调用链接示例|
| :-: | :-: |
| sse | http://127.0.0.1:8000/sse |
| streamable-http | http://127.0.0.1:8000/mcp |

调用方使用时请将认证信息按照以下格式通过base64编码后放在请求头的authorization中

```json
{
    "AccessKeyId": "your ak",
    "SecretAccessKey": "your sk",
    "SessionToken": "your token",
    "Region": "your region",
    "Endpoint": "your endpoint"
}
```

`Region`和`Endpoint`不是必传的, 默认的region是`cn-beijing`, endpoint是`https://tls-cn-beijing.volces.com`

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).


