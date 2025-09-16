import datetime
import hashlib
import hmac
from dataclasses import asdict
import json
from urllib.parse import quote
from ..model import *

import aiohttp

Service = "volc_torchlight_api"
Version = "2025-01-01"
Region = "cn-north-1"
Host = "mercury.volcengineapi.com"
ContentType = "application/json"


async def web_search_volcengine_auth(ak: str, sk: str, req: WebSearchRequest, tool_name: str):
    now = datetime.datetime.utcnow()
    headers = {
        "X-Traffic-Tag": f"ark_mcp_server_{tool_name}",
    }
    return await volcengine_auth_request("POST", now, {}, headers, ak, sk, "WebSearch", json.dumps(asdict(req)))


def norm_query(params):
    query = ""
    for key in sorted(params.keys()):
        if type(params[key]) == list:
            for k in params[key]:
                query = (
                        query + quote(key, safe="-_.~") + "=" + quote(k, safe="-_.~") + "&"
                )
        else:
            query = (query + quote(key, safe="-_.~") + "=" + quote(params[key], safe="-_.~") + "&")
    query = query[:-1]
    return query.replace("+", "%20")


def hmac_sha256(key: bytes, content: str):
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


def hash_sha256(content: str):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


async def volcengine_auth_request(method, date, query, header, ak, sk, action, body):
    credential = {
        "access_key_id": ak,
        "secret_access_key": sk,
        "service": Service,
        "region": Region,
    }
    request_param = {
        "body": body,
        "host": Host,
        "path": "/",
        "method": method,
        "content_type": ContentType,
        "date": date,
        "query": {"Action": action, "Version": Version, **query},
    }
    if body is None:
        request_param["body"] = ""
    x_date = request_param["date"].strftime("%Y%m%dT%H%M%SZ")
    short_x_date = x_date[:8]
    x_content_sha256 = hash_sha256(request_param["body"])
    sign_result = {
        "Host": request_param["host"],
        "X-Content-Sha256": x_content_sha256,
        "X-Date": x_date,
        "Content-Type": request_param["content_type"],
    }
    signed_headers_str = ";".join(
        ["content-type", "host", "x-content-sha256", "x-date"]
    )
    canonical_request_str = "\n".join(
        [request_param["method"].upper(),
         request_param["path"],
         norm_query(request_param["query"]),
         "\n".join(
             [
                 "content-type:" + request_param["content_type"],
                 "host:" + request_param["host"],
                 "x-content-sha256:" + x_content_sha256,
                 "x-date:" + x_date,
             ]
         ),
         "",
         signed_headers_str,
         x_content_sha256,
         ]
    )
    hashed_canonical_request = hash_sha256(canonical_request_str)
    credential_scope = "/".join([short_x_date, credential["region"], credential["service"], "request"])
    string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hashed_canonical_request])
    k_date = hmac_sha256(credential["secret_access_key"].encode("utf-8"), short_x_date)
    k_region = hmac_sha256(k_date, credential["region"])
    k_service = hmac_sha256(k_region, credential["service"])
    k_signing = hmac_sha256(k_service, "request")
    signature = hmac_sha256(k_signing, string_to_sign).hex()

    sign_result["Authorization"] = "HMAC-SHA256 Credential={}, SignedHeaders={}, Signature={}".format(
        credential["access_key_id"] + "/" + credential_scope,
        signed_headers_str,
        signature,
    )
    header = {**header, **sign_result}

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=method,
            url=f"https://{request_param['host']}{request_param['path']}",
            headers=header,
            timeout=aiohttp.ClientTimeout(total=600),
            params=request_param["query"],
            data=request_param["body"]
        ) as response:
            # 在上下文内读取所有数据，避免连接关闭问题
            response.raise_for_status()  # 手动调用
            data = await response.json()
            return data
        return None
    return None