import json

import httpx
import pytest

from mcp_server_sms.auth import Credentials
from mcp_server_sms.client import SmsClient

CREDENTIALS = Credentials("fixture-access-key", "fixture-secret-key", "fixture-session-token")


@pytest.mark.parametrize(
    "action,exception,unknown",
    [
        ("SendSmsForAgent", httpx.ReadTimeout, True),
        ("SendSmsForAgent", httpx.WriteTimeout, True),
        ("SendSmsForAgent", httpx.RemoteProtocolError, True),
        ("SendSmsForAgent", httpx.ConnectError, False),
        ("ListSubAccountForAgent", httpx.ReadTimeout, False),
    ],
)
async def test_transport_failures_never_retry(action, exception, unknown):
    calls = []

    def handler(request):
        calls.append(request)
        raise exception("secret diagnostic must not leak", request=request)

    client = SmsClient(transport=httpx.MockTransport(handler))
    result = await client.call(action, {}, CREDENTIALS)
    assert len(calls) == 1
    assert result["success"] is False
    assert result["error"]["outcome_unknown"] is unknown
    assert "secret diagnostic" not in json.dumps(result)


@pytest.mark.parametrize(
    "status,body,unknown",
    [
        (200, b"not-json", True),
        (502, b"gateway error", True),
        (200, b'{"Result":{}}', True),
        (200, b'{"Result":{"MessageIds":[]}}', True),
        (
            200,
            b'{"ResponseMetadata":{"RequestId":"public-id","Error":{"Code":"RE:0012","Message":"private text"}}}',
            False,
        ),
    ],
)
async def test_write_response_is_not_guessed(status, body, unknown):
    client = SmsClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(status, content=body))
    )
    result = await client.call("SendSmsForAgent", {}, CREDENTIALS)
    assert result["success"] is False
    assert result["error"]["outcome_unknown"] is unknown
    assert "private text" not in json.dumps(result)
    if not unknown:
        assert result["error"]["code"] == "RE:0012"
        assert result["request_id"] == "public-id"


async def test_official_signer_carries_sts_without_logging(capsys, caplog):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json={"Result": {"List": [], "Total": 0}})

    client = SmsClient(transport=httpx.MockTransport(handler))
    result = await client.call("ListSubAccountForAgent", {"SubAccountName": "示例"}, CREDENTIALS)
    assert result["success"]
    request = calls[0]
    assert request.url.host == "sms.volcengineapi.com"
    assert "Credential=fixture-access-key/" in request.headers["authorization"]
    assert "/cn-north-1/volcSMS/request" in request.headers["authorization"]
    assert request.headers["x-security-token"] == CREDENTIALS.session_token
    assert request.headers["x-content-sha256"]
    captured = capsys.readouterr()
    assert CREDENTIALS.secret_key not in captured.out + captured.err + caplog.text


@pytest.mark.parametrize(
    "content_type,content,success",
    [
        ("text/csv", "phone,name\n13800000000,示例\n".encode(), True),
        ("application/octet-stream", b"phone,name\n", True),
        ("text/html", b"<html>gateway login</html>", False),
        ("text/csv", b"\xff", False),
    ],
)
async def test_csv_response_contract(content_type, content, success):
    client = SmsClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                content=content,
                headers={"content-type": content_type},
            )
        )
    )
    result = await client.call("TemplateUploadDemo", {}, CREDENTIALS)
    assert result["success"] is success
    if success:
        assert result["result"]["content"] == content.decode()


async def test_business_values_and_upstream_references_are_preserved():
    value = {
        "Content": " 原始正文13800000000 ",
        "ticket": "upstream-ticket",
        "url": "https://upload.example/a?signature=opaque",
        "status": 0,
        "AccessKeyId": "private",
        "nested": {"SecretAccessKey": "private"},
    }
    client = SmsClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"Result": value}))
    )
    result = await client.call("ListSecondTemplate", {}, CREDENTIALS)
    assert result["result"] == {
        key: value[key] for key in ("Content", "ticket", "url", "status")
    } | {"nested": {}}


async def test_redirects_are_not_followed():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(302, headers={"location": "https://untrusted.example/"})

    result = await SmsClient(transport=httpx.MockTransport(handler)).call(
        "SendSmsForAgent", {}, CREDENTIALS
    )
    assert len(calls) == 1
    assert result["error"]["outcome_unknown"]


async def test_incomplete_upload_authorization_is_not_reported_as_success():
    client = SmsClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={"Result": {"file": "fixture.csv"}})
        )
    )
    result = await client.call("GetUploadTosURL", {"suffix": "csv"}, CREDENTIALS)
    assert result["success"] is False
