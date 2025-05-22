import json
from urllib.parse import urlparse

import requests

from mcp_server_apmplus.config import ApmplusConfig
from mcp_server_apmplus.model import *

SERVER_SERVICE = "apmplus_server"
DEFAULT_REGION = "cn-beijing"


class ApmplusApi(object):
    def __init__(self, cred: ApmplusConfig):
        if cred.access_key == "" or cred.secret_key == "" or cred.endpoint == "":
            raise ValueError("access_key, secret_key or endpoint is empty")
        self.cred = cred

    def do_request(self, service, region, req: requests.Request) -> requests.Response:
        # 添加header
        req.headers["Content-Type"] = "application/json"
        req.headers["Host"] = urlparse(self.cred.endpoint).hostname
        # 签名
        self.cred.append_authorization(
            urlparse(req.url).path,
            req.method,
            req.headers,
            req.data,
            None,
            req.params,
            region,
            service,
        )
        req = req.prepare()
        with requests.Session() as session:
            resp = session.send(req)
            return resp

    def server_list_alert_rule(self, req: ApmplusServerListAlertRuleRequest) -> str:
        req_json = json.dumps(req.to_dict())
        query = {
            "Action": "GetAlertRuleList",
            "Version": "2022-07-11",
            "Region": req.region_id,
        }
        request = requests.Request(
            method="POST",
            url=self.cred.endpoint,
            data=req_json,
            params=query,
        )
        response = self.do_request(SERVER_SERVICE, req.region_id, request)
        if response.status_code != 200:
            raise Exception(
                f"get_result failed, status_code: {response.status_code}, response: {response.text},request_headers: {request.headers}, request_url:{request.url}, request_params:{request.params}, request_data:{request.data},request_body:{request.json}"
            )
        return response.text

    def server_list_notify_group(self, req: ApmplusServerListNotifyGroupRequest) -> str:
        req_json = json.dumps(req.to_dict())
        query = {
            "Action": "NotifyGroupList",
            "Version": "2022-07-11",
            "Region": req.region_id,
        }
        request = requests.Request(
            method="POST",
            url=self.cred.endpoint,
            data=req_json,
            params=query,
        )
        response = self.do_request(SERVER_SERVICE, req.region_id, request)
        if response.status_code != 200:
            raise Exception(
                f"get_result failed, status_code: {response.status_code}, response: {response.text},request_headers: {request.headers}, request_url:{request.url}, request_params:{request.params}, request_data:{request.data},request_body:{request.json}"
            )
        return response.text

    def server_query_metrics(self, req: ApmplusServerQueryMetricsRequest) -> str:
        if not req.region_id:
            req.region_id = DEFAULT_REGION
        req_json = json.dumps(req.to_dict())
        query = {
            "Action": "Draw",
            "Version": "2022-11-09",
            "Region": req.region_id,
        }
        request = requests.Request(
            method="POST",
            url=self.cred.endpoint,
            data=req_json,
            params=query,
        )
        response = self.do_request(SERVER_SERVICE, req.region_id, request)
        if response.status_code != 200:
            raise Exception(
                f"get_result failed, status_code: {response.status_code}, response: {response.text},request_headers: {request.headers}, request_url:{request.url}, request_params:{request.params}, request_data:{request.data},request_body:{request.json}"
            )
        return response.text


if __name__ == "__main__":
    req = ApmplusServerQueryMetricsRequest(
        region_id="",
        query="histogram_quantile(0.99, sum(rate(gen_ai_client_operation_duration_bucket{}[5m])) by (le))",
        start_time=1746777063,
        end_time=1746780663,
    )
    # Body的格式需要配合Content-Type，API使用的类型请阅读具体的官方文档，如:json格式需要json.dumps(obj)
    config = ApmplusConfig(
        access_key="",
        secret_key="",
        endpoint="https://open.volcengineapi.com",
    )
    api = ApmplusApi(config)
    response_body = api.server_query_metrics(req)
    print(response_body)
