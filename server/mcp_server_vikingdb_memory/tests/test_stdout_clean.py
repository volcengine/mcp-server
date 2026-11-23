import importlib

import pytest
from mcp_server_vikingdb_memory.common.memory_client import VikingDBMemoryService


@pytest.fixture
def server(monkeypatch):
    # The service pings the API on construction; keep the test offline.
    monkeypatch.setattr(VikingDBMemoryService, "get_body", lambda *a, **k: {}, raising=False)
    monkeypatch.setenv("VOLCENGINE_ACCESS_KEY", "ak")
    monkeypatch.setenv("VOLCENGINE_SECRET_KEY", "sk")
    module = importlib.import_module("mcp_server_vikingdb_memory.server")
    return importlib.reload(module)


def test_tools_do_not_write_to_stdout(server, capsys, monkeypatch):
    """With the stdio transport, stdout carries the JSON-RPC stream."""
    ok = {"code": 0, "data": {"result_list": []}, "request_id": "r"}
    monkeypatch.setattr(server.vm, "add_messages", lambda **k: ok)
    monkeypatch.setattr(server.vm, "search_memory", lambda **k: ok)
    server.add_memories("hello")
    server.search_memory("hello")

    def boom(**k):
        raise RuntimeError("boom")

    monkeypatch.setattr(server.vm, "add_messages", boom)
    monkeypatch.setattr(server.vm, "search_memory", boom)
    server.add_memories("hello")
    server.search_memory("hello")
    assert capsys.readouterr().out == ""
