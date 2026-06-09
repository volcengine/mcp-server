from __future__ import annotations

from typing import Optional

try:
    from pydantic import Field
except Exception:  # pragma: no cover
    def Field(*args, **kwargs):
        if args:
            return args[0]
        return kwargs.get("default", None)

try:
    from mcp.server.fastmcp.server import Context
    from mcp.server.session import ServerSession
except Exception:  # pragma: no cover
    class Context:  # type: ignore
        pass

    class ServerSession:  # type: ignore
        pass

from base.client import MediKitClient
from ..utils.async_poller import poll_until_complete
from ..utils.response import error_response, query_task_response


# 本 domain 注册的 tool 名称列表
TOOL_NAMES = ["query_task"]


def register_tools(mcp, client: MediKitClient) -> None:
    @mcp.tool(
        name="query_task",
        description="查询异步任务状态。提交异步任务后使用此工具获取结果。推荐使用 poll_interval_seconds + max_poll_attempts 控制轮询，例如 poll_interval_seconds=2、max_poll_attempts=10。传递这两个参数时，不需要再传 poll_complete【不推荐】。单次调用时长 poll_interval_seconds * max_poll_attempts 建议不超过 30s，避免服务与 client 断链；若未查到终态，建议再次发起查询。",
    )
    async def query_task(
        task_id: str = Field(..., description="异步任务 ID，由异步能力提交后返回"),
        poll_interval_seconds: Optional[float] = Field(10, description="轮询间隔（秒）。推荐与 max_poll_attempts 搭配使用，例如 2。"),
        max_poll_attempts: Optional[int] = Field(0, description="最大轮询次数。0 表示仅查一次不轮询。推荐与 poll_interval_seconds 搭配使用，例如 10。"),
        poll_complete: Optional[bool] = Field(False, description="是否阻塞直到任务完成。推荐使用 poll_interval_seconds + max_poll_attempts 控制轮询；传递这两个参数时通常不需要再传 poll_complete。"),
        *,
        ctx: Context,
    ) -> dict:
        """查询异步任务状态。"""
        try:
            def _do_query() -> dict:
                return client.call(api_name="query_task", task_id=task_id)

            result = _do_query()

            # 如果配置了轮询且任务未终态，进入轮询逻辑
            status = result.get("status")
            if status not in {"completed", "failed", "canceled"}:
                if poll_complete or max_poll_attempts > 0:
                    result = await poll_until_complete(
                        _do_query,
                        poll_interval_seconds=poll_interval_seconds or 10,
                        max_poll_attempts=max_poll_attempts or 0,
                        poll_complete=poll_complete or False,
                    )

            return query_task_response(result)
        except Exception as exc:
            return error_response(str(exc))

    # 注册 domain -> tools 映射
    if hasattr(mcp, "register_domain_tools"):
        mcp.register_domain_tools("shared", TOOL_NAMES)
