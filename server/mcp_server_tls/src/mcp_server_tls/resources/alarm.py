import logging
from typing import Optional, Dict, Any, List

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import (
    CreateAlarmNotifyGroupRequest,
    DeleteAlarmNotifyGroupRequest,
    DescribeAlarmNotifyGroupsRequest,
    CreateAlarmRequest,
    DeleteAlarmRequest,
    DescribeAlarmsRequest
)
from volcengine.tls.tls_responses import (
    CreateAlarmNotifyGroupResponse,
    DeleteAlarmNotifyGroupResponse,
    DescribeAlarmNotifyGroupsResponse,
    CreateAlarmResponse,
    DeleteAlarmResponse,
    DescribeAlarmsResponse
)

from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)


async def create_alarm_notify_group_resource(
    auth_info: Dict,
    alarm_notify_group_name: str,
    notify_type: List[str],
    receivers: List[Dict],
    iam_project_name: Optional[str] = None,
) -> Dict:
    """
    Create an alarm notification group
    """
    try:
        # Convert receivers dict to SDK Receiver objects if needed
        from volcengine.tls.tls_requests import Receiver
        receiver_objects = []
        for receiver in receivers:
            if isinstance(receiver, dict):
                receiver_objects.append(Receiver(** receiver))
        
        # Create request object using SDK's CreateAlarmNotifyGroupRequest
        request = CreateAlarmNotifyGroupRequest(
            alarm_notify_group_name=alarm_notify_group_name,
            notify_type=notify_type,
            receivers=receiver_objects,
            iam_project_name=iam_project_name
        )
            
        # Call SDK method
        response: CreateAlarmNotifyGroupResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_alarm_notify_group",
            create_alarm_notify_group_request=request,
        )

        return {
            "alarm_notify_group_id": response.get_alarm_notify_group_id(),
        }
            
    except TLSException as e:
        logger.error("create_alarm_notify_group_resource error: {}".format(str(e)))
        raise e


async def delete_alarm_notify_group_resource(
    auth_info: Dict,
    alarm_notify_group_id: str,
) -> Dict:
    """
    Delete an alarm notification group
    """
    try:
        request = DeleteAlarmNotifyGroupRequest(
            alarm_notify_group_id=alarm_notify_group_id
        )
            
        response: DeleteAlarmNotifyGroupResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_alarm_notify_group",
            delete_alarm_notify_group_request=request,
        )
        
        return {
            "request_id": response.get_request_id(),
        }
            
    except TLSException as e:
        logger.error("delete_alarm_notify_group_resource error: {}".format(str(e)))
        raise e


async def describe_alarm_notify_groups_resource(
    auth_info: Dict,
    alarm_notify_group_name: Optional[str] = None,
    alarm_notify_group_id: Optional[str] = None,
    receiver_name: Optional[str] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
    iam_project_name: Optional[str] = None,
) -> Dict:
    """
    Describe alarm notification groups
    """
    try:
        request = DescribeAlarmNotifyGroupsRequest(
            alarm_notify_group_name=alarm_notify_group_name,
            alarm_notify_group_id=alarm_notify_group_id,
            receiver_name=receiver_name,
            page_number=page_number,
            page_size=page_size,
            iam_project_name=iam_project_name
        )
            
        response: DescribeAlarmNotifyGroupsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_alarm_notify_groups",
            describe_alarm_notify_groups_request=request,
        )
        notify_groups = response.get_alarm_notify_groups()
        for group in notify_groups:
            if group.get_receivers() is not None:
                group.receivers = [vars(receiver) for receiver in group.get_receivers()]

        return {
            "total": response.get_total(),
            "alarm_notify_groups": [vars(group) for group in notify_groups],
        }
    except TLSException as e:
        logger.error("describe_alarm_notify_groups_resource error: {}".format(str(e)))
        raise e


async def create_alarm_resource(
    auth_info: Dict,
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
) -> Dict:
    """
    Create an alarm
    """
    try:
        from volcengine.tls.tls_requests import QueryRequest
        from volcengine.tls.data import AlarmPeriodSetting
        from volcengine.tls.tls_requests import RequestCycle
        from volcengine.tls.data import JoinConfig
        from volcengine.tls.data import TriggerCondition

        query_request_objects = []
        for query_req in query_request:
            query_obj = QueryRequest(** query_req)
            query_request_objects.append(query_obj)
        
        from volcengine.tls.tls_requests import RequestCycle
        cycle_obj = RequestCycle(** request_cycle)

        
        request = CreateAlarmRequest(
            project_id=project_id,
            alarm_name=alarm_name,
            query_request=query_request_objects,
            request_cycle=cycle_obj,
            condition=condition,
            alarm_period=alarm_period,
            alarm_notify_group=alarm_notify_group,
            status=status,
            trigger_period=trigger_period,
            user_define_msg=user_define_msg,
            severity=severity,
            alarm_period_detail=AlarmPeriodSetting(**alarm_period_detail) if alarm_period_detail else None,
            join_configurations=[JoinConfig(**join_config) for join_config in join_configurations] if join_configurations else None,
            trigger_conditions=[TriggerCondition(**trigger_condition) for trigger_condition in trigger_conditions] if trigger_conditions else None,
        )
            
        response: CreateAlarmResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_alarm",
            create_alarm_request=request,
        )
        
        return {
            "alarm_id": response.get_alarm_id(),
        }

            
    except TLSException as e:
        logger.error("create_alarm_resource error: {}".format(str(e)))
        raise e


async def delete_alarm_resource(
    auth_info: Dict,
    alarm_id: str,
) -> Dict:
    """
    Delete an alarm
    """
    try:
        request = DeleteAlarmRequest(
            alarm_id=alarm_id
        )
            
        response: DeleteAlarmResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_alarm",
            delete_alarm_request=request,
        )
        
        return {
            "request_id": response.get_request_id(),
        }
            
    except TLSException as e:
        logger.error("delete_alarm_resource error: {}".format(str(e)))
        raise e


async def describe_alarms_resource(
    auth_info: Dict,
    project_id: str,
    alarm_name: Optional[str] = None,
    alarm_id: Optional[str] = None,
    topic_name: Optional[str] = None,
    topic_id: Optional[str] = None,
    status: Optional[bool] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
) -> Dict:
    """
    Describe alarms
    """
    try:

        request = DescribeAlarmsRequest(
            project_id=project_id,
            alarm_name=alarm_name,
            alarm_id=alarm_id,
            topic_name=topic_name,
            topic_id=topic_id,
            status=status,
            page_number=page_number,
            page_size=page_size
        )
            
        response: DescribeAlarmsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_alarms",
            describe_alarms_request=request,
        )

        alarms = response.get_alarms()
        for alarm in alarms:
            if alarm.get_query_request() is not None:
                alarm.query_request = [vars(req) for req in alarm.get_query_request()]
            if alarm.get_request_cycle() is not None:
                alarm.request_cycle = vars(alarm.get_request_cycle())
            if alarm.get_alarm_notify_group() is not None:
                for notify_group in alarm.get_alarm_notify_group():
                    if notify_group.get_receivers() is not None:
                        notify_group.receivers = [vars(receiver) for receiver in notify_group.get_receivers()]
                alarm.alarm_notify_group = [vars(group) for group in alarm.get_alarm_notify_group()]
            if alarm.get_alarm_period_detail() is not None:
                alarm.alarm_period_detail = alarm.get_alarm_period_detail().json()
            if alarm.get_join_configurations() is not None:
                alarm.join_configurations = [vars(config) for config in alarm.get_join_configurations()]
            if alarm.get_trigger_conditions() is not None:
                alarm.trigger_conditions = [vars(condition) for condition in alarm.get_trigger_conditions()]



        return {
            "total": response.get_total(),
            "alarms": [vars(alarm) for alarm in alarms],
        }
            
    except TLSException as e:
        logger.error("describe_alarms_resource error: {}".format(str(e)))
        raise e