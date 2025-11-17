import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)
openapi_cli = vedbm_resource_sdk.client


@mcp_server.tool(
    description="Create a Network AllowList for VeDB MySQL. 触发示例：创建一个名为test_whitelist的IP白名单，允许IP地址192.168.1.0/24访问",
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


@mcp_server.tool(
    description="Bind a Network AllowList to VeDB MySQL instances. 触发示例：将白名单acl-****绑定到实例vedbm-****",
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

@mcp_server.tool(
    description="查询实例绑定的白名单信息。触发示例：查询实例vedbm-****当前绑定的所有白名单信息"
)
def list_bound_allow_lists(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_instance_allow_lists(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询指定实例连接终端的详细信息。触发示例：查询实例vedbm-****的所有连接终端详细信息"
)
def get_db_endpoint(instance_id: str,
                         endpoint_id: Optional[str] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_endpoint(req)
    return resp.to_dict()

@mcp_server.tool(
    description="创建连接终端。触发示例：在实例vedbm-****中创建一个名为自定义读写终端的连接终端，关联节点vedbm-****-0和vedbm-****-1，读写模式为读写"
)
def create_db_endpoint(instance_id: str,
                       nodes: Annotated[str, Field(description='连接终端关联的多个节点ID之间使用英文逗号分隔', examples=['vedbm-****-0,vedbm-****-1'])],
                       auto_add_new_nodes: Optional[Annotated[bool,Field(description='后续新创建的只读节点是否自动加入该连接终端')]] = False,
                       consist_level: Optional[Annotated[str,Field(examples=['Eventual','Global','Session'])]] = None,
                    #    consist_timeout: Optional[Annotated[int,Field(description='延迟很大时，只读节点同步最新数据的超时时间，单位为us')]] = 10000,
                       consist_timeout_action: Optional[Annotated[str,Field(description='只读节点同步数据超时后的超时策略', examples=['ReadMaster','ReturnError'])]] = None,
                       description: str = None,
                       distributed_transaction: Optional[Annotated[bool,Field(description='开启事务拆分')]] = True,
                       endpoint_name: Optional[Annotated[str,Field(examples=['自定义终端'])]] = None,
                       master_accept_read_requests: Optional[Annotated[bool,Field(description='主节点接受读请求')]] = True,
                       read_write_mode: Optional[Annotated[str,Field(examples=['ReadOnly','ReadWrite'])]] = 'ReadOnly') -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_type": "Custom",
        "nodes": nodes,
        "auto_add_new_nodes": auto_add_new_nodes,
        "consist_level": consist_level,
        # "consist_timeout": consist_timeout,
        "consist_timeout_action": consist_timeout_action,
        "description": description,
        "distributed_transaction": distributed_transaction,
        "endpoint_name": endpoint_name,
        "master_accept_read_requests": master_accept_read_requests,
        "read_write_mode": read_write_mode,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_db_endpoint(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询目标白名单的详细信息，例如 IP 地址和绑定的实例详情。触发示例：查询白名单acl-****的详细信息，包括绑定的实例"
)
def describe_allow_list_detail(allow_list_id: str) -> dict[str, Any]:
    req = {
        "allow_list_id": allow_list_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_allow_list_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询所有IP白名单。触发示例：查询北京地域下的所有白名单列表"
)
def list_allow_lists(region_id: Annotated[str, Field(examples=['cn-beijing'])],
                         instance_id: str = None,
                         project_name: Optional[Annotated[str,Field(description='所属项目名称', examples=['default'])]] = None) -> dict[str, Any]:
    req = {
        "region_id": region_id,
        "instance_id": instance_id,
        "project_name": project_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_allow_lists(req)
    return resp.to_dict()
