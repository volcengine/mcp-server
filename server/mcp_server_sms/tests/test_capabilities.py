import base64
import json
import logging
import subprocess
import sys
import textwrap
from contextlib import contextmanager

import httpx
import jsonref
import pytest
from conftest import auth_header, payload, rpc
from jsonschema import Draft202012Validator
from starlette.testclient import TestClient

from mcp_server_sms import observability
from mcp_server_sms.auth import Credentials
from mcp_server_sms.client import SmsClient
from mcp_server_sms.protocol import inline_schema
from mcp_server_sms.server import build_server, create_http_app


@pytest.mark.parametrize(
    "action,params,method",
    [
        (
            "GetSubAccountListForAgent",
            {
                "pageIndex": 2,
                "pageSize": 50,
                "allStatus": True,
                "subAccount": "group",
                "project": "project",
            },
            "POST",
        ),
        (
            "ListSignaturesForAgent",
            {
                "Signature": "完整签名",
                "ExactMatch": True,
                "SubAccounts": ["group"],
                "ChannelTypes": ["CN_NTC"],
                "Industries": ["industry"],
                "Statuses": [3],
                "Page": 1,
                "PageSize": 20,
            },
            "POST",
        ),
        (
            "ListBatchTemplatesForAgent",
            {"TemplateId": "special", "Page": 1, "PageSize": 20},
            "POST",
        ),
        (
            "GetTobTrafficDrivingLinkListForAgent",
            {"link": "https://example.com/a?q=One", "useVolcLink": False},
            "GET",
        ),
        ("GetTobTrafficDrivingPhoneListForAgent", {"id": 12, "number": "4001234567"}, "GET"),
        ("ListRelationTemplateForAgent", {"signature": "示例", "number": "4001234567"}, "GET"),
        (
            "CheckTrafficDrivingExist",
            {"content": " 查询 https://example.com/a?q=One ", "useVolcLink": True},
            "GET",
        ),
        (
            "ListThirdTemplate",
            {"secondTemplateId": "42", "phoneId": 12, "linkId": 13, "subContentId": 14},
            "GET",
        ),
        (
            "AgentGetSignatureTemplateReportStatus",
            {
                "Signature": "示例",
                "ChannelType": "CN_NTC",
                "Industry": "industry",
                "SubAccount": "group",
                "TemplateId": "template",
                "Carrier": "中国移动",
            },
            "GET",
        ),
        (
            "ValidateBatchTaskContentForAgent",
            {
                "subAccount": "group",
                "signature": "示例",
                "templateId": "special",
                "content": " 原始特殊通知 ",
            },
            "POST",
        ),
    ],
)
async def test_supplemental_query_contracts(mcp, api_calls, action, params, method):
    arguments = {"request": {"action": action, "params": params}}
    result = await mcp.call_tool("query_sms_resources", arguments)
    assert not result.is_error
    request = api_calls[0][-1]
    assert request.method == method
    assert request.url.params["Action"] == action
    if method == "POST":
        assert json.loads(request.content) == params
    else:
        assert request.content == b""
        assert dict(request.url.params) == {
            "Action": action,
            "Version": "2026-01-01",
            **{
                key: str(value).lower() if isinstance(value, bool) else str(value)
                for key, value in params.items()
            },
        }
    tool = next(t for t in await mcp.list_tools() if t.name == "query_sms_resources")
    Draft202012Validator(tool.input_schema).validate(arguments)


async def test_service_confirmation_and_activation_are_separate(mcp, api_calls):
    first = {"action": "ConfirmProtocolDocument", "params": {"product": "sms", "documents": [1, 2]}}
    result = await mcp.call_tool("manage_sms_service", {"request": first})
    assert payload(result)["result"] == {"success": [1, 2], "fail": []}
    assert len(api_calls[0]) == 1
    assert json.loads(api_calls[0][0].content) == first["params"]
    result = await mcp.call_tool(
        "manage_sms_service",
        {"request": {"action": "ActivateSmsProductInOneStep", "params": {"product": ["sms"]}}},
    )
    assert not result.is_error
    assert len(api_calls[0]) == 2
    assert api_calls[0][-1].url.params["Action"] == "ActivateSmsProductInOneStep"


async def test_rejected_batch_content_stays_a_business_result(mcp):
    result = await mcp.call_tool(
        "query_sms_resources",
        {
            "request": {
                "action": "ValidateBatchTaskContentForAgent",
                "params": {"subAccount": "group", "signature": "示例", "templateId": "special"},
            }
        },
    )
    assert not result.is_error
    assert payload(result)["result"] == {"Approved": False, "Reason": "请补充任务正文"}


@pytest.mark.parametrize(
    "action,data",
    [
        (
            "BulkCreateTobTrafficDrivingLinkForAgent",
            [
                {
                    "useVolcLink": False,
                    "protocol": "https",
                    "link": "https://example.com/Path?Q=One",
                    "linkDomainIcp": "示例备案",
                    "linkDomainIcpBody": "示例企业",
                }
            ],
        ),
        (
            "BulkCreateTobTrafficDrivingPhoneForAgent",
            [
                {
                    "numberType": 1,
                    "number": "13800000000",
                    "numberPerson": "示例人员",
                    "personType": 1,
                    "personId": "fixture-private-document",
                }
            ],
        ),
    ],
)
async def test_traffic_registration_preserves_confirmed_data(mcp, api_calls, action, data):
    result = await mcp.call_tool(
        "register_traffic_resource", {"request": {"action": action, "params": {"data": data}}}
    )
    assert not result.is_error
    assert len(api_calls[0]) == 1
    assert json.loads(api_calls[0][0].content) == {"data": data}


async def test_invalid_query_action_and_private_validation_do_not_leak(mcp, api_calls):
    secret = "fixture-private-value-do-not-return"
    result = await mcp.call_tool(
        "query_sms_resources",
        {"request": {"action": "SendSmsForAgent", "params": {"AccountId": secret}}},
    )
    assert result.is_error
    assert secret not in result.model_dump_json()
    result = await mcp.call_tool(
        "register_traffic_resource",
        {
            "request": {
                "action": "BulkCreateTobTrafficDrivingPhoneForAgent",
                "params": {"data": [{"numberType": 2, "number": "4001234567", "personId": secret}]},
            }
        },
    )
    assert result.is_error
    assert secret not in result.model_dump_json()
    assert api_calls[0] == []


async def test_statistics_use_native_v4_array_filters_and_groups(mcp, api_calls):
    result = await mcp.call_tool(
        "get_send_statistics",
        {
            "start_time": 100,
            "end_time": 200,
            "sub_account": "group",
            "project": "project",
            "channel_type": ["CN_NTC", "CN_MKT"],
            "signature": "示例签名",
            "template_id": ["template"],
            "standard_error_codes": ["RE:0214"],
            "not_split": True,
            "date_group": 1,
            "standard_error_code_group": 1,
        },
    )
    assert not result.is_error
    request = api_calls[0][-1]
    assert request.url.params["Action"] == "GetTotalSendCountStatV4ForAgent"
    assert json.loads(request.content) == {
        "StartTime": 100,
        "EndTime": 200,
        "SmsAccount": "group",
        "Project": "project",
        "ChannelType": ["CN_NTC", "CN_MKT"],
        "Signature": ["示例签名"],
        "TemplateId": ["template"],
        "StandardErrorCode": ["RE:0214"],
        "IsDomestic": 1,
        "NotSplit": True,
        "DateGroup": 1,
        "StandardErrorCodeGroup": 1,
    }


async def test_account_wide_logs_and_repeated_get_filters(mcp, api_calls):
    await mcp.call_tool("list_send_logs", {"message_id": "message"})
    assert "SubAccount" not in json.loads(api_calls[0][-1].content)
    await mcp.call_tool("list_second_templates", {"sub_accounts": ["group one", "group-two"]})
    request = api_calls[0][-1]
    assert request.url.params.get_list("subAccounts") == ["group one", "group-two"]
    assert "['group" not in str(request.url)


async def test_special_notification_task_uses_body_and_idempotency(mcp, api_calls):
    request = {
        "subAccount": "group",
        "name": "任务",
        "signature": "示例",
        "templateId": "special",
        "fileUrl": "recipients.csv",
        "scheduled": False,
        "sendTime": 0,
        "content": " 原始特殊通知正文 ",
        "idempotencyKey": "stable-key",
    }
    result = await mcp.call_tool("create_batch_task", {"request": request})
    assert not result.is_error
    assert len(api_calls[0]) == 1
    assert api_calls[0][0].url.params["Action"] == "SetBatchTaskForAgent"
    assert json.loads(api_calls[0][0].content) == request
    assert api_calls[0][0].extensions["timeout"]["read"] == 60


async def test_template_traffic_types_and_signature_material_references(mcp, api_calls):
    template = {
        "name": "模板",
        "content": "请查看${url}",
        "channelType": "CN_NTC",
        "templateParams": [{"name": "url", "paramType": 2}],
        "templateTrafficDriving": [[{"name": "url", "paramType": 2, "id": 12}]],
    }
    assert not (await mcp.call_tool("apply_template", {"request": template})).is_error
    assert (
        json.loads(api_calls[0][-1].content)["templateTrafficDriving"]
        == template["templateTrafficDriving"]
    )
    assert api_calls[0][-1].url.params["Action"] == "ApplySmsTemplateV2ForAgent"
    signature = {
        "content": "示例",
        "purpose": 1,
        "signatureIdentificationID": 12,
        "source": 2,
        "appIcp": {"appIcpFileList": [{"fileType": 16, "fileContent": "private/material"}]},
        "uploadFileList": [{"fileType": 6, "fileContent": "private/extra"}],
        "isLimitSubAccount": 1,
        "subAccounts": ["group"],
    }
    assert not (await mcp.call_tool("apply_signature", {"request": signature})).is_error
    assert json.loads(api_calls[0][-1].content) == signature


async def test_wire_schemas_are_inline_and_keep_nested_constraints(mcp, qualification_request):
    tools = await mcp.list_tools()
    assert len(tools) == 30
    for tool in tools:
        for schema in (tool.input_schema, tool.output_schema):
            if schema is None:
                continue
            Draft202012Validator.check_schema(schema)
            serialized = json.dumps(schema)
            for forbidden in ('"$ref"', '"$defs"', '"definitions"'):
                assert forbidden not in serialized
    tool = next(t for t in tools if t.name == "apply_qualification")
    validator = Draft202012Validator(tool.input_schema)
    validator.validate({"request": qualification_request})
    del qualification_request["businessInfo"]["businessCertificateName"]
    assert not validator.is_valid({"request": qualification_request})


def test_schema_keeps_reference_siblings_and_rejects_external_loading():
    schema = {
        "$defs": {"name": {"type": "string"}},
        "type": "object",
        "properties": {"name": {"$ref": "#/$defs/name", "description": "名字", "minLength": 2}},
    }
    original = json.loads(json.dumps(schema))
    output = inline_schema(schema)
    assert output["properties"]["name"] == {"type": "string", "description": "名字", "minLength": 2}
    assert schema == original
    with pytest.raises(jsonref.JsonRefError):
        inline_schema({"$ref": "https://example.invalid/private-schema"})


def test_gateway_bare_sts_is_accepted_but_oauth_tokens_are_not(api_calls, credentials_env):
    with TestClient(
        create_http_app(build_server(api_calls[1]), "https://testserver"),
        base_url="https://testserver",
    ) as http:
        assert rpc(http, "tools/list", token=auth_header("two").split(" ", 1)[1]).status_code == 200
        assert rpc(http, "tools/list", token="Bearer not.a.sts-token").status_code == 401
        assert rpc(http, "tools/list", token=base64.b64encode(b"{}").decode()).status_code == 401
    assert api_calls[0] == []


async def test_tool_and_api_observations_share_correlation_without_private_data(
    mcp, caplog, monkeypatch
):
    spans = []

    class Span:
        def __init__(self, attributes):
            self.attributes, self.events = attributes, []

        def add_event(self, name, attributes):
            self.events.append((name, attributes))

        def set_status(self, status):
            pass

    class Tracer:
        @contextmanager
        def start_as_current_span(self, name, **kwargs):
            span = Span(kwargs["attributes"])
            spans.append(span)
            yield span

    monkeypatch.setattr(observability.trace, "get_tracer", lambda name: Tracer())
    caplog.set_level(logging.INFO, logger="mcp_server_sms.calls")
    result = await mcp.call_tool(
        "register_traffic_resource",
        {
            "request": {
                "action": "BulkCreateTobTrafficDrivingPhoneForAgent",
                "params": {
                    "data": [
                        {
                            "numberType": 1,
                            "number": "13800000000",
                            "personId": "fixture-private-person-id",
                        }
                    ]
                },
            }
        },
    )
    assert not result.is_error
    assert {s.attributes["kind"] for s in spans} == {"tool", "api"}
    assert len({s.attributes["correlation_id"] for s in spans}) == 1
    assert all([event[0] for event in span.events] == ["start", "end"] for span in spans)
    assert "fixture-private-person-id" not in caplog.text
    assert "fixture-secret-key" not in caplog.text
    assert "13800000000" not in caplog.text


@pytest.mark.parametrize(
    "result", [{"taskId": "task"}, {"taskId": "task", "totalCount": True, "dupCount": 0}]
)
def test_missing_or_invalid_batch_counts_leave_write_outcome_unknown(result):
    response = httpx.Response(200, json={"ResponseMetadata": {}, "Result": result})
    decoded = SmsClient.decode("SetBatchTaskForAgent", response, Credentials("ak", "sk"))
    assert decoded["error"]["outcome_unknown"] is True


def test_empty_counts_are_valid_and_private_resource_fields_are_removed():
    credentials = Credentials("fixture-ak", "fixture-sk")
    decoded = SmsClient.decode(
        "SetBatchTaskForAgent",
        httpx.Response(200, json={"Result": {"taskId": "task", "totalCount": 0, "dupCount": 0}}),
        credentials,
    )
    assert decoded["success"] is True
    decoded = SmsClient.decode(
        "ListSignaturesForAgent",
        httpx.Response(
            200,
            json={
                "Result": {
                    "List": [
                        {
                            "AuditOpinion": "保留审核意见",
                            "SubAccounts": [],
                            "operatorPerson": {"personIDCard": "private"},
                            "unknown": {"fileContent": "private-material", "businessStatus": 0},
                        }
                    ],
                    "Total": 1,
                }
            },
        ),
        credentials,
    )
    assert decoded["result"] == {
        "List": [
            {"AuditOpinion": "保留审核意见", "SubAccounts": [], "unknown": {"businessStatus": 0}}
        ],
        "Total": 1,
    }


def test_uncertain_api_error_has_same_outcome_at_tool_and_api_boundaries(caplog):
    calls = []

    def respond(request):
        calls.append(request)
        return httpx.Response(
            200,
            json={
                "ResponseMetadata": {
                    "RequestId": "fixture-uncertain",
                    "Error": {"Code": "1999", "Message": "private"},
                }
            },
        )

    api = SmsClient(transport=httpx.MockTransport(respond))
    caplog.set_level(logging.INFO, logger="mcp_server_sms.calls")
    with TestClient(
        create_http_app(build_server(api), "https://testserver"), base_url="https://testserver"
    ) as http:
        response = rpc(
            http,
            "tools/call",
            token=auth_header("one"),
            params={
                "name": "manage_sms_service",
                "arguments": {
                    "request": {
                        "action": "ActivateSmsProductInOneStep",
                        "params": {"product": ["sms"]},
                    }
                },
            },
        )
    assert response.json()["result"]["isError"]
    assert '"outcome_unknown": true' in response.json()["result"]["content"][0]["text"]
    assert len(calls) == 1
    ends = [
        json.loads(record.getMessage().removeprefix("sms_call "))
        for record in caplog.records
        if record.name == "mcp_server_sms.calls"
    ]
    ends = [event for event in ends if event["event"] == "end"]
    assert {event["kind"] for event in ends} == {"api", "tool"}
    assert all(
        event["result_class"] == "unknown"
        and event["error_code"] == "1999"
        and event["request_id"] == "fixture-uncertain"
        for event in ends
    )


def test_observation_failures_do_not_override_result_or_leave_span_open(monkeypatch):
    closed = []

    class Span:
        def add_event(self, *args):
            raise RuntimeError("trace unavailable")

        def set_status(self, *args):
            raise RuntimeError("trace unavailable")

    class Tracer:
        @contextmanager
        def start_as_current_span(self, *args, **kwargs):
            try:
                yield Span()
            finally:
                closed.append(True)

    def broken_log(*args):
        raise RuntimeError("log unavailable")

    monkeypatch.setattr(observability.trace, "get_tracer", lambda name: Tracer())
    monkeypatch.setattr(logging.getLogger("mcp_server_sms.calls"), "info", broken_log)
    result = {"success": False, "error": {"code": "fixture", "outcome_unknown": True}}
    with observability.observe_call("api", "fixture-action") as observation:
        observation.record(result)
    assert observation.result_class == "unknown"
    assert closed == [True]


@pytest.mark.parametrize(
    "action,result",
    [
        ("ValidateBatchTaskContentForAgent", {"Reason": "missing decision"}),
        ("ValidateBatchTaskContentForAgent", {"Approved": "false"}),
        ("TemplateUploadDemoForAgent", {"value": ""}),
        ("ConfirmProtocolDocument", {"success": [1]}),
        ("ActivateSmsProductInOneStep", {"list": []}),
    ],
)
def test_incomplete_decisions_are_not_reported_as_success(action, result):
    decoded = SmsClient.decode(
        action,
        httpx.Response(200, json={"Result": result}),
        Credentials("fixture-ak", "fixture-sk"),
    )
    assert decoded["success"] is False


def test_partial_protocol_confirmation_is_preserved_without_activation():
    calls = []

    def respond(request):
        calls.append(request)
        return httpx.Response(200, json={"Result": {"success": [1], "fail": [2]}})

    api = SmsClient(transport=httpx.MockTransport(respond))
    with TestClient(
        create_http_app(build_server(api), "https://testserver"), base_url="https://testserver"
    ) as http:
        response = rpc(
            http,
            "tools/call",
            token=auth_header("one"),
            params={
                "name": "manage_sms_service",
                "arguments": {
                    "request": {
                        "action": "ConfirmProtocolDocument",
                        "params": {"product": "sms", "documents": [1, 2]},
                    }
                },
            },
        )
    assert response.json()["result"]["structuredContent"]["result"] == {"success": [1], "fail": [2]}
    assert len(calls) == 1
    assert calls[0].url.params["Action"] == "ConfirmProtocolDocument"


@pytest.mark.parametrize(
    "action,params,result",
    [
        (
            "ConfirmProtocolDocument",
            {"product": "sms", "documents": [1, 2]},
            {"success": [1], "fail": []},
        ),
        (
            "ConfirmProtocolDocument",
            {"product": "sms", "documents": [1, 2]},
            {"success": [], "fail": []},
        ),
        (
            "ConfirmProtocolDocument",
            {"product": "sms", "documents": [1, 2]},
            {"success": [1, 2], "fail": [2]},
        ),
        (
            "ConfirmProtocolDocument",
            {"product": "sms", "documents": [1, 2]},
            {"success": [1, 3], "fail": []},
        ),
        (
            "ActivateSmsProductInOneStep",
            {"product": ["sms"]},
            {"list": [{"product": "other-product", "orderStatus": 1}]},
        ),
        (
            "ActivateSmsProductInOneStep",
            {"product": ["sms"]},
            {"list": [{"product": "sms", "orderStatus": 1}, {"product": "sms", "orderStatus": 1}]},
        ),
    ],
)
def test_service_results_must_match_the_submitted_targets(action, params, result):
    calls = []

    def respond(request):
        calls.append(request)
        return httpx.Response(200, json={"Result": result})

    api = SmsClient(transport=httpx.MockTransport(respond))
    with TestClient(
        create_http_app(build_server(api), "https://testserver"), base_url="https://testserver"
    ) as http:
        response = rpc(
            http,
            "tools/call",
            token=auth_header("one"),
            params={
                "name": "manage_sms_service",
                "arguments": {"request": {"action": action, "params": params}},
            },
        )
    outcome = response.json()["result"]
    assert outcome["isError"] is True
    assert '"outcome_unknown": true' in outcome["content"][0]["text"]
    assert len(calls) == 1
    assert json.loads(calls[0].content) == params


def test_valid_activation_business_failure_is_preserved():
    result = {"list": [{"product": "sms", "orderStatus": 0, "orderDetail": "业务未开通"}]}
    decoded = SmsClient.decode(
        "ActivateSmsProductInOneStep",
        httpx.Response(200, json={"Result": result}),
        Credentials("fixture-ak", "fixture-sk"),
        params={"product": ["sms"]},
    )
    assert decoded["success"] is True
    assert decoded["result"] == result


def test_factory_default_logging_excludes_private_get_parameters(tmp_path):
    code = textwrap.dedent("""
        import asyncio
        import json
        import logging
        import httpx
        from mcp_server_sms.auth import Credentials
        from mcp_server_sms.client import SmsClient
        from mcp_server_sms.server import build_server, create_http_app

        records = []

        class Capture(logging.Handler):
            def emit(self, record):
                records.append(record)

        async def main():
            async with SmsClient(transport=httpx.MockTransport(
                lambda request: httpx.Response(200, json={"Result": {"list": []}})
            )) as api:
                create_http_app(build_server(api))
                logging.getLogger().addHandler(Capture())
                result = await api.call("CheckTrafficDrivingExist", {
                    "content": "fixture-private-sms-body-13800000000"
                }, Credentials("fixture-ak", "fixture-sk"))
                assert result["success"]
            print(json.dumps({
                "root_level": logging.getLogger().level,
                "httpx_records": sum(record.name == "httpx" for record in records),
                "api_events": [json.loads(record.getMessage().removeprefix("sms_call "))["event"]
                               for record in records if record.name == "mcp_server_sms.calls"],
            }))

        asyncio.run(main())
    """)
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=True,
        timeout=30,
    )
    assert json.loads(completed.stdout) == {
        "root_level": logging.WARNING,
        "httpx_records": 0,
        "api_events": ["start", "end"],
    }
    assert "fixture-private-sms-body" not in completed.stderr
