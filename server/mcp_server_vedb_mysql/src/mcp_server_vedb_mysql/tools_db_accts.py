import logging
from typing import Any, Final, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)
openapi_cli = vedbm_resource_sdk.client


@mcp_server.tool(
    description="Retrieve a list of databases created in a specific VeDB MySQL instance, including privileges info",
)
def list_vedb_mysql_instance_databases(
        instance_id: str
) -> dict[str, Any]:
    logger.info("list_vedb_mysql_instance_databases")
    batch_size: Final = 100

    req = volcenginesdkvedbm.models.DescribeDatabasesRequest(
        instance_id=instance_id,
        page_size=batch_size,
        page_number=1,
    )
    rsp = volcenginesdkvedbm.models.DescribeDatabasesResponse(databases=[])

    try:
        while True:
            rsp_page = openapi_cli.describe_databases(req)
            rsp.databases.extend(rsp_page.databases)
            if len(rsp_page.databases) < batch_size:
                break
            req.page_number += 1

        rsp.total = len(rsp.databases)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}


@mcp_server.tool(
    description="Obtain a list of accounts in a single VeDB MySQL instance, with their privilege details. 触发示例：查询实例中的所有账号列表及权限详情",
)
def list_vedb_mysql_instance_accounts(
    instance_id: str
) -> dict[str, Any]:
    logger.info("list_vedb_mysql_instance_accounts")
    batch_size: Final = 100

    req = volcenginesdkvedbm.models.DescribeDBAccountsRequest(
        instance_id=instance_id,
        page_size=batch_size,
        page_number=1,
    )
    rsp = volcenginesdkvedbm.models.DescribeDBAccountsResponse(accounts=[])

    try:
        while True:
            rsp_page = openapi_cli.describe_db_accounts(req)
            rsp.accounts.extend(rsp_page.accounts)
            if len(rsp_page.accounts) < batch_size:
                break
            req.page_number += 1

        rsp.total = len(rsp.accounts)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}
    

@mcp_server.tool(
    description="修改实例内某个mysql账号的描述信息。触发示例：vedbm-instanceid下修改账号user1的描述信息为开发账号"
)
def modify_db_account_description(instance_id: str,
                                  account_name: str,
                                  account_desc: str) -> str:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_desc": account_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    vedbm_resource_sdk.modify_db_account_description(req)
    return "succ"


@mcp_server.tool(
    description="修改实例内某个mysql数据库的描述信息。触发示例：vedbm-instanceid下修改数据库test_db的描述信息为测试数据库"
)
def modify_database_description(instance_id: str,
                                db_name: str,
                                db_desc: str) -> str:
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "db_desc": db_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    vedbm_resource_sdk.modify_database_description(req)
    return "succ"

@mcp_server.tool(
    description="在实例内创建mysql账号。触发示例：在实例vedbm-instanceid内创建普通新账号test_mcp，密码为Password123"
)
def create_db_account(instance_id: str,
                      account_name: str,
                      account_password: str,
                      account_type: Annotated[str, Field(examples=['Normal','Super'])],
                      account_desc: str = None,
                      account_privileges: list[dict[str, Any]] = None) -> str:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_password": account_password,
        "account_type": account_type,
        "account_desc": account_desc,
        "account_privileges": account_privileges,
    }
    req = {k: v for k, v in req.items() if v is not None}
    vedbm_resource_sdk.create_db_account(req)
    return "succ"

@mcp_server.tool(
    description="在实例内创建mysql数据库。触发示例：vedbm-instanceid下创建数据库test_db"
)
def create_database(instance_id: str,
                    db_name: str,
                    character_set_name: Optional[str] = 'utf8mb4',
                    databases_privileges: Optional[list[dict[str, Any]]] = None,
                    db_desc: Optional[str] = None) -> str:
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "character_set_name": character_set_name,
        "databases_privileges": databases_privileges,
        "db_desc": db_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    vedbm_resource_sdk.create_database(req)
    return "succ"
