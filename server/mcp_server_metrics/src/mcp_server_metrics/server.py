import logging
import os
from typing import Optional, Dict, List, Any

from mcp.server.fastmcp import Context, FastMCP

from mcp_server_metrics.api import MetricsApi
from mcp_server_metrics.config import MetricsConfig, load_config, parse_authorization
from mcp_server_metrics.model import (
    ListWorkspaceRequest,
    ListWorkspaceResponse,
    GetWorkspaceInfoRequest,
    GetWorkspaceInfoResponse,
    ListQueryClustersRequest,
    ListQueryClustersResponse,
    GetQueryClusterRequest,
    GetQueryClusterResponse,
    ListPreaggRequest,
    ListPreaggResponse,
    InfluxQueryRequest,
    InfluxQueryResponse,
    MetricsQueryRequest,
    MetricsQueryResponse,
)

# Initialize logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    os.getenv("MCP_SERVER_NAME", "mcp_server_metrics"),
    port=int(os.getenv("MCP_SERVER_PORT", "8000")),
    host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
    streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp")
)


def init_auth_config() -> MetricsConfig:
    """Initialize auth config from env or request context."""
    conf = load_config()  # load default config from env

    # Get context from request if available
    try:
        ctx: Context = mcp.get_context()
        raw_request = ctx.request_context.request

        auth = None
        if raw_request:
            auth = raw_request.headers.get("authorization", None)
        if auth is None:
            auth = os.getenv("authorization", None)
        if auth is not None:
            if " " in auth:
                _, base64_data = auth.split(" ", 1)
            else:
                base64_data = auth

            config = parse_authorization(base64_data)
            return config
    except Exception as e:
        logger.warning(f"Failed to parse authorization from context: {e}")

    if not conf.is_valid():
        raise ValueError("No valid auth info found")
    return conf


@mcp.tool()
async def list_workspace(
    region: str = "cn-beijing",
    PageNumber: int = 1,
    PageSize: int = 10,
    Name: str = "",
    ProjectName: str = "default",
    ListGlobal: bool = False,
):
    """
    List workspaces from the metrics console.

    Args:
        region: Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou, default: cn-beijing)
        PageNumber: Page number for pagination (default: 1)
        PageSize: Page size for pagination (default: 10)
        Filters: Filters to apply (optional, Filters only support filtering by "Name" parameter for workspace names.)
        ProjectName: Project name (default: "default")
        ListGlobal: Whether to list global workspaces (default: False)

    Returns:
        List of workspaces with metadata
    """
    try:
        if PageNumber < 1:
            raise ValueError("PageNumber must be at least 1")
        if PageSize < 1 or PageSize > 100:
            raise ValueError("PageSize must be between 1 and 100")

        req = ListWorkspaceRequest(
            region=region,
            PageNumber=PageNumber,
            PageSize=PageSize,
            Filters={"Name": Name} if Name else None,
            ProjectName=ProjectName,
            ListGlobal=ListGlobal,
        )

        config = init_auth_config()
        api = MetricsApi(config)
        return api.list_workspaces(req)
    except ValueError as e:
        logger.error(f"Validation error in list_workspace: {e}")
        raise
    except Exception as e:
        logger.error(f"Error in list_workspace: {e}")
        raise


@mcp.tool()
async def get_workspace(
    WorkspaceID: str,
    region: str = "cn-beijing",
):
    """
    Get workspace information from the metrics console.

    Args:
        WorkspaceID: Workspace ID
        region: Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou, default: cn-beijing)

    Returns:
        Workspace information
    """
    try:
        req = GetWorkspaceInfoRequest(
            WorkspaceID=WorkspaceID,
            region=region,
        )

        config = init_auth_config()
        api = MetricsApi(config)
        return api.get_workspace_info(req)
    except Exception as e:
        logger.error(f"Error in get_workspace: {e}")
        raise


@mcp.tool()
async def list_query_clusters(
    region: str = "cn-beijing",
    PageNumber: int = 1,
    PageSize: int = 10,
    Name: str = "",
    ProjectName: str = "default",
):
    """
    List query clusters from the metrics console.

    Args:
        region: Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou, default: cn-beijing)
        PageNumber: Page number for pagination (default: 1)
        PageSize: Page size for pagination (default: 10)
        Name: Cluster name to filter (optional)
        ProjectName: Project name (default: "default")

    Returns:
        List of query clusters with metadata
    """
    try:
        if PageNumber < 1:
            raise ValueError("PageNumber must be at least 1")
        if PageSize < 1 or PageSize > 100:
            raise ValueError("PageSize must be between 1 and 100")
        
        req = ListQueryClustersRequest(
            region=region,
            PageNumber=PageNumber,
            PageSize=PageSize,
            Name=Name,
            ProjectName=ProjectName
        )

        config = init_auth_config()
        api = MetricsApi(config)
        return api.list_query_clusters(req)
    except Exception as e:
        logger.error(f"Error in list_query_clusters: {e}")
        raise


@mcp.tool()
async def get_query_cluster(
    ClusterID: str,
    region: str = "cn-beijing",
):
    """
    Get query cluster information from the metrics console.

    Args:
        ClusterID: Query cluster ID
        region: Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou, default: cn-beijing)

    Returns:
        Query cluster information
    """
    try:
        req = GetQueryClusterRequest(
            ClusterID=ClusterID,
            region=region,
        )

        config = init_auth_config()
        api = MetricsApi(config)
        return api.get_query_cluster(req)
    except Exception as e:
        logger.error(f"Error in get_query_cluster: {e}")
        raise


@mcp.tool()
async def list_preagg(
    WorkspaceName: str,
    region: str = "cn-beijing",
    PageNumber: int = 1,
    PageSize: int = 10,
    onlyShowMine: bool = True,
):
    """
    List preaggregation rules from the metrics console.

    Args:
        WorkspaceName: Workspace name to filter (required)
        region: Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou, default: cn-beijing)
        PageNumber: Page number for pagination (default: 1)
        PageSize: Page size for pagination (default: 10)
        onlyShowMine: Whether to only show rules created by current user (default: True)

    Returns:
        List of preaggregation rules with metadata
    """
    try:
        # 参数验证
        if PageNumber < 1:
            raise ValueError("PageNumber must be at least 1")
        if PageSize < 1 or PageSize > 100:
            raise ValueError("PageSize must be between 1 and 100")
        if not WorkspaceName:
            raise ValueError("WorkspaceName is required")

        req = ListPreaggRequest(
            WorkspaceName=WorkspaceName,
            region=region,
            PageNumber=PageNumber,
            PageSize=PageSize,
            onlyShowMine=onlyShowMine,
        )

        config = init_auth_config()
        api = MetricsApi(config)
        return api.list_preagg(req)
    except Exception as e:
        logger.error(f"Error in list_preagg: {e}")
        raise


@mcp.tool()
async def influx_query(
    Workspace: str,
    Queries: List[str],
    region: str = "cn-beijing",
    Epoch: Optional[str] = None,
):
    """
    InfluxDB query from cross cluster proxy.

    Args:
        Workspace: Workspace name
        Queries: List of InfluxQL query strings
        region: Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou, default: cn-beijing)
        Epoch: Time stamp precision (s/ms/us/ns, optional)

    Returns:
        Query results
    """
    try:
        req = InfluxQueryRequest(
            Workspace=Workspace,
            Queries=Queries,
            region=region,
            Epoch=Epoch,
        )

        config = init_auth_config()
        api = MetricsApi(config)
        return api.influx_query(req)
    except Exception as e:
        logger.error(f"Error in influx_query: {e}")
        raise


@mcp.tool()
async def metrics_query(
    Workspace: str,
    Queries: List[Dict[str, Any]],
    region: str = "cn-beijing",
    Start: str = "10m-ago",
    End: str= "now",
):
    """
    Query metrics data from cross cluster proxy.

    Args:
        Workspace: Workspace name
        Queries: List of query objects with metric details
        region: Target region (e.g. cn-beijing, cn-shanghai, cn-guangzhou, default: cn-beijing)
        Start: Start time in seconds (timestamp string)
        End: End time in seconds (timestamp string)

    Returns:
        Metrics query results
    """
    try:
        req = MetricsQueryRequest(
            Workspace=Workspace,
            Queries=Queries,
            Start=Start,
            End=End,
            region=region,
        )

        config = init_auth_config()
        api = MetricsApi(config)
        return api.metrics_query(req)
    except Exception as e:
        logger.error(f"Error in metrics_query: {e}")
        raise
