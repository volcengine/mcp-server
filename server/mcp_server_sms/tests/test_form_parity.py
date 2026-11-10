"""MCP 协议下验证表单的新业务分支，短信接口使用 HTTP 替身。"""

import asyncio
import base64
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


@contextmanager
def form_api(respond):
    calls = []

    def transport(request):
        action = request.url.params["Action"]
        params = json.loads(request.content) if request.content else dict(request.url.params)
        calls.append((action, params))
        result = respond(action, params)
        if isinstance(result, httpx.Response):
            return result
        return httpx.Response(200, json={
            "Result": result, "ResponseMetadata": {"RequestId": "form-fixture"},
        })

    server = build_server(SmsClient(transport=httpx.MockTransport(transport)))
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
            "legal_person_name": "测试人", "private": True, "offer_manual_review": True,
        })
        assert private(check) == {
            "manualReview": True, "code": "enterprise_check_mismatch", "requestId": "form-fixture",
        }
        assert "force_skip_check" not in json.dumps(check)
        assert len(calls) == 1

        qualification_request.pop("businessCheckTicket")
        result = call("apply_qualification", {
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
        result = call("apply_qualification", {
            "request": qualification_request, "confirm_manual_review": True,
        })
        assert result["isError"]
        assert result["structuredContent"]["error"]["code"] == "AccessDenied"
        assert len(calls) == 1


def test_signature_rechecks_current_company_and_requires_accepting_name_risk():
    def respond(action, _params):
        if action == "GetSignatureIdentificationList":
            return {"list": [{
                "id": 15, "purpose": 1, "auditStatus": 3, "usable": True,
                "businessInfo": {"businessCertificateName": "主体公司"},
            }], "total": 1}
        assert action == "ApplySmsSignatureV2"
        return {"applyId": "application", "status": 1}

    request = {"content": "其他品牌", "purpose": 1, "signatureIdentificationID": 15, "source": 1,
               "projectName": "试点项目"}
    with form_api(respond) as (call, calls):
        for name, accepted, error in (
            ("旧主体公司", True, "qualification_changed"),
            ("主体公司", False, "signature_name_risk"),
        ):
            result = call("apply_signature", {
                "request": request,
                "confirmation": {"businessCertificateName": name, "acceptNameRisk": accepted},
            })
            assert result["structuredContent"]["error"]["code"] == error
        assert [action for action, _ in calls] == ["GetSignatureIdentificationList"] * 2
        result = call("apply_signature", {
            "request": request,
            "confirmation": {"businessCertificateName": "主体公司", "acceptNameRisk": True},
        })
        assert result["structuredContent"]["result"]["applyId"] == "application"
        assert calls[-1] == ("ApplySmsSignatureV2", request)


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


def test_traffic_registration_reports_readback_partial_without_rewriting():
    numbers = [{"numberType": 2, "number": f"400123456{index}"} for index in (1, 2)]
    create_phone = "BulkCreateTobTrafficDrivingPhoneForAgent"

    def respond(action, params):
        if action == create_phone:
            return ""
        assert action == "GetTobTrafficDrivingPhoneListForAgent"
        rows = [{"id": 23, "number": numbers[0]["number"], "personId": "private-field"}]
        return {"list": rows if params["number"] == numbers[0]["number"] else []}

    with form_api(respond) as (call, calls):
        result = call("register_traffic_resource", {
            "request": {"action": create_phone, "params": {"data": numbers}}, "read_back": True,
        })
        assert result["structuredContent"]["result"] == {
            "resourceIds": [23], "submittedRecordCount": 2, "verified": False,
        }
        assert [action for action, _ in calls].count(create_phone) == 1
        assert "private-field" not in json.dumps(result)


@pytest.mark.parametrize("accepted", [True, False])
def test_traffic_readback_requires_accepted_write_and_preserves_link_path(accepted):
    link = "https://EXAMPLE.com/Offer?Case=Keep"
    request = {"action": "BulkCreateTobTrafficDrivingLinkForAgent", "params": {"data": [{
        "useVolcLink": False, "protocol": "https", "link": link,
        "linkDomainIcp": "备案号", "linkDomainIcpBody": "备案主体",
    }]}}

    def respond(action, params):
        if action == request["action"]:
            assert params["data"][0]["link"] == link
            return "" if accepted else None
        assert action == "GetTobTrafficDrivingLinkListForAgent" and accepted
        return {"list": [
            {"id": 55, "link": "https://example.com/Offer?Case=Keep"},
            {"id": 56, "link": "https://example.com/offer?Case=Keep"},
        ]}

    with form_api(respond) as (call, calls):
        result = call("register_traffic_resource", {"request": request, "read_back": True})
        if accepted:
            assert result["structuredContent"]["result"]["resourceIds"] == [55]
        else:
            assert result["structuredContent"]["error"]["outcome_unknown"] is True
            assert len(calls) == 1


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


@pytest.mark.parametrize("batch_only,content_changed", [(False, False), (True, False), (False, True)])
def test_batch_trial_checks_template_then_sends_exactly_one_mobile(batch_only, content_changed):
    template = {"TemplateId": "t", "ChannelType": "CN_NTC", "BatchOnly": batch_only,
                "TemplateContent": "你好 ${name}"}

    def respond(action, params):
        if action == "ListBatchTemplatesForAgent":
            return {"List": [template], "Total": 1}
        if action == "TemplateUploadDemoForAgent":
            return {"value": "phone,name\n"}
        assert action == "SendSmsForAgent"
        assert params["Mobiles"] == "13800000000"
        assert json.loads(params["TemplateParam"]) == {"name": " 原样 "}
        return {"MessageIds": ["fixture-message"]}

    with form_api(respond) as (call, calls):
        result = call("send_batch_test_sms", {"request": {
            "sub_account": "g", "signature": "示例签名", "template_id": "t",
            "mobile": "13800000000", "template_params": {"name": " 原样 "},
            "template_content": "过期正文" if content_changed else template["TemplateContent"],
        }})
        sends = [params for action, params in calls if action == "SendSmsForAgent"]
        if batch_only or content_changed:
            assert result["isError"] and not sends
        else:
            assert len(sends) == 1 and private(result)["messageId"] == "fixture-message"
        assert "13800000000" not in json.dumps(result)


def test_batch_traffic_checks_rendered_content_only_and_reuses_identical_rows():
    text = "查看 ${url}"
    template = {"TemplateId": "t", "ChannelType": "CN_NTC", "TemplateContent": text}
    csv = ("phone,url\n13800000000,https://example.com/A\n"
           "13800000001,https://example.com/B\n13800000002,https://example.com/A\n")

    def respond(action, params):
        if action == "ListBatchTemplatesForAgent":
            return {"List": [template], "Total": 1}
        if action == "TemplateUploadDemoForAgent":
            return {"value": "phone,url\n"}
        if action == "ListSecondTemplate":
            return {"list": [{"templateId": "t", "useVolcLink": True}]}
        assert action == "CheckTrafficDrivingExist" and params["useVolcLink"] == "true"
        return {"list": [{"paramType": 2, "isExist": params["content"].endswith("/B")}]}

    with form_api(respond) as (call, calls):
        response = call("check_batch_traffic_resources", {"request": {
            "sub_account": "g", "signature": "签名", "template_id": "t", "template_content": text,
            "file": {"name": "demo.csv", "data": base64.b64encode(csv.encode()).decode()},
        }})
        report = response["structuredContent"]["result"]
        assert report == {
            "totalRows": 3, "checkedRows": 3, "failedRows": 0, "uncheckedRows": 0,
            "missingResourceRows": 2, "missingRowNumbers": [2, 4],
        }
        checked = [params["content"] for action, params in calls if action == "CheckTrafficDrivingExist"]
        assert sorted(checked) == ["查看 https://example.com/A", "查看 https://example.com/B"]
        assert "example.com" not in json.dumps(response)


def test_virtual_template_without_short_link_detail_reports_uncovered_rows():
    def respond(action, _params):
        if action == "ListBatchTemplatesForAgent":
            return {"List": [{
                "TemplateId": "virtual", "ChannelType": "CN_NTC", "BatchOnly": True,
                "TemplateContent": "${content}", "TaskFields": [{"Name": "content", "Required": True}],
            }], "Total": 1}
        if action == "TemplateUploadDemoForAgent":
            return {"value": "phone\n"}
        assert action == "ListSecondTemplate"
        return {"list": []}

    with form_api(respond) as (call, calls):
        response = call("check_batch_traffic_resources", {"request": {
            "sub_account": "g", "signature": "签名", "template_id": "virtual", "content": "演示通知",
            "file": {"name": "demo.csv", "data": base64.b64encode(b"phone\n13800000000\n").decode()},
        }})
        assert response["structuredContent"]["result"] == {
            "totalRows": 1, "checkedRows": 0, "failedRows": 0, "uncheckedRows": 1,
            "missingResourceRows": 0, "missingRowNumbers": [], "reason": "short_link_mode_unavailable",
        }
        assert len(calls) == 3


def test_uncertain_trial_does_not_change_existing_direct_send_error():
    def respond(action, _params):
        if action == "ListBatchTemplatesForAgent":
            return {"List": [{"TemplateId": "t", "ChannelType": "CN_NTC", "TemplateContent": "演示"}]}
        if action == "TemplateUploadDemoForAgent":
            return {"value": "phone\n"}
        assert action == "SendSmsForAgent"
        return httpx.Response(200, json={"ResponseMetadata": {"Error": {"Code": "1999"}}})

    selection = {"sub_account": "g", "signature": "签名", "template_id": "t"}
    with form_api(respond) as (call, _):
        direct = call("send_sms", {**selection, "mobiles": ["13800000000"]})
        trial = call("send_batch_test_sms", {"request": {
            **selection, "mobile": "13800000000", "template_content": "演示",
        }})
        assert direct["structuredContent"]["error"]["outcome_unknown"] is False
        assert trial["structuredContent"]["error"]["outcome_unknown"] is True
