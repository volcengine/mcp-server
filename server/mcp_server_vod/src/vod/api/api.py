from src.base.base_service import BaseService
from .config import api_info
from typing import Dict, Any



class VodAPI(BaseService):

    def __init__(self):
        super().__init__()
        self.set_api_info(api_info)
 