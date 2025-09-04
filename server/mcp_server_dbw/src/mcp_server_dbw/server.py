import os
from pydantic import Field
import logging
import argparse
from mcp.server.fastmcp import FastMCP
from mcp_server_dbw.resource.dbw_resource import DBWSDK
from typing import List, Dict, Any, Optional

# 初始化MCP服务
mcp_server = FastMCP("dbw_mcp_server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))
logger = logging.getLogger("dbw_mcp_server")

dbw_resource = DBWSDK(
    region=os.getenv('VOLCENGINE_REGION', "cn-beijing"),
    ak=os.getenv('VOLCENGINE_ACCESS_KEY'),
    sk=os.getenv('VOLCENGINE_SECRET_KEY'),
    host=os.getenv('VOLCENGINE_ENDPOINT'),
    instance_id=os.getenv('VOLCENGINE_INSTANCE_ID'),
    instance_type=os.getenv('VOLCENGINE_INSTANCE_TYPE'),
    database=os.getenv('VOLCENGINE_DATABASE'),
)


@mcp_server.tool(
    name="nl2sql",
    description="根据自然语言生成SQL语句",
)
def nl2sql(
        query: str = Field(default="", description="自然语言问题"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型"),
        database: Optional[str] = Field(default=None, description="火山引擎数据库名称"),
        tables: Optional[List[str]] = Field(default=None, description="可选的火山引擎数据库内涉及的数据表列表"),
) -> dict[str, Any]:
    """
    根据自然语言生成SQL语句

    Args:
        query (str): 自然语言问题
        instance_id (str, optional): 火山引擎数据库实例ID
        instance_type (str, optional): 火山引擎数据库实例类型
        database (str, optional): 火山引擎数据库名称
        tables (List[str], optional): 可选的火山引擎数据库内涉及的数据表列表
    Returns:
        sql (str): 根据自然语言问题生成的SQL语句
    """
    instance_id = dbw_resource.instance_id or instance_id
    if not instance_id:
        raise ValueError("instance_id is required")

    instance_type = dbw_resource.instance_type or instance_type
    if not instance_type:
        raise ValueError("instance_type is required")

    database = dbw_resource.database or database
    if not database:
        raise ValueError("database is required")

    req = {
        "query": query,
        "instance_id": instance_id,
        "instance_type": instance_type,
        "database": database,
        "tables": tables,
    }
    resp = dbw_resource.nl2sql(req)

    return resp.to_dict()


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the DBW MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting DBW MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting DBW MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
