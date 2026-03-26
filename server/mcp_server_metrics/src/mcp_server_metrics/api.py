import logging
import requests
import json
from typing import Any, Dict

from mcp_server_metrics.config import MetricsConfig
from mcp_server_metrics.model import *

logger = logging.getLogger(__name__)

# Service name for signing
METRICS_SERVICE_NAME = "metrics"


class MetricsApi:
    """API client for Volcengine Metrics."""

    def __init__(self, config: MetricsConfig):
        self.config = config

    def _make_request(
        self,
        method: str,
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        region: str = None,
    ) -> Dict[str, Any]:
        """Make a request to the Metrics API with appropriate signing."""
        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

        query = params or {}
        body = json.dumps(data) if data else ""
        post_params = {}

        # Use request-specific region if provided, otherwise config default
        target_region = region or self.config.region

        # Sign the request - path is empty for root URL
        self.config.append_authorization(
            "/",
            method,
            headers,
            body,
            post_params,
            query,
            target_region,
            METRICS_SERVICE_NAME,
        )

        # Get endpoint based on target region
        url = self.config.get_endpoint(target_region)

        logger.debug(f"Making {method} request to {url} with params={params}")

        try:
            response = requests.request(
                method,
                url,
                params=params,
                data=body,
                headers=headers,
                timeout=30,
            )

            # Detailed error logging
            if response.status_code != 200:
                logger.error(f"API Error {response.status_code}: {response.text}")
                logger.error(f"Request URL: {response.url}")
                logger.error(f"Request Headers: {dict(response.request.headers)}")
                logger.error(f"Request Body: {response.request.body}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error {e.response.status_code}: {e.response.text}")
            logger.error(f"Request URL: {e.response.url}")
            logger.error(f"Request Headers: {dict(e.response.request.headers)}")
            logger.error(f"Request Body: {e.response.request.body}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {e}")
            raise

    def list_workspaces(self, request: ListWorkspaceRequest) -> ListWorkspaceResponse:
        """List workspaces from metrics."""
        params = {
            "Action": "ListWorkspace",
            "Version": "2024-06-29",
        }
        
        data = {
            "PageNumber": request.PageNumber,
            "PageSize": request.PageSize,
            "Filters": request.Filters,
            "ProjectName": request.ProjectName,
            "ListGlobal": request.ListGlobal,
        }
     
        logger.debug(f"Calling list_workspaces with params: {params}, data: {data}")
        response = self._make_request("POST", params=params, data=data, region=request.Region)
        return ListWorkspaceResponse(**response)

    def get_workspace_info(self, request: GetWorkspaceInfoRequest) -> GetWorkspaceInfoResponse:
        """Get workspace information from metrics."""
        params = {
            "Action": "GetWorkspaceInfo",
            "Version": "2024-06-29",
        }
        
        data = {
            "WorkspaceId": request.WorkspaceID,
        }

        logger.debug(f"Calling get_workspace_info with params: {params}, data: {data}")
        response = self._make_request("POST", params=params, data=data, region=request.Region)
        return GetWorkspaceInfoResponse(**response)

    def list_query_clusters(self, request: ListQueryClustersRequest) -> ListQueryClustersResponse:
        """List query clusters from metrics."""
        params = {
            "Action": "ListQueryClusters",
            "Version": "2024-06-29",
        }
        
        data = {
            "Page": {
                "PageNumber": request.PageNumber,
                "PageSize": request.PageSize,
            },
            "Name": request.Name.strip() if request.Name else None,
            "ProjectName": request.ProjectName,
        }

        logger.debug(f"Calling list_query_clusters with params: {params}, data: {data}")
        response = self._make_request("POST", params=params, data=data, region=request.Region)
        return ListQueryClustersResponse(**response)

    def get_query_cluster(self, request: GetQueryClusterRequest) -> GetQueryClusterResponse:
        """Get query cluster information from metrics."""
        params = {
            "Action": "GetQueryCluster",
            "Version": "2024-06-29",
        }
        
        data = {
            "Id": request.ClusterID,
        }

        logger.debug(f"Calling get_query_cluster with params: {params}, data: {data}")
        response = self._make_request("POST", params=params, data=data, region=request.Region)
        return GetQueryClusterResponse(**response)

    def list_preagg(self, request: ListPreaggRequest) -> ListPreaggResponse:
        """List preaggregation rules from metrics."""
        params = {
            "Action": "ListPreagg",
            "Version": "2024-06-29",
        }
        
        data = {
            "PageNumber": request.PageNumber,
            "PageSize": request.PageSize,
            "onlyShowMine": request.onlyShowMine,
        }
        
        if request.WorkspaceName:
            data["Filters"] = {"WorkspaceName": request.WorkspaceName}

        logger.debug(f"Calling list_preagg with params: {params}, data: {data}")
        response = self._make_request("POST", params=params, data=data, region=request.Region)
        return ListPreaggResponse(**response)

    def influx_query(self, request: InfluxQueryRequest) -> InfluxQueryResponse:
        """InfluxDB query from metrics."""
        params = {
            "Action": "InfluxQuery",
            "Version": "2024-06-29",
        }
        
        data = {
            "Workspace": request.Workspace,
            "Queries": request.Queries,
        }
        
        if request.Epoch:
            data["Epoch"] = request.Epoch

        logger.debug(f"Calling influx_query with params: {params}, data: {data}")
        response = self._make_request("POST", params=params, data=data, region=request.Region)
        return InfluxQueryResponse(**response)

    def metrics_query(self, request: MetricsQueryRequest) -> MetricsQueryResponse:
        """Query metrics data from metrics."""
        params = {
            "Action": "MetricsQuery",
            "Version": "2024-06-29",
        }
        
        data = {
            "Workspace": request.Workspace,
            "Queries": request.Queries,
            "Start": request.Start,
            "End": request.End,
        }

        logger.debug(f"Calling metrics_query with params: {params}, data: {data}")
        response = self._make_request("POST", params=params, data=data, region=request.Region)
        return MetricsQueryResponse(**response)
