import os
import logging
import argparse
import json
import base64

from pydantic import Field
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from mcp_server_dbw.resource.dbw_resource import DBWClient
from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context
from starlette.requests import Request


logger = logging.getLogger("dbw_mcp_server")

# 初始化MCP服务
mcp_server = FastMCP("DBW MCP Server",
                     host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
                     port=int(os.getenv("MCP_SERVER_PORT", "8000")),
                     streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))
REMOTE_MCP_SERVER = False

DBW_CLIENT = DBWClient(
    region=os.getenv("VOLCENGINE_REGION"),
    ak=os.getenv("VOLCENGINE_ACCESS_KEY"),
    sk=os.getenv("VOLCENGINE_SECRET_KEY"),
    host=os.getenv("VOLCENGINE_ENDPOINT"),
    instance_id=os.getenv("VOLCENGINE_INSTANCE_ID"),
    instance_type=os.getenv("VOLCENGINE_INSTANCE_TYPE"),
    database=os.getenv("VOLCENGINE_DATABASE"),
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
    if REMOTE_MCP_SERVER:
        dbw_client = get_dbw_client(mcp_server.get_context())
    else:
        dbw_client = DBW_CLIENT

    instance_id = dbw_client.instance_id or instance_id
    if not instance_id:
        raise ValueError("instance_id is required")

    instance_type = dbw_client.instance_type or instance_type
    if not instance_type:
        raise ValueError("instance_type is required")

    database = dbw_client.database or database
    if not database:
        raise ValueError("database is required")

    req = {
        "query": query,
        "instance_id": instance_id,
        "instance_type": instance_type,
        "database": database,
    }
    if tables is not None:
        req["tables"] = tables

    resp = dbw_client.nl2sql(req)

    return resp.to_dict()


def get_dbw_client(ctx: Context[ServerSession, object, any]) -> DBWClient:
    auth = None
    raw_request: Request = ctx.request_context.request

    if raw_request:
        # 从 header 的 authorization 字段读取 base64 编码后的 sts json
        auth = raw_request.headers.get("authorization", None)
    if auth is None:
        # 如果 header 中没有认证信息，可能是 stdio 模式，尝试从环境变量获取
        auth = os.getenv("authorization", None)
    if auth is None:
        # 获取认证信息失败
        raise ValueError("Missing authorization info.")
    if ' ' in auth:
        _, base64_data = auth.split(' ', 1)
    else:
        base64_data = auth

    auth_info = {}

    try:
        decoded_str = base64.b64decode(base64_data).decode('utf-8')
        data: dict = json.loads(decoded_str)

        if not data.get('AccessKeyId'):
            raise ValueError("failed to get remote ak")
        if not data.get('SecretAccessKey'):
            raise ValueError("failed to get remote sk")

        auth_info["current_time"] = data.get('CurrentTime')
        auth_info["expired_time"] = data.get('ExpiredTime')
        auth_info["region"] = data.get("Region")
        auth_info["ak"] = data.get('AccessKeyId')
        auth_info["sk"] = data.get('SecretAccessKey')
        auth_info["token"] = data.get('SessionToken')
    except Exception as e:
        raise ValueError("Decode authorization info error, {}", e)

    return DBWClient(
        region=os.getenv('VOLCENGINE_REGION') or auth_info["region"] or "cn-beijing",
        ak=auth_info["ak"],
        sk=auth_info["sk"],
    )


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the DBW MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        type=str,
        choices=["sse", "stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (sse, stdio or streamable-http)",
    )
    parser.add_argument(
        "--remote",
        "-r",
        action="store_true",
        help="Set True to deploy the remote MCP Server")
    args = parser.parse_args()

    global REMOTE_MCP_SERVER
    global DBW_CLIENT

    if args.remote:
        if args.transport == "sse":
            raise ValueError("Remote MCP Server does not support SSE")
        REMOTE_MCP_SERVER = True

    try:
        logger.info(f"Starting DBW MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting DBW MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
