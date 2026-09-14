import time

import pytest
from sqlalchemy import update

from mcp_server_sms.core.api_protocol import ResolvedCredentials
from mcp_server_sms.server import (
    SignatureRequest,
    TemplateRequest,
    SendRequest,
    BatchLaunchRequest,
)
from mcp_server_sms.store import StoreError, records


def test_frozen_signature_operation_revalidates_and_deduplicates(
    runtime, owner, credentials, sms
):
    request = SignatureRequest(
        content="测试签名",
        purpose=1,
        qualification_id=11,
        sub_account=["group-one"],
        channel_type=["CN_NTC"],
        source=1,
    )
    result = runtime.prepare("signature", request.model_dump(), owner, credentials)
    operation = result["operationId"]
    with pytest.raises(StoreError):
        runtime.execute(operation, "another-owner", credentials)
    with pytest.raises(StoreError):
        runtime.execute(
            operation, owner, ResolvedCredentials("different-key", "different-secret")
        )
    for _ in range(2):
        assert runtime.execute(operation, owner, credentials)["success"] is True
    assert sum(action == "ApplySmsSignatureV2" for action, _ in sms.calls) == 1


def test_resource_review_changed_since_preview_prevents_write(
    runtime, owner, credentials, sms
):
    request = SignatureRequest(
        content="测试签名",
        purpose=1,
        qualification_id=11,
        sub_account=["group-one"],
        channel_type=["CN_NTC"],
        source=1,
    )
    result = runtime.prepare("signature", request.model_dump(), owner, credentials)
    sms.responses["GetSignatureIdentificationList"] = {
        "success": True,
        "result": {"List": []},
        "error": None,
    }
    assert (
        runtime.execute(result["operationId"], owner, credentials)["success"] is False
    )
    assert not any(action == "ApplySmsSignatureV2" for action, _ in sms.calls)


def test_model_options_match_retained_workflow_parser(runtime):
    models = [
        (
            "template-preview",
            TemplateRequest(
                name="test",
                content="内容",
                channel_type="CN_NTC",
                signature=["测试"],
                sub_account=["one"],
            ),
        ),
        (
            "send-preview",
            SendRequest(
                sub_account="one",
                signature="测试",
                template_id="T1",
                mobile=["13800000000"],
                template_params={},
            ),
        ),
        (
            "batch-launch-preview",
            BatchLaunchRequest(
                sub_account="one",
                task_id="task",
                file_sha256="a" * 64,
                total_count=1,
                valid_count=1,
                invalid_count=0,
                dup_count=0,
            ),
        ),
    ]
    for command, model in models:
        assert runtime.arguments(command, model.model_dump()).command == command


def approved_resources(sms):
    template = {
        "TemplateId": "T1",
        "Status": 3,
        "Content": "会议时间为${time}",
        "TemplateName": "会议通知",
        "ChannelType": "CN_NTC",
        "TemplateParams": [{"name": "time"}],
        "Signatures": ["测试签名"],
        "SubAccounts": ["group-one"],
    }

    def ok(result):
        return {"success": True, "result": result, "error": None}

    sms.responses.update(
        {
            "GetSubAccountDetail": ok({"subAccountId": "group-one", "status": 1}),
            "ListSignatureForAgent": ok(
                {
                    "List": [
                        {
                            "Signature": "测试签名",
                            "Status": 3,
                            "SubAccounts": ["group-one"],
                            "ChannelTypes": ["CN_NTC"],
                        }
                    ]
                }
            ),
            "ListSmsTemplateForAgent": ok({"List": [template]}),
            "ListSecondTemplate": ok({"List": [template]}),
            "SendSmsForAgent": ok({"MessageId": "fixture-message"}),
            "ApplySmsTemplateV2": ok({"templateId": "T1", "status": 1}),
        }
    )
    return template, ok


def test_send_uses_exact_variables_and_masks_preview(runtime, owner, credentials, sms):
    import json
    from mcp_server_sms.core.workflows import CliError

    approved_resources(sms)
    request = SendRequest(
        sub_account="group-one",
        signature="测试签名",
        template_id="T1",
        mobile=["13800000000"],
        template_params={"time": "明天九点"},
    )
    prepared = runtime.prepare("send", request.model_dump(), owner, credentials)
    assert "13800000000" not in json.dumps(prepared)
    assert "明天九点" not in json.dumps(prepared, ensure_ascii=False)
    assert (
        runtime.operation_result(prepared["operationId"], owner, credentials)["status"]
        == "not_executed"
    )
    result = runtime.execute(prepared["operationId"], owner, credentials)
    assert result["success"]
    assert (
        runtime.operation_result(prepared["operationId"], owner, credentials) == result
    )
    assert sum(action == "SendSmsForAgent" for action, _ in sms.calls) == 1
    request.template_params = {"wrong": "值"}
    with pytest.raises(CliError):
        runtime.prepare("send", request.model_dump(), owner, credentials)


@pytest.mark.parametrize("outcome_unknown", [False, True])
def test_execution_result_outlives_preview(
    runtime, owner, credentials, sms, outcome_unknown
):
    approved_resources(sms)
    if outcome_unknown:
        sms.responses["SendSmsForAgent"] = {
            "success": False,
            "error": {"code": "outcome_unknown", "outcome_unknown": True},
        }
    request = SendRequest(
        sub_account="group-one",
        signature="测试签名",
        template_id="T1",
        mobile=["13800000000"],
        template_params={"time": "明天九点"},
    )
    prepared = runtime.prepare("send", request.model_dump(), owner, credentials)
    operation_id = prepared["operationId"]
    result = runtime.execute(operation_id, owner, credentials)
    with runtime.store.engine.begin() as connection:
        connection.execute(
            update(records)
            .where(records.c.id == operation_id)
            .values(expires=time.time() - 1)
        )
    runtime.store.cleanup()

    assert runtime.operation_result(operation_id, owner, credentials) == result
    with pytest.raises(StoreError):
        runtime.operation_result(operation_id, "another-owner", credentials)
    with pytest.raises(StoreError):
        runtime.execute(operation_id, owner, credentials)
    assert sum(action == "SendSmsForAgent" for action, _ in sms.calls) == 1


def test_template_and_ordinary_batch_creation_do_not_launch(
    runtime, owner, credentials, sms, monkeypatch
):
    from mcp_server_sms.core import workflows
    from mcp_server_sms.server import BatchRequest, BatchLaunchRequest

    template, ok = approved_resources(sms)
    request = TemplateRequest(
        name="会议",
        content="会议时间为${time}",
        channel_type="CN_NTC",
        signature=["测试签名"],
        sub_account=["group-one"],
        template_param=["time"],
    )
    prepared = runtime.prepare("template", request.model_dump(), owner, credentials)
    assert runtime.execute(prepared["operationId"], owner, credentials)["success"]
    uploaded = runtime.inputs.stage(
        owner, "batch_csv", b"phone,time\n13800000000,09:00\n", "text/csv"
    )
    batch = BatchRequest(
        file_id=uploaded["fileId"],
        sub_account="group-one",
        task_name="fixture-batch",
        signature="测试签名",
        template_id="T1",
    )
    prepared = runtime.prepare_batch(batch.model_dump(), owner, credentials)
    sms.responses["GetUploadTosURL"] = ok(
        {"url": "https://upload.example/fixture", "file": "fixture-object"}
    )
    task = {
        "taskId": "task-one",
        "subAccount": "group-one",
        "status": 2,
        "signature": "测试签名",
        "templateId": "T1",
        "templateName": "会议通知",
        "channelType": "CN_NTC",
        "fileUrl": "fixture-object",
        "scheduled": False,
        "totalCount": 1,
        "validCount": 1,
        "invalidCount": 0,
        "dupCount": 0,
    }
    sms.responses["SetBatchTask"] = ok({"taskId": "task-one", "status": 2})
    sms.responses["GetBatchTaskDetail"] = ok(task)
    captured = []
    original = workflows.execute

    def execute(args, client, **kwargs):
        return original(
            args, client, uploader=lambda url, body: captured.append(body), **kwargs
        )

    monkeypatch.setattr(workflows, "execute", execute)
    created = runtime.execute(prepared["operationId"], owner, credentials)
    assert created["success"], created
    assert captured == [b"phone,time\n13800000000,09:00\n"]
    assert not any(action == "ConsentBatchTask" for action, _ in sms.calls)
    metadata = created["result"]
    launch = BatchLaunchRequest(
        sub_account="group-one",
        task_id="task-one",
        file_sha256=metadata["fileSha256"],
        total_count=1,
        valid_count=1,
        invalid_count=0,
        dup_count=0,
    )
    planned = runtime.prepare("batch_launch", launch.model_dump(), owner, credentials)
    sms.responses["ConsentBatchTask"] = ok({"taskId": "task-one"})
    assert runtime.execute(planned["operationId"], owner, credentials)["success"]
    assert sum(action == "ConsentBatchTask" for action, _ in sms.calls) == 1


def test_batch_rejects_otp_and_foreign_files(runtime, owner, credentials, sms):
    from mcp_server_sms.core.workflows import CliError
    from mcp_server_sms.server import BatchRequest

    template, ok = approved_resources(sms)
    uploaded = runtime.inputs.stage(
        owner, "batch_csv", b"phone,time\n13800000000,09:00\n", "text/csv"
    )
    request = BatchRequest(
        file_id=uploaded["fileId"],
        sub_account="group-one",
        task_name="batch",
        signature="测试签名",
        template_id="T1",
    )
    with pytest.raises(StoreError):
        runtime.prepare_batch(request.model_dump(), "other-owner", credentials)
    template["ChannelType"] = "CN_OTP"
    with pytest.raises(CliError):
        runtime.prepare_batch(request.model_dump(), owner, credentials)


async def test_template_detail_exposes_reviewable_content_and_checks_binding(
    runtime, owner, credentials, sms, monkeypatch
):
    from mcp_server_sms.server import build_server
    from mcp.server.mcpserver.exceptions import ToolError

    template, _ = approved_resources(sms)
    monkeypatch.setattr(runtime, "caller", lambda ctx: (owner, credentials))
    server = build_server(runtime)
    result = await server.call_tool(
        "get_template",
        {"template_id": "T1", "signature": "测试签名", "sub_account": "group-one"},
    )
    detail = result.structured_content
    assert detail["content"] == "会议时间为${time}"
    assert detail["variables"] == ["time"]
    assert detail["contentRedacted"] is False
    with pytest.raises(ToolError):
        await server.call_tool(
            "get_template",
            {"template_id": "T1", "signature": "其他签名", "sub_account": "group-one"},
        )
    template["Content"] = "联系13800000000，会议时间为${time}"
    result = await server.call_tool(
        "get_template",
        {"template_id": "T1", "signature": "测试签名", "sub_account": "group-one"},
    )
    assert result.structured_content["contentRedacted"] is True
    assert "13800000000" not in result.structured_content["content"]
    assert all(action == "ListSecondTemplate" for action, _ in sms.calls)
