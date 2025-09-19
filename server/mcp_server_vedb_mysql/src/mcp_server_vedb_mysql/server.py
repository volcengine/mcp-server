#!/usr/bin/env python3
import argparse
import logging
import os
import time
from pydantic import Field
from typing import Final, Any, Literal

import volcenginesdkcore
import volcenginesdkvedbm
from mcp.server.fastmcp import FastMCP
from mcp_server_vedb_mysql.config import load_config

openapi_cli = None

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/mcp.vedbmysql.log"
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("VeDB MySQL MCP Server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))


@mcp.tool(
    description="Retrieve a list of all VeDB MySQL instances for the user, including a batch of instance IDs and basic information",
)
def list_vedb_mysql_instances(
    # query: Optional[str] = None
) -> dict[str, Any]:
    logger.info(f"list_vedb_mysql_instances")
    batch_size: Final = 100

    req = volcenginesdkvedbm.models.DescribeDBInstancesRequest(
        page_size=batch_size,
        page_number=1,
    )
    rsp = volcenginesdkvedbm.models.DescribeDBInstancesResponse(instances=[])

    try:
        while True:
            rsp_page = openapi_cli.describe_db_instances(req)
            rsp.instances.extend(rsp_page.instances)
            if len(rsp_page.instances) < batch_size:
                break
            req.page_number += 1

        rsp.total = len(rsp.instances)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}


@mcp.tool(
    description="Retrieve detailed information about a specific VeDB MySQL instance",
)
def describe_vedb_mysql_detail(
    instance_id: str
) -> dict[str, Any]:
    logger.info("describe_vedb_mysql_detail")

    req = volcenginesdkvedbm.models.DescribeDBInstanceDetailRequest(instance_id=instance_id)
    try:
        rsp = openapi_cli.describe_db_instance_detail(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}


@mcp.tool(
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


@mcp.tool(
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


@mcp.tool(
    description="Modify a specific VeDB MySQL instance's alias",
)
def modify_vedb_mysql_instance_alias(
        instance_id: str, new_alias: str
) -> dict[str, Any]:
    logger.info("modify_vedb_mysql_instance_alias")

    req = volcenginesdkvedbm.models.ModifyDBInstanceNameRequest(
        instance_id=instance_id,
        instance_new_name=new_alias,
    )

    try:
        openapi_cli.modify_db_instance_name(req)
        return {"success": "true"}

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}


@mcp.tool(
    description="Create a Network AllowList for VeDB MySQL",
)
def create_vedb_mysql_allowlist(
        name: str,
        contents: str = "0.0.0.0/0,127.0.0.1"
) -> str:
    req = volcenginesdkvedbm.models.CreateAllowListRequest(
        allow_list=contents,
        allow_list_name=name,
    )
    return "allow_list_id: " + openapi_cli.create_allow_list(req).allow_list_id


@mcp.tool(
    description="Bind a Network AllowList to VeDB MySQL instances",
)
def bind_allowlist_to_vedb_mysql_instances(
        allow_list_id: str,
        instances_id: set[str],
) -> str:
    req = volcenginesdkvedbm.models.AssociateAllowListRequest(
        allow_list_ids=[allow_list_id],
        instance_ids=list(instances_id),
    )
    openapi_cli.associate_allow_list(req)
    return "bind success"


@mcp.tool(
    description="Create a VeDB MySQL instance",
)
def create_vedb_mysql_instance(
    instance_alias: str,
    zone_id: str,
    vpc_id: str,
    subnet_id: str = "<可参考现有实例属性>",
    db_version: Literal["MySQL_8_0", "MySQL_5_7"] = "MySQL_8_0",
    lower_case_table_names: bool = False,
) -> dict[str, Any]:
    logger.info("create_vedb_mysql_instance")

    req = volcenginesdkvedbm.models.CreateDBInstanceRequest(
        charge_type="PostPaid",
        instance_name=instance_alias,
        db_engine_version=db_version,
        db_minor_version="3.0" if db_version == "MySQL_8_0" else "2.0",
        node_spec="vedb.mysql.g4.large",
        node_number=2,
        lower_case_table_names="0" if lower_case_table_names else "1",
        vpc_id=vpc_id,
        subnet_id=subnet_id,
        zone_ids=zone_id,
        tags=[volcenginesdkvedbm.TagForCreateDBInstanceInput(key="Source", value="CreateFromMCP")],
    )

    instance_id = openapi_cli.create_db_instance(req).instance_id

    # wait running
    start_at = time.time()
    running = False
    while time.time() - start_at < 20*60:
        rsp = describe_vedb_mysql_detail(instance_id=instance_id)
        if 'error' not in rsp and rsp['instance_detail']['instance_status'] == 'Running':
            running = True
            break
        time.sleep(3)

    rsp = {
        "instance_id": instance_id,
        "suggests": ["Create a network AllowList", "Bind AllowList for " + instance_id]
    }
    if not running:
        rsp["suggests"] = "Wait for instance creating finish (Running status)"
    return rsp


def main():
    parser = argparse.ArgumentParser(description="Run the VeDB MySQL MCP Server")
    parser.add_argument("--config", "-c", help="Path to config file")  # 新增config参数
    parser.add_argument("--transport", "-t", choices=["sse", "stdio"], default="stdio")
    
    args = parser.parse_args()
    try:
        # 修改配置加载方式
        if args.config:
            config = load_config(args.config)
        else:
            config = load_config()
        # Initialize VeDB MySQL service
        logger.info(
            f"Initialized VeDB MySQL Base service"
        )

        # Initialize SDK
        configuration = volcenginesdkcore.Configuration()
        configuration.host = config.endpoint
        configuration.region = config.region
        configuration.ak = config.access_key_id
        configuration.sk = config.access_key_secret
        configuration.zone = config.zone

        global openapi_cli
        openapi_cli = volcenginesdkvedbm.VEDBMApi(volcenginesdkcore.ApiClient(
            configuration, "X-VedbCli-Source", "mcp"))

        # Run the MCP server
        logger.info(
            f"Starting VeDB MySQL MCP Server with {args.transport} transport"
        )
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting VeDB MySQL MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
