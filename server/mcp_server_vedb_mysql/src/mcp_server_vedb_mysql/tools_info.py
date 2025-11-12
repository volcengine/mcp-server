import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)


@mcp_server.tool(
    description="查询存储价格"
)
def describe_storage_payable_price(storage_types: Annotated[str, Field(description='存储类型，取值：`Clusterpool`：存储空间；`ColdDataArchive`：冷数据存储空间')]) -> dict[str, Any]:
    req = {
        "storage_types": storage_types,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_storage_payable_price(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询当前地域下实例支持的可用区资源"
)
def describe_availability_zones(region_id: Optional[Annotated[str,Field(description='地域 ID。(您可以调用DescribeRegions接口查询可创建实例的地域信息，包括地域 ID。)', examples=['cn-beijing'])]] = None) -> dict[str, Any]:
    """调用 DescribeAvailabilityZones 接口查询当前地域下实例支持的可用区资源。

    Args:
        region_id (str, optional): 地域 ID。
            (
            您可以调用DescribeRegions接口查询可创建实例的地域信息，包括地域 ID。
            )
            示例值：cn-beijing

    Returns: 包含以下字段的字典
        region_id (str, optional): 地域 ID。
            示例值：cn-beijing
        zones (list[dict[str, Any]], optional): 可用区列表。
    """
    req = {
        "region_id": region_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_availability_zones(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定可用区支持的节点规格信息"
)
def describe_db_instance_specs(zone_ids: Optional[Annotated[str,Field(description='可用区 ID。(可调用DescribeAvailabilityZones接口查询实例支持的可用区资源。)', examples=['cn-beijing-b'])]] = None) -> dict[str, Any]:
    """用 DescribeDBInstanceSpecs 接口查询指定可用区支持的节点规格信息。

    Args:
        zone_ids (str, optional): 可用区 ID。
            (
            可调用DescribeAvailabilityZones接口查询实例支持的可用区资源。
            )
            示例值：cn-beijing-b

    Returns: 包含以下字段的字典
        node_specs (list[dict[str, Any]], optional): 节点规格配置列表。
        total (int, optional): 符合查询条件的数量。
            示例值：2
    """
    req = {
        "zone_ids": zone_ids,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_specs(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询指定配置实例的价格详情"
)
def describe_db_instance_price_detail(node_spec: Annotated[str, Field(description='实例的节点规格代码。(关于实例节点规格的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。)', examples=['vedb.mysql.x4.xlarge'])],
                                      node_number: Annotated[int, Field(description='实例节点数量。取值范围为 2~16 个。', examples=['2'])],
                                      charge_type: Optional[Annotated[str,Field(description='计算计费类型。取值：- `PostPaid`：按量计费（后付费）。<ve>- `PrePaid`：包年包月（预付费）。</ve>', examples=['PostPaid枚举值：PostPaid,PrePaid'])]] = None,
                                      number: Optional[Annotated[int,Field(description='实例数量，取值范围 1~50，默认值为 `1`。', examples=['1'])]] = '1',
                                      period: Optional[Annotated[int,Field(description='预付费场景下的购买时长。(当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。)', examples=['1'])]] = '1',
                                      period_unit: Optional[Annotated[str,Field(description='预付费场景下的购买周期。- `Month`：包月。- `Year`：包年。(当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。)', examples=['Month枚举值：month,year'])]] = None,
                                      pre_paid_storage_in_gb: Optional[Annotated[int,Field(description='预付费场景下的存储空间大小。(当 `StorageChargeType`（存储计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。)', examples=['50'])]] = None,
                                      storage_charge_type: Optional[Annotated[str,Field(description='存储计费类型。不传入该参数时，存储计费类型默认与计算计费类型取值一致，取值如下：- `PostPaid`：按量计费（后付费）。<ve>- `PrePaid`：包年包月（预付费）。)warning- 当计算计费类型取值为 `PostPaid` 时，存储计费类型也只能取值为 `PostPaid`。- 当计算计费类型取值为 `PrePaid` 时，存储计费类型可取值为 `PrePaid` 或 `PostPaid`。)</ve>', examples=['PostPaid枚举值：PostPaid,PrePaid'])]] = None) -> dict[str, Any]:
    """调用 DescribeDBInstancePriceDetail 接口查询指定配置实例的价格详情。

    Args:
        node_spec (str): 实例的节点规格代码。
            (
            关于实例节点规格的详细信息，请参见[产品规格](https://www.volcengine.com/docs/6357/73614)。
            )
            示例值：vedb.mysql.x4.xlarge
        node_number (int): 实例节点数量。取值范围为 2~16 个。
            示例值：2
        charge_type (str, optional): 计算计费类型。取值：
            - `PostPaid`：按量计费（后付费）。
            <ve>- `PrePaid`：包年包月（预付费）。</ve>
            示例值：PostPaid
            枚举值：PostPaid,PrePaid
        number (int, optional): 实例数量，取值范围 1~50，默认值为 `1`。
            示例值：1
        period (int, optional): 预付费场景下的购买时长。
            (
            当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。
            )
            示例值：1
        period_unit (str, optional): 预付费场景下的购买周期。
            - `Month`：包月。
            - `Year`：包年。
            (
            当 `ChargeType`（计算计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。
            )
            示例值：Month
            枚举值：month,year
        pre_paid_storage_in_gb (int, optional): 预付费场景下的存储空间大小。
            (
            当 `StorageChargeType`（存储计费类型） 取值为 `PrePaid`（包年包月） 时，该参数必填。
            )
            示例值：50
        storage_charge_type (str, optional): 存储计费类型。不传入该参数时，存储计费类型默认与计算计费类型取值一致，取值如下：
            - `PostPaid`：按量计费（后付费）。
            <ve>
            - `PrePaid`：包年包月（预付费）。
            )warning
            - 当计算计费类型取值为 `PostPaid` 时，存储计费类型也只能取值为 `PostPaid`。
            - 当计算计费类型取值为 `PrePaid` 时，存储计费类型可取值为 `PrePaid` 或 `PostPaid`。
            )
            </ve>
            示例值：PostPaid
            枚举值：PostPaid,PrePaid

    Returns: 包含以下字段的字典
        charge_item_prices (list[dict[str, Any]], optional): 指定配置下的各项费用明细。
        charge_type (str, optional): 计算计费类型，取值：
            - `PostPaid`：按量计费（后付费）。
            <ve>- `PrePaid`：包年包月（预付费）。</ve>
            示例值：PostPaid
        config_item_prices (list[dict[str, Any]], optional): 指定配置的详细计费信息。
        currency (str, optional): 货币单位。<ve>默认值为 `人民币`</ve>。
            示例值：<ve>人民币</ve><bp>USD</bp>
        discount_price (float, optional): 指定配置下的折扣总价。
            示例值：0.2478
        original_price (float, optional): 指定配置下的原始总价。
            示例值：1.18
        payable_price (float, optional): 指定配置下的应付总价。
            示例值：0.2478
    """
    req = {
        "node_spec": node_spec,
        "node_number": node_number,
        "charge_type": charge_type,
        "number": number,
        "period": period,
        "period_unit": period_unit,
        "pre_paid_storage_in_gb": pre_paid_storage_in_gb,
        "storage_charge_type": storage_charge_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_price_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询实例可用的地域资源"
)
def describe_regions() -> dict[str, Any]:
    """调用 DescribeRegions 接口查询实例可用的地域资源。

    Returns: 包含以下字段的字典
        regions (list[dict[str, Any]], optional): 地域列表。
    """
    req = {
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_regions(req)
    return resp.to_dict()
