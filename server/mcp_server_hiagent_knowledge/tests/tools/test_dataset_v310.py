from __future__ import annotations
import pytest
from mcp_server_hiagent_knowledge.versions.v3_1_0.tools.dataset import list_datasets

class Client:
    def __init__(self):
        self.calls = []
    def call(self, **kwargs):
        self.calls.append(kwargs)
        return {}

@pytest.mark.parametrize("name", [None, "", "finance"])
@pytest.mark.parametrize("page_number,page_size", [(1, 20), (2, 50)])
def test_310_request_remains_page_number_contract(name, page_number, page_size):
    client = Client()
    list_datasets(client, workspace_id="ws", name=name, page_number=page_number, page_size=page_size)
    body = {"WorkspaceID": "ws", "PageNumber": page_number, "PageSize": page_size}
    if name is not None:
        body["Filter"] = {"Name": name}
    assert client.calls == [{"action": "ListDatasets", "version": "2023-08-01", "service": "app", "body": body}]

def test_310_workspace_required():
    with pytest.raises(ValueError, match="workspace_id"):
        list_datasets(Client(), workspace_id="")
