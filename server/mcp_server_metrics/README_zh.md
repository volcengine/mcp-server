# Metrics MCP Server ![产品Logo](./logo.svg)

火山引擎指标服务（Metrics）是一个全面的指标管理和监控系统，提供了广泛的指标收集、存储、查询和可视化功能。Metrics MCP Server 提供指标查询、仪表盘管理和数据分析等功能，助力运维排查、数据分析等场景下基于自然语言驱动的指标管理和分析体验。

<table>
  <tr>
    <td>版本</td>
    <td>v0.1.0</td>
  </tr>
  <tr>
    <td>描述</td>
    <td>自然语言驱动查询和管理火山引擎 Metrics 数据</td>
  </tr>
  <tr>
    <td>分类</td>
    <td>可观测</td>
  </tr>
  <tr>
    <td>标签</td>
    <td>指标, 监控, 可观测</td>
  </tr>
</table>

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: metrics_list_workspace

#### 详细描述

查询当前账户下指定地域的所有工作区列表。

#### 调试所需的输入参数:

输入：

```json
{
    "name": "metrics_list_workspace",
    "description": "查询在指定地域下的所有Metrics工作区实例信息",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "page_number": {
                "default": 1,
                "description": "分页页码",
                "type": "integer"
            },
            "page_size": {
                "default": 10,
                "description": "分页大小",
                "type": "integer"
            },
            "name": {
                "description": "工作区名称，用于过滤",
                "type": "string"
            }
        },
        "required": [
	    "region"
	]
    }
}
```

输出：

- 工作区列表及元数据

#### 最容易被唤起的 Prompt示例

请列出在 cn-beijing 地域下的所有工作区实例信息。

### Tool 2: metrics_get_workspace_info

#### 详细描述

查询当前账户下指定地域的指定工作区详情信息。

#### 调试所需的输入参数:

输入：

```json
{
    "name": "metrics_get_workspace_info",
    "description": "查询在指定地域下的指定工作区详情信息",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace_id": {
                "description": "工作区 ID",
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

输出：

- 工作区详情信息

#### 最容易被唤起的 Prompt示例

请获取在 cn-beijing 地域下工作区 ID 为 "test-workspace-id" 的工作区信息。

### Tool 3: metrics_list_query_clusters

#### 详细描述

查询当前账户下指定地域的所有查询集群列表。

#### 调试所需的输入参数:

输入：

```json
{
    "name": "metrics_list_query_clusters",
    "description": "查询当前账户下指定地域的所有查询集群列表",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "page_number": {
                "default": 1,
                "description": "分页页码",
                "type": "integer"
            },
            "page_size": {
                "default": 10,
                "description": "分页大小",
                "type": "integer"
            },
            "name": {
                "description": "查询集群名称，用于过滤",
                "type": "string"
            }
        },
        "required": [
            "region"
        ]
    }
}
```

输出：

- 查询集群列表及元数据

#### 最容易被唤起的 Prompt示例

请列出在 cn-beijing 地域下的所有查询集群。

### Tool 4: metrics_get_query_cluster

#### 详细描述

查询当前账户下指定地域的指定查询集群详情信息。

#### 调试所需的输入参数:

输入：

```json
{
    "name": "metrics_get_query_cluster",
    "description": "查询当前账户下指定地域的指定查询集群详情信息",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "cluster_id": {
                "description": "查询集群 ID",
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

输出：

- 查询集群详情信息

#### 最容易被唤起的 Prompt示例

请获取在 cn-beijing 地域下查询集群 ID 为 "test-cluster-id" 的查询集群信息。

### Tool 5: metrics_list_preagg

#### 详细描述

查询当前账户下指定地域指定工作区下的所有预聚合规则列表。。

#### 调试所需的输入参数:

输入：

```json
{
    "name": "metrics_list_preagg",
    "description": "查询当前账户下指定地域指定工作区下的所有预聚合规则列表",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace_name": {
                "description": "工作区名称",
                "type": "string"
            },
            "page_number": {
                "default": 1,
                "description": "分页页码",
                "type": "integer"
            },
            "page_size": {
                "default": 10,
                "description": "分页大小",
                "type": "integer"
            },
            "only_show_mine": {
                "default": true,
                "description": "是否只显示当前用户创建的规则",
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

输出：

- 预聚合规则列表及元数据

#### 最容易被唤起的 Prompt示例

请获取在 cn-beijing 地域下工作区名为 "test_workspace_name" 中的所有预聚合规则。

### Tool 6: metrics_influx_query

#### 详细描述

从当前账户指定地域指定工作区中，查询 InfluxDB 指标数据。

#### 调试所需的输入参数:

输入：

```json
{
    "name": "metrics_influx_query",
    "description": "从当前账户指定地域指定工作区中，查询 InfluxDB 指标数据",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace": {
                "description": "工作区名称",
                "type": "string"
            },
            "queries": {
                "description": "InfluxQL 查询语句列表",
                "type": "array",
                "items": {"type": "string"}
            },
            "epoch": {
                "description": "时间戳精度 (s/ms/us/ns)",
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

输出：

- 查询数据结果

#### 最容易被唤起的 Prompt示例

请在 cn-beijing 地域下工作区名为 "test_workspace_name" 中使用 InfluxQL 查询过去三十分钟的 CPU 使用率。

### Tool 7: metrics_query

#### 详细描述

从当前账户指定地域指定工作区中，查询 Metrics/OpenTSDB 指标数据。从指标服务查询指标数据。

#### 调试所需的输入参数:

输入：

```json
{
    "name": "metrics_query",
    "description": "从当前账户指定地域指定工作区中，查询 Metrics/OpenTSDB 指标数据",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspace": {
                "description": "工作区名称",
                "type": "string"
            },
            "queries": {
                "description": "查询配置详情列表",
                "type": "array",
                "items": {"type": "object"}
            },
            "start": {
                "default": "10m-ago",
                "description": "查询起始时间",
                "type": "string"
            },
            "end": {
                "default": "now",
                "description": "查询结束时间",
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

输出：

- 指标查询结果

#### 最容易被唤起的 Prompt示例

请在 cn-beijing 地域下工作区名为 "test_workspace_name" 中使用 Metrics/OpenTSDB 协议查询过去三十分钟的 CPU 使用率。

## 可适配平台

方舟、Trae、Cursor、Claude Desktop 或支持 MCP Server 调用的其他终端

## 服务开通链接 (整体产品)

https://console.volcengine.com/cloud-monitor/metrics

## 鉴权方式

API Key ([签名机制](https://www.volcengine.com/docs/6731/942192))

## 安装部署

### 系统依赖

- 安装 Python3.10或更高版本
- 安装uv

  - MacOS/Linux

  ```text
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

  - Windows

  ```text
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 环境变量

| 环境变量名            | 描述                    | 默认值     | 获取方式                                                         |
| --------------------- | ----------------------- | ---------- | ---------------------------------------------------------------- |
| VOLCENGINE_ACCESS_KEY | 火山引擎账号 ACCESS KEY | -          | [火山引擎访问控制台](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_SECRET_KEY | 火山引擎账号 SECRET KEY | -          | [火山引擎访问控制台](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_REGION     | 火山引擎 地域           | cn-beijing | -                                                                |

### 部署

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
