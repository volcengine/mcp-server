import logging
from typing import Optional, Dict, Any, List

from mcp_server_tls.config import TLS_CONFIG
from mcp_server_tls.resources.rule import (
    create_rule_resource,
    delete_rule_resource,
    describe_rule_resource,
    describe_rules_resource,
    apply_rule_to_host_groups_resource,
    delete_rule_from_host_groups_resource
)
from mcp_server_tls.utils import get_sdk_auth_info

logger = logging.getLogger(__name__)


async def create_rule_tool(
    rule_name: str,
    topic_id: Optional[str] = None,
    paths: Optional[List[str]] = None,
    log_type: Optional[str] = "minimalist_log",
    extract_rule: Optional[Dict] = None,
    exclude_paths: Optional[List[Dict]] = None,
    user_define_rule: Optional[Dict] = None,
    log_sample: Optional[str] = None,
    input_type: Optional[int] = 0,
    container_rule: Optional[Dict] = None,
) -> dict:
    """Create a log collection rule.

    This tool creates a log collection rule for a specified topic.

    Args:
        rule_name: Collection rule name (required)
        topic_id: Log topic ID
        paths: Collection paths list (optional, defaults to None)
        log_type: Log type (optional, defaults to "minimalist_log")
        extract_rule: Log extraction rule configuration (optional)
            delimiter: Log delimiter
            begin_regex: Regular expression for matching the first line of logs
            log_regex: Regular expression for matching the entire log entry
            keys: Log field names
            time_key: Field name of the log time field
            time_format: Parsing format for the time field
            time_zone: Time zone of the log time field
            filter_key_regex: Regular expression for filtering fields
                key: Name of the filter field
                regex: Regular expression that the log content of the filter field needs to match
            un_match_up_load_switch: Whether to upload logs that failed parsing
            un_match_log_key: Key name for logs that failed parsing (when uploading such logs)
            log_template: Automatically extract log fields based on the specified log template
                log_type: Type of log template: Nginx
                log_format: Content of the log template
            quote: Quotation mark
            time_extract_regex: Regular expression for extracting the time field
            enable_nanosecond: Whether to enable parsing of nanosecond-level time
            time_sample: Sample log of the time field
        exclude_paths: Exclude paths configuration (optional)
            type: Exclude path type(File, Path)
            value: Exclude path value
        user_define_rule: User-defined rule configuration (optional)
            parse_path_rule: Rule for parsing collection paths
                path_sample: Sample collection path in actual scenarios
                regex: Regular expression used to extract path fields
                keys: List of field names
            shard_hash_key: Rule for routing log shards
                hash_key: hashkey used for shard routing
            enable_raw_log: Whether to upload raw logs
            fields: Add constant fields to logs
            plugin: LogCollector plugin configuration
                processors: LogCollector plugin processors
            advanced: LogCollector advanced configuration
                close_inactive: Waiting time to release log file handles
                close_timeout: Maximum duration for LogCollector to monitor log files
                no_line_terminator_eof_max_time: Maximum waiting time when a log file has no line terminator
                close_removed: Whether to release the log file handle after the log file is deleted
                close_renamed: Whether to release the log file handle after the log file is renamed
                close_eof: Whether to release the log file handle after reading to the end of the log file
            tail_files: LogCollector collection strategy (specifies whether LogCollector collects incremental logs or full logs)
            raw_log_key: Key name of the raw log
            enable_hostname: Whether to add a hostname field
            hostname_key: Key name of the hostname field
            host_group_label_key: Key name of the host group label field
            enable_host_group_label: Whether to add a host group label field
            tail_size_kb: Backtracking threshold for incremental collection
            ignore_older: Time threshold (in hours) for ignoring log files that have not been updated
            multi_collects_type: Allows multiple collections of log files (values: Empty, RuleID, TopicIDRuleName)
        log_sample: Log sample (optional)
        input_type: Input type, 0 for host file, 1 for K8s stdout, 2 for K8s container file (optional, defaults to 0)
        container_rule: Container collection rule (optional)
            stream: Collection mode(stdout,stderr,all)
            container_name_regex: Name of the container to be collected
            include_container_label_regex: Specifies containers to be collected; when the whitelist is not enabled, all containers are collected
            exclude_container_label_regex: Blacklist for specifying containers not to be collected; when the blacklist is not enabled, all containers are collected
            include_container_env_regex: Container environment variable whitelist for specifying containers to be collected; when the whitelist is not enabled, all containers are collected
            exclude_container_env_regex: Container environment variable blacklist for specifying containers not to be collected; when the blacklist is not enabled, all containers are collected
            env_tag: Whether to use environment variables as log tags and add them to raw log data
            kubernetes_rule: Collection rules for Kubernetes containers
                namespace_name_regex: Name of the Kubernetes Namespace to be collected; if no Namespace name is specified, all containers are collected
                workload_type: Specifies containers to be collected by workload type; only one type can be selected
                workload_name_regex: Specifies containers to be collected by workload name
                include_pod_label_regex: Pod Label whitelist for specifying containers to be collected
                exclude_pod_label_regex: Specifies containers not to be collected via Pod Label blacklist; if not enabled, all containers are collected
                pod_name_regex: Specifies containers to be collected by Pod name
                label_tag: Kubernetes Label as log tags and add them to raw log data
                annotation_tag: Kubernetes Annotation as log tags and add them to raw log data
                enable_all_label_tag: Whether to use all Kubernetes Labels as log tags and add them to raw log data
                exclude_pod_annotation_regex: Specifies containers not to be collected via Pod Annotation blacklist; if not enabled, all containers are collected
                include_pod_annotation_regex: Pod Annotation whitelist for specifying containers to be collected

    Returns:
        Dictionary containing rule_id and other information

    Examples:
        # Create rule for Kubernetes container logs
        create_rule_tool(
            topic_id="topic-k8s",
            rule_name="k8s-container-logs",
            paths=["/var/log/pods/*/*.log"],
            log_type="delimiter_log",
            extract_rule={"delimiter":"#", "keys:["time", "level", "msg"]},
            input_type=2,
            log_sample="he#hewe#werwef",
            container_rule={
              "container_name_regex": "nginx-*",
              "kubernetes_rule": {
                "namespace_name_regex": "default",
                "workload_type": "Deployment",
                "enable_all_label_tag": true
              }
            }
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        topic_id = topic_id or TLS_CONFIG.topic_id
        if not topic_id or not topic_id.strip():
            raise ValueError("topic_id is required")
        if not rule_name or not rule_name.strip():
            raise ValueError("rule_name is required")

        return await create_rule_resource(
            auth_info=auth_info,
            topic_id=topic_id,
            rule_name=rule_name,
            paths=paths,
            log_type=log_type,
            extract_rule=extract_rule,
            exclude_paths=exclude_paths,
            user_define_rule=user_define_rule,
            log_sample=log_sample,
            input_type=input_type,
            container_rule=container_rule,
        )

    except Exception as e:
        logger.error("call tool error: create_rule_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def delete_rule_tool(
    rule_id: str,
) -> dict:
    """Delete a log collection rule.

    This tool deletes a log collection rule by its ID.

    Args:
        rule_id: Rule ID (required)

    Returns:
        Dictionary containing operation result

    Examples:
        # Delete rule
        delete_rule_tool("rule-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not rule_id or not rule_id.strip():
            raise ValueError("rule_id is required")

        return await delete_rule_resource(
            auth_info=auth_info,
            rule_id=rule_id,
        )

    except Exception as e:
        logger.error("call tool error: delete_rule_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_rule_tool(
    rule_id: str,
) -> dict:
    """Describe a log collection rule.

    This tool gets detailed information about a specific collection rule.

    Args:
        rule_id: Rule ID (required)

    Returns:
        Dictionary containing rule detailed information

    Examples:
        # Get rule details
        describe_rule_tool("rule-123456")
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        if not rule_id or not rule_id.strip():
            raise ValueError("rule_id is required")

        return await describe_rule_resource(
            auth_info=auth_info,
            rule_id=rule_id,
        )

    except Exception as e:
        logger.error("call tool error: describe_rule_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def describe_rules_tool(
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
) -> dict:
    """Describe log collection rules with filtering.

    This tool queries collection rules with various filtering options and pagination.

    Args:
        project_id: Project ID for filtering (optional)
        project_name: Project name for filtering (optional)
        iam_project_name: IAM project name for filtering (optional)
        rule_id: Rule ID for filtering (optional)
        rule_name: Rule name for filtering (optional)
        topic_id: Topic ID for filtering (optional)
        topic_name: Topic name for filtering (optional)
        page_number: Page number for pagination (optional, defaults to 1)
        page_size: Page size for pagination (optional, defaults to 20, max 100)
        log_type: Log type for filtering (optional)
        pause: Pause status for filtering (optional)

    Returns:
        Dictionary containing total count and rules list

    Examples:
        # Query all rules for default project
        describe_rules_tool()

        # Query rules by name filter
        describe_rules_tool(
            rule_name="nginx-access-log"
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        project_id = project_id or TLS_CONFIG.project_id

        return await describe_rules_resource(
            auth_info=auth_info,
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
            pause=pause,
        )

    except Exception as e:
        logger.error("call tool error: describe_rules_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def apply_rule_to_host_groups_tool(
    rule_id: str,
    host_group_ids: List[str],
) -> dict:
    """Apply rule to host groups.

    This tool applies a collection rule to specified host groups.

    Args:
        rule_id: Rule ID (required)
        host_group_ids: List of host group IDs (required)

    Returns:
        Dictionary containing operation result

    Examples:
        # Apply rule to host groups
        apply_rule_to_host_groups_tool(
            rule_id="rule-123456",
            host_group_ids=["host-group-1", "host-group-2"]
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        # Validate required parameters
        if not rule_id or not rule_id.strip():
            raise ValueError("rule_id is required")
        if not host_group_ids or len(host_group_ids) == 0:
            raise ValueError("host_group_ids is required and cannot be empty")

        return await apply_rule_to_host_groups_resource(
            auth_info=auth_info,
            rule_id=rule_id,
            host_group_ids=host_group_ids,
        )

    except Exception as e:
        logger.error("call tool error: apply_rule_to_host_groups_tool, err is {}".format(str(e)))
        return {"error": str(e)}


async def delete_rule_from_host_groups_tool(
    rule_id: str,
    host_group_ids: List[str],
) -> dict:
    """Delete rule from host groups.

    This tool removes a collection rule from specified host groups.

    Args:
        rule_id: Rule ID (required)
        host_group_ids: List of host group IDs (required)

    Returns:
        Dictionary containing operation result

    Examples:
        # Remove rule from host groups
        delete_rule_from_host_groups_tool(
            rule_id="rule-123456",
            host_group_ids=["host-group-1", "host-group-2"]
        )
    """
    try:

        from mcp_server_tls.server import mcp

        auth_info = get_sdk_auth_info(mcp.get_context())

        # Validate required parameters
        if not rule_id or not rule_id.strip():
            raise ValueError("rule_id is required")
        if not host_group_ids or len(host_group_ids) == 0:
            raise ValueError("host_group_ids is required and cannot be empty")

        return await delete_rule_from_host_groups_resource(
            auth_info=auth_info,
            rule_id=rule_id,
            host_group_ids=host_group_ids,
        )

    except Exception as e:
        logger.error("call tool error: delete_rule_from_host_groups_tool, err is {}".format(str(e)))
        return {"error": str(e)}