import os
import asyncio
from typing import Optional
from pydantic import Field
import logging
import argparse
from typing import Any, Literal
from mcp.server.fastmcp import FastMCP
from mcp_server_rds_mysql.resource.rds_mysql_resource import RDSMySQLSDK

# 初始化MCP服务
mcp_server = FastMCP("rds_mysql_mcp_server", port=int(os.getenv("PORT", "8000")))
logger = logging.getLogger("rds_mysql_mcp_server")

rds_mysql_resource = RDSMySQLSDK(
    region=os.getenv('VOLCENGINE_REGION'), ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY'), host=os.getenv('VOLCENGINE_HOST')
)

@mcp_server.tool(name = "describe_db_instances",description = "查询RDSMySQL实例列表")
def describe_db_instances(page_number: int, instance_id: str = None, instance_name: str = None) -> dict[str, Any]:
    """查询RDSMySQL实例列表

    Args:
        instance_id (str): 实例ID
        instance_name (str): 实例名称
        page_number (int): 实例列表页数
    """
    req = {
        "instance_id": instance_id, "instance_name": instance_name, "page_number": page_number, "page_size": 20,
    }
    resp = rds_mysql_resource.describe_db_instances(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_db_instance_detail", description="查询RDSMySQL实例详情")
def describe_db_instance_detail(instance_id: str) -> dict[str, Any]:
    """查询RDSMySQL实例详情
       Args:
           instance_id (str): 实例ID
   """
    req = {
        "instance_id": instance_id,
    }
    resp = rds_mysql_resource.describe_db_instance_detail(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_instance_engine_minor_versions",
    description="查询RDSMySQL实例可升级的内核小版本"
)
def describe_db_instance_engine_minor_versions(instance_ids: list[str]) -> dict[str, Any]:
    """查询RDSMySQL实例可升级的内核小版本

        Args:
            instance_ids (list[str]): 实例ID列表
    """
    req = {
        "instance_ids": instance_ids,
    }
    resp = rds_mysql_resource.describe_db_instance_engine_minor_versions(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_accounts",
    description="查询RDS MySQL实例的数据库账号"
)
def describe_db_accounts(
        instance_id: str,
        account_name: Optional[str] = None,
        page_number: int = 1,
        page_size: int = 10
) -> dict[str, Any]:
    """查询RDS MySQL实例的数据库账号列表

    Args:
        instance_id (str): 实例ID
        account_name (Optional[str]): 数据库账号名称，支持模糊查询
        page_number (int): 当前页页码，最小值为1，默认1
        page_size (int): 每页记录数，范围1-1000，默认10
    """
    # 构建请求参数
    req = {
        "instance_id": instance_id,
        "page_number": page_number,
        "page_size": page_size
    }

    # 添加可选参数
    if account_name is not None:
        req["account_name"] = account_name

    # 发送请求
    resp = rds_mysql_resource.describe_db_accounts(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_databases",
    description="根据指定RDS MySQL 实例ID 查看数据库列表"
)
def describe_databases(
        instance_id: str,
        db_name: Optional[str] = None,
        page_number: int = 1,
        page_size: int = 10
) -> dict[str, Any]:
    """根据指定RDS MySQL 实例ID 查看数据库列表

    Args:
        instance_id (str): 实例ID
        db_name (Optional[str]): 数据库名称，支持模糊查询
        page_number (int): 当前页页码，最小值为1，默认1
        page_size (int): 每页记录数，范围1-1000，默认10
    """
    # 构建请求参数
    req = {
        "instance_id": instance_id,
        "page_number": page_number,
        "page_size": page_size
    }

    # 添加可选参数DBName
    if db_name is not None:
        req["db_name"] = db_name

    # 发送请求
    resp = rds_mysql_resource.describe_databases(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_instance_parameters",
    description="获取RDS MySQL实例参数列表"
)
def describe_db_instance_parameters(
        instance_id: str,
        parameter_name: str = None,
        node_id: str = None
) -> dict[str, Any]:
    """
    获取RDS MySQL实例参数列表

    Args:
        instance_id (str): 实例ID
        parameter_name (str, optional): 参数名
        node_id (str, optional): 查询指定节点的参数设置，如不设置该字段，只返回主节点和备节点的参数设置
    """
    req = {
        "InstanceId": instance_id,
        "ParameterName": parameter_name,
        "NodeId": node_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mysql_resource.describe_db_instance_parameters(req)
    return resp.to_dict()


@mcp_server.tool(
    name="create_rds_mysql_instance",
    description="创建 RDS MySQL 实例"
)
def create_rds_mysql_instance(
        vpc_id: str = Field(description="私有网络 ID"),
        subnet_id: str = Field(description="子网 ID"),
        instance_name: Optional[str] = Field(default="", description="实例名称，默认为系统自动生成"),
        db_engine_version: str = Field(default="MySQL_8_0", description="数据库版本，例如 'MySQL_8_0'"),
        # 主节点配置
        primary_zone: str = Field(default="cn-beijing-a", description="主节点可用区"),
        primary_spec: str = Field(default="rds.mysql.1c2g", description="主节点规格，格式如 'rds.mysql.1c2g'"),
        # 备节点配置
        secondary_count: int = Field(default=1, description="备节点数量"),
        secondary_zone: Optional[str] = Field(default=None, description="备节点可用区，默认与主节点不同区"),
        secondary_spec: str = Field(default="rds.mysql.1c2g", description="备节点规格"),
        # 只读节点配置
        read_only_count: int = Field(default=0, description="只读节点数量"),
        read_only_zone: str = Field(default="cn-beijing-a", description="只读节点可用区"),
        read_only_spec: str = Field(default="rds.mysql.1c2g", description="只读节点规格"),
        # 存储配置
        storage_space: int = Field(default=20, description="存储空间大小(GB)"),
        storage_type: str = Field(default="LocalSSD", description="存储类型，默认本地SSD"),
        # 付费配置
        charge_type: str = Field(default="PostPaid", description="付费类型，默认后付费")
) -> dict[str, Any]:
    """创建 RDS MySQL 实例

    Args:
        vpc_id: 私有网络 ID
        subnet_id: 子网 ID
        instance_name: 实例名称
        db_engine_version: 数据库版本
        primary_zone: 主节点可用区
        primary_spec: 主节点规格
        secondary_count: 备节点数量
        secondary_zone: 备节点可用区
        secondary_spec: 备节点规格
        read_only_count: 只读节点数量
        read_only_zone: 只读节点可用区
        read_only_spec: 只读节点规格
        storage_space: 存储空间大小(GB)
        storage_type: 存储类型
        charge_type: 付费类型

    Returns:
        dict: 创建结果，包含实例ID和订单号等信息
    """
    # 构建节点信息列表
    node_info = []

    # 添加主节点
    node_info.append({
        "NodeType": "Primary",
        "ZoneId": primary_zone,
        "NodeSpec": primary_spec
    })

    # 添加备节点
    for _ in range(secondary_count):
        zone = secondary_zone or primary_zone  # 备节点默认同主节点可用区
        node_info.append({
            "NodeType": "Secondary",
            "ZoneId": zone,
            "NodeSpec": secondary_spec
        })

    # 添加只读节点
    for _ in range(read_only_count):
        node_info.append({
            "NodeType": "ReadOnly",
            "ZoneId": read_only_zone,
            "NodeSpec": read_only_spec
        })

    # 构建请求数据
    data = {
        "DBEngineVersion": db_engine_version,
        "NodeInfo": node_info,
        "StorageType": storage_type,
        "StorageSpace": storage_space,
        "VpcId": vpc_id,
        "SubnetId": subnet_id,
        "ChargeInfo": {"ChargeType": charge_type},
    }

    # 添加可选的实例名称
    if instance_name:
        data["InstanceName"] = instance_name

    # 发送创建请求
    resp = rds_mysql_resource.create_db_instance(data)
    return resp.to_dict()
@mcp_server.tool(
    name="describe_azs",
    description="获取实例创建可用区"
)
def describe_azs() -> dict[str, Any]:
    """获取实例创建可用区
    """
    req = {"region_id": os.getenv('VOLCENGINE_REGION')}
    try:
        resp = rds_mysql_resource.describe_azs(req)
        return resp.to_dict()
    except Exception as e:
        raise Exception(str(e) + str(req))


@mcp_server.tool(
    name="describe_allow_lists",
    description="获取RDSMySQL实例白名单"
)
def describe_allow_lists(region_id: str) -> dict[str, Any]:
    """获取RDSMySQL实例白名单
       Args:
           region_id (str): 地区ID
       Returns:
       {
            "AllowLists": [] 白名单列表
       }
    """
    req = {"region_id": region_id}
    resp = rds_mysql_resource.describe_allow_lists(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_node_specs",
    description="获取实例部署规格"
)
def describe_node_specs(region_id: str) -> dict[str, Any]:
    """
    Args:
        region_id (str): 地区ID

    Returns:
    {
        "ResponseMetadata": {}
        "Result": {
            "ConfigServerNodeSpecs": []  config-server组件可选规格
            "MongosNodeSpecs": [] mongos组件可选规格
            "NodeSpecs": [] 副本集节点可选规格
            "ShardNodeSpecs": [] 分片集群可选规格
        }
    }
    """
    req = {"region_id": region_id}
    resp = rds_mysql_resource.describe_node_spec(req)
    return resp.to_dict()


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the RDSMySQL MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting RDSMySQL MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting RDSMySQL MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
