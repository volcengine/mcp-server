import argparse
import base64
import json
import logging
import os
from typing import Optional

import volcenginesdkcore
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from starlette.requests import Request

from mcp_server_apmplus.api import ApmplusApi, ApmplusConfig, DEFAULT_REGION
from mcp_server_apmplus.config import (
    load_config,
    ENV_MCP_SERVER_PORT,
    ENV_MCP_SERVER_NAME,
    ENV_MCP_SERVER_HOST,
    ENV_MCP_SERVER_MODE,
    ENV_MCP_DEV_MODE,
)
from mcp_server_apmplus.model import *

# Initialize FastMCP server
mcp = FastMCP(
    os.getenv(ENV_MCP_SERVER_NAME, "mcp_server_apmplus"),
    port=int(os.getenv(ENV_MCP_SERVER_PORT, "8000")),
    host=os.getenv(ENV_MCP_SERVER_HOST, "127.0.0.1"),
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global variables
config: Optional[ApmplusConfig] = None


@mcp.tool()
async def apmplus_server_list_alert_rule(
    region: str = "cn-beijing",
    keyword: str = "",
    page_number: int = 1,
    page_size: int = 10,
):
    """
    List alert rules.
    Args:
        region (str, optional): Region ID. Defaults to cn-beijing.
        keyword (str, optional): Search keyword. Defaults to "".
        page_number (int, optional): Page number for pagination. Defaults to 1.
        page_size (int, optional): Page size for pagination. Defaults to 10.
    Returns:
        A list of alert rules.
    """
    try:
        if isinstance(region, str) and not region.strip():
            region = DEFAULT_REGION
        if isinstance(keyword, str) and not keyword.strip():
            keyword = None

        req = ApmplusServerListAlertRuleRequest(
            region=region,
            keyword=keyword,
            page_number=page_number,
            page_size=page_size,
        )

        conf = init_auth_config(region)
        api = ApmplusApi(conf)
        return api.server_list_alert_rule(req)
    except Exception as e:
        logging.error(f"Error in apmplus_server_list_alert_rule: {e}")
        raise


@mcp.tool()
async def apmplus_server_list_notify_group(
    region: str = "cn-beijing",
    keyword: str = "",
    page_number: int = 1,
    page_size: int = 10,
):
    """
    List notify group.
    Args:
        region (str, optional): Region ID. Defaults to cn-beijing.
        keyword (str, optional): Search keyword. Defaults to "".
        page_number (int, optional): Page number for pagination. Defaults to 1.
        page_size (int, optional): Page size for pagination. Defaults to 10.
    Returns:
        A list of notify group.
    """
    try:
        if isinstance(region, str) and not region.strip():
            region = DEFAULT_REGION
        if isinstance(keyword, str) and not keyword.strip():
            keyword = None

        req = ApmplusServerListNotifyGroupRequest(
            region=region,
            keyword=keyword,
            page_number=page_number,
            page_size=page_size,
        )

        conf = init_auth_config(region)
        api = ApmplusApi(conf)
        return api.server_list_notify_group(req)
    except Exception as e:
        logging.error(f"Error in apmplus_server_list_notify_group: {e}")
        raise


@mcp.tool()
async def apmplus_server_query_metrics(
    region: str = "cn-beijing",
    query: str = "",
    start_time: int = None,
    end_time: int = None,
):
    """
    Query metrics.
    Args:
        region (str, optional): Region ID. Defaults to cn-beijing.
        query (str): Metric expression in PromQL format.
        start_time (int): Start time in seconds.
        end_time (int): End time in seconds.
    Returns:
        metrics.
    """
    try:
        if isinstance(region, str) and not region.strip():
            region = DEFAULT_REGION

        req = ApmplusServerQueryMetricsRequest(
            region=region,
            query=query,
            start_time=start_time,
            end_time=end_time,
        )

        conf = init_auth_config(region)
        api = ApmplusApi(conf)
        return api.server_query_metrics(req)
    except Exception as e:
        logging.error(f"Error in apmplus_server_query_metrics: {e}")
        raise


@mcp.tool()
async def apmplus_server_get_trace_detail(
    trace_id: str,
    suggest_time: int,
    region: str = "cn-beijing",
):
    """
    Get trace detail information.
    Args:
        trace_id (str, optional): Trace ID.
        suggest_time (int, optional): Suggest time in seconds.
        region (str, optional): Region ID. Defaults to cn-beijing.
    Returns:
        trace detail information.
    """
    try:
        conf = init_auth_config(region)
        req = {"suggest_time": suggest_time, "trace_id": trace_id}
        api = ApmplusApi(conf)
        return await api.server_get_trace_detail(req, conf)
    except Exception as e:
        logging.error(f"Error in apmplus_server_get_trace_detail: {e}")
        raise


@mcp.tool()
async def apmplus_server_list_span(
    start_time: int,
    end_time: int,
    filters: list[dict] = None,
    order: str = "DESC",
    order_by: str = "",
    offset: int = 0,
    limit: int = 10,
    min_call_cost_millisecond: int = 0,
    max_call_cost_millisecond: int = 0,
    project_name: str = None,
    tag_filters: list[dict] = None,
    region: str = "cn-beijing",
):
    """
    Get a list of trace span.
    Args:
        start_time (int): Start time in seconds, example: 1693536000
        end_time (int): End time in seconds, example: 1693546000
        filters (list[dict], optional): Filter expression.
                                    Each dict contains:
                                    - 'Op' (str): in, not_in
                                    - 'Key' (str): Filter key
                                    - 'Values' (list[str]): Filter values
        order (str, optional): Order direction. Defaults to DESC.
        order_by (str, optional): Order by field. Defaults to "".
        offset (int, optional): Offset for pagination. Defaults to 0.
        limit (int, optional): Limit for pagination. Defaults to 10.
        min_call_cost_millisecond (int, optional): Minimum call cost in milliseconds. Defaults to 0.
        max_call_cost_millisecond (int, optional): Maximum call cost in milliseconds. Defaults to 0.
        project_name (str, optional): The project name.
        tag_filters (list[dict], optional): List of tag filters. Each dict contains:
                                             - 'Key' (str): Tag key
                                             - 'Value' (list[str]): Tag value
                                             Max 10 tag pairs.
                                             Empty value means no restriction on tag value.
        region (str, optional): Region ID. Defaults to cn-beijing.
    Returns:
        A list of span.
    """
    try:
        conf = init_auth_config(region)
        req = {
            "start_time": start_time,
            "end_time": end_time,
            "filters": filters,
            "order": order,
            "order_by": order_by,
            "offset": offset,
            "limit": limit,
            "min_call_cost_millisecond": min_call_cost_millisecond,
            "max_call_cost_millisecond": max_call_cost_millisecond,
            "project_name": project_name,
            "tag_filters": tag_filters,
        }
        api = ApmplusApi(conf)
        return await api.server_list_span(req, conf)
    except Exception as e:
        logging.error(f"Error in apmplus_server_list_span: {e}")
        raise


def init_auth_config(region: str) -> ApmplusConfig:
    """Initialize auth config from env or request context."""
    conf = load_config()  # load default config from env
    if region and len(region) > 0:
        conf.region = region
        conf.endpoint = get_endpoint_by_region(region)

    if os.getenv(ENV_MCP_DEV_MODE, "False") != "True":
        # 从 context 中获取 header
        ctx: Context[ServerSession, object] = mcp.get_context()
        raw_request: Request | None = ctx.request_context.request

        auth = None
        if raw_request:
            # 从 header 的 authorization 字段读取 base64 编码后的 sts json
            auth = raw_request.headers.get("authorization", None)
        if auth is None:
            # 如果 header 中没有认证信息，可能是 stdio 模式，尝试从环境变量获取
            auth = os.getenv("authorization", None)
        if auth is not None:
            if " " in auth:
                _, base64_data = auth.split(" ", 1)
            else:
                base64_data = auth

            try:
                # 解码 Base64
                decoded_str = base64.b64decode(base64_data).decode("utf-8")
                data = json.loads(decoded_str)
                # 获取字段
                conf.access_key = data.get("AccessKeyId")
                conf.secret_key = data.get("SecretAccessKey")
                conf.session_token = data.get("SessionToken")
                return conf
            except Exception as e:
                raise ValueError("Decode authorization info error", e)
    if not conf.is_valid():
        raise ValueError("No valid auth info found")
    return conf


def get_endpoint_by_region(region: str = None) -> str:
    return f"apmplus-server.{region}.volcengineapi.com"


def main():
    parser = argparse.ArgumentParser(description="Run the APMPlus MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default=os.getenv(ENV_MCP_SERVER_MODE, "stdio"),
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )

    args = parser.parse_args()

    try:
        # Load configuration from environment variables
        global config

        config = load_config()
        volcenginesdkcore.Configuration.set_default(config.to_volc_configuration())

        # Run the MCP server
        logger.info(f"Starting APMPlus MCP Server with {args.transport} transport")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting APMPlus MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
