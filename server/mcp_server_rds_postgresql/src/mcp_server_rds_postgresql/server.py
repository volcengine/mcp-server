import os
import asyncio
import re
from pydantic import Field
import logging
import argparse
from typing import Optional, List, Dict, Any, Literal
from mcp.server.fastmcp import FastMCP
from mcp_server_rds_postgresql.resource.rds_postgresql_resource import RDSPostgreSQLSDK

# Initialize the MCP service
mcp_server = FastMCP("rds_postgresql_mcp_server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))
logger = logging.getLogger("rds_postgresql_mcp_server")

rds_postgresql_resource = RDSPostgreSQLSDK(
    region=os.getenv('VOLCENGINE_REGION'), ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY'), host=os.getenv('VOLCENGINE_ENDPOINT')
)

@mcp_server.tool(
    name="describe_db_instances",
    description="Query the list of RDS PostgreSQL instances"
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
    Query the list of RDS PostgreSQL instances

    Args:
        page_number (int, optional): The current page number, with a minimum value of 1. The default value is 1.
        page_size (int, optional): The number of records per page, with a minimum value of 1 and a maximum value not exceeding 1000. The default value is 10.
        instance_id (str, optional): The instance ID.
        instance_name (str, optional): The instance name.
        instance_status (str, optional): The instance status, such as Running, Creating, etc.
        db_engine_version (str, optional): The compatible version, such as PostgreSQL_15, PostgreSQL_16.
        create_time_start (str, optional): The start time for querying instance creation.
        create_time_end (str, optional): The end time for querying instance creation.
        zone_id (str, optional): The availability zone to which the instance belongs.
        charge_type (str, optional): The billing type, such as PostPaid, PrePaid.
        tag_filters (List[Dict[str, str]], optional): An array of tag key - value pairs used for query filtering.
        project_name (str, optional): The project name.
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
                raise ValueError("Each element in TagFilters must be a dictionary containing the Key field")

    resp = rds_postgresql_resource.describe_db_instances(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_db_instance_detail", description="Query the details of an RDS PostgreSQL instance")
def describe_db_instance_detail(instance_id: str) -> dict[str, Any]:
    """Query the details of an RDS PostgreSQL instance
       Args:
           instance_id (str): The instance ID
   """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_db_instance_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_databases",
    description="Get the list of databases for a specified RDS PostgreSQL instance"
)
def describe_databases(
        instance_id: str,
        page_number: int = 1,
        page_size: int = 10,
        db_name: str = None,
) -> dict[str, Any]:
    """
    Get the list of databases for a specified RDS PostgreSQL instance

    Args:
        page_number (int, optional): The current page number, with a minimum value of 1. The default value is 1.
        page_size (int, optional): The number of records per page, with a minimum value of 1 and a maximum value not exceeding 1000. The default value is 10.
        instance_id (str): The instance ID.
        db_name (str, optional): The database name.
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
    description="Get the list of accounts for a specified RDS PostgreSQL instance"
)
def describe_db_accounts(
        instance_id: str,
        page_number: int = 1,
        page_size: int = 10,
        account_name: str = None,
) -> dict[str, Any]:
    """
    Get the list of accounts for a specified RDS PostgreSQL instance

    Args:
        page_number (int, optional): The current page number, with a minimum value of 1. The default value is 1.
        page_size (int, optional): The number of records per page, with a minimum value of 1 and a maximum value not exceeding 1000. The default value is 10.
        instance_id (str): The instance ID.
        account_name (str, optional): The account name, supporting fuzzy queries.
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
    description="Get the list of schemas for a specified RDS PostgreSQL instance"
)
def describe_schemas(
        instance_id: str,
        page_number: int = 1,
        page_size: int = 10,
        db_name: str = None,
) -> dict[str, Any]:
    """
    Get the list of schemas for a specified RDS PostgreSQL instance

    Args:
        page_number (int, optional): The current page number, with a minimum value of 1. The default value is 1.
        page_size (int, optional): The number of records per page, with a minimum value of 1 and a maximum value not exceeding 1000. The default value is 10.
        instance_id (str): The instance ID.
        db_name (str, optional): The database name.
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
    description="Get the list of parameters for a specified RDS PostgreSQL instance"
)
def describe_db_instance_parameters(
        instance_id: str,
        parameter_name: str = None,
) -> dict[str, Any]:
    """
    Get the list of parameters for a specified RDS PostgreSQL instance

    Args:
        instance_id (str): The instance ID.
        parameter_name (str, optional): The parameter name, supporting fuzzy queries.
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
    description="Get RDS PostgreSQL specified region's white list"
)
def describe_allow_lists(
        region_id: str,
        instance_id: str = None,
) -> dict[str, Any]:
    """
    Get RDS PostgreSQL specified region's white list

    Args:
        region_id (str): Region ID
        instance_id (str, optional): Instance ID
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
    description="Get RDS PostgreSQL white list detail"
)
def describe_allow_list_detail(
        allow_list_id: str
) -> dict[str, Any]:
    """
    Get RDS PostgreSQL white list detail

    Args:
        allow_list_id (str): White list ID
    """
    req = {
        "allow_list_id": allow_list_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_allow_list_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_backups",
    description="Get RDS PostgreSQL instance backup list"
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
    Get RDS PostgreSQL instance backup list

    Args:
        page_number (int, optional): Current page number, with a minimum value of 1, default value is 1
        page_size (int, optional): Number of records per page, with a minimum value of 1, maximum value not exceeding 1000, default value is 10
        instance_id (str): Instance ID
        backup_id (str, optional): Backup ID
        backup_start_time (str, optional): Backup created earliest time, format is yyyy-MM-ddTHH:mm:ss.sssZ（UTC time）
        backup_end_time (str, optional): Backup created latest time, format is yyyy-MM-ddTHH:mm:ss.sssZ（UTC time）
        backup_status (str, optional): Backup status, enum value：
            - Success: Backup success
            - Failed: Backup failed
            - Running: Backup in progress
        backup_type (str, optional): Backup type, enum value：
            - Full: Full backup
            - Increment: Incremental backup
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
    description="Get RDS PostgreSQL instance backup policy"
)
def describe_backup_policy(
        instance_id: str
) -> dict[str, Any]:
    """
    Get RDS PostgreSQL instance backup policy

    Args:
        instance_id (str): Instance ID
    """
    req = {
        "instance_id": instance_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_postgresql_resource.describe_backup_policy(req)
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_instance",
    description="Create RDS PostgreSQL instance"
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
    Create RDS PostgreSQL instance
    
    Args:
        vpc_id (str): VPC ID
        subnet_id (str): Subnet ID
        db_engine_version (str): Database engine version, default value is PostgreSQL_14
        storage_space (int, optional): Storage space in GB, default value is 100
        storage_type (str): Storage type, default value is LocalSSD
        instance_name (str, optional): Instance name
        project_name (str, optional): Project name
        tags (list[dict], optional): Tag list
        primary_zone (str): Primary node availability zone
        primary_spec (str): Primary node specification, default value is rds.postgres.1c2g
        secondary_zone (str): Secondary node availability zone
        secondary_spec (str): Secondary node specification, default value is rds.postgres.1c2g
        read_only_zone (str): Read - only node availability zone
        read_only_spec (str): Read - only node specification, default value is rds.postgres.1c2g
        read_only_count (int, optional): Number of read - only nodes, default value is 0
        charge_type (str): Billing type, default value is PostPaid
        auto_renew (bool, optional): Whether to auto - renew, default value is False
        period_unit (str, optional): Purchase cycle in prepaid scenarios, default value is Month
        period (int, optional): Purchase duration in prepaid scenarios, default value is 1
        number (int, optional): Number of instances to purchase. Can take integer values between 1 and 20, default value is 1
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
    description="Create RDS PostgreSQL database"
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
    Create RDS PostgreSQL database
    
    Args:
        instance_id (str): Instance ID
        db_name (str): Database name
        character_set_name (str, optional): Database character set. Currently supported character sets include: utf8 (default), latin1, ascii
        c_type (str, optional): Character classification. Valid values: C (default), C.UTF-8, en_US.utf8, zh_CN.utf8, and POSIX
        collate (str, optional): Sorting rule. Valid values: C (default), C.UTF-8, en_US.utf8, zh_CN.utf8, and POSIX
        owner (str, optional): Database owner
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
        raise ValueError("instance_id is a required parameter")
    if not db_name:
        raise ValueError("db_name is a required parameter")
    
    valid_charsets = {"utf8", "latin1", "ascii"}
    if character_set_name and character_set_name not in valid_charsets:
        raise ValueError(f"Invalid character set: {character_set_name}, supported character sets are: {', '.join(valid_charsets)}")
    
    valid_c_types = {"C", "C.UTF-8", "en_US.utf8", "zh_CN.utf8", "POSIX"}
    if c_type and c_type not in valid_c_types:
        raise ValueError(f"Invalid character classification: {c_type}, supported character classifications are: {', '.join(valid_c_types)}")

    valid_collates = {"C", "C.UTF-8", "en_US.utf8", "zh_CN.utf8", "POSIX"}
    if collate and collate not in valid_collates:
        raise ValueError(f"Invalid sorting rule: {collate}, supported sorting rules are: {', '.join(valid_collates)}")

    resp = rds_postgresql_resource.create_database(data)

    if resp is None:
        return {
            "Message": "Success"
        }
    return resp.to_dict()

@mcp_server.tool(
    name="create_db_account",
    description="Create RDS PostgreSQL database account"
)
def create_db_account(
        instance_id: str,
        account_name: str,
        account_password: str,
        account_type: str = "Normal",
        account_privileges: Optional[str] = None,
) -> dict[str, Any]:
    """
    Create RDS PostgreSQL database account
    
    Args:
        instance_id (str): Instance ID
        account_name (str): Database account name. The rules for setting the account name are as follows:
            - 2 to 63 characters in length
            - Consists of letters, numbers, underscores (_), or hyphens (-)
            - Starts with a letter and ends with a letter or number
            - Cannot start with pg_
            - Cannot use reserved keywords. All prohibited keywords can be found in [Prohibited Keywords](https://www.volcengine.com/docs/6438/80243)
        account_password (str): Database account password. The rules for setting the database account password are as follows:
            - 8 to 32 characters in length
            - Consists of any three of uppercase letters, lowercase letters, numbers, and special characters
            - Special characters are !@#$%^*()&_+-=
        account_type (str, optional): Database account type. Valid values are as follows:
            - Super: High - privilege account
            - Normal: Normal account
            - InstanceReadOnly: Instance read - only account
        account_privileges (str, optional): Account permission information. Multiple permissions are separated by English commas (,). Valid values:
            - Login: Login permission
            - Inherit: Inheritance permission
            - CreateRole: Create role permission
            - CreateDB: Create database permission
    """
    if not instance_id:
        raise ValueError("instance_id is a required parameter")
    if not account_name:
        raise ValueError("account_name is a required parameter")
    if not account_password:
        raise ValueError("account_password is a required parameter")

    if account_name.startswith("pg_"):
        raise ValueError("Account name cannot start with pg_")
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{0,61}[a-zA-Z0-9]$', account_name):
        raise ValueError(
            "Account name does not meet the naming rules: 2 to 63 characters in length, starts with a letter, ends with a letter or number, consists of letters, numbers, underscores, or hyphens, and cannot use reserved keywords. All prohibited keywords can be found in [Prohibited Keywords](https://www.volcengine.com/docs/6438/80243)")

    if not (8 <= len(account_password) <= 32):
        raise ValueError("Password length must be between 8 and 32 characters")

    conditions = [
        bool(re.search(r'[A-Z]', account_password)),  # Uppercase letters
        bool(re.search(r'[a-z]', account_password)),  # Lowercase letters
        bool(re.search(r'[0-9]', account_password)),  # Numbers
        bool(re.search(r'[!@#$%^&*()_+\-=,.&?|/]', account_password))  # Special characters
    ]

    if sum(conditions) < 3:
        raise ValueError("Password must contain at least three of uppercase letters, lowercase letters, numbers, and special characters")

    valid_account_types = {"Super", "Normal", "InstanceReadOnly"}
    if account_type and account_type not in valid_account_types:
        raise ValueError(f"Invalid account type: {account_type}, supported account types are: {', '.join(valid_account_types)}")
    
    if account_privileges:
        valid_privileges = {"Login", "Inherit", "CreateRole", "CreateDB"}
        privileges = set(account_privileges.split(','))
        if not privileges.issubset(valid_privileges):
            raise ValueError(f"Invalid permission information: {account_privileges}, supported permission information are: {', '.join(valid_privileges)}")

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
    description="Create RDS PostgreSQL database Schema"
)
def create_schema(
        instance_id: str,
        db_name: str,
        schema_name: str,
        owner: str,
) -> dict[str, Any]:
    """
    Create RDS PostgreSQL database Schema
    
    Args:
        instance_id (str): Instance ID
        db_name (str): Database name
        schema_name (str): Schema name
            - 2 to 63 characters in length
            - Consists of letters, numbers, underscores (_), or hyphens (-)
            - Starts with a letter and ends with a letter or number
            - Cannot use reserved keywords. All prohibited keywords can be found in [Prohibited Keywords](https://www.volcengine.com/docs/6438/80243)
            - Cannot start with pg_
        owner (str): Schema owner
    """
    if not instance_id:
        raise ValueError("instance_id is a required parameter")
    if not db_name:
        raise ValueError("db_name is a required parameter")
    if not schema_name:
        raise ValueError("schema_name is a required parameter")
    if not owner:
        raise ValueError("owner is a required parameter")

    if schema_name.startswith("pg_"):
        raise ValueError("Schema name cannot start with pg_")

    import re
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{0,61}[a-zA-Z0-9]$', schema_name):
        raise ValueError(
            "Schema name does not meet the naming rules: 2 to 63 characters in length, starts with a letter, ends with a letter or number, consists of letters, numbers, underscores, or hyphens, and cannot use reserved keywords. All prohibited keywords can be found in [Prohibited Keywords](https://www.volcengine.com/docs/6438/80243)")

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