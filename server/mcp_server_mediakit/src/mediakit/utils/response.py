from __future__ import annotations
from typing import Any

QUERY_RESERVED_FIELDS = frozenset(
    {"task_id", "task_type", "request_id", "status", "success", "error", "result"}
)
QUERY_IGNORED_RESULT_FIELDS = frozenset({"usage"})

def _non_empty_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text == "<nil>":
        return None
    return text

def _is_failure_envelope(payload: dict[str, Any]) -> bool:
    if not payload or "error" not in payload:
        return False
    success = payload.get("success")
    return isinstance(success, bool) and not success

def _is_business_failure(payload: dict[str, Any]) -> bool:
    success = payload.get("success")
    return isinstance(success, bool) and not success

def _is_terminal_failure(payload: dict[str, Any]) -> bool:
    status = (_non_empty_string(payload.get("status")) or "").lower()
    return status in {"failed", "canceled", "cancelled"}

def _is_completed_task_status(payload: dict[str, Any]) -> bool:
    status = (_non_empty_string(payload.get("status")) or "").lower()
    return status == "completed"

def _business_failure_response(payload: dict[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {"success": False}
    error_field = payload.get("error")
    output["error"] = error_field if error_field is not None else "unknown error"
    if task_id := _non_empty_string(payload.get("task_id")):
        output["task_id"] = task_id
    if task_type := _non_empty_string(payload.get("task_type")):
        output["task_type"] = task_type
    if request_id := _non_empty_string(payload.get("request_id")):
        output["request_id"] = request_id
    if status := _non_empty_string(payload.get("status")):
        output["status"] = status
    return output

def error_response(error: object = None, **metadata: Any) -> dict[str, Any]:
    if isinstance(error, dict) and _is_failure_envelope(error):
        output = _business_failure_response(error)
        output.update({key: value for key, value in metadata.items() if value is not None})
        return output
    output: dict[str, Any] = {"success": False, "error": error or "unknown error"}
    output.update({key: value for key, value in metadata.items() if value is not None})
    return output

def async_task_response(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        return error_response(None)
    if _is_business_failure(result):
        return _business_failure_response(result)
    task_id = result.get("task_id")
    if not isinstance(task_id, str) or not task_id:
        return error_response({"message": "missing non-empty task_id"})
    output = {key: result[key] for key in ("task_id", "task_type", "request_id") if result.get(key) not in (None, "")}
    if isinstance(result.get("success"), bool):
        output["success"] = result["success"]
    return output

def sync_result_response(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        return error_response(None)
    if _is_business_failure(result):
        return _business_failure_response(result)
    task_result = result.get("result")
    if not isinstance(task_result, dict):
        return error_response({"message": "missing result object"})
    output = dict(task_result)
    if result.get("request_id") is not None:
        output["request_id"] = result["request_id"]
    if result.get("usage") is not None:
        output["usage"] = result["usage"]
    return output

def query_task_response(result: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(result, dict):
        return error_response(None)
    if not result:
        return {}
    output: dict[str, Any] = {
        "task_id": _non_empty_string(result.get("task_id")) or "",
    }
    if task_type := _non_empty_string(result.get("task_type")):
        output["task_type"] = task_type
    if request_id := _non_empty_string(result.get("request_id")):
        output["request_id"] = request_id
    if status := _non_empty_string(result.get("status")):
        output["status"] = status
    task_result = result.get("result")
    if isinstance(task_result, dict):
        output["result"] = {
            key: value
            for key, value in task_result.items()
            if key not in QUERY_IGNORED_RESULT_FIELDS
        }
    if _is_business_failure(result) or _is_terminal_failure(result):
        output["success"] = False
        error_field = result.get("error")
        output["error"] = error_field if error_field is not None else "unknown error"
    output.pop("usage", None)
    if (
        _is_completed_task_status(result)
        and not _is_business_failure(result)
        and not _is_terminal_failure(result)
        and result.get("usage") is not None
    ):
        output["usage"] = result["usage"]
    return output
