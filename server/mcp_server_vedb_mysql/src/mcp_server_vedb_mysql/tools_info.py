import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)


@mcp_server.tool(
    description="查询存储单价。触发示例：查询北京地域下存储容量为100GB的存储费用价格"
)
def describe_storage_payable_price(storage_types: Annotated[str, Field(examples=['Clusterpool'])]) -> dict[str, Any]:
    req = {
        "storage_types": storage_types,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_storage_payable_price(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询当前地域下实例支持的可用区资源。触发示例：查询北京地域下支持的所有可用区信息"
)
def describe_availability_zones(region_id: Optional[Annotated[str,Field(examples=['cn-beijing'])]] = None) -> dict[str, Any]:
    req = {
        "region_id": region_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_availability_zones(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定可用区支持的节点规格信息。触发示例：查询北京地域下可用的所有veDB MySQL实例规格"
)
def describe_db_instance_specs(zone_ids: Optional[Annotated[str,Field(examples=['cn-beijing-b'])]] = None) -> dict[str, Any]:
    req = {
        "zone_ids": zone_ids,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_specs(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询指定配置实例的价格详情。触发示例：查询北京地域下规格为vedb.mysql.x4.large、节点数为2的按量付费实例价格"
)
def describe_db_instance_price_detail(node_spec: Annotated[str, Field(examples=['vedb.mysql.x4.xlarge'])],
                                      node_number: int,
                                      charge_type: Optional[Annotated[str,Field(examples=['PostPaid','PrePaid'])]] = None,
                                      number: Optional[Annotated[int,Field(examples=[1])]] = 1,
                                      period: Optional[Annotated[int,Field(examples=[1])]] = 1,
                                      period_unit: Optional[Annotated[str,Field(examples=['month','year'])]] = None,
                                      pre_paid_storage_in_gb: Optional[Annotated[int,Field(description='预付费场景下的存储空间大小')]] = None,
                                      storage_charge_type: Optional[Annotated[str,Field(examples=['PostPaid','PrePaid'])]] = None) -> dict[str, Any]:
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
    description="查询实例可用的地域资源。触发示例：查询veDB MySQL支持的所有地域列表"
)
def describe_regions() -> dict[str, Any]:
    req = {
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_regions(req)
    return resp.to_dict()
