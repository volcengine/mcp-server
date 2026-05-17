"""MediaKit API 请求客户端

封装 HTTP 请求能力，支持 GET / POST / PUT / DELETE / PATCH 等多种请求方式。
自动注入鉴权 Header（x-amk-api-key / x-mediakit-endpoint），
鉴权参数获取优先级：MCP Context > 实例变量 > 环境变量 > 默认值。

同时提供基于 api_info 路由表的高层调用接口 call(api_name, **kwargs)。

Streamable HTTP / SSE 模式下的鉴权：
  - client 持有 _mcp_instance 引用（指向 BaseMCP）
  - 每次 HTTP 请求前调用 update_auth_from_mcp() 从当前 MCP context 动态获取 headers
  - 更新到实例变量 _api_key / _endpoint，避免修改全局环境变量
"""

from __future__ import annotations

import logging
import os
from typing import Any, Optional

import httpx

from .api_info import api_info
from .constant import (
    MEDIAKIT_API_KEY_ENV,
    MEDIAKIT_API_KEY_HEADER,
    DEFAULT_ENDPOINT,
    DEFAULT_RUNTIME,
    DEFAULT_SURFACE,
    ENDPOINT_ENV,
    ENDPOINT_HEADER,
    RUNTIME_ENV,
    RUNTIME_HEADER,
)

try:
    from mcp.server.fastmcp.server import Context
    from mcp.server.session import ServerSession
except Exception:  # pragma: no cover
    class Context:  # type: ignore
        pass

    class ServerSession:  # type: ignore
        pass

logger = logging.getLogger(__name__)


class MediKitClient:
    """MediaKit API 请求客户端

    提供与 MediaKit API 交互的 HTTP 能力：
      1. 底层：get / post / put / delete / patch / request
      2. 高层：call(api_name, **kwargs) 基于 api_info 路由表自动路由

    鉴权参数（MEDIAKIT_API_KEY / MEDIAKIT_ENDPOINT）通过以下优先级获取：
      1. MCP Context Header（Streamable HTTP 模式，通过 _mcp_instance.get_context() 获取）
      2. 实例变量（_api_key / _endpoint，由 update_auth_from_mcp() 更新）
      3. 环境变量（Studio stdio 模式）
      4. 默认值（仅 MEDIAKIT_ENDPOINT，默认 DEFAULT_ENDPOINT）
    """

    DEFAULT_TIMEOUT = 30.0

    def __init__(self, timeout: float | None = None) -> None:
        self._timeout = timeout or self.DEFAULT_TIMEOUT
        self._mcp_instance: Any = None
        self._extra_headers: dict[str, str] = {}
        self._api_key: str | None = None
        self._endpoint: str | None = None
        self._runtime: str | None = None

    # ─── MCP 实例绑定 ──────────────────────────────────

    def set_mcp_instance(self, mcp_instance: Any) -> None:
        """绑定 BaseMCP 实例，用于动态获取当前请求上下文"""
        self._mcp_instance = mcp_instance

    def set_headers(self, key: str, value: str) -> None:
        """设置额外 header（如 x-tt-tools-name）"""
        self._extra_headers[key] = value

    # ─── 从 MCP Context 更新凭证 ───────────────────────

    def update_auth_from_mcp(self) -> None:
        """从 MCP context 动态更新凭证（Streamable HTTP 模式）

        每次发起 HTTP 请求前调用，将当前请求的 headers 更新到实例变量。
        """
        if self._mcp_instance is None:
            logger.debug("update_auth_from_mcp: _mcp_instance is None, skipping")
            return

        try:
            ctx = self._mcp_instance.get_context()
            if ctx is None:
                logger.debug("update_auth_from_mcp: get_context() returned None")
                return

            self._update_auth_from_context(ctx)
        except Exception as e:
            logger.debug(f"update_auth_from_mcp: failed to get context: {e}")

    def _update_auth_from_context(
        self, ctx: Optional[Context[ServerSession, object, Any]] = None
    ) -> None:
        """从 MCP context 的 headers 中提取凭证并更新到实例变量"""
        if ctx is None:
            return

        try:
            raw_request = ctx.request_context.request
            if not raw_request:
                return

            headers = raw_request.headers
            if not headers:
                return

            api_key = headers.get(MEDIAKIT_API_KEY_HEADER)
            endpoint = headers.get(ENDPOINT_HEADER)
            runtime = headers.get(RUNTIME_HEADER)

            if api_key:
                self._api_key = api_key
                logger.debug("Credentials updated from MCP context: api_key")
            if endpoint:
                self._endpoint = endpoint
                logger.debug("Credentials updated from MCP context: endpoint")
            if runtime:
                self._runtime = runtime
        except Exception as e:
            logger.warning(f"Failed to update credentials from context: {e}")

    # ─── 鉴权参数解析 ───────────────────────────────────

    def _resolve_api_key(self) -> str:
        """解析 MEDIAKIT_API_KEY

        优先级：实例变量 > 环境变量
        未找到时抛出 ValueError。
        """
        if self._api_key:
            return self._api_key
        env_val = os.environ.get(MEDIAKIT_API_KEY_ENV, "")
        if not env_val:
            raise ValueError(
                f"缺少 API Key，请通过环境变量 {MEDIAKIT_API_KEY_ENV} "
                f"或 Header {MEDIAKIT_API_KEY_HEADER} 设置"
            )
        return env_val

    def _resolve_endpoint(self) -> str:
        """解析 MEDIAKIT_ENDPOINT

        优先级：实例变量 > 环境变量 > DEFAULT_ENDPOINT
        """
        if self._endpoint:
            return self._endpoint
        return os.environ.get(ENDPOINT_ENV, "") or DEFAULT_ENDPOINT

    def _resolve_surface(self) -> str:
        return DEFAULT_SURFACE

    def _resolve_runtime(self) -> str:
        if self._runtime:
            return self._runtime
        return os.environ.get(RUNTIME_ENV, "") or DEFAULT_RUNTIME

    # ─── 请求 Header 构建 ──────────────────────────────

    def _build_request_headers(self) -> dict[str, str]:
        """构建请求 Header，注入鉴权信息"""
        api_key = self._resolve_api_key()
        headers: dict[str, str] = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "x-surface": self._resolve_surface(),
            "x-runtime": self._resolve_runtime(),
        }
        return headers

    # ─── 响应处理 ──────────────────────────────────────

    @staticmethod
    def _handle_response(response: httpx.Response) -> dict[str, Any]:
        """处理 HTTP 响应，检查状态码并解析 JSON

        非 2xx 状态码抛出 httpx.HTTPStatusError。
        """
        response.raise_for_status()
        return response.json()

    # ─── 通用请求方法 ──────────────────────────────────

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """通用 HTTP 请求方法

        每次请求前自动调用 update_auth_from_mcp() 更新凭证。

        Args:
            method: HTTP 方法（GET / POST / PUT / DELETE / PATCH）
            path: API 路径，如 /api/v1/tools/trim-video
            headers: 额外请求 Header
            params: URL 查询参数
            json: JSON 请求体
            data: Form 请求体

        Returns:
            API 响应 JSON 解析结果

        Raises:
            ValueError: 缺少 MEDIAKIT_API_KEY
            httpx.HTTPStatusError: API 返回非 2xx 状态码
        """
        self.update_auth_from_mcp()
        request_headers = self._build_request_headers()
        endpoint = self._resolve_endpoint()
        url = f"{endpoint.rstrip('/')}/{path.lstrip('/')}"

        with httpx.Client(timeout=self._timeout) as client:
            response = client.request(
                method=method.upper(),
                url=url,
                headers=request_headers,
                params=params,
                json=json,
                data=data,
            )
        return self._handle_response(response)

    # ─── 便捷方法 ──────────────────────────────────────

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """GET 请求，参数走 query string"""
        return self.request("GET", path, headers=headers, params=params)

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """POST 请求，支持 JSON body 或 form data"""
        return self.request("POST", path, headers=headers, json=json, data=data)

    def put(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """PUT 请求"""
        return self.request("PUT", path, headers=headers, json=json, data=data)

    def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """DELETE 请求"""
        return self.request("DELETE", path, headers=headers, params=params)

    def patch(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """PATCH 请求"""
        return self.request("PATCH", path, headers=headers, json=json, data=data)

    # ─── 基于 api_info 路由表的高层调用 ────────────────

    def call(
        self,
        api_name: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """根据 api_info 路由表调用指定 API。

        路径中的占位符（如 {task_id}）会从 kwargs 中提取并替换，
        剩余的参数作为 query params 或 json body 传入。

        Args:
            api_name: API 名称（snake_case），如 "query_task"
            **kwargs: 请求参数
                - 路径参数：匹配 path 中的 {xxx} 占位符
                - GET / DELETE：剩余参数作为 query params 传入
                - POST / PUT / PATCH：剩余参数作为 json body 传入

        Returns:
            API 响应 JSON

        Raises:
            KeyError: api_info 中不存在该 API
            httpx.HTTPStatusError: API 返回非 2xx 状态码
        """
        route = api_info[api_name]
        method = route["method"].upper()
        path = route["path"]

        # 提取路径参数并替换占位符
        path_params = {}
        remaining_kwargs = dict(kwargs)
        for key in list(remaining_kwargs.keys()):
            placeholder = "{" + key + "}"
            if placeholder in path:
                path_params[key] = remaining_kwargs.pop(key)
        path = path.format(**path_params)
        remaining_kwargs = {
            key: value for key, value in remaining_kwargs.items() if value is not None
        }

        if method == "GET":
            return self.get(path, params=remaining_kwargs)
        if method == "POST":
            return self.post(path, json=remaining_kwargs)
        if method == "PUT":
            return self.put(path, json=remaining_kwargs)
        if method == "DELETE":
            return self.delete(path, params=remaining_kwargs)
        if method == "PATCH":
            return self.patch(path, json=remaining_kwargs)

        return self.request(method, path, json=remaining_kwargs)


# ─── 工厂函数 ──────────────────────────────────────

def create_client(timeout: float | None = None) -> MediKitClient:
    """创建新的 MediKitClient 实例。

    每个请求使用独立 client 实例，避免并发场景下鉴权信息冲突。
    实际并发安全由 update_auth_from_mcp() 保证（动态获取当前请求上下文）。
    """
    return MediKitClient(timeout=timeout)
