import os

from dotenv import load_dotenv

from mcp_server_tls.consts import *

class TlsConfig:

    ak: str
    sk: str
    region: str
    endpoint: str
    token: str
    project_id: str
    account_id: str
    enabled_tools: list

    def __init__(self):

        self.ak = os.getenv("VOLCENGINE_ACCESS_KEY") or os.getenv("VOLC_ACCESSKEY") or os.getenv("AK")
        self.sk = os.getenv("VOLCENGINE_SECRET_KEY") or os.getenv("VOLC_SECRETKEY") or os.getenv("SK")
        self.region = os.getenv("VOLCENGINE_REGION") or os.getenv("REGION")
        self.endpoint = os.getenv("VOLCENGINE_ENDPOINT") or os.getenv("ENDPOINT")
        self.token =os.getenv("VOLCENGINE_TOKEN") or os.getenv("TOKEN", "")
        self.account_id = os.getenv("VOLCENGINE_ACCOUNT_ID") or os.getenv("ACCOUNT_ID")

        self.project_id = os.getenv("TLS_PROJECT_ID") or os.getenv("PROJECT_ID")
        self.topic_id = os.getenv("TLS_TOPIC_ID") or os.getenv("TOPIC_ID")

        self.mcp_host = os.getenv("MCP_SERVER_HOST") or "127.0.0.1"
        self.mcp_port = os.getenv("MCP_SERVER_PORT") or os.getenv("MCP_PORT") or os.getenv("PORT") or 8000
        self.deploy_mode = os.getenv("MCP_DEPLOY_MODE") or os.getenv("DEPLOY_MODE") or DEPLOY_MODE_LOCAL
        self.enabled_tools = (os.getenv("MCP_ENABLED_TOOLS") or os.getenv("ENABLED_TOOLS") or "all").split(",")

        self._validate()

    def _validate(self):
        self._validate_deploy_mode()
        self._validate_deploy_mode_dependencies()

    def _validate_ak(self):
        if not self.ak:
            raise ValueError("environment variables AK is required")

    def _validate_sk(self):
        if not self.sk:
            raise ValueError("environment variables SK is required")

    def _validate_region(self):
        if not self.region:
            raise ValueError("environment variables REGION is required")

    def _validate_deploy_mode(self):
        if self.deploy_mode not in (DEPLOY_MODE_LOCAL, DEPLOY_MODE_REMOTE):
            raise ValueError("environment variables DEPLOY_MODE should be {} or {}".format(DEPLOY_MODE_LOCAL, DEPLOY_MODE_REMOTE))

    def _validate_endpoint(self):
        if not self.endpoint:
            raise ValueError("environment variables ENDPOINT is required")

        # fix Inspector bug
        self.endpoint = self.endpoint.replace(r'\x3a', ':')

        if not (self.endpoint.startswith("http://") or self.endpoint.startswith("https://")):
            raise ValueError(f"Invalid environment variables endpoint: {self.endpoint}. It must start with 'http://' or 'https://'.")

    def _validate_deploy_mode_dependencies(self):
        if self.deploy_mode == DEPLOY_MODE_LOCAL:
            self._validate_ak()
            self._validate_sk()
            self._validate_region()
            self._validate_endpoint()
        else:
            self._validate_deploy_mode_remote_should_not_exist()

    def _validate_deploy_mode_remote_should_not_exist(self):
        if self.ak:
            raise ValueError("environment variables VOLCENGINE_ACCESS_KEY should not be set")
        if self.sk:
            raise ValueError("environment variables VOLCENGINE_SECRET_KEY should not be set")
        if self.token:
            raise ValueError("environment variables VOLCENGINE_TOKEN should not be set")
        if self.project_id:
            raise ValueError("environment variables TLS_PROJECT_ID should not be set")
        if self.topic_id:
            raise ValueError("environment variables TLS_TOPIC_ID should not be set")
        if self.account_id:
            raise ValueError("environment variables VOLCENGINE_ACCOUNT_ID should not be set")
        if bool(self.region) ^ bool(self.endpoint):
            raise ValueError("environment variables VOLCENGINE_REGION and VOLCENGINE_ENDPOINT should be set togather")

load_dotenv()

TLS_CONFIG = TlsConfig()
