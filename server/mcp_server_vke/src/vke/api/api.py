# coding=utf-8
import os
import base64
import json

from starlette.requests import Request
from mcp.server.fastmcp import FastMCP

from base.base_service import BaseService

from .config import api_info

VEFAAS_IAM_CRIDENTIAL_PATH = "/var/run/secrets/iam/credential"


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
        elif os.path.exists(VEFAAS_IAM_CRIDENTIAL_PATH):
            with open(VEFAAS_IAM_CRIDENTIAL_PATH, "r") as f:
                cred_dict = json.load(f)
                ak = cred_dict["access_key_id"]
                sk = cred_dict["secret_access_key"]
                session_token = cred_dict.get("session_token", "")
        else:
            ak = os.getenv("VOLCENGINE_ACCESS_KEY")
            sk = os.getenv("VOLCENGINE_SECRET_KEY")
            session_token = os.getenv("VOLCENGINE_SESSION_TOKEN", "")

        if not ak:
            raise ValueError("access key is not provided")
        if not sk:
            raise ValueError("secret key is not provided")

        super().__init__(
            region=region,
            ak=ak,
            sk=sk,
            session_token=session_token,
        )
        self.set_api_info(api_info)
