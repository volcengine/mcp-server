import json
from dataclasses import replace
from types import SimpleNamespace
from mcp.server.mcpserver.context import Context

import pytest

from mcp_server_sms.core import qualification
from mcp_server_sms.store import StoreError
from mcp_server_sms.runtime import Runtime, GuardedClient
from mcp_server_sms.server import build_server


def test_submit_and_resume_on_another_instance(
    runtime, settings, owner, credentials, ready_flow, sms
):
    prepared = runtime.prepare_qualification(ready_flow, None, owner, credentials)
    another = runtime.prepare_qualification(ready_flow, None, owner, credentials)
    second = Runtime(settings)
    result = second.execute(prepared["operationId"], owner, credentials)
    assert result["success"] and result["result"]["qualificationId"] == 123
    assert runtime.execute(prepared["operationId"], owner, credentials) == result
    assert (
        runtime.execute(another["operationId"], owner, credentials)["result"][
            "qualificationId"
        ]
        == 123
    )
    status = runtime.qualification_status(ready_flow, owner, credentials)
    assert status["result"]["status"] == "submitted_for_review"
    assert (
        "sections"
        not in runtime.store.get(ready_flow, owner, "qualification")["data"]["state"]
    )
    assert (
        sum(action == "ApplySignatureIdentificationForAgent" for action, _ in sms.calls)
        == 1
    )
    assert "测试经办人" not in json.dumps(prepared, ensure_ascii=False)
    assert "fixture-ticket" not in json.dumps(prepared)


def test_changed_preview_does_not_submit(runtime, owner, credentials, ready_flow, sms):
    prepared = runtime.prepare_qualification(ready_flow, None, owner, credentials)
    runtime.change_qualification(
        ready_flow, lambda draft: draft.set_base("变更后的资质", 1), owner, credentials
    )
    result = runtime.execute(prepared["operationId"], owner, credentials)
    assert result["success"] is False
    assert result["error"]["code"] == "stale_qualification_preview"
    assert not any(
        action == "ApplySignatureIdentificationForAgent" for action, _ in sms.calls
    )


def test_unknown_submission_is_not_retried_or_cancelled(
    runtime, owner, credentials, ready_flow, sms
):
    sms.responses["ApplySignatureIdentificationForAgent"] = {
        "success": False,
        "request_id": "unknown-fixture",
        "error": {"code": "outcome_unknown", "outcome_unknown": True},
    }
    prepared = runtime.prepare_qualification(ready_flow, None, owner, credentials)
    assert (
        runtime.execute(prepared["operationId"], owner, credentials)["success"] is False
    )
    result = runtime.cancel_qualification(ready_flow, owner, credentials)
    assert result["result"]["status"] == "qualification_submission_outcome_unknown"
    assert result["result"]["outcomeUnknown"] is True
    assert (
        sum(action == "ApplySignatureIdentificationForAgent" for action, _ in sms.calls)
        == 1
    )


def test_foreign_and_cancelled_drafts_never_return_material(
    runtime, owner, credentials, ready_flow
):
    with pytest.raises(StoreError):
        runtime.qualification_status(ready_flow, "foreign-owner", credentials)
    runtime.cancel_qualification(ready_flow, owner, credentials)
    result = runtime.qualification_status(ready_flow, owner, credentials)
    assert result["status"] == "finished"
    assert "sections" not in json.dumps(result)
    with pytest.raises(StoreError):
        runtime.prepare_qualification(ready_flow, None, owner, credentials)


def test_business_change_preserves_name_and_invalidates_checks(
    runtime, owner, credentials, ready_flow
):
    original = runtime.store.get(ready_flow, owner, "qualification")["data"]["state"]
    document = dict(original["sections"]["business"])
    document["businessCertificateName"] = "变更后的测试企业名称与资质名称不同"
    file_id = runtime.inputs.stage(
        owner, "qualification_data", json.dumps(document).encode(), "application/json"
    )["fileId"]
    result = runtime.update_qualification_information(
        ready_flow, "business", file_id, owner, credentials
    )
    assert result["revision"] > 7
    assert result["materialName"] == "测试资质"
    assert result["readyForPreview"] is False
    assert "business_check" in result["missing"]


def test_sms_result_recovers_after_process_loss(
    runtime, owner, credentials, ready_flow, sms
):
    guard = GuardedClient(
        sms,
        runtime.store,
        owner,
        f"qualification:{ready_flow}:submit:7",
        runtime.settings.operation_ttl,
    )
    guard.call("ApplySignatureIdentificationForAgent", {"fixture": "submitted"})
    result = runtime.qualification_status(ready_flow, owner, credentials)
    assert result["result"]["qualificationId"] == 123
    assert (
        runtime.cancel_qualification(ready_flow, owner, credentials)["result"]["status"]
        == "submitted_for_review"
    )
    assert (
        "sections"
        not in runtime.store.get(ready_flow, owner, "qualification")["data"]["state"]
    )


async def test_complete_application_uses_public_tools_without_web(
    runtime, owner, credentials, sms, monkeypatch, tmp_path
):
    runtime = Runtime(
        replace(runtime.settings, public_url="", oidc_issuer="", token_audience="")
    )
    monkeypatch.setattr(runtime, "caller", lambda ctx: (owner, credentials))
    server = build_server(runtime)
    context = Context(request_context=SimpleNamespace(request=None), mcp_server=server)

    async def call(name, args):
        response = await server.call_tool(name, args, context)
        assert not response.is_error, response.content
        return response.structured_content

    requirements = await call("get_qualification_requirements", {})
    assert "personIDCard" in requirements["privateInputSchemas"]["person"]["properties"]
    draft = await call("create_qualification_draft", {"name": "接口验收", "purpose": 1})
    draft_id = draft["draftId"]
    assert "url" not in draft
    business = {
        "businessCertificateType": 1,
        "businessCertificateName": "测试企业",
        "unifiedSocialCreditIdentifier": "911101080000000000",
        "legalPersonName": "测试法人",
        "businessCertificateValidityPeriodStart": "2020-01-01",
        "businessCertificateValidityPeriodEnd": "2099-12-31",
    }
    person = {
        "certificateType": 0,
        "personName": "测试经办人",
        "personIDCard": "110101199001010000",
        "personMobile": "",
    }
    for target, data in [("business", business), ("operator", person)]:
        name = target + ".json"
        (tmp_path / name).write_text(json.dumps(data))
        uploaded = await call(
            "import_input_file",
            {
                "relative_path": name,
                "kind": "qualification_data",
                "content_type": "application/json",
            },
        )
        saved = await call(
            "update_qualification_information",
            {"draft_id": draft_id, "target": target, "file_id": uploaded["fileId"]},
        )
        assert data.get("personName", "测试法人") not in json.dumps(
            saved, ensure_ascii=False
        )
        action = (
            "ThreeElementEnterpriseCheckForAgent"
            if target == "business"
            else "ThreeElementPersonCheckForAgent"
        )
        sms.responses[action] = {
            "success": True,
            "result": {"status": "0", "ticket": "private-ticket-" + target},
        }
        await call(
            "check_qualification_information", {"draft_id": draft_id, "target": target}
        )
    await call(
        "set_qualification_responsible", {"draft_id": draft_id, "same_operator": True}
    )
    ready = await call("get_qualification_draft", {"draft_id": draft_id})
    assert ready["readyForPreview"]
    prepared = await call("prepare_qualification_application", {"draft_id": draft_id})
    assert "private-ticket" not in json.dumps(prepared)
    submitted = await call(
        "execute_sms_operation", {"operation_id": prepared["operationId"]}
    )
    assert submitted["result"]["qualificationId"] == 123
    body = next(
        params
        for action, params in sms.calls
        if action == "ApplySignatureIdentificationForAgent"
    )
    assert body["materialName"] == "接口验收"
    assert "legalPerson" not in body
    assert body["responsibleCheckTicket"] == body["operatorCheckTicket"]


def test_ocr_result_is_private_and_uploaded_material_invalidates_preview(
    runtime, owner, credentials, ready_flow, monkeypatch
):
    monkeypatch.setattr(
        qualification,
        "upload_qualification_file_bytes",
        lambda *args: {"imageUri": "private-image-uri", "imageSuffix": "png"},
    )
    monkeypatch.setattr(
        qualification,
        "ocr_business_certificate_image",
        lambda *args: {
            "legalPersonName": "私密法人姓名",
            "businessCertificateName": "测试企业",
        },
    )
    content = b"\x89PNG\r\n\x1a\n" + b"fixture"
    uploaded = runtime.inputs.stage(owner, "qualification_image", content, "image/png")
    result = runtime.upload_qualification_document(
        ready_flow,
        uploaded["fileId"],
        {"target": "business", "certificate_type": 1},
        owner,
        credentials,
    )
    assert not result["readyForPreview"]
    assert "private-image-uri" not in json.dumps(result)
    recognized = runtime.recognize_qualification_document(
        ready_flow, "business", owner, credentials
    )
    assert "私密法人姓名" not in json.dumps(recognized, ensure_ascii=False)
    assert (
        runtime.inputs.document(recognized["reviewFileId"], owner)["legalPersonName"]
        == "私密法人姓名"
    )


def test_code_preview_verification_and_removal(
    runtime, owner, credentials, ready_flow, sms
):
    with runtime.store.locked(ready_flow, owner, "qualification") as (record, lease):
        state = record["data"]["state"]
        state["mobileVerificationRequired"] = True
        state["sections"]["operator"]["personMobile"] = "13800000000"
        runtime.store.save(ready_flow, owner, record["data"], lease=lease)
    sms.responses["SendSmsVerifyCodeByMobile"] = {
        "success": True,
        "result": {"messageId": "verification-fixture"},
    }
    sms.responses["CheckSmsVerifyCodeByMobile"] = {
        "success": True,
        "result": {"status": 0},
    }
    prepared = runtime.prepare_qualification(ready_flow, "operator", owner, credentials)
    assert "13800000000" not in json.dumps(prepared)
    assert runtime.execute(prepared["operationId"], owner, credentials)["success"]
    repeated = runtime.prepare_qualification(ready_flow, "operator", owner, credentials)
    assert (
        runtime.execute(repeated["operationId"], owner, credentials)["success"] is False
    )
    uploaded = runtime.inputs.stage(
        owner, "verification_code", b'{"code":"1234"}', "application/json"
    )
    result = runtime.verify_qualification_code(
        ready_flow,
        "operator",
        uploaded["fileId"],
        "11111111-1111-4111-8111-111111111111",
        owner,
        credentials,
    )
    assert result["mobileVerifications"]["operator"] is True
    assert "1234" not in json.dumps(result)
    with pytest.raises(StoreError):
        runtime.inputs.read(uploaded["fileId"], owner)
    assert sum(action == "SendSmsVerifyCodeByMobile" for action, _ in sms.calls) == 1


def test_cancelled_preview_cannot_submit(runtime, owner, credentials, ready_flow, sms):
    prepared = runtime.prepare_qualification(ready_flow, None, owner, credentials)
    runtime.cancel_qualification(ready_flow, owner, credentials)
    result = runtime.execute(prepared["operationId"], owner, credentials)
    assert result["success"] is False
    assert result["error"]["code"] == "qualification_draft_cancelled"
    assert not any(
        action == "ApplySignatureIdentificationForAgent" for action, _ in sms.calls
    )
