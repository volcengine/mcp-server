#!/usr/bin/env python3
import argparse
import logging
import os
from typing import Dict, Optional, Final, Any

import volcenginesdkcore
import volcenginesdkrdsmysqlv2

from mcp_server_rds_mysql.config import load_config
from mcp.server.fastmcp import FastMCP


openapi_cli = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/mcp.rdsmysql.log"
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("RDS MySQL MCP Server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))


@mcp.tool(
    description="查看用户的 RDS MySQL 实例列表（支持分页查询）",
)
def list_rds_mysql_instances(
    page_number: int = 1,   
    page_size: int = 20    
) -> dict[str, Any]:
    logger.info(f"Querying RDS instances: page={page_number}, size={page_size}")
    MAX_PAGE_SIZE: Final = 100 
    page_size = min(page_size, MAX_PAGE_SIZE) 

    req = volcenginesdkrdsmysqlv2.models.DescribeDBInstancesRequest(
        page_size=page_size,
        page_number=page_number,
    )

    try:
        rsp = openapi_cli.describe_db_instances(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in list_rds_mysql_instances: {str(e)}")
        return {"error": str(e)}


@mcp.tool(
    description="根据指定RDS MySQL 实例ID 查看实例详情",
)
def describe_rds_mysql_detail(
    instance_id: str
) -> dict[str, Any]:
    logger.info("describe_rds_mysql_detail")

    req = volcenginesdkrdsmysqlv2.models.DescribeDBInstanceDetailRequest(instance_id=instance_id)
    try:
        rsp = openapi_cli.describe_db_instance_detail(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe_rds_mysql_detail: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="根据指定RDS MySQL 实例ID 查询实例可升级的内核小版本",
)
def list_rds_mysql_instance_engine_minor_versions(
    instance_id: str
) -> dict[str, Any]:
    logger.info("list_rds_mysql_instance_engine_minor_versions")

    req = volcenginesdkrdsmysqlv2.models.DescribeDBInstanceEngineMinorVersionsRequest(
        instance_id=instance_id
    )

    try:
        rsp = openapi_cli.describe_db_instance_engine_minor_versions(req)      
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe_db_instance_engine_minor_versions: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="根据指定RDS MySQL 实例ID 查看数据库的账号列表（支持分页查询）",
)
def list_rds_mysql_instance_accounts(
    instance_id: str,
    page_number: int = 1,  
    page_size: int = 20   
) -> dict[str, Any]:
    logger.info(f"Querying RDS instances: page={page_number}, size={page_size}")
    MAX_PAGE_SIZE: Final = 100 
    page_size = min(page_size, MAX_PAGE_SIZE)  

    req = volcenginesdkrdsmysqlv2.models.DescribeDBAccountsRequest(
        instance_id=instance_id,
        page_size=page_size,
        page_number=page_number,
    )

    try:
        rsp = openapi_cli.describe_db_accounts(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in list_rds_mysql_instance_accounts: {str(e)}")
        return {"error": str(e)}


@mcp.tool(
    description="根据指定RDS MySQL 实例ID 查看数据库列表（支持分页查询）",
)
def list_rds_mysql_instance_databases(
        instance_id: str,
        page_number: int = 1,    # 当前页码（默认第1页）
        page_size: int = 20     # 每页数量（默认20条，最大建议50）
) -> dict[str, Any]:
    logger.info(f"Querying RDS instances: page={page_number}, size={page_size}")
    MAX_PAGE_SIZE: Final = 100  # 对接API最大限制
    page_size = min(page_size, MAX_PAGE_SIZE)  # 防止超限

    req = volcenginesdkrdsmysqlv2.models.DescribeDatabasesRequest(
        instance_id=instance_id,
        page_size=page_size,
        page_number=page_number,
    )
    rsp = volcenginesdkrdsmysqlv2.models.DescribeDatabasesResponse(databases=[])

    try:
        rsp = openapi_cli.describe_databases(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="根据指定RDS MySQL 实例ID 查询实例参数",
)
def list_rds_mysql_instance_parameters(
    instance_id: str,
) -> dict[str, Any]: 
    req = volcenginesdkrdsmysqlv2.models.DescribeDBInstanceParametersRequest(
        instance_id=instance_id ,
    )

    try:
        rsp = openapi_cli.describe_db_instance_parameters(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in list_rds_mysql_instance_parameters: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询 MySQL 实例的参数模板列表（支持分页查询）",
)
def list_rds_mysql_parameter_templates(
    offset: int = 0,    
    limit: int = 20   
) -> dict[str, Any]:
    MAX_PAGE_SIZE: Final = 100 
    page_size = min(limit, MAX_PAGE_SIZE)  

    req = volcenginesdkrdsmysqlv2.models.ListParameterTemplatesRequest(
        offset=offset,
        limit=limit
    )

    try:
        rsp = openapi_cli.list_parameter_templates(req)   
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in list_rds_mysql_parameter_templates: {str(e)}")
        return {"error": str(e)}


@mcp.tool(
    description="根据参数模版ID 查询指定的参数模板详情",
)
def describe_rds_mysql_parameter_template(
    template_id: str
) -> dict[str, Any]:
    logger.info("describe_rds_mysql_parameter_template")

    req = volcenginesdkrdsmysqlv2.models.DescribeParameterTemplateRequest(
        template_id=template_id
    )
    try:
        rsp = openapi_cli.describe_parameter_template(req)
        return rsp.to_dict()

    except Exception as e:
        logger.error(f"Error in describe_rds_mysql_parameter_template: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="修改 RDS MySQL 实例名称",
)
def modify_rds_mysql_instance_alias(
        instance_id: str, new_alias: str
) -> dict[str, Any]:
    logger.info("modify_rds_mysql_instance_alias")

    req = volcenginesdkrdsmysqlv2.models.ModifyDBInstanceNameRequest(
        instance_id=instance_id,
        instance_new_name=new_alias,
    )

    try:
        openapi_cli.modify_db_instance_name(req)
        return {"success": "true"}

    except Exception as e:
        logger.error(f"Error in modify_rds_mysql_instance_alias: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="修改 RDS MySQL 实例的数据库账号的描述信息",
)
def modify_rds_mysql_account_description(
    instance_id: str, account_name: str, account_desc: str
) -> dict[str, Any]:
    logger.info("modify_rds_mysql_account_description")

    req = volcenginesdkrdsmysqlv2.models.ModifyDBAccountDescriptionRequest(
        instance_id=instance_id,
        account_name=account_name,
        account_desc=account_desc,
    )

    try:
        openapi_cli.modify_db_account_description(req)
        return {"success": "true"}

    except Exception as e:
        logger.error(f"Error in modify_rds_mysql_account_description: {str(e)}")
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Run the RDS MySQL MCP Server")
    parser.add_argument("--config", "-c", help="Path to config file")  # 新增config参数
    parser.add_argument("--transport", "-t", choices=["sse", "stdio"], default="stdio")
    
    args = parser.parse_args()
    try:
        # 修改配置加载方式
        if args.config:
            config = load_config(args.config)
        else:
            config = load_config()
        # Initialize RDS MySQL service
        logger.info(
            f"Initialized RDS MySQL Base service"
        )

        # Initialize SDK
        configuration = volcenginesdkcore.Configuration()
        configuration.host = config.endpoint
        configuration.region = config.region
        configuration.ak = config.access_key_id
        configuration.sk = config.access_key_secret
        configuration.zone = config.zone

        global openapi_cli
        volcenginesdkcore.Configuration.set_default(configuration)
        openapi_cli = volcenginesdkrdsmysqlv2.RDSMYSQLV2Api()

        # Run the MCP server
        logger.info(
            f"Starting RDS MySQL MCP Server with {args.transport} transport"
        )
        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting RDS MySQL MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
