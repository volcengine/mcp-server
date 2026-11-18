import httpx
import pytest

from mcp_server_sms.auth import Credentials
from mcp_server_sms.batch_checks import BatchTrafficCheck, check_batch_traffic
from mcp_server_sms.client import SmsClient
from mcp_server_sms.protocol import SmsAPIError
from mcp_server_sms.qualification_checks import check_enterprise
from mcp_server_sms.service_onboarding import _submit_service_onboarding


@pytest.fixture
def backend_failure():
    payload = {"ResponseMetadata": {
        "RequestId": "original-request", "Error": {
            "Code": "1999", "Message": " 原始后端错误\n业务结果请查询 ", "Details": {"reason": "原始字段"},
        },
    }}
    return SmsClient.decode("ThreeElementEnterpriseCheckForAgent", httpx.Response(503, json=payload), Credentials("fixture-ak", "fixture-sk"))


async def test_manual_review_option_keeps_original_backend_failure(backend_failure):
    async def call(*_):
        raise SmsAPIError(backend_failure)

    result = await check_enterprise(call, {}, offer_manual_review=True)
    assert result["result"]["manualReview"] is True
    assert result["result"]["failure"] == backend_failure


async def test_manual_review_option_keeps_original_transport_error():
    async def call(action, _params):
        def fail(request):
            raise httpx.ConnectTimeout("connection timed out", request=request)
        async with SmsClient(transport=httpx.MockTransport(fail)) as client:
            return await client.call(action, {}, Credentials("fixture-ak", "fixture-sk"))

    result = await check_enterprise(call, {}, offer_manual_review=True)
    assert result["result"]["manualReview"] is True
    assert result["result"]["failure"]["error"] == {
        "code": "ConnectTimeout", "message": "connection timed out", "source": "transport",
    }


@pytest.mark.parametrize("failure_stage", ["activation", "refresh"])
async def test_service_flow_keeps_backend_errors_without_claiming_rejection(backend_failure, failure_stage):
    async def call(action, _params):
        if action == "ConfirmProtocolDocument":
            return {"result": {"success": [1], "fail": []}, "request_id": "agreement-request"}
        if action == "ActivateSmsProductInOneStep" and failure_stage == "refresh":
            return {"result": {"list": [{"product": "sms", "orderStatus": 1}]}, "request_id": "activation-request"}
        raise SmsAPIError(backend_failure)

    result = await _submit_service_onboarding(call, Credentials("fixture-ak", "fixture-sk"), {
        "status": "activation_required", "protocols": [{"id": 1}],
    })
    assert result["failure"] == backend_failure
    assert result["status"] == ("activation_error" if failure_stage == "activation" else "activation_pending")


@pytest.mark.parametrize("failure_action", ["ListSecondTemplate", "CheckTrafficDrivingExist"])
async def test_batch_traffic_summary_keeps_each_original_api_failure(backend_failure, failure_action):
    async def call(action, _params):
        if action == failure_action:
            raise SmsAPIError(backend_failure)
        return {"result": {"list": [{"TemplateId": "template", "useVolcLink": False}]}, "request_id": "template-request"}

    result = await check_batch_traffic(call, BatchTrafficCheck(
        sub_account="group", signature="签名", template_id="template", content="演示通知",
    ), data=b"phone\n13800000000\n", columns=["phone"])
    assert result["failures"] == [backend_failure]
    assert result["checkedRows"] == 0
    assert result["failedRows"] == (1 if failure_action == "CheckTrafficDrivingExist" else 0)
