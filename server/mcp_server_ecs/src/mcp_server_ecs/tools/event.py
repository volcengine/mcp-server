"""
System events related tool functions
"""

from typing import List

import volcenginesdkecs
from mcp import types
from pydantic import Field
from volcenginesdkecs.models import *

from mcp_server_ecs.common.client import get_volc_ecs_client
from mcp_server_ecs.common.errors import handle_error
from mcp_server_ecs.tools import mcp


@mcp.tool(
    name="describe_system_events",
    description="Query system events",
)
async def describe_system_events(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    createdAtStart: str = Field(
        default="",
        description="以CreatedAtStart为起点，筛选创建时间在其之后的事件。默认值为CreatedAtEnd前24小时（参考请求参数CreatedAtEnd），格式为RCF3339",
    ),
    createdAtEnd: str = Field(
        default="",
        description="以CreatedAtEnd为终点，筛选创建时间在其之前的事件。默认值为现在，格式为RCF3339",
    ),
    eventIds: List[str] = Field(
        default=[],
        description="事件ID，最多支持100个ID。您可以通过事件通知或调用本接口查询获取",
    ),
    resourceIds: List[str] = Field(
        default=[],
        description="资源ID，最多支持100个ID。您可以调用DescribeInstances接口，查询获取实例ID",
    ),
    status: List[str] = Field(
        default=[],
        description="""
                    系统事件的状态，最多支持10个。
                    UnknownStatus：未知状态
                    Executing：执行中
                    Succeeded：执行成功
                    Failed：执行失败
                    Inquiring：待响应
                    Scheduled：计划执行
                    Rejected：用户拒绝执行
                    Canceled：已取消
                    Pending：已暂停
                    Recovered：已恢复
                """,
    ),
    event_types: List[str] = Field(
        default=[],
        description="""
                    系统事件的类型，最多支持100个。
                    SystemFailure_Stop：因系统故障实例停止。
                    SystemFailure_Reboot：因系统故障实例重启。
                    DiskError_Redeploy：因硬盘异常实例重新部署。
                    GpuError_Redeploy：GPU异常，导致实例重新部署。
                    SystemMaintenance_Redeploy：因系统维护实例重新部署。
                    SystemMaintenance_StopAndRepair：实例停止，系统维修。
                    SystemFailure_Redeploy：因系统故障实例重新部署。
                    SystemFailure_Repair：系统故障，进行维修。
                    DiskErrorDetected：硬盘异常。
                    DiskError_ReplaceDisk：因硬盘异常更换硬盘。
                    InstanceOOM：实例内存OOM。
                    MemoryRiskDetected：内存运行存在风险。
                    InstanceFileSystemFailure_StopAndRepair：因文件系统异常实例停机修复。
                """,
    ),
    needNum: int = Field(
        default=20,
        description="事件较多时，可以通过该字段控制查询总数，需要根据用户的意图来设置",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_system_events(
                volcenginesdkecs.DescribeSystemEventsRequest(
                    created_at_start=createdAtStart,
                    created_at_end=createdAtEnd,
                    event_ids=eventIds,
                    resource_ids=resourceIds,
                    status=status,
                    types=event_types,
                    max_results=20,
                    next_token=next_token,
                )
            )

            if not response or not getattr(response, "system_events", None):
                return handle_error("describe_system_events")

            for event in response.system_events:
                filtered_event = {
                    "Id": event.id,
                    "ResourceId": event.resource_id,
                    "Category": event.category,
                    "ExtraInfo": event.extra_info,
                    "Status": event.status,
                    "Type": event.type,
                    "CreatedAt": event.created_at,
                    "UpdatedAt": event.updated_at,
                }
                total_results.append(filtered_event)

            if len(total_results) >= needNum or not response.next_token:
                total_results = total_results[:needNum]
                break

            next_token = response.next_token

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        return handle_error("describe_system_events", e)
