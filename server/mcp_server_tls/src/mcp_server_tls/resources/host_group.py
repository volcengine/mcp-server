import logging
from typing import Optional, Dict, Any, List
from volcengine.tls.TLSService import TLSService
from volcengine.tls.data import HostGroupHostsRulesInfo, RuleInfo
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import (
    CreateHostGroupRequest,
    DeleteHostGroupRequest,
    DescribeHostGroupRequest,
    DescribeHostGroupsRequest,
    DescribeHostsRequest,
    DescribeHostGroupRulesRequest
)
from volcengine.tls.tls_responses import (
    CreateHostGroupResponse,
    DeleteHostGroupResponse,
    DescribeHostGroupResponse,
    DescribeHostGroupsResponse,
    DescribeHostsResponse,
    DescribeHostGroupRulesResponse
)

from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)


async def create_host_group_resource(
        auth_info: Dict,
        host_group_name: str,
        host_group_type: str,
        host_ip_list: Optional[List[str]] = None,
        host_identifier: Optional[str] = None,
        auto_update: Optional[bool] = False,
        update_start_time: Optional[str] = None,
        update_end_time: Optional[str] = None,
        service_logging: Optional[bool] = False,
        iam_project_name: Optional[str] = None,
) -> Dict:
    """
    Create a host group
    
    This function creates a host group for log collection management.
    Host groups can be organized by IP addresses or host identifiers.

    """
    try:
        request = CreateHostGroupRequest(
            host_group_name=host_group_name,
            host_group_type=host_group_type,
            host_ip_list=host_ip_list,
            host_identifier=host_identifier,
            auto_update=auto_update,
            update_start_time=update_start_time,
            update_end_time=update_end_time,
            service_logging=service_logging,
            iam_project_name=iam_project_name
        )

        response: CreateHostGroupResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_host_group",
            create_host_group_request=request,
        )

        return {
            "host_group_id": response.get_host_group_id(),
        }


    except TLSException as e:
        logger.error("create_host_group_resource error: {}".format(str(e)))
        raise e


async def delete_host_group_resource(
        auth_info: Dict,
        host_group_id: str,
) -> Dict:
    """
    Delete a host group
    """
    try:
        request = DeleteHostGroupRequest(
            host_group_id=host_group_id
        )

        response: DeleteHostGroupResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_host_group",
            delete_host_group_request=request,
        )

        return {
            "request_id": response.get_request_id(),
        }

    except TLSException as e:
        logger.error("delete_host_group_resource error: {}".format(str(e)))
        raise e


async def describe_host_group_resource(
        auth_info: Dict,
        host_group_id: str,
) -> Dict:
    """
    Describe a host group
    """
    try:
        request = DescribeHostGroupRequest(
            host_group_id=host_group_id
        )

        response: DescribeHostGroupResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_host_group",
            describe_host_group_request=request,
        )

        host_group_info = response.get_host_group_hosts_rules_info()
        host_group_info_to_dict(host_group_info)
        return vars(host_group_info)


    except TLSException as e:
        logger.error("describe_host_group_resource error: {}".format(str(e)))
        raise e


async def describe_host_groups_resource(
        auth_info: Dict,
        host_group_id: Optional[str] = None,
        host_group_name: Optional[str] = None,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 20,
        auto_update: Optional[bool] = None,
        host_identifier: Optional[str] = None,
        service_logging: Optional[bool] = None,
        iam_project_name: Optional[str] = None,
) -> Dict:
    """
    Describe host groups with filtering
    """
    try:
        request = DescribeHostGroupsRequest(
            host_group_id=host_group_id,
            host_group_name=host_group_name,
            page_number=page_number,
            page_size=page_size,
            auto_update=auto_update,
            host_identifier=host_identifier,
            service_logging=service_logging,
            iam_project_name=iam_project_name
        )

        response: DescribeHostGroupsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_host_groups",
            describe_host_groups_request=request,
        )

        for host_group in response.get_host_group_hosts_rules_infos():
            host_group_info_to_dict(host_group)

        return {
            "total": response.get_total(),
            "host_groups": [vars(host_group) for host_group in response.get_host_group_hosts_rules_infos()],
        }

    except TLSException as e:
        logger.error("describe_host_groups_resource error: {}".format(str(e)))
        raise e


async def describe_hosts_resource(
        auth_info: Dict,
        host_group_id: str,
        ip: Optional[str] = None,
        heartbeat_status: Optional[int] = None,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 20,
) -> Dict:
    """
    Describe hosts in a host group
    """
    try:
        request = DescribeHostsRequest(
            host_group_id=host_group_id,
            ip=ip,
            heartbeat_status=heartbeat_status,
            page_number=page_number,
            page_size=page_size
        )

        response: DescribeHostsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_hosts",
            describe_hosts_request=request,
        )

        return {
            "total": response.get_total(),
            "hosts": [vars(host) for host in response.get_host_infos()],
        }
    except TLSException as e:
        logger.error("describe_hosts_resource error: {}".format(str(e)))
        raise e


async def describe_host_group_rules_resource(
        auth_info: Dict,
        host_group_id: str,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 20,
) -> Dict:
    """
    Describe rules associated with a host group
    """
    try:
        request = DescribeHostGroupRulesRequest(
            host_group_id=host_group_id,
            page_number=page_number,
            page_size=page_size
        )

        response: DescribeHostGroupRulesResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_host_group_rules",
            describe_host_group_rules_request=request,
        )
        if response.get_rule_infos() is not None:
            for rule_info in response.get_rule_infos():
                rule_info_to_dict(rule_info)

        return {
            "total": response.get_total(),
            "rules": [vars(rule_info) for rule_info in response.get_rule_infos()],
        }
    except TLSException as e:
        logger.error("describe_host_group_rules_resource error: {}".format(str(e)))
        raise e


def host_group_info_to_dict(host_group: HostGroupHostsRulesInfo):
    host_group.host_group_info = vars(host_group.get_host_group_info())
    host_group.host_infos = [vars(host_info) for host_info in host_group.get_host_infos()]
    if host_group.get_rule_infos() is not None:
        for rule_info in host_group.get_rule_infos():
            rule_info_to_dict(rule_info)
        host_group.rule_infos = [vars(rule_info) for rule_info in host_group.get_rule_infos()]


def rule_info_to_dict(rule_info: RuleInfo):
    if rule_info.get_extract_rule() is not None:
        rule_info.extract_rule = rule_info.get_extract_rule().json()
    if rule_info.get_exclude_paths() is not None:
        rule_info.exclude_paths = [vars(exclude_path) for exclude_path in rule_info.get_exclude_paths()]
    if rule_info.get_container_rule() is not None:
        rule_info.container_rule = rule_info.get_container_rule().json()
    if rule_info.get_user_define_rule() is not None:
        rule_info.user_define_rule = rule_info.get_user_define_rule().json()
