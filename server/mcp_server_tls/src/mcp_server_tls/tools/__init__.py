# src/server/tools/__init__.py

from mcp_server_tls.tools.project import describe_project_tool, describe_projects_tool, create_project_tool, delete_project_tool

from mcp_server_tls.tools.topic import describe_topic_tool, describe_topics_tool, create_topic_tool, delete_topic_tool

from mcp_server_tls.tools.log import search_logs_v2_tool, put_logs_v2_tool, consume_logs_tool, describe_cursor_tool, describe_log_context_tool

from mcp_server_tls.tools.index import create_index_tool, delete_index_tool, describe_index_tool

from mcp_server_tls.tools.text_analysis import text2sql

from mcp_server_tls.tools.download import create_download_task_tool, describe_download_tasks_tool, describe_download_url_tool

from mcp_server_tls.tools.host_group import create_host_group_tool, delete_host_group_tool, describe_host_group_tool, describe_host_groups_tool, describe_hosts_tool, describe_host_group_rules_tool

from mcp_server_tls.tools.rule import create_rule_tool, delete_rule_tool, describe_rule_tool, describe_rules_tool, apply_rule_to_host_groups_tool, delete_rule_from_host_groups_tool

from mcp_server_tls.tools.alarm import create_alarm_notify_group_tool, delete_alarm_notify_group_tool, describe_alarm_notify_groups_tool, create_alarm_tool, delete_alarm_tool, describe_alarms_tool

SUPPORT_TOOLS = {
    # project
    "describe_project_tool": describe_project_tool,
    "describe_projects_tool": describe_projects_tool,
    "create_project_tool": create_project_tool,
    # "delete_project_tool": delete_project_tool,
    # topic
    "describe_topic_tool": describe_topic_tool,
    "describe_topics_tool": describe_topics_tool,
    "create_topic_tool": create_topic_tool,
    # "delete_topic_tool": delete_topic_tool,
    # log
    "search_logs_v2_tool": search_logs_v2_tool,
    "put_logs_v2_tool": put_logs_v2_tool,
    # "consume_logs_tool": consume_logs_tool,
    # "describe_cursor_tool": describe_cursor_tool,
    # "describe_log_context_tool": describe_log_context_tool,
    # index
    "create_index_tool": create_index_tool,
    # "delete_index_tool": delete_index_tool,
    "describe_index_tool": describe_index_tool,
    # text_analysis
    "text2sql": text2sql,
    # download
    "create_download_task_tool": create_download_task_tool,
    "describe_download_tasks_tool": describe_download_tasks_tool,
    "describe_download_url_tool": describe_download_url_tool,
    # # host group
    # "create_host_group_tool": create_host_group_tool,
    # "delete_host_group_tool": delete_host_group_tool,
    # "describe_host_group_tool": describe_host_group_tool,
    # "describe_host_groups_tool": describe_host_groups_tool,
    # "describe_hosts_tool": describe_hosts_tool,
    # "describe_host_group_rules_tool": describe_host_group_rules_tool,
    # # rule
    # "create_rule_tool": create_rule_tool,
    # "delete_rule_tool": delete_rule_tool,
    # "describe_rule_tool": describe_rule_tool,
    # "describe_rules_tool": describe_rules_tool,
    # "apply_rule_to_host_groups_tool": apply_rule_to_host_groups_tool,
    # "delete_rule_from_host_groups_tool": delete_rule_from_host_groups_tool,
    # # alarm
    # "create_alarm_notify_group_tool": create_alarm_notify_group_tool,
    # "delete_alarm_notify_group_tool": delete_alarm_notify_group_tool,
    # "describe_alarm_notify_groups_tool": describe_alarm_notify_groups_tool,
    # "create_alarm_tool": create_alarm_tool,
    # "delete_alarm_tool": delete_alarm_tool,
    # "describe_alarms_tool": describe_alarms_tool,
}
