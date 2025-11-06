# VMP MCP Server ![产品Logo](./logo.svg)

托管 Prometheus 服务（VMP）是完全继承和对接开源 Prometheus 生态的新一代云原生监控引擎系统。VMP MCP Server 提供 Prometheus 工作区查询、指标查询等功能，助力运维排查、数据分析等场景下基于自然语言驱动的指标查询分析体验。

<table>
  <tr>
    <td>版本</td>
    <td>v0.1.0</td>
  </tr>
  <tr>
    <td>描述</td>
    <td>自然语言驱动查询分析 Prometheus 指标数据</td>
  </tr>
  <tr>
    <td>分类</td>
    <td>可观测</td>
  </tr>
  <tr>
    <td>标签</td>
    <td>Prometheus, 监控, 可观测</td>
  </tr>
</table>

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: create_workspace

#### 详细描述
创建指定地域下的VMP工作区实例

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "create_workspace",
    "description": "创建指定地域下的VMP工作区实例",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "name": {
                "description": "工作区实例的名称",
                "type": "string"
            },
            "description": {
                "description": "工作区实例的描述",
                "type": "string"
            },
            "delete_protection_enabled": {
                "description": "是否开启工作区实例的删除保护",
                "type": "boolean"
            },
            "instance_type_id": {
                "description": "工作区实例的类型ID",
                "type": "string"
            },
            "project_name": {
                "description": "工作区实例所属的项目名称",
                "type": "string"
            },
            "username": {
                "description": "工作区实例的basic auth用户名,必须和 password 字段一起设置",
                "type": "string"
            },
            "password": {
                "description": "工作区实例的basic auth密码,必须和 username 字段一起设置",
                "type": "string"
            },
            "public_access_enabled": {
                "description": "是否开启工作区实例的公共访问",
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
输出：
- 工作区ID

#### 最容易被唤起的 Prompt示例
请在cn-beijing地域下创建一个名称为 vmp-1234567890abcdef，类型为 vmp.standard.15d 的VMP工作区实例

### Tool 2: update_workspace

#### 详细描述
查询当前账户下指定地域的所有工作区信息

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "update_workspace",
    "description": "更新指定地域下的VMP工作区实例信息",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspaceId": {
                "description": "要更新的VMP工作区实例ID",
                "type": "string"
            },
            "name": {
                "description": "工作区实例的新名称",
                "type": "string"
            },
            "delete_protection_enabled": {
                "description": "是否开启工作区实例的删除保护",
                "type": "boolean"
            },
            "description": {
                "description": "工作区实例的新描述",
                "type": "string"
            },
            "name": {
                "description": "工作区实例的新名称",
                "type": "string"
            },
            "public_access_enabled": {
                "description": "是否开启工作区实例的公共访问",
                "type": "boolean"
            },
            "search_latency_offset": {
                "description": "工作区实例的搜索延迟偏移量,需要是一个时间 duration 字符串(e.g. 1m, 1h)",
                "type": "string"
            },
            "username": {
                "description": "工作区实例的basic auth用户名,必须和 password 字段一起设置",
                "type": "string"
            },
            "password": {
                "description": "工作区实例的basic auth密码,必须和 username 字段一起设置",
                "type": "string"
            },
            "active_series": {
                "description": "工作区实例的最大活跃时间序列数",
                "type": "integer"
            },
            "ingest_samples_per_second": {
                "description": "工作区实例的最大每秒写入样本数",
                "type": "integer"
            },
            "public_query_bandwidth": {
                "description": "工作区实例的最大公网查询带宽, 单位Mbps",
                "type": "integer"
            },
            "public_write_bandwidth": {
                "description": "工作区实例的最大公网写入带宽, 单位Mbps",
                "type": "integer"
            },
            "query_per_second": {
                "description": "工作区实例的最大公网查询每秒请求数",
                "type": "integer"
            },
            "scan_samples_per_second": {
                "description": "工作区实例的最扫描每秒样本数",
                "type": "integer"
            },
            "scan_series_per_second": {
                "description": "工作区实例的最扫描每秒时间序列数",
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
输出：
- 工作区ID

#### 最容易被唤起的 Prompt示例
请列出帮忙调整一下工作区Id为vmp-1234567890abcdef的VMP工作区的查询每秒请求数为200

### Tool 3: list_workspaces

#### 详细描述
查询当前账户下指定地域的所有工作区信息

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "list_workspaces",
    "description": "查询在指定地域下的所有VMP工作区实例信息",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        }
    }
}
```
输出：
- 工作区列表

#### 最容易被唤起的 Prompt示例
请列出在cn-beijing地域下的所有VMP工作区实例信息

### Tool 4: delete_workspace

#### 详细描述
删除当前账户下指定地域的指定工作区实例

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "delete_workspace",
    "description": "删除在指定地域下的指定VMP工作区实例",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "workspaceId": {
                "description": "要删除的VMP工作区实例ID",
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
输出：
- 工作区ID

#### 最容易被唤起的 Prompt示例
请删除在cn-beijing地域下的VMP工作区实例vmp-1234567890abcdef

### Tool 5: list_workspace_instance_types

#### 详细描述
删除当前账户下指定地域的指定工作区实例

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "list_workspace_instance_types",
    "description": "查询在指定地域下的所有VMP工作区实例类型",
    "inputSchema": {
        "type": "object",
        "properties": {
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            },
            "instanceTypeId": {
                "description": "要查询的VMP工作区实例类型ID",
                "type": "string"
            }
        }
    }
}
```
输出：
- 工作区类型列表

#### 最容易被唤起的 Prompt示例
请列出在cn-beijing地域下的所有的工作区类型

### Tool 6: query_metrics

#### 详细描述
在指定的VMP工作区中，执行指定的PromQL的Instant查询

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "query_metrics",
    "description": "在指定的VMP工作区中，执行指定的PromQL查询语句",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "要查询的VMP工作区实例ID",
                "type": "string"
            },
            "query": {
                "description": "PromQL查询语句",
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
                "description": "查询时间，格式为RFC3339 或 Unix 时间戳，默认为当前时间"
            },
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
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
输出：
- 指标查询结果

#### 最容易被唤起的 Prompt示例
查询cn-beijing地域下的VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746实例中，当前时间的cpu使用率


### Tool 7: query_range_metrics

#### 详细描述
在指定的VMP工作区中，执行指定时间范围的PromQL的查询

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "query_range_metrics",
    "description": "在指定的VMP工作区中，执行指定时间范围的PromQL的查询",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "目标VMP工作区实例ID",
                "type": "string"
            },
            "query": {
                "description": "PromQL查询语句",
                "type": "string"
            },
            "start": {
                "description": "查询起始时间，格式为RFC3339 或 Unix 时间戳",
                "type": "string"
            },
            "end": {
                "description": "查询截止时间，格式为RFC3339 或 Unix 时间戳",
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
                "description": "查询Step，duration格式，可选传入，不传会根据查询时间范围自动计算"
            },
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
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
输出：
- 指标查询结果

#### 最容易被唤起的 Prompt示例
查询cn-beijing地域下的VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746实例中，最近一小时中cpu使用率top3的pod


### Tool 8: query_metric_names

#### 详细描述
查询指定VMP工作区下，匹配指定过滤条件的指标名称列表

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "query_metric_names",
    "description": "查询指定VMP工作区下，匹配指定过滤条件的指标名称列表",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "目标VMP工作区实例ID",
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
                "description": "Series Selector，用于过滤匹配的指标范围，标准的Promtheus Vector Selector语法，如：{job=~\"kubelet\"}"
            },
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
                "type": "string"
            }
        },
        "required": [
            "workspaceId"
        ]
    }
}
```
输出：
- 匹配的指标名称列表

#### 最容易被唤起的 Prompt示例
VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746中，cpu相关的指标有哪些


### Tool 9: query_metric_labels

#### 详细描述
查询指定VMP工作区下，指定指标的所有标签名称列表

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "query_metric_labels",
    "description": "查询指定VMP工作区下，指定指标的所有标签名称列表",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "目标VMP工作区实例ID",
                "type": "string"
            },
            "metricName": {
                "description": "要查询的指标名称",
                "type": "string"
            },
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
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
输出：
- 指标的标签名称列表

#### 最容易被唤起的 Prompt示例
VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746中，container_cpu_usage_seconds_total指标有哪些label

### Tool 10: query_series

#### 详细描述
查询指定VMP工作区下，指定指标的所有标签名称列表

#### 调试所需的输入参数:
输入：
```json 
{
    "name": "query_series",
    "description": "查询指定VMP工作区下，指定标签筛选器下的所有时间序列",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workspaceId": {
                "description": "目标VMP工作区实例ID",
                "type": "string"
            },
            "match": {
                "type": "string",
                "description": "Series Selector，用于过滤匹配的指标范围，标准的Promtheus Vector Selector语法，如：{job=~\"kubelet\"}"
            },
            "start": {
                "description": "查询起始时间，格式为RFC3339 或 Unix 时间戳",
                "type": "string"
            },
            "end": {
                "description": "查询截止时间，格式为RFC3339 或 Unix 时间戳",
                "type": "string"
            },
            "region": {
                "default": "cn-beijing",
                "description": "目标地域(e.g. cn-beijing, cn-shanghai, cn-guangzhou)",
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
输出：
- 指标的标签名称列表

#### 最容易被唤起的 Prompt示例
VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746中，up 指标有哪些时序数据

## 可适配平台  
方舟、Trae、Cursor、Claude Desktop 或支持 MCP Server 调用的其他终端

## 服务开通链接 (整体产品)  
https://console.volcengine.com/prometheus

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
| 环境变量名 | 描述 | 默认值 | 获取方式 |
| --- | --- | --- | --- |
| VOLCENGINE_ACCESS_KEY | 火山引擎账号 ACCESS KEY | - | [火山引擎访问控制台](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_SECRET_KEY | 火山引擎账号 SECRET KEY | - | [火山引擎访问控制台](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_REGION | 火山引擎 地域 | cn-beijing | - |

### 部署

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


