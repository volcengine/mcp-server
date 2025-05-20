from vcloud.base.base_service import BaseService
from .config import *
from ...base.aksk import get_ak, get_sk

class VeenedgeAPI(BaseService):
    def __init__(self):
        super().__init__(
            ak=get_ak(),
            sk=get_sk(),
            service_info_map=service_info_map,
        )
        self.set_api_info(api_info)
