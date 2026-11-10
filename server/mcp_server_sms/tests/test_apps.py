import asyncio
import base64
import hashlib
import json
from importlib.resources import files
from pathlib import Path

import httpx
import pytest
from conftest import auth_header, payload, rpc
from jsonschema import Draft202012Validator
from starlette.testclient import TestClient

from mcp_server_sms.auth import Credentials
from mcp_server_sms.client import SmsClient
from mcp_server_sms.forms import FORM_URI
from mcp_server_sms.server import build_server, create_http_app
from mcp_server_sms.upload_models import MaterialUpload, RecipientsUpload, SmsRequestError
from mcp_server_sms.uploads import IMAGEX, FileUploader


@pytest.mark.parametrize(
    "name,form",
    [
        ("apply_qualification", "qualification"),
        ("apply_signature", "signature"),
        ("register_traffic_resource", "traffic"),
        ("create_batch_task", "batch"),
        ("open_sms_service_onboarding", "service"),
    ],
)
async def test_open_form_never_writes_or_replays(name, form, mcp, api_calls):
    for _ in range(2):
        result = await mcp.call_tool(name, {})
        assert payload(result)["form"] == form
        assert payload(result)["mode"] == "input"
    assert api_calls[0] == []
    tool = next(tool for tool in await mcp.list_tools() if tool.name == name)
    assert tool.meta["ui"]["resourceUri"] == FORM_URI


_DRAFT_FILE = {"name": "fixture-private.png", "data": "Zml4dHVyZS1wcml2YXRl"}


@pytest.mark.parametrize(
    "name,form,draft",
    [
        ("apply_qualification", "qualification", {
            "purpose": 2, "materialName": "测试资质", "sameOperator": False, "includeLegal": True,
            "businessInfo": {
                "businessCertificateType": 4, "businessCertificateName": "测试企业",
                "unifiedSocialCreditIdentifier": "fixture-credit", "legalPersonName": "测试法人",
                "businessCertificateValidityPeriodStart": "2020-01-01",
                "businessCertificateValidityPeriodEnd": "长期", "businessCertificate": _DRAFT_FILE,
            },
            "operatorPerson": {
                "personName": "测试经办人", "personIDCard": "fixture-private-identity",
                "personMobile": "13800000000",
                "personCertificate": {"front": _DRAFT_FILE, "back": _DRAFT_FILE},
            },
            "responsiblePersonInfo": {"personName": "测试责任人"},
            "legalPerson": {"certificateType": 1, "personCertificate": {"document": _DRAFT_FILE}},
            "powerOfAttorney": [_DRAFT_FILE], "otherMaterials": [_DRAFT_FILE],
        }),
        ("apply_signature", "signature", {
            "content": "测试签名", "source": 3, "signatureIdentificationID": 12,
            "subAccounts": ["group"], "isLimitSubAccount": 1, "desc": " 测试说明 ",
            "trademark": {
                "trademarkCn": "测试商标", "trademarkEn": "Example", "trademarkNumber": "001",
                "trademarkFileList": [_DRAFT_FILE],
            },
            "uploadFileList": [_DRAFT_FILE],
        }),
        ("apply_signature", "signature", {"appIcp": {"appIcpFilling": "fixture-icp"}}),
        ("register_traffic_resource", "traffic", {
            "kind": "link", "data": [
                {"useVolcLink": True, "jumpLink": "https://example.com/Path?Q=A"},
                {"useVolcLink": False, "protocol": "缺省", "linkDomainIcpBody": "示例企业"},
            ],
        }),
        ("register_traffic_resource", "traffic", {
            "kind": "phone", "data": [
                {"numberType": 1, "number": "13800000000", "numberPerson": "测试人员",
                 "personType": 1, "personId": "fixture-private-id"},
                {"numberType": 2, "company": "示例企业", "numberProvince": "北京", "numberCity": "北京"},
            ],
        }),
        ("create_batch_task", "batch", {
            "name": "测试任务", "signature": "测试签名", "templateId": "template",
            "content": " 原文 ", "scheduled": True, "sendTime": 1800000001,
            "recipientsFile": {"name": "list.csv", "data": "cGhvbmUKMTM4MDAwMDAwMDAK"},
        }),
    ],
)
async def test_host_prefill_is_partial_private_and_never_writes(
    name, form, draft, mcp, api_calls, caplog
):
    arguments = {"prefill": draft}
    tool = next(tool for tool in await mcp.list_tools() if tool.name == name)
    Draft202012Validator(tool.input_schema).validate(arguments)
    result = await mcp.call_tool(name, arguments)
    assert not result.is_error
    assert payload(result)["form"] == form
    assert payload(result)["mode"] == "input"
    assert payload(result)["result"] is None
    assert result.meta["sms/form"]["prefill"] == draft
    assert "prefill" not in payload(result)
    assert "prefill" not in json.loads(result.content[0].text)
    events = [
        json.loads(record.getMessage().removeprefix("sms_call "))
        for record in caplog.records if record.name == "mcp_server_sms.calls"
    ]
    form_events = [event for event in events if event["kind"] == "form"]
    assert [event["event"] for event in form_events] == ["start", "end"]
    assert form_events[-1]["path"] == "prefilled"
    assert form_events[-1]["result_class"] == "success"
    assert "fixture-private" not in caplog.text
    assert api_calls[0] == []


async def test_prefill_and_request_are_mutually_exclusive_for_every_form(
    mcp, api_calls, qualification_request
):
    requests = {
        "apply_qualification": qualification_request,
        "apply_signature": {
            "content": "测试签名", "purpose": 1, "source": 1, "signatureIdentificationID": 12,
        },
        "register_traffic_resource": {
            "action": "BulkCreateTobTrafficDrivingPhoneForAgent",
            "params": {"data": [{"numberType": 2, "number": "4008000000"}]},
        },
        "create_batch_task": {
            "subAccount": "group", "signature": "测试签名", "templateId": "template",
            "name": "测试任务", "fileUrl": "private/list.csv", "scheduled": False,
            "sendTime": 0, "idempotencyKey": "fixture-key",
        },
    }
    for name, request in requests.items():
        prefill = {"kind": "phone"} if name == "register_traffic_resource" else {}
        result = await mcp.call_tool(name, {"prefill": prefill, "request": request})
        assert result.is_error
        assert "不可同时传入" in result.content[0].text
    assert api_calls[0] == []


@pytest.mark.parametrize(
    "name,draft",
    [
        ("apply_qualification", {"businessCheckTicket": "fixture-private-ticket"}),
        ("apply_qualification", {"operatorPerson": {"code": "fixture-private-code"}}),
        ("apply_qualification", {"businessInfo": {"fixture-private-value-as-key": "value"}}),
        ("apply_signature", {"uploadFileList": [{"fileContent": "fixture-private-reference"}]}),
        ("create_batch_task", {"fileUrl": "fixture-private-key"}),
        ("create_batch_task", {"scheduled": False, "sendTime": 1800000000}),
    ],
)
async def test_prefill_rejects_forged_verification_or_upload_results(name, draft, mcp, api_calls):
    result = await mcp.call_tool(name, {"prefill": draft})
    assert result.is_error
    assert result.structured_content["error"]["code"] == "invalid_arguments"
    assert "fixture-private" not in result.model_dump_json()
    if "businessInfo" in draft:
        assert result.structured_content["error"]["fields"] == [
            {"field": ["prefill", "businessInfo"], "type": "extra_forbidden"},
        ]
    assert api_calls[0] == []


async def test_invalid_upload_is_definite_and_does_not_echo_file_bytes(mcp, api_calls):
    result = await mcp.call_tool(
        "upload_sms_file",
        {
            "request": {
                "kind": "material",
                "category": "unsupported",
                "name": "image.png",
                "data": "fixture-private-file",
            }
        },
    )
    assert result.is_error
    assert result.structured_content["error"]["code"] == "invalid_arguments"
    assert result.structured_content["error"]["outcome_unknown"] is False
    assert "fixture-private-file" not in result.model_dump_json()
    assert not api_calls[0]


def test_ui_resource_is_self_contained_and_uses_standard_apps_metadata(api_calls):
    with TestClient(
        create_http_app(build_server(api_calls[1]), host="0.0.0.0"),
        base_url="https://testserver",
    ) as http:
        listed = rpc(http, "resources/list", token=auth_header("one"))
        resource = listed.json()["result"]["resources"][0]
        assert resource["uri"] == FORM_URI
        assert resource["mimeType"] == "text/html;profile=mcp-app"
        response = rpc(http, "resources/read", token=auth_header("one"), params={"uri": FORM_URI})
        assert response.status_code == 200 and "result" in response.json(), response.text
    content = response.json()["result"]["contents"][0]
    assert content["mimeType"] == "text/html;profile=mcp-app"
    assert content["_meta"]["ui"]["csp"]["connectDomains"] == []
    assert content["_meta"]["ui"]["csp"]["resourceDomains"] == []
    assert '<script type="module"' in content["text"]
    assert 'src="/src/' not in content["text"]
    assert 'href="/src/' not in content["text"]
    assert "wizard-page" in content["text"] and "signature-page" in content["text"]
    assert "traffic-page" in content["text"] and "batch-page" in content["text"]
    assert api_calls[0] == []


@pytest.mark.parametrize("private", [None, True])
def test_private_ocr_values_do_not_enter_model_content_or_structured_output(private):
    record = {"personName": "fixture-private-name", "personIDCard": "fixture-private-document"}
    api = SmsClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"Result": record}))
    )
    with TestClient(
        create_http_app(build_server(api), host="0.0.0.0"), base_url="https://testserver"
    ) as http:
        tools = rpc(http, "tools/list", token=auth_header("one")).json()["result"]["tools"]
        tool = next(item for item in tools if item["name"] == "recognize_qualification_document")
        assert tool["inputSchema"]["properties"]["private"]["default"] is True
        assert "private=False" in tool["description"] and "structuredContent" in tool["description"]
        arguments = {"id_card_front_image": "fixture/front", "id_card_back_image": "fixture/back"}
        if private is not None:
            arguments["private"] = private
        response = rpc(
            http, "tools/call", token=auth_header("one"),
            params={"name": "recognize_qualification_document", "arguments": arguments},
        )
    result = response.json()["result"]
    assert result["_meta"]["sms/form"]["result"] == record
    assert "fixture-private" not in json.dumps(result["content"])
    assert "fixture-private" not in json.dumps(result["structuredContent"])


def material_api(request):
    assert request.url.params["Action"] == "GetMUploadParam"
    return httpx.Response(
        200,
        json={
            "Result": {
                "token": {
                    "accessKeyId": "image-access",
                    "secretAccessKey": "image-secret",
                    "sessionToken": "image-token",
                }
            }
        },
    )


def image_responder(request, calls, upload_host=None):
    calls.append(request)
    action = request.url.params.get("Action")
    if action == "ApplyImageUpload":
        return httpx.Response(
            200,
            json={
                "Result": {
                    "UploadAddress": {
                        "UploadHosts": [upload_host or f"{IMAGEX['serviceId']}.up.imagex-accelerate.volces.com"],
                        "SessionKey": "fixture-session",
                        "StoreInfos": [
                            {"StoreUri": "bucket/material.png", "Auth": "fixture-upload-auth"}
                        ],
                    }
                }
            },
            headers={"set-cookie": "tenant=first; Secure; Path=/"},
        )
    if action == "CommitImageUpload":
        return httpx.Response(
            200, json={"Result": {"Results": [{"Uri": "bucket/material.png", "UriStatus": 2000}]}}
        )
    return httpx.Response(200, json={"code": 2000})


def test_upload_credentials_never_leave_server_and_material_bytes_are_unchanged(caplog):
    calls = []
    api = SmsClient(transport=httpx.MockTransport(material_api))
    uploader = FileUploader(
        api, transport=httpx.MockTransport(lambda request: image_responder(request, calls))
    )
    data = b"\x89PNG\r\n\x1a\nfixture-image"
    with TestClient(
        create_http_app(build_server(api, uploader), host="0.0.0.0"),
        base_url="https://testserver",
    ) as http:
        tools = rpc(http, "tools/list", token=auth_header("one")).json()["result"]["tools"]
        upload_tool = next(tool for tool in tools if tool["name"] == "upload_sms_file")
        assert upload_tool["_meta"]["ui"]["visibility"] == ["app"]
        response = rpc(
            http,
            "tools/call",
            token=auth_header("one"),
            params={
                "name": "upload_sms_file",
                "arguments": {
                    "request": {
                        "kind": "material",
                        "category": "business",
                        "name": "material.png",
                        "data": base64.b64encode(data).decode(),
                    }
                },
            },
        )
    result = response.json()["result"]
    assert not result["isError"], result
    assert result["_meta"]["sms/form"]["result"]["fileContent"] == "bucket/material.png"
    assert len(calls) == 3 and calls[1].content == data
    assert "AWS4-HMAC-SHA256" in calls[0].headers["authorization"]
    assert calls[0].headers["x-amz-security-token"] == "image-token"
    assert "cookie" not in calls[2].headers
    assert json.loads(calls[2].content)["SuccessOids"] == ["bucket/material.png"]
    for secret in (
        "image-access",
        "image-secret",
        "image-token",
        "fixture-upload-auth",
        "fixture-session",
    ):
        assert secret not in json.dumps(result)
        assert secret not in caplog.text
    assert "bucket/material.png" not in json.dumps(result["structuredContent"])


async def test_normal_sms_call_still_redacts_internal_upload_credentials():
    async with SmsClient(transport=httpx.MockTransport(material_api)) as api:
        result = await api.call("GetMUploadParam", {}, Credentials("fixture-ak", "fixture-sk"))
    assert result["success"] is True
    assert result["result"] is None
    assert "image-secret" not in json.dumps(result)
    assert "image-token" not in json.dumps(result)


@pytest.mark.parametrize(
    "data,valid",
    [
        (b"phone,name\n13800000000,one\n13800000000,two\n", True),
        (b"mobile,name\n13800000000,one\n", False),
        (b"phone,name\nnot-a-phone,one\n", False),
        (b"phone,name\n", False),
    ],
)
async def test_recipient_upload_validates_native_header_and_preserves_file(data, valid):
    sms_calls, upload_calls = [], []

    def sms(request):
        sms_calls.append(request)
        result = (
            {"value": "phone,name\n13800000000,example\n"}
            if request.url.params["Action"] == "TemplateUploadDemoForAgent"
            else {
                "file": "fixture.csv",
                "url": "https://fixture.volces.com/fixture.csv?signature=opaque",
            }
        )
        return httpx.Response(200, json={"Result": result})

    def put(request):
        upload_calls.append(request)
        return httpx.Response(200)

    request = RecipientsUpload(
        kind="recipients",
        name="names.csv",
        data=base64.b64encode(data).decode(),
        sub_account="group",
        template_id="template",
    )
    async with (
        SmsClient(transport=httpx.MockTransport(sms)) as api,
        FileUploader(api, transport=httpx.MockTransport(put)) as uploader,
    ):
        if not valid:
            with pytest.raises(SmsRequestError):
                await uploader.upload(request, Credentials("fixture-ak", "fixture-sk"))
            assert len(sms_calls) == 1 and not upload_calls
            return
        result = await uploader.upload(request, Credentials("fixture-ak", "fixture-sk"))
    assert result["totalCount"] == 2 and result["dupCount"] == 1
    assert result["samples"][0] == {"phone": "138****0000", "params": {"name": "one"}}
    assert len(upload_calls) == 1 and upload_calls[0].content == data
    assert "authorization" not in upload_calls[0].headers
    assert "url" not in result


async def test_material_upload_timeout_stays_unknown_without_retry():
    calls = []

    def timeout(request):
        calls.append(request)
        raise httpx.ReadTimeout("fixture internal details")

    request = MaterialUpload(
        kind="material",
        category="identity",
        name="image.png",
        data=base64.b64encode(b"fixture-image").decode(),
    )
    async with (
        SmsClient(transport=httpx.MockTransport(material_api)) as api,
        FileUploader(api, transport=httpx.MockTransport(timeout)) as uploader,
    ):
        with pytest.raises(SmsRequestError) as caught:
            await uploader.upload(request, Credentials("fixture-ak", "fixture-sk"))
    assert caught.value.result["error"]["outcome_unknown"] is True
    assert "internal details" not in str(caught.value)
    assert len(calls) == 1


@pytest.mark.parametrize(
    "stage,expected_calls",
    [("ApplyImageUpload", 1), ("UploadMaterial", 2), ("CommitImageUpload", 3)],
)
async def test_incomplete_upload_results_never_advance_or_report_success(stage, expected_calls):
    calls = []

    def respond(request):
        current = request.url.params.get("Action") or "UploadMaterial"
        if current == stage:
            calls.append(request)
            return httpx.Response(200, json={"Result": {}, "code": 0})
        return image_responder(request, calls)

    request = MaterialUpload(
        kind="material",
        category="business",
        name="image.png",
        data=base64.b64encode(b"fixture").decode(),
    )
    async with (
        SmsClient(transport=httpx.MockTransport(material_api)) as api,
        FileUploader(api, transport=httpx.MockTransport(respond)) as uploader,
    ):
        with pytest.raises(SmsRequestError) as caught:
            await uploader.upload(request, Credentials("fixture-ak", "fixture-sk"))
    assert caught.value.result["error"]["outcome_unknown"]
    assert len(calls) == expected_calls


async def test_upload_capacity_rejects_without_queueing_and_releases_slots():
    entered, release = asyncio.Event(), asyncio.Event()
    started, calls = [], []

    async def respond(request):
        if request.url.params.get("Action") == "ApplyImageUpload":
            started.append(request)
            if len(started) == 2:
                entered.set()
            await release.wait()
        return image_responder(request, calls)

    request = MaterialUpload(
        kind="material",
        category="business",
        name="image.png",
        data=base64.b64encode(b"fixture").decode(),
    )
    credentials = Credentials("fixture-ak", "fixture-sk")
    async with (
        SmsClient(transport=httpx.MockTransport(material_api)) as api,
        FileUploader(api, transport=httpx.MockTransport(respond)) as uploader,
    ):
        pending = [asyncio.create_task(uploader.upload(request, credentials)) for _ in range(2)]
        try:
            await asyncio.wait_for(entered.wait(), 3)
            with pytest.raises(SmsRequestError) as caught:
                await uploader.upload(request, credentials)
            assert caught.value.result["error"]["code"] == "upload_busy"
            assert caught.value.result["error"]["outcome_unknown"] is False
            assert len(started) == 2
        finally:
            release.set()
            await asyncio.gather(*pending)
        assert (await uploader.upload(request, credentials))["fileContent"] == "bucket/material.png"


def test_installed_package_includes_html_resource():
    assert files("mcp_server_sms").joinpath("static/forms.html").is_file()


def test_bundled_html_matches_the_reviewed_frontend_sources():
    root = Path(__file__).resolve().parents[1]
    static = files("mcp_server_sms").joinpath("static")
    manifest = json.loads(static.joinpath("build-manifest.json").read_text())
    for name, digest in manifest["sources"].items():
        path = (root / name).resolve()
        assert path.is_relative_to(root)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, (
            f"Rebuild UI: {name} changed"
        )
    assert (
        hashlib.sha256(static.joinpath("forms.html").read_bytes()).hexdigest()
        == manifest["htmlSha256"]
    )


def test_explicit_public_ocr_keeps_original_fields_for_authorized_callers():
    record = {"personName": "fixture-name", "personIDCard": "fixture-document"}
    api = SmsClient(transport=httpx.MockTransport(
        lambda request: httpx.Response(200, json={"Result": record})
    ))
    with TestClient(
        create_http_app(build_server(api), host="0.0.0.0"), base_url="https://testserver"
    ) as http:
        response = rpc(http, "tools/call", token=auth_header("one"), params={
            "name": "recognize_qualification_document",
            "arguments": {"id_card_front_image": "fixture/front", "id_card_back_image": "fixture/back", "private": False},
        })
    result = response.json()["result"]
    assert result["structuredContent"]["result"] == record
    assert json.loads(result["content"][0]["text"])["result"] == record
    assert "sms/form" not in result.get("_meta", {})


@pytest.mark.parametrize("host", [
    f"{IMAGEX['serviceId']}.up.imagex-{IMAGEX['region']}.volces.com",
    f"{IMAGEX['serviceId']}.up.imagex-accelerate.volces.com",
    "tos-lf-x.snssdk.com", "tos-hl-x.snssdk.com",
    "tos-nc2-slb2.bytecdn.cn", "tos-nc2-slb1.bytecdn.cn",
    "tos-lf-x-tob.bytecdn.cn", "tos-lq-x-tob.bytecdn.cn", "tos-hl-x-tob.bytecdn.cn",
])
async def test_material_upload_allows_documented_service_and_legacy_hosts(host):
    calls = []
    request = MaterialUpload(kind="material", category="identity", name="image.png", data=base64.b64encode(b"fixture-image").decode())
    async with (
        SmsClient(transport=httpx.MockTransport(material_api)) as api,
        FileUploader(api, transport=httpx.MockTransport(lambda r: image_responder(r, calls, host))) as uploader,
    ):
        result = await uploader.upload(request, Credentials("fixture-ak", "fixture-sk"))
    assert result["fileContent"] == "bucket/material.png"
    assert len(calls) == 3 and calls[1].url.host == host


@pytest.mark.parametrize("host", [
    "upload.example.invalid", "localhost", "127.0.0.1", "169.254.169.254",
    "other-service.up.imagex-cn-north-1.volces.com", "evil.volces.com",
    "tos-lf-x.snssdk.com.evil.invalid", "sub.tos-lf-x.snssdk.com",
    "unrelated.bytecdn.cn", "tos-lf-x-tob.bytecdn.cn:443",
])
async def test_untrusted_material_hosts_stop_before_file_and_authorization_are_sent(host):
    calls = []
    request = MaterialUpload(kind="material", category="identity", name="image.png", data=base64.b64encode(b"fixture-private-image").decode())
    async with (
        SmsClient(transport=httpx.MockTransport(material_api)) as api,
        FileUploader(api, transport=httpx.MockTransport(lambda r: image_responder(r, calls, host))) as uploader,
    ):
        with pytest.raises(SmsRequestError) as caught:
            await uploader.upload(request, Credentials("fixture-ak", "fixture-sk"))
    assert caught.value.result["error"]["code"] == "invalid_upload_address"
    assert caught.value.result["error"]["outcome_unknown"] is False
    assert len(calls) == 1 and calls[0].url.params["Action"] == "ApplyImageUpload"
    assert "fixture-private-image" not in str(caught.value)
