import pytest
from cryptography.fernet import Fernet

from mcp_server_sms.auth import subject_identity
from mcp_server_sms.config import Settings
from mcp_server_sms.core.api_protocol import ResolvedCredentials
from mcp_server_sms.runtime import Runtime


@pytest.fixture
def settings(tmp_path):
    return Settings(
        database_url="sqlite:///" + str(tmp_path / "state.db"),
        encryption_key=Fernet.generate_key().decode(),
        public_url="https://testserver",
        oidc_issuer="https://issuer.example",
        token_audience="sms-mcp",
        input_root=str(tmp_path),
    )


@pytest.fixture
def runtime(settings):
    return Runtime(settings)


@pytest.fixture
def owner():
    return subject_identity("https://issuer.example", "caller-one")


@pytest.fixture
def credentials():
    return ResolvedCredentials(
        "fixture-access-key", "fixture-secret-key", "fixture-session-token"
    )


class FakeSmsClient:
    def __init__(self):
        self._timeout = 1
        self.calls = []
        self.responses = {}

    def call(self, action, params, **kwargs):
        self.calls.append((action, params))
        result = self.responses.get(action)
        if callable(result):
            return result(params)
        if result is not None:
            return result
        defaults = {
            "GetAccountIdentRankForAgent": {
                key: False
                for key in [
                    "isOnlyTwoElement",
                    "isSkipOtherUse",
                    "needOtherUseCheck",
                    "operatorThreeElement",
                    "needOperatorImage",
                    "needOperatorMobile",
                    "responsibleThreeElement",
                    "needResponsibleImage",
                    "needResponsibleMobile",
                    "needBusinessCertificateImage",
                ]
            },
            "ListAllSmsProduct": {"businessName": "测试企业", "userType": "enterprise"},
            "ListSubAccountForAgent": {
                "List": [
                    {
                        "SubAccount": "group-one",
                        "SubAccountName": "测试消息组",
                        "Status": 1,
                    }
                ]
            },
            "GetSignatureIdentificationList": {
                "List": [{"id": 11, "purpose": 1, "auditStatus": 3, "usable": True}]
            },
            "ApplySignatureIdentificationForAgent": 123,
            "ApplySmsSignatureV2": {"applyId": 100, "status": 1},
        }
        return {
            "success": True,
            "request_id": "fixture-request",
            "result": defaults.get(action, {}),
            "error": None,
        }


@pytest.fixture
def sms(monkeypatch):
    from mcp_server_sms import runtime as runtime_module

    client = FakeSmsClient()
    monkeypatch.setattr(runtime_module, "SmsApiClient", lambda credentials: client)
    return client


@pytest.fixture
def ready_flow(runtime, owner, credentials, sms):
    opened = runtime.create_qualification_draft("测试资质", 1, owner, credentials)
    flow_id = opened["draftId"]
    with runtime.store.locked(flow_id, owner, "qualification") as (record, lease):
        state = record["data"]["state"]
        state.update(
            revision=7,
            materialName="测试资质",
            purpose=1,
            sameOperator=True,
            legalAcknowledged=True,
            baseSaved=True,
        )
        state["sections"] = {
            "business": {
                "businessCertificateType": 1,
                "businessCertificateName": "测试企业",
                "unifiedSocialCreditIdentifier": "911101080000000000",
                "legalPersonName": "测试法人",
                "businessCertificateValidityPeriodStart": "2020-01-01",
                "businessCertificateValidityPeriodEnd": "2099-12-31",
            },
            "operator": {
                "certificateType": 0,
                "personName": "测试经办人",
                "personIDCard": "110101199001010000",
                "personMobile": "",
            },
        }
        state["checks"] = {
            target: {
                "matched": True,
                "canContinue": True,
                "status": "0",
                "ticket": "fixture-ticket-" + target,
            }
            for target in ["business", "operator"]
        }
        runtime.store.save(flow_id, owner, record["data"], lease=lease)
    return flow_id
