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
mcp_server = FastMCP("rds_mysql_mcp_server", port=int(os.getenv("MCP_SERVER_PORT", "8000")))
logger = logging.getLogger("rds_mysql_mcp_server")

rds_mysql_resource = RDSMySQLSDK(
    region=os.getenv('VOLCENGINE_REGION'), ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY'), host=os.getenv('VOLCENGINE_ENDPOINT')
)

from typing import List, Dict, Any, Optional

@mcp_server.tool(
    name="describe_db_instances",
    description="查询RDS MySQL实例列表"
)
def describe_db_instances(
        page_number: int = Field(default=1, description="当前页页码，取值最小为1"),
        page_size: int = Field(default=10, description="每页记录数，最小值为1，最大值不超过1000"),
        instance_id: Optional[str] = Field(default=None, description="实例ID"),
        instance_name: Optional[str] = Field(default=None, description="实例名称"),
        instance_status: Optional[str] = Field(default=None, description="实例状态，如Running、Creating等"),
        db_engine_version: Optional[str] = Field(default=None, description="兼容版本，如MySQL_5_7、MySQL_8_0"),
        create_time_start: Optional[str] = Field(default=None, description="查询创建实例的开始时间"),
        create_time_end: Optional[str] = Field(default=None, description="查询创建实例的结束时间"),
        zone_id: Optional[str] = Field(default=None, description="实例所属可用区"),
        charge_type: Optional[str] = Field(default=None, description="计费类型，如PostPaid、PrePaid"),
        instance_type: Optional[str] = Field(default=None, description="实例类型，如DoubleNode"),
        node_spec: Optional[str] = Field(default=None, description="主节点规格"),
        tag_filters: Optional[List[Dict[str, str]]] = Field(default=None, description="用于查询筛选的标签键值对数组"),
        project_name: Optional[str] = Field(default=None, description="项目名称"),
        private_network_ip_address: Optional[str] = Field(default=None, description="实例默认终端的IP地址"),
        kernel_version: Optional[List[str]] = Field(default=None, description="内核小版本列表"),
        private_network_vpc_id: Optional[str] = Field(default=None, description="私有网络的ID"),
        storage_type: Optional[str] = Field(default=None, description="实例存储类型，如LocalSSD")
) -> dict[str, Any]:
    """
    查询RDS MySQL实例列表

    Args:
        page_number (int, optional): 当前页页码，取值最小为1，默认值为1
        page_size (int, optional): 每页记录数，最小值为1，最大值不超过1000，默认值为10
        instance_id (str, optional): 实例ID
        instance_name (str, optional): 实例名称
        instance_status (str, optional): 实例状态，如Running、Creating等
        db_engine_version (str, optional): 兼容版本，如MySQL_5_7、MySQL_8_0
        create_time_start (str, optional): 查询创建实例的开始时间
        create_time_end (str, optional): 查询创建实例的结束时间
        zone_id (str, optional): 实例所属可用区
        charge_type (str, optional): 计费类型，如PostPaid、PrePaid
        instance_type (str, optional): 实例类型，如DoubleNode
        node_spec (str, optional): 主节点规格
        tag_filters (List[Dict[str, str]], optional): 用于查询筛选的标签键值对数组
        project_name (str, optional): 项目名称
        private_network_ip_address (str, optional): 实例默认终端的IP地址
        kernel_version (List[str], optional): 内核小版本列表
        private_network_vpc_id (str, optional): 私有网络的ID
        storage_type (str, optional): 实例存储类型，如LocalSSD
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
        "instance_type": instance_type,
        "node_spec": node_spec,
        "tag_filters": tag_filters,
        "project_name": project_name,
        "page_number": page_number,
        "page_size": page_size,
        "private_network_ip_address": private_network_ip_address,
        "kernel_version": kernel_version,
        "private_network_vpc_id": private_network_vpc_id,
        "storage_type": storage_type
    }

    req = {k: v for k, v in req.items() if v is not None}

    if tag_filters is not None:
        for filter_item in tag_filters:
            if not isinstance(filter_item, dict) or 'Key' not in filter_item:
                raise ValueError("TagFilters中的每个元素必须是包含Key字段的字典")

    resp = rds_mysql_resource.describe_db_instances(req)
    return resp.to_dict()


@mcp_server.tool(name="describe_db_instance_detail", description="查询RDSMySQL实例详情")
def describe_db_instance_detail(
        instance_id: str = Field(description="实例ID")
) -> dict[str, Any]:
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
def describe_db_instance_engine_minor_versions(
        instance_ids: List[str] = Field(description="实例ID列表")
) -> dict[str, Any]:
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
        instance_id: str = Field(description="实例ID"),
        account_name: Optional[str] = Field(default=None, description="数据库账号名称，支持模糊查询"),
        page_number: int = Field(default=1, description="当前页页码，最小值为1"),
        page_size: int = Field(default=10, description="每页记录数，范围1-1000")
) -> dict[str, Any]:
    """查询RDS MySQL实例的数据库账号列表

    Args:
        instance_id (str): 实例ID
        account_name (Optional[str]): 数据库账号名称，支持模糊查询
        page_number (int): 当前页页码，最小值为1，默认1
        page_size (int): 每页记录数，范围1-1000，默认10
    """
    req = {
        "instance_id": instance_id,
        "page_number": page_number,
        "page_size": page_size
    }

    # 添加可选参数
    if account_name is not None:
        req["account_name"] = account_name

    resp = rds_mysql_resource.describe_db_accounts(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_databases",
    description="根据指定RDS MySQL 实例ID 查看数据库列表"
)
def describe_databases(
        instance_id: str = Field(description="实例ID"),
        db_name: Optional[str] = Field(default=None, description="数据库名称，支持模糊查询"),
        page_number: int = Field(default=1, description="当前页页码，最小值为1"),
        page_size: int = Field(default=10, description="每页记录数，范围1-1000")
) -> dict[str, Any]:
    """根据指定RDS MySQL 实例ID 查看数据库列表

    Args:
        instance_id (str): 实例ID
        db_name (Optional[str]): 数据库名称，支持模糊查询
        page_number (int): 当前页页码，最小值为1，默认1
        page_size (int): 每页记录数，范围1-1000，默认10
    """
    req = {
        "instance_id": instance_id,
        "page_number": page_number,
        "page_size": page_size
    }

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
        instance_id: str = Field(description="实例ID"),
        parameter_name: Optional[str] = Field(default=None, description="参数名"),
        node_id: Optional[str] = Field(default=None,
                                       description="查询指定节点的参数设置，如不设置该字段，只返回主节点和备节点的参数设置")
) -> dict[str, Any]:
    """
    获取RDS MySQL实例参数列表

    Args:
        instance_id (str): 实例ID
        parameter_name (str, optional): 参数名
        node_id (str, optional): 查询指定节点的参数设置，如不设置该字段，只返回主节点和备节点的参数设置
    """
    req = {
        "instance_id": instance_id,
        "parameter_name": parameter_name,
        "node_id": node_id
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mysql_resource.describe_db_instance_parameters(req)
    return resp.to_dict()


@mcp_server.tool(
    name="list_parameter_templates",
    description="查询MySQL实例的参数模板列表"
)
def list_parameter_templates(
    template_category: Optional[str] = Field(default=None, description="模板类别，取值为 DBEngine（数据库引擎参数）"),
    template_type: str = Field(default="Mysql", description="参数模板的数据库类型"),
    template_type_version: Optional[str] = Field(default=None, description="参数模板的数据库版本，如 MySQL_5_7 或 MySQL_8_0"),
    template_source: Optional[str] = Field(default=None, description="参数模板来源，取值范围：System（系统）、User（用户）"),
    limit: int = Field(default=10, description="每页记录数，范围1-100"),
    offset: int = Field(default=0, description="当前页查询偏移量"),
    project_name: Optional[str] = Field(default=None, description="所属项目名称"),
    template_name: Optional[str] = Field(default=None, description="模板名称")
) -> dict[str, Any]:
    """
    查询MySQL实例的参数模板列表

    Args:
        template_category (str, optional): 模板类别，取值为 DBEngine（数据库引擎参数）
        template_type (str, optional): 参数模板的数据库类型，默认值为 Mysql
        template_type_version (str, optional): 参数模板的数据库版本，如 MySQL_5_7 或 MySQL_8_0
        template_source (str, optional): 参数模板来源，取值范围：System（系统）、User（用户）
        limit (int, optional): 每页记录数，范围1-100，默认10
        offset (int, optional): 当前页查询偏移量，默认0
        project_name (str, optional): 所属项目名称
        template_name (str, optional): 模板名称
    """
    req = {
        "template_category": template_category,
        "template_type": template_type,
        "template_type_version": template_type_version,
        "template_source": template_source,
        "limit": limit,
        "offset": offset,
        "project_name": project_name,
        "template_name": template_name
    }
    req = {k: v for k, v in req.items() if v is not None}

    if 'Limit' in req and not (1 <= req['Limit'] <= 100):
        raise ValueError("Limit参数必须在1-100之间")

    if 'Offset' in req and req['Offset'] < 0:
        raise ValueError("Offset参数必须大于等于0")

    resp = rds_mysql_resource.list_parameter_templates(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_parameter_template",
    description="查询指定的参数模板详情"
)
def describe_parameter_template(
        template_id: str = Field(description="参数模板 ID"),
        project_name: Optional[str] = Field(default=None, description="所属项目名称")
) -> dict[str, Any]:
    """
    查询指定的参数模板详情

    Args:
        template_id (str): 参数模板 ID
        project_name (str, optional): 所属项目名称
    """
    req = {
        "template_id": template_id,
        "project_name": project_name
    }
    req = {k: v for k, v in req.items() if v is not None}

    if not template_id:
        raise ValueError("template_id是必选参数")

    resp = rds_mysql_resource.describe_parameter_template(req)
    return resp.to_dict()


@mcp_server.tool(
    name="describe_db_instance_price_detail",
    description="查询数据库实例价格详情"
)
def describe_db_instance_price_detail(
        node_info: list[dict[str, Any]] = Field(description="实例的节点配置列表，每个节点配置包含NodeType、NodeSpec等字段"),
        storage_type: str = Field(description="实例存储类型，取值为 LocalSSD，表示本地 SSD 盘"),
        storage_space: int = Field(description="实例存储空间，取值范围：[20, 3000]，单位：GB，步长 10GB"),
        charge_type: str = Field(description="计费类型，取值：PostPaid（按量付费）、PrePaid（包年包月）"),
        node_id: Optional[str] = Field(default=None, description="节点 ID，创建实例或新增节点时无需传入，变更节点配置或删除节点时必传"),
        zone_id: Optional[str] = Field(default=None, description="节点所在可用区，创建实例和新增节点时必传，变更配置或删除节点时可不传"),
        node_operate_type: Optional[str] = Field(default=None, description="操作类型，创建实例时无需传入，修改配置时必传，取值：Create、Modify"),
        period_unit: Optional[str] = Field(default=None, description="预付费场景下的购买周期，取值：Month（月）、Year（年），ChargeType为PostPaid时无需传入"),
        period: Optional[int] = Field(default=None, description="预付费模式下的时长数量"),
        number: Optional[int] = Field(default=1, description="实例个数"),
        project_name: Optional[str] = Field(default=None, description="所属的项目，子账号场景下需传入有权限的项目名称"),
        proxy_node_custom: Optional[dict[str, Any]] = Field(default=None, description="实例的代理配置")
) -> dict[str, Any]:
    """
    查询数据库实例价格详情

    Args:
        node_info (list[dict[str, Any]]): 实例的节点配置列表，必选
        storage_type (str): 实例存储类型，必选
        storage_space (int): 实例存储空间，必选
        charge_type (str): 计费类型，必选
        node_id (str, optional): 节点 ID，可选
        zone_id (str, optional): 节点所在可用区，可选
        node_operate_type (str, optional): 操作类型，可选
        period_unit (str, optional): 预付费购买周期，可选
        period (int, optional): 预付费时长数量，可选
        number (int, optional): 实例个数，默认为1
        project_name (str, optional): 所属项目名称，可选
        proxy_node_custom (dict[str, Any], optional): 代理配置，可选
    """
    req = {
        "node_info": node_info,
        "storage_type": storage_type,
        "storage_space": storage_space,
        "charge_type": charge_type,
        "node_id": node_id,
        "zone_id": zone_id,
        "period_unit": period_unit,
        "period": period,
        "number": number,
        "project_name": project_name,
    }
    req = {k: v for k, v in req.items() if v is not None}

    # 必选参数校验
    if not node_info:
        raise ValueError("node_info是必选参数")
    if not all(
        node.get("NodeType") in ["Primary", "Secondary", "ReadOnly"] and
        node.get("NodeSpec")
        for node in node_info
    ):
        raise ValueError("node_info中的每个节点必须包含有效的NodeType和NodeSpec字段")
    if not storage_type:
        raise ValueError("storage_type是必选参数")
    if storage_space is None or not (20 <= storage_space <= 3000 and storage_space % 10 == 0):
        raise ValueError("storage_space是必选参数，取值范围：[20, 3000]，步长10GB")
    if not charge_type:
        raise ValueError("charge_type是必选参数")
    if charge_type == "PrePaid" and (period_unit is None or period is None):
        raise ValueError("预付费模式下period_unit和period是必选参数")
    if node_operate_type and node_operate_type not in ["Create", "Modify"]:
        raise ValueError("node_operate_type必须是Create或Modify")

    resp = rds_mysql_resource.describe_db_instance_price_detail(req)
    return resp.to_dict()


@mcp_server.tool(
    name="modify_db_instance_name",
    description="修改RDS MySQL实例名称"
)
def modify_db_instance_name(
        instance_id: str = Field(description="实例 ID"),
        instance_new_name: str = Field(
            description="实例的新名称。命名规则：不能以数字、中划线开头，只能包含中文、字母、数字、下划线和中划线，长度限制在 1~128 之间")
) -> dict[str, Any]:
    """
    修改RDS MySQL实例名称

    Args:
        instance_id (str): 实例 ID
        instance_new_name (str): 实例的新名称。命名规则：
            - 不能以数字、中划线开头
            - 只能包含中文、字母、数字、下划线和中划线
            - 长度限制在 1~128 之间
    """
    if not instance_id:
        raise ValueError("instance_id是必选参数")

    if not instance_new_name:
        raise ValueError("instance_new_name是必选参数")

    import re
    if not re.match(r'^[^\d-][\w\-\u4e00-\u9fa5]{0,127}$', instance_new_name):
        raise ValueError("实例名称不符合命名规则：不能以数字、中划线开头，只能包含中文、字母、数字、下划线和中划线，长度1~128")

    req = {
        "instance_id": instance_id,
        "instance_new_name": instance_new_name
    }

    resp = rds_mysql_resource.modify_db_instance_name(req)
    return resp.to_dict()


@mcp_server.tool(
    name="modify_db_account_description",
    description="修改RDS MySQL实例账号的描述信息"
)
def modify_db_account_description(
        instance_id: str = Field(description="实例 ID"),
        account_name: str = Field(description="数据库账号名称"),
        host: str = Field(default="%", description="指定账号访问数据库的 IP 地址，默认值为 %"),
        account_desc: Optional[str] = Field(default=None, description="数据库账号的描述信息，长度不超过 256 个字符")
) -> dict[str, Any]:
    """
    修改RDS MySQL实例账号的描述信息

    Args:
        instance_id (str): 实例 ID
        account_name (str): 数据库账号名称
        host (str, optional): 指定账号访问数据库的 IP 地址，默认值为 %。
            - 若指定为 %，允许该账号从任意 IP 地址访问数据库
            - 支持使用通配符设定可访问数据库的 IP 地址段
            - 如指定 Host 为 192.10.10.%，则表示该账号可从 192.10.10.0~192.10.10.255 之间的 IP 地址访问数据库
            - 指定的 Host 需要添加在实例所绑定的白名单中
            - 如创建的账号类型为高权限账号，主机 IP 只能指定为 %
        account_desc (str, optional): 数据库账号的描述信息，长度不超过 256 个字符。
            - 该字段可选，如果不设置该字段，或者设置了该字段但传入空字符串（即长度为 0），则会清空原有备注
    """
    if not instance_id:
        raise ValueError("instance_id是必选参数")

    if not account_name:
        raise ValueError("account_name是必选参数")

    if account_desc is not None and len(account_desc) > 256:
        raise ValueError("account_desc长度不能超过256个字符")

    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "host": host,
        "account_desc": account_desc
    }

    req = {k: v for k, v in req.items() if v is not None}

    resp = rds_mysql_resource.modify_db_account_description(req)
    return resp.to_dict()


@mcp_server.tool(
    name="create_rds_mysql_instance",
    description="创建 RDS MySQL 实例"
)
def create_rds_mysql_instance(
        vpc_id: str = Field(title="私有网络 ID", description="需要使用describe_vpcs获取"),
        subnet_id: str = Field(title="子网 ID", description="需要使用describe_subnets获取，subnet_id只有一个可用区属性，多可用区时找到一个与主节点或者备节点所在的可用区相同的即可"),
        db_engine_version: str = Field(default="MySQL_8_0", description="数据库版本"),
        instance_name: Optional[str] = Field(default=None, description="实例名称"),
        primary_zone: str = Field(default="cn-beijing-a", description="主节点可用区"),
        primary_spec: str = Field(default="rds.mysql.1c2g", description="主节点规格"),
        secondary_count: int = Field(default=1, description="备节点数量"),
        secondary_zone: Optional[str] = Field(default=None, description="备节点可用区，默认与主节点相同，多可用区需要不同"),
        secondary_spec: str = Field(default="rds.mysql.1c2g", description="备节点规格"),
        read_only_count: int = Field(default=0, description="只读节点数量"),
        read_only_zone: str = Field(default="cn-beijing-a", description="只读节点可用区"),
        read_only_spec: str = Field(default="rds.mysql.1c2g", description="只读节点规格"),
        storage_space: int = Field(default=20, description="存储空间大小(GB)"),
        storage_type: str = Field(default="LocalSSD", description="存储类型"),
        charge_type: str = Field(default="PostPaid", description="付费类型"),
        auto_renew: Optional[bool] = Field(default=None, description="预付费场景下是否自动续费"),
        period_unit: Optional[str] = Field(default=None, description="预付费场景下的购买周期(Month/Year)"),
        period: Optional[int] = Field(default=None, description="预付费场景下的购买时长"),
        instance_type: str = Field(
                    default="DoubleNode",
                    description="实例类型，可选值：DoubleNode（双节点）、MultiNode（多节点）",
                    choices=["DoubleNode", "MultiNode"]
                ),
        super_account_name: Optional[str] = Field(default=None, description="高权限账号名称"),
        super_account_password: Optional[str] = Field(default=None, description="高权限账号密码"),
        lower_case_table_names: str = Field(default="1", description="表名是否区分大小写"),
        db_time_zone: Optional[str] = Field(default=None, description="时区"),
        db_param_group_id: Optional[str] = Field(default=None, description="参数模板 ID"),
        project_name: Optional[str] = Field(default=None, description="实例所属项目"),
        allow_list_ids: Optional[List[str]] = Field(default=None, description="白名单 ID 列表"),
        port: int = Field(default=3306, description="默认终端的私网端口"),
        instance_tags: Optional[List[Dict]] = Field(default=None, description="实例标签列表"),
        maintenance_window: Optional[Dict] = Field(default=None, description="维护窗口配置")
) -> dict[str, Any]:
    """创建 RDS MySQL 实例

    Args:
        vpc_id: 私有网络 ID
        subnet_id: 子网 ID
        db_engine_version: 数据库版本，默认 MySQL_8_0
        instance_name: 实例名称
        primary_zone: 主节点可用区，默认 cn-beijing-a
        primary_spec: 主节点规格，默认 rds.mysql.1c2g
        secondary_count: 备节点数量，默认 1
        secondary_zone: 备节点可用区，默认与主节点相同
        secondary_spec: 备节点规格，默认 rds.mysql.1c2g
        read_only_count: 只读节点数量，默认 0
        read_only_zone: 只读节点可用区，默认 cn-beijing-a
        read_only_spec: 只读节点规格，默认 rds.mysql.1c2g
        storage_space: 存储空间大小(GB)，默认 20
        storage_type: 存储类型，默认 LocalSSD
        charge_type: 付费类型，默认 PostPaid
        auto_renew: 预付费场景下是否自动续费
        period_unit: 预付费场景下的购买周期(Month/Year)
        period: 预付费场景下的购买时长
        instance_type: 实例类型，默认 DoubleNode
        super_account_name: 高权限账号名称
        super_account_password: 高权限账号密码
        lower_case_table_names: 表名是否区分大小写，默认 1
        db_time_zone: 时区
        db_param_group_id: 参数模板 ID
        project_name: 实例所属项目
        allow_list_ids: 白名单 ID 列表
        port: 默认终端的私网端口，默认 3306
        instance_tags: 实例标签列表
        maintenance_window: 维护窗口配置

    Returns:
        dict: 创建结果，包含实例ID和订单号等信息
    """
    node_info = []

    node_info.append({
        "NodeType": "Primary",
        "ZoneId": primary_zone,
        "NodeSpec": primary_spec
    })

    for i in range(secondary_count):
        zone = secondary_zone or primary_zone
        node_info.append({
            "NodeType": "Secondary",
            "ZoneId": zone,
            "NodeSpec": secondary_spec
        })


    for i in range(read_only_count):
        node_info.append({
            "NodeType": "ReadOnly",
            "ZoneId": read_only_zone,
            "NodeSpec": read_only_spec
        })

    data = {
        "db_engine_version": db_engine_version,
        "node_info": node_info,
        "storage_type": storage_type,
        "storage_space": storage_space,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "instance_type": instance_type,
        "lower_case_table_names": lower_case_table_names,
        "port": port,
        "charge_info": {
            "ChargeType": charge_type,
            "AutoRenew": auto_renew,
            "PeriodUnit": period_unit,
            "Period": period
        }
    }


    if instance_name is not None:
        data["instance_name"] = instance_name

    if super_account_name is not None:
        data["super_account_name"] = super_account_name

    if super_account_password is not None:
        data["super_account_password"] = super_account_password

    if db_time_zone is not None:
        data["db_time_zone"] = db_time_zone

    if db_param_group_id is not None:
        data["db_param_group_id"] = db_param_group_id

    if project_name is not None:
        data["project_name"] = project_name

    if allow_list_ids is not None:
        data["allow_list_ids"] = allow_list_ids

    if instance_tags is not None:
        data["instance_tags"] = instance_tags

    if maintenance_window is not None:
        data["maintenance_window"] = maintenance_window

    resp = rds_mysql_resource.create_db_instance(data)
    return resp.to_dict()


@mcp_server.tool(
    name="create_database",
    description="创建RDS MySQL实例数据库"
)
def create_database(
        instance_id: str = Field(description="实例 ID"),
        db_name: str = Field(description="数据库名称。命名规则：名称唯一，长度为 2~64 个字符，以字母开头，以字母或数字结尾，由字母、数字、下划线或中划线组成，不能使用预留字"),
        character_set_name: str = Field(default="utf8mb4", description="数据库字符集，支持：utf8、utf8mb4、latin1、ascii"),
        database_privileges: Optional[List[Dict]] = Field(default=None, description="授权数据库权限信息"),
        db_desc: Optional[str] = Field(default=None, description="数据库的描述信息，长度不超过 256 个字符")
) -> dict[str, Any]:
    """
    创建RDS MySQL实例数据库

    Args:
        instance_id (str): 实例 ID
        db_name (str): 数据库名称。命名规则：
            - 名称唯一
            - 长度为 2~64 个字符
            - 以字母开头，以字母或数字结尾
            - 由字母、数字、下划线（_）或中划线（-）组成
            - 不能使用某些预留字，包括 root、admin 等
        character_set_name (str, optional): 数据库字符集，默认为 utf8mb4。支持：utf8、utf8mb4、latin1、ascii
        database_privileges (list[dict], optional): 授权数据库权限信息，每个权限项包含：
            - AccountName (str): 需授权的账号名称（必选）
            - Host (str, optional): 指定的数据库账号可以访问数据库的 IP 地址，默认值为 %
            - AccountPrivilege (str): 授予的账号权限类型，取值：ReadWrite、ReadOnly、DDLOnly、DMLOnly、Custom
            - AccountPrivilegeDetail (str, optional): 当 AccountPrivilege 为 Custom 时必填，指定具体权限
        db_desc (str, optional): 数据库的描述信息，长度不超过 256 个字符
    """
    if not instance_id:
        raise ValueError("instance_id是必选参数")

    if not db_name:
        raise ValueError("db_name是必选参数")

    valid_charsets = {"utf8", "utf8mb4", "latin1", "ascii"}
    if character_set_name not in valid_charsets:
        raise ValueError(f"无效的字符集: {character_set_name}，支持的字符集为: {', '.join(valid_charsets)}")

    if db_desc is not None and len(db_desc) > 256:
        raise ValueError("db_desc长度不能超过256个字符")

    req = {
        "instance_id": instance_id,
        "db_name": db_name,
        "character_set_name": character_set_name,
        "database_privileges": database_privileges,
        "db_desc": db_desc
    }

    req = {k: v for k, v in req.items() if v is not None}

    resp = rds_mysql_resource.create_database(req)
    if resp is None:
        return {
            "Message": "Success"
        }


@mcp_server.tool(
    name="create_allow_list",
    description="创建RDS MySQL实例白名单"
)
def create_allow_list(
        allow_list_name: str = Field(..., title="白名单名称", description="需满足：不能以数字或中划线（-）开头，只能包含中文、字母、数字、下划线（_）和中划线（-），长度需为 1~128 个字符"),
        allow_list_desc: str = Field(None, description="长度不可超过 200 个字符"),
        allow_list_type: str = Field("IPv4", description="白名单内的 IP 地址类型，当前仅支持 IPv4 地址"),
        allow_list: str = Field(None, description="输入 IP 地址或 CIDR 格式的 IP 地址段，多个地址间用英文逗号（,）隔开，每个白名单分组中最多支持设置 300 个 IP 地址或 CIDR 格式的 IP 地址段，不允许设置重复的地址，该字段不能与 UserAllowList 字段同时使用"),
        security_group_ids: list[str] = Field(None, description="需要关联的安全组 ID 列表，单个白名单单次最多可选择添加 10 个安全组，该字段不能与 SecurityGroupBindInfos 同时使用"),
        security_group_bind_infos: list[dict] = Field(None, description="白名单关联的安全组的信息，每个信息包含：BindMode (str): 关联安全组的模式，取值：IngressDirectionIp（入方向 IP）、AssociateEcsIp（关联 ECSIP）；SecurityGroupId (str): 安全组 ID；IpList (list[str], optional): 安全组的 IP；SecurityGroupName (str, optional): 安全组名称；该字段不能与 SecurityGroupIds 同时使用"),
        allow_list_category: str = Field("Ordinary", description="白名单分类，取值：Ordinary（普通白名单）、Default（默认白名单），默认值为 Ordinary"),
        user_allow_list: str = Field(None, description="安全组之外的、需要加入白名单的 IP 地址，可输入 IP 地址或 CIDR 格式的 IP 地址段，该字段不能与 AllowList 字段同时使用"),
        project_name: str = Field(None, description="所属的项目")
) -> dict[str, Any]:
    """
    创建RDS MySQL实例白名单

    Args:
        allow_list_name (str): 白名单名称，需满足：
            - 不能以数字或中划线（-）开头
            - 只能包含中文、字母、数字、下划线（_）和中划线（-）
            - 长度需为 1~128 个字符
        allow_list_desc (str, optional): 白名单的备注信息，长度不可超过 200 个字符
        allow_list_type (str, optional): 白名单内的 IP 地址类型，当前仅支持 IPv4 地址
        allow_list (str, optional): 输入 IP 地址或 CIDR 格式的 IP 地址段，多个地址间用英文逗号（,）隔开
            - 每个白名单分组中最多支持设置 300 个 IP 地址或 CIDR 格式的 IP 地址段
            - 不允许设置重复的地址
            - 该字段不能与 UserAllowList 字段同时使用
        security_group_ids (list[str], optional): 需要关联的安全组 ID 列表，单个白名单单次最多可选择添加 10 个安全组
            - 该字段不能与 SecurityGroupBindInfos 同时使用
        security_group_bind_infos (list[dict], optional): 白名单关联的安全组的信息，每个信息包含：
            - BindMode (str): 关联安全组的模式，取值：IngressDirectionIp（入方向 IP）、AssociateEcsIp（关联 ECSIP）
            - SecurityGroupId (str): 安全组 ID
            - IpList (list[str], optional): 安全组的 IP
            - SecurityGroupName (str, optional): 安全组名称
            - 该字段不能与 SecurityGroupIds 同时使用
        allow_list_category (str, optional): 白名单分类，取值：Ordinary（普通白名单）、Default（默认白名单），默认值为 Ordinary
        user_allow_list (str, optional): 安全组之外的、需要加入白名单的 IP 地址，可输入 IP 地址或 CIDR 格式的 IP 地址段
            - 该字段不能与 AllowList 字段同时使用
        project_name (str, optional): 所属的项目
    """
    # 验证必选参数
    if not allow_list_name:
        raise ValueError("allow_list_name是必选参数")

    # 验证白名单名称格式
    import re
    if not re.match(r'^[^\d-][\w\-\u4e00-\u9fa5]{0,127}$', allow_list_name):
        raise ValueError(
            "白名单名称不符合命名规则：不能以数字或中划线开头，只能包含中文、字母、数字、下划线和中划线，长度1~128")

    # 验证描述信息长度
    if allow_list_desc is not None and len(allow_list_desc) > 200:
        raise ValueError("allow_list_desc长度不能超过200个字符")

    # 验证IP地址类型
    valid_allow_list_types = {"IPv4"}
    if allow_list_type not in valid_allow_list_types:
        raise ValueError(f"无效的allow_list_type: {allow_list_type}，支持的类型为: {', '.join(valid_allow_list_types)}")

    # 验证白名单分类
    valid_categories = {"Ordinary", "Default"}
    if allow_list_category not in valid_categories:
        raise ValueError(
            f"无效的allow_list_category: {allow_list_category}，支持的分类为: {', '.join(valid_categories)}")

    # 验证AllowList和UserAllowList不能同时存在
    if allow_list is not None and user_allow_list is not None:
        raise ValueError("allow_list和user_allow_list字段不能同时使用")

    # 验证SecurityGroupIds和SecurityGroupBindInfos不能同时存在
    if security_group_ids is not None and security_group_bind_infos is not None:
        raise ValueError("security_group_ids和security_group_bind_infos字段不能同时使用")

    # 验证SecurityGroupIds长度
    if security_group_ids is not None and len(security_group_ids) > 10:
        raise ValueError("security_group_ids最多只能包含10个安全组ID")

    req = {
        "allow_list_name": allow_list_name,
        "allow_list_desc": allow_list_desc,
        "allow_list_type": allow_list_type,
        "allow_list": allow_list,
        "security_group_ids": security_group_ids,
        "security_group_bind_infos": security_group_bind_infos,
        "allow_list_category": allow_list_category,
        "user_allow_list": user_allow_list,
        "project_name": project_name
    }

    req = {k: v for k, v in req.items() if v is not None}

    # 调用接口
    resp = rds_mysql_resource.create_allow_list(req)
    return resp.to_dict()


@mcp_server.tool(
    name="associate_allow_list",
    description="绑定RDS MySQL实例与白名单"
)
def associate_allow_list(
    instance_ids: list[str] = Field(
            title="实例ID列表",
            description=(
                "需要绑定白名单的实例ID列表\n"
                "- 支持一次传入多个实例ID，单次最多可传入200个实例ID\n"
                "- 不支持同时传入多个实例ID和多个白名单ID，仅允许：\n"
                "  - 将多个实例同时绑定到同一个白名单（此时allow_list_ids长度应为1）\n"
                "  - 或将一个实例同时绑定到多个白名单（此时instance_ids长度应为1）"
            ),
            min_items=1,
            max_items=200
        ),
    allow_list_ids: list[str] = Field(
            title="白名单ID列表",
            description=(
                "需要绑定实例的白名单ID列表\n"
                "- 支持一次传入多个白名单ID，单次最多可传入100个白名单ID\n"
                "- 不支持同时传入多个实例ID和多个白名单ID，仅允许：\n"
                "  - 将多个实例同时绑定到同一个白名单（此时allow_list_ids长度应为1）\n"
                "  - 或将一个实例同时绑定到多个白名单（此时instance_ids长度应为1）"
            ),
            min_items=1,
            max_items=100
        )
) -> dict[str, Any]:
    """
    绑定RDS MySQL实例与白名单

    Args:
        instance_ids (list[str]): 需要绑定白名单的实例 ID 列表
            - 支持一次传入多个实例 ID，单次最多可传入 200 个实例 ID
            - 不支持同时传入多个实例 ID 和多个白名单 ID，仅允许：
                - 将多个实例同时绑定到同一个白名单（此时 allow_list_ids 长度应为 1）
                - 或将一个实例同时绑定到多个白名单（此时 instance_ids 长度应为 1）
        allow_list_ids (list[str]): 需要绑定实例的白名单 ID 列表
            - 支持一次传入多个白名单 ID，单次最多可传入 100 个白名单 ID
            - 不支持同时传入多个实例 ID 和多个白名单 ID，仅允许：
                - 将多个实例同时绑定到同一个白名单（此时 allow_list_ids 长度应为 1）
                - 或将一个实例同时绑定到多个白名单（此时 instance_ids 长度应为 1）
    """
    if not instance_ids:
        raise ValueError("instance_ids是必选参数，不能为空列表")

    if not allow_list_ids:
        raise ValueError("allow_list_ids是必选参数，不能为空列表")

    if len(instance_ids) > 200:
        raise ValueError("单次最多可传入200个实例ID")

    if len(allow_list_ids) > 100:
        raise ValueError("单次最多可传入100个白名单ID")

    if len(instance_ids) > 1 and len(allow_list_ids) > 1:
        raise ValueError(
            "不支持同时传入多个实例ID和多个白名单ID，仅允许：将多个实例绑定到同一个白名单，或将一个实例绑定到多个白名单")

    req = {
        "instance_ids": instance_ids,
        "allow_list_ids": allow_list_ids
    }

    resp = rds_mysql_resource.associate_allow_list(req)
    if resp is None:
        return {
            "Message": "Success"
        }


@mcp_server.tool(
    name="create_db_account",
    description="创建RDS MySQL实例数据库账号"
)
def create_db_account(
    instance_id: str = Field(
            title="实例ID",
            description="需要创建账号的RDS MySQL实例ID"
        ),
    account_name: str = Field(
            title="数据库账号名称",
            description=(
                "数据库账号名称，规则：\n"
                "- 长度为2~32个字符\n"
                "- 以字母开头，以字母或数字结尾\n"
                "- 由字母、数字、下划线（_）和中划线（-）组成\n"
                "- 账号名称在实例内必须唯一\n"
                "- 不能使用某些预留字（高权限账号除外）"
            )
        ),
    account_password: str = Field(
            title="数据库账号密码",
            description=(
                "数据库账号密码，规则：\n"
                "- 长度为8~32个字符\n"
                "- 由大写字母、小写字母、数字、特殊字符中的至少三种组成\n"
                "- 特殊字符为!@#$%^&*()_+-=,.&?|/"
            )
        ),
    account_type:  str = Field(
            title="数据库账号类型",
            description="取值范围：Super（高权限账号，一个实例只能创建一个）或Normal（普通账号）"
        ),
    account_desc: str = Field(
            None,
            title="账号描述",
            description="账号信息描述，长度不超过256个字符",
            max_length=256
        ),
    host: str = Field(
            "%",
            title="访问IP地址",
            description=(
                "指定账号访问数据库的IP地址，默认值为%。\n"
                "若指定为%，允许从任意IP地址访问；\n"
                "高权限账号的主机IP只能指定为%"
            )
        ),
    account_privileges: str = Field(
            None,
            title="数据库权限信息",
            description=(
                "账号的指定数据库权限信息，每个权限项包含：\n"
                "- DBName (str): 数据库名称\n"
                "- AccountPrivilege (str): 权限类型（ReadWrite、ReadOnly等）\n"
                "- AccountPrivilegeDetail (str, optional): 当权限类型为Custom或Global时必填"
            )
        ),
    dry_run: bool = Field(
            False,
            title="是否预览SQL",
            description="是否预览创建账号的SQL语句，默认值为false"
        ),
    table_column_privileges: list[dict] = Field(
            None,
            title="表列权限设置",
            description=(
                "账号的表列权限设置，包含：\n"
                "- DBName (str): 数据库名称\n"
                "- TablePrivileges (list[dict], optional): 表权限信息\n"
                "- ColumnPrivileges (list[dict], optional): 列权限信息"
            )
        )
) -> dict[str, Any]:
    """
    创建RDS MySQL实例数据库账号

    Args:
        instance_id (str): 实例 ID
        account_name (str): 数据库账号名称。命名规则：
            - 长度为 2~32 个字符
            - 以字母开头，以字母或数字结尾
            - 由字母、数字、下划线（_）和中划线（-）组成
            - 账号名称在实例内必须是唯一的
            - 不能使用某些预留字（高权限账号除外）
        account_password (str): 数据库账号的密码。规则：
            - 长度为 8~32 个字符
            - 由大写字母、小写字母、数字、特殊字符中的至少三种组成
            - 特殊字符为 !@#$%^&*()_+-=,.&?|/
        account_type (str): 数据库账号类型，取值范围：
            - Super：高权限账号，一个实例只能创建一个
            - Normal：普通账号
        account_desc (str, optional): 账号信息描述信息，长度不超过 256 个字符
        host (str, optional): 指定账号访问数据库的 IP 地址，默认值为 %。
            - 若指定为 %，允许该账号从任意 IP 地址访问数据库
            - 如创建的账号类型为高权限账号，主机 IP 只能指定为 %
        account_privileges (list[dict], optional): 账号的指定数据库权限信息，每个权限项包含：
            - DBName (str): 需修改账号授权的或账号已有权限的数据库名称
            - AccountPrivilege (str): 数据库权限的类型，取值：ReadWrite、ReadOnly、DDLOnly、DMLOnly、Custom、Global、None
            - AccountPrivilegeDetail (str, optional): 账号的权限信息，当 AccountPrivilege 为 Custom 或 Global 时必填
        dry_run (bool, optional): 是否预览创建账号的 SQL 语句，默认值为 false
        table_column_privileges (list[dict], optional): 账号的表列权限设置，包含：
            - DBName (str): 对账号进行权限设置的表所属的数据库的名称
            - TablePrivileges (list[dict], optional): 账号的表权限信息，包含：
                - TableName (str): 表名
                - AccountPrivilegeDetail (str): 表权限，如 "ALTER,CREATE"
            - ColumnPrivileges (list[dict], optional): 账号的列权限信息，包含：
                - TableName (str): 表名
                - ColumnName (str): 列名
                - AccountPrivilegeDetail (str): 列权限，如 "UPDATE,INSERT"
    """
    if not instance_id:
        raise ValueError("instance_id是必选参数")

    if not account_name:
        raise ValueError("account_name是必选参数")

    if not account_password:
        raise ValueError("account_password是必选参数")

    if not account_type:
        raise ValueError("account_type是必选参数")

    import re
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]{0,30}[a-zA-Z0-9]$', account_name):
        raise ValueError(
            "账号名称不符合命名规则：长度为2~32个字符，以字母开头，以字母或数字结尾，由字母、数字、下划线或中划线组成")

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

    valid_account_types = {"Super", "Normal"}
    if account_type not in valid_account_types:
        raise ValueError(f"无效的account_type: {account_type}，支持的类型为: {', '.join(valid_account_types)}")

    if account_type == "Super" and host != "%":
        raise ValueError("当account_type为Super时，Host的取值只能为%")

    if account_desc is not None and len(account_desc) > 256:
        raise ValueError("account_desc长度不能超过256个字符")

    req = {
        "instance_id": instance_id,
        "account_name": account_name,
        "account_desc": account_desc,
        "host": host,
        "account_password": account_password,
        "account_type": account_type,
        "account_privileges": account_privileges,
        "dry_run": dry_run,
        "table_column_privileges": table_column_privileges
    }

    req = {k: v for k, v in req.items() if v is not None}

    resp = rds_mysql_resource.create_db_account(req)
    if resp is None:
        return {
            "Message": "Success"
        }



@mcp_server.tool(
    name="describe_vpcs",
    description="查询满足指定条件的VPC，用于创建实例"
)
def describe_vpcs(
        page_number: int = Field(default=1, description="当前页页码，最小值为1"),
        page_size: int = Field(default=5, description="每页记录数，范围1-1000")
) -> dict[str, Any]:
    if not page_number:
        page_number = 1
    if not page_size:
        page_size = 5
    req = {
        "page_number": page_number,
        "page_size": page_size
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mysql_resource.describe_vpcs(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_subnets",
    description="查询满足指定条件的子网，用于创建实例"
)
def describe_subnets(
        vpc_id: str = Field(
            ...,
            description="VPC ID",
        ),
        zone_id: str = Field(
            "cn-beijing-a",
            description="可用区ID，默认为cn-beijing-a，主节点或备节点所在的可用区",
        ),
) -> dict[str, Any]:
    req = {
        "vpc_id": vpc_id,
        "zone_id": zone_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = rds_mysql_resource.describe_subnets(req)
    return resp.to_dict()

def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the RDS MySQL MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting RDS MySQL MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting RDS MySQL MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
