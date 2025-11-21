from src.base.base_service import BaseService
from .config import api_info


class VodAPI(BaseService):

    def __init__(self):
        super().__init__()
        self.set_api_info(api_info)
    