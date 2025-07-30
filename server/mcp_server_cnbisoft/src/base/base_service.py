# coding:utf-8
from .base_trait import BaseTrait  # Modify it if necessary


class BaseService(BaseTrait):
    def __init__(self, region='cn-north-1', ak=None, sk=None, service_info_map=None,):
        super().__init__({
            'ak': ak,
            'sk': sk,
           'region': region,
           'service_info_map': service_info_map
        })
  