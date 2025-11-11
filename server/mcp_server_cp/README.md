# CP MCP Server

## Version
v1.0.0

## Overview

CP MCP Server is the official MCP Server launched by CodePipeline (CP), supporting convenient troubleshooting of pipeline execution-related issues through natural language.

## Category
Devops

## Tags
CI/CD, DevOps, Continuous Delivery, Pipeline, Application Deployment

## Features

- Query workspace infomation
- Query pipeline infomation
- Query pipeline execution records
- Query pipeline execution failed task information

## Available Tools

This MCP Server product provides the following Tools (capabilities):

### Tool 1: list_workspaces
This tool is used to list all available workspaces.

#### Type
saas

#### Detailed Description
This tool allows you to query and retrieve a list of workspaces from the CodePipeline service.
You can filter workspaces by name, control the number of results per page, and browse through large result sets using pagination tokens.

#### Input Parameters Required for Debugging:
Input:
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "description": "Filter workspace name, optional parameter. If provided, only returns workspaces with names containing this string.",
        "type": "string"
      },
      "limit": {
        "description": "Maximum number of workspaces to return per page, optional parameter. Default is 20, valid values are between 1 and 100.",
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 20
      },
      "page_token": {
        "description": "Pagination token for retrieving next page of results, optional parameter. This token should be obtained from the 'NextToken' field of a previous list_workspaces response. Format is \"page_{page_number}\" (e.g., \"page_2\" for page 2).",
        "type": ["string", "null"]
      }
    }
  },
  "name": "list_workspaces",
  "description": "List workspaces with pagination support. This tool allows you to query and retrieve a list of workspaces from the CodePipeline service. You can filter workspaces by name, control the number of results per page, and browse through large result sets using pagination tokens."
}
```
Output:
    - Workspace list
    - Pagination token (if there are more results)
    - Total number of workspaces
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
#### Most Easily Triggered Prompt Examples
View the list of workspaces containing "demo" in their name.

### Tool 2: list_pipelines
This tool is used to list all pipelines under a specified workspace.

#### Type
saas

#### Detailed Description
This tool allows you to query and retrieve a list of pipelines under a specified workspace from the CodePipeline service. You can filter pipelines by name, control the number of results per page, and browse through large result sets using pagination tokens.

#### Input Parameters Required for Debugging:
Input:
```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["workspace_id"],
    "properties": {
      "workspace_id": {
        "description": "Workspace ID, required parameter. Specifies the workspace for which to list pipelines.",
        "type": "string"
      },
      "name": {
        "description": "Filter pipeline name, optional parameter. If provided, only returns pipelines with names containing this string.",
        "type": "string"
      },
      "limit": {
        "description": "Maximum number of pipelines to return per page, optional parameter. Default is 20, valid values are between 1 and 100.",
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 20
      },
      "page_token": {
        "description": "Pagination token for retrieving next page of results, optional parameter. This token should be obtained from the 'NextToken' field of a previous list_pipelines response. Format is \"page_{page_number}\" (e.g., \"page_2\" for page 2).",
        "type": ["string", "null"]
      }
    }
  },
  "name": "list_pipelines",
  "description": "List pipelines under a specified workspace with pagination support. This tool allows you to query and retrieve a list of pipelines from the CodePipeline service. You can filter pipelines by name, control the number of results per page, and browse through large result sets using pagination tokens."
}
```
Output:
    - Pipeline list
    - Pagination token (if there are more results)
    - Total number of pipelines
```json 
{
  "Pipelines": [
    {
      "Id": "**********c714f129540d**********",
      "Name": "demo-pipeline",
      "WorkspaceId": "**********f84555b4585b**********",
      "Description": "Example pipeline",
      "Spec": {"Stages": [...]},
      "Url": "https://console.volcengine.com/cp/region:cp+cn-beijing/v2/workspace/**********f84555b4585b**********/pipeline/**********c714f129540d**********"
    }
  ],
  "NextToken": "page_2",
  "TotalCount": 10
}

```
#### Most Easily Triggered Prompt Examples
View the list of pipelines under the workspace with ID "**********f84555b4585b**********".
Or
View the list of pipelines under the workspace named "demo01".

### Tool 3: list_pipeline_runs
This tool is used to list execution records of a specified pipeline.

#### Type
saas

#### Detailed Description
This tool allows you to query and retrieve a list of execution records for a specified pipeline from the CodePipeline service. You can control the number of results per page and browse through large result sets using pagination tokens.

#### Input Parameters Required for Debugging:
Input:
```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["workspace_id", "pipeline_id"],
    "properties": {
      "workspace_id": {
        "description": "Workspace ID, required parameter. The workspace where the pipeline is located.",
        "type": "string"
      },
      "pipeline_id": {
        "description": "Pipeline ID, required parameter. The pipeline for which to list execution records.",
        "type": "string"
      },
      "limit": {
        "description": "Maximum number of execution records to return per page, optional parameter. Default is 3, valid values are between 1 and 100.",
        "type": "integer",
        "minimum": 1,
        "maximum": 100,
        "default": 3
      },
      "page_token": {
        "description": "Pagination token for retrieving next page of results, optional parameter. This token should be obtained from the 'NextToken' field of a previous list_pipeline_runs response.",
        "type": ["string", "null"]
      }
    }
  },
  "name": "list_pipeline_runs",
  "description": "List execution records of a specified pipeline with pagination support. This tool allows you to query and retrieve a list of execution records for a specified pipeline from the CodePipeline service. You can control the number of results per page and browse through large result sets using pagination tokens."
}
```
Output:
    - Pipeline execution record list
    - Pagination token (if there are more results)
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
      "Stages": [{"Id": "stage-c1", "Name": "Stage 1", "Status": "Success"}, {"Id": "stage-c2", "Name": "Stage 2", "Status": "Failed"}],
      "Url": "https://console.volcengine.com/cp/region:cp+cn-beijing/v2/workspace/**********f84555b4585b**********/pipeline/**********c714f129540d**********/record/**********d61f401193ca**********"
    }
  ],
  "NextToken": "token123456"
}

```
#### Most Easily Triggered Prompt Examples
View the latest execution records of the demo-ppl pipeline.

### Tool 4: list_failed_tasks
This tool is used to list failed tasks in a specified pipeline execution record.

#### Type
saas

#### Detailed Description
This tool allows you to query and retrieve a list of failed tasks in a specified pipeline execution record from the CodePipeline service.

#### Input Parameters Required for Debugging:
Input:
```json 
{
  "inputSchema": {
    "type": "object",
    "required": ["workspace_id", "pipeline_id", "pipeline_run_id"],
    "properties": {
      "workspace_id": {
        "description": "Workspace ID, required parameter. The workspace where the pipeline is located.",
        "type": "string"
      },
      "pipeline_id": {
        "description": "Pipeline ID, required parameter. The pipeline for which to query failed tasks.",
        "type": "string"
      },
      "pipeline_run_id": {
        "description": "Pipeline execution record ID, required parameter. The execution record for which to query failed tasks.",
        "type": "string"
      }
    }
  },
  "name": "list_failed_tasks",
  "description": "List failed tasks in a specified pipeline execution record. This tool allows you to query and retrieve a list of failed tasks in a specified pipeline execution record from the CodePipeline service."
}
```
Output:
    - List of stages containing failed tasks
```json 
{
  "Stages": [
    {
      "Id": "**********6ba865cd9d5d02e",
      "Name": "stage-c2",
      "DisplayName": "Stage stage-c2",
      "Status": "Failed",
      "FailedTasks": [
        {
          "Id": "**********44f881722ead28deb404",
          "TaskRunID": "**********312978f286a1d487a32",
          "Name": "262e2a",
          "DisplayName": "Command Execution",
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
#### Most Easily Triggered Prompt Examples
Analyze failed tasks and failure logs from the second execution of the demo-ppl pipeline.

## Service Activation Link
[Volcano Continuous Delivery Service Activation Link](https://console.volcengine.com/cp)

## Authentication Method
Obtain the corresponding access ak/sk for your account in the Volcano Engine management console. You need to set VOLCENGINE_AK and VOLCENGINE_SK in the configuration based on the obtained ak and sk.

## Compatible Platforms
Trae/Cursor/Claude

To integrate Volcano Continuous Delivery functionality in AI tools such as Trae, Cursor, or Claude, you can add the following content to the MCP configuration:
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
        "VOLCENGINE_AK": "<your_volcengin_account_access_key>",
        "VOLCENGINE_SK": "<your_volcengin_account_secret_key>",
        "VOLCENGINE_REGION": "<your_region>"
      }
    }
  }
}
```

Currently supported regions: ["cn-beijing"]