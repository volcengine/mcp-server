# src/server/resources/__init__.py

from mcp_server_tls.resources.project import describe_project_resource, describe_projects_resource

from mcp_server_tls.resources.topic import describe_topic_resource, describe_topics_resource

from mcp_server_tls.resources.log import search_logs_v2_resource, put_logs_v2_resource

from mcp_server_tls.resources.text_analysis import (
    create_app_instance_resource,
    describe_app_instances_resource,
    create_app_scene_meta_resource,
    describe_session_answer_resource,
)

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
    # topic
    "describe_topic": {
        "fn": describe_topic_resource,
        "uri": "/DescribeTopic?TopicId={topic_id}",
    },
    "describe_topics": {
        "fn": describe_topics_resource,
        "uri": "/DescribeTopics/ProjectId={project_id}",
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
    }
}
