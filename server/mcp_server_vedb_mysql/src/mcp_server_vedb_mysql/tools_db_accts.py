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
    description="修改mysqld账号的描述信息。触发示例：修改账号user1的描述信息为开发账号"
)
def modify_db_account_description(instance_id: str,
                                  account_name: str,
                                  account_desc: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_desc": account_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_account_description(req)
    return resp.to_dict()


@mcp_server.tool(
    description="修改mysqld数据库的描述信息。触发示例：修改数据库test_db的描述信息为测试数据库"
)
def modify_database_description(instance_id: str,
                                db_name: str,
                                db_desc: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "db_desc": db_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_database_description(req)
    return resp.to_dict()


@mcp_server.tool(
    description="将高权限账号的权限重置到初始状态。触发示例：重置高权限账号admin的权限到初始状态"
)
def reset_account_priv(instance_id: str,
                       account_name: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.reset_account(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为账号撤销对数据库的权限。触发示例：撤销账号user1对数据库test_db的所有权限"
)
def revoke_db_account_privilege(instance_id: str,
                                account_name: str,
                                db_names: Annotated[str, Field(description='多个数据库用英文逗号隔开')]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "db_names": db_names,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.revoke_db_account_privilege(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为账号赋予指定数据库的权限。触发示例：为账号user1授予对数据库test_db的读写权限"
)
def grant_db_account_privilege(instance_id: str,
                               account_name: str,
                               account_privileges: Annotated[list[dict[str, Any]], Field(examples=['[{"DBName":"db1","AccountPrivilege":"ReadWrite"}]'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_privileges": account_privileges,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.grant_db_account_privilege(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改数据库账号密码。调用 ResetDBAccount 接口修改数据库账号密码。触发示例：修改账号user1的密码为NewPassword456"
)
def reset_account_passwd(instance_id: str,
                     account_name: str,
                     account_password: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_password": account_password,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.reset_db_account(req)
    return resp.to_dict()


@mcp_server.tool(
    description="创建管理数据库的账号"
)
def create_db_account(instance_id: str,
                      account_name: str,
                      account_password: str,
                      account_type: Annotated[str, Field(examples=['Normal','Super'])],
                      account_desc: str = None,
                      account_privileges: list[dict[str, Any]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_password": account_password,
        "account_type": account_type,
        "account_desc": account_desc,
        "account_privileges": account_privileges,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_db_account(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为实例创建数据库。触发示例：创建数据库test_db，字符集为utf8mb4"
)
def create_database(instance_id: str,
                    db_name: str,
                    character_set_name: Optional[str] = 'utf8mb4',
                    databases_privileges: Optional[list[dict[str, Any]]] = None,
                    db_desc: Optional[str] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "character_set_name": character_set_name,
        "databases_privileges": databases_privileges,
        "db_desc": db_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_database(req)
    return resp.to_dict()

@mcp_server.tool(
    description="删除数据库账号。触发示例：删除账号user1"
)
def delete_db_account(instance_id: str,
                      account_name: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_account(req)
    return resp.to_dict()


@mcp_server.tool(
    description="删除实例的数据库。触发示例：删除数据库test_db"
)
def delete_database(instance_id: str,
                    db_name: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_database(req)
    return resp.to_dict()
