# CP MCP Server

## 版本信息
当前版本为 v1.0.0。

## 产品描述
### 短描述
CP MCP Server 是 CodePipeline（CP）官方推出的MCP Server，支持通过自然语言的方式便捷的排查流水线执行相关的问题。
### 长描述
CP MCP Server 是 CodePipeline（CP）官方推出的MCP Server，支持通过自然语言的方式便捷的查看工作区，流水线，执行记录，执行日志查看等功能。

## 分类
开发与运维 

## 标签
CI/CD, DevOps，持续交付, 流水线，应用部署

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1：list_workspaces
该工具用于列出所有可用的工作空间。

#### 类型
saas

#### 详细描述

此工具允许您从 CodePipeline 服务查询和检索工作空间列表。
您可以按名称过滤工作空间，控制每页结果数量，并通过分页令牌浏览大型结果集。

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "description": "过滤工作区名称，可选参数。如果提供，只返回名称包含此字符串的工作区。",
        "type": "string"
      },
      "limit": {
        "description": "每页返回的最大工作区数量，可选参数。默认值为20，有效值在1到100之间。",
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 20
      },
      "page_token": {
        "description": "分页令牌，用于检索下一页结果，可选参数。此令牌应从上一次list_workspaces调用响应的'NextToken'字段获取。格式为\"page_{page_number}\"(例如，第2页为\"page_2\")。",
        "type": ["string", "null"]
      }
    }
  },
  "name": "list_workspaces",
  "description": "列出工作区并支持分页功能。此工具允许您从CodePipeline服务查询和检索工作区列表。您可以按名称过滤工作区，控制每页结果数量，并通过分页令牌浏览大型结果集。"
}
```
输出：
    - 工作区列表
    - 分页令牌（如果有更多结果）
    - 工作区总数
```json 
{
  "Workspaces": [
    {
      "Id": "**********8d4164b74e59**********",
      "Name": "demo01",
      "Url": "https://console.volcengine.com/cp/region:cp+cn-beijing/v2/workspace/**********8d4164b74e59**********"
    },
    {
      "Id": "**********f84555b4585b**********",
      "Name": "demo02",
      "Url": "https://console.volcengine.com/cp/region:cp+cn-beijing/v2/workspace/**********f84555b4585b**********"
    }
  ],
  "NextToken": "",
  "TotalCount": 2
}

```
#### 最容易被唤起的 Prompt示例

查看名称包含"demo"的工作区列表。

### Tool 2：list_pipelines
该工具用于列出指定工作区下的所有流水线。

#### 类型
saas

#### 详细描述

此工具允许您从CodePipeline服务查询和检索指定工作区下的流水线列表。您可以按名称过滤流水线，控制每页结果数量，并通过分页令牌浏览大型结果集。

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["workspace_id"],
    "properties": {
      "workspace_id": {
        "description": "工作区ID，必需参数。指定要列出流水线的工作区。",
        "type": "string"
      },
      "name": {
        "description": "过滤流水线名称，可选参数。如果提供，只返回名称包含此字符串的流水线。",
        "type": "string"
      },
      "limit": {
        "description": "每页返回的最大流水线数量，可选参数。默认值为20，有效值在1到100之间。",
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 20
      },
      "page_token": {
        "description": "分页令牌，用于检索下一页结果，可选参数。此令牌应从上一次list_pipelines调用响应的'NextToken'字段获取。格式为\"page_{page_number}\"(例如，第2页为\"page_2\")。",
        "type": ["string", "null"]
      }
    }
  },
  "name": "list_pipelines",
  "description": "列出指定工作区下的流水线并支持分页功能。此工具允许您从CodePipeline服务查询和检索流水线列表。您可以按名称过滤流水线，控制每页结果数量，并通过分页令牌浏览大型结果集。"
}
```
输出：
    - 流水线列表
    - 分页令牌（如果有更多结果）
    - 流水线总数
```json 
{
  "Pipelines": [
    {
      "Id": "**********c714f129540d**********",
      "Name": "demo-pipeline",
      "WorkspaceId": "**********f84555b4585b**********",
      "Description": "示例流水线",
      "Spec": {"Stages": [...]},
      "Url": "https://console.volcengine.com/cp/region:cp+cn-beijing/v2/workspace/**********f84555b4585b**********/pipeline/**********c714f129540d**********"
    }
  ],
  "NextToken": "page_2",
  "TotalCount": 10
}

```
#### 最容易被唤起的 Prompt示例
查看ID为"**********f84555b4585b**********"的工作区下的流水线列表。
或
查看名称为"demo01"的工作区下的流水线列表


### Tool 3：list_pipeline_runs
该工具用于列出指定流水线的执行记录。

#### 类型
saas

#### 详细描述

此工具允许您从CodePipeline服务查询和检索指定流水线的执行记录列表。您可以控制每页结果数量，并通过分页令牌浏览大型结果集。

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["workspace_id", "pipeline_id"],
    "properties": {
      "workspace_id": {
        "description": "工作区ID，必需参数。流水线所在的工作区。",
        "type": "string"
      },
      "pipeline_id": {
        "description": "流水线ID，必需参数。要列出执行记录的流水线。",
        "type": "string"
      },
      "limit": {
        "description": "每页返回的最大执行记录数量，可选参数。默认值为3，有效值在1到100之间。",
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 3
      },
      "page_token": {
        "description": "分页令牌，用于检索下一页结果，可选参数。此令牌应从上一次list_pipeline_runs调用响应的'NextToken'字段获取。",
        "type": ["string", "null"]
      }
    }
  },
  "name": "list_pipeline_runs",
  "description": "列出指定流水线的执行记录并支持分页功能。此工具允许您从CodePipeline服务查询和检索指定流水线的执行记录列表。您可以控制每页结果数量，并通过分页令牌浏览大型结果集。"
}
```
输出：
    - 流水线执行记录列表
    - 分页令牌（如果有更多结果）
```json 
{
  "PipelineRuns": [
    {
      "Id": "**********d61f401193ca**********",
      "PipelineId": "**********c714f129540d**********",
      "WorkspaceId": "**********f84555b4585b**********",
      "Status": "Failed",
      "StartTime": "2025-10-01T12:00:00Z",
      "FinishTime": "2025-10-01T12:05:00Z",
      "Index": 2,
      "Parameters": {},
      "Trigger": {"Type": "Manual"},
      "Spec": {"Stages": [...]},
      "Stages": [{"Id": "stage-c1", "Name": "阶段1", "Status": "Success"}, {"Id": "stage-c2", "Name": "阶段2", "Status": "Failed"}],
      "Url": "https://console.volcengine.com/cp/region:cp+cn-beijing/v2/workspace/**********f84555b4585b**********/pipeline/**********c714f129540d**********/record/**********d61f401193ca**********"
    }
  ],
  "NextToken": "token123456"
}

```
#### 最容易被唤起的 Prompt示例
查看demo-ppl流水线的最新执行记录。

### Tool 4：list_failed_tasks
该工具用于列出指定流水线执行记录中的失败任务。

#### 类型
saas

#### 详细描述

此工具允许您从CodePipeline服务查询和检索指定流水线执行记录中的失败任务列表。

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["workspace_id", "pipeline_id", "pipeline_run_id"],
    "properties": {
      "workspace_id": {
        "description": "工作区ID，必需参数。流水线所在的工作区。",
        "type": "string"
      },
      "pipeline_id": {
        "description": "流水线ID，必需参数。要查询失败任务的流水线。",
        "type": "string"
      },
      "pipeline_run_id": {
        "description": "流水线执行记录ID，必需参数。要查询失败任务的执行记录。",
        "type": "string"
      }
    }
  },
  "name": "list_failed_tasks",
  "description": "列出指定流水线执行记录中的失败任务。此工具允许您从CodePipeline服务查询和检索指定流水线执行记录中的失败任务列表。"
}
```
输出：
    - 包含失败任务的阶段列表
```json 
{
  "Stages": [
    {
      "Id": "**********6ba865cd9d5d02e",
      "Name": "stage-c2",
      "DisplayName": "阶段stage-c2",
      "Status": "Failed",
      "FailedTasks": [
        {
          "Id": "**********44f881722ead28deb404",
          "TaskRunID": "**********312978f286a1d487a32",
          "Name": "262e2a",
          "DisplayName": "命令执行",
          "Status": "Failed",
          "Steps": [
            {
              "Name": "step-c5",
              "Status": "Failed",
              "LogUri": "",
              "StartTime": "2025-10-09T15:23:09+08:00",
              "FinishTime": "2025-10-09T15:23:09+08:00"
            }
          ],
          "StartTime": "2025-10-09T15:23:00+08:00",
          "FinishTime": "2025-10-09T15:23:10+08:00",
          "FailedReason": "Failed",
          "FailedMessage": "\"step-step-c5\" exited with code 1 (image: \"cp-controller-cn-beijing.cr.volces.com/cp-v2-system/exec-bash@sha256:**********9e2698d6fd95a42db3442f5248a17fa623572419c2c306bc81bf5d\"); for logs run: kubectl -n cp-2100483201 logs **********44dc946a3e6220986ee9f32935a37118b5bbb9a9cc9993b-pod -c step-step-c5\n",
          "FailedStepLogURL": {
            "Url": "https://cp-v2.tos-cn-beijing.volces.com/v2/log/2100483201/**********f84555b4585b95525c30d1/**********4f129540dd1a933e3c27/**********401193caf1d248cba156/**********44f881722ead28deb404/**********312978f286a1d487a32/step-c5.log"
          }
        }
      ]
    }
  ]
}

```
#### 最容易被唤起的 Prompt示例
分析demo-ppl流水线第二次执行的失败任务及失败日志。


## 服务开通链接

[火山持续交付服务开通链接](https://console.volcengine.com/cp)

## 鉴权方式
在火山引擎管理控制台获取账号相应的访问ak/sk。 需要在配置中根据获取到的ak，sk，设置 VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY


## 可适配平台
Trae/Cursor/Claude

如需在Trae、Cursor或Claude等AI工具中集成火山持续交付功能，可以在MCP配置中添加以下内容：
```json 
{
  "mcpServers": {
    "code_pipeline": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cp",
        "mcp-server-cp"
      ],
      "env": {
        "VOLCENGINE_ENDPOINT": "cp.<your_region>.volcengineapi.com",
        "VOLCENGINE_ACCESS_KEY": "<your_volcengin_account_access_key>",
        "VOLCENGINE_SECRET_KEY": "<your_volcengin_account_secret_key>",
        "VOLCENGINE_REGION": "<your_region>"
      }
    }
  }
}
```

当前支持的Region: ["cn-beijing"]


## 使用示例

* 查看名称包含"demo"的工作区列表
* 查看名称为"demo-workspace"工作区下的流水线列表 或 查看id为"xxx"的工作区下的流水线列表
* 查看名称为"demo-pipeline"最新的执行记录 或 查看id为"xxxx"最新的执行记录
* 查看执行记录id为"xxx"中执行失败的任务详情
