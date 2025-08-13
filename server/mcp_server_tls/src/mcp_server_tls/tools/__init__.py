# src/server/tools/__init__.py

from mcp_server_tls.tools.project import describe_project_tool, describe_projects_tool

from mcp_server_tls.tools.topic import describe_topic_tool, describe_topics_tool

from mcp_server_tls.tools.log import search_logs_v2_tool, put_logs_v2_tool

from mcp_server_tls.tools.text_analysis import text2sql

SUPPORT_TOOLS = {
    # project
    "describe_project_tool": describe_project_tool,
    "describe_projects_tool": describe_projects_tool,
    # topic
    "describe_topic_tool": describe_topic_tool,
    "describe_topics_tool": describe_topics_tool,
    # log
    "search_logs_v2_tool": search_logs_v2_tool,
    "put_logs_v2_tool": put_logs_v2_tool,
    # text_analysis
    "text2sql": text2sql,
}
