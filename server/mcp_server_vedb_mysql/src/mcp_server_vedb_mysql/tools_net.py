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


# @mcp_server.tool(
#     description="设置指定节点在主备切换时被选为主节点的优先级"
# )
def modify_db_node_config(instance_id: str,
                          failover_priority: Annotated[int,Field(examples=[0,15])],
                          node_id: Annotated[str,Field(examples=['vedbm-****-1'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "failover_priority": failover_priority,
        "node_id": node_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_node_config(req)
    return resp.to_dict()


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


# @mcp_server.tool(
#     description="修改连接地址端口或前缀。触发示例：将实例vedbm-2pf2xk5v的连接终端vedbm-2pf2xk5v-Custom-50yv的私网地址前缀修改为vedbm-new，并将端口修改为3307"
# )
def modify_db_endpoint_address(instance_id: str,
                               endpoint_id: str,
                               domain_prefix: Optional[Annotated[str,Field(description='私网地址前缀', examples=['readwriteport'])]] = None,
                               port: int = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "network_type": "Private",
        "domain_prefix": domain_prefix,
        "port": port,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_endpoint_address(req)
    return resp.to_dict()


# @mcp_server.tool(
#     description="修改私网地址的解析方式。触发示例：将实例vedbm-2pf2xk5v的连接终端vedbm-2pf2xk5v-Custom-50yv的私网地址解析方式设置为支持公网解析"
# )
def modify_db_endpoint_dns(instance_id: str,
                           endpoint_id: str,
                           dns_visibility: Annotated[bool, Field(description='支持公网解析')]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "network_type": "Private",
        "dns_visibility": dns_visibility,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_endpoint_dns(req)
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

# @mcp_server.tool(
#     description="删除连接终端。触发示例：删除实例vedbm-2pf2xk5v的连接终端vedbm-2pf2xk5v-Custom-50yv"
# )
def delete_db_endpoint(instance_id: str,
                       endpoint_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_endpoint(req)
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

# @mcp_server.tool(
#     description="修改连接终端。参数参考create_db_endpoint。触发示例：修改实例vedbm-2pf2xk5v的连接终端vedbm-2pf2xk5v-Custom-50yv的名称为新名称，并设置自动添加新节点"
# )
def modify_db_endpoint(instance_id: str,
                       endpoint_id: str,
                       auto_add_new_nodes: bool = None,
                       consist_level: str = None,
                       consist_timeout: Optional[int] = None,
                       consist_timeout_action: str = None,
                       description: str = None,
                       distributed_transaction: bool = None,
                       endpoint_name: str = None,
                       master_accept_read_requests: bool = None,
                       nodes: str = None,
                       nodes_weight: list[dict[str, Any]] = None,
                       read_write_mode: str = None,
                       weight_mode: Optional[Annotated[str,Field(description='权重分配策略', examples=['custom','off'])]] = 'off') -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "auto_add_new_nodes": auto_add_new_nodes,
        "consist_level": consist_level,
        "consist_timeout": consist_timeout,
        "consist_timeout_action": consist_timeout_action,
        "description": description,
        "distributed_transaction": distributed_transaction,
        "endpoint_name": endpoint_name,
        "master_accept_read_requests": master_accept_read_requests,
        "nodes": nodes,
        "nodes_weight": nodes_weight,
        "read_write_mode": read_write_mode,
        "weight_mode": weight_mode,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_endpoint(req)
    return resp.to_dict()

# @mcp_server.tool(
#     description="修改目标白名单设置，例如白名单名称、IP白名单地址等。触发示例：将白名单acl-d1fd76693bd54e658912e7337d5b****的名称修改为new_name，并添加IP地址10.0.0.0/24"
# )
def modify_allow_list(allow_list_id: Annotated[str, Field(examples=['acl-****'])],
                      allow_list_name: str,
                      allow_list: Optional[Annotated[str,Field(examples=['192.168.1.0,0.0.0.0/0'])]] = None,
                      allow_list_desc: Optional[Annotated[str,Field(description='备注信息')]] = None,
                      apply_instance_num: Optional[Annotated[int,Field(description='白名单所绑定的实例个数(用于确认本次修改的影响范围，避免误操作引发故障，可调用DescribeAllowLists接口查询总数)')]] = None,
                      modify_mode: Optional[Annotated[str,Field(examples=['Append','Cover','Delete'])]] = None) -> dict[str, Any]:
    req = {
        "allow_list_id": allow_list_id,
        "allow_list_name": allow_list_name,
        "allow_list": allow_list,
        "allow_list_desc": allow_list_desc,
        "apply_instance_num": apply_instance_num,
        "modify_mode": modify_mode,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_allow_list(req)
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


# @mcp_server.tool(
#     description="为指定的实例创建公网连接地址，即开启实例的公网访问功能。触发示例：为实例vedbm-****的连接终端vedbm-****-Custom-50yv创建公网地址"
# )
def create_db_endpoint_public_address(instance_id: str,
                                      endpoint_id: Annotated[str, Field(description='连接终端ID(可调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID)', examples=['vedbm-****-Custom-***'])],
                                      eip_id: Annotated[str, Field(description='实例需要绑定的EIP ID(可调用DescribeEipAddresses接口查询已创建的EIP的详细信息)')]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "eip_id": eip_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_db_endpoint_public_address(req)
    return resp.to_dict()

# @mcp_server.tool(
#     description="删除目标白名单。触发示例：删除白名单acl-d1fd76693bd54e658912e7337d5b****"
# )
def delete_allow_list(allow_list_id: str) -> dict[str, Any]:
    req = {
        "allow_list_id": allow_list_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_allow_list(req)
    return resp.to_dict()

# @mcp_server.tool(
#     description="删除指定实例的公网连接地址，即关闭公网访问功能。触发示例：删除实例vedbm-****的连接终端vedbm-****-Custom-50yv的公网地址"
# )
def delete_db_endpoint_public_address(instance_id: str,
                                      endpoint_id: Annotated[str, Field(description='连接终端ID')]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_endpoint_public_address(req)
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
