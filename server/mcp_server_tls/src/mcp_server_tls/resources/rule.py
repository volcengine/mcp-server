import json
import logging
from typing import Optional, Dict, Any, List
from volcengine.tls.TLSService import TLSService
from volcengine.tls.const import RULE_INFOS
from volcengine.tls.data import FilterKeyRegex, LogTemplate, KubernetesRule, RuleInfo
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import (
    CreateRuleRequest,
    DeleteRuleRequest,
    DescribeRuleRequest,
    DescribeRulesRequest,
    ApplyRuleToHostGroupsRequest,
    DeleteRuleFromHostGroupsRequest
)
from volcengine.tls.tls_responses import (
    CreateRuleResponse,
    DeleteRuleResponse,
    DescribeRuleResponse,
    DescribeRulesResponse,
    ApplyRuleToHostGroupsResponse,
    DeleteRuleFromHostGroupsResponse
)

from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)


async def create_rule_resource(
    auth_info: Dict,
    topic_id: str,
    rule_name: str,
    paths: Optional[List[str]] = None,
    log_type: Optional[str] = "minimalist_log",
    extract_rule: Optional[Dict] = None,
    exclude_paths: Optional[List[Dict]] = None,
    user_define_rule: Optional[Dict] = None,
    log_sample: Optional[str] = None,
    input_type: Optional[int] = 0,
    container_rule: Optional[Dict] = None,
) -> Dict:
    """
    Create a log collection rule
    """
    try:
        from volcengine.tls.tls_requests import ExtractRule, ExcludePath, UserDefineRule, ContainerRule
        
        extract_rule_obj = None
        if extract_rule:
            extract_rule_obj = ExtractRule(**extract_rule)
            if "filter_key_regex" in extract_rule and extract_rule["filter_key_regex"]:
                extract_rule_obj.filter_key_regex = []
                for filter_key_regex in extract_rule["filter_key_regex"]:
                    extract_rule_obj.filter_key_regex.append(FilterKeyRegex(**filter_key_regex))
            if "log_template" in extract_rule and extract_rule["log_template"]:
                extract_rule_obj.log_template = LogTemplate(**extract_rule["log_template"])

        exclude_paths_obj = None
        if exclude_paths:
            exclude_paths_obj = []
            for exclude_path in exclude_paths:
                exclude_paths_obj.append(ExcludePath(**exclude_path))
        
        user_define_rule_obj = None
        if user_define_rule:
            user_define_rule_obj = UserDefineRule(**user_define_rule)
        
        container_rule_obj = None
        if container_rule:
            container_rule_obj = ContainerRule(**container_rule)
            if "kubernetes_rule" in container_rule and container_rule["kubernetes_rule"]:
                container_rule_obj.kubernetes_rule = KubernetesRule(**container_rule["kubernetes_rule"])

        request = CreateRuleRequest(
            topic_id=topic_id,
            rule_name=rule_name,
            paths=paths,
            log_type=log_type,
            extract_rule=extract_rule_obj,
            exclude_paths=exclude_paths_obj,
            user_define_rule=user_define_rule_obj,
            log_sample=log_sample,
            input_type=input_type,
            container_rule=container_rule_obj
        )
            
        response: CreateRuleResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_rule",
            create_rule_request=request,
        )

        return {
            "rule_id": response.get_rule_id(),
        }

    except TLSException as e:
        logger.error("create_rule_resource error: {}".format(str(e)))
        raise e


async def delete_rule_resource(
    auth_info: Dict,
    rule_id: str,
) -> Dict:
    """
    Delete a log collection rule
    """
    try:
        request = DeleteRuleRequest(
            rule_id=rule_id
        )
            
        response: DeleteRuleResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_rule",
            delete_rule_request=request,
        )
        
        return {
            "request_id": response.get_request_id(),
        }
            
    except TLSException as e:
        logger.error("delete_rule_resource error: {}".format(str(e)))
        raise e


async def describe_rule_resource(
    auth_info: Dict,
    rule_id: str,
) -> Dict:
    """
    Describe a log collection rule
    """
    try:
        request = DescribeRuleRequest(
            rule_id=rule_id
        )
            
        response: DescribeRuleResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_rule",
            describe_rule_request=request,
        )

        rule_info: RuleInfo = response.get_rule_info()
        if rule_info:
            if rule_info.extract_rule:
                rule_info.extract_rule = rule_info.extract_rule.json()
            if rule_info.exclude_paths:
                rule_info.exclude_paths = [vars(exclude_path) for exclude_path in rule_info.exclude_paths]
            if rule_info.user_define_rule:
                rule_info.user_define_rule = rule_info.user_define_rule.json()
            if rule_info.container_rule:
                rule_info.container_rule = rule_info.container_rule.json()
            response.rule_info = vars(rule_info)

        host_group_infos = response.get_host_group_infos()
        if host_group_infos:
            response.host_group_infos = [vars(host_group_info) for host_group_info in host_group_infos]
        result = vars(response)
        result.pop("headers")
        result.pop("response")

        return result
            
    except TLSException as e:
        logger.error("describe_rule_resource error: {}".format(str(e)))
        raise e


async def describe_rules_resource(
    auth_info: Dict,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
    iam_project_name: Optional[str] = None,
    rule_id: Optional[str] = None,
    rule_name: Optional[str] = None,
    topic_id: Optional[str] = None,
    topic_name: Optional[str] = None,
    page_number: Optional[int] = 1,
    page_size: Optional[int] = 20,
    log_type: Optional[str] = None,
    pause: Optional[int] = None,
) -> Dict:
    """
    Describe log collection rules with filtering
    """
    try:
        request = DescribeRulesRequest(
            project_id=project_id,
            project_name=project_name,
            iam_project_name=iam_project_name,
            rule_id=rule_id,
            rule_name=rule_name,
            topic_id=topic_id,
            topic_name=topic_name,
            page_number=page_number,
            page_size=page_size,
            log_type=log_type,
            pause=pause
        )
            
        response: DescribeRulesResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_rules",
            describe_rules_request=request,
        )

        return {
            "total": response.get_total(),
            "rules": response.response[RULE_INFOS],
        }
            
    except TLSException as e:
        logger.error("describe_rules_resource error: {}".format(str(e)))
        raise e


async def apply_rule_to_host_groups_resource(
    auth_info: Dict,
    rule_id: str,
    host_group_ids: List[str],
) -> Dict:
    """
    Apply rule to host groups
    """
    try:
        request = ApplyRuleToHostGroupsRequest(
            rule_id=rule_id,
            host_group_ids=host_group_ids
        )
            
        response: ApplyRuleToHostGroupsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="apply_rule_to_host_groups",
            apply_rule_to_host_groups_request=request,
        )
        
        return {
            "request_id": response.get_request_id(),
        }
            
    except TLSException as e:
        logger.error("apply_rule_to_host_groups_resource error: {}".format(str(e)))
        raise e


async def delete_rule_from_host_groups_resource(
    auth_info: Dict,
    rule_id: str,
    host_group_ids: List[str],
) -> Dict:
    """
    Delete rule from host groups
    """
    try:
        request = DeleteRuleFromHostGroupsRequest(
            rule_id=rule_id,
            host_group_ids=host_group_ids
        )
            
        response: DeleteRuleFromHostGroupsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_rule_from_host_groups",
            delete_rule_from_host_groups_request=request,
        )
        
        return {
            "request_id": response.get_request_id(),
        }
            
    except TLSException as e:
        logger.error("delete_rule_from_host_groups_resource error: {}".format(str(e)))
        raise e