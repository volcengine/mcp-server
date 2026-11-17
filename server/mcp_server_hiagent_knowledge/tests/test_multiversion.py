from __future__ import annotations
import asyncio
import inspect
import pytest
from mcp_server_hiagent_knowledge import main
from mcp_server_hiagent_knowledge.common import config
from mcp_server_hiagent_knowledge.common.tools.dataset import get_dataset
from mcp_server_hiagent_knowledge.versions import DEFAULT_VERSION, load_version_module
from mcp_server_hiagent_knowledge.versions.v3_1_0.tools import dataset as v310
from mcp_server_hiagent_knowledge.versions.v3_2_1.tools import dataset as v321
from mcp_server_hiagent_knowledge.versions.v3_3_0.tools import dataset as v330

class RecordingClient:
    def __init__(self):
        self.calls = []
        self.response = {"Result": {}}
    def call(self, **kwargs):
        self.calls.append(kwargs)
        return self.response

def test_default_is_330_and_shared_objects_are_identical():
    assert DEFAULT_VERSION == "v3.3.0"
    assert v310.get_dataset is v321.get_dataset is get_dataset
    assert v330.get_dataset is not get_dataset
    for version in ["v3.1.0", "v3.2.1", "v3.3.0"]:
        assert load_version_module(version).load_server_config is config.load_server_config

@pytest.mark.parametrize("version,name,required,fields", [
    ("v3.1.0", "list_datasets", ["workspace_id"], {"workspace_id", "name", "page_number", "page_size"}),
    ("v3.2.1", "list_datasets", ["workspace_id"], {"workspace_id", "name", "page_number", "page_size"}),
    ("v3.3.0", "list_datasets", [], {"workspace_id", "user_id", "keyword", "limit", "cursor", "ids"}),
])
def test_version_schema_and_filters_are_isolated(version, name, required, fields):
    impl = load_version_module(version)
    tools = asyncio.run(impl.create_mcp_server(client=RecordingClient(), enabled_tools=[name]).list_tools())
    assert {t.name for t in tools} == {"health_check", name}
    tool = next(t for t in tools if t.name == name)
    assert tool.parameters.get("required", []) == required
    assert set(tool.parameters["properties"]) == fields
    other = "nonexistent_discovery_tool"
    with pytest.raises(ValueError, match="unknown tool name"):
        impl.create_mcp_server(client=RecordingClient(), enabled_tools=[other])

def test_321_reuses_310_discovery_objects():
    assert v321.list_datasets is v310.list_datasets
    assert v321.register_dataset_tools is v310.register_dataset_tools
    assert v321.DATASET_TOOL_NAMES is v310.DATASET_TOOL_NAMES
    assert v321.DATASET_TOOL_NAMES == ("list_datasets", "get_dataset")

@pytest.mark.parametrize("name", [None, "", "finance"])
@pytest.mark.parametrize("page_number,page_size", [(1, 20), (2, 50)])
def test_321_request_retains_310_contract(name, page_number, page_size):
    client = RecordingClient()
    assert v321.list_datasets(client, workspace_id="ws", name=name, page_number=page_number, page_size=page_size) is client.response
    body = {"WorkspaceID": "ws", "PageNumber": page_number, "PageSize": page_size}
    if name is not None:
        body["Filter"] = {"Name": name}
    assert client.calls == [{"action": "ListDatasets", "version": "2023-08-01", "service": "app", "body": body}]

def test_321_workspace_remains_required():
    assert inspect.signature(v321.list_datasets).parameters["workspace_id"].default is inspect.Parameter.empty
    with pytest.raises(ValueError, match="workspace_id"):
        v321.list_datasets(RecordingClient(), workspace_id="")

@pytest.mark.parametrize("version", ["v3.1.0", "v3.2.1", "v3.3.0"])
def test_unchanged_retrieval_and_health_for_all_versions(version):
    client = RecordingClient()
    server = load_version_module(version).create_mcp_server(client=client)
    asyncio.run(server.call_tool("search_knowledge", {"workspace_id": "ws", "dataset_ids": ["ds"], "queries": ["q"]}))
    assert client.calls[0]["body"] == {"WorkspaceID": "ws", "DatasetIDs": ["ds"], "ToolName": "knowledge_search", "KnowledgeSearch": {"Queries": ["q"]}}

@pytest.mark.parametrize("env,flag,expected", [(None, None, "v3.3.0"), ("v3.2.1", None, "v3.2.1"), ("v3.2.1", "v3.3.0", "v3.3.0"), ("v3.3.0", "v3.1.0", "v3.1.0")])
def test_cli_version_precedence(monkeypatch, env, flag, expected):
    selected = []
    class Stub:
        def run(self, **kwargs):
            pass
    for version in ["v3.1.0", "v3.2.1", "v3.3.0"]:
        def create(*, _version=version, **kwargs):
            selected.append(_version)
            return Stub()
        monkeypatch.setattr(load_version_module(version), "create_mcp_server", create)
    for key in ["HIAGENT_VERSION", "HIAGENT_TOOLS", "HIAGENT_DISABLED_TOOLS"]:
        monkeypatch.delenv(key, raising=False)
    if env:
        monkeypatch.setenv("HIAGENT_VERSION", env)
    monkeypatch.setattr("sys.argv", ["hiagent"] + (["--hiagent-version", flag] if flag else []))
    main.main()
    assert selected == [expected]
