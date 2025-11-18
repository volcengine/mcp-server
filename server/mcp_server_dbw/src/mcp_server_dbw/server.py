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
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
        tables: Optional[List[str]] = Field(default=None, description="可选的Database内涉及的Table或Collection列表（关系型数据库实例推荐不填写，Mongo实例必填一个Collection）"),
) -> dict[str, Any]:
    """
    根据自然语言问题生成SQL语句

    Args:
        query (str): 待生成SQL语句的自然语言问题
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
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
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
) -> dict[str, Any]:
    """
    执行SQL语句并返回执行结果

    Args:
        commands (str): 待执行的SQL语句集合
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
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
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        page_number: Optional[int] = Field(default=1, description="分页查询时的页码（默认为1，即从第一页数据开始返回）"),
        page_size: Optional[int] = Field(default=100, description="分页大小（默认为100）")
) -> dict[str, Any]:
    """
    查询数据库实例的Database列表

    Args:
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
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
    if not page_number:
        page_number = 1
    if not page_size:
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
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
        page_number: Optional[int] = Field(default=1, description="分页查询时的页码（默认为1，即从第一页数据开始返回）"),
        page_size: Optional[int] = Field(default=100, description="分页大小（默认为100）")
) -> dict[str, Any]:
    """
    查询数据库实例的Table列表

    Args:
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
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
    if not page_number:
        page_number = 1
    if not page_size:
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
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称")
) -> dict[str, Any]:
    """
    查询数据库实例的Table元信息

    Args:
        table (str): Table名称
        instance_id (str, optional): 火山引擎数据库实例ID（需开启安全管控）
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
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


@mcp_server.tool(
    name="describe_slow_logs",
    description="查询数据库实例的慢日志信息",
)
def describe_slow_logs(
        start_time: int = Field(default=None, description="查询慢日志的开始时间，使用秒时间戳格式"),
        end_time: int = Field(default=None, description="查询慢日志的结束时间，使用秒时间戳格式"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        node_id: Optional[str] = Field(default=None, description="火山引擎数据库实例节点ID"),
        page_number: Optional[int] = Field(default=1, description="分页查询时的页码（默认为1，即从第一页数据开始返回）"),
        page_size: Optional[int] = Field(default=100, description="分页大小（默认为100）"),
        sort_by: Optional[str] = Field(default="ASC", description="按照降序或升序方式排列慢日志（ASC表示升序，DESC表示降序）"),
        order_by: Optional[str] = Field(default="Timestamp", description="返回结果的排序方法（Timestamp按照查询开始时间排序，QueryTime按照查询时间排序，LockTime按照锁的等待时间排序，RowsExamined按照扫描的行数排序，RowsSent按照返回的行数排序")
) -> dict[str, Any]:
    """
    查询数据库实例的慢日志信息

    Args:
        start_time (int): 查询慢日志的开始时间，使用秒时间戳格式
        end_time (int): 查询慢日志的结束时间，使用秒时间戳格式
        instance_id (str, optional): 火山引擎数据库实例ID
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
        node_id (str, optional): 火山引擎数据库实例节点ID
        page_number (int, optional): 分页查询时的页码（默认为1，即从第一页数据开始返回）
        page_size (int, optional): 分页大小（默认为100）
        sort_by (str, optional): 按照降序或升序方式排列慢日志（ASC表示升序，DESC表示降序）
        order_by (str, optional): 返回结果的排序方法（Timestamp按照查询开始时间排序，QueryTime按照查询时间排序，LockTime按照锁的等待时间排序，RowsExamined按照扫描的行数排序，RowsSent按照返回的行数排序
    Returns:
        total (int): 慢日志数量
        slow_logs (list): 慢日志列表信息，列表中的每个值对应一条慢日志记录，结构如下
            - connection_id (int): 连接ID
            - db (str): Database名称
            - lock_time (float): 表示执行被查询对象时需要的锁等待时间，即查询对象可能在别的会话中被锁定，其他语言就需要等待锁释放才可以执行查询操作，这段时间就是锁等待时间
            - query_time (float): 表示查询语句的耗时
            - timestamp (int): 按照查询开始时间排序
            - rows_examined (int): 表示查询时需要扫描的行数
            - rows_sent (int): 命中查询结果后返回数据的行数
            - sql_template (str): SQL模板
            - sql_text (str): SQL文本即实际执行的查询语句
            - source_ip (str): IP地址
            - user (str): 执行者名称
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
    if start_time is None:
        raise ValueError("start_time is required")
    if end_time is None:
        raise ValueError("end_time is required")
    if not page_number:
        page_number = 1
    if not page_size:
        page_size = 100
    if not sort_by:
        sort_by = "ASC"
    if not order_by:
        order_by = "Timestamp"

    req = {
        "region_id": dbw_client.region,
        "instance_id": instance_id,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size,
        "sort_by": sort_by,
        "order_by": order_by,
    }
    if node_id is not None:
        req["node_id"] = node_id

    resp = dbw_client.describe_slow_logs(req)
    return resp.to_dict()


@mcp_server.tool(
    name="list_slow_query_advice",
    description="获取数据库实例的慢日志诊断详情信息",
)
def list_slow_query_advice(
        advice_type: str = Field(default="", description="建议类型（no_advice表示无建议，index_advice表示索引建议，rewrite_sql_advice表示改写SQL建议）"),
        summary_id: str = Field(default="", description="每次慢日志诊断的唯一标识"),
        group_by: str = Field(default="", description="聚合类型（Advice表示按建议聚合，Module表示按模块聚合）"),
        order_by: str = Field(default="", description="排序类型（QueryTimeRatioNow表示按当前查询时间占比排序，Benefit表示按收益排序）"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        page_number: Optional[int] = Field(default=1, description="分页查询时的页码（默认为1，即从第一页数据开始返回）"),
        page_size: Optional[int] = Field(default=100, description="分页大小（默认为100）"),
) -> dict[str, Any]:
    """
    获取数据库实例的慢日志诊断详情信息

    Args:
        advice_type (str): 建议类型（no_advice表示无建议，index_advice表示索引建议，rewrite_sql_advice表示改写SQL建议）
        summary_id (str): 每次慢日志诊断的唯一标识
        group_by (str): 聚合类型（Advice表示按建议聚合，Module表示按模块聚合）
        order_by (str): 排序类型（QueryTimeRatioNow表示按当前查询时间占比排序，Benefit表示按收益排序）
        instance_id (str, optional): 火山引擎数据库实例ID
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
        page_number (int, optional): 分页查询时的页码（默认为1，即从第一页数据开始返回）
        page_size (int, optional): 分页大小（默认为100）
    Returns:
        total (int): 慢日志诊断建议总数
        advices (list[Advice]): 按模块聚合的诊断建议，如果请求参数中group_by取值为Module，则返回advices字段，列表中的每个值为Advice Object，定义如下：
            - db (str): Database名称
            - agg (Agg): 聚合信息，结构定义如下：
                - db (str): Database名称
                - user (str): 用户名
                - table (str): 表名
                - source_ip (str): 客户端地址
                - sql_method (str): SQL类型
                - sql_template (str): 慢SQL模板
                - execute_count (int): 执行次数
                - lock_time_ratio (double): 锁总耗时占比
                - lock_time_stats (dict): 锁耗时的统计结果，以秒为单位
                - rows_sent_ratio (double): 返回总行数占比
                - rows_sent_stats (dict): 返回行数的统计结果
                - sql_template_id (str): 慢SQL模板哈希值
                - last_appear_time (int): 最后一次出现的时间
                - query_time_ratio (double): 查询总耗时占比
                - query_time_stats (dict): 查询耗时的统计结果，以秒为单位
                - sql_fingerprint (str): SQL指纹
                - first_appear_time (int): 第一次出现的时间
                - pt_analysis_result (str): 仿PT解析工具输出结果的文本字符串
                - execute_count_ratio (double): 执行总次数占比
                - rows_examined_ratio (double): 扫描总行数占比
                - rows_examined_stats (dict): 扫描行数的统计结果
            - rist (str): 风险
            - user (list[str]): 用户名列表
            - advice (str): 诊断建议（如果请求参数中advice_type取值为index_advice，该字段为索引SQL；如果请求参数中advice_type取值为rewrite_sql_advice，该字段为SQL建议）
            - benefit (double): 优化后预估总耗时收益
            - speed_up (double): 优化后预估性能提升倍数
            - sql_module (str): SQL模版
            - source_ips (list[str]): 客户端IP列表
            - table_name (str): 表名
            - advice_level (str): 优化推荐程度
            - advice_index_size (double): 推荐索引大小预估
            - query_time_avg_after (double): 优化后查询时间预估
        advices_by_group (list): 按建议聚合的诊断建议，如果请求参数中group_by取值为Advice，则返回advices_by_group字段，列表中的每个值的定义如下：
            - advice (str): 按建议聚合的诊断建议（如果请求参数中advice_type取值为index_advice，该字段为索引SQL；如果请求参数中advice_type取值为rewrite_sql_advice，该字段为SQL建议）
            - advices (list[Advice]): 按模块聚合的诊断建议，结构定义同上述advices字段
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
    if not advice_type:
        raise ValueError("advice_type is required")
    if not summary_id:
        raise ValueError("summary_id is required")
    if not group_by:
        raise ValueError("group_by is required")
    if not order_by:
        raise ValueError("order_by is required")
    if not page_number:
        page_number = 1
    if not page_size:
        page_size = 100

    req = {
        "instance_id": instance_id,
        "instance_type": instance_type,
        "advice_type": advice_type,
        "summary_id": summary_id,
        "group_by": group_by,
        "order_by": order_by,
        "page_number": page_number,
        "page_size": page_size,
    }

    resp = dbw_client.list_slow_query_advice_api(req)
    return resp.to_dict()


@mcp_server.tool(
    name="slow_query_advice_task_history",
    description="获取数据库实例的慢日志诊断历史信息",
)
def slow_query_advice_task_history(
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）"),
        page_number: Optional[int] = Field(default=1, description="分页查询时的页码（默认为1，即从第一页数据开始返回）"),
        page_size: Optional[int] = Field(default=100, description="分页大小（默认为100）"),
) -> dict[str, Any]:
    """
    获取数据库实例的慢日志诊断历史信息

    Args:
        instance_id (str, optional): 火山引擎数据库实例ID
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL和VeDBMySQL，并严格要求大小写一致）
        page_number (int, optional): 分页查询时的页码（默认为1，即从第一页数据开始返回）
        page_size (int, optional): 分页大小（默认为100）
    Returns:
        total (int): 慢日志诊断任务总数
        res_list (list): 慢日志诊断历史列表（由创建时间从新到旧排序），列表中的每个值对应一条慢日志诊断记录，结构如下：
            - db (str): Database名称
            - date (str): 诊断日期（使用UTC+8时区，例如20250427）
            - status (str): 诊断任务状态（INIT表示诊断中，SUCCESS表示诊断成功，EXCEPTION表示诊断异常）
            - summary_id (str): 每次诊断的唯一标识
            - slow_query_num (int): 总诊断慢SQL数量
            - advice_index_num (int): 索引建议SQL数量
            - no_advice_sql_num (int): 无建议SQL数量
            - advice_rewrite_num (int): 待改写SQL数量
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
    if not page_number:
        page_number = 1
    if not page_size:
        page_size = 100

    req = {
        "instance_id": instance_id,
        "instance_type": instance_type,
        "page_number": page_number,
        "page_size": page_size,
    }

    resp = dbw_client.slow_query_advice_task_history_api(req)
    return resp.to_dict()


@mcp_server.tool(
    name="create_dml_sql_change_ticket",
    description="针对数据库实例创建DML数据变更工单",
)
def create_dml_sql_change_ticket(
        sql_text: str = Field(default="", description="待执行的DML SQL语句（普通SQL变更可以支持多条DML语句，多条SQL语句间用英文分号隔开；普通SQL变更，适用于少量数据变更场景，支持多条语句）"),
        ticket_execute_type: str = Field(default="Auto", description="工单执行类型（Auto表示审批完成自动执行；Manual表示手动执行；Cron表示定时执行）"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL、VeDBMySQL和Postgres，并严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
        exec_start_time: Optional[int] = Field(default=None, description="执行开始时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行开始时间）"),
        exec_end_time: Optional[int] = Field(default=None, description="执行结束时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行结束时间，且需要晚于执行开始时间）"),
        title: Optional[str] = Field(default=None, description="工单标题"),
        memo: Optional[str] = Field(default=None, description="工单备注信息，详实的备注信息有利于后期维护")
) -> dict[str, Any]:
    """
    针对数据库实例创建DML数据变更工单

    Args:
        sql_text (str): 待执行的DML SQL语句（普通SQL变更可以支持多条DML语句，多条SQL语句间用英文分号隔开；普通SQL变更，适用于少量数据变更场景，支持多条语句）
        ticket_execute_type (str): 工单执行类型（Auto表示审批完成自动执行；Manual表示手动执行；Cron表示定时执行）
        instance_id (str, optional): 火山引擎数据库实例ID
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL、VeDBMySQL和Postgres，并严格要求大小写一致）
        database (str, optional): Database名称
        exec_start_time (int, optional): 执行开始时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行开始时间）
        exec_end_time (int, optional): 执行结束时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行结束时间，且需要晚于执行开始时间）
        title (str, optional): 工单标题
        memo (str, optional): 工单备注信息，详实的备注信息有利于后期维护
    Returns:
        ticket_id (str): 工单号
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
    if not sql_text:
        raise ValueError("sql_text is required")
    if not ticket_execute_type:
        ticket_execute_type = "Auto"

    req = {
        "instance_id": instance_id,
        "instance_type": instance_type,
        "database_name": database,
        "sql_text": sql_text,
        "ticket_execute_type": ticket_execute_type,
    }
    if exec_start_time is not None:
        req["exec_start_time"] = exec_start_time
    if exec_end_time is not None:
        req["exec_end_time"] = exec_end_time
    if title is not None:
        req["title"] = title
    if memo is not None:
        req["memo"] = memo

    # resp = dbw_client.
    # return resp.to_dict()


@mcp_server.tool(
    name="create_ddl_sql_change_ticket",
    description="针对数据库实例创建DDL结构变更工单",
)
def create_ddl_sql_change_ticket(
        sql_text: str = Field(default="", description="待执行的DDL SQL语句（普通SQL变更可以下发多条DDL语句，多条SQL语句间用英文分号隔开。注意DDL有锁表风险，建议选择无锁结构变更逐条提交）"),
        ticket_execute_type: str = Field(default="Auto", description="工单执行类型（Auto表示审批完成自动执行；Manual表示手动执行；Cron表示定时执行）"),
        instance_id: Optional[str] = Field(default=None, description="火山引擎数据库实例ID"),
        instance_type: Optional[str] = Field(default=None, description="火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL、VeDBMySQL和Postgres，并严格要求大小写一致）"),
        database: Optional[str] = Field(default=None, description="Database名称"),
        exec_start_time: Optional[int] = Field(default=None, description="执行开始时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行开始时间）"),
        exec_end_time: Optional[int] = Field(default=None, description="执行结束时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行结束时间，且需要晚于执行开始时间）"),
        title: Optional[str] = Field(default=None, description="工单标题"),
        memo: Optional[str] = Field(default=None, description="工单备注信息，详实的备注信息有利于后期维护")
) -> dict[str, Any]:
    """
    针对数据库实例创建DDL结构变更工单

    Args:
        sql_text (str): 待执行的DDL SQL语句（普通SQL变更可以下发多条DDL语句，多条SQL语句间用英文分号隔开。注意DDL有锁表风险，建议选择无锁结构变更逐条提交）
        ticket_execute_type (str): 工单执行类型（Auto表示审批完成自动执行；Manual表示手动执行；Cron表示定时执行）
        instance_id (str, optional): 火山引擎数据库实例ID
        instance_type (str, optional): 火山引擎数据库实例类型（可通过instance_id前缀获取，当前支持MySQL、VeDBMySQL和Postgres，并严格要求大小写一致）
        database (str, optional): Database名称
        exec_start_time (int, optional): 执行开始时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行开始时间）
        exec_end_time (int, optional): 执行结束时间，使用秒时间戳格式（当ticket_execute_type设置为Cron时，需要指定执行结束时间，且需要晚于执行开始时间）
        title (str, optional): 工单标题
        memo (str, optional): 工单备注信息，详实的备注信息有利于后期维护
    Returns:
        ticket_id (str): 工单号
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
    if not sql_text:
        raise ValueError("sql_text is required")
    if not ticket_execute_type:
        ticket_execute_type = "Auto"

    req = {
        "instance_id": instance_id,
        "instance_type": instance_type,
        "database_name": database,
        "sql_text": sql_text,
        "ticket_execute_type": ticket_execute_type,
    }
    if exec_start_time is not None:
        req["exec_start_time"] = exec_start_time
    if exec_end_time is not None:
        req["exec_end_time"] = exec_end_time
    if title is not None:
        req["title"] = title
    if memo is not None:
        req["memo"] = memo

    # resp = dbw_client.
    # return resp.to_dict()


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
