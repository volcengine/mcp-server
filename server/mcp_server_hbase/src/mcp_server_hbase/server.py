import os
import re
import argparse
import logging
from typing import List, Dict, Any, Optional, Annotated
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from mcp_server_hbase.resource.hbase_resource import HBASESDK

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

mcp_server = FastMCP("hbase_mcp_server",
                     host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
                     port=int(os.getenv("PORT", "8000")),
                     stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
                     streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))

hbase_resource_sdk = HBASESDK(region=os.getenv('VOLCENGINE_REGION','cn-beijing'), ak=os.getenv('VOLCENGINE_ACCESS_KEY'), sk=os.getenv('VOLCENGINE_SECRET_KEY'), host=os.getenv('VOLCENGINE_ENDPOINT'))


@mcp_server.tool(
    name="modify_db_instance_name",
    description="调用 ModifyDBInstanceName 接口修改实例名称。"
)
def modify_db_instance_name(instance_name: Annotated[str, Field(description='修改后的实例新名称。名称需同时满足以下要求：- 不能以数字、中划线（-）开头。- 只能包含中文、字母、数字、下划线和中划线, 长度需要在 1~128 个字符内。', examples=['test_api'])],
                            instance_id: Annotated[str, Field(description='实例 ID', examples=['hb-cn019f341d51****'])],
                            client_token: Optional[Annotated[str,Field(description='用于保证请求的幂等性，防止重复提交请求。由客户端生成该参数值，要保证在不同请求间唯一，大小写敏感且不超过 127 个 ASCII 字符。', examples=['WbiAlPqJM6tMoSOYhT****'])]] = None) -> dict[str, Any]:
    """调用 ModifyDBInstanceName 接口修改实例名称。

    Args:
        instance_name (str): 修改后的实例新名称。名称需同时满足以下要求：
            - 不能以数字、中划线（-）开头。
            - 只能包含中文、字母、数字、下划线和中划线。
            - 长度需要在 1~128 个字符内。
            示例值：test_api
        instance_id (str): 实例 ID。
            :::tip
            您可以调用[DescribeDBInstances](https://www.volcengine.com/docs/6695/152923)接口查询目标地域下所有 HBase 实例的基本信息，包括实例 ID。
            :::
            示例值：hb-cn019f341d51****
        client_token (str, optional): 用于保证请求的幂等性，防止重复提交请求。由客户端生成该参数值，要保证在不同请求间唯一，大小写敏感且不超过 127 个 ASCII 字符。
            示例值：WbiAlPqJM6tMoSOYhT****
    """
    req = {
        "instance_name": instance_name,
        "instance_id": instance_id,
        "client_token": client_token,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = hbase_resource_sdk.modify_db_instance_name(req)
    return {
        "success": True,
        "message": f"实例 {instance_id} 已修改名称为 {instance_name}"
    }

@mcp_server.tool(
    name="create_db_instance",
    description="创建实例"
)
def create_db_instance(engine_version: Annotated[str, Field(description='HBase 数据库引擎版本。当前仅支持 HBase 2.0 版本，取值为`HBase_2.0`。', examples=['HBase_2.0'])],
                       zone_id: Annotated[str, Field(description='可用区 ID。- 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，则只需输入一个可用区 ID。- 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，则需要输入两个不同的可用区 ID，第一个为主可用区 ID，第二个为备可用区 ID，多个可用区 ID 之间使用英文逗号（,）分隔。:::tip您可以调用[DescribeZones](https://www.volcengine.com/docs/6695/152922)接口查询 HBase 实例指定地域下所有可用区的资源信息，包括可用区 ID。:::', examples=['cn-beijing-a'])],
                       region_id: Annotated[str, Field(description='地域 ID。:::tip您可以调用[DescribeRegions](https://www.volcengine.com/docs/6695/152921)接口查询 HBase 实例所有可用的地域资源信息，包括地域 ID。:::', examples=['cn-beijing'])],
                       master_spec: Annotated[str, Field(description='Master 节点的规格码。:::tip- 关于 Master 节点所支持的规格信息，请参见[实例规格](https://www.volcengine.com/docs/6695/111795)。- Master 节点数量为固定值，且不支持增减。:::', examples=['hbase.x1.medium'])],
                       rs_count: Annotated[int, Field(description='RegionServer 节点数量。- 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，取值范围为 2~100 之间的整数。- 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，取值范围为 4~100 之间的偶数整数，节点数量平均分配至主/备可用区。', examples=['4'])],
                       rs_spec: Annotated[str, Field(description='RegionServer 节点的规格码。:::tip关于 RegionServer 节点所支持的规格信息，请参见[实例规格](https://www.volcengine.com/docs/6695/111795)。:::', examples=['hbase.x1.large'])],
                       storage_capacity: Annotated[int, Field(description='存储空间大小，步长为 10GiB。- 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，取值范围为 100~20,000。- 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，取值范围为 200~20,000。:::tip多可用区采用主副本架构，实际可用容量为总容量的一半。:::', examples=['1000'])],
                       vpc_id: Annotated[str, Field(description='私有网络 ID。:::tip您可以调用[DescribeVpcs](https://www.volcengine.com/docs/6401/70495)接口查询可创建 HBase 实例的私有网络信息，包括私有网络 ID。:::', examples=['vpc-2d66uvmd9i8lc58ozz****'])],
                       subnet_id: Annotated[str, Field(description='子网 ID。子网必须属于所选的可用区。- 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，只需输入一个子网 ID。- 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，则需要输入两个不同的子网 ID。第一个为主可用区的子网 ID，第二个为备可用区的子网 ID，多个子网 ID 之间使用英文逗号（,）分隔。:::tip- 子网是私有网络内的 IP 地址块私有网络中的所有云资源都必须部署在子网内，子网为云资源分配私网 IP 地址，您可以调用[CreateSubnet](https://www.volcengine.com/docs/6401/70496)接口创建子网。- 您可以调用[DescribeSubnets](https://www.volcengine.com/docs/6401/70497)接口查询指定可用区内的所有子网列表信息，包括子网 ID。:::', examples=['subnet-2d6pl8bcpl2io58ozfd43'])],
                       charge_type: Annotated[str, Field(description='计费类型，取值：- `PostPaid`：按量计费（后付费）。- `PrePaid`：包年包月（预付费）。', examples=['PostPaid'])],
                       area: Optional[Annotated[str,Field(description='公共服务区或者售卖区。', examples=['PublicServiceArea or SalesArea'])]] = None,
                       auto_renew: Optional[Annotated[bool,Field(description='预付费场景下是否自动续费。取值：- `true`：自动续费。- `false`：不自动续费（默认）。:::tip仅当`ChargeType`为 PrePaid 时有效。:::', examples=['false'])]] = False,
                       cold_storage: Optional[Annotated[int,Field(description='设置容量型存储空间大小，取值范围：800GiB~1,000,000GiB，步长为 10GiB。', examples=['800'])]] = None,
                       deletion_protection: Optional[Annotated[str,Field(description='实例删除保护功能开关状态。取值范围：- `enabled`：已开启。- `disabled`：未开启（默认）。:::tip关于实例删除保护的更多信息，请参见[实例删除保护](https://www.volcengine.com/docs/6695/147035)。:::', examples=['enabled'])]] = 'disabled',
                       enable_auth: Optional[Annotated[bool,Field(description='是否开启登录认证。取值：- `true`：开启登录认证。实例创建成功后，您需要立即为实例创建数据库账号，详情请参见[CreateDBAccount](https://www.volcengine.com/docs/6695/1246239)。- `false`：不开启登录认证（默认）。:::tip- 仅当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，支持开启登录认证。- 开启登录认证后，仅对 Java 客户端生效，Thrift 连接依旧采用直连方式。:::', examples=['false'])]] = False,
                       enable_cloud_storage: Optional[Annotated[bool,Field(description='是否开通存储型容量，取值：- `true`：开通容量型存储。- `false`：不开通容量型存储（默认）。:::tip- 容量型存储的详细介绍，请参见[冷热分离介绍](https://www.volcengine.com/docs/6695/1181837)。- 仅当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，支持冷热分离功能。:::', examples=['true'])]] = False,
                       instance_name: Optional[Annotated[str,Field(description='实例名称。名称需同时满足如下要求：- 不能以数字、中划线（-）开头。- 只能包含中文、字母、数字、下划线（_）和中划线（-）。- 长度需要在 1~128 个字符内。:::tip若该参数留空，实例 ID 会默认作为实例名称。:::', examples=['test_api'])]] = None,
                       instance_type: Optional[Annotated[str,Field(description='实例类型。当前仅支持标准型，取值默认为`Standard`。', examples=['Standard'])]] = 'Standard',
                       multi_az: Optional[Annotated[bool,Field(description='实例的部署方式，取值：- `true`：多可用区部署。- `false`：单可用区部署（默认）。:::tip多可用区部署为邀测功能，如需使用，请[提交工单](https://console.volcengine.com/workorder/create/)联系技术支持申请。关于可用区部署方案的更多详情，请参见[多可用区同城容灾解决方案](https://www.volcengine.com/docs/6695/1337143)。:::', examples=['false'])]] = False,
                       project_name: Optional[Annotated[str,Field(description='选择实例所属的项目。若该参数留空，新建的实例默认加入`default`项目。', examples=['default'])]] = 'default',
                       purchase_months: Optional[Annotated[int,Field(description='购买时长，单位：月。取值范围：`1`，`2`，`3`，`4`，`5`，`6`，`7`，`8`，`9`，`12`，`24`，`36`。:::tip当`ChargeType`为`PrePaid`时，该参数必填。:::', examples=['1'])]] = None,
                       storage_type: Optional[Annotated[str,Field(description='实例的存储类型，取值：- `HdfsHdd`：HDD 文件存储（默认）。- `HdfsSsd`：SSD 文件存储。', examples=['HdfsHdd'])]] = 'HdfsHdd',
                       tags: Optional[Annotated[list[dict[str, Any]],Field(description='需要绑定的标签键和标签值数组对象。', examples=[''])]] = None) -> dict[str, Any]:
    """创建实例

    Args:
        engine_version (str): HBase 数据库引擎版本。当前仅支持 HBase 2.0 版本，取值为`HBase_2.0`。
            示例值：HBase_2.0
        zone_id (str): 可用区 ID。
            - 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，则只需输入一个可用区 ID。
            - 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，则需要输入两个不同的可用区 ID，第一个为主可用区 ID，第二个为备可用区 ID，多个可用区 ID 之间使用英文逗号（,）分隔。
            :::tip
            您可以调用[DescribeZones](https://www.volcengine.com/docs/6695/152922)接口查询 HBase 实例指定地域下所有可用区的资源信息，包括可用区 ID。
            :::
            示例值：cn-beijing-a
        region_id (str): 地域 ID。
            :::tip
            您可以调用[DescribeRegions](https://www.volcengine.com/docs/6695/152921)接口查询 HBase 实例所有可用的地域资源信息，包括地域 ID。
            :::
            示例值：cn-beijing
        master_spec (str): Master 节点的规格码。
            :::tip
            - 关于 Master 节点所支持的规格信息，请参见[实例规格](https://www.volcengine.com/docs/6695/111795)。
            - Master 节点数量为固定值，且不支持增减。
            :::
            示例值：hbase.x1.medium
        rs_count (int): RegionServer 节点数量。
            - 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，取值范围为 2~100 之间的整数。
            - 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，取值范围为 4~100 之间的偶数整数，节点数量平均分配至主/备可用区。
            示例值：4
        rs_spec (str): RegionServer 节点的规格码。
            :::tip
            关于 RegionServer 节点所支持的规格信息，请参见[实例规格](https://www.volcengine.com/docs/6695/111795)。
            :::
            示例值：hbase.x1.large
        storage_capacity (int): 存储空间大小，步长为 10GiB。
            - 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，取值范围为 100~20,000。
            - 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，取值范围为 200~20,000。
            :::tip
            多可用区采用主副本架构，实际可用容量为总容量的一半。
            :::
            示例值：1000
        vpc_id (str): 私有网络 ID。
            :::tip
            您可以调用[DescribeVpcs](https://www.volcengine.com/docs/6401/70495)接口查询可创建 HBase 实例的私有网络信息，包括私有网络 ID。
            :::
            示例值：vpc-2d66uvmd9i8lc58ozz****
        subnet_id (str): 子网 ID。子网必须属于所选的可用区。
            - 当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，只需输入一个子网 ID。
            - 当`MultiAZ`（部署方式）取值为`true`（多可用区部署）时，则需要输入两个不同的子网 ID。第一个为主可用区的子网 ID，第二个为备可用区的子网 ID，多个子网 ID 之间使用英文逗号（,）分隔。
            :::tip
            - 子网是私有网络内的 IP 地址块私有网络中的所有云资源都必须部署在子网内，子网为云资源分配私网 IP 地址，您可以调用[CreateSubnet](https://www.volcengine.com/docs/6401/70496)接口创建子网。
            - 您可以调用[DescribeSubnets](https://www.volcengine.com/docs/6401/70497)接口查询指定可用区内的所有子网列表信息，包括子网 ID。
            :::
            示例值：subnet-2d6pl8bcpl2io58ozfd43
        charge_type (str): 计费类型，取值：
            - `PostPaid`：按量计费（后付费）。
            - `PrePaid`：包年包月（预付费）。
            示例值：PostPaid
        area (str, optional): 公共服务区或者售卖区。
            示例值：PublicServiceArea or SalesArea
        auto_renew (bool, optional): 预付费场景下是否自动续费。取值：
            - `true`：自动续费。
            - `false`：不自动续费（默认）。
            :::tip
            仅当`ChargeType`为 PrePaid 时有效。
            :::
            示例值：false
        cold_storage (int, optional): 设置容量型存储空间大小，取值范围：800GiB~1,000,000GiB，步长为 10GiB。
            示例值：800
        deletion_protection (str, optional): 实例删除保护功能开关状态。取值范围：
            - `enabled`：已开启。
            - `disabled`：未开启（默认）。
            :::tip
            关于实例删除保护的更多信息，请参见[实例删除保护](https://www.volcengine.com/docs/6695/147035)。
            :::
            示例值：enabled
        enable_auth (bool, optional): 是否开启登录认证。取值：
            - `true`：开启登录认证。实例创建成功后，您需要立即为实例创建数据库账号，详情请参见[CreateDBAccount](https://www.volcengine.com/docs/6695/1246239)。
            - `false`：不开启登录认证（默认）。
            :::tip
            - 仅当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，支持开启登录认证。
            - 开启登录认证后，仅对 Java 客户端生效，Thrift 连接依旧采用直连方式。
            :::
            示例值：false
        enable_cloud_storage (bool, optional): 是否开通存储型容量，取值：
            - `true`：开通容量型存储。
            - `false`：不开通容量型存储（默认）。
            :::tip
            - 容量型存储的详细介绍，请参见[冷热分离介绍](https://www.volcengine.com/docs/6695/1181837)。
            - 仅当`MultiAZ`（部署方式）取值为`false`（单可用区部署）时，支持冷热分离功能。
            :::
            示例值：true
        instance_name (str, optional): 实例名称。名称需同时满足如下要求：
            - 不能以数字、中划线（-）开头。
            - 只能包含中文、字母、数字、下划线（_）和中划线（-）。
            - 长度需要在 1~128 个字符内。
            :::tip
            若该参数留空，实例 ID 会默认作为实例名称。
            :::
            示例值：test_api
        instance_type (str, optional): 实例类型。当前仅支持标准型，取值默认为`Standard`。
            示例值：Standard
        multi_az (bool, optional): 实例的部署方式，取值：
            - `true`：多可用区部署。
            - `false`：单可用区部署（默认）。
            :::tip
            多可用区部署为邀测功能，如需使用，请[提交工单](https://console.volcengine.com/workorder/create/)联系技术支持申请。关于可用区部署方案的更多详情，请参见[多可用区同城容灾解决方案](https://www.volcengine.com/docs/6695/1337143)。
            :::
            示例值：false
        project_name (str, optional): 选择实例所属的项目。若该参数留空，新建的实例默认加入`default`项目。
            示例值：default
        purchase_months (int, optional): 购买时长，单位：月。取值范围：`1`，`2`，`3`，`4`，`5`，`6`，`7`，`8`，`9`，`12`，`24`，`36`。
            :::tip
            当`ChargeType`为`PrePaid`时，该参数必填。
            :::
            示例值：1
        storage_type (str, optional): 实例的存储类型，取值：
            - `HdfsHdd`：HDD 文件存储（默认）。
            - `HdfsSsd`：SSD 文件存储。
            示例值：HdfsHdd
        tags (list[dict[str, Any]], optional): 需要绑定的标签键和标签值数组对象。

    Returns: 包含以下字段的字典
        instance_id (str, optional): 实例 ID。
            示例值：hb-cn01762cf4d6****
        order_no (str, optional): 订单 ID。
            示例值：Order730602621667020****
    """
    req = {
        "engine_version": engine_version,
        "zone_id": zone_id,
        "region_id": region_id,
        "master_spec": master_spec,
        "rs_count": rs_count,
        "rs_spec": rs_spec,
        "storage_capacity": storage_capacity,
        "vpc_id": vpc_id,
        "subnet_id": subnet_id,
        "charge_type": charge_type,
        "area": area,
        "auto_renew": auto_renew,
        "cold_storage": cold_storage,
        "deletion_protection": deletion_protection,
        "enable_auth": enable_auth,
        "enable_cloud_storage": enable_cloud_storage,
        "instance_name": instance_name,
        "instance_type": instance_type,
        "multi_az": multi_az,
        "project_name": project_name,
        "purchase_months": purchase_months,
        "storage_type": storage_type,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = hbase_resource_sdk.create_db_instance(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instance_detail",
    description="调用 DescribeDBInstanceDetail 接口查询指定实例的详细信息。"
)
def describe_db_instance_detail(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用[DescribeDBInstances](https://www.volcengine.com/docs/6695/152923)接口查询目标地域下所有 HBase 实例的基本信息，包括实例 ID。:::', examples=['hb-cn019f341d51****'])]) -> dict[str, Any]:
    """调用 DescribeDBInstanceDetail 接口查询指定实例的详细信息。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用[DescribeDBInstances](https://www.volcengine.com/docs/6695/152923)接口查询目标地域下所有 HBase 实例的基本信息，包括实例 ID。
            :::
            示例值：hb-cn019f341d51****

    Returns: 包含以下字段的字典
        auto_renew (bool, optional): 预付费场景下是否自动续费。取值：
            - `true`：自动续费。
            - `false`：不自动续费。
            示例值：false
        charge_status (str, optional): 计费状态。取值：
            - `Normal`：正常。
            - `Overdue`：欠费。
            - `Shutdown`：关停。
            示例值：Normal
        charge_type (str, optional): 计费类型，取值：
            - `PostPaid`：按量计费（后付费）。
            - `PrePaid`：包年包月（预付费）。
            示例值：PostPaid
        cold_storage (int, optional): 实例总容量型存储空间大小，单位 GiB。
            示例值：800
        create_time (str, optional): 实例创建时间（UTC 时间）。
            示例值：2022-11-07T07:17:55Z
        db_instance_endpoint (list[dict[str, Any]], optional): 连接地址信息列表。
            示例值：请参见返回示例。
        deletion_protection (str, optional): 实例删除保护功能开关状态。取值范围：
            - `enabled`：已开启。
            - `disabled`：未开启。
            :::tip
            关于实例删除保护的更多信息，请参见[实例删除保护](https://www.volcengine.com/docs/6695/147035)。
            :::
            示例值：enabled
        enable_auth (bool, optional): 是否开启登录认证。取值：
            - `true`：已开启登录认证。
            - `false`：未开启登录认证。
            示例值：false
        engine_version (str, optional): HBase 数据库版本。当前仅支持 HBase 2.0 版本。
            示例值：HBase_2.0
        expire_time (str, optional): 预付费场景下计费到期的时间，格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。
            示例值：2023-09-22T08:08:35Z
        instance_id (str, optional): 实例 ID。
            示例值：hb-cnglbbb73ea0****
        instance_name (str, optional): 实例名称。
            示例值：test_api
        instance_type (str, optional): 实例类型，当前仅支持 `Standard` 标准版。
            示例值：Standard
        master_count (int, optional): Master 节点个数。
            - 单可用区部署，默认包含 2 个 Master 节点。
            - 多可用区部署，默认包含 4 个 Master 节点，并平均分配至主/备可用区。
            示例值：2
        master_spec (str, optional): Master 节点的规格码。
            示例值：hbase.x1.medium
        minor_version (str, optional): 小版本号
        multi_az (bool, optional): 实例的部署方式，取值：
            - `true`：多可用区部署。
            - `false`：单可用区部署。
            示例值：false
        node_pool (str, optional): 实例所属的节点池
        primary_subnet_id (str, optional): 实时主可用区子网 ID。
            示例值：subnet-3jhhy08zsuakg3pncmfwx****
        primary_zone_id (str, optional): 实时主可用区 ID。
            示例值：cn-beijing-a
        private_dns_visibility (bool, optional): 私网DNS可见
        project_name (str, optional): 实例所属的项目名称。
            示例值：default
        region_id (str, optional): 实例所属的地域 ID。
            示例值：cn-beijing
        rs_count (int, optional): RegionServer 节点的数量。
            :::tip
            多可用区实例，节点数量平均配置至主/备可用区。
            :::
            示例值：2
        rs_spec (str, optional): RegionServer 节点的规格码。
            示例值：hbase.x1.large
        standby_subnet_id (str, optional): 实时备可用区子网 ID。
            示例值：subnet-2gd0b9x8hfeo050ztz08a****
        standby_used_storage (float, optional): 备实例已使用的存储容量，单位：GiB。
            示例值：0
        standby_zone_id (str, optional): 实时备可用区 ID。
            示例值：cn-beijing-b
        status (str, optional): 实例当前状态。关于实例状态的更多说明，请参见[实例状态说明](https://www.volcengine.com/docs/6695/131252)。
            示例值：Running
        storage_capacity (int, optional): 实例总存储容量，单位：GiB。
            :::tip
            实例为多可用区部署时，实际可用容量为总容量的一半。
            :::
            示例值：500
        storage_type (str, optional): 实例的存储类型，取值：
            - `HdfsHdd`：HDD 文件存储。
            - `HdfsSsd`：SSD 文件存储。
            示例值：HdfsHdd
        subnet_id (str, optional): 实例所属的子网 ID。
            - 单可用区实例，仅包含一个可用区的子网 ID。
            - 多可用区实例，包含主/备两个子网 ID。
            示例值：subnet-2d6pl8bcpl2io58ozfd43****
        tags (list[dict[str, Any]], optional): 实例绑定的标签键和标签值数组对象。
            示例值：请参见返回示例。
        used_cold_storage (int, optional): 实例已使用的容量型存储空间大小，单位 GiB。
            示例值：500
        used_storage (float, optional): 主实例已使用的存储容量，单位：GiB。
            示例值：0
        vpc_id (str, optional): 实例所属的私有网络 ID。
            示例值：vpc-rs5811nceqyov0x58x4****
        vpc_name (str, optional): 实例所属的私有网络名称。
            示例值：test_vpc
        zone_id (str, optional): 实例所属的可用区 ID。
            示例值：cn-beijing-a
        zone_name (str, optional): 实例所属的可用区名称。
            示例值：可用区A
    """
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = hbase_resource_sdk.describe_db_instance_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    name="describe_db_instances",
    description="调用 DescribeDBInstances 接口查询 HBase 实例列表信息。"
)
def describe_db_instances(region_id: Annotated[str, Field(description='地域 ID。:::tip您可以调用[DescribeRegions](https://www.volcengine.com/docs/6695/152921)接口查询 HBase 实例所有可用的地域资源信息，包括地域 ID。:::', examples=['cn-beijing'])],
                          page_number: Annotated[int, Field(description='实例信息列表的页码，取值为不超过 Integer 数据类型的最大值，起始值为1。', examples=['1'])],
                          page_size: Annotated[int, Field(description='每页记录数。取值为 1~100 间的整数。', examples=['10'])],
                          create_time_end: Optional[Annotated[str,Field(description='查询结束时间，系统会查询创建时间等于或早于查询结束时间的所有实例。格式为*yyyy-MM-dd*T*HH:mm*Z（UTC 时间）。:::tip若同时传入了查询开始时间（`CreateTimeStart`）和查询结束时间（`CreateTimeEnd`），查询开始时间需早于结束时间。:::', examples=['2022-11-08T12:26:30Z'])]] = None,
                          create_time_start: Optional[Annotated[str,Field(description='查询开始时间，系统会查询创建时间等于或晚于查询开始时间的所有实例。格式为*yyyy-MM-dd*T*HH:mm*Z（UTC 时间）。:::tip若同时传入了查询开始时间（`CreateTimeStart`）和查询结束时间（`CreateTimeEnd`），查询开始时间需早于结束时间。:::', examples=['2022-11-08T12:26:23Z'])]] = None,
                          instance_id: Optional[Annotated[str,Field(description='指定需要查询的实例 ID。支持模糊查询。', examples=['hb-cn019f341d51****'])]] = None,
                          instance_name: Optional[Annotated[str,Field(description='指定需要查询的实例名称。支持模糊查询。', examples=['hbase_test'])]] = None,
                          instance_status: Optional[Annotated[str,Field(description='指定需要查询的实例状态。', examples=['Running'])]] = None,
                          project_name: Optional[Annotated[str,Field(description='指定实例所属的项目名称，若该参数留空，则表示查询所有项目下符合筛选条件的实例。', examples=['default'])]] = None,
                          tag_filters: Optional[Annotated[list[dict[str, Any]],Field(description='基于标签对实例进行过滤。', examples=[''])]] = None,
                          tags: Optional[Annotated[list[dict[str, Any]],Field(description='用于查询筛选的标签键值对数组。:::tip单次最多支持同时传入 10 组标签键值对进行查询筛选。:::', examples=['请参见请求示例。'])]] = None) -> dict[str, Any]:
    """调用 DescribeDBInstances 接口查询 HBase 实例列表信息。

    Args:
        region_id (str): 地域 ID。
            :::tip
            您可以调用[DescribeRegions](https://www.volcengine.com/docs/6695/152921)接口查询 HBase 实例所有可用的地域资源信息，包括地域 ID。
            :::
            示例值：cn-beijing
        page_number (int): 实例信息列表的页码，取值为不超过 Integer 数据类型的最大值，起始值为1。
            示例值：1
        page_size (int): 每页记录数。取值为 1~100 间的整数。
            示例值：10
        create_time_end (str, optional): 查询结束时间，系统会查询创建时间等于或早于查询结束时间的所有实例。格式为*yyyy-MM-dd*T*HH:mm*Z（UTC 时间）。
            :::tip
            若同时传入了查询开始时间（`CreateTimeStart`）和查询结束时间（`CreateTimeEnd`），查询开始时间需早于结束时间。
            :::
            示例值：2022-11-08T12:26:30Z
        create_time_start (str, optional): 查询开始时间，系统会查询创建时间等于或晚于查询开始时间的所有实例。格式为*yyyy-MM-dd*T*HH:mm*Z（UTC 时间）。
            :::tip
            若同时传入了查询开始时间（`CreateTimeStart`）和查询结束时间（`CreateTimeEnd`），查询开始时间需早于结束时间。
            :::
            示例值：2022-11-08T12:26:23Z
        instance_id (str, optional): 指定需要查询的实例 ID。支持模糊查询。
            示例值：hb-cn019f341d51****
        instance_name (str, optional): 指定需要查询的实例名称。支持模糊查询。
            示例值：hbase_test
        instance_status (str, optional): 指定需要查询的实例状态。
            示例值：Running
        project_name (str, optional): 指定实例所属的项目名称，若该参数留空，则表示查询所有项目下符合筛选条件的实例。
            示例值：default
        tag_filters (list[dict[str, Any]], optional): 基于标签对实例进行过滤。
        tags (list[dict[str, Any]], optional): 用于查询筛选的标签键值对数组。
            :::tip
            单次最多支持同时传入 10 组标签键值对进行查询筛选。
            :::
            示例值：请参见请求示例。

    Returns: 包含以下字段的字典
        instances (list[dict[str, Any]], optional): 实例基本信息。
            示例值：请参见返回示例。
        total_count (int, optional): 实例数量。
            示例值：1
    """
    req = {
        "region_id": region_id,
        "page_number": page_number,
        "page_size": page_size,
        "create_time_end": create_time_end,
        "create_time_start": create_time_start,
        "instance_id": instance_id,
        "instance_name": instance_name,
        "instance_status": instance_status,
        "project_name": project_name,
        "tag_filters": tag_filters,
        "tags": tags,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = hbase_resource_sdk.describe_db_instances(req)
    return resp.to_dict()

@mcp_server.tool(
    name="modify_instance_deletion_protection_policy",
    description="调用 ModifyInstanceDeletionProtectionPolicy 接口开启或关闭实例删除保护功能。"
)
def modify_instance_deletion_protection_policy(instance_id: Annotated[str, Field(description='实例 ID。:::tip您可以调用[DescribeDBInstances](https://www.volcengine.com/docs/6695/152923)接口查询目标地域下所有 HBase 实例的基本信息，包括实例 ID。:::', examples=['hb-cngl56292097****'])],
                                               deletion_protection: Annotated[str, Field(description='开启或关闭实例删除保护功能。取值范围：- `enabled`：开启。- `disabled`：关闭。:::tip关于实例删除保护的更多信息，请参见[实例删除保护](https://www.volcengine.com/docs/6695/147035)。:::', examples=['enabled'])]) -> dict[str, Any]:
    """调用 ModifyInstanceDeletionProtectionPolicy 接口开启或关闭实例删除保护功能。

    Args:
        instance_id (str): 实例 ID。
            :::tip
            您可以调用[DescribeDBInstances](https://www.volcengine.com/docs/6695/152923)接口查询目标地域下所有 HBase 实例的基本信息，包括实例 ID。
            :::
            示例值：hb-cngl56292097****
        deletion_protection (str): 开启或关闭实例删除保护功能。取值范围：
            - `enabled`：开启。
            - `disabled`：关闭。
            :::tip
            关于实例删除保护的更多信息，请参见[实例删除保护](https://www.volcengine.com/docs/6695/147035)。
            :::
            示例值：enabled
    """
    req = {
        "instance_id": instance_id,
        "deletion_protection": deletion_protection,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = hbase_resource_sdk.modify_instance_deletion_protection_policy(req)
    return {
        "success": True,
        "message": f"实例 {instance_id} 删除保护策略已修改为 {deletion_protection}"
    }


"""Main entry point for the MCP server."""
def main():
    """Main entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="Run the Hbase MCP Server")
    parser.add_argument(
        "--transport",
        "-t",
        choices=["streamable-http", "stdio"],
        default="stdio",
        help="Transport protocol to use (streamable-http or stdio)",
    )

    args = parser.parse_args()
    try:
        logger.info(f"Starting Hbase MCP Server with {args.transport} transport")
        mcp_server.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Hbase MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()