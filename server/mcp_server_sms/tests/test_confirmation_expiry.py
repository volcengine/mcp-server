"""核验预览确认的有效期和签名绑定，所有短信接口均使用模拟响应。"""

import pytest
from test_form_parity import form_api, private

SEND = {
    "subAccount": "g", "signature": "签名", "templateId": "SPT_fixture",
    "mobiles": ["13800000000"], "templateParams": {"time": "明天"},
}
TEMPLATE = {
    "name": "预约通知", "content": "预约 ${time}", "channelType": "CN_NTC",
    "signatures": ["签名"], "templateParams": [{"name": "time", "paramType": 1}],
}

pytestmark = pytest.mark.parametrize(
    "preview_tool,submit_tool,body,write_action,prefix",
    [
        ("preview_sms_send", "send_sms", SEND, "SendSmsForAgent", "send"),
        ("preview_template", "submit_template", TEMPLATE, "ApplySmsTemplateV2ForAgent", "template"),
    ],
)


@pytest.fixture
def clock(monkeypatch):
    now = [2000000000]
    for module in ("send_checks", "template_checks", "server"):
        monkeypatch.setattr(f"mcp_server_sms.{module}.time", lambda: now[0])
    return now


def respond(action, _params):
    if action == "ListSecondTemplate":
        return {"List": [{
            "TemplateId": "SPT_fixture", "TemplateContent": "预约 ${time}",
            "TemplateParams": [{"Name": "time"}], "ChannelType": "CN_NTC",
            "Signatures": ["签名"], "SubAccounts": ["g"], "BatchOnly": False, "TaskFields": [],
        }]}
    if action == "ListAllSmsProduct":
        return {"userType": "enterprise", "mktParam": 1}
    if action == "CheckTrafficDrivingExist":
        return {"list": []}
    if action == "SendSmsForAgent":
        return {"MessageIds": ["fixture-message"]}
    assert action == "ApplySmsTemplateV2ForAgent"
    return {"templateId": "fixture-template", "status": 1}


def preview_result(tool, result):
    return private(result) if tool == "preview_template" else result["structuredContent"]["result"]


@pytest.mark.parametrize("elapsed", [299, 300, 301])
def test_preview_confirmation_expires_at_signed_deadline(
    clock, preview_tool, submit_tool, body, write_action, prefix, elapsed
):
    with form_api(respond) as (call, calls):
        view = preview_result(preview_tool, call(preview_tool, {"request": body}))
        confirmation = view["confirmation"]
        assert confirmation["expires_at"] == clock[0] + 300
        clock[0] += elapsed
        result = call(submit_tool, {"request": body, "confirmation": confirmation})
        if elapsed < 300:
            assert not result.get("isError")
            assert [action for action, _ in calls].count(write_action) == 1
        else:
            assert result["structuredContent"]["error"]["code"] == f"{prefix}_confirmation_expired"
            assert all(action != write_action for action, _ in calls)


def test_confirmation_deadline_cannot_be_extended_without_a_new_preview(
    clock, preview_tool, submit_tool, body, write_action, prefix
):
    with form_api(respond) as (call, calls):
        view = preview_result(preview_tool, call(preview_tool, {"request": body}))
        forged = {**view["confirmation"], "expires_at": view["confirmation"]["expires_at"] + 3600}
        result = call(submit_tool, {"request": body, "confirmation": forged})
        assert result["structuredContent"]["error"]["code"] == f"{prefix}_confirmation_changed"
        assert all(action != write_action for action, _ in calls)


def test_fresh_preview_after_expiry_can_be_submitted(
    clock, preview_tool, submit_tool, body, write_action, prefix
):
    with form_api(respond) as (call, calls):
        old = preview_result(preview_tool, call(preview_tool, {"request": body}))["confirmation"]
        clock[0] += 301
        current = preview_result(preview_tool, call(preview_tool, {"request": body}))["confirmation"]
        assert current["expires_at"] > old["expires_at"]
        result = call(submit_tool, {"request": body, "confirmation": current})
        assert not result.get("isError")
        assert [action for action, _ in calls].count(write_action) == 1


def test_confirmation_schema_rejects_old_or_untyped_deadlines_before_api_calls(
    clock, preview_tool, submit_tool, body, write_action, prefix
):
    with form_api(respond) as (call, calls):
        for confirmation in (
            "a" * 64,
            {"signature": "a" * 64, "expires_at": True},
            {"signature": "a" * 64, "expires_at": "2000000300"},
        ):
            assert call(submit_tool, {"request": body, "confirmation": confirmation})["isError"]
        assert calls == []
