import unittest
from unittest.mock import patch

import mcp_server_apmplus.server as server
from mcp_server_apmplus.config import *

AK = ""
SK = ""


class TestModels(unittest.IsolatedAsyncioTestCase):
    async def test_list_alert_rule(self):
        with patch.dict(
            os.environ,
            {
                ENV_VOLCENGINE_ACCESS_KEY: AK,
                ENV_VOLCENGINE_SECRET_KEY: SK,
                ENV_MCP_DEV_MODE: "True",
            },
            clear=False,
        ):
            resp = await server.apmplus_server_list_alert_rule(
                keyword="test",
            )
            print(resp)

    async def test_list_notify_group(self):
        with patch.dict(
            os.environ,
            {
                ENV_VOLCENGINE_ACCESS_KEY: AK,
                ENV_VOLCENGINE_SECRET_KEY: SK,
                ENV_MCP_DEV_MODE: "True",
            },
            clear=False,
        ):
            resp = await server.apmplus_server_list_notify_group(
                keyword="test",
            )
            print(resp)

    async def test_query_metrics(self):
        with patch.dict(
            os.environ,
            {
                ENV_VOLCENGINE_ACCESS_KEY: AK,
                ENV_VOLCENGINE_SECRET_KEY: SK,
                ENV_MCP_DEV_MODE: "True",
            },
            clear=False,
        ):
            resp = await server.apmplus_server_query_metrics(
                query="histogram_quantile(0.99, sum(rate(gen_ai_client_operation_duration_bucket{}[5m])) by (le))",
                start_time=1746777063,
                end_time=1746780663,
            )
            print(resp)

    async def test_apmplus_server_get_trace_detail(self):
        with patch.dict(
            os.environ,
            {
                ENV_VOLCENGINE_ACCESS_KEY: AK,
                ENV_VOLCENGINE_SECRET_KEY: SK,
                ENV_MCP_DEV_MODE: "True",
            },
            clear=False,
        ):
            init_config()
            resp = await server.apmplus_server_get_trace_detail(
                trace_id="test",
                suggest_time=1746777063,
            )
            print(resp)

    async def test_apmplus_server_list_span(self):
        with patch.dict(
            os.environ,
            {
                ENV_VOLCENGINE_ACCESS_KEY: AK,
                ENV_VOLCENGINE_SECRET_KEY: SK,
                ENV_MCP_DEV_MODE: "True",
            },
            clear=False,
        ):
            init_config()
            resp = await server.apmplus_server_list_span(
                start_time=1746777063,
                end_time=1746780663,
            )
            print(resp)


def init_config():
    config = load_config()
    server.config = volcenginesdkcore.Configuration.set_default(
        config.to_volc_configuration()
    )


if __name__ == "__main__":
    unittest.main()
