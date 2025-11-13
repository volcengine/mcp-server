import logging
import os
import argparse
import typing
from mcp.server.fastmcp import FastMCP

import volcenginesdkcore
import yaml

from .config import load_config, CodePipelineConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


MCP_SERVER_NAME = "CodePipeline"

API_METHOD = "POST"
API_SERVICE = "cp"
API_VERSION = "2023-05-01"
API_CONTENT_TYPE = "application/json"

# Initialize FastMCP server
mcp = FastMCP(MCP_SERVER_NAME, port=int(os.getenv("PORT", "8000")))

# Global variables
client = None
region = None


@mcp.tool(name="list_workspaces", description="List workspaces with pagination support")
async def list_workspaces(
    name: str = None,  # Filter by workspace name
    limit: int = 20,   # Maximum number of items to return, default is 20
    page_token: str | None = None   # Cursor for pagination
) -> typing.Dict[str, typing.Any]:
    """List workspaces with support for filtering, pagination, and result limits.
    
    This tool allows you to query and retrieve a list of workspaces from the CodePipeline service.
    You can filter workspaces by name, control the number of results per page, and navigate through
    large result sets using pagination tokens.
    
    Args:
        name: Optional. Filter workspaces by name. If provided, only workspaces whose names
              contain this string will be returned.
        limit: Optional. Maximum number of workspaces to return per page. Default is 20,
               and valid values are between 1 and 100.
        page_token: Optional. Pagination token to retrieve the next page of results.
                    This token should be obtained from the 'NextToken' field in the
                    response of a previous list_workspaces call.
                    Format: "page_{page_number}" (e.g., "page_2" for the second page)
    
    Returns:
        A dictionary containing the following fields:
        - Workspaces: List of workspace objects, each containing only Id and Name fields.
        - NextToken: Token to use for retrieving the next page of results. If empty,
                     there are no more results.
        - TotalCount: Total number of workspaces that match the filter criteria.
    
    Example Usage:
        # Get first page of workspaces, up to 10 items
        response = await list_workspaces(limit=10)
        
        # Get next page using the returned NextToken
        if response['NextToken']:
            next_page = await list_workspaces(
                limit=10,
                page_token=response['NextToken']
            )
        
        # Filter workspaces by name containing "project"
        filtered_workspaces = await list_workspaces(name="project", limit=20)
    
    Raises:
        ValueError: If the provided page_token has an invalid format.
        RuntimeError: If there's an issue with the API request or response handling.
    """
    # Initialize client if not already initialized
    global client
    if client is None:
        init_client()

    # 解析 page_token → 当前页码
    current_page = 1
    if page_token:
        if not page_token.startswith("page_"):
            raise ValueError("Invalid page_token")
        try:
            current_page = int(page_token.split("_")[1])
        except (IndexError, ValueError):
            raise ValueError("Invalid page_token format")

    # Build request parameters
    request_params = {
        "Filter": {
            "Name": name
        },
        "PageNumber": current_page,
        "PageSize": limit,
    }
        
    # Send request to get workspace list
    response = send_cp_request(request_params, action="ListWorkspaces")
    
    # Process response data and return workspace list with pagination info
    if response:
        # Extract necessary data from response
        items = response.get("Items", [])
        total_count = response.get("TotalCount", 0)
        page_number = response.get("PageNumber", 1)
        page_size = response.get("PageSize", limit)
        
        # Calculate nextToken based on pagination information
        # If there are more items to retrieve, set nextToken to the next page number
        current_offset = (page_number - 1) * page_size
        has_more = current_offset + len(items) < total_count
        next_token = f"page_{page_number + 1}" if has_more else ""
        
        # Extract only Id and Name from each workspace
        filtered_workspaces = []
        for workspace in items:
            filtered_workspace = {
                "Id": workspace.get("Id"),
                "Name": workspace.get("Name"),
                "Url": f"https://console.volcengine.com/cp/region:cp+{region}/v2/workspace/{workspace.get('Id')}"
            }
            filtered_workspaces.append(filtered_workspace)
            
        result = {
            "Workspaces": filtered_workspaces,
            "NextToken": next_token,
            "TotalCount": total_count
        }
        return result
    
    # Return empty result if request fails
    return {
        "Workspaces": [],
        "NextToken": "",
        "TotalCount": 0
    }

@mcp.tool(name="list_pipelines", description="List pipelines of specified workspace with pagination support")
async def list_pipelines(
    workspace_id: str, # Workspace ID to list pipelines from
    name: str = None,  # Filter by pipeline name
    limit: int = 20,   # Maximum number of items to return, default is 20
    page_token: str | None = None   # Cursor for pagination
) -> typing.Dict[str, typing.Any]:
    """List pipelines of specified workspace with pagination support.
    
    This tool allows you to query and retrieve a list of pipelines from the CodePipeline service.
    You can filter pipelines by name, control the number of results per page, and navigate through
    large result sets using pagination tokens.
    
    Args:
        workspace_id: Workspace ID to list pipelines from
        name: Optional. Filter pipelines by name. If provided, only pipelines whose names
              contain this string will be returned.
        limit: Optional. Maximum number of pipelines to return per page. Default is 20,
               and valid values are between 1 and 100.
        page_token: Optional. Pagination token to retrieve the next page of results.
                    This token should be obtained from the 'NextToken' field in the
                    response of a previous list_pipelines call.
                    Format: "page_{page_number}" (e.g., "page_2" for the second page)
    
    Returns:
        A dictionary containing the following fields:
        - Pipelines: List of pipeline objects, each containing details like Id, Name,

                      Status, StatusSummary, CreateTime, UpdateTime, and Arn.
        - NextToken: Token to use for retrieving the next page of results. If empty,
                     there are no more results.
        - TotalCount: Total number of pipelines that match the filter criteria.
    
    Example Usage:
        # Get first page of pipelines for workspace "ws-123", up to 10 items
        response = await list_pipelines(workspace_id="ws-123", limit=10)
        
        # Get next page using the returned NextToken
        if response['NextToken']:
            next_page = await list_pipelines(
                workspace_id="ws-123",
                limit=10,
                page_token=response['NextToken']
            )
        
        # Filter pipelines by name containing "dev"
        filtered_pipelines = await list_pipelines(
            workspace_id="ws-123",
            name="dev",
            limit=20
        )
    
    Raises:
        ValueError: If the provided page_token has an invalid format.
    """
    # Initialize client if not already initialized
    global client
    if client is None:
        init_client()

    # 解析 page_token → 当前页码
    current_page = 1
    if page_token:
        if not page_token.startswith("page_"):
            raise ValueError("Invalid page_token")
        try:
            current_page = int(page_token.split("_")[1])
        except (IndexError, ValueError):
            raise ValueError("Invalid page_token format")

    # Build request parameters
    request_params = {
        "WorkspaceId": workspace_id,
        "Filter": {
            "Name": name
        },
        "PageNumber": current_page,
        "PageSize": limit,
    }

    # Send request to get pipeline list
    response = send_cp_request(request_params, action="ListPipelines")
    
    # Process response data and return pipeline list with pagination info
    if response:
        # Extract necessary data from response
        items = response.get("Items", [])
        total_count = response.get("TotalCount", 0)
        page_number = response.get("PageNumber", 1)
        page_size = response.get("PageSize", limit)
        
        # Calculate nextToken based on pagination information
        # If there are more items to retrieve, set nextToken to the next page number
        current_offset = (page_number - 1) * page_size
        has_more = current_offset + len(items) < total_count
        next_token = f"page_{page_number + 1}" if has_more else ""

        filtered_pipelines = []
        for pipeline in items:
            # 处理Spec字段，尝试将YAML字符串解析为字典
            spec_value = pipeline.get("Spec")
            if spec_value:
                try:
                    # 尝试将YAML字符串解析为Python字典
                    parsed_spec = yaml.safe_load(spec_value)
                    spec_value = parsed_spec
                except yaml.YAMLError as e:
                    logger.warning(f"Failed to parse Spec as YAML: {e}")
                    # 如果解析失败，保留原始字符串
                    pass
            
            filtered_pipeline = {
                "Id": pipeline.get("Id"),
                "Name": pipeline.get("Name"),
                "WorkspaceId": pipeline.get("WorkspaceId"),
                "Description": pipeline.get("Description"),
                "Spec": spec_value,
                "Url": f"https://console.volcengine.com/cp/region:cp+{region}/v2/workspace/{pipeline.get('WorkspaceId')}/pipeline/{pipeline.get('Id')}"
            }
            filtered_pipelines.append(filtered_pipeline)
        
        result = {
            "Pipelines": filtered_pipelines,
            "NextToken": next_token,
            "TotalCount": total_count
        }
        return result
    
    # Return empty result if request fails
    return {
        "Pipelines": [],
        "NextToken": "",
        "TotalCount": 0
    }

@mcp.tool(name="list_pipeline_runs", description="List pipelineruns of specified pipeline with pagination support")
async def list_pipeline_runs(
    workspace_id: str, # Workspace ID
    pipeline_id: str,  # Pipeline ID
    limit: int = 3,   # Maximum number of items to return, default is 3
    page_token: str | None = None   # Cursor for pagination
) -> typing.Dict[str, typing.Any]:
    """List pipeline runs of specified pipeline with pagination support.
    
    This tool allows you to query and retrieve a list of pipeline runs for a specific pipeline
    from the CodePipeline service. You can control the number of results per page and navigate 
    through large result sets using pagination tokens.
    
    Args:
        workspace_id: Workspace ID that contains the pipeline.
        pipeline_id: Pipeline ID to list runs for.
        limit: Optional. Maximum number of pipeline runs to return per page. Default is 3,
               and valid values are between 1 and 100.
        page_token: Optional. Pagination token to retrieve the next page of results.
                    This token should be obtained from the 'NextToken' field in the
                    response of a previous list_pipeline_runs call.
    
    Returns:
        A dictionary containing the following fields:
        - PipelineRuns: List of pipeline run objects, each containing details like Id, 
                        PipelineId, WorkspaceId, Status, StartTime, FinishTime, Index,
                        Parameters, Trigger, Spec, and Stages.
        - NextToken: Token to use for retrieving the next page of results. If empty,
                     there are no more results.
    
    Example Usage:
        # Get first page of pipeline runs for pipeline "p-123" in workspace "ws-123", up to 5 items
        response = await list_pipeline_runs(workspace_id="ws-123", pipeline_id="p-123", limit=5)
        
        # Get next page using the returned NextToken
        if response['NextToken']:
            next_page = await list_pipeline_runs(
                workspace_id="ws-123",
                pipeline_id="p-123",
                limit=5,
                page_token=response['NextToken']
            )
    
    Raises:
        ValueError: If the provided parameters are invalid.
    """

    # Initialize client if not already initialized
    global client
    if client is None:
        init_client()

    # page_token 是 realtoken 不需要处理
    # Build request parameters
    request_params = {
        "WorkspaceId": workspace_id,
        "PipelineId": pipeline_id,
        "NextToken": page_token,
        "MaxResults": limit,
    }

    # Send request to get pipelinerun list
    response = send_cp_request(request_params, action="ListPipelineRuns")
    
    # Process response data and return pipelinerun list with pagination info
    if response:
        # Extract necessary data from response
        items = response.get("Items", [])
        next_token = response.get("NextToken", "")
        

        filtered_pipelineruns = []
        for pipelinerun in items:
            spec_value = pipelinerun.get("Spec")
            if spec_value:
                try:
                    # 尝试将YAML字符串解析为Python字典
                    parsed_spec = yaml.safe_load(spec_value)
                    spec_value = parsed_spec
                except yaml.YAMLError as e:
                    logger.warning(f"Failed to parse Spec as YAML: {e}")
                    # 如果解析失败，保留原始字符串
                    pass

            filtered_pipelinerun = {
                "Id": pipelinerun.get("Id"),
                "PipelineId": pipeline_id,
                "WorkspaceId": workspace_id,
                "Status": pipelinerun.get("Status"),
                "StartTime": pipelinerun.get("StartTime"),
                "FinishTime": pipelinerun.get("FinishTime"),
                "Index": pipelinerun.get("Index"),
                "Parameters": pipelinerun.get("Parameters", {}),
                "Trigger": pipelinerun.get("Trigger"),
                "Spec": spec_value,
                "Stages": pipelinerun.get("Stages", []),
                "Url": f"https://console.volcengine.com/cp/region:cp+{region}/v2/workspace/{workspace_id}/pipeline/{pipeline_id}/record/{pipelinerun.get('Id')}",
            }
            filtered_pipelineruns.append(filtered_pipelinerun)
        
        result = {
            "PipelineRuns": filtered_pipelineruns,
            "NextToken": next_token,
        }
        return result
    
    return {
        "PipelineRuns": [],
        "NextToken": "",
    }

@mcp.tool(name="list_failed_tasks", description="List failed tasks of specified pipeline run")
async def list_failed_tasks(
    workspace_id: str, # Workspace ID
    pipeline_id: str,  # Pipeline ID
    pipeline_run_id: str,  # PipelineRun ID
) -> typing.Dict[str, typing.Any]:
    """List failed tasks of specified pipeline run.
    
    Args:
        workspace_id: Workspace ID that contains the pipeline.
        pipeline_id: Pipeline ID to list failed tasks for.
        pipeline_run_id: PipelineRun ID to list failed tasks for.
    
    Returns:
        A dictionary containing the following fields:
        - Stages: List of stage objects, each containing details like Id, Name, DisplayName, 
                  Status, and FailedTasks. FailedTasks is a list of task objects that failed 
                  in this stage.
    
    Example Usage:
        # Get failed tasks for pipeline run "pr-123" in workspace "ws-123"
        response = await list_failed_tasks(workspace_id="ws-123", pipeline_id="p-123", pipeline_run_id="pr-123")
    
    Raises:
        ValueError: If the provided parameters are invalid.
    """
    # Initialize client if not already initialized
    global client
    if client is None:
        init_client()

    # Build request parameters
    request_params = {
        "WorkspaceId": workspace_id,
        "PipelineId": pipeline_id,
        "PipelineRunId": pipeline_run_id,
    }

    # Send request to get pipelinerun details list
    response = send_cp_request(request_params, action="ListPipelineRunStagesInner")

    if response:
        # Extract necessary data from response
        stages = response.get("Items", [])
        filtered_stages = []
        for stage in stages:
            if stage.get("Status") == "Failed":
                filtered_stage = {
                    "Id": stage.get("Id"),
                    "Name": stage.get("Name"),
                    "DisplayName": stage.get("DisplayName"),
                    "Status": stage.get("Status")                
                }
                failed_tasks = []
                stage_tasks = stage.get("Tasks", [])
                for task in stage_tasks:
                    if task.get("Status") == "Failed":
                        faild_step_name = None
                        last_taskrun_id = None
                        task_id = task.get("Id")
                        for step in task.get("Steps", []):
                            if step.get("Status") == "Failed":
                                faild_step_name = step.get("Name")
                                break
                        else:
                            continue
                        taskrunsResp = list_taskruns(workspace_id, pipeline_id, pipeline_run_id, task_id)
                        taskruns = taskrunsResp.get("Items", [])
                        if taskruns:
                            last_taskrun_id = taskruns[0].get("Id")
                        failedStepLogURL = get_step_log_url(workspace_id, pipeline_id, pipeline_run_id, task_id, last_taskrun_id, faild_step_name)
                        task["FailedStepLogURL"] = failedStepLogURL
                        failed_tasks.append(task)
                filtered_stage["FailedTasks"] = failed_tasks
                filtered_stages.append(filtered_stage)
        return {
            "Stages": filtered_stages,
        }
    return {
        "Stages": [],
    }

def list_taskruns(
    workspace_id: str, # Workspace ID
    pipeline_id: str,  # Pipeline ID
    pipeline_run_id: str,  # PipelineRun ID
    task_id: str,  # Task ID
) -> typing.Dict[str, typing.Any]:
    # Initialize client if not already initialized
    global client
    if client is None:
        init_client()

    # Build request parameters only fetch latest taskrun
    request_params = {
        "WorkspaceId": workspace_id,
        "PipelineId": pipeline_id,
        "PipelineRunId": pipeline_run_id,
        "TaskId": task_id,
        "PageSize": 1,
        "PageNumber": 1,
    }

    # Send request to get taskrun list
    response = send_cp_request(request_params, action="ListTaskRuns")
    if response:
        # Return the full response to preserve the Items structure
        return response
    return {
        "Items": [],
        "PageSize": 1,
        "PageNumber": 1,
        "TotalCount": 0
    }

def get_step_log_url(
    workspace_id: str, # Workspace ID
    pipeline_id: str,  # Pipeline ID
    pipeline_run_id: str,  # PipelineRun ID
    task_id: str, # Task ID
    task_run_id: str,  # TaskRun ID
    step_name: str,  # Step name
) -> typing.Dict[str, typing.Any]:
    # Initialize client if not already initialized
    global client
    if client is None:
        init_client()

    # Build request parameters only fetch latest taskrun
    request_params = {
        "WorkspaceId": workspace_id,
        "PipelineId": pipeline_id,
        "PipelineRunId": pipeline_run_id,
        "TaskId": task_id,
        "TaskRunId": task_run_id,
        "StepName": step_name,
    }

    # Send request to get taskrun list
    response = send_cp_request(request_params, action="GetTaskRunLogDownloadURI")
    if response:
        return {
            "Url": response.get("Url"),
        }
    return {
        "Url": ""
    }

def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run CodePipeline MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (stdio or streamable-http)",
    )

    args = parser.parse_args()

    try:
        # Run the MCP server
        logger.info(f"Starting CodePipeline MCP Server with {args.transport} transport")
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting CodePipeline MCP Server: {str(e)}")
        raise




def init_client() -> any:
    """Initialize the client."""
    global client
    global region

    conf = load_config()
    region = conf.volcengine_region

    configuration = volcenginesdkcore.Configuration()
    configuration.ak = conf.volcengine_ak
    configuration.sk = conf.volcengine_sk
    configuration.host = conf.volcengine_endpoint
    configuration.region = conf.volcengine_region

    config = volcenginesdkcore.Configuration.set_default(configuration)
    client = volcenginesdkcore.UniversalApi(volcenginesdkcore.ApiClient(config))   


def send_cp_request(req: dict, action: str, version: str = "2023-05-01") -> dict[str, any] | None:
    try:
        res = client.do_call(
            volcenginesdkcore.UniversalInfo(method=API_METHOD, action=action, service=API_SERVICE, version=API_VERSION, content_type=API_CONTENT_TYPE),
            req)
        return res
    except Exception as e:
        logger.error(f"Error in send_cp_request: {str(e)}")
        return None


if __name__ == "__main__":
    main()