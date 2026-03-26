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
mcp = None


def init_server(
    name: str = None,
    port: int = None,
    host: str = None,
    streamable_http_path: str = None
):
    """Initialize the FastMCP server with custom configuration and register tools."""
    global mcp
    
    if mcp is None:
        mcp = FastMCP(
            name or os.getenv("MCP_SERVER_NAME", "mcp_server_metrics"),
            port=port or int(os.getenv("MCP_SERVER_PORT", "8000")),
            host=host or os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
            streamable_http_path=streamable_http_path or os.getenv("STREAMABLE_HTTP_PATH", "/mcp")
        )
        
        # Register all tools after server initialization
        register_tools(mcp)
    
    return mcp


def register_tools(server: FastMCP):
    """Register all tools with the given FastMCP server instance."""
    
    def init_auth_config() -> MetricsConfig:
        """Initialize auth config from env or request context."""
        conf = load_config()  # load default config from env
    
        # Get context from request if available
        try:
            ctx: Context = server.get_context()
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
    
    @server.tool()
    async def list_workspace(
        PageNumber: int = 1,
        PageSize: int = 10,
        Name: str = "",
        ProjectName: str = "default",
        ListGlobal: bool = False,
        Region: Optional[str] = None,
    ):
        """
        List workspaces from the metrics console.

        Args:
            PageNumber: Page number for pagination (default: 1)
            PageSize: Page size for pagination (default: 10)
            Filters: Filters to apply (optional, Filters only support filtering by "Name" parameter for workspace names.)
            ProjectName: Project name (default: "default")
            ListGlobal: Whether to list global workspaces (default: False)
            Region: Volcengine region (optional, defaults to VOLCENGINE_REGION environment variable if not provided)

        Returns:
            List of workspaces with metadata
        """
        try:
            if PageNumber < 1:
                raise ValueError("PageNumber must be at least 1")
            if PageSize < 1 or PageSize > 100:
                raise ValueError("PageSize must be between 1 and 100")

            req = ListWorkspaceRequest(
                PageNumber=PageNumber,
                PageSize=PageSize,
                Filters={"Name": Name} if Name else None,
                ProjectName=ProjectName,
                ListGlobal=ListGlobal,
                Region=Region,
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

    @server.tool()
    async def get_workspace(
        WorkspaceID: str,
        Region: Optional[str] = None,
    ):
        """
        Get workspace information from the metrics console.

        Args:
            WorkspaceID: Workspace ID
            Region: Volcengine region (optional, defaults to VOLCENGINE_REGION environment variable if not provided)

        Returns:
            Workspace information
        """
        try:
            req = GetWorkspaceInfoRequest(
                WorkspaceID=WorkspaceID,
                Region=Region,
            )

            config = init_auth_config()
            api = MetricsApi(config)
            return api.get_workspace_info(req)
        except Exception as e:
            logger.error(f"Error in get_workspace: {e}")
            raise

    @server.tool()
    async def list_query_clusters(
        PageNumber: int = 1,
        PageSize: int = 10,
        Name: str = "",
        ProjectName: str = "default",
        Region: Optional[str] = None,
    ):
        """
        List query clusters from the metrics console.

        Args:
            PageNumber: Page number for pagination (default: 1)
            PageSize: Page size for pagination (default: 10)
            Name: Cluster name to filter (optional)
            ProjectName: Project name (default: "default")
            Region: Volcengine region (optional, defaults to VOLCENGINE_REGION environment variable if not provided)

        Returns:
            List of query clusters with metadata
        """
        try:
            if PageNumber < 1:
                raise ValueError("PageNumber must be at least 1")
            if PageSize < 1 or PageSize > 100:
                raise ValueError("PageSize must be between 1 and 100")

            req = ListQueryClustersRequest(
                PageNumber=PageNumber,
                PageSize=PageSize,
                Name=Name,
                ProjectName=ProjectName,
                Region=Region,
            )

            config = init_auth_config()
            api = MetricsApi(config)
            return api.list_query_clusters(req)
        except Exception as e:
            logger.error(f"Error in list_query_clusters: {e}")
            raise

    @server.tool()
    async def get_query_cluster(
        ClusterID: str,
        Region: Optional[str] = None,
    ):
        """
        Get query cluster information from the metrics console.

        Args:
            ClusterID: Query cluster ID
            Region: Volcengine region (optional, defaults to VOLCENGINE_REGION environment variable if not provided)

        Returns:
            Query cluster information
        """
        try:
            req = GetQueryClusterRequest(
                ClusterID=ClusterID,
                Region=Region,
            )

            config = init_auth_config()
            api = MetricsApi(config)
            return api.get_query_cluster(req)
        except Exception as e:
            logger.error(f"Error in get_query_cluster: {e}")
            raise

    @server.tool()
    async def list_preagg(
        WorkspaceName: str = "",
        PageNumber: int = 1,
        PageSize: int = 10,
        onlyShowMine: bool = True,
        Region: Optional[str] = None,
    ):
        """
        List preaggregation rules from the metrics console.

        Args:
            WorkspaceName: Workspace name to filter (required, defaults to METRICS_WORKSPACE_NAME environment variable if not provided)
            PageNumber: Page number for pagination (default: 1)
            PageSize: Page size for pagination (default: 10)
            onlyShowMine: Whether to only show rules created by current user (default: True)
            Region: Volcengine region (optional, defaults to VOLCENGINE_REGION environment variable if not provided)

        Returns:
            List of preaggregation rules with metadata
        """
        try:
            if PageNumber < 1:
                raise ValueError("PageNumber must be at least 1")
            if PageSize < 1 or PageSize > 100:
                raise ValueError("PageSize must be between 1 and 100")

            config = init_auth_config()
            
            final_workspace_name = WorkspaceName or config.workspace_name
            if not final_workspace_name:
                raise ValueError("WorkspaceName is required. Please provide it as a parameter or set METRICS_WORKSPACE_NAME environment variable")

            req = ListPreaggRequest(
                WorkspaceName=final_workspace_name,
                PageNumber=PageNumber,
                PageSize=PageSize,
                onlyShowMine=onlyShowMine,
                Region=Region,
            )

            api = MetricsApi(config)
            return api.list_preagg(req)
        except Exception as e:
            logger.error(f"Error in list_preagg: {e}")
            raise

    @server.tool()
    async def influx_query(
        Queries: List[str],
        Workspace: str = "",
        Epoch: Optional[str] = None,
        Region: Optional[str] = None,
    ):
        """
        InfluxDB query from cross cluster proxy.

        Args:
            Queries: List of InfluxQL query strings
            Workspace: Workspace name (defaults to METRICS_WORKSPACE_NAME environment variable if not provided)
            Epoch: Time stamp precision (s/ms/us/ns, optional)
            Region: Volcengine region (optional, defaults to VOLCENGINE_REGION environment variable if not provided)

        Returns:
            Query results
        """
        try:
            config = init_auth_config()
            
            final_workspace = Workspace or config.workspace_name
            if not final_workspace:
                raise ValueError("Workspace is required. Please provide it as a parameter or set METRICS_WORKSPACE_NAME environment variable")

            req = InfluxQueryRequest(
                Workspace=final_workspace,
                Queries=Queries,
                Epoch=Epoch,
                Region=Region,
            )

            api = MetricsApi(config)
            return api.influx_query(req)
        except Exception as e:
            logger.error(f"Error in influx_query: {e}")
            raise

    @server.tool()
    async def metrics_query(
        Queries: List[Dict[str, Any]],
        Workspace: str = "",
        Start: str = "10m-ago",
        End: str= "now",
        Region: Optional[str] = None,
    ):
        """
        Query metrics data from cross cluster proxy.

        Args:
            Queries: List of query objects with metric details
            Workspace: Workspace name (defaults to METRICS_WORKSPACE_NAME environment variable if not provided)
            Start: Start time in seconds (timestamp string)
            End: End time in seconds (timestamp string)
            Region: Volcengine region (optional, defaults to VOLCENGINE_REGION environment variable if not provided)

        Returns:
            Metrics query results
        """
        try:
            config = init_auth_config()
            
            final_workspace = Workspace or config.workspace_name
            if not final_workspace:
                raise ValueError("Workspace is required. Please provide it as a parameter or set METRICS_WORKSPACE_NAME environment variable")

            req = MetricsQueryRequest(
                Workspace=final_workspace,
                Queries=Queries,
                Start=Start,
                End=End,
                Region=Region,
            )

            api = MetricsApi(config)
            return api.metrics_query(req)
        except Exception as e:
            logger.error(f"Error in metrics_query: {e}")
            raise
