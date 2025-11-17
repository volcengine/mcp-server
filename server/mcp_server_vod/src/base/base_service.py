from volcengine.vod.VodService import VodService
import json
import os


class BaseService(VodService):

    def __init__(self):
        if os.getenv("VOLCENGINE_REGION") is None:
            region = "cn-north-1"
        else:
            region = os.getenv("VOLCENGINE_REGION")

        super().__init__(region=region)
        self.set_ak(os.getenv("VOLCENGINE_ACCESS_KEY"))
        self.set_sk(os.getenv("VOLCENGINE_SECRET_KEY"))
        self.service_info.header["x-tt-mcp"] = 'volc'
        self.service_info.header["x-tt-env"] = 'ppe_volcengine'
        self.service_info.header["x-use-ppe"] = '1'
        self.service_info.header["x-volc-env"] = 'ppe_vedit_gateway'
        print(os.getenv("VOLCENGINE_ACCESS_KEY"), os.getenv("VOLCENGINE_SECRET_KEY"))
        
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
