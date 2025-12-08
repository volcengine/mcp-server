from volcengine.vod.VodService import VodService
import json
import os
from typing import Dict, Any
from src.base.credential import get_volcengine_credentials_base

class BaseService(VodService):

    def __init__(self):
        if os.getenv("VOLCENGINE_REGION") is None:
            region = "cn-north-1"
        else:
            region = os.getenv("VOLCENGINE_REGION")

        super().__init__(region=region)
        credentials = get_volcengine_credentials_base()
        self.set_ak(credentials.access_key_id)
        self.set_sk(credentials.secret_access_key)
        self.set_session_token(credentials.session_token)
        self.service_info.header["x-tt-mcp"] = 'volc'
        self.mcp_state = {}
        
    @staticmethod
    def get_api_info():
        return api_info
    def set_api_info(self, api_info):
        self.api_info = {**self.api_info, **api_info}
        return
        
    def mcp_get(self, action, params={}, doseq=0):
        res = self.get(action, params, doseq)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json

    def mcp_post(self, action, params={}, body={}):
        res = self.json(action, params, body)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json
    def set_state(self, state: Dict[str, Any] = {}):
        self.mcp_state = {
            **self.mcp_state,
            **state
        }
    def get_state(self):
        return self.mcp_state
