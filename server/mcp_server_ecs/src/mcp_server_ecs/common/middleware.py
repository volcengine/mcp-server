"""
MCP Server Metrics 中间件

用于统计工具调用次数、成功/失败率、耗时等指标。
输出结构化日志，便于 TLS 等日志采集系统解析统计。

实现原理:
    通过替换 MCP Server 底层的 CallToolRequest handler，
    在请求处理层面拦截所有工具调用，实现真正的中间件效果。

使用方式:
    from mcp_server_ecs.common.middleware import install_metrics_handler
    
    mcp = FastMCP("ECS MCP Server", ...)
    
    # 在所有 @mcp.tool() 注册完成后，启动前调用
    install_metrics_handler(mcp)

日志输出格式:
    [MCP_METRICS] {"timestamp": 1701590400.123, "type": "tool_call", "tool": "describe_instances", "status": "success", "duration_ms": 45.23}
"""

import json
import time
from typing import TYPE_CHECKING

from mcp import types

from mcp_server_ecs.common.logs import LOG

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP

# 日志前缀，便于 TLS 过滤
LOG_PREFIX = "[MCP_METRICS]"


def _log_metric(**kwargs) -> None:
    """输出结构化日志"""
    log_data = {
        "timestamp": time.time(),
        "type": "tool_call",
        **kwargs
    }
    metric_log = f"{LOG_PREFIX} {json.dumps(log_data, ensure_ascii=False)}"
    LOG.info(metric_log)


def install_metrics_handler(mcp: "FastMCP") -> None:
    """
    安装 metrics handler，拦截所有 CallToolRequest
    
    这是真正的中间件方案，通过替换底层 request handler 实现，
    不需要修改任何工具代码，对所有工具调用生效。
    
    注意: 必须在所有 @mcp.tool() 注册完成后调用
    
    Args:
        mcp: FastMCP 实例
    
    TLS 采集配置建议:
    - 过滤规则: 包含 "[MCP_METRICS]"
    - JSON 解析: 提取日志中的 JSON 部分
    - 聚合统计: count by tool, status
    """
    server = mcp._mcp_server
    original_handler = server.request_handlers[types.CallToolRequest]
    
    async def metrics_handler(req: types.CallToolRequest) -> types.ServerResult:
        """带 metrics 统计的 CallToolRequest handler"""
        tool_name = req.params.name if req.params else "unknown"
        start_time = time.time()
        
        try:
            result = await original_handler(req)
            duration_ms = (time.time() - start_time) * 1000
            
            # result 是 ServerResult，内部包含 CallToolResult
            # 需要检查 result.root.isError
            is_error = False
            error_msg = None
            if hasattr(result, 'root') and hasattr(result.root, 'isError'):
                is_error = result.root.isError
                # 如果是错误，提取错误信息
                if is_error and hasattr(result.root, 'content'):
                    for content in result.root.content:
                        if hasattr(content, 'text'):
                            error_msg = content.text
                            break
            
            metric_data = {
                "tool": tool_name,
                "status": "error" if is_error else "success",
                "duration_ms": round(duration_ms, 2),
            }
            if error_msg:
                metric_data["error_msg"] = error_msg
            
            _log_metric(**metric_data)
            return result
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            
            _log_metric(
                tool=tool_name,
                status="error",
                duration_ms=round(duration_ms, 2),
                error_type=type(e).__name__,
                error_msg=str(e),
            )
            raise
    
    # 替换 handler
    server.request_handlers[types.CallToolRequest] = metrics_handler
    LOG.info("MCP metrics handler installed - all tool calls will be monitored")
