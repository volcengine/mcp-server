"""模板核对与申请的动态限制和授权绑定回归，所有接口均为 HTTP 替身。"""

import json

import httpx
import pytest
from test_form_parity import form_api, private

BASE = {
    "name": "预约通知", "content": " 原文 ${time} ", "channelType": "CN_NTC",
    "signatures": ["测试签名"], "templateParams": [{"name": "time", "paramType": 1}],
}


def response_for(account=None, fixed=None, resource=None):
    def respond(action, _params):
        if action == "ListAllSmsProduct":
            return account if account is not None else {"userType": "enterprise", "mktParam": 1, "businessName": "测试企业"}
        if action == "CheckTrafficDrivingExist":
            return fixed if fixed is not None else {"list": []}
        if action.startswith("GetTobTrafficDriving"):
            return resource
        assert action == "ApplySmsTemplateV2ForAgent"
        return {"templateId": "template-test", "status": 1}
    return respond


@pytest.mark.parametrize("changes", [
    {"name": "中" * 34}, {"name": "a" * 51}, {"desc": "😀" * 151},
    {"content": "预约 ${VOLC_SMS_URL_TOKEN}", "templateParams": [{"name": "VOLC_SMS_URL_TOKEN", "paramType": 1}]},
    {"content": "${time}${time}"}, {"content": " ${time}" * 21},
    {"channelType": "CN_MKT", "content": "活动优惠", "templateParams": []},
    {"channelType": "CN_OTP", "content": "预约 ${time}"},
    {"shortUrlConfig": {"isEnabled": 1}}, {"shortUrlConfig": {"isNeedClickDetails": "true"}},
    {"shortUrlConfig": {"uaCheckStrategy": True}},
    {"templateParams": [{"name": "time", "paramType": True}]},
    {"content": "查看 ${url}", "templateParams": [{"name": "url", "paramType": 2}],
        "templateTrafficDriving": [[{"name": "url", "paramType": 2, "content": "https://example.com"}]]},
])
def test_static_invalid_fields_do_not_query_or_apply(changes):
    with form_api(response_for()) as (call, calls):
        result = call("preview_template", {"request": {**BASE, **changes}})
        assert result["isError"]
        assert calls == []


@pytest.mark.parametrize("account,channel,code", [
    ({}, "CN_NTC", "invalid_response"),
    ({"userType": "smb"}, "CN_NTC", "template_account_restricted"),
    ({"userType": "enterprise", "mktParam": 0}, "CN_MKT", "template_account_restricted"),
    ({"userType": "enterprise"}, "CN_MKT", "invalid_response"),
    ({"userType": "enterprise", "mktParam": True}, "CN_MKT", "invalid_response"),
    ({"userType": "enterprise", "mktParam": "1"}, "CN_MKT", "invalid_response"),
])
def test_account_restrictions_stop_before_traffic_or_apply(account, channel, code):
    content = f"{BASE['content']} 拒收请回复R" if channel == "CN_MKT" else BASE["content"]
    with form_api(response_for(account=account)) as (call, calls):
        result = call("preview_template", {"request": {**BASE, "channelType": channel, "content": content}})
        assert result["structuredContent"]["error"]["code"] == code
        assert [action for action, _ in calls] == ["ListAllSmsProduct"]


@pytest.mark.parametrize("fixed,code", [
    ({}, "invalid_response"), ({"list": None}, "invalid_response"),
    ({"list": [{"paramType": 2}]}, "invalid_response"),
    ({"list": [{"paramType": True, "isExist": True}]}, "invalid_response"),
    ({"list": [{"paramType": 3, "isExist": "true"}]}, "invalid_response"),
    ({"list": [{"paramType": 2, "isExist": False}]}, "fixed_traffic_missing"),
    ({"list": [
        {"paramType": 2, "isExist": True, "id": 21, "content": "https://example.com/a"},
        {"paramType": 2, "isExist": True, "id": 22, "content": "https://example.com/b"},
    ]}, "too_many_traffic_params"),
])
def test_missing_or_incomplete_fixed_check_never_creates(fixed, code):
    with form_api(response_for(fixed=fixed)) as (call, calls):
        result = call("preview_template", {"request": BASE})
        assert result["structuredContent"]["error"]["code"] == code
        assert [action for action, _ in calls] == ["ListAllSmsProduct", "CheckTrafficDrivingExist"]


@pytest.mark.parametrize("action", ["ListAllSmsProduct", "CheckTrafficDrivingExist"])
def test_query_failure_preserves_error_and_does_not_apply(action):
    normal = response_for()

    def respond(kind, params):
        if kind == action:
            return httpx.Response(400, json={"ResponseMetadata": {"RequestId": "query-request",
                "Error": {"Code": "1999", "Message": "前检查询失败原文"}}})
        return normal(kind, params)
    with form_api(respond) as (call, calls):
        result = call("preview_template", {"request": BASE})
        assert result["structuredContent"]["error"]["message"] == "前检查询失败原文"
        assert result["structuredContent"]["request_id"] == "query-request"
        assert all(kind != "ApplySmsTemplateV2ForAgent" for kind, _ in calls)


def test_preview_is_private_and_submission_rechecks_without_rewriting():
    body = {**BASE, "desc": " 原用途 ", "project": "项目",
        "shortUrlConfig": {"isEnabled": "0", "isNeedClickDetails": "1", "belong": "VMS", "uaCheckStrategy": 3}}
    with form_api(response_for()) as (call, calls):
        preview = call("preview_template", {"request": body})
        assert preview["structuredContent"]["result"] is None
        assert "原文" not in json.dumps(preview["content"], ensure_ascii=False)
        view = private(preview)
        assert view["request"] == {**body, "area": "cn"}
        assert calls == [("ListAllSmsProduct", {"Action": "ListAllSmsProduct", "Version": "2026-01-01"}),
            ("CheckTrafficDrivingExist", {"content": body["content"], "useVolcLink": "false", "Action": "CheckTrafficDrivingExist", "Version": "2026-01-01"})]
        result = call("submit_template", {"request": view["request"], "confirmation": view["confirmation"]})
        assert not result.get("isError")
        assert [action for action, _ in calls] == [
            "ListAllSmsProduct", "CheckTrafficDrivingExist", "ListAllSmsProduct",
            "CheckTrafficDrivingExist", "ApplySmsTemplateV2ForAgent",
        ]
        assert calls[-1][1] == {
            **body, "area": "cn", "templateTrafficDriving": [], "fixTrafficDriving": [],
        }


def test_submit_includes_checked_fixed_traffic_and_id_only_variable_bindings():
    body = {**BASE, "content": "固定号码 4008000000，变量 ${url}",
        "templateParams": [{"name": "url", "paramType": 2}],
        "templateTrafficDriving": [[{"name": "url", "paramType": 2, "id": 12}]]}
    resource = {"list": [{"id": 12, "useVolcLink": False, "link": "https://example.com/variable"}]}
    fixed = {"list": [
        {"paramType": 3, "isExist": True, "id": 31, "content": "4008000000"},
    ]}
    with form_api(response_for(resource=resource, fixed=fixed)) as (call, calls):
        view = private(call("preview_template", {"request": body}))
        result = call("submit_template", {"request": body, "confirmation": view["confirmation"]})
        assert not result.get("isError")
        assert calls[-1] == ("ApplySmsTemplateV2ForAgent", {
            **body, "area": "cn",
            "templateTrafficDriving": [[{"name": "url", "paramType": 2, "id": 12}]],
            "fixTrafficDriving": [{"paramType": 3, "id": 31, "content": "4008000000"}],
        })


@pytest.mark.parametrize("change", ["body", "identity", "account", "fixed", "signature"])
def test_changed_confirmation_never_applies(change):
    account = {"userType": "enterprise", "businessName": "企业一", "mktParam": 1}
    fixed = {"list": []}
    with form_api(response_for(account=account, fixed=fixed)) as (call, calls):
        view = private(call("preview_template", {"request": BASE}))
        args = {"request": BASE, "confirmation": view["confirmation"]}
        if change == "body":
            args["request"] = {**BASE, "content": "修改的 ${time}"}
        elif change == "account":
            account["businessName"] = "企业二"
        elif change == "fixed":
            fixed["list"] = [{"paramType": 3, "isExist": True, "id": 31, "content": "4008000000"}]
        elif change == "signature":
            args["confirmation"] = {**view["confirmation"], "signature": "0" * 64}
        result = call("submit_template", args, identity="two" if change == "identity" else "one")
        assert result["structuredContent"]["error"]["code"] == "template_confirmation_changed"
        assert all(action != "ApplySmsTemplateV2ForAgent" for action, _ in calls)


def test_restricted_account_or_missing_resource_at_submit_stops_write():
    account = {"userType": "enterprise"}
    fixed = {"list": []}
    with form_api(response_for(account=account, fixed=fixed)) as (call, calls):
        view = private(call("preview_template", {"request": BASE}))
        account["userType"] = "smb"
        result = call("submit_template", {"request": BASE, "confirmation": view["confirmation"]})
        assert result["structuredContent"]["error"]["code"] == "template_account_restricted"
        account["userType"] = "enterprise"
        fixed["list"] = [{"paramType": 3, "isExist": False}]
        result = call("submit_template", {"request": BASE, "confirmation": view["confirmation"]})
        assert result["structuredContent"]["error"]["code"] == "fixed_traffic_missing"
        assert all(action != "ApplySmsTemplateV2ForAgent" for action, _ in calls)


@pytest.mark.parametrize("resource", [
    {"list": []}, {"list": [{"id": 12, "link": "https://example.com"}]},
    {"list": [{"id": 12, "useVolcLink": True, "link": "https://example.com"}]},
    {"list": [{"id": 12, "useVolcLink": False, "link": "https://example.com"}] * 2},
])
def test_explicit_resource_ids_need_complete_current_account_record(resource):
    body = {**BASE, "content": "查看 ${url}", "templateParams": [{"name": "url", "paramType": 2}],
        "templateTrafficDriving": [[{"name": "url", "paramType": 2, "id": 12}]]}
    with form_api(response_for(resource=resource)) as (call, calls):
        result = call("preview_template", {"request": body})
        assert result["isError"]
        assert [action for action, _ in calls] == ["ListAllSmsProduct", "GetTobTrafficDrivingLinkListForAgent"]


def test_short_link_id_resolves_jump_url_and_combined_traffic_count():
    body = {**BASE, "channelType": "CN_MKT", "content": "查看 ${url} 拒收请回复R",
        "templateParams": [{"name": "url", "paramType": 2}], "shortUrlConfig": {"isEnabled": "1"},
        "templateTrafficDriving": [[{"name": "url", "paramType": 2, "id": 12}]]}
    resources = {"list": [{"id": 12, "useVolcLink": True, "jumpLink": "https://example.com/A?Q=B"}]}
    fixed = {"list": []}
    with form_api(response_for(resource=resources, fixed=fixed)) as (call, calls):
        view = private(call("preview_template", {"request": body}))
        assert view["request"]["templateTrafficDriving"][0][0]["content"] == "https://example.com/A?Q=B"
        assert calls[1][0] == "GetTobTrafficDrivingLinkListForAgent"
        assert calls[1][1]["id"] == "12" and calls[1][1]["useVolcLink"] == "true"
        assert calls[-1][1]["useVolcLink"] == "true"
        fixed["list"] = [{"paramType": 2, "isExist": True, "id": 32, "content": "https://example.com/fixed"}]
        result = call("preview_template", {"request": body})
        assert result["structuredContent"]["error"]["code"] == "too_many_traffic_params"
        assert all(action != "ApplySmsTemplateV2ForAgent" for action, _ in calls)


def test_regular_link_lookup_uses_matching_resource_mode():
    body = {**BASE, "content": "查看 ${url}", "templateParams": [{"name": "url", "paramType": 2}],
        "templateTrafficDriving": [[{"name": "url", "paramType": 2, "id": 12}]]}
    resources = {"list": [{"id": 12, "useVolcLink": False, "link": "https://example.com/A"}]}
    with form_api(response_for(resource=resources)) as (call, calls):
        view = private(call("preview_template", {"request": body}))
        assert view["request"]["templateTrafficDriving"][0][0]["content"] == "https://example.com/A"
        assert calls[1][0] == "GetTobTrafficDrivingLinkListForAgent"
        assert calls[1][1]["id"] == "12" and calls[1][1]["useVolcLink"] == "false"


def test_smb_fixed_link_and_marketing_risks_are_preview_warnings():
    body = {**BASE, "channelType": "CN_MKT", "content": "活动详情 https://example.com 拒收请回复R", "templateParams": []}
    with form_api(response_for(account={"userType": "smb"}, fixed={"list": [
        {"paramType": 2, "isExist": True, "id": 32, "content": "https://example.com/fixed"},
    ]})) as (call, calls):
        view = private(call("preview_template", {"request": body}))
        assert len(view["warnings"]) == 2
        assert len(calls) == 2
    otp = {**BASE, "channelType": "CN_OTP", "content": "验证码 ${time}"}
    with form_api(response_for(fixed={"list": [
        {"paramType": 3, "isExist": True, "id": 31, "content": "4008000000"},
    ]})) as (call, _):
        result = call("preview_template", {"request": otp})
        assert result["structuredContent"]["error"]["code"] == "invalid_otp_template"


def test_submit_requires_server_confirmation_before_queries():
    with form_api(response_for()) as (call, calls):
        result = call("submit_template", {"request": BASE})
        assert result["isError"] and calls == []
