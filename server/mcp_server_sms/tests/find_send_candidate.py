"""Find recently delivered SMS resource combinations via read-only MCP calls.

Runs an explicitly selected wheel and the master Skill's supported credential
resolver. It never invokes preparation, sending, or resource mutation tools.
Credentials remain in memory; output contains only safe resource metadata.
"""

import argparse
import asyncio
import contextlib
import datetime
import importlib
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

from cryptography.fernet import Fernet
from live_readonly import tool_payload
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

READ_TOOLS = frozenset(
    {
        "list_message_groups",
        "analyze_delivery",
        "get_message_group",
        "list_signatures",
        "list_templates",
        "get_template",
    }
)


def rows(payload):
    value = payload.get("result", payload)
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        for key in ("List", "list", "Items", "items"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


async def discover(session, args):
    queries = 0

    async def call(name, arguments):
        nonlocal queries
        if name not in READ_TOOLS:
            raise ValueError("This discovery client permits read-only tools only")
        cost = 1 + (
            arguments.get("max_pages", 0) if arguments.get("include_logs") else 0
        )
        if queries + cost > args.max_queries:
            raise RuntimeError("Read-only query budget exhausted")
        queries += cost
        result = await session.call_tool(name, arguments)
        if result.is_error:
            # Tool errors are already filtered by the SMS server. Do not dump
            # exception objects, the process environment or credentials.
            raise RuntimeError(
                "MCP query failed: "
                + " ".join(getattr(item, "text", "") for item in result.content)
            )
        await asyncio.sleep(0.3)
        return tool_payload(result)

    if args.queries:
        for query in args.queries:
            print(
                json.dumps(
                    {
                        "stage": "query",
                        "tool": query["tool"],
                        "data": await call(query["tool"], query["arguments"]),
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        return
    if args.query:
        print(
            json.dumps(
                {
                    "stage": "query",
                    "tool": args.query,
                    "data": await call(args.query, args.arguments),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        return
    groups = rows(await call("list_message_groups", {}))
    end = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).replace(
        microsecond=0
    )
    window = {
        "start": (end - datetime.timedelta(days=args.days)).isoformat(),
        "end": end.isoformat(),
        "bucket": "total",
    }
    print(
        json.dumps(
            {"stage": "discovery", "groupCount": len(groups), "window": window},
            ensure_ascii=False,
        ),
        flush=True,
    )
    excluded = set(args.exclude_group)
    # Interleave recent and older groups instead of assuming creation order is
    # evidence of active traffic. Delivery records determine eligibility.
    ordered = []
    for index in range((len(groups) + 1) // 2):
        ordered.append(groups[index])
        opposite = len(groups) - index - 1
        if opposite != index:
            ordered.append(groups[opposite])
    scanned = 0
    candidates = []
    seen = set()
    for group in ordered:
        group_id = group.get("SubAccount")
        if not group_id or group_id in excluded:
            continue
        if queries + 12 > args.max_queries:
            break
        report = await call("analyze_delivery", {**window, "sub_account": group_id})
        data = report.get("result", report)
        metrics = data["trend"][0]["metrics"]
        delivered = metrics["receipts"]["success"]
        submitted = metrics["submission_success_rate"]["numerator"]
        scanned += 1
        if scanned % 10 == 0 or delivered:
            print(
                json.dumps(
                    {
                        "stage": "group_stats",
                        "scanned": scanned,
                        "queries": queries,
                        "groupId": group_id,
                        "groupName": group.get("SubAccountName"),
                        "submitted": submitted,
                        "delivered": delivered,
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
        if not isinstance(delivered, int) or delivered <= 0:
            continue
        logs = await call(
            "analyze_delivery",
            {
                **window,
                "sub_account": group_id,
                "include_logs": True,
                "page_size": 100,
                "max_pages": 3,
            },
        )
        records = logs.get("result", logs)["send_logs"]["records"]
        detail_payload = await call("get_message_group", {"sub_account": group_id})
        detail = detail_payload.get("result", detail_payload)
        if str(detail.get("status")) != "1":
            continue
        for record in sorted(
            records, key=lambda item: item.get("sendTime") or 0, reverse=True
        ):
            signature, template_id = record.get("signature"), record.get("templateId")
            key = (group_id, signature, template_id)
            if (
                record.get("receiptState") != "success"
                or not signature
                or not template_id
                or key in seen
                or queries + 3 > args.max_queries
            ):
                continue
            seen.add(key)
            signatures = rows(
                await call(
                    "list_signatures",
                    {
                        "signature": signature,
                        "sub_account": [group_id],
                        "page": 1,
                        "page_size": 100,
                    },
                )
            )
            if not any(
                item.get("Signature") == signature
                and str(item.get("Status")) in {"3", "5"}
                and item.get("usable") is not False
                for item in signatures
            ):
                continue
            templates = rows(
                await call(
                    "list_templates",
                    {
                        "template_id": template_id,
                        "signature": [signature],
                        "sub_account": [group_id],
                        "page": 1,
                        "page_size": 100,
                    },
                )
            )
            if not any(
                str(item.get("TemplateId", item.get("templateId"))) == template_id
                and str(item.get("Status", item.get("status"))) in {"3", "5"}
                for item in templates
            ):
                continue
            template = await call(
                "get_template",
                {
                    "template_id": template_id,
                    "signature": signature,
                    "sub_account": group_id,
                },
            )
            candidate = {
                "groupId": group_id,
                "groupName": group.get("SubAccountName"),
                "groupCapabilities": detail.get("channelTypeToIndustryConfig"),
                "recentDelivered": delivered,
                "evidenceMessageId": record["messageId"],
                "evidenceReceiptTime": record["receiptTime"],
                "template": template,
            }
            candidates.append(candidate)
            print(
                json.dumps({"stage": "candidate", **candidate}, ensure_ascii=False),
                flush=True,
            )
            if len(candidates) >= args.candidates:
                break
        if len(candidates) >= args.candidates:
            break
    print(
        json.dumps(
            {
                "stage": "completed",
                "groupsScanned": scanned,
                "queries": queries,
                "candidateCount": len(candidates),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )


async def main(args):
    sys.path.insert(0, str(Path(args.skill_dir) / "scripts"))
    with (
        contextlib.redirect_stdout(io.StringIO()),
        contextlib.redirect_stderr(io.StringIO()),
    ):
        skill_api = importlib.import_module("api_client")
        credentials = skill_api.SmsApiClient()._credential_resolver.resolve()
    uvx = shutil.which("uvx")
    if not uvx:
        raise RuntimeError("uvx is required")
    with tempfile.TemporaryDirectory(prefix="sms-mcp-resource-discovery-") as directory:
        parameters = StdioServerParameters(
            command=uvx,
            args=[
                "--offline",
                "--python",
                sys.executable,
                "--from",
                args.wheel,
                "mcp-server-sms",
                "--transport",
                "stdio",
            ],
            env={
                "UV_CACHE_DIR": args.cache_dir,
                "UV_TOOL_DIR": args.tool_dir,
                "SMS_MCP_DATABASE_URL": "sqlite:///"
                + str(Path(directory) / "state.db"),
                "SMS_MCP_ENCRYPTION_KEY": Fernet.generate_key().decode(),
                "SMS_MCP_LOCAL_SUBJECT": "read-only-resource-discovery",
                "VOLCENGINE_ACCESS_KEY": credentials.access_key,
                "VOLCENGINE_SECRET_KEY": credentials.secret_key,
                "VOLCENGINE_SESSION_TOKEN": credentials.session_token,
            },
        )
        try:
            async with (
                stdio_client(parameters) as (read, write),
                ClientSession(read, write, read_timeout_seconds=60) as session,
            ):
                await session.discover()
                await discover(session, args)
        except Exception as error:  # noqa: BLE001 -- redact all transport failures.

            def safe_messages(exception):
                if isinstance(exception, BaseExceptionGroup):
                    return [
                        item
                        for child in exception.exceptions
                        for item in safe_messages(child)
                    ]
                return [
                    skill_api.sanitize_output(
                        str(exception),
                        secrets=(
                            credentials.access_key,
                            credentials.secret_key,
                            credentials.session_token,
                        ),
                    )
                ]

            print(
                json.dumps(
                    {"stage": "failed", "errors": safe_messages(error)},
                    ensure_ascii=False,
                ),
                flush=True,
            )
            return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True)
    parser.add_argument("--wheel", required=True)
    parser.add_argument("--cache-dir", required=True)
    parser.add_argument("--tool-dir", required=True)
    parser.add_argument("--days", type=int, choices=range(1, 91), default=7)
    parser.add_argument("--max-queries", type=int, choices=range(15, 121), default=110)
    parser.add_argument("--candidates", type=int, choices=range(1, 6), default=3)
    parser.add_argument("--exclude-group", action="append", default=[])
    parser.add_argument("--query", choices=sorted(READ_TOOLS))
    parser.add_argument("--arguments", type=json.loads, default={})
    parser.add_argument("--queries", type=json.loads)
    try:
        raise SystemExit(asyncio.run(main(parser.parse_args())))
    except Exception as error:  # noqa: BLE001 -- never expose auth exception details.
        print(json.dumps({"stage": "failed", "errorType": type(error).__name__}))
        raise SystemExit(1)
