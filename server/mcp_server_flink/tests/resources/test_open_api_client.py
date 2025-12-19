import json
import logging

import pytest

from mcp_server_flink.utils.open_api_client import RequestParams, openapi_client_invoke, DEFAULT_OPENAPI_CONTEXT

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@pytest.mark.parametrize("method", ["GET"])
def test_openapi_client_invoke(monkeypatch, method):
    params = RequestParams(
        host="open.volcengineapi.com",
        body={},
        method=method,
        headers={},
        action="GetGMSUserToken",
        version="2021-06-01",
        content_type="text/plain",
    )

    # 执行 top_invoke
    resp = openapi_client_invoke(DEFAULT_OPENAPI_CONTEXT.credential, params)
    logger.info(f"invoke response: {json.dumps(resp)}")
