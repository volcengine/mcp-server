import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk

logger = logging.getLogger(__name__)


@mcp_server.tool(
    description="取消待执行的计划内事件。触发示例：取消实例vedbm-****下ID为xxx的待执行事件"
)
def cancel_schedule_events(event_id: list[str],
                           instance_ids: list[str]) -> dict[str, Any]:
    req = {
        "event_id": event_id,
        "instance_ids": instance_ids,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.cancel_schedule_events(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查看当前账号下的计划内事件。触发示例：查看实例vedbm-****的所有待执行事件"
)
def describe_schedule_events(begin_time: Optional[Annotated[str,Field(description='UTC时间', examples=['2024-03-13T03:07:19Z'])]] = None,
                             end_time: str = None,
                             event_id: str = None,
                             event_kind: Optional[Annotated[str,Field(examples=['ModifyDBInstanceParameters','ModifyDBInstanceSpec','RestartDBInstance','UpgradeInstance'])]] = None,
                             instance_id: str = None,
                             limit: int = 500,
                             offset: int = 0,
                             project_name: Optional[Annotated[str,Field(description='事件对应实例所属的项目名称', examples=['default'])]] = None,
                             status: Optional[Annotated[str,Field(examples=['cancel','executing','failure','finish','pending'])]] = None) -> dict[str, Any]:
    req = {
        # "account_id": account_id,
        "begin_time": begin_time,
        "end_time": end_time,
        "event_id": event_id,
        "event_kind": event_kind,
        "instance_id": instance_id,
        "limit": limit,
        "offset": offset,
        "project_name": project_name,
        "status": status,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_schedule_events(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改待执行事件的执行时间。触发示例：将实例vedbm-****中ID为xxx的事件修改为在可维护时间段执行"
)
def modify_schedule_events(event_id: list[str],
                           instance_ids: list[str],
                           planned_start_time: Optional[Annotated[str,Field(description='UTC时间', examples=['2024-03-13T03:07:19Z'])]] = None,
                           schedule_type: Optional[Annotated[str,Field(examples=['Immediate','MaintainTime','SpecifiedTime'])]] = None) -> dict[str, Any]:
    req = {
        "event_id": event_id,
        "instance_ids": instance_ids,
        "planned_start_time": planned_start_time,
        "schedule_type": schedule_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_schedule_events(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改实例的可维护时间段。触发示例：将实例vedbm-****的可维护时间段修改为每周日的19:00Z-20:59Z"
)
def modify_db_instance_maintenance_window(instance_id: str,
                                          maintenance_time: Annotated[str, Field(description='UTC时间', examples=['19:00Z-20:59Z'])],
                                          day_of_week: Optional[Annotated[list[str],Field(examples=['["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]'])]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "maintenance_time": maintenance_time,
        "day_kind": "Week",
        "day_of_month": [],
        "day_of_week": day_of_week,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_instance_maintenance_window(req)
    return resp.to_dict()
