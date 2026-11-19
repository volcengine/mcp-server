"""Shared server assembly; version packages supply only discovery differences."""
from collections.abc import Iterable
from fastmcp import FastMCP
from .client import HiAgentOpenAPIClient
from .config import load_hiagent_config
from .tools._common import OpenAPIClient
from .tools.filtering import resolve_enabled_tools
from .tools.knowledge import KNOWLEDGE_ENGINE_ACTION, KNOWLEDGE_TOOL_NAMES, register_knowledge_tools

ALWAYS_ON_TOOL_NAME = "health_check"

def _remove_tool(mcp: FastMCP, name: str) -> None:
    provider = getattr(mcp, "local_provider", None)
    if provider is not None and hasattr(provider, "remove_tool"):
        provider.remove_tool(name)
    else:
        mcp.remove_tool(name)

def create_mcp_server(client: OpenAPIClient | None = None, *, dataset_module,
                      hiagent_version: str, knowledge_action: str = KNOWLEDGE_ENGINE_ACTION,
                      enabled_tools: Iterable[str] | None = None,
                      disabled_tools: Iterable[str] | None = None) -> FastMCP:
    names = (*dataset_module.DATASET_TOOL_NAMES, *KNOWLEDGE_TOOL_NAMES)
    config = load_hiagent_config()
    openapi_client = client or HiAgentOpenAPIClient(config)
    keep = set(resolve_enabled_tools(names, enabled=enabled_tools, disabled=disabled_tools,
                                    always_on=(ALWAYS_ON_TOOL_NAME,)))
    mcp = FastMCP(name="hiagent-knowledge-mcp-server", instructions=(
        "HiAgent Knowledge MCP Server exposes capability-named knowledge tools. "
        f"Application compatibility version: {hiagent_version}. "
        f"Discover datasets with {dataset_module.DATASET_TOOL_NAMES[0]}, inspect with get_dataset. "
        "Retrieval tools: search_knowledge, grep_knowledge_chunks, list_document_infos, "
        "list_document_chunks, search_wiki, read_wiki_page, read_wiki_source_chunk, read_wiki_source_doc. "
        "Tool filters use exact names for the selected version. Supports stdio and streamable-http, "
        "AK/SK credentials from HIAGENT_TOP_HOST, HIAGENT_ACCESS_KEY_ID, HIAGENT_SECRET_ACCESS_KEY."
    ))
    @mcp.tool()
    def health_check() -> dict[str, object]:
        """Report server and configuration state, never credentials."""
        return {"status": "ok", "hiagent_version": hiagent_version, "auth": "aksk",
                "configured": config.is_configured, "top_host_configured": bool(config.top_host),
                "account_id_configured": bool(config.account_id),
                "access_key_configured": bool(config.access_key_id),
                "secret_key_configured": bool(config.secret_access_key),
                "region": config.region, "service": config.service}
    dataset_module.register_dataset_tools(mcp, openapi_client)
    register_knowledge_tools(mcp, openapi_client, action=knowledge_action)
    for name in names:
        if name not in keep:
            _remove_tool(mcp, name)
    return mcp
