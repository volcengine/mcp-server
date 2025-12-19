# coding:utf-8
import json
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.Policy import *
from volcengine.util.Util import *
from volcengine.ServiceInfo import ServiceInfo
from volcengine.Credentials import Credentials

api_info = {}

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_SOCKET_TIMEOUT = 60


class BaseTrait(Service):
    def __init__(self, param=None):
        if param is None:
            param = {}
        self.param = param
        if "region" not in param:
            raise ValueError("region is not set")

        region = param.get("region", "")
        self.service_info = BaseTrait.get_service_info(region)
        self.api_info = BaseTrait.get_api_info()
        if param.get("ak", None) and param.get("sk", None):
            self.set_ak(param["ak"])
            self.set_sk(param["sk"])
        if param.get("session_token", None):
            self.set_session_token(param["session_token"])
        super(BaseTrait, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(
        region,
    ):
        return ServiceInfo(
            f"vke.{region}.volcengineapi.com",
            {"Accept": "application/json", "x-tt-mcp": "volc"},
            Credentials("", "", "vke", region),
            DEFAULT_CONNECT_TIMEOUT,
            DEFAULT_SOCKET_TIMEOUT,
            "https",
        )

    @staticmethod
    def get_api_info():
        return api_info

    def set_api_info(self, api_info):
        self.api_info = {**self.api_info, **api_info}
        return

    def mcp_get(self, action, params={}, doseq=0):
        res = self.get(action, params, doseq)
        if res == "":
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json

    def mcp_post(self, action, params={}, body={}):
        res = self.json(action, params, body)
        if res == "":
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json
