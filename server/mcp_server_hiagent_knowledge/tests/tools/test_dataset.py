from __future__ import annotations
import pytest
from mcp_server_hiagent_knowledge.versions.v3_3_0.tools.dataset import get_dataset, list_datasets

class RecordingClient:
    def __init__(self):
        self.calls = []
        self.response = {"Result": {"ListDatasets": {"Items": [{"DatasetID": "own-1"}, {"DatasetID": "shared-1", "WorkspaceID": "source"}], "NextCursor": "next"}}}
    def call(self, **kwargs):
        self.calls.append(kwargs)
        return self.response

def test_discovery_without_workspace_auto_discovers():
    client = RecordingClient()
    assert list_datasets(client) is client.response
    assert client.calls == [{"action": "CallKnowledgeTool", "version": "2023-08-01", "service": "app", "body": {"ToolName": "list_datasets", "ListDatasets": {}}}]

@pytest.mark.parametrize("workspace_id", ["", "   "])
def test_discovery_treats_blank_workspace_as_unspecified(workspace_id):
    client = RecordingClient()
    list_datasets(client, workspace_id=workspace_id)
    assert "WorkspaceID" not in client.calls[0]["body"]

def test_discovery_with_workspace_scopes_request():
    client = RecordingClient()
    list_datasets(client, workspace_id="ws-1")
    assert client.calls[0]["body"] == {"WorkspaceID": "ws-1", "ToolName": "list_datasets", "ListDatasets": {}}

def test_discovery_cursor_filter_and_identity():
    client = RecordingClient()
    list_datasets(client, workspace_id="ws-1", user_id="iam", keyword="finance", limit=10, cursor="next")
    assert client.calls[0]["body"] == {"WorkspaceID": "ws-1", "ToolName": "list_datasets", "UserInfo": {"UserID": "iam", "UserChannel": "IAM"}, "ListDatasets": {"Filter": {"Keyword": "finance"}, "Limit": 10, "Cursor": "next"}}

@pytest.mark.parametrize("ids", [[], ["ds-2", "ds-1", "ds-2"]])
def test_discovery_ids_preserve_empty_and_order(ids):
    client = RecordingClient()
    list_datasets(client, ids=ids)
    assert client.calls[0]["body"]["ListDatasets"] == {"IDs": ids}

def test_discovery_empty_filter_and_cursor_are_forwarded():
    client = RecordingClient()
    list_datasets(client, keyword="", cursor="")
    assert client.calls[0]["body"]["ListDatasets"] == {"Filter": {"Keyword": ""}, "Cursor": ""}

@pytest.mark.parametrize("limit", [0, 101])
def test_discovery_leaves_value_validation_to_backend(limit):
    client = RecordingClient()
    list_datasets(client, ids=[], limit=limit)
    assert client.calls[0]["body"]["ListDatasets"] == {"IDs": [], "Limit": limit}

@pytest.mark.parametrize("user_id", ["", "   "])
def test_discovery_rejects_empty_explicit_identity(user_id):
    client = RecordingClient()
    with pytest.raises(ValueError, match="user_id"):
        list_datasets(client, workspace_id="ws-1", user_id=user_id)
    assert not client.calls

def test_discovery_only_uses_unified_tool():
    client = RecordingClient()
    list_datasets(client, workspace_id="ws-1", keyword="k", limit=5)
    assert client.calls[0]["body"]["ToolName"] == "list_datasets"
    assert set(client.calls[0]["body"]) == {"ToolName", "ListDatasets", "WorkspaceID"}

def test_get_dataset_reads_one_dataset_through_discovery():
    client = RecordingClient()
    assert get_dataset(client, workspace_id="ws-1", dataset_id="own-1") == {"Result": {"Dataset": {"DatasetID": "own-1"}}}
    assert client.calls[0] == {"action": "CallKnowledgeTool", "version": "2023-08-01", "service": "app", "body": {"WorkspaceID": "ws-1", "ToolName": "list_datasets", "ListDatasets": {"IDs": ["own-1"]}}}

def test_get_dataset_without_workspace_omits_workspace_id():
    client = RecordingClient()
    assert get_dataset(client, dataset_id="shared-1") == {"Result": {"Dataset": {"DatasetID": "shared-1", "WorkspaceID": "source"}}}
    assert client.calls[0] == {"action": "CallKnowledgeTool", "version": "2023-08-01", "service": "app", "body": {"ToolName": "list_datasets", "ListDatasets": {"IDs": ["shared-1"]}}}

@pytest.mark.parametrize("dataset_id", ["absent"])
def test_get_dataset_rejects_dataset_outside_visible_scope(dataset_id):
    with pytest.raises(ValueError, match="not visible in workspace"):
        get_dataset(RecordingClient(), workspace_id="ws-1", dataset_id=dataset_id)
    with pytest.raises(ValueError, match="not visible to the caller"):
        get_dataset(RecordingClient(), dataset_id=dataset_id)

def test_get_dataset_accepts_visible_shared_dataset():
    client = RecordingClient()
    assert get_dataset(client, workspace_id="ws-1", dataset_id="shared-1") == {"Result": {"Dataset": {"DatasetID": "shared-1", "WorkspaceID": "source"}}}

def test_get_dataset_requires_dataset_id():
    with pytest.raises(ValueError, match="dataset_id"):
        get_dataset(RecordingClient(), workspace_id="ws-1", dataset_id="")
