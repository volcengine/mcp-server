import logging
from functools import wraps
from typing import Callable

from .common import to_json

logger = logging.getLogger(__name__)


def _format_error(e: Exception) -> str:
    error_msg = str(e) if str(e) else f"{type(e).__name__}"
    return error_msg


def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> str:
        try:
            result = await func(*args, **kwargs)
            if isinstance(result, str):
                return result
            if isinstance(result, list):
                if result and hasattr(result[0], 'model_dump'):
                    result = [item.model_dump() for item in result]
            elif hasattr(result, 'model_dump'):
                result = result.model_dump()
            return to_json(result)
        except Exception as e:
            error_msg = _format_error(e)
            logger.error(f"Error in {func.__name__}: {error_msg}")
            return to_json({"error": error_msg})
    return wrapper
