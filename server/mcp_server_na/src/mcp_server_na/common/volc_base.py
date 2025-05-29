import json

from volcengine import Credentials
from volcengine import ServiceInfo
from volcengine.base import Service


def get_normalized_params(params=None):
    if params is None:
        return None
    normalized_params = {}
    for key in params:
        value = params[key]
        if value is None:
            continue
        if isinstance(value, list):
            if len(value) == 0:
                normalized_params[key] = value
            for i in range(len(value)):
                new_key = "%s.%d" % (key, i)
                normalized_params[new_key] = str(value[i])
        else:
            normalized_params[key] = str(value)
    return normalized_params


class BaseApi(Service.Service):
    def __init__(self, region, endpoint, api_info, service, ak, sk):
        """init function.
        :param region:   region of request
        :param api_info: an object of volcengine.ApiInfo.ApiInfo()
        :param endpoint: endpoint of top gateway
        :param service:  a specific service name registered on top gateway
        :param ak:       account ak
        :param sk:       account ak
        """
        self.connection_timeout = 10
        self.socket_timeout = 10
        self.schema = 'http'
        self.header = dict()
        self.header["Content-Type"] = "application/json"
        self.endpoint = endpoint

        self.credential = Credentials.Credentials(ak, sk, service, region)
        self.service_info = ServiceInfo.ServiceInfo(self.endpoint,
                                                    self.header,
                                                    self.credential,
                                                    self.connection_timeout,
                                                    self.socket_timeout,
                                                    self.schema)
        self.api_info = api_info
        Service.Service.__init__(self, self.service_info, self.api_info)

    def get(self, action, params, doseq=0):
        res = super(BaseApi, self).get(action, params, doseq)
        try:
            res_json = json.loads(res)
        except Exception as e:
            raise Exception("res body is not json, %s, %s" % (e, res))
        if "ResponseMetadata" not in res_json:
            raise Exception("ResponseMetadata not in resp body, action %s, resp %s" % (action, res))
        elif "Error" in res_json["ResponseMetadata"]:
            raise Exception("%s failed, %s" % (action, res))
        return res_json
