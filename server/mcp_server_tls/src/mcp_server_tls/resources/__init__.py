# src/server/resources/__init__.py

from mcp_server_tls.resources.project import describe_project_resource, describe_projects_resource, create_project_resource, delete_project_resource

from mcp_server_tls.resources.topic import describe_topic_resource, describe_topics_resource, create_topic_resource, delete_topic_resource

from mcp_server_tls.resources.log import search_logs_v2_resource, put_logs_v2_resource, consume_logs_resource, describe_cursor_resource, describe_log_context_resource

from mcp_server_tls.resources.index import create_index_resource, delete_index_resource, describe_index_resource

from mcp_server_tls.resources.text_analysis import (
    create_app_instance_resource,
    describe_app_instances_resource,
    create_app_scene_meta_resource,
    describe_session_answer_resource,
)

from mcp_server_tls.resources.download import create_download_task_resource, describe_download_tasks_resource, describe_download_url_resource

from mcp_server_tls.resources.host_group import create_host_group_resource, delete_host_group_resource, describe_host_group_resource, describe_host_groups_resource, describe_hosts_resource, describe_host_group_rules_resource

from mcp_server_tls.resources.rule import create_rule_resource, delete_rule_resource, describe_rule_resource, describe_rules_resource, apply_rule_to_host_groups_resource, delete_rule_from_host_groups_resource

from mcp_server_tls.resources.alarm import create_alarm_notify_group_resource, delete_alarm_notify_group_resource, describe_alarm_notify_groups_resource, create_alarm_resource, delete_alarm_resource, describe_alarms_resource

SUPPORT_RESOURCES = {
    # project
    "describe_project": {
        "fn": describe_project_resource,
        "uri": "/DescribeProject?ProjectId={project_id}",
    },
    "describe_projects": {
        "fn": describe_projects_resource,
        "uri": "/DescribeProjects",
    },
    "create_project": {
        "fn": create_project_resource,
        "uri": "/CreateProject",
    },
    "delete_project": {
        "fn": delete_project_resource,
        "uri": "/DeleteProject?ProjectId={project_id}",
    },
    # topic
    "describe_topic": {
        "fn": describe_topic_resource,
        "uri": "/DescribeTopic?TopicId={topic_id}",
    },
    "describe_topics": {
        "fn": describe_topics_resource,
        "uri": "/DescribeTopics/ProjectId={project_id}",
    },
    "create_topic": {
        "fn": create_topic_resource,
        "uri": "/CreateTopic",
    },
    "delete_topic": {
        "fn": delete_topic_resource,
        "uri": "/DeleteTopic?TopicId={topic_id}",
    },
    # log
    "search_logs_v2_resource": {
        "fn": search_logs_v2_resource,
        "uri": "/SearchLogs?topic_id={topic_id}&query={query}&start_time={start_time}&end_time={end_time}&limit={limit}",
    },
    "put_logs_v2_resource": {
        "fn": put_logs_v2_resource,
        "uri": "/putLogs?logs={logs}&log_time={log_time}"
    },
    "consume_logs_resource": {
        "fn": consume_logs_resource,
        "uri": "/ConsumeLogs?topic_id={topic_id}&shard_id={shard_id}&cursor={cursor}"
    },
    "describe_cursor_resource": {
        "fn": describe_cursor_resource,
        "uri": "/DescribeCursor?topic_id={topic_id}&shard_id={shard_id}&from_time={from_time}"
    },
    "describe_log_context_resource": {
        "fn": describe_log_context_resource,
        "uri": "/DescribeLogContext?topic_id={topic_id}&context_flow={context_flow}&package_offset={package_offset}&source={source}"
    },
    # index
    "create_index_resource": {
        "fn": create_index_resource,
        "uri": "/CreateIndex"
    },
    "delete_index_resource": {
        "fn": delete_index_resource,
        "uri": "/DeleteIndex?topic_id={topic_id}"
    },
    "describe_index_resource": {
        "fn": describe_index_resource,
        "uri": "/DescribeIndex?topic_id={topic_id}"
    },
    # text_analysis
    "create_app_instance_resource": {
        "fn": create_app_instance_resource,
        "uri": "/CreateAppInstance?InstanceName={instance_name}&InstanceType={instance_type}&Description={description}",
    },
    "describe_app_instances_resource": {
        "fn": describe_app_instances_resource,
        "uri": "/DescribeAppInstances?InstanceId={instance_name}&InstanceType={instance_type}",
    },
    "create_app_scene_meta_resource": {
        "fn": create_app_scene_meta_resource,
        "uri": "/CreateAppSceneMeta?InstanceId={instance_id}&CreateAPPMetaType={app_meta_type}&Id={topic_id}&Record={record}",
    },
    "describe_session_answer_resource": {
        "fn": describe_session_answer_resource,
        "uri":  "/DescribeSessionAnswer?InstanceId={instance_id}&TopicId={topic_id}&SessionId={session_id}"
"&Question={question}&ParentMessageId={parent_message_id}&QuestionId={question_id}&Intent={intent}",
    },
    # download
    "create_download_task_resource": {
        "fn": create_download_task_resource,
        "uri": "/CreateDownloadTask"
    },
    "describe_download_tasks_resource": {
        "fn": describe_download_tasks_resource,
        "uri": "/DescribeDownloadTasks?TopicId={topic_id}&PageNumber={page_number}&PageSize={page_size}&TaskName={task_name}"
    },
    "describe_download_url_resource": {
        "fn": describe_download_url_resource,
        "uri": "/DescribeDownloadUrl?TaskId={task_id}"
    },
    # host group
    "create_host_group_resource": {
        "fn": create_host_group_resource,
        "uri": "/CreateHostGroup"
    },
    "delete_host_group_resource": {
        "fn": delete_host_group_resource,
        "uri": "/DeleteHostGroup?HostGroupId={host_group_id}"
    },
    "describe_host_group_resource": {
        "fn": describe_host_group_resource,
        "uri": "/DescribeHostGroup?HostGroupId={host_group_id}"
    },
    "describe_host_groups_resource": {
        "fn": describe_host_groups_resource,
        "uri": "/DescribeHostGroups"
    },
    "describe_hosts_resource": {
        "fn": describe_hosts_resource,
        "uri": "/DescribeHosts?HostGroupId={host_group_id}&Ip={ip}&HeartbeatStatus={heartbeat_status}&PageNumber={page_number}&PageSize={page_size}"
    },
    "describe_host_group_rules_resource": {
        "fn": describe_host_group_rules_resource,
        "uri": "/DescribeHostGroupRules?HostGroupId={host_group_id}&PageNumber={page_number}&PageSize={page_size}"
    },
    # rule
    "create_rule_resource": {
        "fn": create_rule_resource,
        "uri": "/CreateRule"
    },
    "delete_rule_resource": {
        "fn": delete_rule_resource,
        "uri": "/DeleteRule?RuleId={rule_id}"
    },
    "describe_rule_resource": {
        "fn": describe_rule_resource,
        "uri": "/DescribeRule?RuleId={rule_id}"
    },
    "describe_rules_resource": {
        "fn": describe_rules_resource,
        "uri": "/DescribeRules"
    },
    "apply_rule_to_host_groups_resource": {
        "fn": apply_rule_to_host_groups_resource,
        "uri": "/ApplyRuleToHostGroups"
    },
    "delete_rule_from_host_groups_resource": {
        "fn": delete_rule_from_host_groups_resource,
        "uri": "/DeleteRuleFromHostGroups"
    },
    # alarm
    "create_alarm_notify_group_resource": {
        "fn": create_alarm_notify_group_resource,
        "uri": "/CreateAlarmNotifyGroup"
    },
    "delete_alarm_notify_group_resource": {
        "fn": delete_alarm_notify_group_resource,
        "uri": "/DeleteAlarmNotifyGroup?AlarmNotifyGroupId={alarm_notify_group_id}"
    },
    "describe_alarm_notify_groups_resource": {
        "fn": describe_alarm_notify_groups_resource,
        "uri": "/DescribeAlarmNotifyGroups"
    },
    "create_alarm_resource": {
        "fn": create_alarm_resource,
        "uri": "/CreateAlarm"
    },
    "delete_alarm_resource": {
        "fn": delete_alarm_resource,
        "uri": "/DeleteAlarm?AlarmId={alarm_id}"
    },
    "describe_alarms_resource": {
        "fn": describe_alarms_resource,
        "uri": "/DescribeAlarms"
    }
}
