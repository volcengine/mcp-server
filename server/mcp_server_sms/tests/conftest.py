import base64
import json

import httpx
import pytest
from mcp.types import CallToolResult, ListToolsResult
from starlette.testclient import TestClient

from mcp_server_sms.client import SmsClient
from mcp_server_sms.server import build_server, create_http_app


@pytest.fixture
def credentials_env(monkeypatch):
    monkeypatch.setenv("VOLCENGINE_ACCESS_KEY", "fixture-access-key-one")
    monkeypatch.setenv("VOLCENGINE_SECRET_KEY", "fixture-secret-key-one")
    monkeypatch.setenv("VOLCENGINE_SESSION_TOKEN", "fixture-session-token-one")


@pytest.fixture
def api_calls():
    calls = []

    def respond(request):
        calls.append(request)
        action = request.url.params["Action"]
        results = {
            "SendSmsForAgent": {"MessageIds": ["fixture-message"]},
            "ApplySmsSignatureV2": {"applyId": "fixture-signature", "status": 1},
            "ApplySmsTemplateV2": {"templateId": "fixture-template", "status": 1},
            "ApplySignatureIdentificationForAgent": 123,
            "ThreeElementEnterpriseCheckForAgent": {
                "status": 0,
                "ticket": "upstream-enterprise-ticket",
            },
            "ThreeElementPersonCheckForAgent": {"status": 0, "ticket": "upstream-person-ticket"},
            "SendSmsVerifyCodeByMobile": {"messageId": "fixture-verification-message"},
            "CheckSmsVerifyCodeByMobile": {"status": 2},
            "SetBatchTask": {"taskId": "fixture-task", "totalCount": 1, "dupCount": 0},
            "GetUploadTosURL": {
                "file": "fixture.csv",
                "url": "https://upload.example/fixture.csv?signature=opaque",
            },
            "ConsentBatchTask": None,
            "DeleteBatchTask": None,
        }
        return httpx.Response(
            200,
            json={
                "ResponseMetadata": {"RequestId": "fixture-request"},
                "Result": results.get(action, {"List": [], "Total": 0}),
            },
        )

    return calls, SmsClient(transport=httpx.MockTransport(respond))


def auth_header(suffix):
    raw = {
        "AccessKeyId": "fixture-access-key-" + suffix,
        "SecretAccessKey": "fixture-secret-key-" + suffix,
        "SessionToken": "fixture-token-" + suffix,
    }
    return "Bearer " + base64.b64encode(json.dumps(raw).encode()).decode()


def rpc(client, method, *, token=None, params=None):
    arguments = {
        "_meta": {
            "io.modelcontextprotocol/protocolVersion": "2026-07-28",
            "io.modelcontextprotocol/clientInfo": {"name": "sms-acceptance", "version": "1"},
            "io.modelcontextprotocol/clientCapabilities": {},
        },
        **(params or {}),
    }
    headers = {
        "Accept": "application/json, text/event-stream",
        "MCP-Protocol-Version": "2026-07-28",
        "MCP-Method": method,
    }
    if token:
        headers["Authorization"] = token
    if params and "name" in params:
        headers["Mcp-Name"] = params["name"]
    return client.post(
        "/mcp",
        headers=headers,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": arguments},
    )


@pytest.fixture
def mcp(api_calls):
    # Exercise the actual protocol boundary: direct MCPServer.call_tool calls
    # have no request Context and do not convert ToolError into wire results.
    with TestClient(
        create_http_app(build_server(api_calls[1]), "https://testserver"),
        base_url="https://testserver",
    ) as http:

        class ToolClient:
            async def call_tool(self, name, arguments):
                response = rpc(
                    http,
                    "tools/call",
                    token=auth_header("one"),
                    params={"name": name, "arguments": arguments},
                )
                assert response.status_code == 200, response.text
                return CallToolResult.model_validate(response.json()["result"])

            async def list_tools(self):
                response = rpc(http, "tools/list", token=auth_header("one"))
                assert response.status_code == 200, response.text
                return ListToolsResult.model_validate(response.json()["result"]).tools

        yield ToolClient()


def payload(result):
    if result.structured_content is not None:
        return result.structured_content
    return json.loads("\n".join(item.text for item in result.content if item.type == "text"))


@pytest.fixture
def qualification_request():
    person = {"certificateType": 0, "personName": "示例经办人", "personIDCard": "fixture-id"}
    return {
        "purpose": 1,
        "materialName": "接口测试资质",
        "sameOperator": True,
        "businessInfo": {
            "businessCertificateType": 1,
            "businessCertificateName": "示例企业",
            "unifiedSocialCreditIdentifier": "fixture-enterprise-id",
            "legalPersonName": "示例法人",
            "businessCertificateValidityPeriodStart": "2020-01-01",
            "businessCertificateValidityPeriodEnd": "长期",
            "businessCertificate": {"fileType": 1, "fileContent": "existing/material-uri"},
        },
        "operatorPerson": person,
        "responsiblePersonInfo": person,
        "businessCheckTicket": "upstream-enterprise-ticket",
        "operatorCheckTicket": "upstream-person-ticket",
        "responsibleCheckTicket": "upstream-person-ticket",
    }
