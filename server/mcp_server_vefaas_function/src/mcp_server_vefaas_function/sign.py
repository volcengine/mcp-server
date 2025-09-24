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

import datetime
import hashlib
import hmac
import json
import os
from urllib.parse import quote
import base64
import requests
import datetime
import os
import base64
import json
import logging
from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context
from starlette.requests import Request

logger = logging.getLogger(__name__)

# 以下参数视服务不同而不同，一个服务内通常是一致的
Service = "apig"
Version = "2021-03-03"
Region = "cn-beijing"
Host = "iam.volcengineapi.com"
ContentType = "application/x-www-form-urlencoded"

AK_KEY = "VOLCENGINE_ACCESS_KEY"
SK_KEY = "VOLCENGINE_SECRET_KEY"

ALT_AK_KEY = 'VOLC_ACCESSKEY'
ALT_SK_KEY = 'VOLC_SECRETKEY'

# 请求的凭证，从IAM或者STS服务中获取
AK = os.getenv(AK_KEY) or os.getenv(ALT_AK_KEY)
SK = os.getenv(SK_KEY) or os.getenv(ALT_SK_KEY)


# 当使用临时凭证时，需要使用到SessionToken传入Header，并计算进SignedHeader中，请自行在header参数中添加X-Security-Token头
# SessionToken = ""


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


# 第一步：准备辅助函数。
# sha256 非对称加密
def hmac_sha256(key: bytes, content: str):
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


# sha256 hash算法
def hash_sha256(content: str):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# 第二步：签名请求函数
def request(method, date, query, header, ak, sk, token, action, body, region = None, timeout=None):
    # 第三步：创建身份证明。其中的 Service 和 Region 字段是固定的。ak 和 sk 分别代表
    # AccessKeyID 和 SecretAccessKey。同时需要初始化签名结构体。一些签名计算时需要的属性也在这里处理。
    # 初始化身份证明结构体

    credential = {
        "access_key_id": ak,
        "secret_access_key": sk,
        "service": Service,
        "region": region or Region,
    }

    if token is not None:
        credential["session_token"] = token

    if action in ['CodeUploadCallback', 'CreateDependencyInstallTask', 'GetDependencyInstallTaskStatus',
                  'GetDependencyInstallTaskLogDownloadURI', "ListTemplates", "GetTemplateDetail", "GetRevision",
                  "CreateApplication", "GetApplication", "ReleaseApplication", "ListTriggers", "GetApplicationRevisionLog"]:
        credential["service"] = "vefaas"

    content_type = ContentType
    version = Version
    if method == "POST":
        content_type = "application/json"

    if action == "CreateRoute" or action == "ListRoutes":
        version = "2022-11-12"

    # 初始化签名结构体
    request_param = {
        "body": body,
        "host": Host,
        "path": "/",
        "method": method,
        "content_type": content_type,
        "date": date,
        "query": {"Action": action, "Version": version, **query},
        "timeout": timeout,
    }
    if body is None:
        request_param["body"] = ""
    # 第四步：接下来开始计算签名。在计算签名前，先准备好用于接收签算结果的 signResult 变量，并设置一些参数。
    # 初始化签名结果的结构体
    x_date = request_param["date"].strftime("%Y%m%dT%H%M%SZ")
    short_x_date = x_date[:8]
    x_content_sha256 = hash_sha256(request_param["body"])
    sign_result = {
        "Host": request_param["host"],
        "X-Content-Sha256": x_content_sha256,
        "X-Date": x_date,
        "Content-Type": request_param["content_type"],
    }
    # 第五步：计算 Signature 签名。
    signed_headers_str = ";".join(
        ["content-type", "host", "x-content-sha256", "x-date"]
    )
    # signed_headers_str = signed_headers_str + ";x-security-token"
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

    # 打印正规化的请求用于调试比对
    logger.debug("canonical_request=%s", canonical_request_str)
    hashed_canonical_request = hash_sha256(canonical_request_str)

    # 打印hash值用于调试比对
    logger.debug("hashed_canonical_request=%s", hashed_canonical_request)
    credential_scope = "/".join([short_x_date, credential["region"], credential["service"], "request"])
    string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hashed_canonical_request])

    # 打印最终计算的签名字符串用于调试比对
    logger.debug("string_to_sign=%s", string_to_sign)
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
    header = {**header, **{"X-Security-Token": token}}
    # 第六步：将 Signature 签名写入 HTTP Header 中，并发送 HTTP 请求。
    r = requests.request(method=method,
                         url="https://{}{}".format(request_param["host"], request_param["path"]),
                         headers=header,
                         params=request_param["query"],
                         data=request_param["body"],
                         timeout=request_param["timeout"],
                         )
    return r.json()


def get_authorization_credentials(ctx: Context = None) -> tuple[str, str, str]:
    """
    Gets authorization credentials from either environment variables or request headers.
    
    Args:
        ctx: The server context object
        
    Returns:
        tuple: (access_key, secret_key, session_token)
        
    Raises:
        ValueError: If authorization information is missing or invalid
    """
    # First try environment variables
    if AK_KEY in os.environ and SK_KEY in os.environ:
        return (
            os.environ[AK_KEY],
            os.environ[SK_KEY],
            ""  # No session token for static credentials
        )
    elif ALT_AK_KEY in os.environ and ALT_SK_KEY in os.environ:
        return (
            os.environ[ALT_AK_KEY],
            os.environ[ALT_SK_KEY],
            ""  # No session token for static credentials
        )

    # Try getting auth from request or environment
    _ctx: Context[ServerSession, object] = ctx
    raw_request: Request = _ctx.request_context.request
    auth = None

    if raw_request:
        # Try to get authorization from request headers
        auth = raw_request.headers.get("authorization", None)

    if auth is None:
        # Try to get from environment if not in headers
        auth = os.getenv("authorization", None)

    if auth is None:
        raise ValueError("Missing authorization info.")

    # Parse the authorization string
    if ' ' in auth:
        _, base64_data = auth.split(' ', 1)
    else:
        base64_data = auth

    try:
        # Decode Base64 and parse JSON
        decoded_str = base64.b64decode(base64_data).decode('utf-8')
        data = json.loads(decoded_str)

        return (
            data.get('AccessKeyId'),
            data.get('SecretAccessKey'),
            data.get('SessionToken')
        )
    except Exception as e:
        raise ValueError(f"Failed to decode authorization info: {str(e)}")


if __name__ == "__main__":
    # response_body = request("Get", datetime.datetime.utcnow(), {}, {}, AK, SK, "ListUsers", None)
    # print(response_body)

    now = datetime.datetime.utcnow()

    # Body的格式需要配合Content-Type，API使用的类型请阅读具体的官方文档，如:json格式需要json.dumps(obj)
    # response_body = request("GET", now, {"Limit": "2"}, {}, AK, SK, "ListGateways", None)
    # print(response_body)

    # response_body = request("POST", now, {"Limit": "10"}, {}, AK, SK, "ListUsers", "UnUseParam=ASDF")
    # print(response_body)

    body = {
        "Name": "xxxxxx",
        "GatewayId": "gciqjm7qahbthkcuufaked",
        "SourceType": "VeFaas",
        "UpstreamSpec": {
            "VeFaas": {
                "FunctionId": "vyyzfaked"
            }
        }
    }

    response_body = request("POST", now, {}, {}, AK, SK, "CreateUpstream", json.dumps(body))
    print(response_body)
