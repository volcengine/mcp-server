# coding:utf-8
import json
from volcengine.base.Service import Service
from volcengine.const.Const import *
from volcengine.Policy import *
from volcengine.util.Util import *


api_info = {
    
}


class BaseTrait(Service):
    def __init__(self, param=None):
        if param is None:
            param = {}
        self.param = param
        region = param.get('region', REGION_CN_NORTH1)
        service_info_map= param.get('service_info_map', {})
        self.service_info = BaseTrait.get_service_info(region,service_info_map)
        self.api_info = BaseTrait.get_api_info()
        if param.get('ak', None) and param.get('sk', None):
            self.set_ak(param['ak'])
            self.set_sk(param['sk'])
        super(BaseTrait, self).__init__(self.service_info, self.api_info)

    @staticmethod
    def get_service_info(region, service_info_map):
        service_info = service_info_map.get(region, None)
        if not service_info:
            raise Exception('BaseService not support region %s' % region)
        return service_info

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
        