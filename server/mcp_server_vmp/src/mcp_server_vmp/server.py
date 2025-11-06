import argparse
import base64
import json
import logging
import os
from typing import Optional

import volcenginesdkcore
from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.fastmcp.resources import HttpResource
from mcp.server.session import ServerSession
from starlette.requests import Request

import mcp_server_vmp.config as config
import mcp_server_vmp.vmpapi as vmpapi

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(os.getenv(config.ENV_MCP_SERVER_NAME, "mcp_server_vmp"), host=os.getenv(config.ENV_MCP_SERVER_HOST, "0.0.0.0"), port=int(os.getenv(config.ENV_MCP_SERVER_PORT, "8000")))
vmpApiClient : vmpapi.VMPApiClient = None

@mcp.tool()
async def list_workspaces(region: str = "cn-beijing"):
    """list volcengine managed prometheus(VMP) workspaces in specific region.

    Args:
        region: target region

    Returns:
        A list of prometheus workspaces
    """
    conf = init_auth_config(region)
    return await vmpApiClient.list_workspaces(conf)

@mcp.tool()
async def list_workspace_instance_types(region: str = "cn-beijing", instanceTypeId: Optional[str] = None):
    """list volcengine managed prometheus(VMP) workspace instance types.

    Args:
        instanceTypeId: target prometheus instance type id
        region: target region

    Returns:
        A list of prometheus instance types
    """
    conf = init_auth_config(region)

    return await vmpApiClient.list_workspace_instance_types(conf, instanceTypeId=instanceTypeId)

@mcp.tool()
async def create_workspace(region: str = "cn-beijing",
        delete_protection_enabled: bool = True,
        description: Optional[str] = None,
        instance_type_id: str = "vmp.standard.15d",
        name: str = "default",
        password: Optional[str] = None,
        project_name: Optional[str] = None,
        public_access_enabled: bool = False,
        username: Optional[str] = None,
):
    """create volcengine managed prometheus(VMP) workspace in specific region.

    Args:
        delete_protection_enabled: enable delete protection for workspace,
        description: workspace description
        instance_type_id: workspace instance type id
        name: workspace name
        password: workspace basic auth password
        project_name: workspace project name
        public_access_enabled: enable public access for workspace
        username: workspace basic auth username

    Returns:
        A list of prometheus workspaces
    """
    conf = init_auth_config(region)
    req = {
        "delete_protection_enabled": delete_protection_enabled,
        "description": description,
        "instance_type_id": instance_type_id,
        "name": name,
        "password": password,
        "project_name": project_name,
        "public_access_enabled": public_access_enabled,
        "username": username
    }
    req = {k: v for k, v in req.items() if v is not None}
    return await vmpApiClient.create_workspace(req, conf)

@mcp.tool()
async def delete_workspace(workspaceId: str, region: str = "cn-beijing"):
    """delete volcengine managed prometheus(VMP) workspace in specific region.

    Args:
        workspaceId: target prometheus workspace id
        region: target region

    Returns:
        Prometheus workspaceID
    """
    conf = init_auth_config(region)
    return await vmpApiClient.delete_workspace(workspaceId, conf)

@mcp.tool()
async def update_workspace(region: str = "cn-beijing",
        workspaceId: str = None,
        delete_protection_enabled: Optional[bool] = None,
        description: Optional[str] = None,
        name: Optional[str] = None,
        password: Optional[str] = None,
        public_access_enabled: Optional[bool] = None,
        search_latency_offset: Optional[str] = None,
        username: Optional[str] = None,
        active_series: Optional[int] = None,
        ingest_samples_per_second: Optional[int] = None,
        public_query_bandwidth: Optional[int] = None,
        public_write_bandwidth: Optional[int] = None,
        query_per_second: Optional[int] = None,
        scan_samples_per_second: Optional[int] = None,
        scan_series_per_second: Optional[int] = None
        ):
    """update volcengine managed prometheus(VMP) workspace in specific region.

    Args:
        WorkspaceId: target prometheus workspace id
        region: target region
        delete_protection_enabled: enable delete protection for workspace,
        description: workspace description
        name: workspace name
        password: workspace password
        public_access_enabled: enable public access for workspace
        search_latency_offset: search latency offset for workspace
        username: workspace username
        active_series: active series quota for workspace
        ingest_samples_per_second: ingest samples per second quota for workspace
        public_query_bandwidth: public query bandwidth quota for workspace
        public_write_bandwidth: public write bandwidth quota for workspace
        query_per_second: query per second quota for workspace
        scan_samples_per_second: scan samples per second quota for workspace
        scan_series_per_second: scan series per second quota for workspace
    Returns:
        Prometheus workspaceID
    """
    init_auth_config(region)
    req = {
        "id": workspaceId,
        "delete_protection_enabled": delete_protection_enabled,
        "description": description,
        "name": name,
        "password": password,
        "public_access_enabled": public_access_enabled,
        "quota": {
            "active_series": active_series,
            "ingest_samples_per_second": ingest_samples_per_second,
            "public_query_bandwidth": public_query_bandwidth,
            "public_write_bandwidth": public_write_bandwidth,
            "query_per_second": query_per_second,
            "scan_samples_per_second": scan_samples_per_second,
            "scan_series_per_second": scan_series_per_second
        },
        "search_latency_offset": search_latency_offset,
        "username": username
    }
    filtered_req = {k: v for k, v in req.items() if v is not None}
    if "quota" in filtered_req and isinstance(filtered_req["quota"], dict):
        filtered_req["quota"] = {k: v for k, v in filtered_req["quota"].items() if v is not None}
        if not filtered_req["quota"]:
            del filtered_req["quota"]
    req = filtered_req
    conf = init_auth_config(region)
    return await vmpApiClient.update_workspace(req, conf)

@mcp.tool()
async def query_metrics(workspaceId: str, query: str, time: Optional[str] = None, region: str = "cn-beijing"):
    """Execute an instant query against specific volcengine managed prometheus(VMP) workspace.
    
    Args:
        workspaceId: target prometheus workspace id
        query: prometheus query expression in PromQL format
        time: Optional RFC3339 or Unix timestamp (default: current time)
        region: target region

    Returns:
        Query result with type (vector, matrix, scalar, string) and values
    """
    conf = init_auth_config(region)
    return await vmpApiClient.query_instant_metrics(workspaceId, query, time, conf)

@mcp.tool()
async def query_range_metrics(workspaceId: str, query: str, start: str, end: str, step: Optional[str] = None, region: str = "cn-beijing"):
    """Execute a range query against specific volcengine managed prometheus(VMP) workspace.
    
    Args:
        workspaceId: target prometheus workspace id
        query: prometheus query expression in PromQL format
        start: RFC3339 or Unix timestamp
        end: RFC3339 or Unix timestamp
        step: query resolution step width in duration format (e.g., '15s', '1m', '1h')
        region: target region
    
    Returns:
        Range query result with type (usually matrix) and values over time
    """
    conf = init_auth_config(region)
    return await vmpApiClient.query_range_metrics(workspaceId, query, start, end, step, conf)

@mcp.tool()
async def query_metric_names(workspaceId: str, match: Optional[str] = None, region: str = "cn-beijing"):
    """List all metric names in specific volcengine managed prometheus(VMP) workspace.

    Args:
        workspaceId: target prometheus workspace id
        match: series selector that selects the series from which to read the metric names (e.g. 'up{job="node"}')
        region: target region

    Returns:
        A list of metric names
    """
    conf = init_auth_config(region)
    return await vmpApiClient.query_label_values(workspaceId, "__name__", match=[match], dynamicConf=conf)

@mcp.tool()
async def query_metric_labels(workspaceId: str, metricName: str, region: str = "cn-beijing"):
    """List all labels of specific metric in volcengine managed prometheus(VMP) workspace.
    Args:
        workspaceId: target prometheus workspace id
        metricName: target metric name
        region: target region
    Returns:
        A list of metric labels
    """
    conf = init_auth_config(region)
    return await vmpApiClient.query_label_names(workspaceId, match=[metricName], dynamicConf=conf)

@mcp.tool()
async def query_series(workspaceId: str, match: str, start: Optional[str] = None, end: Optional[str] = None, region: str = "cn-beijing"):
    """List all series in specific volcengine managed prometheus(VMP) workspace that match the given series selector.

    Args:
        workspaceId: target prometheus workspace id
        match: series selector that selects the series to return (e.g. 'up{job="node"}')
        start: Optional RFC3339 or Unix timestamp (default: current time)
        end: Optional RFC3339 or Unix timestamp (default: current time)
        region: target region

    Returns:
        A list of series
    """
    conf = init_auth_config(region)
    return await vmpApiClient.query_series(workspaceId, match, start, end, dynamicConf=conf)

mcp.add_resource(HttpResource(
    uri="resource://vmp/metrics/dcgm",
    name="DCGM 常见指标",
    description="NVIDIA DCGM 是用于管理和监控基于 Linux 系统的 NVIDIA GPU 大规模集群的一体化工具。本文介绍 DCGM 常见的查询指标。",
    mime_type="text/html",
    url="https://www.volcengine.com/docs/6731/163095"))

mcp.add_resource(HttpResource(
    uri="resource://vmp/metrics/node-exporter",
    name="node-exporter 常见指标",
    description="node-exporter 是 Prometheus 官方提供的 exporter，主要用来采集 Linux 类型节点的相关信息和运行指标，包括主机的 CPU、内存、Load、Filesystem、Network 等。本文为您介绍 node-exporter 常见的指标。",
    mime_type="text/html",
    url="https://www.volcengine.com/docs/6731/177137"))

mcp.add_resource(HttpResource(
    uri="resource://vmp/metrics/kube-state-metrics",
    name="kube-state-metrics 常见指标",
    description="kube-state-metrics 通过监听 Kubernetes API 服务器来生成不同资源的状态的 Metrics 数据。用来获取 Kubernetes 集群中各种资源对象的组件，例如 Deployment、Daemonset、Nodes 和 Pods 等。本文为您介绍 kube-state-metrics 常见的指标。",
    mime_type="text/html",
    url="https://www.volcengine.com/docs/6731/177138"))

mcp.add_resource(HttpResource(
    uri="resource://vmp/metrics/cadvisor",
    name="cAdvisor 常见指标",
    description="cAdvisor 是 Google 开源的容器资源监控和性能分析工具，cAdvisor 对 Node 节点上的资源及容器进行实时监控和性能数据采集，包括 CPU 、内存、网络吞吐量及文件系统等。本文为您介绍 cAdvisor 常见的指标。",
    mime_type="text/html",
    url="https://www.volcengine.com/docs/6731/177139"))

def init_auth_config(region: str) -> config.VMPConfig:
    """Initialize auth config from env or request context."""
    conf = config.load_env_config() # load default config from env
    if region and len(region) > 0:
        conf.volcengine_region = region
        if conf.volcengine_endpoint is None or len(conf.volcengine_endpoint) == 0:
            conf.volcengine_endpoint = get_vmp_service_endpoint_by_region(region)

    # 从 context 中获取 header
    ctx: Context[ServerSession, object] = mcp.get_context()
    raw_request: Request = ctx.request_context.request

    auth = None
    if raw_request:
        # 从 header 的 authorization 字段读取 base64 编码后的 sts json
        auth = raw_request.headers.get("authorization", None)
    if auth is None:
        # 如果 header 中没有认证信息，可能是 stdio 模式，尝试从环境变量获取
        auth = os.getenv("authorization", None)
    if auth is not None:
        if ' ' in auth:
            _, base64_data = auth.split(' ', 1)
        else:
            base64_data = auth

        try:
            # 解码 Base64
            decoded_str = base64.b64decode(base64_data).decode('utf-8')
            data = json.loads(decoded_str)
            # 获取字段
            conf.volcengine_ak = data.get('AccessKeyId')
            conf.volcengine_sk = data.get('SecretAccessKey')
            conf.session_token = data.get('SessionToken')
            return conf
        except Exception as e:
            raise ValueError("Decode authorization info error", e)
    if not conf.is_valid():
        raise ValueError("No valid auth info found")
    return conf

def get_vmp_service_endpoint_by_region(region_id: str = None) -> str:
    return f"vmp.{region_id}.volcengineapi.com"

def main():
    """Start A Volcengine Managed Prometheus server."""
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run the Volcengine Managed Prometheus MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default=os.getenv(config.ENV_MCP_SERVER_MODE, "stdio"),
        help="Transport protocol to use (sse or stdio or streamable-http, default: stdio)",
    )

    # Init the VMP API client using default config
    conf = config.load_env_config()
    volcenginesdkcore.Configuration.set_default(conf.to_volc_configuration())
    global vmpApiClient 
    vmpApiClient = vmpapi.VMPApiClient(conf)

    args = parser.parse_args()
    logger.info(f"Starting Volcengine Managed Prometheus Server with {args.transport} transport")
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()