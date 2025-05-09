import logging
import os

from mcp.server.fastmcp import FastMCP
from mcp_server_apmplus.api import *
from mcp_server_apmplus.config import load_config
from mcp_server_apmplus.model import *

# Initialize FastMCP server
mcp = FastMCP("APMPlus MCP Server", port=int(os.getenv("PORT", "8000")))


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
        req = ApmplusServerListAlertRuleRequest(
            region_id=region_id,
            keyword=keyword,
            page_number=page_number,
            page_size=page_size,
        )
        config = load_config()
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
        req = ApmplusServerListNotifyGroupRequest(
            region_id=region_id,
            keyword=keyword,
            page_number=page_number,
            page_size=page_size,
        )
        config = load_config()
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
        req = ApmplusServerQueryMetricsRequest(
            region_id=region_id,
            query=query,
            start_time=start_time,
            end_time=end_time,
        )
        config = load_config()
        api = ApmplusApi(config)
        return api.server_query_metrics(req)
    except Exception as e:
        logging.error(f"Error in apmplus_server_query_metrics: {e}")
        raise
