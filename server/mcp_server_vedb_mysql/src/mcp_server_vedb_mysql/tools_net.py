import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)
openapi_cli = vedbm_resource_sdk.client


@mcp_server.tool(
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


@mcp_server.tool(
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


@mcp_server.tool(
    description="设置指定节点在主备切换时被选为主节点的优先级"
)
def modify_db_node_config(instance_id: str,
                          failover_priority: Annotated[int,Field(description='节点切主的优先级，取值为 0~15。数值越大，优先级越高', examples=['5'])],
                          node_id: Annotated[str,Field(examples=['vedbm-h441603c68aaa****-**'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "failover_priority": failover_priority,
        "node_id": node_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_node_config(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询实例绑定的白名单信息"
)
def describe_instance_allow_lists(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_instance_allow_lists(req)
    return resp.to_dict()


@mcp_server.tool(
    description="修改连接地址端口或前缀"
)
def modify_db_endpoint_address(instance_id: str,
                               endpoint_id: Annotated[str, Field(description='连接终端 ID。(您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。)', examples=['vedbm-2pf2xk5v****-Custom-50yv'])],
                               network_type: Annotated[str, Field(description='网络地址类型，取值固定为 `Private`，即私网地址。', examples=['Private枚举值：Private,Public'])],
                               domain_prefix: Optional[Annotated[str,Field(description='新的私网地址前缀。连接地址前缀规则如下：- 连接地址前缀至少包含 8 个字符、总长度（含后缀）不得超过 63 个字符。- 以小写字母开头，且以小写字母或数字结尾。- 由小写字母、数字和连字符（-）组成。(- 仅支持修改私网连接地址前缀，不支持修改公网连接地址前缀。- 新地址生效后，老地址会在三分钟后关闭，请同步修改应用程序的连接配置，否则可能会影响业务，请谨慎操作。)', examples=['vedbm-55556hhh'])]] = None,
                               port: Optional[Annotated[int,Field(description='输入新的端口号，端口号取值范围为 1000~65534。(修改端口号，会同步修改私网和公网的端口号。新端口生效后，老端口会即刻关闭，请同步修改应用程序的连接配置，否则可能会影响业务，请谨慎操作。)', examples=['3307'])]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "network_type": network_type,
        "domain_prefix": domain_prefix,
        "port": port,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_endpoint_address(req)
    return resp.to_dict()


@mcp_server.tool(
    description="修改私网地址的解析方式"
)
def modify_db_endpoint_dns(instance_id: str,
                           endpoint_id: Annotated[str, Field(description='连接终端 ID。(您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。)', examples=['vedbm-2pf2xk5v****-Custom-50yv'])],
                           network_type: Annotated[str, Field(description='网络地址类型，取值固定为 `Private`，即私网地址。', examples=['Private枚举值：Private'])],
                           dns_visibility: Annotated[bool, Field(description='解析方式，取值：- `false`：火山引擎私网解析（默认）。- `true`：火山引擎私网以及公网解析。', examples=['true'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "network_type": network_type,
        "dns_visibility": dns_visibility,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_endpoint_dns(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询指定实例连接终端的详细信息"
)
def describe_db_endpoint(instance_id: str,
                         endpoint_id: Optional[Annotated[str,Field(description='连接终端 ID。(您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。)', examples=['vedbm-2pf2xk5v****-Custom-50yv'])]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_endpoint(req)
    return resp.to_dict()

@mcp_server.tool(
    description="删除连接终端"
)
def delete_db_endpoint(instance_id: str,
                       endpoint_id: Annotated[str, Field(description='连接终端 ID。(您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。)', examples=['vedbm-2pf2xk5v****-Custom-50yv'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_endpoint(req)
    return resp.to_dict()

@mcp_server.tool(
    description="创建连接终端"
)
def create_db_endpoint(instance_id: str,
                       endpoint_type: Annotated[str, Field(description='连接终端类型。取值固定为 `Custom`，表示自定义终端。', examples=['Custom枚举值：Custom'])],
                       nodes: Annotated[str, Field(description='连接终端关联的节点 ID，多个节点 ID 之间使用英文逗号（,）分隔。填写规则如下：- 当 `ReadWriteMode` 取值为 `ReadWrite` 时，必须传入主节点，可按需选择是否传入只读节点。(建议关联主节点和至少一个只读节点。仅关联主节点时，不支持读写分离。)- 当 `ReadWriteMode` 取值为 `ReadOnly` 时，可以传入一个或多个只读节点。(您可以调用DescribeDBInstanceDetail接口，查询指定实例的详细信息，包括节点 ID。)', examples=['vedbm-2pf2xk5v****-0,vedbm-2pf2xk5v****-1'])],
                       auto_add_new_nodes: Optional[Annotated[bool,Field(description='设置后续新创建的只读节点是否自动加入该连接终端。取值：- `true`：自动加入。- `false`：不自动加入（默认）。', examples=['true'])]] = 'false',
                       consist_level: Optional[Annotated[str,Field(description='一致性级别，关于一致性级别的详细介绍请参见[一致性级别](https://www.volcengine.com/docs/6357/1144276)。取值范围：- `Eventual`：最终一致性。- `Session`：会话一致性。- `Global`：全局一致性。(- 当 `ReadWriteMode` 取值为 `ReadWrite` 时，可选择的一致性级别有 `Eventual`、`Session`（默认）、`Global`。- 当 `ReadWriteMode` 取值为 `ReadOnly` 时，一致性级别默认为 `Eventual`，且不可更改。)', examples=['Session枚举值：Eventual,Global,Session'])]] = None,
                       consist_timeout: Optional[Annotated[int,Field(description='延迟很大时，只读节点同步最新数据的超时时间，单位为 us，取值范围为 1us~100000000us，默认值为 10000us。(当 `ConsistLevel` 取值为 `Global` 或 `Session` 时，该参数才生效。)', examples=['10000'])]] = '10000',
                       consist_timeout_action: Optional[Annotated[str,Field(description='只读节点同步数据超时后的超时策略，支持以下两种策略：- `ReturnError`：返回 SQL 报错（`wait replication complete timeout, please retry`）。- `ReadMaster`：发送请求到主节点（默认）。(当 `ConsistLevel` 取值为 `Global` 或 `Session` 时，该参数才生效。)', examples=['ReadMaster枚举值：ReadMaster,ReturnError'])]] = None,
                       description: Optional[Annotated[str,Field(description='连接终端的描述信息。长度不能超过 200 个字符。', examples=['这是对连接终端的描述'])]] = None,
                       distributed_transaction: Optional[Annotated[bool,Field(description='设置是否开启事务拆分，关于事务拆分的详细介绍请参见[事务拆分](https://www.volcengine.com/docs/6357/1144274)。取值范围：- `true`：开启（默认）。- `false`：不开启。(仅当 `ReadWriteMode` 取值为`ReadWrite` 时，支持开启事务拆分。)', examples=['true'])]] = 'true',
                       endpoint_name: Optional[Annotated[str,Field(description='连接终端名称，设置规则如下：- 不能以数字或中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度为 1~64 个字符。', examples=['自定义终端'])]] = None,
                       master_accept_read_requests: Optional[Annotated[bool,Field(description='主节点接受读请求。取值范围：- `true`：（默认）当开启主节点接受读功能后，非事务读请求会按活跃请求数负载均衡的模式发送至主节点或只读节点。- `false`：当关闭主节点接受读功能后，此时主节点只接受事务读请求，而非事务读请求不会发往主节点。(仅当 `ReadWriteMode` 取值为`ReadWrite` 时，支持开启主节点接受读。)', examples=['true'])]] = 'true',
                       read_write_mode: Optional[Annotated[str,Field(description='终端读写模式。取值：- `ReadWrite`：读写终端。- `ReadOnly`：只读终端（默认）。', examples=['ReadOnly枚举值：ReadOnly,ReadWrite'])]] = 'ReadOnly') -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "endpoint_type": endpoint_type,
        "nodes": nodes,
        "auto_add_new_nodes": auto_add_new_nodes,
        "consist_level": consist_level,
        "consist_timeout": consist_timeout,
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
    description="修改连接终端"
)
def modify_db_endpoint(instance_id: str,
                       endpoint_id: Annotated[str, Field(description='连接终端 ID。(您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。)', examples=['vedbm-2pf2xk5v****-Custom-50yv'])],
                       auto_add_new_nodes: Optional[Annotated[bool,Field(description='设置新创建的只读节点是否自动加入该连接终端。取值：端。取值：- `true`：自动加入。- `false`：不自动加入。(仅默认终端和自定义终端支持设置该参数。可通过 `EndpointId` 快速判断连接终端类型。如 `EndpointId` 中含有 `default` 或 `custom` 字段，则说明该终端类型为默认终端或自定义终端。)', examples=['true'])]] = None,
                       consist_level: Optional[Annotated[str,Field(description='一致性级别，关于一致性级别的详细介绍请参见[一致性级别](https://www.volcengine.com/docs/6357/1144276) 。取值范围：- `Eventual`：最终一致性。- `Session`：会话一致性。- `Global`：全局一致性。(- 当 `ReadWriteMode` 取值为 `ReadWrite` 时，可选择的一致性级别有 `Eventual`、`Session`（默认）、`Global`。- 当 `ReadWriteMode` 为 `ReadOnly` 时，一致性级别默认为 `Eventual`，且不可更改。- 一致性级别从最终一致性的调整到会话一致性或全局一致性，仅对新连接生效。从会话一致性或全局一致性调整到最终一致性，存量连接立即生效。)', examples=['Session枚举值：Eventual,Global,Session'])]] = None,
                       consist_timeout: Optional[Annotated[int,Field(description='延迟很大时，只读节点同步最新数据的超时时间，单位为 us，取值范围为 1us~100000000us，默认值为 10000us。(当 `ConsistLevel` 取值为 `Global` 或 `Session` 时，该参数才生效。)', examples=['10000'])]] = None,
                       consist_timeout_action: Optional[Annotated[str,Field(description='只读节点同步数据超时后的超时策略，支持以下两种策略：- `ReturnError`：返回 SQL 报错（`wait replication complete timeout, please retry`）。- `ReadMaster`：发送请求到主节点（默认）。(当 `ConsistLevel` 取值为 `Global` 或 `Session` 时，该参数才生效。)', examples=['ReadMaster枚举值：ReadMaster,ReturnError'])]] = None,
                       description: Optional[Annotated[str,Field(description='连接终端的描述信息。长度不能超过 200 个字符。', examples=['这是对连接终端的描述'])]] = None,
                       distributed_transaction: Optional[Annotated[bool,Field(description='设置是否开启事务拆分，关于事务拆分的详细介绍请参见[事务拆分](https://www.volcengine.com/docs/6357/1144274)。取值范围：- `true`：开启（默认）。- `false`：不开启。(- 仅当 `ReadWriteMode` 取值为`ReadWrite` 时，支持开启事务拆分。- 修改事务拆分状态仅对新连接生效，已有的连接保持原来的配置。)', examples=['true'])]] = None,
                       endpoint_name: Optional[Annotated[str,Field(description='实例连接终端名称。终端名称的设置规则如下：- 不能以数字或中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度为 1~64 个字符。', examples=['自定义只读终端'])]] = None,
                       master_accept_read_requests: Optional[Annotated[bool,Field(description='主节点接受读请求。取值范围：- `true`：（默认）当开启**主节点接受读**功能后，非事务读请求会按活跃请求数负载均衡的模式发送至主节点或只读节点。- `false`：当关闭**主节点接受读**功能后，此时主节点只接受事务读请求，而非事务读请求不会发往主节点。(- 仅对默认终端和自定义读写终端有效。- 修改主节点接受读功能对所有连接立即生效。)', examples=['true'])]] = None,
                       nodes: Optional[Annotated[str,Field(description='连接终端所关联节点的节点 ID。多个节点 ID 之间使用英文逗号（,）分隔，填写规则如下：- 当 `ReadWriteMode` 从 `ReadOnly` 修改为 `ReadWrite` 时，必须传入主节点，可按需选择是否传入只读节点。(建议关联主节点和至少一个只读节点。仅关联主节点时，不支持读写分离。)- 当 `ReadWriteMode` 从 `ReadWrite` 修改为 `ReadOnly` 时，可以传入一个节点或多个只读节点，不可传入主节点。(- 当修改了终端的读写模式，即更改了 `ReadWriteMode` 的取值时必填。- 您可以调用DescribeDBInstanceDetail接口，查询指定实例的详细信息，包括节点 ID。)', examples=['vedbm-2pf2xk5v****-0,vedbm-2pf2xk5v****-1'])]] = None,
                       nodes_weight: Optional[Annotated[list[dict[str, Any]],Field(description='自定义读权重分配，即节点的请求权重', examples=['[  { "NodeId" : "mysql-e26822cf****-r84eb", "Weight" : 100 }, { "NodeId" : "mysql-e26822cf****-r90ab", "Weight" : 200 } ]'])]] = None,
                       read_write_mode: Optional[Annotated[str,Field(description='终端读写模式。取值：- `ReadWrite`：读写终端。- `ReadOnly`：只读终端。)warning如果修改了读写模式，则需要在 Nodes 参数中提供节点列表。)', examples=['ReadOnly枚举值：ReadOnly,ReadWrite'])]] = None,
                       weight_mode: Optional[Annotated[str,Field(description='权重分配策略', examples=['custom枚举值：custom,off'])]] = 'off') -> dict[str, Any]:
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

@mcp_server.tool(
    description="修改目标白名单设置，例如白名单名称、IP 白名单地址等"
)
def modify_allow_list(allow_list_id: Annotated[str, Field(description='白名单 ID。', examples=['acl-d1fd76693bd54e658912e7337d5b****'])],
                      allow_list_name: Annotated[str, Field(description='白名单名称。- 如需修改白名单名称，此参数应指定为新的白名单名称。名称需满足以下要求：- 不能以数字、中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度需在 1~128 个字符内。- 无需修改白名单名称时，此参数指定为原白名单的名称即可。您可以调用DescribeAllowLists接口查询指定地域下所有的白名单列表信息，包括白名单名称。', examples=['test'])],
                      allow_list: Optional[Annotated[str,Field(description='输入 IP 地址或 CIDR 格式的 IP 地址段。(- 当需要变更白名单中的 IP 地址时，该参数必填。- 当需要指定 ApplyInstanceNum 参数时，此参数为必填。- 每个白名单中最多支持设置 1000 个 IP 地址或 CIDR 格式的 IP 地址段。不允许设置重复的地址，多个地址间用英文逗号（,）隔开。特殊示例如下所示：- 设置 0.0.0.0/0，表示允许所有地址访问。- 设置 127.0.0.1，表示禁止所有地址访问。- 同时设置 0.0.0.0/0 和 127.0.0.1，表示允许所有地址访问。- 设置 CIDR 192.168.1.0/24，表示允许该网段内的 IP 地址访问。- 设置 192.168.1.1，表示仅允许该 IP 地址访问。)', examples=['192.168.1.0'])]] = None,
                      allow_list_desc: Optional[Annotated[str,Field(description='白名单的备注信息，长度不可超过 200 个字符。', examples=['test'])]] = None,
                      apply_instance_num: Optional[Annotated[int,Field(description='白名单所绑定的实例个数。(* 此参数用于确认本次修改的影响范围，避免误操作引发故障。* 当指定 AllowList 参数时，该参数必填，参数值为已绑定该白名单的实例总数。您可以调用DescribeAllowLists接口查询指定地域下白名单绑定的实例总数。)', examples=['1'])]] = None,
                      modify_mode: Optional[Annotated[str,Field(description='修改白名单的方式，支持设置为：* `Cover`（默认）：使用 AllowList 参数中的值覆盖原白名单。* `Append`：在原白名单中增加 AllowList 参数中输入的 IP 地址。* `Delete`：在原白名单中删除 AllowList 参数中输入的 IP 地址。至少需要保留一个 IP 地址。', examples=['Cover枚举值：Append,Cover,Delete'])]] = None) -> dict[str, Any]:
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
    description="查询目标白名单的详细信息，例如 IP 地址和绑定的实例详情"
)
def describe_allow_list_detail(allow_list_id: Annotated[str, Field(description='白名单 ID。', examples=['acl-d1fd76693bd54e658912e7337d5b****'])]) -> dict[str, Any]:
    """调用 DescribeAllowListDetail 接口查询目标白名单的详细信息，例如 IP 地址和绑定的实例详情。

    Args:
        allow_list_id (str): 白名单 ID。
            示例值：acl-d1fd76693bd54e658912e7337d5b****

    Returns: 包含以下字段的字典
        allow_list (str, optional): 白名单内的 IP 地址列表。
            示例值：10.1.***.***,10.2.***.***/24
        allow_list_desc (str, optional): 白名单的备注。
            示例值：test
        allow_list_id (str, optional): 白名单 ID。
            示例值：acl-d1fd76693bd54e658912e7337d5b****
        allow_list_name (str, optional): 白名单名称。
            示例值：test
        allow_list_type (str, optional): 白名单内的 IP 地址类型。当前仅支持指定为 `IPv4`，表示 IPv4 地址。
            示例值：IPv4
        associated_instance_num (int, optional): 绑定的全部实例数量。
            示例值：0
        associated_instances (list[dict[str, Any]], optional): 已绑定当前白名单的实例信息。
        project_name (str, optional): 所属项目名称。
            示例值：test_project
    """
    req = {
        "allow_list_id": allow_list_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_allow_list_detail(req)
    return resp.to_dict()


@mcp_server.tool(
    description="为指定的实例创建公网连接地址，即开启实例的公网访问功能"
)
def create_db_endpoint_public_address(instance_id: str,
                                      endpoint_id: Annotated[str, Field(description='连接终端 ID。(您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。)', examples=['vedbm-2pf2xk5v****-Custom-50yv'])],
                                      eip_id: Annotated[str, Field(description='实例需要绑定的 EIP ID。(您可以调用DescribeEipAddresses接口查询已创建的 EIP 的详细信息，包括 EIP ID。)', examples=['eip-2fef2qcfbfw8w5oxruw3w****'])]) -> dict[str, Any]:
    """调用 CreateDBEndpointPublicAddress 接口为指定的实例创建公网连接地址，即开启实例的公网访问功能。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        endpoint_id (str): 连接终端 ID。
            (
            您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。
            )
            示例值：vedbm-2pf2xk5v****-Custom-50yv
        eip_id (str): 实例需要绑定的 EIP ID。
            (
            您可以调用DescribeEipAddresses接口查询已创建的 EIP 的详细信息，包括 EIP ID。
            )
            示例值：eip-2fef2qcfbfw8w5oxruw3w****
    """
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
        "eip_id": eip_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_db_endpoint_public_address(req)
    return resp.to_dict()

@mcp_server.tool(
    description="删除目标白名单"
)
def delete_allow_list(allow_list_id: Annotated[str, Field(description='白名单 ID。', examples=['acl-d1fd76693bd54e658912e7337d5b****'])]) -> dict[str, Any]:
    """调用 DeleteAllowList 接口删除目标白名单。

    Args:
        allow_list_id (str): 白名单 ID。
            示例值：acl-d1fd76693bd54e658912e7337d5b****
    """
    req = {
        "allow_list_id": allow_list_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_allow_list(req)
    return resp.to_dict()

@mcp_server.tool(
    description="删除指定实例的公网连接地址，即关闭公网访问功能"
)
def delete_db_endpoint_public_address(instance_id: str,
                                      endpoint_id: Annotated[str, Field(description='连接终端 ID。(您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。)', examples=['vedbm-2pf2xk5v****-Custom-50yv'])]) -> dict[str, Any]:
    """调用 DeleteDBEndpointPublicAddress 接口删除指定实例的公网连接地址，即关闭公网访问功能。

    Args:
        instance_id (str): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        endpoint_id (str): 连接终端 ID。
            (
            您可以调用DescribeDBEndpoint接口，获取连接终端的详细信息，包括连接终端 ID。
            )
            示例值：vedbm-2pf2xk5v****-Custom-50yv
    """
    req = {
        "instance_id": instance_id,
        "endpoint_id": endpoint_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_db_endpoint_public_address(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询当前账号下指定地域内的所有 IP 白名单信息"
)
def describe_allow_lists(region_id: Annotated[str, Field(description='地域 ID。(您可以调用DescribeRegions接口查询可创建实例的地域信息，包括地域 ID。)', examples=['cn-beijing'])],
                         instance_id: Optional[Annotated[str,Field(description='实例 ID。', examples=['vedbm-r3xq0zdl****'])]] = None,
                         project_name: Optional[Annotated[str,Field(description='所属项目名称，创建时若该参数留空，则默认加入 `default` 项目。(项目是一个虚拟的概念，包括一组资源、用户和角色。通过项目可以对一组资源进行统一的查看和管理，并且控制项目内用户和角色管理这些资源的权限。更多详情，请参见[资源管理](https://www.volcengine.com/docs/6649/94333)。)', examples=['default'])]] = None) -> dict[str, Any]:
    """调用 DescribeAllowLists 接口查询当前账号下指定地域内的所有 IP 白名单信息。

    Args:
        region_id (str): 地域 ID。
            (
            您可以调用DescribeRegions接口查询可创建实例的地域信息，包括地域 ID。
            )
            示例值：cn-beijing
        instance_id (str, optional): 实例 ID。
            示例值：vedbm-r3xq0zdl****
        project_name (str, optional): 所属项目名称，创建时若该参数留空，则默认加入 `default` 项目。
            (
            项目是一个虚拟的概念，包括一组资源、用户和角色。通过项目可以对一组资源进行统一的查看和管理，并且控制项目内用户和角色管理这些资源的权限。更多详情，请参见[资源管理](https://www.volcengine.com/docs/6649/94333)。
            )
            示例值：default

    Returns: 包含以下字段的字典
        allow_lists (list[dict[str, Any]], optional): 白名单信息列表。
    """
    req = {
        "region_id": region_id,
        "instance_id": instance_id,
        "project_name": project_name,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_allow_lists(req)
    return resp.to_dict()
