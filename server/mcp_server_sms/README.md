# Volcengine SMS MCP Server

[简体中文](README_zh.md)

An independent adapter for Volcengine SMS APIs. Each tool receives its complete API input, makes one upstream request and returns the result. It supports MCP **2026-07-28**, stdio and **stateless Streamable HTTP**.

There is no database, business cache, qualification draft, stored preview, generic execution ticket, local file service or UI. It does not load or depend on a Skill. The client owns interaction and user confirmation; the SMS service owns business validation, applications, tasks and delivery records.

## Tools

| Capability | Tools |
| --- | --- |
| Account and message groups | `list_message_groups`, `get_message_group`, `get_account_information` |
| Qualifications | `get_qualification_requirements`, `list_qualifications`, `recognize_qualification_document`, `check_qualification_enterprise`, `check_qualification_person`, `apply_qualification` |
| Mobile verification | `send_verification_code`, `verify_code` |
| Signatures and templates | `list_signatures`, `apply_signature`, `list_templates`, `list_second_templates`, `apply_template` |
| Sending and reports | `send_sms`, `list_send_logs`, `get_send_statistics` |
| Ordinary batches | `get_batch_upload_url`, `get_batch_csv_template`, `create_batch_task`, `get_batch_task`, `list_batch_tasks`, `start_batch_task`, `cancel_batch_task` |

There are **26 tools**. Ordinary batches cover domestic notification and marketing SMS. Special notification batches, OTP batches and international SMS are outside this server's scope.

Tools preserve the upstream result structure and IDs. They do not select a template, rewrite content, deduplicate recipients, synthesize qualification-check tickets or decide whether a human approved an operation. A `ticket` returned by a qualification check is an upstream business receipt, not MCP state; the caller provides it when submitting the complete application. Client configuration must provide the application/scene/template values required by mobile verification APIs.

Qualification images must already be available through the existing SMS material channel. OCR and application tools accept its file references; there is no MCP-owned `fileId`, filesystem access or upload endpoint. The client must arrange a private material channel and handle OCR results and personal information appropriately. For batches, `get_batch_upload_url` returns the upstream signed upload URL and `file` key: upload the CSV directly, then pass that key as `fileUrl` to `create_batch_task`. Creating a task does not start it.

## Install and configure

Python 3.11 or later is required. From source:

```bash
uv sync --extra test
uv run mcp-server-sms --transport stdio
```

For stdio, supply `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY` and optionally `VOLCENGINE_SESSION_TOKEN` in the client process environment. No local subject, encryption key or database URL is required. Do not place credentials in prompts or source control.

After version 0.1.0 has been published:

```bash
uvx --from 'mcp-server-sms==0.1.0' mcp-server-sms --transport stdio
```

Development clients can use an explicit wheel path before publication.

## Streamable HTTP

```bash
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000 \
  --public-url https://sms-mcp.example.com
```

Connect to `/mcp`. The deployment supplies HTTPS and access policy. Every HTTP request carries `Authorization: Bearer <Base64 JSON>` with the following credential fields:

```json
{"AccessKeyId":"<access-key>","SecretAccessKey":"<secret-key>","SessionToken":"<optional-session-token>"}
```

This follows the repository's credential-passing convention; it is **not an OAuth access token** and Base64 is not encryption. The client or trusted gateway must construct the header outside model context. HTTP never falls back to process credentials. Each SMS call uses these credentials for official V4 signing, and SMS/IAM enforces resource access. The server has no OAuth login flow or persistent caller identity.

`--public-url` adds the deployment's HTTPS origin to DNS-rebinding protection. Without it, only local HTTP hosts are accepted. Requests do not require a protocol session or shared process state. Replicas can serve requests independently.

The HTTP connection pool is owned by the MCP server lifespan and closed at shutdown. Credentials and signed headers remain per-request, and response cookies are not retained between callers. Connection reuse does not introduce business state or a database.

## Outcomes and confirmation

- The client must obtain user authorization before calling tools with side effects. Tool annotations describe behavior; they do not prove user consent.
- SMS API acceptance and delivery are separate. Use the returned Message ID with `list_send_logs`; an empty result does not prove failure.
- Application creation is not audit approval. Query qualification, signature or template state separately.
- No API calls are automatically retried. A timeout or unconfirmed write returns `outcome_unknown`; do not blindly repeat it. This adapter does not provide durable request deduplication or an exactly-once guarantee.
- Unstructured HTTP 400/401/403/404/405/413/415/422/429 responses are explicit rejections. Other unstructured statuses, server errors, and malformed or incomplete successful write responses remain uncertain. API-response errors include `http_status` without echoing the response body.
- The upload API's top-level `url` is returned byte-for-byte, including its signed credential parameters. Other fields still undergo credential redaction. Treat the complete URL as a temporary capability; do not redact it before upload or expose it in logs.
- A successful API call can contain a failed business check, such as an invalid verification code. Inspect the upstream `status` value.
- The API adapter does not log request bodies or credentials. Upstream error text is not echoed, and authentication fields are removed from results; ordinary business content is preserved. Clients and deployment platforms must also configure their own logging and private-data handling.

## Development

```bash
uv sync --extra test
uv run ruff check src tests
uv run pytest -q
uv build
uv run python -m twine check dist/*
```

Tests cover direct API calls, request serialization, credential isolation, uncertain writes, business error responses, file-response decoding and the stateless protocol. They do not submit real qualifications or send real SMS. Actual write tests require separate customer authorization.

API fields are checked against the [official SMS SDK](https://github.com/volcengine/volcengine-python-sdk/tree/3b116781c5b8bb648f215b29587f2ec74d9e5d02/volcenginesdkvolcsms). V4 signing uses the [official Python SDK](https://github.com/volcengine/volc-sdk-python). Qualification extension APIs use the existing SMS service contract; SDK coverage and account availability must be verified for the deployment.

The repository's package workflow builds PRs and publishes new versions after merge, with maintainer PyPI permissions. Package publication does not deploy a cloud service. Licensed under Apache-2.0.
