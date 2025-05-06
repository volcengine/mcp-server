import logging
from dataclasses import dataclass
from re import Match
from typing import List, Optional

import volcenginesdkcore
from volcenginesdkcore.interceptor import RuntimeOption

import mcp_server_vmp.config as config
import mcp_server_vmp.models as models
import mcp_server_vmp.utils as utils

SERVICE_CODE = "vmp"
SERVICE_VERSION = "2021-03-03"
CONTENT_TYPE = "application/json"


logger = logging.getLogger("vmpapi")

@dataclass
class Workspace:
    id : str
    name : str
    description : str

class VMPApi:
    """VMP API."""

    conf : config.VMPConfig
    client : volcenginesdkcore.UniversalApi

    def __init__(self, conf: config.VMPConfig) -> None:
        self.conf = conf
        self.client = utils.UniversalApi(volcenginesdkcore.ApiClient(configuration=conf.to_volc_configuration()))

    def list_workspaces(self, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """List workspaces."""
        resp = self.client.do_call(
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

    def query_instant_metrics(self, workspaceId: str, query: str, time: str = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """instant query metrics."""
        resp = self.client.do_call(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="QueryInstant",
                content_type=CONTENT_TYPE,
            ),
            models.QueryInstantMetricsRequest(
                WorkspaceId=workspaceId,
                Expression=query,
                Time=time,
            ).with_runtime_option(dynamicConf.to_runtime_option()),
        )
        return resp

    def query_range_metrics(self, workspaceId: str, query: str, start: str, end: str, 
        step: Optional[str] = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """range query metrics."""
        resp = self.client.do_call(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="QueryRange",
                content_type=CONTENT_TYPE,
            ),
            models.QueryRangeMetricsRequest(
                WorkspaceId=workspaceId,
                Expression= query,
                Start=start,
                End=end,
                Step=step,
            ).with_runtime_option(dynamicConf.to_runtime_option()),
        )
        return resp

    def query_label_values(self, workspaceId: str, label: str, start: Optional[str] = None, end: Optional[str] = None, 
        match: Optional[List[str]] = None, limit: Optional[int] = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """label values."""
        resp = self.client.do_call(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="QueryLabelValues",
                content_type=CONTENT_TYPE,
            ),
            models.QueryLabelValuesRequest(
                WorkspaceId=workspaceId,
                Label=label,
                Start=start,
                End=end,
                Match=match,
                Limit=limit,
            ).with_runtime_option(dynamicConf.to_runtime_option()), 
        )
        return resp

    def query_label_names(self, workspaceId: str, start: Optional[str] = None, end: Optional[str] = None, 
        match: Optional[List[str]] = None, limit: Optional[int] = None, dynamicConf: config.VMPConfig = None) -> dict[str, any] | None:
        """label names."""
        resp = self.client.do_call(
            volcenginesdkcore.UniversalInfo(
                method="POST",
                service=SERVICE_CODE,
                version=SERVICE_VERSION,
                action="QueryLabels",
                content_type=CONTENT_TYPE,
            ),
            models.QueryLabelNamesRequest(
                WorkspaceId=workspaceId,
                Start=start,
                End=end,
                Match=match,
                Limit=limit,
            ).with_runtime_option(dynamicConf.to_runtime_option()),
        )
        return resp


