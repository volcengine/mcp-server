"""MCP 协议下验证表单的新业务分支，短信接口使用 HTTP 替身。"""

import asyncio
import hashlib
import json
from contextlib import contextmanager

import httpx
import pytest
from conftest import auth_header, rpc
from starlette.testclient import TestClient

from mcp_server_sms.auth import Credentials
from mcp_server_sms.client import SmsClient
from mcp_server_sms.configuration import FORM_CONFIG
from mcp_server_sms.protocol import SmsAPIError
from mcp_server_sms.server import build_server, create_http_app
from mcp_server_sms.service_onboarding import ServiceOnboarding
from mcp_server_sms.uploads import FileUploader


@contextmanager
def form_api(respond, *, file_data=None):
    calls = []

    def transport(request):
        action = request.url.params["Action"]
        params = json.loads(request.content) if request.content else dict(request.url.params)
        calls.append((action, params))
        if file_data is not None and action == "GetUploadTosURL":
            result = {"file": "fixture.csv", "url": "https://fixture.volces.com/fixture.csv?signature=put"}
        elif file_data is not None and action == "GetFilePublicTosURL":
            result = {"fileName": "fixture.csv", "url": "https://fixture.volces.com/fixture.csv?signature=get"}
        else:
            result = respond(action, params)
        if isinstance(result, httpx.Response):
            return result
        return httpx.Response(200, json={
            "Result": result, "ResponseMetadata": {"RequestId": "form-fixture"},
        })

    class FileStream(httpx.AsyncByteStream):
        async def __aiter__(self):
            yield file_data
    api = SmsClient(transport=httpx.MockTransport(transport))
    uploader = FileUploader(api, transport=httpx.MockTransport(
        lambda _: httpx.Response(200, stream=FileStream())
    ))
    server = build_server(api, uploader)
    with TestClient(create_http_app(server, public_url="https://testserver", host="0.0.0.0"), base_url="https://testserver") as http:
        def call(name, args=None, *, identity="one"):
            response = rpc(http, "tools/call", token=auth_header(identity), params={
                "name": name, "arguments": args or {},
            })
            assert response.status_code == 200
            return response.json()["result"]

        yield call, calls


def private(result):
    return result["_meta"]["sms/form"]["result"]


def test_qualification_manual_review_uses_upstream_ticket_only_after_confirmation(qualification_request):
    def respond(action, _params):
        if action == "ThreeElementEnterpriseCheckForAgent":
            return {"status": 2, "ticket": "fixture-unmatched-ticket"}
        assert action == "ApplySignatureIdentificationForAgent"
        return 321

    with form_api(respond) as (call, calls):
        check = call("check_qualification_enterprise", {
            "business_certificate_name": "示例公司", "unified_social_credit_identifier": "credit",
            "legal_person_name": "测试人",
        })
        assert private(check) == {
            "manualReview": True, "code": "enterprise_check_mismatch", "requestId": "form-fixture",
        }
        assert "force_skip_check" not in json.dumps(check)
        assert len(calls) == 1

        qualification_request.pop("businessCheckTicket")
        result = call("submit_qualification", {
            "request": qualification_request, "confirm_manual_review": True,
        })
        assert result["structuredContent"]["result"] == 321
        assert [action for action, _ in calls] == [
            "ThreeElementEnterpriseCheckForAgent", "ThreeElementEnterpriseCheckForAgent",
            "ApplySignatureIdentificationForAgent",
        ]
        assert calls[-1][1] == {**qualification_request, "businessCheckTicket": "force_skip_check"}


def test_manual_review_cannot_bypass_permission_rejection(qualification_request):
    def respond(action, _params):
        assert action == "ThreeElementEnterpriseCheckForAgent"
        return httpx.Response(403, json={"ResponseMetadata": {"Error": {"Code": "AccessDenied"}}})

    qualification_request.pop("businessCheckTicket")
    with form_api(respond) as (call, calls):
        result = call("submit_qualification", {
            "request": qualification_request, "confirm_manual_review": True,
        })
        assert result["isError"]
        assert result["structuredContent"]["error"]["code"] == "AccessDenied"
        assert len(calls) == 1


@pytest.mark.parametrize("params", [{}, {"purpose": 0}, {"purpose": 1}, {"purpose": 2}])
def test_signature_candidates_use_native_binding_array_without_pagination(params):
    candidates = [{
        "id": 15, "purpose": 1, "materialName": "示例资质",
        "businessCertificateName": "主体公司",
    }]
    with form_api(lambda *_: candidates) as (call, calls):
        result = call("query_sms_resources", {
            "request": {"action": "GetApplySignatureBind", "params": params},
        })
        assert result["structuredContent"]["result"] == candidates
        assert calls == [("GetApplySignatureBind", {
            "Action": "GetApplySignatureBind", "Version": "2026-01-01",
            **{key: str(value) for key, value in params.items()},
        })]


@pytest.mark.parametrize("candidates", [[], None])
def test_signature_candidates_preserve_native_empty_result(candidates):
    with form_api(lambda *_: candidates) as (call, calls):
        result = call("query_sms_resources", {
            "request": {"action": "GetApplySignatureBind", "params": {}},
        })
        assert result["structuredContent"]["result"] == candidates
        assert len(calls) == 1


def test_signature_candidates_reject_full_list_parameters_before_dispatch():
    with form_api(lambda *_: pytest.fail("invalid query accessed provider")) as (call, calls):
        result = call("query_sms_resources", {
            "request": {"action": "GetApplySignatureBind", "params": {
                "id": 15, "status": [3], "pageIndex": 1, "pageSize": 100,
            }},
        })
        assert result["isError"]
        assert calls == []


@pytest.mark.parametrize("backend_error", [None, "1001"])
def test_signature_submission_leaves_qualification_validation_to_sms(backend_error):
    def respond(action, _params):
        assert action == "ApplySmsSignatureV2"
        if backend_error:
            return httpx.Response(200, json={"ResponseMetadata": {
                "RequestId": "signature-rejected",
                "Error": {"Code": backend_error, "Message": "material no review"},
            }})
        return {"applyId": "application", "status": 1}

    request = {"content": "其他品牌", "purpose": 1, "signatureIdentificationID": 15, "source": 1,
               "projectName": "试点项目"}
    with form_api(respond) as (call, calls):
        result = call("submit_signature", {"request": request})
        if backend_error:
            assert result["isError"]
            assert result["structuredContent"]["error"]["code"] == backend_error
        else:
            assert result["structuredContent"]["result"]["applyId"] == "application"
        assert calls == [("ApplySmsSignatureV2", request)]


def test_traffic_preview_checks_protocol_duplicates_and_number_format_without_writes():
    link = {
        "useVolcLink": False, "protocol": "http", "link": "https://example.com/Upper?Q=One",
        "linkDomainIcp": "备案号", "linkDomainIcpBody": "备案主体",
    }
    create_link = "BulkCreateTobTrafficDrivingLinkForAgent"
    with form_api(lambda *_: pytest.fail("preview accessed provider")) as (call, calls):
        for action, rows, error in (
            (create_link, [link], "traffic_protocol_mismatch"),
            (create_link, [{**link, "protocol": "https"}] * 2, "duplicate_traffic_resource"),
            ("BulkCreateTobTrafficDrivingPhoneForAgent", [
                {"numberType": 2, "number": "13800000000"},
            ], "invalid_traffic_number"),
        ):
            response = call("preview_traffic_resource", {
                "request": {"action": action, "params": {"data": rows}},
            })
            assert response["structuredContent"]["error"]["code"] == error
        assert calls == []


@pytest.mark.parametrize("kind,count", [("phone", 100), ("link", 10)])
def test_bulk_traffic_registration_returns_without_per_item_readback(kind, count):
    if kind == "phone":
        action = "BulkCreateTobTrafficDrivingPhoneForAgent"
        rows = [{"numberType": 2, "number": f"40012345{index:02d}"} for index in range(count)]
    else:
        action = "BulkCreateTobTrafficDrivingLinkForAgent"
        rows = [{"useVolcLink": False, "protocol": "https",
                 "link": f"https://EXAMPLE.com/Offer{index}?Case=Keep",
                 "linkDomainIcp": "备案号", "linkDomainIcpBody": "备案主体"}
                for index in range(count)]
    request = {"action": action, "params": {"data": rows}}
    with form_api(lambda *_: "") as (call, calls):
        result = call("submit_traffic_resources", {"request": request})
        assert result["structuredContent"]["result"] == ""
        assert calls == [(action, request["params"])]


@pytest.mark.parametrize("response", [None, {"resourceIds": [23]}, "unexpected"])
def test_traffic_registration_keeps_unknown_result_without_readback_or_retry(response):
    request = {"action": "BulkCreateTobTrafficDrivingPhoneForAgent", "params": {"data": [
        {"numberType": 2, "number": "4001234567"},
    ]}}
    with form_api(lambda *_: response) as (call, calls):
        result = call("submit_traffic_resources", {"request": request})
        assert result["isError"]
        assert result["structuredContent"]["error"]["outcome_unknown"] is True
        assert calls == [(request["action"], request["params"])]


@pytest.mark.parametrize("renewal,partial", [(False, False), (True, False), (False, True)])
def test_service_only_acts_on_confirmed_current_agreements(renewal, partial):
    catalog = FORM_CONFIG["smsOnboarding"]
    all_ids = [item["id"] for item in catalog["protocols"]]
    documents = [all_ids[1]] if renewal else []
    signed = False
    active = renewal

    def respond(action, params):
        nonlocal signed, active
        if action == "ListAllSmsProduct":
            return {
                "status": 1, "isNewAccount": False, "businessName": "示例账号",
                "documents": [] if signed else documents,
                "list": [{"product": "sms", "status": 2 if active else 0,
                          "userStatus": 1 if active else 0, "isAllowed": True}],
            }
        if action == "ConfirmProtocolDocument":
            assert params == {"product": "sms", "documents": documents if renewal else all_ids}
            if partial:
                return {"success": params["documents"][:-1], "fail": params["documents"][-1:]}
            signed = True
            return {"success": params["documents"], "fail": []}
        assert action == "ActivateSmsProductInOneStep" and not renewal and not partial
        assert signed and params == {"product": ["sms"]}
        active = True
        return {"list": [{"product": "sms", "orderStatus": 1}]}

    with form_api(respond) as (call, calls):
        opened = call("open_sms_service_onboarding")
        assert opened["structuredContent"]["form"] == "service" and not calls
        result = call("get_sms_service_onboarding")
        view = private(result)
        assert view["status"] == ("protocol_confirmation_required" if renewal else "activation_required")
        assert [item["id"] for item in view["protocols"]] == (documents if renewal else all_ids)
        assert view["confirmation"] not in json.dumps(result["structuredContent"])

        request = {"confirmation": view["confirmation"]}
        stale = call("submit_sms_service_onboarding", request, identity="other")
        assert stale["structuredContent"]["error"]["code"] == "service_confirmation_changed"
        assert [action for action, _ in calls] == ["ListAllSmsProduct"] * 2
        result = private(call("submit_sms_service_onboarding", request))
        assert result["status"] == ("protocol_confirmation_failed" if partial else "available")
        assert "confirmation" not in result
        assert [action for action, _ in calls].count("ActivateSmsProductInOneStep") == (not renewal and not partial)


async def test_service_reopen_and_concurrent_submits_stay_locked_until_status_is_known():
    onboarding = ServiceOnboarding()
    credentials = Credentials("fixture-access", "fixture-secret")
    entered = asyncio.Event()
    finish = asyncio.Event()
    calls = []
    active = False

    async def call(action, params):
        calls.append(action)
        if action == "ListAllSmsProduct":
            value = {"status": 1, "isNewAccount": False, "documents": [], "list": [
                {"product": "sms", "status": 2 if active else 0, "userStatus": int(active), "isAllowed": True},
            ]}
        elif action == "ConfirmProtocolDocument":
            entered.set()
            await finish.wait()
            value = {"success": params["documents"], "fail": []}
        else:
            assert action == "ActivateSmsProductInOneStep"
            # 下单异常和拒绝可能共用同一状态，待只读核对。
            value = {"list": [{"product": "sms", "orderStatus": 2}]}
        return {"success": True, "error": None, "result": value, "request_id": "fixture"}

    initial = await onboarding.read(call, credentials)
    submit = asyncio.create_task(onboarding.submit(call, credentials, initial["confirmation"]))
    await asyncio.wait_for(entered.wait(), timeout=2)
    try:
        during = await onboarding.read(call, credentials)
        assert during["status"] == "submission_in_progress" and "confirmation" not in during
        with pytest.raises(SmsAPIError) as concurrent:
            await onboarding.submit(call, credentials, initial["confirmation"])
        assert concurrent.value.result["error"]["code"] == "service_submission_pending"
    finally:
        finish.set()
    assert (await submit)["status"] == "submission_outcome_unknown"
    reopened = await onboarding.read(call, credentials)
    assert reopened["status"] == "submission_outcome_unknown" and "confirmation" not in reopened
    with pytest.raises(SmsAPIError):
        await onboarding.submit(call, credentials, initial["confirmation"])
    assert calls.count("ActivateSmsProductInOneStep") == calls.count("ConfirmProtocolDocument") == 1
    active = True
    assert (await onboarding.read(call, credentials))["status"] == "available"
    assert (await onboarding.submit(call, credentials, initial["confirmation"]))["status"] == "available"


async def test_late_onboarding_read_cannot_release_a_new_pending_submission():
    onboarding = ServiceOnboarding()
    credentials = Credentials("fixture-access", "fixture-secret")
    protocol_ids = [item["id"] for item in FORM_CONFIG["smsOnboarding"]["protocols"]]
    documents = [protocol_ids[0]]
    signed = []
    reading = asyncio.Event()
    release = asyncio.Event()

    def status(pending):
        return {"status": 1, "isNewAccount": False, "documents": pending, "list": [
            {"product": "sms", "status": 2, "userStatus": 1, "isAllowed": True},
        ]}

    async def call(action, params):
        if action == "ListAllSmsProduct":
            value = status(documents)
        else:
            assert action == "ConfirmProtocolDocument"
            signed.append(params["documents"])
            value = {"success": params["documents"], "fail": []}
        return {"success": True, "error": None, "result": value, "request_id": "fixture"}

    async def delayed_read(action, _params):
        assert action == "ListAllSmsProduct"
        reading.set()
        await release.wait()
        return {"success": True, "error": None, "result": status([]), "request_id": "old-read"}

    first = await onboarding.read(call, credentials)
    assert (await onboarding.submit(call, credentials, first["confirmation"]))["status"] == "protocol_confirmation_pending"
    stale_read = asyncio.create_task(onboarding.read(delayed_read, credentials))
    await asyncio.wait_for(reading.wait(), timeout=2)
    try:
        documents = []
        assert (await onboarding.read(call, credentials))["status"] == "available"
        documents = [protocol_ids[1]]
        second = await onboarding.read(call, credentials)
        assert (await onboarding.submit(call, credentials, second["confirmation"]))["status"] == "protocol_confirmation_pending"
    finally:
        release.set()
    assert (await stale_read)["status"] == "protocol_confirmation_pending"
    with pytest.raises(SmsAPIError) as caught:
        await onboarding.submit(call, credentials, second["confirmation"])
    assert caught.value.result["error"]["code"] == "service_submission_pending"
    assert signed == [[protocol_ids[0]], [protocol_ids[1]]]


@pytest.mark.parametrize("error_code", [None, "1001"])
def test_batch_trial_sends_once_and_preserves_sms_validation_result(error_code):
    def respond(action, params):
        assert action == "SendSmsForAgent"
        assert params["Mobiles"] == "13800000000"
        assert json.loads(params["TemplateParam"]) == {"name": " 原样 "}
        if error_code:
            return httpx.Response(200, json={"ResponseMetadata": {
                "Error": {"Code": error_code, "Message": "template unavailable"},
            }})
        return {"MessageIds": ["fixture-message"]}

    with form_api(respond) as (call, calls):
        result = call("send_batch_test_sms", {"request": {
            "sub_account": "g", "signature": "示例签名", "template_id": "t",
            "mobile": "13800000000", "template_params": {"name": " 原样 "},
        }})
        assert [action for action, _ in calls] == ["SendSmsForAgent"]
        if error_code:
            assert result["isError"]
            assert result["structuredContent"]["error"]["code"] == error_code
        else:
            assert private(result)["messageId"] == "fixture-message"
        assert "13800000000" not in json.dumps(result)


def test_batch_traffic_checks_rendered_content_only_and_reuses_identical_rows():
    text = "查看 ${url}"
    csv = ("phone,url\n13800000000,https://example.com/A\n"
           "13800000001,https://example.com/B\n13800000002,https://example.com/A\n")

    def respond(action, params):
        if action == "ListSecondTemplate":
            return {"list": [{"templateId": "t", "useVolcLink": True}]}
        assert action == "CheckTrafficDrivingExist" and params["useVolcLink"] == "true"
        return {"list": [{"paramType": 2, "isExist": params["content"].endswith("/B")}]}

    with form_api(respond, file_data=csv.encode()) as (call, calls):
        prepared = private(call("prepare_recipients_upload", {"request": {
            "name": "demo.csv", "size": len(csv.encode()), "sha256": hashlib.sha256(csv.encode()).hexdigest(),
            "sub_account": "g", "template_id": "t",
        }}))
        response = call("complete_recipients_upload", {"request": prepared["confirmation"], "columns": ["phone", "url"], "traffic": {
            "sub_account": "g", "signature": "签名", "template_id": "t", "content": text,
        }})
        report = private(response)["trafficReport"]
        assert report == {
            "totalRows": 3, "checkedRows": 3, "failedRows": 0, "uncheckedRows": 0,
            "missingResourceRows": 2, "missingRowNumbers": [2, 4],
        }
        checked = [params["content"] for action, params in calls if action == "CheckTrafficDrivingExist"]
        assert sorted(checked) == ["查看 https://example.com/A", "查看 https://example.com/B"]
        assert "example.com" not in json.dumps(response["content"])
        assert "example.com" not in json.dumps(response["structuredContent"])


def test_virtual_template_without_short_link_detail_reports_uncovered_rows():
    def respond(action, _params):
        assert action == "ListSecondTemplate"
        return {"list": []}

    data = b"phone\n13800000000\n"
    with form_api(respond, file_data=data) as (call, calls):
        prepared = private(call("prepare_recipients_upload", {"request": {
            "name": "demo.csv", "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "sub_account": "g", "template_id": "virtual",
        }}))
        response = call("complete_recipients_upload", {"request": prepared["confirmation"], "columns": ["phone"], "traffic": {
            "sub_account": "g", "signature": "签名", "template_id": "virtual", "content": "演示通知",
        }})
        report = private(response)["trafficReport"]
        assert report.pop("failures")[0]["error"]["code"] == "short_link_mode_unknown"
        assert report == {
            "totalRows": 1, "checkedRows": 0, "failedRows": 0, "uncheckedRows": 1,
            "missingResourceRows": 0, "missingRowNumbers": [], "reason": "short_link_mode_unavailable",
        }
        assert [action for action, _ in calls] == ["GetUploadTosURL", "GetFilePublicTosURL", "ListSecondTemplate"]


@pytest.mark.parametrize("code", ["1001", "1999", "SY:0500"])
def test_backend_errors_are_not_classified_across_both_send_forms(code):
    def respond(action, _params):
        if action == "ListSecondTemplate":
            return {"List": [{
                "TemplateId": "t", "TemplateContent": "测试内容",
                "TemplateParams": [], "ChannelType": "CN_NTC",
                "Signatures": ["签名"], "SubAccounts": ["g"],
                "BatchOnly": False, "TaskFields": [],
            }]}
        assert action == "SendSmsForAgent"
        return httpx.Response(200, json={"ResponseMetadata": {"Error": {"Code": code}}})

    selection = {"sub_account": "g", "signature": "签名", "template_id": "t"}
    with form_api(respond) as (call, calls):
        request = {"subAccount": "g", "signature": "签名", "templateId": "t", "mobiles": ["13800000000"]}
        preview = call("preview_sms_send", {"request": request})
        direct = call("send_sms", {
            "request": request,
            "confirmation": preview["structuredContent"]["result"]["confirmation"],
        })
        trial = call("send_batch_test_sms", {"request": {
            **selection, "mobile": "13800000000",
        }})
        for result in (direct, trial):
            assert result["structuredContent"]["error"]["code"] == code
            assert "outcome_unknown" not in result["structuredContent"]["error"]
            assert result["structuredContent"]["error"]["backend_response"] == {
                "ResponseMetadata": {"Error": {"Code": code}},
            }
        assert [action for action, _ in calls] == [
            "ListSecondTemplate", "ListSecondTemplate",
            "SendSmsForAgent", "SendSmsForAgent",
        ]


def test_send_rechecks_template_resource_after_confirmation():
    query_count = 0

    def respond(action, _params):
        nonlocal query_count
        assert action == "ListSecondTemplate"
        query_count += 1
        return {"List": [{
            "TemplateId": "t",
            "TemplateContent": "通知${text}" if query_count == 1 else "变更${text}",
            "TemplateParams": [{"Name": "text"}],
            "ChannelType": "CN_NTC",
            "Signatures": ["签名"],
            "SubAccounts": ["g"],
            "BatchOnly": False,
            "TaskFields": [],
        }]}

    request = {
        "subAccount": "g", "signature": "签名", "templateId": "t",
        "mobiles": ["13800000000"], "templateParams": {"text": "内容"},
    }
    with form_api(respond) as (call, calls):
        preview = call("preview_sms_send", {"request": request})
        result = call("send_sms", {
            "request": request,
            "confirmation": preview["structuredContent"]["result"]["confirmation"],
        })
        assert result["isError"] is True
        assert result["structuredContent"]["error"]["code"] == "send_confirmation_changed"
        assert [action for action, _ in calls] == [
            "ListSecondTemplate", "ListSecondTemplate",
        ]


def test_send_confirmation_cannot_cross_authorized_accounts():
    def respond(action, _params):
        assert action == "ListSecondTemplate"
        return {"List": [{
            "TemplateId": "t", "TemplateContent": "通知${text}",
            "TemplateParams": [{"Name": "text"}], "ChannelType": "CN_NTC",
            "Signatures": ["签名"], "SubAccounts": ["g"],
            "BatchOnly": False, "TaskFields": [],
        }]}

    request = {
        "subAccount": "g", "signature": "签名", "templateId": "t",
        "mobiles": ["13800000000"], "templateParams": {"text": "内容"},
    }
    with form_api(respond) as (call, calls):
        preview = call("preview_sms_send", {"request": request}, identity="one")
        result = call("send_sms", {
            "request": request,
            "confirmation": preview["structuredContent"]["result"]["confirmation"],
        }, identity="two")
        assert result["isError"] is True
        assert result["structuredContent"]["error"]["code"] == "send_confirmation_changed"
        assert [action for action, _ in calls] == [
            "ListSecondTemplate", "ListSecondTemplate",
        ]
