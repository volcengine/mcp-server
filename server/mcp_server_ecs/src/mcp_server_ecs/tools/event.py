"""
System events and subscriptions related tool functions
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
    description="查询系统事件 (Query system events)\n\n查询ECS实例的系统事件，包括计划运维事件和非预期运维事件。\n系统事件包括实例重启、重新部署、硬盘异常、GPU异常、内存OOM等。",
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

            if not response:
                handle_error("describe_system_events")

            system_events = getattr(response, "system_events", None) or []
            for event in system_events:
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
        handle_error("describe_system_events", e)


@mcp.tool(
    name="update_system_events",
    description="更新系统事件状态 (Update system events status)\n\n更新系统事件的状态，如确认执行、设置执行时间窗口等。\n用于响应需要用户确认的计划运维事件。",
)
async def update_system_events(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    eventIds: List[str] = Field(
        description="事件ID列表（必填），最多支持100个",
    ),
    status: str = Field(
        description="事件状态（必填）。取值：Executing (执行中)",
    ),
    operatedStartAt: str = Field(
        default="",
        description="用户期望的事件执行开始时间，格式为RFC3339",
    ),
    operatedEndAt: str = Field(
        default="",
        description="用户期望的事件执行结束时间，格式为RFC3339",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)

        response = volc_client.update_system_events(
            volcenginesdkecs.UpdateSystemEventsRequest(
                event_ids=eventIds,
                status=status,
                operated_start_at=operatedStartAt if operatedStartAt else None,
                operated_end_at=operatedEndAt if operatedEndAt else None,
            )
        )

        if not response:
            handle_error("update_system_events")

        operation_details = getattr(response, "operation_details", None) or []
        return [
            types.TextContent(type="text", text=f"Results: {operation_details}")
        ]

    except Exception as e:
        handle_error("update_system_events", e)


@mcp.tool(
    name="describe_event_types",
    description="查询事件类型列表 (Query event types)\n\n查询ECS支持的系统事件类型，包括非预期运维事件、计划运维事件、状态变化事件等。\n可查询哪些事件需要用户响应。",
)
async def describe_event_types(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    kind: str = Field(
        default="",
        description="事件种类。取值：UnexpectedOperations（非预期运维事件）、PlannedOperations（计划运维事件）、StateChange（状态变化事件）、BalanceWarning（费用预警事件）、TaskStatus（任务状态类事件）",
    ),
    responseRequired: bool = Field(
        default=False,
        description="是否需要用户响应。true：需要用户响应，false：不需要用户响应",
    ),
    eventTypes: List[str] = Field(
        default=[],
        description="事件类型列表，最多支持100个",
    ),
    needNum: int = Field(
        default=50,
        description="事件类型较多时，可以通过该字段控制查询总数",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_event_types(
                volcenginesdkecs.DescribeEventTypesRequest(
                    kind=kind if kind else None,
                    response_required=responseRequired,
                    types=eventTypes if eventTypes else None,
                    max_results=50,
                    next_token=next_token,
                )
            )

            if not response:
                handle_error("describe_event_types")

            event_types = getattr(response, "event_types", None) or []
            for event_type in event_types:
                filtered_event_type = {
                    "Type": event_type.type,
                    "Kind": event_type.kind,
                    "ResponseRequired": event_type.response_required,
                    "Description": getattr(event_type, "description", None),
                }
                total_results.append(filtered_event_type)

            if len(total_results) >= needNum or not response.next_token:
                total_results = total_results[:needNum]
                break

            next_token = response.next_token

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        handle_error("describe_event_types", e)


@mcp.tool(
    name="describe_subscriptions",
    description="查询事件订阅列表 (Query event subscriptions)\n\n查询已配置的系统事件订阅，包括订阅的事件类型和通知方式。\n支持短信、邮件、站内信、飞书等通知方式。",
)
async def describe_subscriptions(
    region: str = Field(
        default="cn-beijing",
        description="默认为cn-beijing. 可为：ap-southeast-1, cn-beijing2, cn-shanghai, cn-guangzhou 等",
    ),
    subscriptionIds: List[str] = Field(
        default=[],
        description="订阅ID列表，最多支持100个",
    ),
    type: str = Field(
        default="",
        description="订阅类型。取值：Notification（消息通知，包括短信/邮件/站内信/飞书）",
    ),
    needNum: int = Field(
        default=20,
        description="订阅较多时，可以通过该字段控制查询总数",
    ),
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    try:
        volc_client = get_volc_ecs_client(region)
        total_results = []
        next_token = None

        while True:
            response = volc_client.describe_subscriptions(
                volcenginesdkecs.DescribeSubscriptionsRequest(
                    subscription_ids=subscriptionIds if subscriptionIds else None,
                    type=type if type else None,
                    max_results=20,
                    next_token=next_token,
                )
            )

            if not response:
                handle_error("describe_subscriptions")

            subscriptions = getattr(response, "subscriptions", None) or []
            for subscription in subscriptions:
                filtered_subscription = {
                    "SubscriptionId": subscription.id,
                    "Type": subscription.type,
                    "EventTypes": subscription.event_types,
                    "CreatedAt": subscription.created_at,
                    "UpdatedAt": subscription.updated_at,
                }
                total_results.append(filtered_subscription)

            if len(total_results) >= needNum or not response.next_token:
                total_results = total_results[:needNum]
                break

            next_token = response.next_token

        return [types.TextContent(type="text", text=f"Results: {total_results}")]

    except Exception as e:
        handle_error("describe_subscriptions", e)
