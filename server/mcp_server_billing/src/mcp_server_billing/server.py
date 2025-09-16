import base64
import json
import os
import time
import urllib.parse
from contextvars import ContextVar
from typing import Dict, Optional, Any, Sequence, Callable
import aiohttp
import uvicorn

from fastmcp.utilities.logging import configure_logging, get_logger
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from volcenginesdkcore.rest import ApiException

#  SSE
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.datastructures import Headers
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Mount, Route
#  STDIO
from mcp.server.stdio import stdio_server

from .model import OAuthClientRegistration, TopResponseModel
from .openapi import openapi_to_mcp_tools
from .sdk_tool import create_api_client, create_universal_info
from .utils import load_config, validate_auth_header, filter_params, load_swagger
from .variable import *

# 定义auth_context
auth_context: ContextVar[Optional[dict[str, Any]]] = ContextVar("auth_context", default=None)

# 定义logger
logger = get_logger(__name__)
configure_logging("INFO")

# 定义Server
server = Server("mcp-server")

# 获取全局配置
server_config = load_config('cfg.yaml')


class SSEMiddleware:
    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope: Dict, receive: Callable, send: Callable):
        if scope.get("path") in OAUTH_HANDLED_PATHS:
            await self.app(scope, receive, send)
            return
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = Headers(scope=scope)
        auth_header = headers.get(AUTHORIZATION_HEADER)
        if not auth_header:
            return await self._send_401_response(send, "credentials_required",
                                                 "Authentication credentials were not provided.")
        auth_result = validate_auth_header(auth_header, server_config, token_store)
        if not auth_result["is_valid"]:
            return await self._send_401_response(send, "invalid_token",
                                                 "The provided authentication token is invalid or expired.")
        # 认证成功，设置上下文并继续处理请求
        context_token = auth_context.set(auth_result["credentials"])
        try:
            await self.app(scope, receive, send)
        finally:
            auth_context.reset(context_token)

    @staticmethod
    async def _send_401_response(send: Callable, code: str, message: str):
        body = json.dumps({
            "type": f"/errors/{code}",
            "title": "Authentication Required",
            "status": 401,
            "detail": message,
        }).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": 401,
            "headers": [
                (b"content-type", b"application/json"),
                (b"www-authenticate", b'Bearer'),
                (b"content-length", str(len(body)).encode()),
            ],
        })

        await send({
            "type": "http.response.body",
            "body": body,
            "more_body": False
        })


async def serve() -> None:
    mcp_tools = []
    # 读取swagger
    openapi_spec = load_swagger(f'{server_config.service_code}.json')
    try:
        mcp_tools = openapi_to_mcp_tools(openapi_spec)
    except Exception as e:
        logger.error(f"openapi tools error: {e}")
        raise

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return mcp_tools

    @server.call_tool()
    async def call_tool(
            name: str, arguments: dict
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        result: TopResponseModel
        if server_config.credential == CREDENTIAL_TYPE_ENV:
            ak = server_config.ak
            sk = server_config.sk
            session_token = server_config.sts_token
            if ak is None and sk is None:
                resp = {"Code": "Credential Not Set"}
                result = TopResponseModel(**resp)
                return [
                    TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))
                ]
            client = create_api_client(ak=ak, sk=sk, session_token=session_token)
        else:
            # 获取 Context
            current_auth_info = auth_context.get()
            if current_auth_info is None:
                resp = {"Code": "Authorization Failed"}
                result = TopResponseModel(**resp)
                return [
                    TextContent(type="text", text=json.dumps(result.model_dump()))
                ]
            client = create_api_client(
                ak=current_auth_info['ak'], sk=current_auth_info['sk'],
                session_token=current_auth_info['session_token'])
        try:
            arguments = filter_params(arguments)
            paths = openapi_spec.get('paths').get(f'/{name}')
            service_code = paths.get('x-service-code')
            version = paths.get('x-version')
            method = paths.get('x-method')
            content_type = paths.get('x-content-type')
            info = create_universal_info(service=service_code, action=name, version=version,
                                         method=method, content_type=content_type)
            resp, status_code, resp_header = client.do_call_with_http_info(info=info, body=arguments)
            if resp is None:
                resp = {}
            result = TopResponseModel(**resp)
            return [
                TextContent(type="text", text=json.dumps(result.model_dump()))
            ]
        except ApiException as apie:
            error_message = getattr(apie, 'body', None)
            if error_message is None:
                raise ValueError(f"Error processing mcp-server-billing query: {str(apie)}")
            raise ValueError(error_message)
        except Exception as e:
            raise ValueError(f"Error processing mcp-server-billing query: {str(e)}")

    if server_config.transport == TRANSPORT_SSE:
        # Create an SSE transport at an endpoint
        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                    request.scope, request.receive, request._send
            ) as streams:
                await server.run(
                    streams[0], streams[1], server.create_initialization_options()
                )

        middleware = []
        if (server_config.auth == AUTH_TYPE_OAUTH or
                server_config.credential == CREDENTIAL_TYPE_TOKEN):
            middleware = [
                Middleware(SSEMiddleware)
            ]
        starlette_app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
                # 添加OAuth相关路由
                Route("/.well-known/oauth-authorization-server", endpoint=well_known),
                Route("/auth/oauth/register", endpoint=oauth_register, methods=["POST"]),
                Route("/auth/oauth/authorize", endpoint=oauth_authorize, methods=["GET"]),
                Route("/auth/oauth/callback", endpoint=oauth_callback, methods=["GET"]),
                Route("/auth/oauth/token", endpoint=oauth_token, methods=["POST"]),
            ],
            middleware=middleware
        )

        # 添加CORS中间件
        starlette_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )

        config = uvicorn.Config(starlette_app, host="0.0.0.0", port=server_config.sse_port)
        sse_server = uvicorn.Server(config)
        await sse_server.serve()
    else:
        # Create an STDIO transport
        options = server.create_initialization_options()
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, options)


# OAuth处理函数
async def well_known(request: Optional[Request]):
    """处理 .well-known/oauth-authorization-server 端点"""
    base = str(request.base_url).rstrip("/")
    return JSONResponse({
        "issuer": base,
        "registration_endpoint": f"{base}/auth/oauth/register",
        "authorization_endpoint": f"{base}/auth/oauth/authorize",
        "token_endpoint": f"{base}/auth/oauth/token",
        "scopes_supported": server_config.oauth.scope,
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "code_challenge_methods_supported": ["S256"]
    })


async def oauth_authorize(request: Optional[Request]):
    # 获取原始查询参数
    original_query = dict(request.query_params)
    redirect_uri = original_query.get("redirect_uri")
    state_obj = {"redirect_uri": redirect_uri}
    state = base64.urlsafe_b64encode(json.dumps(state_obj).encode()).decode()
    # 替换
    base = str(request.base_url).rstrip("/")
    original_query["redirect_uri"] = f"{base}/auth/oauth/callback"
    original_query["state"] = state
    # 构造最终 OAuth 授权地址
    full_url = f"{server_config.oauth.authorize_url}?{urllib.parse.urlencode(original_query)}"
    return RedirectResponse(full_url)


async def oauth_callback(request: Optional[Request]):
    # 获取原始查询参数
    original_query = dict(request.query_params)
    state = original_query.get("state")
    redirect_uri = json.loads(base64.urlsafe_b64decode(state).decode()).get("redirect_uri")
    # 构造最终 OAuth 授权地址
    full_url = f"{redirect_uri}?{urllib.parse.urlencode(original_query)}"
    return RedirectResponse(full_url)


async def oauth_register(request: Optional[Request]):
    """处理 auth/oauth/register 端点"""
    try:
        # 读取原始请求体
        body = await request.body()
        # 解析JSON数据
        data = json.loads(body)
        client_reg = OAuthClientRegistration(**data)
        return JSONResponse({
            "client_id": server_config.oauth.client_id,
            "client_id_issued_at": int(time.time()),
            "redirect_uris": client_reg.redirect_uris,
            "client_name": client_reg.client_name,
            "grant_types": client_reg.grant_types,
            "response_types": client_reg.response_types,
            "token_endpoint_auth_method": client_reg.token_endpoint_auth_method
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


token_store = {}


async def oauth_token(request: Request):
    """处理 auth/oauth/token 端点 - 从Oauth获取访问令牌"""
    try:
        # 获取请求内容类型
        content_type = request.headers.get('content-type', '')

        # 解析请求参数
        if 'application/json' in content_type:
            body = await request.body()
            params = json.loads(body)
        else:
            # 处理所有非JSON请求为表单格式
            body = await request.body()
            body_str = body.decode('utf-8')
            params = {k: v[0] for k, v in urllib.parse.parse_qs(body_str).items()}

        # 授权码模式
        code = params.get('code')
        grant_type = params.get('grant_type')
        client_id = params.get('client_id', server_config.oauth.client_id)  # 从配置获取
        client_secret = server_config.oauth.client_secret  # 从配置获取
        code_verifier = params.get('code_verifier')

        if not code:
            return JSONResponse({
                "error": "invalid_request",
                "error_description": "Missing required parameter: code"
            }, status_code=400)

        # 准备请求数据
        base = str(request.base_url).rstrip("/")
        token_request_data = {
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
            'redirect_uri': f"{base}/auth/oauth/callback",
            "code_verifier": code_verifier
        }

        # 发送请求到Oauth
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    server_config.oauth.token_url,
                    data=token_request_data,
                    headers={'Accept': 'application/json'}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    return JSONResponse({
                        "error": "oauth_token_error",
                        "error_description": f"Oauth API error: {error_text}"
                    }, status_code=response.status)

                response = await response.json()

                if 'error' in response:
                    return JSONResponse({
                        "error": response.get('error'),
                        "error_description": response.get('error_description')
                    }, status_code=400)

                token_store.setdefault(response.get('access_token'), "1")
                # 成功获取令牌，返回给客户端
                return JSONResponse({
                    "access_token": response.get('access_token'),
                    "token_type": response.get('token_type', 'bearer'),
                    "scope": response.get('scope', ''),
                    "refresh_token": response.get('refresh_token', ''),
                    "expires_in": response.get('expires_in', 0)
                })
    except Exception as e:
        return JSONResponse({
            "error": "server_error",
            "error_description": str(e)
        }, status_code=500)
