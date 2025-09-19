# coding:utf-8
"""
Copyright (year) Beijing Volcano Engine Technology Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
import pytz
from datetime import datetime
import threading
from typing import Dict, Literal, Any
from pydantic import BaseModel
import volcenginesdkcore
import volcenginesdksts
import volcenginesdkvolcobserve


lock = threading.Lock()
mapping = {}

class Credential(BaseModel):
    ak: str
    sk: str
    service: str
    region: str
    # Inner/AssumeRole
    mode: str
    role: str = None
    account_id: int = 0

class RequestParams(BaseModel):
    host: str = ""
    # query or post body
    body: Dict[str, Any] = {}
    method: Literal["POST", "GET", "PUT", "PATCH", "DELETE"]  # 枚举值
    headers: Dict[str, str] = {}  # 字典类型
    action: str
    version: str
    # "text/plain" or "application/json"
    accept: str = "application/json"
    # "text/plain" or "application/json"
    content_type: str = "application/json"

def top_invoke(credential: Credential, params: RequestParams):
    collection_formats = {}
    path_params = {}
    query_params = []
    header_params = {}
    form_params = []
    local_var_files = {}

    configuration = volcenginesdkcore.Configuration()
    configuration.host = params.host
    configuration.ak = credential.ak
    configuration.sk = credential.sk
    configuration.region = credential.region
    configuration.client_side_validation = True

    client = volcenginesdkcore.ApiClient(configuration)
    body_params = params.body
    # HTTP header `Accept`
    header_params['Accept'] = client.select_header_accept(
        [params.accept])  # noqa: E501
    # HTTP header `Content-Type`
    header_params['Content-Type'] = client.select_header_content_type(  # noqa: E501
        [params.content_type])  # noqa: E501
    if params.headers:
        header_params.update(params.headers)
    # Authentication setting
    auth_settings = ['volcengineSign']  # noqa: E501
    true_path = f'/{params.action}/{params.version}/{credential.service}/{params.method.lower()}/{params.content_type.lower().replace("/", "_")}'

    preload_content = False
    if params.host.find("volcengine") != -1:
        preload_content = True
    response = client.call_api(
        true_path, params.method,
        path_params,
        query_params,
        header_params,
        body=body_params,
        post_params=form_params,
        files=local_var_files,
        auth_settings=auth_settings,
        async_req=False,
        response_type='object',
        _return_http_data_only=True,
        _preload_content=preload_content,
        _request_timeout=None,
        collection_formats=collection_formats)

    if not preload_content:
        try:
            response = json.loads(response.data)
        except ValueError:
            response = response.data
    return response


if __name__ == '__main__':
    resp = top_invoke(
        Credential(
            ak="AK****",
            sk="******",
            service="ecs",
            region="cn-beijing",
            mode="AssumeRole",
            role="ServiceRoleForVBH",
            account_id=1400000042
        ),
        RequestParams(
            host="open.volcengineapi.com",
            body={},
            method="GET",
            headers={},
            action="DescribeInstances",
            version="2020-04-01",
            content_type="text/plain",
        )
    )