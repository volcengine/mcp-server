import asyncio
import functools
import hashlib
import json
import time
import httpx

from typing import Any
from mcp_server_tls.consts import *
from volcengine.ApiInfo import ApiInfo
from volcengine.auth.SignerV4 import SignerV4
from volcengine.tls.TLSService import TLSService
from volcengine.tls.tls_exception import TLSException
from volcengine.tls.const import *


HEADER_API_VERSION = "x-tls-apiversion"
API_VERSION_V_0_3_0 = "0.3.0"

API_INFO = {
    # APIs of log projects.
    API_CREATE_APP_INSTANCE: ApiInfo(HTTP_POST, API_CREATE_APP_INSTANCE, {}, {}, {}),
    API_CREATE_APP_SCENE_META: ApiInfo(HTTP_POST, API_CREATE_APP_SCENE_META, {}, {}, {}),
    API_DESCRIBE_APP_INSTANCES: ApiInfo(HTTP_GET, API_DESCRIBE_APP_INSTANCES, {}, {}, {}),
    API_DESCRIBE_SESSION_ANSWER: ApiInfo(HTTP_POST, API_DESCRIBE_SESSION_ANSWER, {}, {}, {}),
}

def __prepare_request(
    client: TLSService,
    api: str,
    params: dict = None,
    body: dict = None,
    request_headers: dict = None,
):
    if params is None:
        params = {}
    if body is None:
        body = {}

    request = client.prepare_request(API_INFO[api], params)

    if request_headers is None:
        request_headers = {CONTENT_TYPE: APPLICATION_JSON}
    request.headers.update(request_headers)

    if "json" in request.headers[CONTENT_TYPE] and api != WEB_TRACKS:
        request.body = json.dumps(body)
    else:
        request.body = body[DATA]

    if len(request.body) != 0:
        if isinstance(request.body, str):
            request.headers[CONTENT_MD5] = hashlib.md5(
                request.body.encode("utf-8")
            ).hexdigest()
        else:
            request.headers[CONTENT_MD5] = hashlib.md5(request.body).hexdigest()

    SignerV4.sign(request, client.service_info.credentials)

    return request

async def call_sdk_method(
    auth_info: dict,
    method_name: str,
    **kwargs,
) -> Any:
    try:
        client = get_sdk_client(auth_info)

        if not hasattr(client, method_name):
            raise AttributeError(f"TLSService 没有方法: {method_name}")

        method = getattr(client, method_name)
        bound_method = functools.partial(method, **kwargs)

        return await asyncio.to_thread(bound_method)

    except Exception as e:
        raise Exception(f"call sdk failed: {method.__name__}, error: {e}")

async def custom_api_call(
    auth_info: dict,
    api: str,
    params: dict = None,
    body: dict = None,
    request_headers: dict = None,
    is_stream: bool = False,
):
    """Customize a standard HTTP request to the Volcengine TLS API
    """
    client: TLSService = get_sdk_client(auth_info)

    if request_headers is None:
        request_headers = {HEADER_API_VERSION: API_VERSION_V_0_3_0}
    elif HEADER_API_VERSION not in request_headers:
        request_headers[HEADER_API_VERSION] = API_VERSION_V_0_3_0
    if CONTENT_TYPE not in request_headers:
        request_headers[CONTENT_TYPE] = APPLICATION_JSON
    request = __prepare_request(client, api, params, body, request_headers)

    method = API_INFO[api].method
    url = request.build()

    if is_stream:
        timeout = 180
    else:
        timeout = 60

    try_count = 0
    expected_quit_timestamp = int(time.time() * 1000 + 60 * 1500)

    async with httpx.AsyncClient() as session:
        while True:
            try_count += 1
            try:
                response = await session.request(
                    method=method,
                    url=url,
                    headers=request.headers,
                    data=request.body,
                    timeout=timeout,
                )
            except Exception as e:
                TLSService.increase_retry_counter_by_one()
                sleep_ms = TLSService.calc_backoff_ms(expected_quit_timestamp)
                if try_count < 5 and sleep_ms > 0:
                    await asyncio.sleep(sleep_ms / 1000)
                else:
                    raise TLSException(
                        error_code=e.__class__.__name__,
                        error_message=e.__str__(),
                    )
            else:
                if response.status_code == 200:
                    TLSService.decrease_retry_counter_by_one()

                    if is_stream:
                        return response

                    if "json" in response.headers[CONTENT_TYPE]:
                        if response.text != "":
                            response = json.loads(response.text)
                        else:
                            response = {}
                    else:
                        response = {DATA: response.content}
                    return response

                elif try_count < 5 and response.status_code in [429, 500, 502, 503]:
                    TLSService.increase_retry_counter_by_one()
                    sleep_ms = TLSService.calc_backoff_ms(expected_quit_timestamp)
                    if sleep_ms > 0:
                        await asyncio.sleep(sleep_ms / 1000)
                    else:
                        raise TLSException(response)
                else:
                    raise TLSException(response)

def get_sdk_client(auth_info: dict) -> TLSService:
    if "ak" not in auth_info:
        raise ValueError("the ak of auth_info is empty")

    if "sk" not in auth_info:
        raise ValueError("the sk of auth_info is empty")

    return TLSService(
        region=auth_info.get("region"),
        endpoint=auth_info.get("endpoint"),
        access_key_id=auth_info.get("ak"),
        access_key_secret=auth_info.get("sk"),
        security_token=auth_info.get("token"),
    )
