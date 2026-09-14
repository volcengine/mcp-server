import json

import pytest
from starlette.testclient import TestClient

from mcp_server_sms.auth import AuthenticationError
from mcp_server_sms.store import StoreError
from mcp_server_sms.server import build_server
from mcp_server_sms.web import create_app


def test_local_files_are_confined_and_do_not_overwrite(runtime, owner, tmp_path):
    inside = tmp_path / "private.json"
    inside.write_text('{"personName":"私密姓名"}')
    staged = runtime.inputs.import_local(
        "private.json", "qualification_data", "application/json", owner
    )
    assert "私密姓名" not in json.dumps(staged, ensure_ascii=False)
    with pytest.raises(StoreError):
        runtime.inputs.read(staged["fileId"], "someone-else")
    with pytest.raises(StoreError):
        runtime.inputs.read(staged["fileId"], owner, "batch_csv")
    with pytest.raises(StoreError):
        runtime.inputs.import_local(
            "../outside.json", "qualification_data", "application/json", owner
        )
    with pytest.raises(StoreError):
        runtime.inputs.import_local(
            str(inside), "qualification_data", "application/json", owner
        )
    (tmp_path / "link.json").symlink_to(inside)
    with pytest.raises(StoreError):
        runtime.inputs.import_local(
            "link.json", "qualification_data", "application/json", owner
        )
    (tmp_path / "linked-dir").symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(StoreError):
        runtime.inputs.import_local(
            "linked-dir/private.json", "qualification_data", "application/json", owner
        )
    with pytest.raises(StoreError):
        runtime.inputs.export_local(staged["fileId"], "private.json", owner)
    runtime.inputs.export_local(staged["fileId"], "review.json", owner)
    assert (tmp_path / "review.json").read_bytes() == inside.read_bytes()
    assert (tmp_path / "review.json").stat().st_mode & 0o777 == 0o600


def test_http_file_exchange_requires_same_owner_and_has_no_web_session(
    runtime, owner, monkeypatch
):
    def authorize(headers):
        token = headers.get("authorization")
        if token == "Bearer fixture-one":
            return owner
        if token == "Bearer fixture-two":
            return "another-owner"
        raise AuthenticationError("missing token")

    monkeypatch.setattr(runtime.auth, "owner", authorize)
    with TestClient(
        create_app(runtime, build_server(runtime)), base_url="https://testserver"
    ) as client:
        assert (
            client.post("/files?kind=qualification_data", content=b"{}").status_code
            == 401
        )
        response = client.post(
            "/files?kind=qualification_data",
            content=b'{"personName":"private-name"}',
            headers={
                "Authorization": "Bearer fixture-one",
                "Content-Type": "application/json",
            },
        )
        assert response.status_code == 201
        assert "private-name" not in response.text
        file_id = response.json()["fileId"]
        assert client.get("/files/" + file_id).status_code == 401
        assert (
            client.get(
                "/files/" + file_id, headers={"Authorization": "Bearer fixture-two"}
            ).status_code
            == 409
        )
        response = client.get(
            "/files/" + file_id, headers={"Authorization": "Bearer fixture-one"}
        )
        assert response.json() == {"personName": "private-name"}
        assert response.headers["cache-control"] == "no-store"
        assert "set-cookie" not in response.headers
        assert client.get("/auth/login/anything").status_code == 404
        assert client.get("/forms/anything").status_code == 404
        assert (
            client.get("/qualification-static/qualification_wizard.js").status_code
            == 404
        )
        too_large = client.post(
            "/files?kind=verification_code",
            content=b"x" * 1025,
            headers={"Authorization": "Bearer fixture-one"},
        )
        assert too_large.status_code == 413


def test_invalid_payloads_never_become_inputs(runtime, owner):
    for kind, data in [
        ("verification_code", b'{"code":"12345"}'),
        ("verification_code", b'{"code":1234}'),
        ("qualification_data", b"[]"),
        ("batch_csv", b"\xff"),
    ]:
        with pytest.raises(StoreError):
            runtime.inputs.stage(owner, kind, data, "application/json")
