"""Opt-in acceptance through a standard MCP client and real delegated SMS identity.

Uses the official Skill's credential resolver in-process after browser login.
Credentials are never printed, written to a file, or passed in argv. This client
only invokes the explicit read-only tools below; it cannot send SMS or apply for
qualifications. The server runs from the exact wheel that will be distributed.
"""

import argparse
import asyncio
import importlib
import json
import pathlib
import shutil
import sys
import subprocess
import time
import tempfile

from cryptography.fernet import Fernet
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client, get_default_environment

READ_TOOLS = (
    ("list_message_groups", {}),
    ("list_qualifications", {"page": 1, "page_size": 10}),
    ("list_signatures", {"page": 1, "page_size": 10}),
    ("list_templates", {"page": 1, "page_size": 10}),
)


def tool_payload(result):
    if isinstance(result.structured_content, dict):
        return result.structured_content
    texts = [
        item.text for item in result.content if getattr(item, "type", "") == "text"
    ]
    try:
        value = json.loads("\n".join(texts))
        return value if isinstance(value, dict) else {}
    except (ValueError, TypeError):
        return {}


def summarize(name, result):
    payload = tool_payload(result)
    if not payload:
        return {"tool": name, "status": "failed", "error": "non_structured_tool_error"}
    error = payload.get("error") or {}
    value = payload.get("result")
    count = None
    if isinstance(value, list):
        count = len(value)
    elif isinstance(value, dict):
        for key in ("List", "list", "Items", "items"):
            if isinstance(value.get(key), list):
                count = len(value[key])
                break
    return {
        "tool": name,
        "status": "failed"
        if result.is_error or payload.get("success") is False
        else "passed",
        "requestId": payload.get("request_id"),
        "errorCode": error.get("code"),
        "returnedCount": count,
    }


async def run(args):
    # Reuse the supported Skill implementation; do not parse its cache ourselves.
    sys.path.insert(0, str(pathlib.Path(args.skill_dir).resolve() / "scripts"))
    skill_api = importlib.import_module("api_client")
    uvx = shutil.which("uvx")
    if not uvx:
        raise RuntimeError("uvx is required")
    command = [
        uvx,
        "--python",
        sys.executable,
        "--from",
        str(pathlib.Path(args.wheel).resolve()),
        "mcp-server-sms",
    ]
    installed_at = time.monotonic()
    installation = subprocess.run(
        command + ["--help"],
        env={**get_default_environment(), "UV_CACHE_DIR": args.cache_dir},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )
    if installation.returncode:
        print(
            json.dumps(
                {
                    "stage": "install_failed",
                    "error": installation.stderr.decode(errors="replace")[:1000],
                }
            ),
            flush=True,
        )
        return 1
    print(
        json.dumps(
            {
                "stage": "installed",
                "elapsedSeconds": round(time.monotonic() - installed_at, 2),
            }
        ),
        flush=True,
    )
    client = skill_api.SmsApiClient()
    credentials = client._credential_resolver.resolve()

    with tempfile.TemporaryDirectory(prefix="sms-mcp-live-") as directory:
        parameters = StdioServerParameters(
            command=uvx,
            args=[
                "--python",
                sys.executable,
                "--from",
                str(pathlib.Path(args.wheel).resolve()),
                "mcp-server-sms",
                "--transport",
                "stdio",
            ],
            env={
                "UV_CACHE_DIR": args.cache_dir,
                "SMS_MCP_DATABASE_URL": "sqlite:///"
                + str(pathlib.Path(directory) / "state.db"),
                "SMS_MCP_ENCRYPTION_KEY": Fernet.generate_key().decode(),
                "SMS_MCP_LOCAL_SUBJECT": "live-readonly-acceptance",
                "VOLCENGINE_ACCESS_KEY": credentials.access_key,
                "VOLCENGINE_SECRET_KEY": credentials.secret_key,
                "VOLCENGINE_SESSION_TOKEN": credentials.session_token,
            },
        )

        def safe_errors(error):
            if isinstance(error, BaseExceptionGroup):
                return [
                    item for nested in error.exceptions for item in safe_errors(nested)
                ]
            return [
                {
                    "type": type(error).__name__,
                    "message": skill_api.sanitize_output(
                        str(error), secrets=tuple(parameters.env.values())
                    ),
                }
            ]

        try:
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(
                    read, write, read_timeout_seconds=60
                ) as session:
                    await session.discover()
                    tools = await session.list_tools()
                    print(
                        json.dumps(
                            {
                                "stage": "connected",
                                "transport": "stdio",
                                "protocolVersion": session.protocol_version,
                                "toolCount": len(tools.tools),
                            },
                            ensure_ascii=False,
                        ),
                        flush=True,
                    )
                    checks = (
                        (("list_message_groups", {"name": args.group_name}),)
                        if args.group_name is not None
                        else READ_TOOLS
                    )
                    for name, arguments in checks:
                        result = await session.call_tool(name, arguments)
                        summary = summarize(name, result)
                        if (
                            args.group_name is not None
                            and summary["status"] == "passed"
                        ):
                            data = tool_payload(result).get("result", {})
                            rows = (
                                data
                                if isinstance(data, list)
                                else next(
                                    (
                                        data[key]
                                        for key in ("List", "list", "Items", "items")
                                        if isinstance(data.get(key), list)
                                    ),
                                    [],
                                )
                            )
                            summary["firstItemKeys"] = (
                                list(rows[0])
                                if rows and isinstance(rows[0], dict)
                                else []
                            )
                            summary["groups"] = [
                                {
                                    "id": row.get("SubAccount"),
                                    "name": row.get("SubAccountName"),
                                }
                                for row in rows[:10]
                            ]
                        print(json.dumps(summary, ensure_ascii=False), flush=True)
                        if summary["status"] != "passed":
                            return 1
        except Exception as error:
            print(
                json.dumps(
                    {"stage": "client_failed", "errors": safe_errors(error)},
                    ensure_ascii=False,
                ),
                flush=True,
            )
            return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True)
    parser.add_argument("--wheel", required=True)
    parser.add_argument("--cache-dir", required=True)
    parser.add_argument("--group-name")
    args = parser.parse_args()
    try:
        return asyncio.run(run(args))
    except Exception as exc:
        # Exceptions can contain SDK objects; never dump credentials or tracebacks.
        print(json.dumps({"stage": "failed", "errorType": type(exc).__name__}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
