from volcengine.ApiInfo import ApiInfo
from typing import Any
from mcp_server_na.common.volc_base import BaseApi


class NAClient(BaseApi):
    def __init__(self, region: str, endpoint: str, ak: str, sk: str):
        api_infos = {
            'CreateDiagnosisInstance': ApiInfo('GET', '/',
                                               {"Action": 'CreateDiagnosisInstance', "Version": "2024-10-01"}, {}, {}),
            'DescribeDiagnosisInstanceDetail': ApiInfo('GET', '/',
                                               {"Action": 'DescribeDiagnosisInstanceDetail', "Version": "2024-10-01"}, {}, {})
        }
        super(NAClient, self).__init__(region, endpoint, api_infos, "location", ak, sk)

    def create_diagnose_instance(self, region: str, resource_type: str, resource_id: str)-> dict[str, Any]:
        params = {"ResourceRegion": region, "ResourceType": resource_type, "ResourceInstanceId": resource_id}
        return self.get("CreateDiagnosisInstance", params)

    def describe_diagnosis_instance_detail(self, diagnosis_instance_id: str) -> dict[str, Any]:
        params={"DiagnosisInstanceId":diagnosis_instance_id}
        return self.get("DescribeDiagnosisInstanceDetail", params)
