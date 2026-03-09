"""HQD Multi-Source Search MCP Server — thin proxy to remote HQD MCP service."""

import argparse
import logging
import os
from typing import Dict, Optional

from mcp.server.fastmcp import FastMCP

from mcp_server_hqd.config import config
from mcp_server_hqd.remote_client import HqdRemoteClient

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Remote client (lazy-initialized on first tool call)
_client: Optional[HqdRemoteClient] = None


def get_client() -> HqdRemoteClient:
    global _client
    if _client is None:
        _client = HqdRemoteClient(config.endpoint)
    return _client


# Create MCP server
mcp = FastMCP("HQD Multi-Source Search", port=config.port)


@mcp.tool()
def describe_datasource(
    datasource_id: str = "all",
    locale: str = "zh-CN",
) -> str:
    """
    获取数据源的可查询元数据信息，包括维度（dimensions）、指标（metrics）和过滤条件（filters）。

    Agent 应先调用此工具了解数据结构，再调用 query_datasource 进行查询。
    支持查询单个数据源或列出所有可用数据源。

    Args:
        datasource_id: 数据源 ID。传入具体 ID 返回该数据源的完整元数据；
                       不传或传 'all' 返回所有已注册数据源的摘要列表。
        locale: 返回字段描述的语言，默认 zh-CN
    """
    logger.info(f"describe_datasource: datasource_id={datasource_id}")
    try:
        return get_client().call_tool("describe_datasource", {
            "datasource_id": datasource_id,
            "locale": locale,
        })
    except Exception as e:
        logger.error(f"Error in describe_datasource: {e}")
        return f'{{"error": "{e}"}}'


@mcp.tool()
def query_datasource(
    datasource_id: str,
    select_fields: Optional[str] = None,
    filters: Optional[str] = None,
    aggregation: Optional[str] = None,
    group_by: Optional[str] = None,
    sort_field: Optional[str] = None,
    sort_order: str = "desc",
    page: int = 1,
    page_size: int = 10,
) -> str:
    """
    查询指定数据源的实际数据。

    使用前请先调用 describe_datasource 获取该数据源的可用维度、指标和过滤条件。

    过滤条件格式: 'field:op:value'，多个用分号(;)分隔。
    操作符: eq(精确), like(模糊), in(批量), not_in(排除), between(范围), range(数值范围), keyword(全文搜索)。

    Args:
        datasource_id: 目标数据源 ID（必填）。
        select_fields: 返回字段列表，逗号分隔。
        filters: 过滤条件字符串。
        aggregation: 聚合方式，格式 '字段:函数'。
        group_by: 分组字段，逗号分隔。
        sort_field: 排序字段名。
        sort_order: 排序方向 (asc/desc，默认 desc)。
        page: 页码（默认 1）。
        page_size: 每页记录数（默认 10，最大 50）。
    """
    logger.info(f"query_datasource: datasource_id={datasource_id}, filters={filters}")
    try:
        args = {"datasource_id": datasource_id}
        if select_fields is not None:
            args["select_fields"] = select_fields
        if filters is not None:
            args["filters"] = filters
        if aggregation is not None:
            args["aggregation"] = aggregation
        if group_by is not None:
            args["group_by"] = group_by
        if sort_field is not None:
            args["sort_field"] = sort_field
        args["sort_order"] = sort_order
        args["page"] = page
        args["page_size"] = page_size

        return get_client().call_tool("query_datasource", args)
    except Exception as e:
        logger.error(f"Error in query_datasource: {e}")
        return f'{{"error": "{e}"}}'


def main():
    """Main entry point for the HQD MCP Server."""
    parser = argparse.ArgumentParser(
        description="Run the HQD Multi-Source Search MCP Server"
    )
    parser.add_argument(
        "--transport", "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()

    logger.info(
        f"Starting HQD MCP Server with {args.transport} transport, "
        f"proxying to {config.endpoint}"
    )

    try:
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting HQD MCP Server: {e}")
        raise


if __name__ == "__main__":
    main()
