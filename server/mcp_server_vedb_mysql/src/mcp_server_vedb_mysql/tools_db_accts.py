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
    description="Obtain a list of accounts in a single VeDB MySQL instance, with their privilege details",
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
    description="修改mysqld账号的描述信息"
)
def modify_db_account_description(instance_id: str,
                                  account_name: Annotated[str, Field(description='数据库账号名称。(您可以调用 [DescribeDBAccounts] 接口查询数据库账号的信息，包括账号名称。)', examples=['testuser'])],
                                  account_desc: Annotated[str, Field(description='账号的描述信息，描述内容长度为 0~256 个字符。可以包含数字、中文、英文、下划线（_）和中划线（-）。(若传入空字符串（即长度为 0），则表示清空原有描述。)', examples=['这是一段账号的描述信息'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_desc": account_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_account_description(req)
    return resp.to_dict()


@mcp_server.tool(
    description="修改mysqld数据库的描述信息"
)
def modify_database_description(instance_id: str,
                                db_name: Annotated[str, Field(description='目标数据库名称。', examples=['testdb1'])],
                                db_desc: Annotated[str, Field(description='数据库的描述信息，描述内容长度为 0~256 个字符。可以包含数字、中文、英文、下划线（_）和中划线（-）。(若传入空字符串（即长度为 0），则表示清空原有描述。)', examples=['这是一段数据库的描述信息'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "db_desc": db_desc,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_database_description(req)
    return resp.to_dict()


@mcp_server.tool(
    description="将高权限账号的权限重置到初始状态"
)
def reset_account_priv(instance_id: str,
                  account_name: Annotated[str, Field(description='高权限账号名称。(您可以调用DescribeDBAccounts接口查询数据库账号的信息，包括账号名称。)', examples=['testuser1'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.reset_account(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为账号撤销对数据库的权限"
)
def revoke_db_account_privilege(instance_id: str,
                                account_name: Annotated[str, Field(description='数据库账号名称。(您可以调用DescribeDBAccounts接口查询数据库账号的信息，包括账号名称。)', examples=['testuser'])],
                                db_names: Annotated[str, Field(description='数据库名称。(* 撤销账号对该数据库的所有权限。* 当有多个数据库时，需用英文逗号（,）隔开。)', examples=['testdb1,testdb2'])]) -> dict[str, Any]:
    """调用 RevokeDBAccountPrivilege 接口为账号撤销对数据库的权限。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        account_name (str): 数据库账号名称。
            (
            您可以调用DescribeDBAccounts接口查询数据库账号的信息，包括账号名称。
            )
            示例值：testuser
        db_names (str): 数据库名称。
            (
            * 撤销账号对该数据库的所有权限。
            * 当有多个数据库时，需用英文逗号（,）隔开。
            )
            示例值：testdb1,testdb2
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "db_names": db_names,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.revoke_db_account_privilege(req)
    return resp.to_dict()

@mcp_server.tool(
    description="为账号赋予指定数据库的权限"
)
def grant_db_account_privilege(instance_id: str,
                               account_name: Annotated[str, Field(description='数据库账号的名称', examples=['testuser'])],
                               account_privileges: Annotated[list[dict[str, Any]], Field(description='账号授权信息', examples=['[{"DBName":"db1","AccountPrivilege":"ReadWrite"}]'])]) -> dict[str, Any]:
    """调用 GrantDBAccountPrivilege 接口为账号赋予指定数据库的权限。

    Args:
        instance_id (str): 实例 ID。
            (
            您可以调用DescribeDBInstances接口查询实例 ID。
            )
            示例值：vedbm-r3xq0zdl****
        account_name (str): 普通数据库账号的名称。
            示例值：testuser
        account_privileges (list[dict[str, Any]]): 重置账号授权信息。
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_privileges": account_privileges,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.grant_db_account_privilege(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改数据库账号密码"
)
def reset_account_passwd(instance_id: str,
                     account_name: Annotated[str, Field(description='数据库账号名称。(您可以调用DescribeDBAccounts接口查询数据库账号的信息，包括账号名称。)', examples=['testuser'])],
                     account_password: Annotated[str, Field(description='数据库账号的密码。账号密码需满足以下要求：* 只能包含大小写字母、数字及以下特殊字符 ``~!@#$%^&*_-+=`|\(){}[]:;\'<>,.?/``。* 长度需在 8~32 个字符内。* 至少包含大写字母、小写字母、数字或特殊字符中的 3 种。', examples=['Test****'])]) -> dict[str, Any]:
    """调用 ResetDBAccount 接口修改数据库账号密码。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        account_name (str): 数据库账号名称。
            (
            您可以调用DescribeDBAccounts接口查询数据库账号的信息，包括账号名称。
            )
            示例值：testuser
        account_password (str): 数据库账号的密码。账号密码需满足以下要求：
            * 只能包含大小写字母、数字及以下特殊字符 ``~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/``。
            * 长度需在 8~32 个字符内。
            * 至少包含大写字母、小写字母、数字或特殊字符中的 3 种。
            示例值：Test****
    """
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
                      account_name: Annotated[str, Field(description='数据库账号名称。账号名称需满足以下要求：* 名称唯一，且长度在 2~32 个字符内。* 由字母、数字、中划线（-）、下划线（_）组成。* 以字母开头，以字母或数字结尾。* 名称内不能包含某些禁用词，详细信息请参见[禁用关键词](https://www.volcengine.com/docs/6357/79942)。', examples=['testuser1'])],
                      account_password: Annotated[str, Field(description='数据库账号的密码。账号密码需满足以下要求：* 只能包含大小写字母、数字及以下特殊字符 ``~!@#$%^&*_-+=`|\(){}[]:;\'<>,.?/``。* 长度需在 8~32 个字符内。* 至少包含大写字母、小写字母、数字或特殊字符中的 3 种。', examples=['Test****'])],
                      account_type: Annotated[str, Field(description='数据库账号类型，取值：- `Super`：高权限账号，一个实例只能创建一个高权限账号，且具备该实例下所有数据库所有权限，可以管理所有普通账号和数据库。- `Normal`：一个实例可以创建多个普通账号，需要手动给普通账号授予特定数据库的权限。', examples=['Normal枚举值：Normal,Super'])],
                      account_desc: Optional[Annotated[str,Field(description='账号的描述信息，描述内容长度为 0~256 个字符。可以包含数字、中文、英文、下划线（_）和中划线（-）。', examples=['这是一段账号的描述信息'])]] = None,
                      account_privileges: Optional[Annotated[list[dict[str, Any]],Field(description='数据库的权限信息。(- 当 `AccountType` 取值为 `Super`时，无需传入该参数，高权限账号默认具备该实例下所有数据库的所有权限。- 当 `AccountType` 取值为 `Normal` 时，建议传入该参数，为普通账号授予指定数据库的指定权限。不设置时，该账号不具备任何数据库的任何权限。)', examples=[''])]] = None) -> dict[str, Any]:
    """调用 CreateDBAccount 接口创建管理数据库的账号。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        account_name (str): 数据库账号名称。账号名称需满足以下要求：
            * 名称唯一，且长度在 2~32 个字符内。
            * 由字母、数字、中划线（-）、下划线（_）组成。
            * 以字母开头，以字母或数字结尾。
            * 名称内不能包含某些禁用词，详细信息请参见[禁用关键词](https://www.volcengine.com/docs/6357/79942)。
            示例值：testuser1
        account_password (str): 数据库账号的密码。账号密码需满足以下要求：
            * 只能包含大小写字母、数字及以下特殊字符 ``~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/``。
            * 长度需在 8~32 个字符内。
            * 至少包含大写字母、小写字母、数字或特殊字符中的 3 种。
            示例值：Test****
        account_type (str): 数据库账号类型，取值：
            - `Super`：高权限账号，一个实例只能创建一个高权限账号，且具备该实例下所有数据库所有权限，可以管理所有普通账号和数据库。
            - `Normal`：一个实例可以创建多个普通账号，需要手动给普通账号授予特定数据库的权限。
            示例值：Normal
            枚举值：Normal,Super
        account_desc (str, optional): 账号的描述信息，描述内容长度为 0~256 个字符。可以包含数字、中文、英文、下划线（_）和中划线（-）。
            示例值：这是一段账号的描述信息
        account_privileges (list[dict[str, Any]], optional): 数据库的权限信息。
            (
            - 当 `AccountType` 取值为 `Super`时，无需传入该参数，高权限账号默认具备该实例下所有数据库的所有权限。
            - 当 `AccountType` 取值为 `Normal` 时，建议传入该参数，为普通账号授予指定数据库的指定权限。不设置时，该账号不具备任何数据库的任何权限。
            )
    """
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
    description="为实例创建数据库"
)
def create_database(instance_id: str,
                    db_name: Annotated[str, Field(description='数据库名称。命名规则：* 名称唯一。以字母开头，以字母或数字结尾。长度在 2~64 个字符内。* 由字母、数字、下划线（_）或中划线（-）组成。* 名称内不能包含某些预留字，详细信息请参见[禁用关键词](https://www.volcengine.com/docs/6357/79942)。', examples=['testdb1'])],
                    character_set_name: Optional[Annotated[str,Field(description='数据库字符集：* `utf8mb4`（默认）* `utf8`* `latin1`* `ascii`', examples=['utf8mb4枚举值：ascii,latin1,utf8,utf8mb4'])]] = 'utf8mb4',
                    databases_privileges: Optional[Annotated[list[dict[str, Any]],Field(description='数据库的权限信息。', examples=[''])]] = None,
                    db_desc: Optional[Annotated[str,Field(description='数据库的描述信息，描述内容长度为 0~256 个字符。可以包含数字、中文、英文、下划线（_）和中划线（-）。', examples=['这是一段数据库的描述信息'])]] = None) -> dict[str, Any]:
    """调用 CreateDatabase 接口为实例创建数据库。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        db_name (str): 数据库名称。命名规则：
            * 名称唯一。以字母开头，以字母或数字结尾。长度在 2~64 个字符内。
            * 由字母、数字、下划线（_）或中划线（-）组成。
            * 名称内不能包含某些预留字，详细信息请参见[禁用关键词](https://www.volcengine.com/docs/6357/79942)。
            示例值：testdb1
        character_set_name (str, optional): 数据库字符集：
            * `utf8mb4`（默认）
            * `utf8`
            * `latin1`
            * `ascii`
            示例值：utf8mb4
            枚举值：ascii,latin1,utf8,utf8mb4
        databases_privileges (list[dict[str, Any]], optional): 数据库的权限信息。
        db_desc (str, optional): 数据库的描述信息，描述内容长度为 0~256 个字符。可以包含数字、中文、英文、下划线（_）和中划线（-）。
            示例值：这是一段数据库的描述信息
    """
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
    description="删除数据库账号"
)
def delete_db_account(instance_id: str,
                      account_name: Annotated[str, Field(description='数据库账号名称。(您可以调用DescribeDBAccounts接口查询数据库账号的信息，包括账号名称。)', examples=['testuser'])]) -> dict[str, Any]:
    """调用 DeleteDBAccount 接口删除数据库账号。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        account_name (str): 数据库账号名称。
            (
            您可以调用DescribeDBAccounts接口查询数据库账号的信息，包括账号名称。
            )
            示例值：testuser
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_account(req)
    return resp.to_dict()


@mcp_server.tool(
    description="删除实例的数据库"
)
def delete_database(instance_id: str,
                    db_name: Annotated[str, Field(description='数据库名称。(您可以调用DescribeDatabases接口查询数据库的信息，包括数据库名称。)', examples=['testdb1'])]) -> dict[str, Any]:
    """调用 DeleteDatabase 接口删除实例的数据库。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        db_name (str): 数据库名称。
            (
            您可以调用DescribeDatabases接口查询数据库的信息，包括数据库名称。
            )
            示例值：testdb1
    """
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_database(req)
    return resp.to_dict()
