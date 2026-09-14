from starlette.testclient import TestClient
from mcp_server_sms.server import build_server
from mcp_server_sms.web import create_app


def rpc(client, method, arguments=None):
    params = {
        "_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientInfo": {
                "name": "sms-tests",
                "version": "1.0",
            },
            "io.modelcontextprotocol/clientCapabilities": {},
        }
    }
    if arguments:
        params.update(arguments)
    return client.post(
        "/mcp",
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params},
        headers={
            "Authorization": "Bearer fixture-token",
            "Accept": "application/json, text/event-stream",
            "MCP-Protocol-Version": "2026-07-28",
            "MCP-Method": method,
            **(
                {"Mcp-Name": arguments["name"]}
                if arguments and "name" in arguments
                else {}
            ),
        },
    )


def test_0728_discovery_and_tools_without_initialize_or_session(
    runtime, owner, monkeypatch
):
    monkeypatch.setattr(runtime.auth, "owner", lambda headers: owner)
    app = create_app(runtime, build_server(runtime))
    with TestClient(app, base_url="https://testserver") as client:
        for method in ["server/discover", "tools/list"]:
            response = rpc(client, method)
            assert response.status_code == 200, response.text
            assert "error" not in response.json(), response.text
            assert "mcp-session-id" not in response.headers
        tools = response.json()["result"]["tools"]
        names = {tool["name"] for tool in tools}
        assert "create_qualification_draft" in names
        assert "prepare_qualification_application" in names
        assert "open_qualification_application" not in names
        assert "open_batch_file_upload" not in names
        assert "prepare_batch_task" in names
        assert not any(
            "public_resource" in name or "notification" in name for name in names
        )
        for tool in tools:
            assert "ctx" not in tool["inputSchema"].get("properties", {})


def test_mcp_requires_verified_token(runtime):
    with TestClient(
        create_app(runtime, build_server(runtime)), base_url="https://testserver"
    ) as client:
        response = client.post("/mcp", json={})
        assert response.status_code == 401
        assert "resource_metadata" in response.headers["www-authenticate"]
        assert (
            client.get("/.well-known/oauth-protected-resource/mcp").json()["resource"]
            == "https://testserver/mcp"
        )


async def test_tool_results_have_usable_structured_content(
    runtime, owner, credentials, sms, monkeypatch
):
    monkeypatch.setattr(runtime, "caller", lambda ctx: (owner, credentials))
    server = build_server(runtime)
    result = await server.call_tool("list_message_groups", {})
    assert result.is_error is False
    assert result.structured_content["success"] is True
    assert result.structured_content["result"]["List"][0]["SubAccount"] == "group-one"
    assert all(tool.output_schema is not None for tool in await server.list_tools())


def test_http_tools_cannot_import_local_files(runtime, owner, monkeypatch, tmp_path):
    (tmp_path / "private.json").write_text('{"private":"customer-data"}')
    monkeypatch.setattr(runtime.auth, "owner", lambda headers: owner)
    with TestClient(
        create_app(runtime, build_server(runtime)), base_url="https://testserver"
    ) as client:
        response = rpc(
            client,
            "tools/call",
            {
                "name": "import_input_file",
                "arguments": {
                    "relative_path": "private.json",
                    "kind": "qualification_data",
                    "content_type": "application/json",
                },
            },
        )
        assert response.status_code == 200, response.text
        assert response.json()["result"]["isError"] is True
        assert "customer-data" not in response.text
