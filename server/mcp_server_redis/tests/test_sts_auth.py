import base64
import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from mcp_server_redis import server as redis_server


def _make_auth_header(payload: dict) -> str:
    return "Bearer " + base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")


class RedisServerSTSAuthTests(unittest.TestCase):
    def setUp(self) -> None:
        redis_server._REDIS_CLIENT_CACHE.clear()
        redis_server._VPC_CLIENT_CACHE.clear()

    def test_parse_authorization_payload_returns_sts_credentials(self):
        header = _make_auth_header(
            {
                "AccessKeyId": "sts-ak",
                "SecretAccessKey": "sts-sk",
                "SessionToken": "sts-token",
                "CurrentTime": "2026-05-28T10:00:00+08:00",
                "ExpiredTime": "2026-05-28T11:00:00+08:00",
                "Region": "cn-beijing",
            }
        )

        credentials = redis_server._parse_authorization_payload(header)

        self.assertEqual(
            credentials,
            {
                "access_key": "sts-ak",
                "secret_key": "sts-sk",
                "session_token": "sts-token",
                "region": "cn-beijing",
            },
        )

    def test_parse_authorization_payload_rejects_expired_sts(self):
        header = _make_auth_header(
            {
                "AccessKeyId": "sts-ak",
                "SecretAccessKey": "sts-sk",
                "SessionToken": "sts-token",
                "CurrentTime": "2026-05-28T12:00:00+08:00",
                "ExpiredTime": "2026-05-28T11:00:00+08:00",
                "Region": "cn-beijing",
            }
        )

        with self.assertRaisesRegex(ValueError, "STS token is expired"):
            redis_server._parse_authorization_payload(header)

    def test_resolve_credentials_prefers_request_authorization(self):
        header = _make_auth_header(
            {
                "AccessKeyId": "header-ak",
                "SecretAccessKey": "header-sk",
                "SessionToken": "header-token",
                "Region": "cn-guangzhou",
            }
        )
        ctx = SimpleNamespace(
            request_context=SimpleNamespace(
                request=SimpleNamespace(headers={"authorization": header})
            )
        )

        with patch.object(redis_server.mcp_server, "get_context", return_value=ctx), patch.dict(
            os.environ,
            {
                "VOLCENGINE_ACCESS_KEY": "env-ak",
                "VOLCENGINE_SECRET_KEY": "env-sk",
                "VOLCENGINE_SESSION_TOKEN": "env-token",
                "VOLCENGINE_REGION": "cn-beijing",
            },
            clear=True,
        ):
            credentials = redis_server._resolve_volcengine_credentials()

        self.assertEqual(credentials["access_key"], "header-ak")
        self.assertEqual(credentials["secret_key"], "header-sk")
        self.assertEqual(credentials["session_token"], "header-token")
        self.assertEqual(credentials["region"], "cn-guangzhou")

    def test_resolve_credentials_supports_env_session_token(self):
        with patch.object(redis_server.mcp_server, "get_context", side_effect=RuntimeError("no context")), patch.dict(
            os.environ,
            {
                "VOLCENGINE_ACCESS_KEY": "env-ak",
                "VOLCENGINE_SECRET_KEY": "env-sk",
                "VOLCENGINE_SESSION_TOKEN": "env-token",
                "VOLCENGINE_REGION": "cn-beijing",
            },
            clear=True,
        ):
            credentials = redis_server._resolve_volcengine_credentials()

        self.assertEqual(credentials["access_key"], "env-ak")
        self.assertEqual(credentials["secret_key"], "env-sk")
        self.assertEqual(credentials["session_token"], "env-token")
        self.assertEqual(credentials["region"], "cn-beijing")

    def test_resolve_credentials_ignores_legacy_env_session_token_name(self):
        with patch.object(redis_server.mcp_server, "get_context", side_effect=RuntimeError("no context")), patch.dict(
            os.environ,
            {
                "VOLCENGINE_ACCESS_KEY": "env-ak",
                "VOLCENGINE_SECRET_KEY": "env-sk",
                "VOLCENGINE_ACCESS_SESSION_TOKEN": "legacy-token",
                "VOLCENGINE_REGION": "cn-beijing",
            },
            clear=True,
        ):
            credentials = redis_server._resolve_volcengine_credentials()

        self.assertEqual(credentials["access_key"], "env-ak")
        self.assertEqual(credentials["secret_key"], "env-sk")
        self.assertEqual(credentials["session_token"], "")
        self.assertEqual(credentials["region"], "cn-beijing")

    def test_get_redis_client_injects_session_token_into_sdk(self):
        with patch.object(redis_server.mcp_server, "get_context", side_effect=RuntimeError("no context")), patch.dict(
            os.environ,
            {
                "VOLCENGINE_ACCESS_KEY": "env-ak",
                "VOLCENGINE_SECRET_KEY": "env-sk",
                "VOLCENGINE_SESSION_TOKEN": "env-token",
                "VOLCENGINE_REGION": "cn-beijing",
                "VOLCENGINE_ENDPOINT": "redis.custom.endpoint",
            },
            clear=True,
        ), patch.object(redis_server, "RedisSDK") as redis_sdk_cls:
            instance = object()
            redis_sdk_cls.return_value = instance

            client = redis_server._get_redis_client()

        self.assertIs(client, instance)
        redis_sdk_cls.assert_called_once_with(
            region="cn-beijing",
            host="redis.custom.endpoint",
            ak="env-ak",
            sk="env-sk",
            session_token="env-token",
        )

    def test_sdk_proxy_uses_request_region_when_dispatching(self):
        fake_client = Mock()
        fake_client.describe_regions.return_value = {"ok": True}

        with patch.object(redis_server, "_get_redis_client", return_value=fake_client) as get_client:
            result = redis_server.redis_resource.describe_regions({"region_id": "cn-shanghai"})

        self.assertEqual(result, {"ok": True})
        get_client.assert_called_once_with("cn-shanghai")
        fake_client.describe_regions.assert_called_once_with({"region_id": "cn-shanghai"})


if __name__ == "__main__":
    unittest.main()
