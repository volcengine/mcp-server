from __future__ import annotations
import asyncio
from typing import Any
import pytest
from mcp_server_hiagent_knowledge.versions.v3_3_0.server import create_mcp_server

class RecordingClient:
    def __init__(self):
        self.calls = []
    def call(self, **kwargs):
        self.calls.append(kwargs)
        return {"ResponseMetadata": {"Action": kwargs["action"]}, "Result": {}}

def _tool_names(server):
    return {tool.name for tool in asyncio.run(server.list_tools())}

def test_server_registers_knowledge_engine_tools():
    assert _tool_names(create_mcp_server(client=RecordingClient())) == {
        "health_check", "list_datasets", "get_dataset", "search_knowledge", "grep_knowledge_chunks",
        "list_document_infos", "list_document_chunks", "search_wiki", "read_wiki_page",
        "read_wiki_source_chunk", "read_wiki_source_doc"}

def test_injected_client_is_used_without_headers():
    client = RecordingClient()
    server = create_mcp_server(client=client)
    asyncio.run(server.call_tool("list_datasets", {"workspace_id": "ws-1"}))
    assert client.calls[0]["action"] == "CallKnowledgeTool"
    assert client.calls[0]["body"]["WorkspaceID"] == "ws-1"

def test_enabled_tools_allowlist_narrows_scope():
    assert _tool_names(create_mcp_server(client=RecordingClient(), enabled_tools=["search_wiki", "read_wiki_page"])) == {"health_check", "search_wiki", "read_wiki_page"}

def test_disabled_tools_denylist_removes_scope():
    names = _tool_names(create_mcp_server(client=RecordingClient(), disabled_tools=["grep_knowledge_chunks", "search_knowledge"]))
    assert "grep_knowledge_chunks" not in names
    assert "search_knowledge" not in names
    assert {"health_check", "list_datasets"} <= names

def test_allowlist_then_denylist_compose():
    assert _tool_names(create_mcp_server(client=RecordingClient(), enabled_tools=["search_wiki", "read_wiki_page", "search_knowledge"], disabled_tools=["search_knowledge"])) == {"health_check", "search_wiki", "read_wiki_page"}

def test_empty_allowlist_keeps_only_health_check():
    assert _tool_names(create_mcp_server(client=RecordingClient(), enabled_tools=[])) == {"health_check"}

def test_allowlist_may_list_health_check_explicitly():
    assert _tool_names(create_mcp_server(client=RecordingClient(), enabled_tools=["health_check"])) == {"health_check"}

def test_unknown_tool_name_raises():
    with pytest.raises(ValueError, match="unknown tool name"):
        create_mcp_server(client=RecordingClient(), enabled_tools=["does_not_exist"])

def test_dataset_discovery_schema_exposes_no_identity_channel():
    tools = asyncio.run(create_mcp_server(client=RecordingClient()).list_tools())
    tool = next(t for t in tools if t.name == "list_datasets")
    assert set(tool.parameters["properties"]) == {"workspace_id", "user_id", "keyword", "limit", "cursor", "ids"}
    assert tool.parameters.get("required", []) == []

def test_dataset_discovery_is_filterable_by_unified_name():
    assert _tool_names(create_mcp_server(client=RecordingClient(), enabled_tools=["list_datasets"])) == {"health_check", "list_datasets"}
    assert "list_datasets" not in _tool_names(create_mcp_server(client=RecordingClient(), disabled_tools=["list_datasets"]))
    with pytest.raises(ValueError, match="unknown tool name"):
        create_mcp_server(client=RecordingClient(), enabled_tools=["nonexistent_discovery_tool"])
