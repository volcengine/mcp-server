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

    async with SmsClient(transport=httpx.MockTransport(handler)) as client:
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
    async with SmsClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(status, content=body))
    ) as client:
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

    async with SmsClient(transport=httpx.MockTransport(handler)) as client:
        result = await client.call(
            "ListSubAccountForAgent", {"SubAccountName": "示例"}, CREDENTIALS
        )
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
    async with SmsClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(
                200,
                content=content,
                headers={"content-type": content_type},
            )
        )
    ) as client:
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
    async with SmsClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"Result": value}))
    ) as client:
        result = await client.call("ListSecondTemplate", {}, CREDENTIALS)
    assert result["result"] == {
        key: value[key] for key in ("Content", "ticket", "url", "status")
    } | {"nested": {}}


async def test_redirects_are_not_followed():
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(302, headers={"location": "https://untrusted.example/"})

    async with SmsClient(transport=httpx.MockTransport(handler)) as client:
        result = await client.call("SendSmsForAgent", {}, CREDENTIALS)
    assert len(calls) == 1
    assert result["error"]["outcome_unknown"]


async def test_incomplete_upload_authorization_is_not_reported_as_success():
    async with SmsClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={"Result": {"file": "fixture.csv"}})
        )
    ) as client:
        result = await client.call("GetUploadTosURL", {"suffix": "csv"}, CREDENTIALS)
    assert result["success"] is False


def test_upload_url_preserves_signed_query_without_disabling_other_redaction():
    url = (
        "https://upload.example/input.csv?X-Tos-Algorithm=TOS4-HMAC-SHA256"
        "&X-Tos-Credential=fixture-access-key%2F20260917%2Fcn-beijing%2Ftos%2Frequest"
        "&X-Tos-Security-Token=fixture-session-token&X-Tos-Signature=fixture-signature"
    )
    response = httpx.Response(
        200,
        json={
            "Result": {
                "file": "input.csv",
                "url": url,
                "debug": {"url": url, "SecretAccessKey": CREDENTIALS.secret_key},
                "message": CREDENTIALS.secret_key,
            }
        },
    )
    result = SmsClient.decode("GetUploadTosURL", response, CREDENTIALS)
    assert result["success"]
    assert result["result"]["url"] == url
    assert result["result"]["message"] == "[REDACTED]"
    assert "SecretAccessKey" not in result["result"]["debug"]
    assert CREDENTIALS.access_key not in result["result"]["debug"]["url"]
    ordinary = SmsClient.decode("ListSecondTemplate", response, CREDENTIALS)
    assert CREDENTIALS.access_key not in ordinary["result"]["url"]


@pytest.mark.parametrize("status", [400, 401, 403, 404, 405, 413, 415, 422, 429])
def test_plain_client_rejection_is_definite_and_retains_http_status(status):
    response = httpx.Response(
        status, text="private gateway body", headers={"x-request-id": "public-id"}
    )
    result = SmsClient.decode("SendSmsForAgent", response, CREDENTIALS)
    assert not result["success"]
    assert result["error"]["outcome_unknown"] is False
    assert result["error"]["code"] == f"http_{status}"
    assert result["error"]["http_status"] == status
    assert result["request_id"] == "public-id"
    assert "private gateway body" not in json.dumps(result)


@pytest.mark.parametrize(
    "status,body",
    [
        (408, b"timeout"),
        (409, b"conflict"),
        (499, b"gateway-specific"),
        (503, b"unavailable"),
        (200, b"broken JSON"),
        (200, b'{"Result":{}}'),
    ],
)
def test_ambiguous_responses_keep_unknown_outcome(status, body):
    result = SmsClient.decode("SendSmsForAgent", httpx.Response(status, content=body), CREDENTIALS)
    assert result["error"]["outcome_unknown"] is True
    assert result["error"]["http_status"] == status
