from __future__ import annotations

from typing import Any


def async_task_response(result: dict[str, Any]) -> dict[str, Any]:
    """异步处理任务 — 从 API 响应中提取 task_id / request_id 返回。

    Returns:
        { "task_id": "xxx", "request_id": "xxx" }
    """
    if not isinstance(result, dict):
        return {"task_id": None}
    output: dict[str, Any] = {"task_id": result.get("task_id")}
    request_id = result.get("request_id")
    if request_id is not None:
        output["request_id"] = request_id
    return output


def query_task_response(result: dict[str, Any]) -> dict[str, Any]:
    """查询任务结果 — 外层保留 task_id/request_id/status，将 result 中的字段解构平铺到外层。

    API 返回结构: { task_id, request_id, success, task_type, status, result: { duration, resolution, video_url } }
    处理后返回: { task_id, request_id, status, duration, resolution, video_url }
    """
    if not isinstance(result, dict):
        return {}

    task_id = result.get("task_id")
    request_id = result.get("request_id")
    status = result.get("status")
    task_result = result.get("result") or {}

    output: dict[str, Any] = {"task_id": task_id}
    if request_id is not None:
        output["request_id"] = request_id
    if status is not None:
        output["status"] = status
    if isinstance(task_result, dict):
        output.update(task_result)
    return output


def error_response(
    error: dict[str, Any] | str | None = None,
    *,
    task_id: str | None = None,
    request_id: str | None = None,
) -> dict[str, Any]:
    """报错响应结构。

    支持两种输入：
    - API 错误响应（dict）：提取 error.message 或 error.error 字段
    - 程序异常（str）：直接使用异常信息

    Returns:
        { "task_id": "xxx", "request_id": "xxx", "error": "message字段的内容" }
    """
    message = ""
    if isinstance(error, dict):
        message = error.get("message") or error.get("error", "") or error.get("msg", "") 
    elif isinstance(error, str):
        message = error
    result: dict[str, Any] = {"error": message}
    if task_id is not None:
        result["task_id"] = task_id
    if request_id is not None:
        result["request_id"] = request_id
    return result
