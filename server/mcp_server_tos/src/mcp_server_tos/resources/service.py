import asyncio
import logging
import os
from typing import List, Dict
from urllib.parse import quote

import httpx
from httpx import Limits
from mcp_server_tos.config import TosConfig
from requests.structures import CaseInsensitiveDict
from tos import TosClientV2, exceptions, HttpMethodType
from tos.http import Request

UNSIGNED_PAYLOAD = 'UNSIGNED-PAYLOAD'
TOS_USER_AGENT = 've-tos-python-sdk/v2.8.1 (linux/amd64;python3.12.0) -- TOS/MCP Server/v0.1.0'

logger = logging.getLogger(__name__)

_global_client = httpx.AsyncClient(
    limits=Limits(
        max_connections=200,
        max_keepalive_connections=50,
        keepalive_expiry=30
    ),
    timeout=30.0,
)


class TosResource:
    client: TosClientV2 = None

    def __init__(self, config: TosConfig):
        self.client = TosClientV2(
            ak=config.access_key,
            sk=config.secret_key,
            security_token=config.security_token,
            region=config.region,
            endpoint=config.endpoint,
        )
        self.user_agent = TOS_USER_AGENT
        self.configured_buckets = self._get_configured_buckets()

    def _get_configured_buckets(self) -> List[str]:
        """从环境变量加载预配置存储桶"""
        bucket_list = os.getenv('TOS_BUCKETS')
        if bucket_list:
            return [b.strip() for b in bucket_list.split(',')]
        return []

    async def get(self, bucket: str, key: str = None, headers: Dict[str, str] = None,
                  params: Dict[str, str] = None):
        if key is not None:
            _is_valid_object_name(key)

        if self.client is None:
            raise exceptions.TosClientError("TosClient is not initialized")

        # 通过变量赋值,防止动态调整 auth endpoint 出现并发问题
        sign_out = self.client.pre_signed_url(HttpMethodType.Http_Method_Get, bucket, key, 3600, headers, params)
        attempt = 0
        while attempt < 3:
            try:
                response = await _global_client.get(sign_out.signed_url, follow_redirects=False,
                                                    headers=headers, params=params,
                                                    timeout=httpx.Timeout(connect=10, read=30, write=10, pool=10))
                if response.status_code >= 500 or response.status_code == 429:
                    await response.aclose()
                    attempt += 1
                    if attempt < 3:
                        logger.warning(f'Retry {attempt}/3 for {bucket}/{key}, Status: {response.status_code}')
                        await asyncio.sleep(2 ** attempt)
                        continue
                    else:
                        raise Exception(f"Failed after 3 retries for {bucket}/{key}")
                else:
                    return response
            except Exception as e:
                attempt += 1
                if attempt < 3:
                    logger.warning(f'Failed to get {bucket}/{key}: {str(e)}, attempt: {attempt}')
                    await asyncio.sleep(2 ** attempt)
                    continue
                else:
                    raise Exception(f"Failed after 3 retries for {bucket}/{key}")


async def call(self, method: str, bucket: str, key: str = None, data=None, headers: Dict[str, str] = None,
               params: Dict[str, str] = None):
    if key is not None:
        _is_valid_object_name(key)

    headers = self._to_case_insensitive_dict(headers)
    params = self._sanitize_dict(params)

    if headers.get('x-tos-content-sha256') is None:
        headers['x-tos-content-sha256'] = UNSIGNED_PAYLOAD

    # 通过变量赋值,防止动态调整 auth endpoint 出现并发问题
    auth = self.client.auth
    endpoint = self.client.endpoint
    url_str = self._make_virtual_host_url(bucket, key)
    req = Request(method, self._make_virtual_host_url(bucket, key),
                  _make_virtual_host_uri(key),
                  _get_virtual_host(bucket, endpoint),
                  data=data,
                  params=params,
                  headers=headers)

    # 若auth 为空即为匿名请求，则不计算签名
    if auth is not None:
        auth.sign_request(req)
    if 'User-Agent' not in req.headers:
        req.headers['User-Agent'] = self.user_agent

    try_count = 0
    async with httpx.AsyncClient() as client:
        while True:
            try_count += 1
            try:
                response = await client.request(method, req.url, follow_redirects=False, headers=req.headers,
                                                params=req.params, data=req.data, timeout=60)
            except Exception as e:
                if try_count <= 3:
                    await asyncio.sleep(2 * try_count)
                    continue
                else:
                    error_msg = f'Failed to call {url_str}: {str(e)}'
                    logger.error(error_msg)
                    raise e
            else:
                if response.status_code == 200 or response.status_code == 206:
                    return response
                if method in ["GET", "HEAD"] and try_count <= 3 and (
                        response.status_code >= 500 or response.status_code == 429):
                    await asyncio.sleep(2 * try_count)
                    continue
                else:
                    raise Exception(f'Call tos url: {url_str} return: {str(response.status_code)}, '
                                    f'request_id: {response.headers.get("x-tos-request-id")}')


def _to_case_insensitive_dict(self, headers: dict):
    self._sanitize_dict(headers)
    return CaseInsensitiveDict(headers)


def _sanitize_dict(self, d: dict):
    if d:
        for k, v in d.items():
            d[k] = v if isinstance(v, str) else v.decode() if isinstance(v, bytes) else str(v)
    return d


def _make_virtual_host_url(self, host, scheme, bucket=None, key=None):
    url = host
    if bucket and key:
        url = '{0}.{1}/{2}'.format(bucket, host, quote(key, '/~'))
    elif bucket and not key:
        url = '{0}.{1}'.format(bucket, host)
    elif key:
        url = '{0}/{1}'.format(host, quote(key, '/~'))

    return self._format_endpoint(scheme + url)


def _format_endpoint(self, endpoint):
    if not endpoint.startswith('http://') and not endpoint.startswith('https://'):
        return 'https://' + endpoint
    else:
        return endpoint


def _is_valid_object_name(object_name):
    """
    - 对象名命名规范
    - 对象名字符长度不能0；
    - 对象名不允许为 . 由于 requests 库中 _remove_path_dot_segments 方法会将 虚拟主机请求 {bucket}.{host}/. 强制转化为 {bucket}.{host}/ 导致最后签名报错
    SDK 会对依照该规范做校验，如果用户指定的对象名与规范不匹配则报错客户端校验失败。
    """
    if len(object_name) < 1:
        raise exceptions.TosClientError('invalid object name, object name is empty')

    if object_name == '.' or object_name == '..':
        raise exceptions.TosClientError("invalid object name, the object name can not use '.'")


def _make_uri(bucket=None, key=None):
    if bucket and not key:
        return '/{0}'.format(bucket)
    if bucket and key:
        return '/{0}/{1}'.format(bucket, key)
    return '/'


def _make_virtual_host_uri(key=None):
    if key:
        return '/{0}'.format(key)
    return '/'


def _get_virtual_host(bucket, endpoint):
    if bucket:
        return bucket + '.' + _get_host(endpoint)
    else:
        return _get_host(endpoint)


def _get_host(endpoint):
    if endpoint.startswith('http://'):
        return endpoint[7:]
    if endpoint.startswith('https://'):
        return endpoint[8:]
    return endpoint
