from src.base.base_service import BaseService
from .config import *
import os


class LiveAPI(BaseService):

    def __init__(self):
        if os.getenv("VOLCENGINE_REGION") is None:
            region = "cn-north-1"
        else:
            region = os.getenv("VOLCENGINE_REGION")

        super().__init__(
            ak=os.getenv("VOLCENGINE_ACCESS_KEY"),
            sk=os.getenv("VOLCENGINE_SECRET_KEY"),
            region=region,
            service_info_map=service_info_map,
        )
        self.set_api_info(api_info)
