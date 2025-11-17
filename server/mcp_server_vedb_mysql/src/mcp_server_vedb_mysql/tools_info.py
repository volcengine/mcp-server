import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)


@mcp_server.tool(
    description="查询当前地域下实例支持的可用区。触发示例：查询北京地域下支持的所有可用区信息"
)
def list_availability_zones(region_id: str = 'cn-beijing') -> dict[str, Any]:
    req = {
        "region_id": region_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_availability_zones(req)
    return resp.to_dict()


@mcp_server.tool(
    description="查询指定可用区支持的节点规格信息。触发示例：查询北京地域下可用的所有veDB MySQL实例规格"
)
def list_available_db_specs() -> dict[str, Any]:
    req = {
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_specs(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询实例可用的地域。触发示例：查询veDB MySQL支持的所有地域列表"
)
def list_region_names() -> dict[str, Any]:
    req = {
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_regions(req)
    return resp.to_dict()
