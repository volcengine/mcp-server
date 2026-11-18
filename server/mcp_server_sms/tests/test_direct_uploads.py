"""直传只交换小参数；实际文件校验及凭据边界仍在服务端。"""

import asyncio
import copy
import gzip
import hashlib
import json

import httpx
import pytest
from conftest import auth_header, rpc
from starlette.testclient import TestClient
from test_apps import image_responder, material_api

from mcp_server_sms.auth import Credentials
from mcp_server_sms.client import SmsClient
from mcp_server_sms.server import build_server, create_http_app
from mcp_server_sms.upload_models import (
    MaterialUploadConfirmation,
    MaterialUploadMetadata,
    RecipientsUploadConfirmation,
    RecipientsUploadMetadata,
    SmsRequestError,
)
from mcp_server_sms.uploads import FileUploader


@pytest.mark.parametrize("size", [1, 7314599, 10485760])
def test_material_plan_is_private_small_and_has_no_file_body(size, caplog):
    calls = []
    api = SmsClient(transport=httpx.MockTransport(material_api))
    uploader = FileUploader(api, transport=httpx.MockTransport(lambda r: image_responder(r, calls)))
    with TestClient(create_http_app(build_server(api, uploader), public_url="https://testserver")) as http:
        arguments = {"request": {"name": "proof.png", "category": "business", "size": size, "crc32": "abcdef12"}}
        plan_result = rpc(http, "tools/call", token=auth_header("one"), params={
            "name": "prepare_material_upload", "arguments": arguments,
        }).json()["result"]
        assert not plan_result["isError"]
        plan = plan_result["_meta"]["sms/form"]["result"]
        assert plan["upload"]["method"] == "PUT"
        assert plan["upload"]["headers"]["Content-CRC32"] == "abcdef12"
        assert len(calls) == 1  # MCP 只申请地址，不传文件字节。
        confirmation_args = {"request": plan["confirmation"]}
        completed = rpc(http, "tools/call", token=auth_header("one"), params={
            "name": "complete_material_upload", "arguments": confirmation_args,
        }).json()["result"]
    assert completed["_meta"]["sms/form"]["result"]["fileContent"] == "bucket/material.png"
    assert len(calls) == 2 and calls[-1].url.params["Action"] == "CommitImageUpload"
    assert len(json.dumps(arguments)) < 32000 and len(json.dumps(confirmation_args)) < 32000
    assert "image-secret" not in json.dumps(plan_result)
    assert "image-access" not in json.dumps(plan_result)
    assert "image-token" not in json.dumps(plan_result)
    for secret in ["fixture-upload-auth", "fixture-session", "bucket/material.png"]:
        assert secret not in json.dumps(plan_result["content"])
        assert secret not in json.dumps(plan_result["structuredContent"])
        assert secret not in caplog.text


@pytest.mark.parametrize("field,value", [("name", "changed.png"), ("uri", "another/file"), ("session_key", "other")])
async def test_material_confirmation_rejects_tampering_before_downstream(field, value):
    calls = []
    credentials = Credentials("ak", "sk", "session")
    async with SmsClient(transport=httpx.MockTransport(material_api)) as api, FileUploader(
        api, transport=httpx.MockTransport(lambda r: image_responder(r, calls))
    ) as uploader:
        plan = await uploader.prepare_material(MaterialUploadMetadata(
            name="proof.png", category="business", size=10, crc32="00000000"
        ), credentials)
        plan["confirmation"]["context"][field] = value
        with pytest.raises(SmsRequestError) as error:
            await uploader.complete_material(MaterialUploadConfirmation.model_validate(plan["confirmation"]), credentials)
        assert error.value.result["error"]["code"] == "upload_authorization_changed"
        assert len(calls) == 1


async def test_confirmation_survives_instance_change_but_rejects_other_credentials_and_expiry(monkeypatch):
    calls = []
    credentials = Credentials("ak", "sk", "session")
    async with SmsClient(transport=httpx.MockTransport(material_api)) as api, FileUploader(
        api, transport=httpx.MockTransport(lambda r: image_responder(r, calls))
    ) as first, FileUploader(api, transport=httpx.MockTransport(lambda r: image_responder(r, calls))) as second:
        plan = await first.prepare_material(MaterialUploadMetadata(
            name="proof.png", category="business", size=10, crc32="00000000"
        ), credentials)
        receipt = MaterialUploadConfirmation.model_validate(plan["confirmation"])
        with pytest.raises(SmsRequestError, match="上传授权无效"):
            await second.complete_material(receipt, Credentials("other", "sk", "session"))
        assert (await second.complete_material(receipt, credentials))["fileContent"] == "bucket/material.png"
        monkeypatch.setattr("mcp_server_sms.uploads.time", lambda: receipt.context.expires_at)
        with pytest.raises(SmsRequestError, match="上传授权已过期"):
            await second.complete_material(receipt, credentials)
        assert len(calls) == 2


def recipients_stack(data, *, download_url="https://bucket.tos-cn-beijing.volces.com/fixture.csv?signature=read", downloaded=None, download_headers=None, reads=None):
    calls = []

    def api_response(request):
        action = request.url.params["Action"]
        calls.append((action, request))
        results = {
            "GetUploadTosURL": {"file": "fixture.csv", "url": "https://bucket.tos-cn-beijing.volces.com/fixture.csv?signature=put"},
            "GetFilePublicTosURL": {"fileName": "fixture.csv", "url": download_url},
            "ListSecondTemplate": {"List": [{"TemplateId": "template", "useVolcLink": False}]},
            "CheckTrafficDrivingExist": {"list": [
                {"isExist": True, "paramType": 2, "id": 12, "content": "https://example.com"},
            ]},
        }
        assert action in results, action
        return httpx.Response(200, json={"Result": results[action]})

    class DownloadStream(httpx.AsyncByteStream):
        async def __aiter__(self):
            if reads is not None:
                reads.append("read")
            yield data if downloaded is None else downloaded

    def download(request):
        calls.append(("Download", request))
        assert request.method == "GET" and "authorization" not in request.headers
        return httpx.Response(200, stream=DownloadStream(), headers=download_headers)

    api = SmsClient(transport=httpx.MockTransport(api_response))
    uploader = FileUploader(api, transport=httpx.MockTransport(download))
    metadata = RecipientsUploadMetadata(
        name="list.csv", size=len(data), sha256=hashlib.sha256(data).hexdigest(),
        sub_account="group", template_id="template",
    )
    return api, uploader, metadata, calls


async def test_recipients_are_read_back_and_validated_by_server_without_transmitting_base64():
    data = b"phone,url\n" + b"13800000000,https://example.com/CaseSensitive\n" * 5000
    api, uploader, metadata, calls = recipients_stack(data)
    credentials = Credentials("ak", "sk", "session")
    async with api, uploader:
        plan = await uploader.prepare_recipients(metadata, credentials)
        receipt = RecipientsUploadConfirmation.model_validate(plan["confirmation"])
        async with uploader.validated_recipients(receipt, credentials, ["phone", "url"]) as (received, result):
            assert received == data
    assert result["totalCount"] == 5000 and result["dupCount"] == 4999
    assert result["samples"][0]["params"]["url"] == "https://example.com/CaseSensitive"
    assert result["samples"][0]["phone"] == "138****0000"
    assert [name for name, _ in calls] == ["GetUploadTosURL", "GetFilePublicTosURL", "Download"]
    assert len(json.dumps(metadata.model_dump())) < 32000
    assert len(json.dumps(receipt.model_dump())) < 32000


@pytest.mark.parametrize("data", [b"wrong,url\n13800000000,x\n", b"phone,url\ninvalid,x\n", b"phone,url\n"])
async def test_direct_recipient_validation_rejects_invalid_csv(data):
    api, uploader, metadata, _ = recipients_stack(data)
    credentials = Credentials("ak", "sk")
    async with api, uploader:
        plan = await uploader.prepare_recipients(metadata, credentials)
        with pytest.raises(SmsRequestError) as error:
            async with uploader.validated_recipients(RecipientsUploadConfirmation.model_validate(plan["confirmation"]), credentials, ["phone", "url"]):
                pytest.fail("无效名单不得进入后续检查")
    assert error.value.result["error"]["code"] == "invalid_csv"


@pytest.mark.parametrize("columns", [[], ["name", "url"], ["phone", "phone"], ["phone", ""]])
async def test_reused_columns_must_be_valid_before_file_download(columns):
    api, uploader, metadata, calls = recipients_stack(b"phone,url\n13800000000,x\n")
    credentials = Credentials("ak", "sk")
    async with api, uploader:
        plan = await uploader.prepare_recipients(metadata, credentials)
        receipt = RecipientsUploadConfirmation.model_validate(plan["confirmation"])
        with pytest.raises(SmsRequestError) as error:
            async with uploader.validated_recipients(receipt, credentials, columns):
                pytest.fail("不完整列定义不能进入名单检查")
        assert error.value.result["error"]["code"] == "invalid_csv_template"
        assert [name for name, _ in calls] == ["GetUploadTosURL"]


@pytest.mark.parametrize("changed,code", [(b"x", "file_content_changed"), (b"x" * 1000, "invalid_file_size")])
async def test_recipients_readback_rejects_changed_or_oversized_bytes(changed, code):
    api, uploader, metadata, calls = recipients_stack(b"phone,url\n13800000000,x\n", downloaded=changed)
    credentials = Credentials("ak", "sk")
    async with api, uploader:
        plan = await uploader.prepare_recipients(metadata, credentials)
        with pytest.raises(SmsRequestError) as error:
            async with uploader.validated_recipients(RecipientsUploadConfirmation.model_validate(plan["confirmation"]), credentials, ["phone", "url"]):
                pytest.fail("无效名单不得进入后续检查")
    assert error.value.result["error"]["code"] == code
    assert "TemplateUploadDemoForAgent" not in [name for name, _ in calls]


async def test_recipients_signed_reference_and_download_domain_are_enforced():
    api, uploader, metadata, calls = recipients_stack(b"phone,url\n13800000000,x\n", download_url="https://example.com/private.csv")
    credentials = Credentials("ak", "sk")
    async with api, uploader:
        plan = await uploader.prepare_recipients(metadata, credentials)
        tampered = copy.deepcopy(plan["confirmation"])
        tampered["context"]["file"] = "another-account.csv"
        with pytest.raises(SmsRequestError) as error:
            async with uploader.read_recipients(RecipientsUploadConfirmation.model_validate(tampered), credentials):
                pytest.fail("篡改的引用不得进入文件读取")
        assert error.value.result["error"]["code"] == "upload_authorization_changed"
        assert len(calls) == 1
        with pytest.raises(SmsRequestError) as error:
            async with uploader.read_recipients(RecipientsUploadConfirmation.model_validate(plan["confirmation"]), credentials):
                pytest.fail("非受信地址不得进入文件读取")
        assert error.value.result["error"]["code"] == "invalid_upload_url"
        assert not any(name == "Download" for name, _ in calls)


def test_batch_traffic_uses_verified_reference_and_preserves_row_coverage():
    data = b"phone,url\n" + b"13800000000,https://example.com/CaseSensitive\n" * 1000
    api, uploader, metadata, calls = recipients_stack(data)
    with TestClient(create_http_app(build_server(api, uploader), public_url="https://testserver")) as http:
        plan = rpc(http, "tools/call", token=auth_header("one"), params={
            "name": "prepare_recipients_upload", "arguments": {"request": metadata.model_dump()},
        }).json()["result"]["_meta"]["sms/form"]["result"]
        request = {"sub_account": "group", "signature": "签名", "template_id": "template", "content": "活动 ${url}"}
        result = rpc(http, "tools/call", token=auth_header("one"), params={
            "name": "complete_recipients_upload", "arguments": {"request": plan["confirmation"], "columns": ["phone", "url"], "traffic": request},
        }).json()["result"]
        assert not result["isError"]
        assert result["_meta"]["sms/form"]["result"]["trafficReport"]["checkedRows"] == 1000
        assert result["_meta"]["sms/form"]["result"]["totalCount"] == 1000
        assert [name for name, _ in calls].count("Download") == 1
        assert "TemplateUploadDemoForAgent" not in [name for name, _ in calls]
        assert "ListBatchTemplatesForAgent" not in [name for name, _ in calls]
        assert "example.com/CaseSensitive" not in json.dumps(result["content"])
        assert "example.com/CaseSensitive" not in json.dumps(result["structuredContent"])
        assert len(json.dumps(request)) < 32000
        assert len([name for name, _ in calls if name == "CheckTrafficDrivingExist"]) == 1
        request["sub_account"] = "another-group"
        rejected = rpc(http, "tools/call", token=auth_header("one"), params={
            "name": "complete_recipients_upload", "arguments": {"request": plan["confirmation"], "columns": ["phone", "url"], "traffic": request},
        }).json()["result"]
        assert rejected["isError"]
        assert rejected["structuredContent"]["error"]["code"] == "uploaded_selection_changed"
        assert [name for name, _ in calls].count("Download") == 1


async def test_readback_capacity_is_held_until_consumption_finishes():
    data = b"phone,url\n13800000000,x\n"
    api, uploader, metadata, _ = recipients_stack(data)
    credentials = Credentials("ak", "sk")
    release, ready = asyncio.Event(), asyncio.Event()
    entered = 0
    async with api, uploader:
        plan = await uploader.prepare_recipients(metadata, credentials)
        receipt = RecipientsUploadConfirmation.model_validate(plan["confirmation"])

        async def hold():
            nonlocal entered
            async with uploader.read_recipients(receipt, credentials) as received:
                assert received == data
                entered += 1
                if entered == 2:
                    ready.set()
                await release.wait()

        tasks = [asyncio.create_task(hold()) for _ in range(2)]
        try:
            await asyncio.wait_for(ready.wait(), timeout=3)
            with pytest.raises(SmsRequestError) as error:
                async with uploader.read_recipients(receipt, credentials):
                    pytest.fail("满载请求不能继续读取")
            assert error.value.result["error"]["code"] == "upload_busy"
        finally:
            release.set()
            await asyncio.gather(*tasks)
        async with uploader.read_recipients(receipt, credentials) as received:
            assert received == data


async def test_compressed_readback_is_rejected_before_reading_or_decompressing():
    data = b"phone,url\n13800000000,x\n"
    compressed = gzip.compress(b"x" * (8 * 1024 * 1024))
    reads = []
    api, uploader, metadata, _ = recipients_stack(
        data, downloaded=compressed, download_headers={"Content-Encoding": "gzip"}, reads=reads,
    )
    credentials = Credentials("ak", "sk")
    async with api, uploader:
        plan = await uploader.prepare_recipients(metadata, credentials)
        receipt = RecipientsUploadConfirmation.model_validate(plan["confirmation"])
        with pytest.raises(SmsRequestError) as error:
            async with uploader.validated_recipients(receipt, credentials, ["phone", "url"]):
                pytest.fail("无效名单不得进入后续检查")
        assert error.value.result["error"]["code"] == "unexpected_content_encoding"
        assert reads == []
