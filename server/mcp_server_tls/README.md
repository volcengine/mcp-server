# TLS MCP Server

The official MCP Server for the logging service can accurately convert natural language into log analysis statements, enabling efficient log analysis. It is easy to use, quick to get started, and suitable for scenarios such as operations troubleshooting and data analysis, unlocking the unlimited potential of the logging service for you.

| Version | v0.1.0 |
| :-: | :-: |
| Description | A new experience of natural language-driven log analysis |
| Category | Cloud Basics - Storage |
| Tags | Logs, Observability, Data Flywheel |

## Tools

### Tool 1: search_logs_v2_tool

This tool allows you to search logs using various query types, including full-text search, key-value search, and SQL queries. It provides flexible time range filtering and limit options to customize search results. The default time range is 15 minutes.

- Required input parameters for debugging:

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
                "description": "Optional log topic ID. Defaults to the topic_id set in the environment variable. If not set, this is required."
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
                "description": "Maximum number of logs to return, default is 10"
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

Use the search_logs_v2_tool to query the top 10 logs with the query "__content__: error".

### Tool 2: text2sql

Converts user input queries into TLS-defined SQL query statements. If the query is ambiguous, further clarification may be requested.

- Required input parameters for debugging:

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
                "description": "Optional log topic ID. Defaults to the topic_id set in the environment variable. If not set, this is required."
            },
            "session_id": {
                "type": "string",
                "description": "Optional session ID for TLS Copilot"
            }
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

Use the text2sql tool to generate an SQL query to count logs where the "__content__" field contains "error".

### Tool 3: describe_project_tool

Retrieve project information for a specified project ID under the current permissions.

- Required input parameters for debugging:

`Input`

```json
{
    "inputSchema": {
        "type": "object",
        "required": [],
        "properties": {
            "project_id": {
                "type": "string",
                "description": "Optional log project ID. Defaults to the project_id set in the environment variable. If not set, this is required."
            }
        }
    },
    "name": "describe_project_tool",
    "description": "Retrieve project information for a specified project ID under the current permissions"
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

Use the describe_project_tool to find the project name for project_id xxx.

### Tool 4: describe_projects_tool

Retrieve information for multiple projects under the current permissions.

- Required input parameters for debugging:

`Input`

```json
{
    "inputSchema": {
        "type": "object",
        "required": [],
        "properties": {}
    },
    "name": "describe_projects_tool",
    "description": "Retrieve information for multiple projects under the current permissions"
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

Use the describe_projects_tool to find the names of the first 10 projects.

### Tool 5: describe_topic_tool

Retrieve topic information for a specified topic ID under the current permissions.

- Required input parameters for debugging:

`Input`

```json
{
    "inputSchema": {
        "type": "object",
        "required": [],
        "properties": {
            "topic_id": {
                "type": "string",
                "description": "Optional log topic ID. Defaults to the topic_id set in the environment variable. If not set, this is required."
            }
        }
    },
    "name": "describe_topic_tool",
    "description": "Retrieve topic information for a specified topic ID under the current permissions"
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

Use the describe_topic_tool to find the shard count for the current topic.

### Tool 6: describe_topics_tool

Retrieve information for multiple topics under a specified project ID within the current permissions.

- Required input parameters for debugging:

`Input`

```json
{
    "inputSchema": {
        "type": "object",
        "required": [],
        "properties": {
            "project_id": {
                "type": "string",
                "description": "Optional log project ID. Defaults to the project_id set in the environment variable. If not set, this is required."
            }
        }
    },
    "name": "describe_topics_tool",
    "description": "Retrieve information for multiple topics under a specified project ID within the current permissions"
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

Use the describe_topics_tool to find the shard count for the first 10 topics under the current project.

### Tool 7: put_logs_v2_tool

upload logs to the specified log topic.

- Required input parameters for debugging:

`Input`

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["logs"],
    "properties": {
      "logs": {
        "type": "array",
        "description": "logs field for the log field to be written, each item in the array is a log, each item consists of multiple key-value key-value pairs"
      },
      "log_time": {
        "type": "int",
        "description": "Log timestamp for writing to the log, default is current time",
      },
      "topic_id": {
        "type": "string",
        "description": "Optional log topic ID, default is the topic_id set in the environment variable, if not set, then must be passed."
      },
      "source": {
        "type": "string",
        "description": "The source of the logs, usually identified by the machine IP",
      },
      "filename": {
        "type": "string",
        "description": "Log file name",
      },
      "hash_key": {
        "type": "string",
        "description": "HashKey of the log group to specify the partition (Shard) to which the current log group is to be written",
      },
      "compression": {
        "type": "string",
        "description": "The compression format of the request body, default is lz4, optional zlib.",
      },
    }
  },
  "name": "put_logs_v2_tool",
  "description": "Call the PutLogs interface to upload logs to the specified log topic. If you need to use searchLogs to query the logs, please set up the index first."
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

Use the put_logs_v2_tool tool to help me write the following logs as [{"user": "peter", "age": 18}, {"user": "marry", "age": 16}]

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
| streamable-http | http://127.0.0.1:8000/mcp/ |

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
