"""模型可见面仅包含查询和开表；详细提交由 App-only 工具承载。"""

import json

import pytest
from conftest import payload

from mcp_server_sms.models import TemplateApplication
from mcp_server_sms.protocol import SmsAPIError
from mcp_server_sms.template_checks import validate_template_application

MODEL_TOOLS = {
    "open_qualification_form", "open_signature_form", "open_traffic_form", "open_batch_task_form",
    "open_template_form", "open_sms_send_form", "open_sms_service_onboarding",
    "query_batch_tasks", "query_sms_resources", "get_account_information",
    "get_qualification_requirements", "list_qualifications", "list_templates",
    "list_second_templates", "list_send_logs", "get_send_statistics", "get_batch_csv_template",
}


async def test_model_tools_are_readonly_and_do_not_accept_submission_requests(mcp):
    tools = await mcp.list_tools()
    visible = {t.name for t in tools if "model" in (t.meta or {}).get("ui", {}).get("visibility", ["model", "app"])}
    assert visible == MODEL_TOOLS
    removed = {"apply_qualification", "apply_signature", "apply_template", "register_traffic_resource",
               "list_message_groups", "get_message_group", "list_signatures", "get_batch_task",
               "list_batch_tasks", "get_batch_upload_url", "manage_sms_service", "upload_sms_file"}
    assert removed.isdisjoint(t.name for t in tools)
    for tool in tools:
        if tool.name in visible:
            assert tool.annotations.read_only_hint is True
            if tool.name.startswith("open_"):
                assert "request" not in tool.input_schema["properties"]
        else:
            assert tool.meta["ui"]["visibility"] == ["app"]
    for name in ["recognize_qualification_document", "check_qualification_enterprise", "check_qualification_person"]:
        tool = next(t for t in tools if t.name == name)
        assert "private" not in tool.input_schema["properties"]


@pytest.mark.parametrize("name,draft", [
    ("open_template_form", {"name": "测试模板", "content": "内容${url}", "channelType": "CN_MKT",
        "signatures": ["签名"], "subAccounts": ["group"], "project": "项目", "desc": " 原文 ",
        "templateParams": [{"name": "url", "paramType": 2}],
        "shortUrlConfig": {"isEnabled": "1", "belong": "VMS", "isNeedClickDetails": "1", "uaCheckStrategy": 3},
        "templateTrafficDriving": [[{"name": "url", "paramType": 2, "id": 12,
            "content": "https://example.com/A?Case=Keep"}]]}),
    ("open_sms_send_form", {"subAccount": "group", "signature": "签名", "templateId": "t",
        "mobiles": ["13800000000"], "templateParams": {"text": " 私密变量 "}}),
])
async def test_new_forms_preserve_all_prefill_fields_without_business_calls(name, draft, mcp, api_calls):
    result = await mcp.call_tool(name, {"prefill": draft})
    assert not result.is_error and payload(result)["mode"] == "input"
    assert result.meta["sms/form"]["prefill"] == draft
    assert "13800000000" not in json.dumps(payload(result))
    assert "私密变量" not in json.dumps(payload(result), ensure_ascii=False)
    assert api_calls[0] == []


async def test_existing_batch_task_opens_without_creating_or_starting(mcp, api_calls):
    reference = {"subAccount": "g", "taskId": "task"}
    result = await mcp.call_tool("open_batch_task_form", {"task": reference})
    assert result.meta["sms/form"]["task"] == reference
    assert payload(result)["form"] == "batch" and api_calls[0] == []
    bad = await mcp.call_tool("open_batch_task_form", {"task": reference, "prefill": {}})
    assert bad.is_error and api_calls[0] == []


async def test_group_detail_and_task_queries_keep_exact_native_contract(mcp, api_calls):
    calls = [
        ("query_sms_resources", "GetSubAccountDetail", {"subAccount": "g"}),
        ("query_batch_tasks", "GetBatchTaskDetail", {"subAccount": "g", "taskId": "task"}),
        ("query_batch_tasks", "GetBatchTaskList", {"subAccount": "g", "taskName": " 原文 ", "pageIndex": 2, "pageSize": 5}),
    ]
    for tool, action, params in calls:
        result = await mcp.call_tool(tool, {"request": {"action": action, "params": params}})
        assert not result.is_error
        request = api_calls[0][-1]
        assert request.method == "GET" and request.url.params["Action"] == action
        assert dict(request.url.params) == {"Action": action, "Version": "2026-01-01", **{k: str(v) for k, v in params.items()}}


@pytest.mark.parametrize("changes,code", [
    ({"templateParams": []}, "invalid_template_variables"),
    ({"templateParams": [{"name": "x", "paramType": 1}]}, "invalid_template_variables"),
    ({"signatures": []}, "signature_required"),
    ({"channelType": "CN_OTP", "content": "${time}${time}"}, "invalid_otp_template"),
    ({"shortUrlConfig": {"isEnabled": "1"}}, "invalid_short_link"),
    ({"templateParams": [{"name": "time", "paramType": 2}]}, "traffic_binding_required"),
])
def test_template_submission_validates_structure_without_rewriting(changes, code):
    request = TemplateApplication.model_validate({"name": "模板", "channelType": "CN_NTC", "signatures": ["签名"],
        "content": " 原文${time} ", "templateParams": [{"name": "time", "paramType": 1}], **changes})
    with pytest.raises(SmsAPIError) as error:
        validate_template_application(request)
    assert error.value.result["error"]["code"] == code


@pytest.mark.parametrize("params", [{}, {"text": "原文"}, {"text": "原文", "extra": "原样传递"}])
async def test_send_leaves_template_validation_to_sms(params, mcp, api_calls):
    result = await mcp.call_tool("send_sms", {"request": {
        "subAccount": "g", "signature": "签名", "templateId": "SPT_fixture",
        "mobiles": ["13800000000"], "templateParams": params,
    }})
    assert not result.is_error
    assert [request.url.params["Action"] for request in api_calls[0]] == ["SendSmsForAgent"]
    assert json.loads(api_calls[0][0].content)["TemplateParam"] == json.dumps(
        params, ensure_ascii=False, separators=(",", ":")
    )
