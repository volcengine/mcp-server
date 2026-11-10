"""工具和物理 API 调用的观测边界，不记录业务参数或凭据。"""

import asyncio
import json
import logging
from contextlib import ExitStack, contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from time import monotonic
from uuid import uuid4

from opentelemetry import trace
from opentelemetry.trace import StatusCode

_LOGGER = logging.getLogger("mcp_server_sms.calls")
_CORRELATION = ContextVar("sms_call_correlation", default=None)


@dataclass
class CallObservation:
    result_class: str = "pending"
    error_code: str | None = None
    request_id: str | None = None

    def record(self, result: dict):
        error = result.get("error") or {}
        self.result_class = (
            "success"
            if result["success"]
            else "unknown"
            if error.get("outcome_unknown")
            else "failed"
        )
        self.error_code = error.get("code")
        self.request_id = result.get("request_id")


def _emit(event, fields, span=None):
    try:
        _LOGGER.info("sms_call %s", json.dumps({"event": event, **fields}, ensure_ascii=False))
    except Exception:
        pass  # 日志旁路失败不影响短信调用。
    if span is not None:
        try:
            span.add_event(
                event, {key: value for key, value in fields.items() if value is not None}
            )
        except Exception:
            pass  # Trace 旁路失败不影响短信调用。


@contextmanager
def observe_call(kind: str, action: str, *, path: str | None = None):
    """为调用生命周期记录成对事件，并沿当前异步上下文传递关联标识。"""
    correlation = _CORRELATION.get() or uuid4().hex
    token = _CORRELATION.set(correlation)
    fields = {"kind": kind, "action": action, "correlation_id": correlation}
    if path is not None:
        fields["path"] = path
    stack, span = ExitStack(), None
    try:
        span = stack.enter_context(
            trace.get_tracer("mcp_server_sms").start_as_current_span(
                "sms." + kind,
                attributes=fields,
                record_exception=False,
                set_status_on_exception=False,
            )
        )
    except Exception:
        pass
    state = CallObservation()
    started = monotonic()
    _emit("start", fields, span)
    try:
        yield state
    except BaseException as exc:
        if state.result_class == "pending":
            state.result_class = (
                "cancelled" if isinstance(exc, asyncio.CancelledError) else "failed"
            )
            state.error_code = type(exc).__name__
        raise
    finally:
        fields.update(
            duration_ms=int((monotonic() - started) * 1000),
            result_class=state.result_class,
            error_code=state.error_code,
            request_id=state.request_id,
        )
        _emit("end", fields, span)
        try:
            if span is not None and state.result_class != "success":
                span.set_status(StatusCode.ERROR)
        except Exception:
            pass
        finally:
            try:
                stack.close()
            except Exception:
                pass
            finally:
                _CORRELATION.reset(token)
