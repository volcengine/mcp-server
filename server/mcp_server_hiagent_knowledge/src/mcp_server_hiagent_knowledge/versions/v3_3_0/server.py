"""v3.3.0 server: shared assembly with standalone CallKnowledgeTool contract."""

from mcp_server_hiagent_knowledge.common.server import create_mcp_server as _create
from mcp_server_hiagent_knowledge.common.tools.knowledge import KNOWLEDGE_USER_ACTION
from .tools import dataset


def create_mcp_server(client=None, *, enabled_tools=None, disabled_tools=None):
    return _create(
        client,
        dataset_module=dataset,
        hiagent_version="v3.3.0",
        knowledge_action=KNOWLEDGE_USER_ACTION,
        workspace_optional=True,
        use_wiki_source_doc_tool=True,
        enabled_tools=enabled_tools,
        disabled_tools=disabled_tools,
    )
