import argparse
import asyncio
import base64
import json
import os
import socket
import sys
from dataclasses import dataclass
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamablehttp_client


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTTP_PORT = 8765
REQUIRED_ENV_VARS = (
    "VOLCENGINE_ACCESS_KEY",
    "VOLCENGINE_SECRET_KEY",
    "VOLCENGINE_SESSION_TOKEN",
)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str
    required: bool = True


def _ensure_required_env_vars() -> None:
    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing:
        raise RuntimeError("Missing required environment variables: " + ", ".join(missing))


def _resolve_region(cli_region: str | None) -> str:
    return cli_region or os.getenv("VOLCENGINE_REGION") or "cn-beijing"


def _build_sts_header(region: str, expired: bool = False) -> str:
    payload = {
        "AccessKeyId": os.environ["VOLCENGINE_ACCESS_KEY"],
        "SecretAccessKey": os.environ["VOLCENGINE_SECRET_KEY"],
        "SessionToken": os.environ["VOLCENGINE_SESSION_TOKEN"],
        "CurrentTime": "2026-06-01T16:00:00+08:00",
        "ExpiredTime": "2026-06-01T17:00:00+08:00",
        "Region": region,
    }
    if expired:
        payload["CurrentTime"] = "2026-06-01T18:00:00+08:00"
        payload["ExpiredTime"] = "2026-06-01T17:00:00+08:00"
    encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    return f"Bearer {encoded}"


def _extract_text(result) -> str:
    content = getattr(result, "content", []) or []
    if not content:
        return ""
    return "\n".join(getattr(item, "text", str(item)) for item in content)


def _extract_structured_content(result):
    return getattr(result, "structuredContent", None)


async def _run_stdio_positive(region: str) -> CheckResult:
    env = {
        "VOLCENGINE_ACCESS_KEY": os.environ["VOLCENGINE_ACCESS_KEY"],
        "VOLCENGINE_SECRET_KEY": os.environ["VOLCENGINE_SECRET_KEY"],
        "VOLCENGINE_SESSION_TOKEN": os.environ["VOLCENGINE_SESSION_TOKEN"],
    }
    if os.getenv("VOLCENGINE_REGION"):
        env["VOLCENGINE_REGION"] = os.environ["VOLCENGINE_REGION"]

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server_redis.server", "--transport", "stdio"],
        env=env,
        cwd=PROJECT_ROOT,
    )
    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = await session.list_tools()
            result = await session.call_tool("describe_db_instances", {"region_id": region, "page_size": 1})

    tool_names = [tool.name for tool in tools.tools]
    data = _extract_structured_content(result) or {}
    if result.isError:
        return CheckResult("stdio + STS env", False, _extract_text(result))
    if "describe_db_instances" not in tool_names:
        return CheckResult("stdio + STS env", False, "Tool list does not include describe_db_instances")
    instance_count = data.get("total_instances_num", "unknown")
    return CheckResult("stdio + STS env", True, f"Tool call succeeded, total_instances_num={instance_count}")


async def _run_stdio_missing_token_control(region: str) -> CheckResult:
    env = {
        "VOLCENGINE_ACCESS_KEY": os.environ["VOLCENGINE_ACCESS_KEY"],
        "VOLCENGINE_SECRET_KEY": os.environ["VOLCENGINE_SECRET_KEY"],
    }
    if os.getenv("VOLCENGINE_REGION"):
        env["VOLCENGINE_REGION"] = os.environ["VOLCENGINE_REGION"]

    server = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_server_redis.server", "--transport", "stdio"],
        env=env,
        cwd=PROJECT_ROOT,
    )
    async with stdio_client(server) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("describe_db_instances", {"region_id": region, "page_size": 1})

    if result.isError:
        return CheckResult(
            "stdio missing session token control",
            True,
            "Call failed as expected: " + _extract_text(result).strip(),
            required=False,
        )
    return CheckResult(
        "stdio missing session token control",
        False,
        "Call still succeeded without VOLCENGINE_SESSION_TOKEN; current AK/SK may not be STS-only credentials.",
        required=False,
    )


async def _wait_for_port(host: str, port: int, timeout_seconds: float = 15) -> None:
    deadline = asyncio.get_running_loop().time() + timeout_seconds
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            if asyncio.get_running_loop().time() >= deadline:
                raise TimeoutError(f"Timed out waiting for server at {host}:{port}")
            await asyncio.sleep(0.2)


async def _start_http_server(port: int):
    env = os.environ.copy()
    for name in (
        "VOLCENGINE_ACCESS_KEY",
        "VOLCENGINE_SECRET_KEY",
        "VOLCENGINE_SESSION_TOKEN",
        "VOLCENGINE_REGION",
        "authorization",
        "AUTHORIZATION",
    ):
        env.pop(name, None)
    env["MCP_SERVER_PORT"] = str(port)
    env["PYTHONUNBUFFERED"] = "1"

    process = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "mcp_server_redis.server",
        "--transport",
        "streamable-http",
        cwd=str(PROJECT_ROOT),
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    await _wait_for_port("127.0.0.1", port)
    return process


async def _stop_http_server(process) -> None:
    if process.returncode is not None:
        return
    process.terminate()
    try:
        await asyncio.wait_for(process.wait(), timeout=5)
    except asyncio.TimeoutError:
        process.kill()
        await process.wait()


async def _run_http_positive(region: str, port: int) -> CheckResult:
    process = await _start_http_server(port)
    try:
        async with streamablehttp_client(
            f"http://127.0.0.1:{port}/mcp",
            headers={"Authorization": _build_sts_header(region)},
        ) as streams:
            read_stream, write_stream, _ = streams
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool("describe_db_instances", {"region_id": region, "page_size": 1})
        data = _extract_structured_content(result) or {}
        if result.isError:
            return CheckResult("streamable-http + Authorization STS", False, _extract_text(result))
        instance_count = data.get("total_instances_num", "unknown")
        return CheckResult(
            "streamable-http + Authorization STS",
            True,
            f"Tool call succeeded, total_instances_num={instance_count}",
        )
    finally:
        await _stop_http_server(process)


async def _run_http_expired_token_control(region: str, port: int) -> CheckResult:
    process = await _start_http_server(port)
    try:
        async with streamablehttp_client(
            f"http://127.0.0.1:{port}/mcp",
            headers={"Authorization": _build_sts_header(region, expired=True)},
        ) as streams:
            read_stream, write_stream, _ = streams
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool("describe_db_instances", {"region_id": region, "page_size": 1})
        if result.isError and "STS token is expired" in _extract_text(result):
            return CheckResult(
                "streamable-http expired token control",
                True,
                "Expired header was rejected as expected.",
            )
        if result.isError:
            return CheckResult(
                "streamable-http expired token control",
                False,
                "Call failed, but not with the expected expiration error: " + _extract_text(result).strip(),
            )
        return CheckResult(
            "streamable-http expired token control",
            False,
            "Expired STS header unexpectedly succeeded.",
        )
    finally:
        await _stop_http_server(process)


def _print_result(result: CheckResult) -> None:
    status = "PASS" if result.passed else ("WARN" if not result.required else "FAIL")
    requirement = "required" if result.required else "optional"
    print(f"[{status}] {result.name} ({requirement})")
    print(f"       {result.detail}")


async def _main_async(region: str, port: int) -> int:
    results = [
        await _run_stdio_positive(region),
        await _run_stdio_missing_token_control(region),
        await _run_http_positive(region, port),
        await _run_http_expired_token_control(region, port + 1),
    ]

    print(f"Redis MCP STS verification started, region={region}, http_port={port}")
    for result in results:
        _print_result(result)

    required_failures = [result for result in results if result.required and not result.passed]
    if required_failures:
        print("\nOverall result: FAIL")
        return 1

    print("\nOverall result: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Redis MCP STS support end-to-end")
    parser.add_argument("--region", help="Region used for Redis API calls. Defaults to VOLCENGINE_REGION or cn-beijing")
    parser.add_argument("--http-port", type=int, default=DEFAULT_HTTP_PORT, help="Base port used for streamable-http verification")
    args = parser.parse_args()

    _ensure_required_env_vars()
    region = _resolve_region(args.region)
    return asyncio.run(_main_async(region, args.http_port))


if __name__ == "__main__":
    raise SystemExit(main())
