import logging
from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk
import volcenginesdkvedbm

logger = logging.getLogger(__name__)


@mcp_server.tool(
    description="取消待执行的计划内事件"
)
def cancel_schedule_events(event_id: Annotated[list[str], Field(description='事件 ID(- 最多支持批量取消 100 个事件。- 仅支持取消事件类型为配置变更（ModifyDBInstanceSpec）或修改参数（ModifyClusterParams），事件状态为待执行（pending）的计划内事件。您可调用DescribeScheduleEvents接口，查询当前账号下待执行的计划内事件)', examples=['["uo7bx101rr291mgi"]'])],
                           instance_ids: Annotated[list[str], Field(description='需要取消的事件所属的实例 ID，多个实例 ID 间用英文逗号（,）分隔。', examples=['["vedbm-ca12cbqv****"]'])],
                           delete_record: Optional[Annotated[bool,Field(description='DeleteRecord', examples=[''])]] = None) -> dict[str, Any]:
    req = {
        "event_id": event_id,
        "instance_ids": instance_ids,
        "delete_record": delete_record,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.cancel_schedule_events(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查看当前账号下的计划内事件"
)
def describe_schedule_events(account_id: Optional[Annotated[int,Field(description='账号 ID。', examples=['12345'])]] = None,
                             begin_time: Optional[Annotated[str,Field(description='事件开始执行时间，格式：YYYY-MM-DDTHH:MM:SSZ（UTC 时间）。', examples=['2024-03-13T03:07:19Z'])]] = None,
                             end_time: Optional[Annotated[str,Field(description='事件执行结束时间，格式：YYYY-MM-DDTHH:MM:SSZ（UTC 时间）。', examples=['2024-03-13T03:07:19Z'])]] = None,
                             event_id: Optional[Annotated[str,Field(description='事件 ID。', examples=['4nbx88ea9dxa****'])]] = None,
                             event_kind: Optional[Annotated[str,Field(description='事件类型。取值：- `ModifyClusterParams`：修改参数。- `ModifyDBInstanceSpec`：配置变更。- `UpgradeInstance`：版本升级。- `RestartDBInstance`：重启实例。', examples=['ModifyClusterParams枚举值：ModifyDBInstanceParameters,ModifyDBInstanceSpec,RestartDBInstance,UpgradeInstance'])]] = None,
                             instance_id: Optional[Annotated[str,Field(description='实例 ID。', examples=['vedbm-r3xq0zdl****'])]] = None,
                             limit: Optional[Annotated[int,Field(description='每页记录数。最小值为 1，最大值不超过 500。默认值为 10。', examples=['10'])]] = '100',
                             offset: Optional[Annotated[int,Field(description='当前页查询偏移量，取值最小为 0。默认值为 0。', examples=['1'])]] = '0',
                             project_name: Optional[Annotated[str,Field(description='事件对应实例所属的项目名称。', examples=['default'])]] = None,
                             status: Optional[Annotated[str,Field(description='事件状态。取值：- `pending`：待执行。- `executing`：执行中。- `failure`：执行失败。- `finish`：已完成。- `cancel`：已取消。', examples=['pending枚举值：cancel,executing,failure,finish,pending'])]] = None) -> dict[str, Any]:
    req = {
        "account_id": account_id,
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
    description="修改待执行事件的执行时间"
)
def modify_schedule_events(event_id: Annotated[list[str], Field(description='事件 ID(- 最多支持选择 100 个事件批量修改执行时间。- 仅支持修改事件类型为配置变更（ModifyDBInstanceSpec）或修改参数（ModifyClusterParams），事件状态为待执行（pending）的计划内事件。您可调用DescribeScheduleEvents接口，查询当前账号下待执行的计划内事件。)', examples=['["uo7bx101rr291mgi"]'])],
                           instance_ids: Annotated[list[str], Field(description='需要修改的事件所属的实例 ID，多个实例 ID 间用英文逗号（,）分隔。', examples=['["vedbm-ca12cbqv****"]'])],
                           planned_start_time: Optional[Annotated[str,Field(description='PlannedStartTime', examples=[''])]] = None,
                           schedule_type: Optional[Annotated[str,Field(description='执行方式，取值：- `Immediate`：立即执行（默认）。- `MaintainTime`：可维护时间段执行。', examples=['Immediate枚举值：Immediate,MaintainTime,SpecifiedTime'])]] = None) -> dict[str, Any]:
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
    description="修改实例的可维护时间段"
)
def modify_db_instance_maintenance_window(instance_id: str,
                                          maintenance_time: Annotated[str, Field(description='实例的可维护时间段。格式：HH:mmZ-HH:mmZ（UTC 时间）。(可维护时间段最小时间间隔 2 小时，最大时间间隔 24 小时，不允许跨天选择时间段。)', examples=['19:00Z-20:59Z'])],
                                          day_kind: Optional[Annotated[str,Field(description='可维护周期粒度，默认取值为：`Week`（周）。', examples=['Week枚举值：Month,Week'])]] = None,
                                          day_of_month: Optional[Annotated[list[int],Field(description='指定每月哪一天为可维护时间段，默认为空，表示每天都指定。', examples=['[]'])]] = None,
                                          day_of_week: Optional[Annotated[str,Field(description='每周的哪一天为可维护时间段，默认取值为每一天：`Monday`，`Tuesday`，`Wednesday`，`Thursday`，`Friday`，`Saturday`，`Sunday`')]] = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "maintenance_time": maintenance_time,
        "day_kind": day_kind,
        "day_of_month": day_of_month,
        "day_of_week": day_of_week,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_instance_maintenance_window(req)
    return resp.to_dict()
