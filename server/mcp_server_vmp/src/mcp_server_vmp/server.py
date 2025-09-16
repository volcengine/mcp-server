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
vmpApiClient : vmpapi.VMPApi = None

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
    vmpApiClient = vmpapi.VMPApi(conf)

    args = parser.parse_args()
    logger.info(f"Starting Volcengine Managed Prometheus Server with {args.transport} transport")
    mcp.run(transport=args.transport)

if __name__ == "__main__":
    main()