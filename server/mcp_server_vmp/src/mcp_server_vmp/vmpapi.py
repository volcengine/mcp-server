import logging
import os
from dataclasses import dataclass
from multiprocessing.pool import ThreadPool
from re import Match
from typing import List, Optional

from requests.auth import CONTENT_TYPE_FORM_URLENCODED
import volcenginesdkcore
from volcenginesdkcore.interceptor import RuntimeOption

from volcenginesdkvmp.api.vmp_api import VMPApi
from volcenginesdkvmp.models import UpdateWorkspaceRequest, UpdateWorkspaceResponse, DeleteWorkspaceRequest, DeleteWorkspaceResponse, ListWorkspaceInstanceTypesRequest, ListWorkspaceInstanceTypesResponse, CreateWorkspaceRequest, CreateWorkspaceResponse, FiltersForListWorkspaceInstanceTypesInput

import mcp_server_vmp.config as config
import mcp_server_vmp.models as models
import mcp_server_vmp.utils as utils
import mcp_server_vmp.sign as sign


SERVICE_CODE = "vmp"
SERVICE_VERSION = "2021-03-03"
CONTENT_TYPE = "application/json"
CONTENT_TYPE_FORM_URLENCODED = "application/x-www-form-urlencoded"

logger = logging.getLogger("vmpapi")

@dataclass
class Workspace:
    id : str
    name : str
    description : str

class VMPApiClient:
    """VMP API Client."""

    conf : config.VMPConfig
    client : volcenginesdkcore.UniversalApi
    vmpApiClient : VMPApi

    def __init__(self, conf: config.VMPConfig) -> None:
        self.conf = conf
        client = volcenginesdkcore.ApiClient(configuration=conf.to_volc_configuration())
        client._pool = ThreadPool(conf.pool_concurrency) # resize the thread pool to allow more concurrent requests
        self.client = utils.UniversalApi(client)
        self.vmpApiClient = VMPApi(client)
    
    def _get_vmp_volc_client(self, dynamicConf: config.VMPConfig) -> VMPApi:
        return VMPApi(volcenginesdkcore.ApiClient(configuration=dynamicConf.to_volc_configuration()))

    async def list_workspaces(self, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """List workspaces."""
        resp = await self.client.do_call_async(
            volcenginesdkcore.UniversalInfo(
                method="POST", 
                service=SERVICE_CODE, 
                version=SERVICE_VERSION,
                action="ListWorkspaces",
                content_type=CONTENT_TYPE,
            ),
            models.ListWorkspacesRequest().with_runtime_option(dynamicConf.to_runtime_option()),
        )
        return resp

    async def create_workspace(self, args: dict, dynamicConf: config.VMPConfig = None) -> CreateWorkspaceResponse:
        """create workspace."""
        client = self.vmpApiClient
        if dynamicConf is not None:
            client = self._get_vmp_volc_client(dynamicConf)
        resp = client.create_workspace(CreateWorkspaceRequest(**args))
        return resp

    async def update_workspace(self, args: dict, dynamicConf: config.VMPConfig = None) -> UpdateWorkspaceResponse:
        """update workspace."""
        client = self.vmpApiClient
        if dynamicConf is not None:
            client = self._get_vmp_volc_client(dynamicConf)
        resp = client.update_workspace(UpdateWorkspaceRequest(**args))
        return resp

    async def delete_workspace(self, workspaceId: str, dynamicConf: config.VMPConfig = None) -> DeleteWorkspaceResponse:
        """delete workspace."""
        client = self.vmpApiClient
        if dynamicConf is not None:
            client = self._get_vmp_volc_client(dynamicConf)
        resp = client.delete_workspace(DeleteWorkspaceRequest(
            id=workspaceId,
        ))
        return resp

    async def list_workspace_instance_types(self, dynamicConf: config.VMPConfig = None, instanceTypeId: Optional[str] = None) -> ListWorkspaceInstanceTypesResponse:
        """list workspace instance types."""
        client = self.vmpApiClient
        if dynamicConf is not None:
            client = self._get_vmp_volc_client(dynamicConf)
        
        resp = client.list_workspace_instance_types(ListWorkspaceInstanceTypesRequest(
            page_number= 1,
            page_size=100,
            filters=FiltersForListWorkspaceInstanceTypesInput(
                ids=[instanceTypeId] if instanceTypeId is not None else None,
            ),
        ))
        return resp

    async def query_instant_metrics(self, workspaceId: str, query: str, time: str = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """instant query metrics."""
        request_params = {
            'query': query,
        }
        if time is not None:
            request_params['time'] = time

        resp = sign.sign_and_request(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="QueryMetrics",
                content_type=CONTENT_TYPE_FORM_URLENCODED,
            ),
            models.Credentials(
                access_key_id=dynamicConf.volcengine_ak,
                secret_access_key=dynamicConf.volcengine_sk,
                session_token=dynamicConf.session_token,
                region=dynamicConf.volcengine_region,
                service=SERVICE_CODE,
            ),
            host=dynamicConf.volcengine_endpoint,
            query={
                'workspace': workspaceId,
            },
            header={
                "Content-Type": CONTENT_TYPE_FORM_URLENCODED,
            },
            body=models.QueryInstantMetricsRequest(
                query=query,
                time=time,
            ),
        )
        return resp
    
    async def query_range_metrics(self, workspaceId: str, query: str, start: str, end: str, 
        step: Optional[str] = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """range query metrics."""
        # Auto-calculate step if not provided
        if step is None:
            step = self._calculate_default_step(start, end)
            logger.info(f"Auto-calculated step: {step}")
        
        resp = sign.sign_and_request(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="QueryMetricsRange",
                content_type=CONTENT_TYPE,
            ),models.Credentials(
                access_key_id=dynamicConf.volcengine_ak,
                secret_access_key=dynamicConf.volcengine_sk,
                session_token=dynamicConf.session_token,
                region=dynamicConf.volcengine_region,
                service=SERVICE_CODE,
            ),
            host=dynamicConf.volcengine_endpoint,
            query={
                'workspace': workspaceId,
            },
            header={
                "Content-Type": CONTENT_TYPE_FORM_URLENCODED,
            },
            body=models.QueryRangeMetricsRequest(
                workspace=workspaceId,
                query= query,
                start=start,
                end=end,
                step=step,
            ),
        )
        return resp

    async def query_label_values(self, workspaceId: str, label: str, start: Optional[str] = None, end: Optional[str] = None, 
        match: Optional[List[str]] = None, limit: Optional[int] = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """label values."""
        resp = sign.sign_and_request(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="GetLabelValues",
                content_type=CONTENT_TYPE,
            ),models.Credentials(
                access_key_id=dynamicConf.volcengine_ak,
                secret_access_key=dynamicConf.volcengine_sk,
                session_token=dynamicConf.session_token,
                region=dynamicConf.volcengine_region,
                service=SERVICE_CODE,
            ),
            host=dynamicConf.volcengine_endpoint,
            query={
                'workspace': workspaceId,
                'label': label,
            },
            header={
                "Content-Type": CONTENT_TYPE_FORM_URLENCODED,
            },
            body=models.GetLabelValuesRequest(
                workspace=workspaceId,
                label=label,
                start=start,
                end=end,
                matches=match,
                limit=limit,
            ), 
        )
        return resp

    async def query_label_names(self, workspaceId: str, start: Optional[str] = None, end: Optional[str] = None, 
        match: Optional[List[str]] = None, limit: Optional[int] = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """label names."""
        resp = sign.sign_and_request(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="GetLabels",
                content_type=CONTENT_TYPE,
            ),models.Credentials(
                access_key_id=dynamicConf.volcengine_ak,
                secret_access_key=dynamicConf.volcengine_sk,
                session_token=dynamicConf.session_token,
                region=dynamicConf.volcengine_region,
                service=SERVICE_CODE,
            ),
            host=dynamicConf.volcengine_endpoint,
            query={
                'workspace': workspaceId,
            },
            header={
                "Content-Type": CONTENT_TYPE_FORM_URLENCODED,
            },
            body=models.GetLabelsRequest(
                workspace=workspaceId,
                start=start,
                end=end,
                matches=match,
                limit=limit,
            ),
        )
        return resp

    async def query_series(self, workspaceId: str, match: Optional[List[str]] = None, start: Optional[str] = None, end: Optional[str] = None, 
        dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """series."""
        resp = sign.sign_and_request(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="GetSeries",
                content_type=CONTENT_TYPE,
            ),models.Credentials(
                access_key_id=dynamicConf.volcengine_ak,
                secret_access_key=dynamicConf.volcengine_sk,
                session_token=dynamicConf.session_token,
                region=dynamicConf.volcengine_region,
                service=SERVICE_CODE,
            ),
            host=dynamicConf.volcengine_endpoint,
            query={
                'workspace': workspaceId,
            },
            header={
                "Content-Type": CONTENT_TYPE_FORM_URLENCODED,
            },
            body=models.GetSeriesRequest(   
                workspace=workspaceId,
                matches=match,
                start=start,
                end=end,
            ),
        )
        return resp

    def _parse_timestamp(self, time_str: str) -> float:
        """Parse RFC3339 or Unix timestamp string to seconds since epoch.
        Uses Python's dateutil library for better RFC3339 compatibility.
        """
        import datetime
        try:
            # First try Unix timestamp
            if time_str.isdigit():
                return float(time_str)
            
            try:
                # Try dateutil parser for comprehensive RFC3339 support
                from dateutil import parser
                dt = parser.parse(time_str)
                # Ensure we have timezone information
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=datetime.timezone.utc)
                return dt.timestamp()
            except ImportError:
                # Fallback to standard library with enhanced RFC3339 support
                # Handle 'Z' timezone suffix
                time_str = time_str.replace('Z', '+00:00')
                
                # Handle most RFC3339 formats with fromisoformat (Python 3.7+)
                try:
                    dt = datetime.datetime.fromisoformat(time_str)
                    # Ensure timezone info exists
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=datetime.timezone.utc)
                    return dt.timestamp()
                except ValueError:
                    # Last resort: handle common timezone format without colon
                    if '+' in time_str and ':' not in time_str.split('+')[-1]:
                        # Format like '2023-01-01T12:00:00+0800'
                        parts = time_str.split('+')
                        time_str = f"{parts[0]}+{parts[1][:2]}:{parts[1][2:]}"
                        dt = datetime.datetime.fromisoformat(time_str)
                        return dt.timestamp()
                    raise
                    
        except (ValueError, TypeError) as e:
            logger.error(f"Failed to parse timestamp {time_str}: {str(e)}")
            raise ValueError(f"Invalid timestamp format: {time_str}")
    
    def _calculate_default_step(self, start: str, end: str) -> str:
        """Calculate default step as (end - start)/100, minimum 5s.
        Returns integer duration format compatible with API requirements.
        """
        try:
            start_time = self._parse_timestamp(start)
            end_time = self._parse_timestamp(end)
            
            # Calculate duration in seconds
            duration_seconds = end_time - start_time
            if duration_seconds <= 0:
                logger.warning(f"Invalid time range: start ({start}) >= end ({end})")
                return "5"
            
            # Calculate step as duration/100
            step_seconds = int(duration_seconds / 100)
            
            # Ensure minimum 5 seconds
            step_seconds = max(step_seconds, 5)
            
            return f"{int(round(step_seconds))}"
        except Exception as e:
            logger.error(f"Failed to calculate default step: {str(e)}")
            return "5"  # Fallback to 5s on error


