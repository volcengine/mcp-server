import os
import asyncio
import logging
import argparse
from typing import Any, Literal
from mcp.server.fastmcp import FastMCP
from mcp_server_mongodb.resource.mongo_resource import MongoDBSDK

# 初始化MCP服务
mcp_server = FastMCP("mongodb_mcp_server", port=int(os.getenv("PORT", "8000")))
logger = logging.getLogger("mongodb_mcp_server")

mongo_resource = MongoDBSDK(
    region=os.getenv('VOLC_REGION'), ak=os.getenv('VOLC_ACCESSKEY'), sk=os.getenv('VOLC_SECRETKEY'), host=os.getenv('HOST')
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
