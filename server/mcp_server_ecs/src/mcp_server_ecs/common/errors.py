from mcp_server_ecs.common.logs import LOG


class ToolExecutionError(Exception):
    """工具执行错误，会被框架捕获并设置 isError=True"""
    pass


def handle_error(action_name: str, error: Exception | None = None) -> None:
    """
    处理 API 错误，抛出异常让框架设置 isError=True
    
    符合 MCP 规范：通过抛出异常让框架自动设置 CallToolResult.isError = True，
    而不是返回错误文本（那样 isError 会保持 False）。

    Args:
        action_name: API action name
        error: Exception object (optional)
    
    Raises:
        ToolExecutionError: 包含错误信息的异常
    """
    if error:
        error_msg = str(error)
        LOG.error(f"Exception when calling {action_name}: {error_msg}")
        raise ToolExecutionError(error_msg) from error
    else:
        LOG.error(f"{action_name} returned empty response")
        raise ToolExecutionError("empty response")
