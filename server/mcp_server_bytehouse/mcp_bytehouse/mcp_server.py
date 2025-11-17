import os
import importlib
import logging
from typing import Sequence
import concurrent.futures
import atexit

import clickhouse_connect
from clickhouse_connect.driver.binding import quote_identifier, format_query_value
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from mcp_bytehouse.mcp_env import config

MCP_SERVER_NAME = "mcp_bytehouse"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(MCP_SERVER_NAME)

QUERY_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=10)
atexit.register(lambda: QUERY_EXECUTOR.shutdown(wait=True))
SELECT_QUERY_TIMEOUT_SECS = 30

load_dotenv()

deps = [
    "clickhouse-connect",
    "python-dotenv",
    "uvicorn",
    "pip-system-certs",
]

mcp = FastMCP(MCP_SERVER_NAME, 
              dependencies=deps, 
              host=os.getenv("MCP_SERVER_HOST","0.0.0.0"), 
              port=int(os.getenv("PORT", "8000")), 
              stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true", 
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))


@mcp.tool()
def list_databases():
    """List available ByteHouse databases"""
    logger.info("Listing all databases")
    client = create_clickhouse_client()
    result = client.command("SHOW DATABASES")
    logger.info(f"Found {len(result) if isinstance(result, list) else 1} databases")
    return result


@mcp.tool()
def list_tables(database: str, like: str = None):
    """List available ByteHouse tables in a database"""
    logger.info(f"Listing tables in database '{database}'")
    client = create_clickhouse_client()
    query = f"SHOW TABLES FROM {quote_identifier(database)}"
    if like:
        query += f" LIKE {format_query_value(like)}"
    result = client.command(query)

    # Get all table comments in one query
    table_comments_query = f"SELECT name, comment FROM system.tables WHERE database = {format_query_value(database)}"
    table_comments_result = client.query(table_comments_query)
    table_comments = {row[0]: row[1] for row in table_comments_result.result_rows}

    # Get all column comments in one query
    column_comments_query = f"SELECT table, name, comment FROM system.columns WHERE database = {format_query_value(database)}"
    column_comments_result = client.query(column_comments_query)
    column_comments = {}
    for row in column_comments_result.result_rows:
        table, col_name, comment = row
        if table not in column_comments:
            column_comments[table] = {}
        column_comments[table][col_name] = comment

    def get_table_info(table):
        logger.info(f"Getting schema info for table {database}.{table}")
        schema_query = f"DESCRIBE TABLE {quote_identifier(database)}.{quote_identifier(table)}"
        schema_result = client.query(schema_query)

        columns = []
        column_names = schema_result.column_names
        for row in schema_result.result_rows:
            column_dict = {}
            for i, col_name in enumerate(column_names):
                column_dict[col_name] = row[i]
            # Add comment from our pre-fetched comments
            if table in column_comments and column_dict['name'] in column_comments[table]:
                column_dict['comment'] = column_comments[table][column_dict['name']]
            else:
                column_dict['comment'] = None
            columns.append(column_dict)

        create_table_query = f"SHOW CREATE TABLE {database}.`{table}`"
        create_table_result = client.command(create_table_query)

        return {
            "database": database,
            "name": table,
            "comment": table_comments.get(table),
            "columns": columns,
            "create_table_query": create_table_result,
        }

    tables = []
    if isinstance(result, str):
        # Single table result
        for table in (t.strip() for t in result.split()):
            if table:
                tables.append(get_table_info(table))
    elif isinstance(result, Sequence):
        # Multiple table results
        for table in result:
            tables.append(get_table_info(table))

    logger.info(f"Found {len(tables)} tables")
    return tables


def execute_query(query: str):
    client = create_clickhouse_client()
    try:
        res = client.query(query, settings={"readonly": 1})
        column_names = res.column_names
        rows = []
        for row in res.result_rows:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                row_dict[col_name] = row[i]
            rows.append(row_dict)
        logger.info(f"Query returned {len(rows)} rows")
        return rows
    except Exception as err:
        logger.error(f"Error executing query: {err}")
        return f"error running query: {err}"

def execute_dml_ddl_query(query: str):
    client = create_clickhouse_client()
    try:
        res = client.command(query)
        return "executed successfully"

    except Exception as err:
        logger.error(f"Error executing query: {err}")
        return f"error running query: {err}"

@mcp.tool()
def run_select_query(query: str):
    """Run a SELECT query in a ByteHouse database
        Note: 调用前转义SQL包含的双引号，确保符合JSON格式
        Note: 不用加FORMAT
    """
    logger.info(f"Executing SELECT query: {query}")
    future = QUERY_EXECUTOR.submit(execute_query, query)
    try:
        result = future.result(timeout=SELECT_QUERY_TIMEOUT_SECS)
        return result
    except concurrent.futures.TimeoutError:
        logger.warning(f"Query timed out after {SELECT_QUERY_TIMEOUT_SECS} seconds: {query}")
        future.cancel()
        return f"Queries taking longer than {SELECT_QUERY_TIMEOUT_SECS} seconds are currently not supported."


@mcp.tool()
def run_dml_ddl_query(query: str):
    """Run a DML/DDL query in a ByteHouse database
    Note: 建表前先询问用户使用的是ByteHouse云数仓还是ByteHouse企业版，推荐优先使用ByteHouse自研的表引擎
    Note: 表引擎优先使用ByteHouse自研的表引擎，可通过get_bytehouse_table_engine_doc获取表引擎的文档，其中doc_name：ha_unique_merge_tree, ha_merge_tree, distributed是企业版的， cnch_merge_tree, cnch_unique_merge_tree是云数仓的
    Note: 调用前转义SQL包含的双引号，确保符合JSON格式
    Note: 企业版默认是用ON CLUSTER使得DDL在全部节点上执行，使用ON CLUSTER子句前，请确认集群名正常，可以查询system.clusters获得
    """
    logger.info(f"Executing DML/DDL query: {query}")
    future = QUERY_EXECUTOR.submit(execute_dml_ddl_query, query)
    try:
        result = future.result(timeout=SELECT_QUERY_TIMEOUT_SECS)
        return result
    except concurrent.futures.TimeoutError:
        logger.warning(f"Query timed out after {SELECT_QUERY_TIMEOUT_SECS} seconds: {query}")
        future.cancel()
        return f"Queries taking longer than {SELECT_QUERY_TIMEOUT_SECS} seconds are currently not supported."

@mcp.tool()
def get_bytehouse_table_engine_doc(doc_name: str):
    """Get the documentation for a ByteHouse table engine
    Node: 有以下几种文档名doc_name ha_unique_merge_tree, ha_merge_tree, distributed, cnch_merge_tree, cnch_unique_merge_tree
    输入对应的表引擎名，返回对应的文档，请参考文档描述，按照用户需求选择对应的表引擎
    """
    try:
        with importlib.resources.open_text('mcp_bytehouse.knowledge', f'{doc_name}.md') as f:
            content = f.read()
            return content
    except FileNotFoundError:
        return f"No documentation found for table engine {doc_name}"
    except Exception as e:
        return f"An error occurred while reading the documentation: {str(e)}"

def create_clickhouse_client():
    client_config = config.get_client_config()
    logger.info(
        f"Creating ByteHouse client connection to {client_config['host']}:{client_config['port']} "
        f"as {client_config['username']} "
        f"(secure={client_config['secure']}, verify={client_config['verify']}, "
        f"connect_timeout={client_config['connect_timeout']}s, "
        f"send_receive_timeout={client_config['send_receive_timeout']}s)"
    )

    try:
        client = clickhouse_connect.get_client(**client_config)
        # Test the connection
        version = client.server_version
        logger.info(f"Successfully connected to ByteHouse server version {version}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to ByteHouse: {str(e)}")
        raise
