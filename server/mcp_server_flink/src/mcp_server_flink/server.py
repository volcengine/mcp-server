import json
import logging
import os
from datetime import datetime
from typing import Optional, Dict

from mcp.server.fastmcp import FastMCP

from mcp_server_flink.resources.event import get_gws_event_list_api
from mcp_server_flink.resources.job_development import create_gws_application_draft_api, \
    update_gws_application_draft_api, list_gws_directory_api, deploy_gws_application_draft_api, \
    offline_gws_application_api, get_gws_application_draft_api
from mcp_server_flink.resources.job_operation import list_gws_application_api, get_grs_app_by_id_api, \
    start_gws_application_api, restart_gws_application_api, stop_gws_application_api
from mcp_server_flink.resources.log import list_gas_logs_api
from mcp_server_flink.resources.project import list_gms_project_api
from mcp_server_flink.resources.resource_pool import list_gmcs_resource_pool_api
from mcp_server_flink.resources.services import JobTypeEnum, LogLevelEnum, ComponentEnum, EngineVersionEnum, \
    PriorityEnum, SchedulePolicyEnum, StartTypeEnum, JobStateEnum
from mcp_server_flink.utils.open_api_client import init_auth_openapi_context
from mcp_server_flink.utils.utils import filter_list_application_response_fields, get_project_id, get_application_id, \
    get_resource_pool_full_name, get_application_uniqued_id, filter_list_resource_pool_response_fields

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create MCP server instance
# FastMCP is a lightweight server implementation used to expose the Serverless Flink API functions
# The server is initialized with a descriptive name and port configuration
# Port is read from environment variable 'PORT' with a default fallback to 8000 if not specified
mcp = FastMCP("ServerlessFlink MCP Server",
              host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
              port=int(os.getenv("MCP_SERVER_PORT", "8000")),
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
              stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true")


@mcp.tool()
def list_flink_application(
        project_name: Optional[str] = "",
        job_name: Optional[str] = "",
        resource_pool: Optional[str] = "",
        job_state: JobStateEnum = JobStateEnum.ALL,
        job_type: JobTypeEnum = JobTypeEnum.FLINK_JOB_TYPE_ALL,
        region: Optional[str] = "",
) -> str:
    """Tool function to get the Serverless Flink application metadata (id, name, accountId, state) list.

    Args:
        project_name: Optional Flink project name used to identify the project to query (default: ""). If not provided, query all flink applications.
        job_name: Optional job name used to filter applications by name (default: "").
        resource_pool: Optional resource pool name used to filter applications by resource pool (default: "").
        job_state: Job State filter for the applications (default: JobStateEnum.ALL). Available states:
            ALL: All job states (default)
            CREATED: Job has been created but not started
            STARTING: Job is in the process of starting
            RUNNING: Job is currently running
            FAILED: Job has failed
            CANCELLING: Job is in the process of being cancelled
            SUCCEEDED: Job completed successfully
            STOPPED: Job has been stopped
        job_type: Job type filter for the applications (default: JobTypeEnum.FLINK_JOB_TYPE_ALL).
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: List of the serverless flink applications. Each application entry is a dictionary
        containing the applications id, appId, name, currentEmitEventTimeLag (means business application delay) and other metadata, e.g. Total, Size, Current.
        If you need to query the detailed information of the job, you can use the get_flink_application_detail tool.

    Examples:
        # get serverless flink applications with multiple filters
        list_flink_application(project_id="project_id", job_name="my_job", resource_pool="compute-pool", job_type=JobTypeEnum.FLINK_BATCH_SQL, job_state=JobStateEnum.RUNNING)
    """
    logger.info(
        f"Received list_flink_application request with project_name: {project_name}, job_name: {job_name}, resource_pool: {resource_pool}, job_type: {job_type}, job_state: {job_state}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)

        logger.info(
            f"Listing serverless flink application with project_id: {project_id}, job_name: {job_name}, resource_pool: {resource_pool}, job_type: {job_type}, job_state: {job_state}"
        )

        response = list_gws_application_api(openapi_context, project_id, job_name, resource_pool, job_state, job_type)
        fields = ["Id", "AccountId", "ApplicationId", "JobName", "JobType", "EngineVersion", "State", "CreateTime",
                  "DeployTime", "StartTime", "EndTime", "CurrentEmitEventTimeLag"]
        filtered_response = filter_list_application_response_fields(response, fields)

        return json.dumps(filtered_response)
    except Exception as e:
        logger.error(f"Error in list_flink_application: {str(e)}")
        return str(e)


@mcp.tool()
def get_flink_application_detail(
        project_name: str,
        job_name: str,
        region: Optional[str] = "",
) -> str:
    """Tool function to retrieve detailed information about a Serverless Flink application.

    Args:
        project_name: Flink project name used to identify the project to query.
        job_name: The job name of the Flink application to retrieve details for.
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: A string representation containing detailed information about the Flink application.
            This includes configuration, status, resource allocation, and other metadata.
            In case of an error, an error message will be returned.

    Examples:
        # Get application details by job name and project name
        get_flink_application_detail(project_name="project_name", job_name="my_job")
    """
    logger.info(f"Received get_flink_application request with job_name: {job_name}, project_name: {project_name}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)

        logger.info(
            f"Getting serverless flink application detail with job_name: {job_name}, project_id: {project_id}"
        )

        response = list_gws_application_api(openapi_context=openapi_context, job_name=job_name, project_id=project_id)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in get_flink_application: {str(e)}")
        return str(e)


@mcp.tool()
def get_flink_runtime_application_info(
        project_name: str,
        job_name: str,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to retrieve runtime information for a Serverless Flink application.

    This function fetches detailed runtime information. The information typically includes jobManager podList & taskManager podList,
    resource metrics, configuration, and other operational details about the running application.

    Args:
        project_name: Flink project name used to identify the project to query.
        job_name: The job name of the Flink application to retrieve details for.
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: A string representation of the application's runtime information.
            This may include metrics, status, configuration details, and other
            operational data. In case of an error, an error message will be returned.

    Examples:
        # Get runtime information for a specific Flink application
        get_flink_runtime_application_info("s-app_123456789")
    """
    logger.info(
        f"Received get_flink_runtime_application_info request with job_name: {job_name}, project_name: {project_name}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        application_id = get_application_id(openapi_context, job_name, project_id)

        logger.info(
            f"Get serverless flink application runtime information with application_id: {application_id}"
        )

        response = get_grs_app_by_id_api(openapi_context, application_id)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in get_flink_runtime_application_info: {str(e)}")
        return str(e)


@mcp.tool()
def list_flink_application_log(
        project_name: str,
        job_name: str,
        start_time: datetime,
        end_time: datetime,
        level: LogLevelEnum = LogLevelEnum.ALL,
        component: ComponentEnum = ComponentEnum.JOBMANAGER,
        pod_name: str = "",
        cursor: str = "",
        page_size: int = 500,
        region: Optional[str] = "",
) -> str:
    """Tool function to retrieve logs for a Serverless Flink application.

    This function fetches log entries for a specified Flink application based on the provided
    filtering criteria. It allows querying logs within a specific time range, filtering by log level,
    component type, specific pod name, and supports pagination for handling large log volumes.

    Args:
        project_name: Flink project name used to identify the project to query.
        job_name: The job name of the Flink application to retrieve details for.
        start_time: The start time for log retrieval in datetime format (in %Y-%m-%dT%H:%M:%S).
        end_time: The end time for log retrieval in datetime format (in %Y-%m-%dT%H:%M:%S).
        level: The log level to filter by (default: LogLevelEnum.ALL). Use the ERROR level for logging exception messages.
        component: The component type to filter logs by (default: ComponentEnum.JOBMANAGER). Some common exception messages can be viewed in the JOBMANAGER.
        pod_name: Optional specific pod name to filter logs from (default: "" for all pods).
        cursor: Optional cursor value for pagination (default: ""). Required for scrolling queries and typically provided in response.
                Example cursor values: "0,1761740046380,1870334373891,6116168"
        page_size: Optional number of log entries to return per page (default: 500).
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: The response containing the requested log entries. Each log entry typically includes
            timestamp, level, message, cursor value and other relevant metadata. For scrolling queries,
            the response Cursor field will include a cursor value to retrieve the next set of logs.

    Examples:
        # Get logs from JOBMANAGER component with pagination
        list_flink_application_log("app_123", "project_456", "2025-10-30T19:45:02", "2025-10-30T19:51:07", page_size=100)

        # Get ERROR level logs from specific TASKMANAGER pod with pagination and cursor
        list_flink_application_log(
            "app_123",
            "project_456",
            "2025-10-30T19:45:02",
            "2025-10-30T19:51:07",
            level=LogLevelEnum.ERROR,
            component=ComponentEnum.TASKMANAGER,
            pod_name="flink-taskmanager-0",
            cursor="0,1761740046380,1870334373891,6116168",
            page_size=200
        )
    """
    logger.info(f"Received list_flink_application_log request with project_name: "
                f"{project_name}, job_name: {job_name}, start_time: {start_time}, end_time: {end_time}, level: {level}, component: {component}, pod_name: {pod_name}, cursor: {cursor}, page_size: {page_size}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        application_id = get_application_id(openapi_context, job_name, project_id)

        logger.info(
            f"Listing serverless flink application log with project_id: "
            f"{project_id}, application_id: {application_id}, start_time: {int(start_time.timestamp() * 1000)}, end_time: {int(end_time.timestamp() * 1000)}, level: {level}, component: {component}, pod_name: {pod_name}, cursor: {cursor}, page_size: {page_size}"
        )

        response = list_gas_logs_api(openapi_context, application_id, project_id, int(start_time.timestamp() * 1000),
                                     int(end_time.timestamp() * 1000), level, component, pod_name, cursor, page_size)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in list_flink_application_log: {str(e)}")
        return str(e)


@mcp.tool()
def get_flink_application_event(
        project_name: str,
        job_name: str,
        limit: int = 50,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to retrieve events for a Serverless Flink application.
    
    This function fetches event logs for a specified Flink application based on the provided
    project name, job name, and optional filtering parameters.
    
    Args:
        project_name: Flink project name used to identify the project containing the application.
        job_name: The name of the Flink job application to retrieve events for.
        limit: Optional maximum number of events to return (default: 50).
        region: Optional region name used to filter applications by region (default: "").
        
    Returns:
        str: The response containing the requested event list in JSON format.
            In case of an error, an error message will be returned as a string.
            
    Examples:
        # Get events with default limit
        get_flink_application_event("project_123", "my_job")
    """
    logger.info(f"Received get_flink_application_event request with project_name: "
                f"{project_name}, job_name: {job_name}, limit: {limit}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        application_uniqued_id = get_application_uniqued_id(openapi_context, job_name, project_id)

        logger.info(
            f"Getting serverless flink application event with project_id: "
            f"{project_id}, application_uniqued_id: {application_uniqued_id}, limit: {limit}")

        response = get_gws_event_list_api(openapi_context, project_id, application_uniqued_id, limit)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in get_flink_application_event: {str(e)}")
        return str(e)


@mcp.tool()
def list_flink_project(
        search_key: Optional[str] = "",
        region: Optional[str] = "",
) -> str:
    """Tool function to query Flink project list
    
    Args:
        search_key: Optional Search keyword used to filter project list (default: ""). If not provided, query the total flink project list.
        region: Optional region name used to filter applications by region (default: "").
        
    Returns:
        str: List of the serverless flink projects. Each project entry is a dictionary
        containing the project name, projectId, and other metadata.

    Examples:
        # get serverless flink projects by project_name
        list_flink_project("project_name")
    """
    logger.info(f"Received list_flink_project request with search_key: {search_key}")

    openapi_context = init_auth_openapi_context(region, "", mcp.get_context())
    try:
        logger.info(
            f"Listing serverless flink project with search_key: {search_key}"
        )

        response = list_gms_project_api(openapi_context, search_key)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in list_flink_application: {str(e)}")
        return str(e)


@mcp.tool()
def list_flink_directory(
        project_name: Optional[str] = "",
        region: Optional[str] = "",
) -> str:
    """Tool function to get the Serverless Flink directory list

    Args:
        project_name: Optional Flink project name used to identify the project to query.
            If not provided, query all directories.
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: List of serverless flink directories. Each directory entry contains 
            directory information such as name, directory_id, Applications(include draft_id) and other metadata.

    Examples:
        # get serverless flink directory list by project_id
        list_flink_directory("project_name")
    """

    logger.info(f"Received list_flink_directory request with project_id: {project_name}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        logger.info(
            f"Listing serverless flink directory with project_id: {project_id}"
        )

        response = list_gws_directory_api(openapi_context, project_id)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in list_flink_directory: {str(e)}")
        return str(e)


@mcp.tool()
def list_flink_resource_pool(
        project_name: str,
        name: Optional[str] = "",
        name_key: Optional[str] = "",
        region: Optional[str] = "",
) -> str:
    """
    Tool function to list Serverless Flink resource pools.
    
    This function retrieves information about resource pools associated with a specific Flink project.
    It supports filtering resource pools by a search key for the name.
    
    Args:
        project_name: Flink project name used to identify the project to query.
        name: Optional resource pool name used to filter resource pools by name (default: "").
            If not provided, all resource pools for the project will be returned.
        name_key: Optional search keyword used to filter resource pools by name (default: "").
            If not provided, all resource pools for the project will be returned.
        region: Optional region name used to filter applications by region (default: "").
    
    Returns:
        str: The response containing a list of serverless Flink resource pools. Each pool entry
            contains information such as name, queue full_name, ID, region, zone, BillingType,and other metadata.
            The BillingType field indicates the billing mode: POST means pay-as-you-go billing， PRE means subscription-based billing (annual or monthly).
            In case of an error, an error message will be returned as a string.
    
    Examples:
        # Get resource pools filtered by a name keyword
        list_flink_resource_pool("project_123", "compute-pool")
    """
    logger.info(f"Received list_flink_resource_pool request with project_name: {project_name}, search_key: {name_key}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        logger.info(
            f"Listing serverless flink resource pool with project_id: {project_id}, search_key: {name_key}"
        )

        response = list_gmcs_resource_pool_api(openapi_context, project_id, name, name_key)
        fields = ["Id", "RegionId", "ZoneId", "Name", "FullName", "Status", "BillingType", "Weight",
                  "Resources", "CreateTime", "UpdateTime", "UserName", "ExpirationTime", "ResourceDomainType"]
        filtered_response = filter_list_resource_pool_response_fields(response, fields)
        return json.dumps(filtered_response)
    except Exception as e:
        logger.error(f"Error in list_flink_resource_pool: {str(e)}")
        return str(e)


@mcp.tool()
def create_flink_application_draft(
        job_name: str,
        project_name: str,
        directory_id: str,
        job_type: JobTypeEnum = JobTypeEnum.FLINK_STREAMING_SQL,
        engine_version: EngineVersionEnum = EngineVersionEnum.FLINK_VERSION_1_17,
        region: Optional[str] = "",
) -> str:
    """Tool function to create a new Serverless Flink application draft

    Args:
        job_name: The name of the Flink job application
        project_name: Flink project name used to identify the project to query.
        directory_id: The ID of the directory to place the application
        job_type: The type of Flink job (default: FLINK_STREAMING_SQL)
        engine_version: The Flink engine version to use (default: FLINK_VERSION_1_17)
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: The response from the API call, containing information about the created application draft.
            such as id, account_id, user_id, job_name, job_id, directory_id, directory_name and other metadata.

    Examples:
        # create serverless flink application draft with default parameters
        create_flink_application_draft("my_job", "project_123", "dir_456")

        # create serverless flink application draft with specific parameters
        create_flink_application_draft(
            "my_batch_job", 
            "project_123", 
            "dir_456", 
            JobTypeEnum.FLINK_BATCH_SQL,
            EngineVersionEnum.FLINK_VERSION_1_16
        )
    """
    logger.info(
        f"Received create_flink_application_draft request with job_name: {job_name}, project_name: {project_name}, job_type: {job_type}, engine_version: {engine_version}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        logger.info(
            f"Creating serverless flink application draft with job_name: {job_name}, project_id: {project_id}, directory_id: {directory_id}, job_type: {job_type}, engine_version: {engine_version}"
        )

        response = create_gws_application_draft_api(openapi_context, job_name, project_id, directory_id, job_type,
                                                    engine_version)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in create_flink_application_draft: {str(e)}")
        return str(e)


@mcp.tool()
def get_flink_application_draft(
        draft_id: str,
        project_name: str,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to retrieve a Serverless Flink application draft.
    
    This function fetches the details of a previously created Flink application draft
    based on the provided draft ID and project name.
    
    Args:
        draft_id: The unique identifier of the application draft to retrieve.
        project_name: Flink project name used to identify the project containing the draft.
        region: Optional region name used to filter applications by region (default: "").
        
    Returns:
        str: The response containing the application draft details in JSON format.
            In case of an error, an error message will be returned as a string.
            
    Examples:
        # Get an application draft by draft ID and project name
        get_flink_application_draft("1986054013710225409", "project_name")
    """
    logger.info(
        f"Received get_flink_application_draft request with draft_id: {draft_id}, project_name: {project_name}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        logger.info(
            f"Getting serverless flink application draft with draft_id: {draft_id}, project_id: {project_id}"
        )

        response = get_gws_application_draft_api(openapi_context, project_id, draft_id)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in get_flink_application_draft: {str(e)}")
        return str(e)


@mcp.tool()
def update_flink_application_draft(
        id: str,
        project_id: str,
        account_id: str,
        user_id: str,
        job_name: str,
        job_id: str,
        directory_id: str,
        directory_name: str,
        sql_text: str,
        dynamic_options: Dict[str, str] = None,
        job_type: JobTypeEnum = JobTypeEnum.FLINK_STREAMING_SQL,
        engine_version: EngineVersionEnum = EngineVersionEnum.FLINK_VERSION_1_17,
        region: Optional[str] = "",
) -> str:
    """Tool function to update an existing Serverless Flink application draft

    Args:
        id: The ID of the application draft to update
        project_id: The ID of the Flink project
        account_id: The ID of the account associated with the application
        user_id: The ID of the user making the update
        job_name: The name of the Flink job application
        job_id: The ID of the job
        directory_id: The ID of the directory containing the application
        directory_name: The name of the directory containing the application
        sql_text: The SQL text for the Flink job
        dynamic_options: Optional dictionary of dynamic configuration options for the job
        job_type: The type of Flink job (default: FLINK_STREAMING_SQL)
        engine_version: The Flink engine version to use (default: FLINK_VERSION_1_17)
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: The response from the API call, containing information about the updated application draft

    Examples:
        # update serverless flink application draft with basic parameters
        update_flink_application_draft(
            id="draft_123",
            project_id="project_123",
            account_id="account_456",
            user_id="user_789",
            job_name="updated_job",
            job_id="job_123",
            directory_id="dir_456",
            directory_name="My Directory",
            sql_text="SELECT * FROM source_table"
        )

        # update with dynamic options
        update_flink_application_draft(
            id="draft_123",
            project_id="project_123",
            account_id="account_456",
            user_id="user_789",
            job_name="updated_job",
            job_id="job_123",
            directory_id="dir_456",
            directory_name="My Directory",
            sql_text="SELECT * FROM source_table",
            dynamic_options={"parallelism.default": "4"},
            job_type=JobTypeEnum.FLINK_BATCH_SQL
        )
    """
    logger.info(
        f"Received update_flink_application_draft request with job_name: {job_name}, project_id: {project_id}, job_type: {job_type}, engine_version: {engine_version}")

    openapi_context = init_auth_openapi_context(region, "", mcp.get_context())
    try:
        logger.info(
            f"Updating serverless flink application draft with job_name: {job_name}, project_id: {project_id}, job_type: {job_type}, engine_version: {engine_version}"
        )

        response = update_gws_application_draft_api(openapi_context, id, project_id, account_id, user_id, job_name,
                                                    job_id, directory_id,
                                                    directory_name, sql_text, dynamic_options, job_type, engine_version)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in update_flink_application_draft: {str(e)}")
        return str(e)


@mcp.tool()
def deploy_flink_application_draft(
        project_id: str,
        id: str,
        resource_pool: str,
        priority: PriorityEnum = PriorityEnum.LEVEL_3,
        schedule_policy: SchedulePolicyEnum = SchedulePolicyEnum.GANG,
        schedule_timeout: Optional[int] = 60,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to deploy a Serverless Flink application draft.

    This function deploys a previously created Flink application draft with specified 
    resource allocation parameters. It handles the deployment process including 
    resource pool assignment, queue selection, priority setting, and scheduling policies.

    Args:
        project_id: The ID of the Flink project containing the application draft.
        id: The ID of the application draft to deploy.
        resource_pool: The name of the resource pool to use for the deployment.
        priority: The priority level for the application deployment (default: PriorityEnum.LEVEL_3).
        schedule_policy: The scheduling policy to use (default: SchedulePolicyEnum.GANG).
        schedule_timeout: Optional timeout for scheduling in seconds (default: 60).
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: The response from the deployment API, containing information about the 
            deployed application. In case of an error, an error message will be returned as a string.

    Examples:
        # Deploy an application draft with default priority and scheduling
        deploy_flink_application_draft(
            project_id="project_123", 
            id="draft_456", 
            resource_pool="compute_pool"
        )

        # Deploy with custom priority and scheduling parameters
        deploy_flink_application_draft(
            project_id="project_123",
            id="draft_456",
            resource_pool="compute_pool",
            priority=PriorityEnum.LEVEL_1,
            schedule_policy=SchedulePolicyEnum.GANG,
            schedule_timeout=120
        )
    """
    logger.info(
        f"Received deploy_flink_application_draft request with project_id: {project_id}, id: {id}, resource_pool: {resource_pool}, priority: {priority}")

    openapi_context = init_auth_openapi_context(region, "", mcp.get_context())
    try:
        queue = get_resource_pool_full_name(openapi_context, resource_pool, project_id)
        logger.info(
            f"Deploying serverless flink application draft with project_id: {project_id}, id: {id}, resource_pool: {resource_pool}, queue: {queue}, priority: {priority}"
        )

        response = deploy_gws_application_draft_api(openapi_context, project_id, id, resource_pool, queue, priority,
                                                    schedule_policy,
                                                    schedule_timeout)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in deploy_flink_application_draft: {str(e)}")
        return str(e)


@mcp.tool()
def offline_flink_application_to_draft(
        job_name: str,
        project_name: str,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to offline a Serverless Flink application and transition it to the draft state. If the application is still running, the
    offline request will fail. If the job is already in the Stopped state, it can be Offline to the job draft state and then redeployed.

    Args:
        job_name: The name of the Flink job application to offline.
        project_name: Flink project name used to identify the project containing the application.
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: The response from the offline API call, containing information about the operation result.
            In case of an error, an error message will be returned as a string.
    """
    logger.info(
        f"Received offline_flink_application_to_draft request with job_name: {job_name}, project_name: {project_name}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        application_uniqued_id = get_application_uniqued_id(openapi_context, job_name, project_id)
        logger.info(
            f"Offline serverless flink offline_flink_application_to_draft with project_id: {project_id}, application_uniqued_id: {application_uniqued_id}"
        )

        response = offline_gws_application_api(openapi_context, project_id, application_uniqued_id)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in offline_flink_application_to_draft: {str(e)}")
        return str(e)


@mcp.tool()
def start_flink_application(
        job_name: str,
        project_name: str,
        start_type: StartTypeEnum = StartTypeEnum.FROM_NEW,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to start a Serverless Flink application.

    This function initiates the execution of a previously deployed Flink application
    with the specified configuration and start type. It handles the application
    startup process including configuration management and state initialization.

    Args:
        job_name: The name of the Flink job application
        project_name: Flink project name used to identify the project to query.
        start_type: The type of start operation to perform (default: StartTypeEnum.FROM_NEW).
            Determines whether to start from a new state or resume from a previous checkpoint.
        region: Optional region name used to filter applications by region (default: "").

    Returns:
        str: The response from the start API, containing information about the started
            application instance. In case of an error, an error message will be returned as a string.
    """
    logger.info(
        f"Received start_flink_application request with job_name: {job_name}, project_name: {project_name}, start_type: {start_type}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        application_uniqued_id = get_application_uniqued_id(openapi_context, job_name, project_id)
        logger.info(
            f"Starting serverless flink application with project_id: {project_id}, application_uniqued_id: {application_uniqued_id}, start_type: {start_type}"
        )

        response = start_gws_application_api(openapi_context, project_id, application_uniqued_id, start_type)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in start_flink_application: {str(e)}")
        return str(e)


@mcp.tool()
def stop_flink_application(
        job_name: str,
        project_name: str,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to stop a running Serverless Flink application.
    
    This function stops the execution of a currently running Flink application
    identified by its job name and project name.
    
    Args:
        job_name: The name of the Flink job application to stop.
        project_name: Flink project name used to identify the project containing the application.
        region: Optional region name used to filter applications by region (default: "").
        
    Returns:
        str: The response from the stop API call, containing information about the operation result.
            In case of an error, an error message will be returned as a string.
    """
    logger.info(
        f"Received stop_flink_application request with job_name: {job_name}, project_name: {project_name}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        application_uniqued_id = get_application_uniqued_id(openapi_context, job_name, project_id)
        logger.info(
            f"Stopping serverless flink application with project_id: {project_id}, application_uniqued_id: {application_uniqued_id}"
        )

        response = stop_gws_application_api(openapi_context, project_id, application_uniqued_id)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in stop_flink_application: {str(e)}")
        return str(e)


@mcp.tool()
def restart_flink_application(
        job_name: str,
        project_name: str,
        start_type: StartTypeEnum = StartTypeEnum.FROM_NEW,
        region: Optional[str] = "",
) -> str:
    """
    Tool function to restart a Serverless Flink application by using atomic operation.
    
    This function restarts a Flink application with specified start type, allowing users to choose between starting from new state or resuming from latest checkpoint.
    It will first stop the running application (if any), and then start it again according to the selected start mode.
    
    Args:
        job_name: The name of the Flink job application to restart.
        project_name: Flink project name used to identify the project containing the application.
        start_type: The type of start operation to perform (default: StartTypeEnum.FROM_NEW).
            FROM_NEW: Start from a completely new state
            FROM_LATEST: Resume from the latest available checkpoint
        region: Optional region name used to filter applications by region (default: "").
        
    Returns:
        str: The response from the restart API call, containing information about the operation result.
            In case of an error, an error message will be returned as a string.
            
    Examples:
        # Restart a Flink application from new state
        restart_flink_application("my_job", "project_123")
    """
    logger.info(
        f"Received restart_flink_application request with job_name: {job_name}, project_name: {project_name}, start_type: {start_type}")

    openapi_context = init_auth_openapi_context(region, project_name, mcp.get_context())
    try:
        project_id = get_project_id(openapi_context, openapi_context.project_name)
        application_uniqued_id = get_application_uniqued_id(openapi_context, job_name, project_id)
        logger.info(
            f"Restarting serverless flink application with project_id: {project_id}, application_uniqued_id: {application_uniqued_id}, start_type: {start_type}"
        )

        response = restart_gws_application_api(openapi_context, project_id, application_uniqued_id, start_type)
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Error in restart_flink_application: {str(e)}")
        return str(e)
