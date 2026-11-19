import json

import httpx
import pytest

from mcp_server_sms.auth import Credentials
from mcp_server_sms.client import SmsClient

CREDENTIALS = Credentials("fixture-access-key", "fixture-secret-key", "fixture-session-token")


@pytest.mark.parametrize("action", ["GetBatchTaskDetail", "GetBatchTaskList"])
async def test_batch_queries_return_summary_without_storage_capabilities(action):
    task = {
        "taskId": "fixture-task", "subAccount": "fixture-group", "status": 2,
        "sendContent": "原文不变", "totalCount": 10, "receiptSuccessCount": 8,
        "fileUrl": "private/recipients.csv",
        "fileViewUrl": "https://fixture.invalid/recipients.csv?X-Tos-Signature=secret-capability",
        "extra": {"privateExport": "another-private-capability"},
    }
    result = task if action == "GetBatchTaskDetail" else {"list": [task], "total": 1}
    async with SmsClient(transport=httpx.MockTransport(
        lambda _: httpx.Response(200, json={"Result": result})
    )) as client:
        response = await client.call(action, {}, CREDENTIALS)
    assert response["success"]
    public = response["result"] if action == "GetBatchTaskDetail" else response["result"]["list"][0]
    assert public == {key: task[key] for key in (
        "taskId", "subAccount", "status", "sendContent", "totalCount", "receiptSuccessCount"
    )}
    assert "private" not in json.dumps(response)
    assert "secret-capability" not in json.dumps(response)
    if action == "GetBatchTaskList":
        assert response["result"]["total"] == 1


@pytest.mark.parametrize(
    "action,exception",
    [
        ("SendSmsForAgent", httpx.ReadTimeout),
        ("SendSmsForAgent", httpx.WriteTimeout),
        ("SendSmsForAgent", httpx.RemoteProtocolError),
        ("SendSmsForAgent", httpx.ConnectError),
        ("GetSubAccountListForAgent", httpx.ReadTimeout),
    ],
)
async def test_transport_failures_preserve_exception_without_guessing_or_retry(action, exception):
    calls = []

    def handler(request):
        calls.append(request)
        raise exception("connection closed while reading response", request=request)

    async with SmsClient(transport=httpx.MockTransport(handler)) as client:
        result = await client.call(action, {}, CREDENTIALS)
    assert len(calls) == 1
    assert result["success"] is False
    assert result["error"]["code"] == exception.__name__
    assert result["error"]["message"] == "connection closed while reading response"
    assert result["error"]["source"] == "transport"
    assert "outcome_unknown" not in result["error"]


@pytest.mark.parametrize(
    "status,body",
    [
        (200, b"not-json"),
        (502, b"gateway error"),
        (200, b'{"Result":{}}'),
        (200, b'{"Result":{"MessageIds":[]}}'),
        (
            200,
            b'{"ResponseMetadata":{"RequestId":"public-id","Error":{"Code":"RE:0012","Message":"private text"}}}',
        ),
    ],
)
async def test_write_response_is_not_guessed(status, body):
    async with SmsClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(status, content=body))
    ) as client:
        result = await client.call("SendSmsForAgent", {}, CREDENTIALS)
    assert result["success"] is False
    assert "outcome_unknown" not in result["error"]
    if b"ResponseMetadata" in body:
        assert result["error"]["code"] == "RE:0012"
        assert result["error"]["message"] == "private text"
        assert result["request_id"] == "public-id"


@pytest.mark.parametrize(
    "action,params",
    [("ListAllSmsProduct", {}), ("GetSubAccountListForAgent", {"SubAccountName": "示例"})],
)
async def test_official_signer_carries_sts_without_logging(action, params, capsys, caplog):
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json={"Result": {"List": [], "Total": 0}})

    async with SmsClient(transport=httpx.MockTransport(handler)) as client:
        result = await client.call(action, params, CREDENTIALS)
    assert result["success"]
    request = calls[0]
    assert request.url.host == "sms.volcengineapi.com"
    assert request.headers["x-request-source"] == "mcp"
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
        ("text/csv", b"", False),
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
        result = await client.call("TemplateUploadDemoForAgent", {}, CREDENTIALS)
    assert result["success"] is success
    if success:
        assert result["result"]["value"] == content.decode()


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
    assert "outcome_unknown" not in result["error"]


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


@pytest.mark.parametrize("status", [400, 401, 403, 404, 405, 408, 409, 413, 415, 422, 429, 499, 503])
def test_http_error_preserves_body_without_interpreting_outcome(status):
    response = httpx.Response(
        status, text="private gateway body", headers={"x-request-id": "public-id"}
    )
    result = SmsClient.decode("SendSmsForAgent", response, CREDENTIALS)
    assert not result["success"]
    assert "outcome_unknown" not in result["error"]
    assert result["error"]["code"] == f"http_{status}"
    assert result["error"]["http_status"] == status
    assert result["request_id"] == "public-id"
    assert result["error"]["message"] == "private gateway body"
    assert result["error"]["backend_response"] == "private gateway body"


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
def test_ambiguous_responses_preserve_evidence_for_the_caller(status, body):
    result = SmsClient.decode("SendSmsForAgent", httpx.Response(status, content=body), CREDENTIALS)
    assert "outcome_unknown" not in result["error"]
    assert result["error"]["http_status"] == status
    assert result["error"]["backend_response"] == (json.loads(body) if body.startswith(b"{") else body.decode())


@pytest.mark.parametrize("action", [
    "ListSignaturesForAgent", "ApplySmsTemplateV2ForAgent", "SendSmsForAgent", "GetMUploadParam",
])
@pytest.mark.parametrize("status,code", [(200, "1007"), (400, 1007), (500, "1999"), (503, "SY:0500")])
def test_all_sms_errors_pass_through_without_rewriting_or_classification(action, status, code):
    message = " 营销模板末尾必须为拒收请回复R\n且退订关键词必须在模版末尾 "
    payload = {"ResponseMetadata": {
        "RequestId": "fixture-request-id", "Action": action,
        "Error": {"Code": code, "Message": message, "Details": {"field": "content", "value": "回T退订"}},
    }}
    decoded = SmsClient.decode(action, httpx.Response(status, json=payload), CREDENTIALS)
    assert decoded["request_id"] == "fixture-request-id"
    assert decoded["error"] == {
        "code": code, "message": message, "http_status": status, "backend_response": payload,
    }


@pytest.mark.parametrize("error", [{"Code": "1007", "Message": ""}, {"Code": "1999"}, {}])
def test_missing_or_empty_error_fields_are_not_replaced(error):
    payload = {"ResponseMetadata": {"RequestId": "", "Error": error}}
    decoded = SmsClient.decode("SendSmsForAgent", httpx.Response(500, json=payload), CREDENTIALS)
    assert decoded["request_id"] == ""
    assert decoded["error"]["code"] == error.get("Code")
    assert decoded["error"]["message"] == error.get("Message")
    assert decoded["error"]["backend_response"] == payload


@pytest.mark.parametrize("action", ["ConsentBatchTask", "DeleteBatchTask"])
@pytest.mark.parametrize("include_result", [False, True])
async def test_batch_status_change_accepts_native_empty_acknowledgement(action, include_result):
    # TOP SuccessResponse(nil) 的 Result 使用 omitempty，线上成功只返回元数据。
    body = {"ResponseMetadata": {
        "RequestId": "fixture-status-request", "Action": action, "Version": "2026-01-01",
        "Service": "volcSMS", "Region": "cn-north-1",
    }}
    if include_result:
        body["Result"] = None
    calls = []

    def handler(request):
        calls.append(request)
        return httpx.Response(200, json=body)

    async with SmsClient(transport=httpx.MockTransport(handler)) as client:
        result = await client.call(action, {"subAccount": "g", "taskId": "task"}, CREDENTIALS)
    assert len(calls) == 1
    assert result["success"] is True
    assert result["result"] is None
    assert result["request_id"] == "fixture-status-request"
    assert result["error"] is None


@pytest.mark.parametrize("action", ["ConsentBatchTask", "DeleteBatchTask"])
@pytest.mark.parametrize("body", [
    {}, {"ResponseMetadata": {}}, {"ResponseMetadata": None},
    {"ResponseMetadata": {"RequestId": "fixture-status-request"}},
    {"ResponseMetadata": {"RequestId": "", "Action": "ConsentBatchTask", "Version": "2026-01-01"}},
    {"ResponseMetadata": {"RequestId": "fixture-status-request", "Action": "OtherAction", "Version": "2026-01-01"}},
    {"ResponseMetadata": {"RequestId": "fixture-status-request", "Action": "ConsentBatchTask", "Version": "invalid"}},
])
def test_batch_status_change_does_not_guess_an_empty_acknowledgement(action, body):
    result = SmsClient.decode(action, httpx.Response(200, json=body), CREDENTIALS)
    assert result["success"] is False
    assert result["error"]["code"] == "invalid_response"
    assert result["error"]["http_status"] == 200
    assert result["error"]["backend_response"] == body


@pytest.mark.parametrize("action", ["SetBatchTaskForAgent", "SendSmsForAgent", "GetBatchTaskDetail"])
def test_metadata_only_response_is_not_accepted_for_actions_requiring_results(action):
    body = {"ResponseMetadata": {
        "RequestId": "fixture-request", "Action": action, "Version": "2026-01-01",
    }}
    result = SmsClient.decode(action, httpx.Response(200, json=body), CREDENTIALS)
    assert result["success"] is False
    assert result["error"]["code"] == "invalid_response"


@pytest.mark.parametrize("action", ["ConsentBatchTask", "DeleteBatchTask"])
@pytest.mark.parametrize("status", [200, 400, 503])
def test_batch_status_change_preserves_native_business_errors(action, status):
    body = {"ResponseMetadata": {
        "RequestId": "fixture-status-request", "Action": action, "Version": "2026-01-01",
        "Error": {"Code": "1999", "Message": "Invalid operation to the record"},
    }}
    result = SmsClient.decode(action, httpx.Response(status, json=body), CREDENTIALS)
    assert result["success"] is False
    assert result["request_id"] == "fixture-status-request"
    assert result["error"] == {
        "code": "1999", "message": "Invalid operation to the record",
        "http_status": status, "backend_response": body,
    }


@pytest.mark.parametrize("action", ["ConsentBatchTask", "DeleteBatchTask"])
@pytest.mark.parametrize("result", [{}, "", True, 0, []])
def test_batch_status_change_rejects_unexpected_result(action, result):
    body = {"ResponseMetadata": {
        "RequestId": "fixture-status-request", "Action": action, "Version": "2026-01-01",
    }, "Result": result}
    decoded = SmsClient.decode(action, httpx.Response(200, json=body), CREDENTIALS)
    assert decoded["success"] is False
    assert decoded["error"]["code"] == "invalid_response"
    assert decoded["error"]["backend_response"] == body


@pytest.mark.parametrize("action", ["ConsentBatchTask", "DeleteBatchTask"])
@pytest.mark.parametrize("error", ["invalid error", False, []])
def test_batch_status_change_does_not_ignore_malformed_error(action, error):
    body = {"ResponseMetadata": {
        "RequestId": "fixture-status-request", "Action": action, "Version": "2026-01-01",
        "Error": error,
    }, "Result": None}
    decoded = SmsClient.decode(action, httpx.Response(200, json=body), CREDENTIALS)
    assert decoded["success"] is False
    assert decoded["error"]["code"] == "invalid_response"
