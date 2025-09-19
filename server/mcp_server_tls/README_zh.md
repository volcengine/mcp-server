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
| streamable-http | http://127.0.0.1:8000/mcp/ |

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

