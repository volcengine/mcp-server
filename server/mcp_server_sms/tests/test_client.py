import datetime
import json

from mcp_server_sms.core.api_client import SmsApiClient
from mcp_server_sms.core.api_protocol import (
    TransportResponse,
    ResponseLostError,
    build_signed_request,
)
from mcp_server_sms.core.action_contracts import ACTION_REGISTRY


def test_v4_signing_carries_action_version_and_sts(credentials):
    request = build_signed_request(
        ACTION_REGISTRY["ListSubAccountForAgent"],
        {},
        credentials.access_key,
        credentials.secret_key,
        datetime.datetime(2026, 9, 11, tzinfo=datetime.timezone.utc),
        action="ListSubAccountForAgent",
        session_token=credentials.session_token,
    )
    assert "Action=ListSubAccountForAgent" in request.url
    assert "Version=2026-01-01" in request.url
    assert request.headers["X-Security-Token"] == credentials.session_token
    assert "x-security-token" in request.authorization
    assert "cn-north-1/volcSMS/request" in request.authorization


def test_mutation_response_lost_and_invalid_response_are_unknown(credentials):
    calls = []

    def lost(request, timeout):
        calls.append(1)
        raise ResponseLostError("fixture failure")

    client = SmsApiClient(credentials, transport=lost)
    assert client.call("SendSmsForAgent", {})["error"]["outcome_unknown"] is True
    assert calls == [1]
    client = SmsApiClient(
        credentials, transport=lambda *args: TransportResponse(200, {}, b"not-json")
    )
    assert client.call("SendSmsForAgent", {})["error"]["outcome_unknown"] is True


def test_template_response_and_private_qualification_fields(credentials):
    result = {
        "List": [
            {
                "TemplateId": "template-one",
                "ShortUrlConfig": {"isEnabled": "0", "unexpected": "private"},
            }
        ]
    }
    client = SmsApiClient(
        credentials,
        transport=lambda *args: TransportResponse(
            200, {}, json.dumps({"Result": result}).encode()
        ),
    )
    response = client.call("ListSmsTemplateForAgent", {})
    assert response["success"]
    assert response["result"]["List"][0]["ShortUrlConfig"] == {"isEnabled": "0"}
    result = {"status": "1", "ticket": "fixture-private-ticket"}
    assert (
        client.call("ThreeElementPersonCheckForAgent", {})["result"]["ticket"]
        == "fixture-private-ticket"
    )


def test_business_error_in_http_200_is_failure(credentials):
    client = SmsApiClient(
        credentials,
        transport=lambda *args: TransportResponse(
            200,
            {},
            json.dumps(
                {
                    "ResponseMetadata": {
                        "RequestId": "fixture",
                        "Error": {"Code": "RE:0001"},
                    }
                }
            ).encode(),
        ),
    )
    result = client.call("ListSubAccountForAgent", {})
    assert not result["success"]
    assert result["error"]["code"] == "RE:0001"
    assert result["request_id"] == "fixture"


def test_unstructured_server_error_on_mutation_is_unknown(credentials):
    client = SmsApiClient(
        credentials, transport=lambda *args: TransportResponse(503, {}, b"{}")
    )
    assert client.call("SendSmsForAgent", {})["error"]["outcome_unknown"]


def test_identifier_and_hash_values_are_not_phone_masked(credentials):
    from mcp_server_sms.core.api_protocol import sanitize_output

    identifier = "aa13812345678bb"
    value = sanitize_output(
        {
            "operationId": identifier,
            "digest": identifier,
            "SubAccounts": [identifier],
            "mobile": "13812345678",
        }
    )
    assert value["operationId"] == identifier
    assert value["digest"] == identifier
    assert value["SubAccounts"] == [identifier]
    assert value["mobile"] == "138****5678"
    result = {
        "List": [{"SubAccount": identifier, "SubAccountName": "fixture", "Status": 1}]
    }
    client = SmsApiClient(
        credentials,
        transport=lambda *args: TransportResponse(
            200, {}, json.dumps({"Result": result}).encode()
        ),
    )
    assert (
        client.call("ListSubAccountForAgent", {})["result"]["List"][0]["SubAccount"]
        == identifier
    )


def test_authorized_upload_url_is_not_rewritten(credentials):
    url = "https://upload.example/path?signature=aa13812345678bb"
    client = SmsApiClient(
        credentials,
        transport=lambda *args: TransportResponse(
            200,
            {},
            json.dumps({"Result": {"url": url, "file": "fixture-file"}}).encode(),
        ),
    )
    assert (
        client.call("GetUploadTosURL", {}, preserve_presigned_url=True)["result"]["url"]
        == url
    )
