import json

import pytest
from conftest import payload


@pytest.mark.parametrize("arguments,expected_size", [({}, 10), ({"page_size": 5}, 5)])
async def test_qualification_query_uses_small_default_and_preserves_override(
    mcp, api_calls, arguments, expected_size
):
    result = await mcp.call_tool("list_qualifications", arguments)
    assert not result.is_error
    assert len(api_calls[0]) == 1
    request = api_calls[0][0]
    assert request.url.params["Action"] == "GetSignatureIdentificationList"
    assert json.loads(request.content) == {"pageIndex": 1, "pageSize": expected_size}


async def test_send_preview_confirmation_does_not_rewrite(
    mcp, api_calls, monkeypatch, tmp_path
):
    monkeypatch.chdir(tmp_path)
    request = {
            "subAccount": "group-one", "signature": "示例签名", "templateId": "SPT_fixture",
            "mobiles": ["13800000000"], "templateParams": {"text": " 原始 内容 "},
    }
    preview = await mcp.call_tool("preview_sms_send", {"request": request})
    confirmation = payload(preview)["result"]["confirmation"]
    result = await mcp.call_tool("send_sms", {
        "request": request, "confirmation": confirmation,
    })
    assert not result.is_error
    assert payload(result)["result"] == {"MessageIds": ["fixture-message"]}
    calls = api_calls[0]
    assert [item.url.params["Action"] for item in calls] == [
        "ListSecondTemplate", "ListSecondTemplate", "SendSmsForAgent",
    ]
    assert json.loads(calls[-1].content) == {
        "SubAccount": "group-one",
        "Signature": "示例签名",
        "TemplateId": "SPT_fixture",
        "Mobiles": "13800000000",
        "TemplateParam": '{"text":" 原始 内容 "}',
    }
    assert list(tmp_path.iterdir()) == []


async def test_complete_qualification_goes_directly_to_upstream(
    mcp, api_calls, qualification_request
):
    checked = await mcp.call_tool(
        "check_qualification_enterprise",
        {
            "business_certificate_name": "示例企业",
            "unified_social_credit_identifier": "fixture-enterprise-id",
            "legal_person_name": "示例法人",
        },
    )
    assert checked.meta["sms/form"]["result"]["ticket"] == "upstream-enterprise-ticket"
    result = await mcp.call_tool("submit_qualification", {"request": qualification_request})
    assert not result.is_error
    assert payload(result)["result"] == 123
    assert len(api_calls[0]) == 2
    assert api_calls[0][-1].url.params["Action"] == "ApplySignatureIdentificationForAgent"
    assert json.loads(api_calls[0][-1].content) == qualification_request


@pytest.mark.parametrize(
    "tool,arguments,action,body",
    [
        (
            "submit_signature",
            {
                "request": {
                    "content": "示例签名",
                    "purpose": 1,
                    "signatureIdentificationID": 12,
                    "source": 1,
                    "desc": "",
                    "subAccounts": ["g"],
                    "channelTypes": ["CN_NTC"],
                    "appIcp": {"appIcpFilling": "fixture-icp"},
                }
            },
            "ApplySmsSignatureV2",
            {
                "content": "示例签名",
                "purpose": 1,
                "signatureIdentificationID": 12,
                "source": 1,
                "desc": "",
                "subAccounts": ["g"],
                "channelTypes": ["CN_NTC"],
                "appIcp": {"appIcpFilling": "fixture-icp"},
            },
        ),
        (
            "submit_template",
            {
                "request": {
                    "name": "通知",
                    "content": "会议${time}",
                    "channelType": "CN_NTC",
                    "templateParams": [{"name": "time", "paramType": 1}],
                    "signatures": ["示例签名"],
                }
            },
            "ApplySmsTemplateV2ForAgent",
            {
                "name": "通知",
                "content": "会议${time}",
                "area": "cn",
                "channelType": "CN_NTC",
                "templateParams": [{"name": "time", "paramType": 1}],
                "signatures": ["示例签名"],
                    "templateTrafficDriving": [],
                    "fixTrafficDriving": [],
            },
        ),
        (
            "verify_code",
            {"app_id": 1, "scene": 3, "mobile": "13800000000", "code": "1234", "function": 2},
            "CheckSmsVerifyCodeByMobile",
            {"appId": 1, "scene": 3, "mobile": "13800000000", "code": "1234", "func": 2},
        ),
        (
            "send_verification_code",
            {"app_id": 1, "scene": 3, "mobile": "13800000000", "template_id": 2, "code_type": 0},
            "SendSmsVerifyCodeByMobile",
            {"appId": 1, "scene": 3, "mobile": "13800000000", "templateId": 2, "codeType": 0},
        ),
        (
            "recognize_qualification_document",
            {"business_certificate_type": 1, "certificate": "material/one"},
            "GetOCRLicenseForAgent",
            {"businessCertificateType": 1, "certificate": "material/one"},
        ),
        (
            "recognize_qualification_document",
            {"id_card_front_image": "material/front", "id_card_back_image": "material/back"},
            "GetOCRLicenseForAgent",
            {"iDCardFrontImage": "material/front", "iDCardBackImage": "material/back"},
        ),
    ],
)
async def test_api_parameter_contracts(mcp, api_calls, tool, arguments, action, body):
    if tool == "submit_template":
        preview = await mcp.call_tool("preview_template", arguments)
        assert not preview.is_error
        arguments = {**arguments, "confirmation": preview.meta["sms/form"]["result"]["confirmation"]}
    result = await mcp.call_tool(tool, arguments)
    assert not result.is_error
    assert len(api_calls[0]) == (5 if tool == "submit_template" else 1)
    request = api_calls[0][-1]
    assert request.url.params["Action"] == action
    assert request.url.params["Version"] == "2026-01-01"
    assert json.loads(request.content) == body
    if tool == "verify_code":
        assert payload(result)["result"]["status"] == 2


async def test_batch_creation_and_launch_are_independent(mcp, api_calls):
    request = {
        "subAccount": "group-one",
        "name": "普通任务",
        "signature": "示例签名",
        "templateId": "fixture-template",
        "fileUrl": "fixture.csv",
        "scheduled": False,
        "sendTime": 0,
        "idempotencyKey": "fixture-batch-key",
    }
    created = await mcp.call_tool("create_batch_task", {"request": request})
    assert not created.is_error
    assert payload(created)["result"]["taskId"] == "fixture-task"
    assert len(api_calls[0]) == 1
    assert api_calls[0][0].url.params["Action"] == "SetBatchTaskForAgent"
    assert json.loads(api_calls[0][0].content) == request
    result = await mcp.call_tool(
        "start_batch_task", {"sub_account": "group-one", "task_id": "fixture-task"}
    )
    assert not result.is_error
    assert api_calls[0][-1].url.params["Action"] == "ConsentBatchTask"
    result = await mcp.call_tool(
        "cancel_batch_task", {"sub_account": "group-one", "task_id": "fixture-task"}
    )
    assert not result.is_error
    assert api_calls[0][-1].url.params["Action"] == "DeleteBatchTask"
    assert len(api_calls[0]) == 3


async def test_invalid_inputs_do_not_reach_sms(mcp, api_calls, qualification_request):
    bad_send = await mcp.call_tool(
        "send_sms",
        {
            "sub_account": "g",
            "signature": "示例签名",
            "template_id": "t",
            "mobiles": ["not-a-number"],
        },
    )
    assert bad_send.is_error
    bad_ocr = await mcp.call_tool(
        "recognize_qualification_document",
        {
            "business_certificate_type": 1,
            "certificate": "one",
            "id_card_front_image": "two",
        },
    )
    assert bad_ocr.is_error
    qualification_request["Account"] = "someone-else"
    assert (await mcp.call_tool("submit_qualification", {"request": qualification_request})).is_error
    bad_batch = {
        "subAccount": "g",
        "name": "n",
        "signature": "s",
        "templateId": "t",
        "templateName": "n",
        "fileUrl": "f",
        "scheduled": False,
        "sendTime": 0,
        "channelType": "CN_OTP",
    }
    assert (await mcp.call_tool("create_batch_task", {"request": bad_batch})).is_error
    assert api_calls[0] == []


async def test_query_contracts_keep_get_and_post_distinct(mcp, api_calls):
    await mcp.call_tool(
        "query_sms_resources", {"request": {"action": "ListSignaturesForAgent", "params": {"Signature": "示例签名", "SubAccounts": ["g"], "Page": 2}}}
    )
    assert json.loads(api_calls[0][-1].content) == {
        "Signature": "示例签名",
        "SubAccounts": ["g"],
        "Page": 2,
        "PageSize": 20,
    }
    await mcp.call_tool(
        "list_second_templates",
        {"template_id": "一级", "second_template_id": "二级", "signatures": "示例签名"},
    )
    request = api_calls[0][-1]
    assert request.method == "GET"
    assert request.content == b""
    assert request.url.params["templateId"] == "一级"
    assert request.url.params["secondTemplateId"] == "二级"
    assert request.url.params["signatures"] == "示例签名"
    await mcp.call_tool(
        "list_send_logs",
        {"sub_account": "g", "message_id": "message-one", "from_time": 100, "to_time": 200},
    )
    assert json.loads(api_calls[0][-1].content) == {
        "SubAccount": "g",
        "MessageId": "message-one",
        "FromTime": 100,
        "ToTime": 200,
        "Page": 1,
        "PageSize": 20,
    }


async def test_tools_are_named_business_operations(mcp):
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    assert len(tools) == 39
    removed = {
        "execute_sms_operation",
        "get_sms_operation_result",
        "create_qualification_draft",
        "import_input_file",
        "export_qualification_review",
        "check_batch_file",
        "match_template",
    }
    assert removed.isdisjoint(tools)
    upload_preparations = {"prepare_material_upload", "prepare_recipients_upload"}
    assert {name for name in tools if name.startswith("prepare_")} == upload_preparations
    for name in upload_preparations | {"complete_material_upload", "complete_recipients_upload"}:
        assert tools[name].meta["ui"]["visibility"] == ["app"]
    for name, tool in tools.items():
        if tool.name not in {
            "recognize_qualification_document", "check_qualification_enterprise",
            "check_qualification_person", "upload_sms_file", "get_sms_service_onboarding",
            "submit_sms_service_onboarding", "send_batch_test_sms",
            "prepare_material_upload", "complete_material_upload",
            "prepare_recipients_upload", "complete_recipients_upload",
            "preview_template",
        }:
            assert tool.output_schema
        assert "ctx" not in tool.input_schema["properties"]
        if name in {"send_sms", "submit_qualification", "start_batch_task", "verify_code"}:
            assert tool.annotations.read_only_hint is False
            assert tool.annotations.idempotent_hint is False
    assert tools["cancel_batch_task"].annotations.destructive_hint is True
    assert tools["open_sms_service_onboarding"].annotations.read_only_hint is True
    for name in ("submit_sms_service_onboarding", "send_batch_test_sms"):
        assert tools[name].meta["ui"]["visibility"] == ["app"]
        assert tools[name].annotations.read_only_hint is False


async def test_qualification_service_decides_when_check_tickets_are_required(
    mcp, api_calls, qualification_request
):
    for key in ("businessCheckTicket", "operatorCheckTicket", "responsibleCheckTicket"):
        qualification_request.pop(key)
    result = await mcp.call_tool("submit_qualification", {"request": qualification_request})
    assert not result.is_error
    assert json.loads(api_calls[0][0].content) == qualification_request
    assert len(api_calls[0]) == 1
