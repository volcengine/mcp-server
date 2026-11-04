from __future__ import annotations

import asyncio
import time
from typing import Any, Callable

_TERMINAL_STATUSES = {"completed", "failed", "canceled", "cancelled"}


def _capped_max_poll_attempts(
    max_poll_attempts: int,
    poll_interval_seconds: float,
    max_poll_timeout_seconds: float,
) -> int:
    if max_poll_attempts <= 0:
        return 0
    if max_poll_timeout_seconds <= 0 or poll_interval_seconds <= 0:
        return max_poll_attempts
    max_by_timeout = int(max_poll_timeout_seconds / poll_interval_seconds)
    return min(max_poll_attempts, max_by_timeout)


async def poll_until_complete(
    callback: Callable[[], dict],
    *,
    poll_interval_seconds: float = 10,
    max_poll_attempts: int = 0,
    poll_complete: bool = False,
    max_poll_timeout_seconds: float = 0,
    initial_result: dict[str, Any] | None = None,
) -> dict:
    """轮询任务直到完成、达到最大次数或超过轮询总时长上限。

    Args:
        callback: 同步查询函数，返回包含 status 字段的 dict
        poll_interval_seconds: 轮询间隔（秒）
        max_poll_attempts: 首次查询后的最大追加查询次数，0 表示仅查一次
        poll_complete: 是否阻塞直到任务完成
        max_poll_timeout_seconds: 轮询总时长上限（秒），0 表示不限制

    Returns:
        最终查询结果 dict
    """
    attempts = 0
    result = initial_result
    if result is None:
        result = callback()
    poll_started = time.monotonic()
    has_deadline = max_poll_timeout_seconds > 0
    deadline = poll_started + max_poll_timeout_seconds
    attempt_limit = _capped_max_poll_attempts(
        max_poll_attempts,
        poll_interval_seconds,
        max_poll_timeout_seconds,
    )

    def timed_out() -> bool:
        return has_deadline and time.monotonic() >= deadline

    while True:
        status = result.get("status")
        if status in _TERMINAL_STATUSES:
            return result
        if not poll_complete and max_poll_attempts == 0:
            return result
        if max_poll_attempts > 0 and attempts >= attempt_limit:
            return result
        if timed_out():
            return result
        await asyncio.sleep(max(poll_interval_seconds, 0))
        if timed_out():
            return result
        result = callback()
        attempts += 1
