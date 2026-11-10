import sys
from unittest.mock import Mock

import httpx
import pytest
from conftest import auth_header, rpc
from starlette.testclient import TestClient

from mcp_server_sms.auth import AuthenticationError, Credentials
from mcp_server_sms.client import SmsClient
from mcp_server_sms.server import build_server, create_http_app, main


def test_stateless_discovery_needs_no_database_or_initialize(api_calls, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    app = create_http_app(build_server(api_calls[1]), host="0.0.0.0")
    with TestClient(app, base_url="https://testserver") as client:
        for method in ("server/discover", "tools/list"):
            response = rpc(client, method, token=auth_header("a"))
            assert response.status_code == 200, response.text
            assert "error" not in response.json()
            assert "mcp-session-id" not in response.headers
            assert response.headers["cache-control"] == "no-store"
        assert len(response.json()["result"]["tools"]) == 30
    assert list(tmp_path.iterdir()) == []
    assert api_calls[0] == []


@pytest.mark.parametrize("version", ["2025-03-26", "2025-06-18", "2025-11-25"])
def test_standard_http_initialize_and_tool_call_for_earlier_clients(api_calls, version):
    app = create_http_app(build_server(api_calls[1]), host="0.0.0.0")
    headers = {"Accept": "application/json, text/event-stream", "Authorization": auth_header("a")}
    with TestClient(app, base_url="https://testserver", headers=headers) as client:
        initialized = client.post("/mcp", json={
            "jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": version, "capabilities": {},
                "clientInfo": {"name": "standard-client", "version": "1"},
            },
        })
        assert initialized.status_code == 200, initialized.text
        assert initialized.json()["result"]["protocolVersion"] == version
        headers = {"MCP-Protocol-Version": version}
        listed = client.post("/mcp", headers=headers, json={
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {},
        })
        assert len(listed.json()["result"]["tools"]) == 30
        called = client.post("/mcp", headers=headers, json={
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "list_message_groups", "arguments": {}},
        })
        assert called.json()["result"]["isError"] is False
    assert len(api_calls[0]) == 1


def test_http_credentials_are_per_request_without_environment_fallback(api_calls, credentials_env):
    app = create_http_app(build_server(api_calls[1]), host="0.0.0.0")
    with TestClient(app, base_url="https://testserver") as client:
        assert rpc(client, "tools/list").status_code == 401
        for suffix in ("a", "b"):
            response = rpc(
                client,
                "tools/call",
                token=auth_header(suffix),
                params={"name": "list_message_groups", "arguments": {}},
            )
            assert response.status_code == 200, response.text
            assert response.json()["result"]["isError"] is False
    assert len(api_calls[0]) == 2
    for suffix, request in zip(("a", "b"), api_calls[0], strict=True):
        assert "Credential=fixture-access-key-" + suffix + "/" in request.headers["authorization"]
        assert request.headers["x-security-token"] == "fixture-token-" + suffix
    with pytest.raises(AuthenticationError):
        Credentials.from_headers({})


@pytest.mark.parametrize(
    "value", ["", "Bearer not-base64", "Bearer W10=", "Basic abc", "Bearer " + "a" * 20000]
)
def test_bad_http_auth_is_rejected_without_exposing_input(value, credentials_env):
    with pytest.raises(AuthenticationError) as caught:
        Credentials.from_headers({"authorization": value})
    assert "not-base64" not in str(caught.value)
    assert "fixture-secret" not in str(caught.value)


def test_loopback_http_has_no_file_routes_and_rejects_untrusted_host(api_calls):
    app = create_http_app(build_server(api_calls[1]))
    with TestClient(app, base_url="http://127.0.0.1:8000") as client:
        response = client.post(
            "/files", content=b"private", headers={"authorization": auth_header("a")}
        )
        assert response.status_code == 404
        response = client.post(
            "/mcp", headers={"authorization": auth_header("a"), "host": "evil.example"}, json={}
        )
        assert response.status_code == 421
    assert api_calls[0] == []


def test_http_client_lives_until_mcp_shutdown_and_keeps_callers_isolated():
    class CountingTransport(httpx.AsyncBaseTransport):
        def __init__(self):
            self.requests = []
            self.close_count = 0

        async def handle_async_request(self, request):
            self.requests.append(request)
            return httpx.Response(
                200,
                json={"Result": {"List": [], "Total": 0}},
                headers={"set-cookie": "identity=caller-a; Path=/; Secure"},
            )

        async def aclose(self):
            self.close_count += 1

    transport = CountingTransport()
    app = create_http_app(build_server(SmsClient(transport=transport)), host="0.0.0.0")
    with TestClient(app, base_url="https://testserver") as client:
        for caller in ("a", "b"):
            response = rpc(
                client,
                "tools/call",
                token=auth_header(caller),
                params={"name": "list_message_groups", "arguments": {}},
            )
            assert response.status_code == 200
            assert response.json()["result"]["isError"] is False
        assert transport.close_count == 0
        for caller, request in zip(("a", "b"), transport.requests, strict=True):
            assert f"Credential=fixture-access-key-{caller}/" in request.headers["authorization"]
            assert request.headers["x-security-token"] == f"fixture-token-{caller}"
            assert "cookie" not in request.headers
    assert transport.close_count == 1


def test_remote_cli_serves_ats_tools_with_sdk_default_security(api_calls, monkeypatch):
    public_url = "https://sms.mcp.volcbiz.com"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp-server-sms",
            "--transport",
            "streamable-http",
            "--host",
            "0.0.0.0",
            "--public-url",
            public_url,
        ],
    )
    monkeypatch.setattr("mcp_server_sms.server.build_server", lambda: build_server(api_calls[1]))
    run = Mock()
    monkeypatch.setattr("uvicorn.run", run)

    main()

    run.assert_called_once()
    app = run.call_args.args[0]
    with TestClient(app, base_url=public_url) as client:
        response = client.post(
            "/mcp",
            headers={
                "authorization": auth_header("a"),
                "accept": "application/json, text/event-stream",
                "origin": "https://www.volcengine.com",
            },
            json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
        )
        assert response.status_code == 200, response.text
        assert len(response.json()["result"]["tools"]) == 30
    assert api_calls[0] == []
