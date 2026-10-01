import json
from urllib.parse import urlparse

import requests
import volcenginesdkcore
from volcenginesdkapmplusserver import APMPLUSSERVERApi, models

from mcp_server_apmplus.config import ApmplusConfig
from mcp_server_apmplus.model import *

SERVER_SERVICE = "apmplus_server"
DEFAULT_REGION = "cn-beijing"


class ApmplusApi(object):
    cred: ApmplusConfig
    apmplusApiClient: APMPLUSSERVERApi

    def __init__(self, cred: ApmplusConfig):
        if cred.access_key == "" or cred.secret_key == "" or cred.endpoint == "":
            raise ValueError("access_key, secret_key or endpoint is empty")
        self.cred = cred
        self.apmplusApiClient = APMPLUSSERVERApi(
            volcenginesdkcore.ApiClient(configuration=cred.to_volc_configuration())
        )

    def _get_volc_client(self, dynamic_conf: ApmplusConfig) -> APMPLUSSERVERApi:
        return APMPLUSSERVERApi(
            volcenginesdkcore.ApiClient(
                configuration=dynamic_conf.to_volc_configuration()
            )
        )

    def do_request(self, service, region, req: requests.Request) -> requests.Response:
        # 添加header
        req.headers["Content-Type"] = "application/json"
        req.headers["Host"] = urlparse(req.url).hostname
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
            "Region": req.region,
        }
        request = requests.Request(
            method="POST",
            url="https://" + self.cred.endpoint,
            data=req_json,
            params=query,
        )
        response = self.do_request(SERVER_SERVICE, req.region, request)
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
            "Region": req.region,
        }
        request = requests.Request(
            method="POST",
            url="https://" + self.cred.endpoint,
            data=req_json,
            params=query,
        )
        response = self.do_request(SERVER_SERVICE, req.region, request)
        if response.status_code != 200:
            raise Exception(
                f"get_result failed, status_code: {response.status_code}, response: {response.text},request_headers: {request.headers}, request_url:{request.url}, request_params:{request.params}, request_data:{request.data},request_body:{request.json}"
            )
        return response.text

    def server_query_metrics(self, req: ApmplusServerQueryMetricsRequest) -> str:
        if not req.region:
            req.region = DEFAULT_REGION
        req_json = json.dumps(req.to_dict())
        query = {
            "Action": "Draw",
            "Version": "2022-11-09",
            "Region": req.region,
        }
        request = requests.Request(
            method="POST",
            url="https://" + self.cred.endpoint,
            data=req_json,
            params=query,
        )
        response = self.do_request(SERVER_SERVICE, req.region, request)
        if response.status_code != 200:
            raise Exception(
                f"get_result failed, status_code: {response.status_code}, response: {response.text},request_headers: {request.headers}, request_url:{request.url}, request_params:{request.params}, request_data:{request.data},request_body:{request.json}"
            )
        return response.text

    async def server_get_trace_detail(
        self, args: dict, dynamic_conf: ApmplusConfig = None
    ) -> models.get_trace_detail_response.GetTraceDetailResponse:
        client = self.apmplusApiClient
        if dynamic_conf is not None:
            client = self._get_volc_client(dynamic_conf)
        return client.get_trace_detail(
            models.get_trace_detail_request.GetTraceDetailRequest(**args)
        )

    async def server_list_span(
        self, args: dict, dynamic_conf: ApmplusConfig = None
    ) -> dict:
        client = self.apmplusApiClient
        if dynamic_conf is not None:
            client = self._get_volc_client(dynamic_conf)
        return client.list_span(models.list_span_request.ListSpanRequest(**args))
