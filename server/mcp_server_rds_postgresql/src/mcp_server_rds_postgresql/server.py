import os
import asyncio
from typing import Optional
from pydantic import Field
import logging
import argparse
from typing import Any, Literal
from mcp.server.fastmcp import FastMCP
from mcp_server_rds_postgresql.resource.rds_postgresql_resource import RDSPostgreSQLSDK

# 初始化MCP服务
mcp_server = FastMCP("rds_postgresql_mcp_server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))
logger = logging.getLogger("rds_postgresql_mcp_server")

rds_postgresql_resource = RDSPostgreSQLSDK(
    region=os.getenv('VOLCENGINE_REGION'), ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY'), host=os.getenv('VOLCENGINE_ENDPOINT')
)

from typing import List, Dict, Any, Optional

@mcp_server.tool(
    name="describe_db_instances",
    description="查询RDS PostgreSQL实例列表"
)
def describe_db_instances(
        page_number: int = 1,
        page_size: int = 10,
        instance_id: str = None,
        instance_name: str = None,
        instance_status: str = None,
        db_engine_version: str = None,
        create_time_start: str = None,
        create_time_end: str = None,
        zone_id: str = None,
        charge_type: str = None,
        project_name: str = None,
        tag_filters: List[Dict[str, str]] = None
) -> dict[str, Any]:
    """
    查询RDS PostgreSQL实例列表

    Args:
        page_number (int, optional): 当前页页码，取值最小为1，默认值为1
        page_size (int, optional): 每页记录数，最小值为1，最大值不超过1000，默认值为10
        instance_id (str, optional): 实例ID
        instance_name (str, optional): 实例名称
        instance_status (str, optional): 实例状态，如Running、Creating等
        db_engine_version (str, optional): 兼容版本，如PostgreSQL_15、PostgreSQL_16
        create_time_start (str, optional): 查询创建实例的开始时间
        create_time_end (str, optional): 查询创建实例的结束时间
        zone_id (str, optional): 实例所属可用区
        charge_type (str, optional): 计费类型，如PostPaid、PrePaid
        tag_filters (List[Dict[str, str]], optional): 用于查询筛选的标签键值对数组
        project_name (str, optional): 项目名称
    """
    req = {
        "instance_id": instance_id,
        "instance_name": instance_name,
        "instance_status": instance_status,
        "db_engine_version": db_engine_version,
        "create_time_start": create_time_start,
        "create_time_end": create_time_end,
        "zone_id": zone_id,
        "charge_type": charge_type,
        "tag_filters": tag_filters,
        "project_name": project_name,
        "page_number": page_number,
        "page_size": page_size
    }

    req = {k: v for k, v in req.items() if v is not None}

    if tag_filters is not None:
        for filter_item in tag_filters:
            if not isinstance(filter_item, dict) or 'Key' not in filter_item:
                raise ValueError("TagFilters中的每个元素必须是包含Key字段的字典")

    resp = rds_postgresql_resource.describe_db_instances(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_db_instance_detail", description="查询RDS PostgreSQL实例详情")
def describe_db_instance_detail(instance_id: str) -> dict[str, Any]:
    """查询RDS PostgreSQL实例详情
       Args:
           instance_id (str): 实例ID
   """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_db_instance_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_databases",
    description="获取指定RDS PostgreSQL实例的数据库列表"
)
def describe_databases(
        instance_id: str,
        page_number: int = 1,
        page_size: int = 10,
        db_name: str = None,
) -> dict[str, Any]:
    """
    获取指定RDS PostgreSQL实例的数据库列表

    Args:
        page_number (int, optional): 当前页页码，取值最小为1，默认值为1
        page_size (int, optional): 每页记录数，最小值为1，最大值不超过1000，默认值为10
        instance_id (str): 实例ID
        db_name (str, optional): 数据库名称
    """
    req = {
        "page_number": page_number,
        "page_size": page_size,
        "db_name": db_name,
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_databases(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_accounts",
    description="获取指定RDS PostgreSQL实例的账号列表"
)
def describe_db_accounts(
        instance_id: str,
        page_number: int = 1,
        page_size: int = 10,
        account_name: str = None,
) -> dict[str, Any]:
    """
    获取指定RDS PostgreSQL实例的账号列表

    Args:
        page_number (int, optional): 当前页页码，取值最小为1，默认值为1
        page_size (int, optional): 每页记录数，最小值为1，最大值不超过1000，默认值为10
        instance_id (str): 实例ID
        account_name (str, optional): 账号名称，支持模糊查询
    """
    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "page_number": page_number,
        "page_size": page_size
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_db_accounts(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_schemas",
    description="获取指定RDS PostgreSQL实例的schema列表"
)
def describe_schemas(
        instance_id: str,
        page_number: int = 1,
        page_size: int = 10,
        db_name: str = None,
) -> dict[str, Any]:
    """
    获取指定RDS PostgreSQL实例的schema列表

    Args:
        page_number (int, optional): 当前页页码，取值最小为1，默认值为1
        page_size (int, optional): 每页记录数，最小值为1，最大值不超过1000，默认值为10
        instance_id (str): 实例ID
        db_name (str, optional): 数据库名称
    """
    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "page_number": page_number,
        "page_size": page_size
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_schemas(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_parameters",
    description="获取指定RDS PostgreSQL实例参数列表"
)
def describe_db_instance_parameters(
        instance_id: str,
        parameter_name: str = None,
) -> dict[str, Any]:
    """
    获取指定RDS PostgreSQL实例参数列表

    Args:
        instance_id (str): 实例ID
        parameter_name (str, optional): 参数名称，支持模糊查询
    """
    req = {
        "instance_id": instance_id,
        "parameter_name": parameter_name
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_db_instance_parameters(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_allow_lists",
    description="获取RDS PostgreSQL指定地域下的白名单列表"
)
def describe_allow_lists(
        region_id: str,
        instance_id: str = None,
) -> dict[str, Any]:
    """
    获取RDS PostgreSQL指定地域下的白名单列表

    Args:
        region_id (str): 地域ID
        instance_id (str, optional): 实例ID
    """
    req = {
        "region_id": region_id,
        "instance_id": instance_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_allow_lists(req)

    return resp.to_dict()

@mcp_server.tool(
    name="describe_allow_list_detail",
    description="获取RDS PostgreSQL白名单详情"
)
def describe_allow_list_detail(
        allow_list_id: str
) -> dict[str, Any]:
    """
    获取RDS PostgreSQL白名单详情

    Args:
        allow_list_id (str): 白名单的 ID
    """
    req = {
        "allow_list_id": allow_list_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_allow_list_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_backups",
    description="获取指定RDS PostgreSQL实例备份列表"
)
def describe_backups(
        instance_id: str,
        page_number: int = 1,
        page_size: int = 10,
        backup_id: str = None,
        backup_start_time: str = None,
        backup_end_time: str = None,
        backup_status: str = None,
        backup_type: str = None,
) -> dict[str, Any]:
    """
    获取指定RDS PostgreSQL实例备份列表

    Args:
        page_number (int, optional): 当前页页码，取值最小为1，默认值为1
        page_size (int, optional): 每页记录数，最小值为1，最大值不超过1000，默认值为10
        instance_id (str): 实例ID
        backup_id (str, optional): 备份ID
        backup_start_time (str, optional): 备份创建最早时间，格式为 yyyy-MM-ddTHH:mm:ss.sssZ（UTC 时间）
        backup_end_time (str, optional): 备份创建最晚时间，格式为 yyyy-MM-ddTHH:mm:ss.sssZ（UTC 时间）
        backup_status (str, optional): 备份状态，枚举值：
            - Success: 备份成功
            - Failed: 备份失败
            - Running: 备份中
        backup_type (str, optional): 备份类型，枚举值：
            - Full: 全量备份
            - Increment: 增量备份
    """
    req = {
        "instance_id": instance_id,
        "backup_id": backup_id,
        "backup_start_time": backup_start_time,
        "backup_end_time": backup_end_time,
        "backup_status": backup_status,
        "backup_type": backup_type,
        "page_number": page_number,
        "page_size": page_size,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_backups(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_backup_policy",
    description="获取指定RDS PostgreSQL实例备份策略"
)
def describe_backup_policy(
        instance_id: str
) -> dict[str, Any]:
    """
    获取指定RDS PostgreSQL实例备份策略

    Args:
        instance_id (str): 实例ID
    """
    req = {
        "instance_id": instance_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_backup_policy(req)
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_instance",
    description="创建RDS PostgreSQL实例"
)
def create_db_instance(
        vpc_id: str,
        subnet_id: str,
        primary_zone: str,
        secondary_zone: str,
        read_only_zone: str,
        db_engine_version: str = "PostgreSQL_14",
        storage_space: int = 100,
        storage_type: str = "LocalSSD",
        instance_name: Optional[str] = None,
        project_name: Optional[str] = None,
        tags: Optional[list[dict]] = None,
        primary_spec: str = "rds.postgres.1c2g",
        secondary_spec: str = "rds.postgres.1c2g",
        read_only_count: int = 0,
        read_only_spec: str = "rds.postgres.1c2g",
        charge_type: str = "PostPaid",
        auto_renew: Optional[bool] = None,
        period_unit: Optional[str] = None,
        period: Optional[int] = None,
        number: Optional[int] = None,
) -> dict[str, Any]:
    """
    创建RDS PostgreSQL实例
    
    Args:
        vpc_id (str): VPC ID
        subnet_id (str): 子网 ID
        db_engine_version (str): 数据库引擎版本，默认值为 PostgreSQL_14
        storage_space (int, optional): 存储空间，单位为 GB，默认值为 100
        storage_type (str): 存储类型，默认值为 LocalSSD
        instance_name (str, optional): 实例名称
        project_name (str, optional): 项目名称
        tags (list[dict], optional): 标签列表
        primary_zone (str): 主节点可用区
        primary_spec (str): 主节点规格，默认值为 rds.postgres.1c2g
        secondary_zone (str): 备节点可用区
        secondary_spec (str): 备节点规格，默认值为 rds.postgres.1c2g
        read_only_zone (str): 只读节点可用区
        read_only_spec (str): 只读节点规格，默认值为 rds.postgres.1c2g
        read_only_count (int, optional): 只读节点数量，默认值为 0
        charge_type (str): 计费类型，默认值为 PostPaid
        auto_renew (bool, optional): 是否自动续费，默认值为 False
        period_unit (str, optional): 预付费场景下的购买周期，默认值为 Month
        period (int, optional): 预付费场景下的购买时长，默认值为 1
        number (int, optional): 实例购买数量。可取 1~20 之间的整数值，默认值为 1
    """
    node_info = []

    node_info.append({
        "NodeType": "Primary",
        "ZoneId": primary_zone,
        "NodeSpec": primary_spec
    })
    node_info.append({
        "NodeType": "Secondary",
        "ZoneId": secondary_zone,
        "NodeSpec": secondary_spec
    })
    for i in range(read_only_count):
        node_info.append({
            "NodeType": "ReadOnly",
            "ZoneId": read_only_zone,
            "NodeSpec": read_only_spec
        })
    
    data = {
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "db_engine_version": db_engine_version,
        "storage_space": storage_space,
        "storage_type": storage_type,
        "instance_name": instance_name,
        "project_name": project_name,
        "tags": tags,
        "node_info": node_info,
        "charge_info": {
            "ChargeType": charge_type,
            "AutoRenew": auto_renew,
            "PeriodUnit": period_unit,
            "Period": period,
            "Number": number,
        },
    }

    resp = rds_postgresql_resource.create_db_instance(data)
    return resp.to_dict()

@mcp_server.tool(
    name="create_database",
    description="创建RDS PostgreSQL数据库"
)
def create_database(
        instance_id: str,
        db_name: str,
        character_set_name: Optional[str] = None,
        c_type: Optional[str] = None,
        collate: Optional[str] = None,
        owner: Optional[str] = None,
) -> dict[str, Any]:
    """
    创建RDS PostgreSQL数据库
    
    Args:
        instance_id (str): 实例 ID
        db_name (str): 数据库名称
        character_set_name (str, optional): 数据库字符集，目前支持的字符集包含：utf8（默认）、latin1、ascii
        c_type (str, optional): 字符分类，取值范围： C（默认）、C.UTF-8、en_US.utf8、zh_CN.utf8 和 POSIX
        collate (str, optional): 排序规则，取值范围：C（默认）、C.UTF-8、en_US.utf8、zh_CN.utf8 和 POSIX
        owner (str, optional): 数据库的 owner
    """
    data = {
        "instance_id": instance_id,
        "db_name": db_name,
        "character_set_name": character_set_name,
        "c_type": c_type,
        "collate": collate,
        "owner": owner,
    }

    if not instance_id:
        raise ValueError("instance_id是必选参数")
    if not db_name:
        raise ValueError("db_name是必选参数")
    
    valid_charsets = {"utf8", "latin1", "ascii"}
    if character_set_name and character_set_name not in valid_charsets:
        raise ValueError(f"无效的字符集: {character_set_name}，支持的字符集为: {', '.join(valid_charsets)}")
    
    valid_c_types = {"C", "C.UTF-8", "en_US.utf8", "zh_CN.utf8", "POSIX"}
    if c_type and c_type not in valid_c_types:
        raise ValueError(f"无效的字符分类: {c_type}，支持的字符分类为: {', '.join(valid_c_types)}")

    valid_collates = {"C", "C.UTF-8", "en_US.utf8", "zh_CN.utf8", "POSIX"}
    if collate and collate not in valid_collates:
        raise ValueError(f"无效的排序规则: {collate}，支持的排序规则为: {', '.join(valid_collates)}")

    resp = rds_postgresql_resource.create_database(data)

    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_account",
    description="创建RDS PostgreSQL数据库账号"
)
def create_db_account(
        instance_id: str,
        account_name: str,
        account_password: str,
        account_type: str = "Normal",
        account_privileges: Optional[str] = None,
) -> dict[str, Any]:
    """
    创建RDS PostgreSQL数据库账号
    
    Args:
        instance_id (str): 实例 ID
        account_name (str): 数据库账号名称。账号名称的设置规则如下：
            - 长度 2~63 个字符
            - 由字母、数字、下划线（_）或中划线（-）组成
            - 以字母开头，字母或数字结尾
            - 不能以 pg_ 开头
            - 不能使用保留关键字，所有被禁用的关键词请参见 [禁用关键词](https://www.volcengine.com/docs/6438/80243)
        account_password (str): 数据库账号的密码。数据库账号密码的设置规则如下：
            - 长度为 8~32 个字符
            - 由大写字母、小写字母、数字、特殊字符中的任意三种组成
            - 特殊字符为 !@#$%^*()&_+-=
        account_type (str, optional): 数据库账号类型，取值范围如下：
            - Super：高权限账号
            - Normal：普通账号
            - InstanceReadOnly：实例只读账号
        account_privileges (str, optional): 账号权限信息。多个权限中间以英文逗号（,）分隔。取值：
            - Login：登录权限
            - Inherit：继承权限
            - CreateRole：创建角色权限
            - CreateDB：创建数据库权限
    """
    if not instance_id:
        raise ValueError("instance_id是必选参数")
    if not account_name:
        raise ValueError("account_name是必选参数")
    if not account_password:
        raise ValueError("account_password是必选参数")

    import re
    if account_name.startswith("pg_"):
        raise ValueError("账号名称不能以 pg_ 开头")
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{0,61}[a-zA-Z0-9]$', account_name):
        raise ValueError(
            "账号名称不符合命名规则：长度为2~63个字符，以字母开头，以字母或数字结尾，由字母、数字、下划线或中划线组成，不能使用保留关键字，所有被禁用的关键词请参见 [禁用关键词](https://www.volcengine.com/docs/6438/80243)")

    if not (8 <= len(account_password) <= 32):
        raise ValueError("密码长度必须为8~32个字符")

    conditions = [
        bool(re.search(r'[A-Z]', account_password)),  # 大写字母
        bool(re.search(r'[a-z]', account_password)),  # 小写字母
        bool(re.search(r'[0-9]', account_password)),  # 数字
        bool(re.search(r'[!@#$%^&*()_+\-=,.&?|/]', account_password))  # 特殊字符
    ]

    if sum(conditions) < 3:
        raise ValueError("密码必须包含大写字母、小写字母、数字、特殊字符中的至少三种")

    valid_account_types = {"Super", "Normal", "InstanceReadOnly"}
    if account_type and account_type not in valid_account_types:
        raise ValueError(f"无效的账号类型: {account_type}，支持的账号类型为: {', '.join(valid_account_types)}")
    
    if account_privileges:
        valid_privileges = {"Login", "Inherit", "CreateRole", "CreateDB"}
        privileges = set(account_privileges.split(','))
        if not privileges.issubset(valid_privileges):
            raise ValueError(f"无效的权限信息: {account_privileges}，支持的权限信息为: {', '.join(valid_privileges)}")

    data = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_password": account_password,
        "account_type": account_type,
        "account_privileges": account_privileges,
    }

    resp = rds_postgresql_resource.create_db_account(data)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_schema",
    description="创建RDS PostgreSQL数据库Schema"
)
def create_schema(
        instance_id: str,
        db_name: str,
        schema_name: str,
        owner: str,
) -> dict[str, Any]:
    """
    创建RDS PostgreSQL数据库Schema
    
    Args:
        instance_id (str): 实例 ID
        db_name (str): 数据库名称
        schema_name (str): Schema 名称
            - 长度 2~63 个字符
            - 由字母、数字、下划线（_）或中划线（-）组成
            - 以字母开头，字母或数字结尾
            - 不能使用保留关键字，所有被禁用的关键词请参见[禁用关键词](https://www.volcengine.com/docs/6438/80243)
            - 不能以 pg_ 开头
        owner (str): Schema 的 owner
    """
    if not instance_id:
        raise ValueError("instance_id是必选参数")
    if not db_name:
        raise ValueError("db_name是必选参数")
    if not schema_name:
        raise ValueError("schema_name是必选参数")
    if not owner:
        raise ValueError("owner是必选参数")

    if schema_name.startswith("pg_"):
        raise ValueError("Schema 名称不能以 pg_ 开头")

    import re
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{0,61}[a-zA-Z0-9]$', schema_name):
        raise ValueError(
            "Schema 名称不符合命名规则：长度为2~63个字符，以字母开头，以字母或数字结尾，由字母、数字、下划线或中划线组成，不能使用保留关键字，所有被禁用的关键词请参见 [禁用关键词](https://www.volcengine.com/docs/6438/80243)")

    data = {
        "instance_id": instance_id,
        "db_name": db_name,
        "schema_name": schema_name,
        "owner": owner,
    }

    resp = rds_postgresql_resource.create_schema(data)
    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the RDS PostgreSQL MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["streamable-http", "stdio"],
        default="stdio",
        help="Transport protocol to use (streamable-http or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting RDS PostgreSQL MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting RDS PostgreSQL MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()