# coding=utf-8
import os
import base64
import json

from starlette.requests import Request
from mcp.server.fastmcp import FastMCP

from base.base_service import BaseService

from .config import api_info


class VkeAPI(BaseService):

    def __init__(self, mcp: FastMCP, region: str = "cn-beijing"):
        ak, sk, session_token = "", "", ""

        if os.getenv("MCP_SERVER_MODE") == "remote":
            raw_request: Request = mcp.get_context().request_context.request
            auth = raw_request.headers.get("authorization", None)
            if auth is None:
                raise ValueError("missing authorization info")

            if " " in auth:
                # Truncate the "Bearer " prefix
                _, base64_data = auth.split(" ", 1)
            else:
                base64_data = auth

            try:
                decoded_str = base64.b64decode(base64_data).decode("utf-8")
                data = json.loads(decoded_str)

                ak = data.get("AccessKeyId")
                sk = data.get("SecretAccessKey")
                session_token = data.get("SessionToken")

            except Exception as e:
                raise ValueError(f"decode authorization info error: {e}")
        else:
            if "VOLCENGINE_ACCESS_KEY" not in os.environ:
                raise ValueError("VOLCENGINE_ACCESS_KEY is not set")
            if "VOLCENGINE_SECRET_KEY" not in os.environ:
                raise ValueError("VOLCENGINE_SECRET_KEY is not set")

            ak = os.getenv("VOLCENGINE_ACCESS_KEY")
            sk = os.getenv("VOLCENGINE_SECRET_KEY")
            session_token = os.getenv("VOLCENGINE_SESSION_TOKEN", "")

        super().__init__(
            region=region,
            ak=ak,
            sk=sk,
            session_token=session_token,
        )
        self.set_api_info(api_info)
