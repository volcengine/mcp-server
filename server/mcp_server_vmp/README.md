#MCP Server 产品名称：MCP Server VMP
[![产品Logo]([./logo.png])]

## 版本信息
v0.1.0

## 产品描述
### 短描述（建议20个字）
自然语言驱动查询分析 Prometheus 指标数据

### 长描述（建议50字，不超过100字）
托管 Prometheus 服务（VMP）是完全继承和对接开源 Prometheus 生态的新一代云原生监控引擎系统。MCP Server VMP 支持 Prometheus 工作区查询、指标查询等功能，提供运维排查、数据分析等场景下基于自然语言驱动的指标查询分析。

## 分类
可观测

## 标签
Prometheus, 监控, 可观测

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: list_workspaces

#### 类型
saas

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
                "title": "Region",
                "type": "string"
            }
        },
        "title": "list_workspacesArguments"
    }
}
```
输出：
- 工作区列表

#### 最容易被唤起的 Prompt示例
请列出在cn-beijing地域下的所有VMP工作区实例信息

### Tool 2: query_metrics

#### 类型
saas

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
                "title": "Workspaceid",
                "type": "string"
            },
            "query": {
                "title": "Query",
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
                "title": "Time"
            },
            "region": {
                "default": "cn-beijing",
                "title": "Region",
                "type": "string"
            }
        },
        "required": [
            "workspaceId",
            "query"
        ],
        "title": "query_metricsArguments"
    }
}
```
输出：
- 指标查询结果

#### 最容易被唤起的 Prompt示例
查询cn-beijing地域下的VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746实例中，当前时间的cpu使用率


### Tool 3: query_range_metrics

#### 类型
saas

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
                "title": "Workspaceid",
                "type": "string"
            },
            "query": {
                "title": "Query",
                "type": "string"
            },
            "start": {
                "title": "Start",
                "type": "string"
            },
            "end": {
                "title": "End",
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
                "title": "Step"
            },
            "region": {
                "default": "cn-beijing",
                "title": "Region",
                "type": "string"
            }
        },
        "required": [
            "workspaceId",
            "query",
            "start",
            "end"
        ],
        "title": "query_range_metricsArguments"
    }
}
```
输出：
- 指标查询结果

#### 最容易被唤起的 Prompt示例
查询cn-beijing地域下的VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746实例中，最近一小时中cpu使用率top3的pod


### Tool 4: query_metric_names

#### 类型
saas

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
                "title": "Workspaceid",
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
                "title": "Match"
            },
            "region": {
                "default": "cn-beijing",
                "title": "Region",
                "type": "string"
            }
        },
        "required": [
            "workspaceId"
        ],
        "title": "query_metric_namesArguments"
    }
}
```
输出：
- 匹配的指标名称列表

#### 最容易被唤起的 Prompt示例
VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746中，cpu相关的指标有哪些


### Tool 5: query_metric_labels

#### 类型
saas

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
                "title": "Workspaceid",
                "type": "string"
            },
            "metricName": {
                "title": "Metricname",
                "type": "string"
            },
            "region": {
                "default": "cn-beijing",
                "title": "Region",
                "type": "string"
            }
        },
        "required": [
            "workspaceId",
            "metricName"
        ],
        "title": "query_metric_labelsArguments"
    }
}
```
输出：
- 指标的标签名称列表

#### 最容易被唤起的 Prompt示例
VMP工作区b73766b5-2e63-4143-bcd1-8a1ba3a94746中，container_cpu_usage_seconds_total指标有哪些label


## 可适配平台  
方舟、cursor、claude desktop 或支持MCP server调用的其他终端

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

### 部署

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


