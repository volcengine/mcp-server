from volcengine.vod.VodService import VodService
import os

class VodAPI(VodService):

    def __init__(self):
        if os.getenv("VOLCENGINE_REGION") is None:
            region = "cn-north-1"
        else:
            region = os.getenv("VOLCENGINE_REGION")

        super().__init__(region=region)
        self.set_ak(os.getenv("VOLCENGINE_ACCESS_KEY"))
        self.set_sk(os.getenv("VOLCENGINE_SECRET_KEY"))
        self.service_info.header["x-tt-mcp"] = 'volc'