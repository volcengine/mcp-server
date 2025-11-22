import logging
from typing import Optional, Dict, Any, List

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.alarm import (
    create_alarm_notify_group_resource,
    delete_alarm_notify_group_resource,
    describe_alarm_notify_groups_resource,
    create_alarm_resource,
    delete_alarm_resource,
    describe_alarms_resource
)
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)


async def create_alarm_notify_group_tool(
    alarm_notify_group_name: str,
    notify_type: List[str],
    receivers: List[Dict],
    iam_project_name: Optional[str] = None,
) -> dict:
    """Create an alarm notification group.

    This tool creates a notification group for alarm alerts.

    Args:
        alarm_notify_group_name: Name of the alarm notification group (required)
        notify_type: Notification types, supports 'Trigger' and 'Recovery' (required)
        receivers: List of receiver information, each containing receiver configuration (required)
            receiver_type: Type of receiver, e.g., 'User' (required)
            receiver_names: List of receiver names (required)
            receiver_channels: List of notification channels, e.g., ['Email', 'Sms', 'Phone'] (required)
            start_time: Start time for notifications (optional)
            end_time: End time for notifications (optional)
            webhook: Webhook URL for notifications (optional)
        iam_project_name: IAM project name (optional)

    Returns:
        Dictionary containing alarm_notify_group_id and other information

    Examples:
        # Create notification group with email receivers
        create_alarm_notify_group_tool(
            alarm_notify_group_name="ops-team",
            notify_type=["Trigger", "Recovery"],
            receivers=[{
                "receiver_type": "User",
                "receiver_names": ["user1", "user2"],
                "receiver_channels": ["Email"],
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "webhook": "https://webhook.example.com/notify"
            }],
            iam_project_name="default"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())


        return await create_alarm_notify_group_resource(
            auth_info=auth_info,
            alarm_notify_group_name=alarm_notify_group_name,
            notify_type=notify_type,
            receivers=receivers,
            iam_project_name=iam_project_name,
        )

    except Exception as e:
        logger.error("call tool error: create_alarm_notify_group_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def delete_alarm_notify_group_tool(
    alarm_notify_group_id: str,
) -> dict:
    """Delete an alarm notification group.

    This tool deletes an alarm notification group by its ID.

    Args:
        alarm_notify_group_id: Alarm notification group ID (required)

    Returns:
        Dictionary containing operation result

    Examples:
        # Delete notification group
        delete_alarm_notify_group_tool("notify-group-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not alarm_notify_group_id or not alarm_notify_group_id.strip():
            raise ValueError("alarm_notify_group_id is required")

        return await delete_alarm_notify_group_resource(
            auth_info=auth_info,
            alarm_notify_group_id=alarm_notify_group_id,
        )

    except Exception as e:
        logger.error("call tool error: delete_alarm_notify_group_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_alarm_notify_groups_tool(
    alarm_notify_group_name: Optional[str] = None,
    alarm_notify_group_id: Optional[str] = None,
    receiver_name: Optional[str] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
    iam_project_name: Optional[str] = None,
) -> dict:
    """Describe alarm notification groups.

    This tool queries alarm notification groups with various filtering options.

    Args:
        alarm_notify_group_name: Alarm notification group name for filtering (optional)
        alarm_notify_group_id: Alarm notification group ID for filtering (optional)
        receiver_name: Receiver name for filtering (optional)
        page_number: Page number for pagination (optional, defaults to 1)
        page_size: Page size for pagination (optional, defaults to 20, max 100)
        iam_project_name: IAM project name for filtering (optional)

    Returns:
        Dictionary containing total count and notification groups list

    Examples:
        # Query all notification groups
        describe_alarm_notify_groups_tool()

        # Query by name filter
        describe_alarm_notify_groups_tool(
            alarm_notify_group_name="ops-team"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        return await describe_alarm_notify_groups_resource(
            auth_info=auth_info,
            alarm_notify_group_name=alarm_notify_group_name,
            alarm_notify_group_id=alarm_notify_group_id,
            receiver_name=receiver_name,
            page_number=page_number,
            page_size=page_size,
            iam_project_name=iam_project_name,
        )

    except Exception as e:
        logger.error("call tool error: describe_alarm_notify_groups_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def create_alarm_tool(
    project_id: str,
    alarm_name: str,
    query_request: List[Dict],
    request_cycle: Dict,
    condition: str,
    alarm_period: int,
    alarm_notify_group: List[str],
    status: Optional[bool] = True,
    trigger_period: Optional[int] = 1,
    user_define_msg: Optional[str] = None,
    severity: Optional[str] = "notice",
    alarm_period_detail: Optional[Dict] = None,
    join_configurations: Optional[List[Dict]] = None,
    trigger_conditions: Optional[List[Dict]] = None,
) -> dict:
    """Create an alarm.

    This tool creates an alarm policy for log monitoring.

    Args:
        project_id: Log project ID (required)
        alarm_name: Alarm policy name (required)
        query_request: List of query requests, each containing query conditions (required)
            topic_id: Log Topic ID
            query: Query statement, with a maximum supported length of 1024
            number: Alert Object Sequence Number (starting from 1 and incrementing sequentially)
            start_time_offset: Start time of the query range (historical time relative to the current time). Unit: minutes. Value range: non-positive. Maximum value: 0, minimum value: -1440
            end_time_offset: End time of the query range (historical time relative to the current time). Unit: minutes. Value range: non-positive; must be greater than StartTimeOffset. Maximum value: 0, minimum value: -1440
            topic_name: Log Topic Name for the execution of the alert policy
            time_span_type: Indicates whether the query uses whole-hour time (newly added whole-hour time option). Non-mandatory; defaults to "Relative" if left blank
            truncated_time: Time Truncation (truncating time to the nearest minute or hour)
        request_cycle: Request cycle configuration (required)
            cycle_type: Execution Cycle Type. Options: Period (Periodic Execution), Fixed (Fixed-time Execution)
            time: Cycle for alert task execution or the fixed time point for fixed-time execution. Unit: minutes. Value range: 1–1440
            cron_tab: Cron Expression. Log Service specifies the scheduled execution of alert tasks via Cron Expression. The minimum granularity of the Cron Expression is minute, following the 24-hour format
        condition: Alarm trigger condition, supports comparison operators (required)
        alarm_period: Alarm period in minutes (required)
        alarm_notify_group: List of alarm notification group IDs (required)
        status: Whether the alarm is enabled (optional, defaults to True)
        trigger_period: Trigger period, number of consecutive periods to trigger (optional, defaults to 1)
        user_define_msg: Custom message content (optional)
        severity: Alarm severity level (optional, defaults to "notice")
        alarm_period_detail: Detailed alarm period configuration (optional)
            sms: SMS Alert Cycle. Unit: minutes. Value range: 10–1440
            phone: Phone Alert Cycle. Unit: minutes. Value range: 10–1440
            email: Email Alert Cycle. Unit: minutes. Value range: 1–1440
            general_webhook: General Webhook Alert Cycle. Unit: minutes. Value range: 1–1440
        join_configurations: Join configuration for multiple query results (optional)
            condition: Join condition, e.g., "$1.uid==$2.uid"
            set_operation_type: Operation type, e.g., "CrossJoin","LeftJoin","RightJoin","InnerJoin","FullJoin"
        trigger_conditions: List of trigger conditions (optional)
            severity: Alarm severity level, e.g., "notice", "warning", "critical" (optional)
            condition: Trigger condition, e.g., "$1.cnt == 5"
            count_condition: Count condition, e.g., "__count__ == 10"

    Returns:
        Dictionary containing alarm_id and other information

    Examples:
        # Create error rate alarm
        create_alarm_tool(
            project_id="project-123",
            alarm_name="error-rate-alert",
            query_request=[{
                "topic_id": "topic-123",
                "query": "Failed | select count(*) as errNum",
                "number": 1,
                "start_time_offset": -15,
                "end_time_offset": 0,
                "time_span_type": "Relative",
                "truncated_time": "Minute"
            },{
                "topic_id": "topic-123",
                "query": "Failed | select count(*) as errNum",
                "number": 2,
                "start_time_offset": -15,
                "end_time_offset": 0,
                "time_span_type": "Relative",
                "truncated_time": "Minute"
            }],
            request_cycle={
                "cycle_type": "Period",
                "time": 5
            },
            condition="count > 100",
            alarm_period=5,
            alarm_notify_group=["notify-group-123"],
            severity="critical",
            alarm_period_detail={
                "sms": 10,
                "phone": 10,
                "email": 1,
                "general_webhook": 1
            },
            join_configurations=[{
                "condition": "$1.uid==$2.uid",
                "set_operation_type": "InnerJoin"
            }],
            trigger_conditions=[{
                "severity": "critical",
                "condition": "$1.cnt == 5",
                "count_condition": "__count__ == 10"
            }]
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        # Use configured project_id if not provided
        project_id = project_id or TLS_CONFIG.project_id
        if not project_id or not project_id.strip():
            raise ValueError("project_id is required")


        return await create_alarm_resource(
            auth_info=auth_info,
            project_id=project_id,
            alarm_name=alarm_name,
            query_request=query_request,
            request_cycle=request_cycle,
            condition=condition,
            alarm_period=alarm_period,
            alarm_notify_group=alarm_notify_group,
            status=status,
            trigger_period=trigger_period,
            user_define_msg=user_define_msg,
            severity=severity,
            alarm_period_detail=alarm_period_detail,
            join_configurations=join_configurations,
            trigger_conditions=trigger_conditions,
        )

    except Exception as e:
        logger.error("call tool error: create_alarm_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def delete_alarm_tool(
    alarm_id: str,
) -> dict:
    """Delete an alarm.

    This tool deletes an alarm policy by its ID.

    Args:
        alarm_id: Alarm policy ID (required)

    Returns:
        Dictionary containing operation result

    Examples:
        # Delete alarm
        delete_alarm_tool("alarm-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not alarm_id or not alarm_id.strip():
            raise ValueError("alarm_id is required")

        return await delete_alarm_resource(
            auth_info=auth_info,
            alarm_id=alarm_id,
        )

    except Exception as e:
        logger.error("call tool error: delete_alarm_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_alarms_tool(
    project_id: Optional[str] = None,
    alarm_name: Optional[str] = None,
    alarm_id: Optional[str] = None,
    topic_name: Optional[str] = None,
    topic_id: Optional[str] = None,
    status: Optional[bool] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
) -> dict:
    """Describe alarms.

    This tool queries alarm policies with various filtering options.

    Args:
        project_id: Log project ID (optional, defaults to configured project_id)
        alarm_name: Alarm policy name for filtering (optional)
        alarm_id: Alarm policy ID for filtering (optional)
        topic_name: Topic name for filtering (optional)
        topic_id: Topic ID for filtering (optional)
        status: Alarm status for filtering (optional)
        page_number: Page number for pagination (optional, defaults to 1)
        page_size: Page size for pagination (optional, defaults to 20, max 100)

    Returns:
        Dictionary containing total count and alarms list

    Examples:
        # Query all alarms for default project
        describe_alarms_tool()

        # Query alarms by name filter
        describe_alarms_tool(
            alarm_name="error-rate-alert"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        project_id = project_id or TLS_CONFIG.project_id

        return await describe_alarms_resource(
            auth_info=auth_info,
            project_id=project_id,
            alarm_name=alarm_name,
            alarm_id=alarm_id,
            topic_name=topic_name,
            topic_id=topic_id,
            status=status,
            page_number=page_number,
            page_size=page_size,
        )

    except Exception as e:
        logger.error("call tool error: describe_alarms_tool, err is {}".format(str(e)))
        return {"error": str(e)}