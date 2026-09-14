import pytest
from conftest import auth_header, rpc
from starlette.testclient import TestClient

from mcp_server_sms.auth import AuthenticationError, Credentials
from mcp_server_sms.server import build_server, create_http_app


def test_stateless_discovery_needs_no_database_or_initialize(api_calls, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    app = create_http_app(build_server(api_calls[1]), "https://testserver")
    with TestClient(app, base_url="https://testserver") as client:
        for method in ("server/discover", "tools/list"):
            response = rpc(client, method, token=auth_header("a"))
            assert response.status_code == 200, response.text
            assert "error" not in response.json()
            assert "mcp-session-id" not in response.headers
            assert response.headers["cache-control"] == "no-store"
        assert len(response.json()["result"]["tools"]) == 26
    assert list(tmp_path.iterdir()) == []
    assert api_calls[0] == []


def test_http_credentials_are_per_request_without_environment_fallback(api_calls, credentials_env):
    app = create_http_app(build_server(api_calls[1]), "https://testserver")
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


def test_http_has_no_file_routes_and_rejects_untrusted_host(api_calls):
    app = create_http_app(build_server(api_calls[1]), "https://testserver")
    with TestClient(app, base_url="https://testserver") as client:
        response = client.post(
            "/files", content=b"private", headers={"authorization": auth_header("a")}
        )
        assert response.status_code == 404
        response = client.post(
            "/mcp", headers={"authorization": auth_header("a"), "host": "evil.example"}, json={}
        )
        assert response.status_code == 421
    assert api_calls[0] == []
