"""Stateless MCP transport and authenticated file exchange; no user interface."""

import asyncio
import contextlib
from urllib.parse import urlsplit

from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount, Route

from .auth import AuthenticationError
from .core.qualification_upload import QualificationUploadError
from .inputs import INPUT_LIMITS
from .store import StoreError


def create_app(runtime, mcp):
    settings = runtime.settings
    settings.validate_http()
    public_url = settings.public_url.rstrip("/")

    async def metadata(request):
        return JSONResponse(
            {
                "resource": public_url + "/mcp",
                "authorization_servers": [settings.oidc_issuer],
                "bearer_methods_supported": ["header"],
            }
        )

    async def upload_file(request):
        kind = request.query_params.get("kind")
        maximum = INPUT_LIMITS.get(kind)
        if maximum is None:
            return JSONResponse({"error": "unsupported_file_kind"}, status_code=400)
        body = bytearray()
        async for chunk in request.stream():
            body.extend(chunk)
            if len(body) > maximum:
                return JSONResponse({"error": "file_too_large"}, status_code=413)
        content_type = request.headers.get("content-type", "").split(";", 1)[0]
        result = await asyncio.to_thread(
            runtime.inputs.stage, request.state.owner, kind, bytes(body), content_type
        )
        return JSONResponse(result, status_code=201)

    async def read_file(request):
        # A trusted host uses this endpoint for customer review, outside model
        # context. No MCP tool returns these private bytes or upload credentials.
        content, content_type = await asyncio.to_thread(
            runtime.inputs.read, request.path_params["file_id"], request.state.owner
        )
        return Response(content, media_type=content_type)

    async def health(request):
        return JSONResponse({"status": "ok"})

    async def handled_error(request, error):
        message = (
            "材料文件处理失败"
            if isinstance(error, QualificationUploadError)
            else str(error)
        )
        return JSONResponse({"success": False, "message": message}, status_code=409)

    mcp_app = mcp.streamable_http_app(
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=[urlsplit(public_url).netloc],
            allowed_origins=[public_url],
        ),
    )

    @contextlib.asynccontextmanager
    async def lifespan(app):
        async def cleanup():
            while True:
                await asyncio.sleep(60)
                try:
                    await asyncio.to_thread(runtime.store.cleanup)
                except Exception:
                    import logging

                    logging.getLogger(__name__).warning("Expired record cleanup failed")

        async with mcp_app.router.lifespan_context(mcp_app):
            task = asyncio.create_task(cleanup())
            try:
                yield
            finally:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task

    app = Starlette(
        routes=[
            Route("/health", health),
            Route("/.well-known/oauth-protected-resource", metadata),
            Route("/.well-known/oauth-protected-resource/mcp", metadata),
            Route("/files", upload_file, methods=["POST"]),
            Route("/files/{file_id}", read_file),
            Mount("/", app=mcp_app),
        ],
        lifespan=lifespan,
        exception_handlers={
            StoreError: handled_error,
            QualificationUploadError: handled_error,
        },
    )

    class Boundary:
        async def __call__(self, scope, receive, send):
            if scope["type"] != "http":
                return await app(scope, receive, send)
            request = Request(scope)
            if scope["path"].rstrip("/") in ("/mcp", "/files") or scope[
                "path"
            ].startswith("/files/"):
                try:
                    request.state.owner = await asyncio.to_thread(
                        runtime.auth.owner, request.headers
                    )
                except AuthenticationError:
                    return await JSONResponse(
                        {"error": "unauthorized"},
                        status_code=401,
                        headers={
                            "WWW-Authenticate": f'Bearer resource_metadata="{public_url}/.well-known/oauth-protected-resource/mcp"'
                        },
                    )(scope, receive, send)

            async def secured_send(message):
                if message["type"] == "http.response.start":
                    message = {
                        **message,
                        "headers": [
                            *message.get("headers", []),
                            (b"cache-control", b"no-store"),
                            (b"x-content-type-options", b"nosniff"),
                            (
                                b"content-security-policy",
                                b"default-src 'none'; frame-ancestors 'none'",
                            ),
                        ],
                    }
                await send(message)

            return await app(scope, receive, secured_send)

    return Boundary()
