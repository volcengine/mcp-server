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
    description="根据自然语言问题生成SQL语句",
)
def nl2sql(
        query: str = Field(default="", description="待生成SQL语句的自然语言问题"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID（需开启安全管控）"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
        tables: Optional[List[str]] = Field(default=None, description="可选的Database内涉及的Table或Collection列表（关系型数据库实例推荐不填写，Mongo实例必填一个Collection）"),
) -> dict[str, Any]:
    """
    根据自然语言问题生成SQL语句

    Args:
        query (str): 待生成SQL语句的自然语言问题
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）
        database (str, optional): Database名称
        tables (List[str], optional): 可选的Database内涉及的Table或Collection列表（关系型数据库实例推荐不填写，Mongo实例必填一个Collection）
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


@mcp_server.tool(
    name="execute_sql",
    description="执行SQL语句并返回执行结果",
)
def execute_sql(
        commands: str = Field(default="", description="待执行的SQL语句集合"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID（需开启安全管控）"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
) -> dict[str, Any]:
    """
    执行SQL语句并返回执行结果

    Args:
        commands (str): 待执行的SQL语句集合
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）
        database (str, optional): Database名称
    Returns:
        results (list): SQL语句集合执行结果列表，列表中的每个值对应一条SQL语句的执行结果，结构如下
            - command_str (str): SQL语句
            - state (str): SQL语句的执行状态
            - reason_detail (str): SQL语句执行失败时返回的信息
            - run_time (int): SQL语句开始执行的时间戳（单位为毫秒）
            - row_count (int): 执行SQL语句返回或影响的记录条数
            - column_names (list[str]): 执行SQL查询语句返回的结果集字段列表
            - rows (list[dict[str, list[str]]]): 执行SQL语句返回或影响的记录行列表，列表中的每个值的结构如下
                cells (dict[str, list[str]]): 执行SQL语句返回或影响的记录行的单元格值列表
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
        "commands": commands,
        "instance_id": instance_id,
        "instance_type": instance_type,
        "database": database,
        "time_out_seconds": 10
    }

    resp = dbw_client.execute_sql(req)
    return resp.to_dict()


@mcp_server.tool(
    name="list_databases",
    description="查询数据库实例的Database列表",
)
def list_databases(
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID（需开启安全管控）"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）"),
        page_number: Optional[int] = Field(default=1, description="分页查询时的页码（默认为1，即从第一页数据开始返回）"),
        page_size: Optional[int] = Field(default=100, description="分页大小（默认为100）")
) -> dict[str, Any]:
    """
    查询数据库实例的Database列表

    Args:
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）
        page_number (int, optional): 分页查询时的页码（默认为1，即从第一页数据开始返回）
        page_size (int, optional): 分页大小（默认为100）
    Returns:
        total (int): 数据库实例的Database总数
        items (list): Database元信息列表，列表中的每个值对应一个Database的元信息，结构如下
            - name (str): Database名称
            - character_set_name (str): Database字符集名称
            - collation_name (str): Database排序集规则
            - is_system_db (bool): Database是否为系统库
            - description (str): Database描述
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
    if page_number is None:
        page_number = 1
    if page_size is None:
        page_size = 100

    req = {
        "instance_id": instance_id,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size,
    }

    resp = dbw_client.list_databases(req)
    return resp.to_dict()


@mcp_server.tool(
    name="list_tables",
    description="查询数据库实例的Table列表",
)
def list_tables(
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID（需开启安全管控）"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
        page_number: Optional[int] = Field(default=1, description="分页查询时的页码（默认为1，即从第一页数据开始返回）"),
        page_size: Optional[int] = Field(default=100, description="分页大小（默认为100）")
) -> dict[str, Any]:
    """
    查询数据库实例的Table列表

    Args:
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）
        database (str, optional): Database名称
        page_number (int, optional): 分页查询时的页码（默认为1，即从第一页数据开始返回）
        page_size (int, optional): 分页大小（默认为100）
    Returns:
        total (int): 指定Database的Table总数
        items (list[str]): 指定Database的Table名称列表
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
    if page_number is None:
        page_number = 1
    if page_size is None:
        page_size = 100

    req = {
        "instance_id": instance_id,
        "instance_type": instance_type,
        "database": database,
        "page_number": page_number,
        "page_size": page_size,
    }

    resp = dbw_client.list_tables(req)
    return resp.to_dict()


@mcp_server.tool(
    name="get_table_info",
    description="查询数据库实例的Table元信息",
)
def get_table_info(
        table: str = Field(default="", description="Table名称"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID（需开启安全管控）"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称")
) -> dict[str, Any]:
    """
    查询数据库实例的Table元信息

    Args:
        table (str): Table名称
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（当前支持MySQL和VeDBMySQL，严格要求大小写一致）
        database (str, optional): Database名称
    Returns:
        table_meta (dict[str, dict[str, Any]]): Table元信息，结构如下
            - name (str): Table名称
            - engine (str): 存储引擎
            - character_set (str): Table字符集
            - collations (str): Table校验规则
            - definition (str): 建表DDL语句
            - columns (list[dict[str, Any]]): Table字段元信息列表，列表中的每个值对应Table一个字段的元信息，结构如下
                - name (str): 字段名称
                - type (str): 字段类型
                - length (str): 字段长度
                - allow_be_null (bool): 字段是否允许为NULL
                - comment (str): 字段注释
                - is_primary_key (bool): 字段是否为主键
                - primary_key_order (str): 字段PrimaryKeyOrder
                - is_auto_increment (bool): 字段是否为AutoIncrement
                - default_value (str): 字段默认值
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
        "instance_id": instance_id,
        "instance_type": instance_type,
        "database": database,
        "table": table,
    }

    resp = dbw_client.get_table_info(req)
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
