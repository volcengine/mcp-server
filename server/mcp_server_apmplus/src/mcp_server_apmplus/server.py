import logging
import os

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from starlette.requests import Request

from mcp_server_apmplus.api import *
from mcp_server_apmplus.config import (
    load_config,
    parse_authorization,
    ENV_MCP_SERVER_PORT,
    ENV_MCP_SERVER_NAME,
    ENV_MCP_SERVER_HOST,
)
from mcp_server_apmplus.model import *

# Initialize FastMCP server
mcp = FastMCP(
    os.getenv(ENV_MCP_SERVER_NAME, "mcp_server_apmplus"),
    port=int(os.getenv(ENV_MCP_SERVER_PORT, "8000")),
    host=os.getenv(ENV_MCP_SERVER_HOST, "127.0.0.1"),
)


@mcp.tool()
async def apmplus_server_list_alert_rule(
    region_id: str,
    keyword: str,
    page_number: int,
    page_size: int,
):
    """
    List alert rules.
    Args:
        region_id: Region ID.
        keyword: query keyword.
        page_number: Page number for pagination.
        page_size: Page size for pagination.
    Returns:
        A list of alert rules.
    """
    try:
        if isinstance(region_id, str) and not region_id.strip():
            region_id = DEFAULT_REGION
        if isinstance(keyword, str) and not keyword.strip():
            keyword = None

        req = ApmplusServerListAlertRuleRequest(
            region_id=region_id,
            keyword=keyword,
            page_number=page_number,
            page_size=page_size,
        )

        config = init_auth_config()
        api = ApmplusApi(config)
        return api.server_list_alert_rule(req)
    except Exception as e:
        logging.error(f"Error in apmplus_server_list_alert_rule: {e}")
        raise


@mcp.tool()
async def apmplus_server_list_notify_group(
    region_id: str,
    keyword: str,
    page_number: int,
    page_size: int,
):
    """
    List notify group.
    Args:
        region_id: Region ID.
        keyword: query keyword.
        page_number: Page number for pagination.
        page_size: Page size for pagination.
    Returns:
        A list of notify group.
    """
    try:
        if isinstance(region_id, str) and not region_id.strip():
            region_id = DEFAULT_REGION
        if isinstance(keyword, str) and not keyword.strip():
            keyword = None

        req = ApmplusServerListNotifyGroupRequest(
            region_id=region_id,
            keyword=keyword,
            page_number=page_number,
            page_size=page_size,
        )

        config = init_auth_config()
        api = ApmplusApi(config)
        return api.server_list_notify_group(req)
    except Exception as e:
        logging.error(f"Error in apmplus_server_list_notify_group: {e}")
        raise


@mcp.tool()
async def apmplus_server_query_metrics(
    region_id: str,
    query: str,
    start_time: int,
    end_time: int,
):
    """
    Query metrics.
    Args:
        region_id: Region ID.
        query: Metric expression in PromQL format.
        start_time: Start time in seconds.
        end_time: End time in seconds.
    Returns:
        metrics.
    """
    try:
        if isinstance(region_id, str) and not region_id.strip():
            region_id = DEFAULT_REGION

        req = ApmplusServerQueryMetricsRequest(
            region_id=region_id,
            query=query,
            start_time=start_time,
            end_time=end_time,
        )

        config = init_auth_config()
        api = ApmplusApi(config)
        return api.server_query_metrics(req)
    except Exception as e:
        logging.error(f"Error in apmplus_server_query_metrics: {e}")
        raise


def init_auth_config() -> ApmplusConfig:
    """Initialize auth config from env or request context."""
    conf = load_config()  # load default config from env

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
        if " " in auth:
            _, base64_data = auth.split(" ", 1)
        else:
            base64_data = auth

        try:
            config = parse_authorization(base64_data)
            return config
        except Exception as e:
            raise ValueError("Decode authorization info error", e)
    if not conf.is_valid():
        raise ValueError("No valid auth info found")
    return conf
