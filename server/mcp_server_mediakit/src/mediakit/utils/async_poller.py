from __future__ import annotations

import asyncio
from typing import Any, Callable


async def poll_until_complete(
    callback: Callable[[], dict],
    *,
    poll_interval_seconds: float = 10,
    max_poll_attempts: int = 0,
    poll_complete: bool = False,
) -> dict:
    """轮询任务直到完成或达到最大次数。

    Args:
        callback: 同步查询函数，返回包含 status 字段的 dict
        poll_interval_seconds: 轮询间隔（秒）
        max_poll_attempts: 最大轮询次数，0 表示仅查一次
        poll_complete: 是否阻塞直到任务完成

    Returns:
        最终查询结果 dict
    """
    attempts = 0
    while True:
        result = callback()
        status = result.get("status")
        if status in {"completed", "failed", "canceled"}:
            return result
        attempts += 1
        if not poll_complete and max_poll_attempts and attempts >= max_poll_attempts:
            return result
        if not poll_complete and max_poll_attempts == 0:
            return result
        await asyncio.sleep(max(poll_interval_seconds, 0))
