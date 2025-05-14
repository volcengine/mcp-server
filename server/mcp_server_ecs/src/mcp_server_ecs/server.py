"""
ECS MCP Server.

This server provides MCP tools to interact with ECS OpenAPI.
"""

import os
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Dict, TypeVar, Optional

import anyio
import uvicorn
from mcp import types
from mcp.server.lowlevel import Server
from mcp.server.sse import SseServerTransport
from mcp.server.stdio import stdio_server
from mcp.shared.context import RequestContext
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route

from mcp_server_ecs.common.config import deploy_config
from mcp_server_ecs.common.logs import LOG
from mcp_server_ecs.tools import TOOL_REGISTRY, get_tool_function, is_tool_registered


LifespanResultT = TypeVar("LifespanResultT")


class GlobalContext:
    def __init__(self):
        self.request_context: Optional[RequestContext] = None
        self.request: Optional[Request] = None

    def set_request_context(self, context: RequestContext):
        self.request_context = context

    def set_request(self, request: Request):
        self.request = request

    def get_request_headers(self) -> Dict[str, str]:
        if self.request and hasattr(self.request, 'headers'):
            return dict(self.request.headers)
        return {}


GLOBAL_CONTEXT = GlobalContext()


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[None]:
    original_handle_request = server._handle_request

    async def wrapped_handle_request(context: RequestContext, *args, **kwargs):
        GLOBAL_CONTEXT.set_request_context(context)
        if hasattr(context, 'request') and context.request:
            GLOBAL_CONTEXT.set_request(context.request)
        return await original_handle_request(context, *args, **kwargs)

    server._handle_request = wrapped_handle_request

    try:
        yield None
    finally:
        server._handle_request = original_handle_request


APP = Server("ecs", lifespan=server_lifespan)


@APP.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name=info["name"],
            description=info["description"],
            inputSchema=info["model"].model_json_schema(),
        )
        for info in TOOL_REGISTRY.values()
    ]


@APP.call_tool()
async def call_tool(name: str, args: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if not is_tool_registered(name):
        return [types.TextContent(
            type="text",
            text="Tool not found"
        )]

    try:

        tool_info = TOOL_REGISTRY[name]
        model_class = tool_info["model"]

        try:
            validated_args = model_class(**args)
            LOG.info(f"Validated args: {validated_args.model_dump()}")
        except Exception as e:
            LOG.error(f"Parameter validation error: {str(e)}")
            return [types.TextContent(
                type="text",
                text=f"Parameter validation error: {str(e)}"
            )]

        tool_function = get_tool_function(name)

        if deploy_config.get("is_local"):
            result = await tool_function(validated_args.model_dump())
        else:
            headers = GLOBAL_CONTEXT.get_request_headers()
            args_with_headers = validated_args.model_dump()
            args_with_headers['__headers'] = headers
            result = await tool_function(args_with_headers)

        return result

    except Exception as e:
        LOG.error(f"Exception: {traceback.format_exc()}")
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


def serve(transport: str):
    if transport == "sse":
        sse = SseServerTransport("/messages/")
        # vefaas
        # sse = SseServerTransport("/ecs/messages/")

        async def handle_sse(request):
            GLOBAL_CONTEXT.set_request(request)

            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await APP.run(
                    streams[0], streams[1], APP.create_initialization_options(), request=request
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
            # vefaas
            # routes=[
            #     Route("/ecs/sse", endpoint=handle_sse),
            #     Mount("/ecs/messages/", app=sse.handle_post_message),
            # ],
        )

        mcp_server_port = os.environ.get(
            "MCP_SERVER_PORT") or deploy_config.get("port")
        LOG.info(f"MCP server port: {mcp_server_port}")

        uvicorn.run(starlette_app, host="0.0.0.0", port=int(mcp_server_port))

    else:
        async def arun():
            async with stdio_server() as streams:
                await APP.run(
                    streams[0], streams[1], APP.create_initialization_options()
                )

        anyio.run(arun)
