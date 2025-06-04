import os
import asyncio
from pydantic import Field
import logging
import argparse
from typing import Any, Literal
from mcp.server.fastmcp import FastMCP
from mcp_server_mongodb.resource.mongo_resource import MongoDBSDK

# 初始化MCP服务
mcp_server = FastMCP("mongodb_mcp_server", port=int(os.getenv("PORT", "8000")))
logger = logging.getLogger("mongodb_mcp_server")

mongo_resource = MongoDBSDK(
    region=os.getenv('VOLCENGINE_REGION'), ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY'), host=os.getenv('VOLCENGINE_HOST')
)

@mcp_server.tool(name="describe_db_instances", description="查询MongoDB实例列表")
def describe_db_instances(page_number: int, instance_id: str = None, instance_name: str = None) -> dict[str, Any]:
    """查询实例列表

    Args:
        instance_id (str): 实例ID
        instance_name (str): 实例名称
        page_number (int): 实例列表页数
    """
    req = {
        "instance_id": instance_id, "instance_name": instance_name, "page_number": page_number, "page_size": 20,
    }
    resp = mongo_resource.describe_db_instances(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_db_instance_detail", description="查询MongoDB实例详情")
def describe_db_instance_detail(instance_id: str) -> dict[str, Any]:
    """查询MongoDB实例详情
       Args:
           instance_id (str): 实例ID
   """
    req = {
        "instance_id": instance_id,
    }
    resp = mongo_resource.describe_db_instance_detail(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_backups_request", description="查询MongoDB备份详情")
def describe_backups_request(page_number: int, instance_id: str,
                             backup_object: Literal["Data", "Log"] = "Data",
                             backup_type: Literal["Logical", "Physical"] = "Physical",
                             backup_status: Literal["Success", "Failed", "Running"] = "Success"
                             ) -> dict[str, Any]:
    """查询备份列表

        Args:
            instance_id (str): 实例ID
            page_number (int): 备份列表页数
            backup_object (Literal["Data", "Log"]) 备份对象，全量数据备份或者是日志备份
            backup_type (Literal["Logical", "Physical"]) 备份方式, 物理备份或者是逻辑备份
            backup_status (Literal["Success", "Failed", "Running"]) 备份状态
    """
    req = {
        "instance_id": instance_id, "backup_object": backup_object, "page_number": page_number,
        "backup_type": backup_type, "backup_status": backup_status, "page_size": 20,
    }
    resp = mongo_resource.describe_backups_request(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_db_instance_parameters", description="获取MongoDB实例参数列表")
def describe_db_instance_parameters(instance_id: str,
                                    parameter_role: Literal["Node", "Shard", "ConfigServer", "Mongos"] = None,
                                    ) -> dict[str, Any]:
    """获取MongoDB实例参数列表

            Args:
                instance_id (str): 实例ID
                parameter_role (Literal["Node", "Shard", "ConfigServer", "Mongos"]) "MongoDB实例组件角色, 副本集对应Node, 分片集群的各个组件对应Shard, ConfigServer, Mongos
        """
    req = {
        "instance_id": instance_id, "parameter_role": parameter_role,
    }
    resp = mongo_resource.describe_db_instance_parameters(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_slow_log", description="获取MongoDB实例慢日志")
def describe_slow_log(instance_id: str, pod_name: str, start_time: int, end_time: int, context: str = None
                      ) -> dict[str, Any]:
    """获取MongoDB实例慢日志

        Args:
            instance_id (str): 实例ID
            pod_name (str): MongoDB实例pod name，也是实例的 node_id, db_instance_detail 方法中可以获取到, 格式: instance_id-${index}
            start_time (int) 查询慢日志的开始时间戳
            end_time (int) 查询慢日志的结束时间戳
            context (str) 上一页慢日志最后一条的位置标识
    """
    req = {
        "instance_id": instance_id, "pod_name": pod_name, "context": context, "limit": 20,
        "start_time": start_time, "end_time": end_time, "sort": "DESC",
    }
    resp = mongo_resource.describe_db_slow_logs(req)
    return resp.to_dict()


@mcp_server.tool(name="create_db_instance", description="创建mongoDB实例")
def create_db_instance(zone_id: str = Field(description="可用区ID, 可以调用describe_azs获取"),
                       vpc_id: str = Field(description="用户的私网id"),
                       subnet_id: str = Field(description="用户的子网id"),
                       db_engine_version: str = Field(default="MongoDB_6_0", description="实例版本",
                                                      example="MongoDB_5_0"),
                       instance_type: str = Field(default="ReplicaSet",
                                                  description="实例类型，分为副本集实例和分片集实例",
                                                  example="ShardedCluster"),
                       node_spec: str = Field(description="当创建副本集实例时代表每个副本的规格，格式为mongo.{x}c{x}g组成, "
                                                          "可以调用describe_node_specs获取其中的spec_name，可以默认获取最小的规格"),
                       storage_space_gb: int = Field(default=100, description="默认存储大小"),

                       allow_list_ids: list[str] = Field(default=None,
                                                         description="实例绑定的网络白名单列表，创建时需要通过调用describe_allow_lists "
                                                                     "获取allow_list_id,可以绑定一个实例大于0的白名单id"),
                       shard_number: int = Field(default=1, description="创建分片集群时需要创建的分片数量"),
                       mongos_node_spec: str = Field(default=None, description="当创建分片集实例时，代表每个mongos组件的规格，格式为mongo"
                                                                               ".mongos.{x}c{x}g组成, "
                                                                               "可以调用describe_node_specs获取其中mognos"
                                                                               "的spec_name，可以默认获取最小的规格"),
                       mongos_node_number: int = Field(default=2, description="创建分片集群时，需要创建的mongos的数量"),
                       ) -> dict[str, Any]:
    """创建实例

    Args:
        mongos_node_number: mongos节点的数量
        mongos_node_spec: mongos的节点的规格
        shard_number: 分片数量
        node_spec: 节点规格
        storage_space_gb: 节点存储大小
        allow_list_ids: 白名单ID
        zone_id(str): 可用区ID
        db_engine_version(str) 实例版本
        instance_type(str) 实例类型
    Returns
        instance_id(str): 返回创建的实例ID
        order_no(str): 订单号
    """
    req = {
        "instance_name": "mcp_server_auto_create",
        "zone_id": zone_id,
        "db_engine": "MongoDB",
        "db_engine_version": db_engine_version,
        "node_spec": node_spec,
        "instance_type": instance_type,
        "storage_space_gb": storage_space_gb,
        "node_number": 3,
        "count": 1,
        "charge_type": "PostPaid",
        "auto_renew": False,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
    }
    if allow_list_ids is not None:
        req["allow_list_ids"] = allow_list_ids
    if instance_type == "ShardedCluster":
        req["shard_number"] = shard_number
        req["mongos_node_spec"] = mongos_node_spec
        req["mongos_node_number"] = mongos_node_number
    resp = mongo_resource.create_db_instance(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_azs", description="获取实例创建可用区")
def describe_azs() -> dict[str, Any]:
    """获取实例创建可用区
    """
    req = {"region_id": os.getenv('VOLCENGINE_REGION')}
    try:
        resp = mongo_resource.describe_azs(req)
        return resp.to_dict()
    except Exception as e:
        raise Exception(str(e) + str(req))


@mcp_server.tool(name="describe_allow_lists", description="获取MongoDB实例白名单")
def describe_allow_lists(region_id: str) -> dict[str, Any]:
    """获取MongoDB实例白名单
       Args:
           region_id (str): 地区ID
       Returns:
       {
            "AllowLists": [] 白名单列表
       }
    """
    req = {"region_id": region_id}
    resp = mongo_resource.describe_allow_lists(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_node_specs", description="获取实例部署规格")
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
    resp = mongo_resource.describe_node_spec(req)
    return resp.to_dict()


def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the LAS MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting MongoDB MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting MongoDB MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
