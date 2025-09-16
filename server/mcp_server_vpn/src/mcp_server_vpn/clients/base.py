import json

from volcengine.ApiInfo import ApiInfo
from typing import Any
from volcengine import Credentials
from volcengine import ServiceInfo
from volcengine.base import Service


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
        self.schema = 'https'
        self.header = dict()
        self.header["Content-Type"] = "application/json"
        self.endpoint = endpoint

        self.credential = Credentials.Credentials(ak, sk, service, region)
        self.service_info = ServiceInfo.ServiceInfo(
            self.endpoint,
            self.header,
            self.credential,
            self.connection_timeout,
            self.socket_timeout,
            self.schema,
        )
        self.api_info = api_info
        Service.Service.__init__(self, self.service_info, self.api_info)

    @staticmethod
    def to_params(obj: Any) -> dict[str, Any]:
        """Convert a request model to a parameters dict, dropping None values.

        ``volcengine-python-sdk`` request models expose ``attribute_map``
        describing how Python attribute names map to request parameter keys. This
        helper applies that mapping so that callers can use snake_case attribute
        names while the API receives the expected camel case keys.
        """

        if hasattr(obj, "to_dict"):
            data = obj.to_dict()
        elif hasattr(obj, "model_dump"):
            data = obj.model_dump()
        elif isinstance(obj, dict):
            data = obj
        else:
            data = getattr(obj, "__dict__", {})

        attr_map = getattr(obj, "attribute_map", None)
        if isinstance(attr_map, dict):
            data = {attr_map.get(k, k): v for k, v in data.items()}

        return {k: v for k, v in data.items() if v is not None}

    def get(self, action, params, doseq=0):
        res = super(BaseApi, self).get(action, params, doseq)
        try:
            res_json = json.loads(res)
        except Exception as e:
            raise Exception("res body is not json, %s, %s" % (e, res))
        if "ResponseMetadata" not in res_json:
            raise Exception(
                "ResponseMetadata not in resp body, action %s, resp %s" % (action, res)
            )
        elif "Error" in res_json["ResponseMetadata"]:
            raise Exception("%s failed, %s" % (action, res))
        return res_json
