# Volcengine SMS MCP Server

[简体中文](README_zh.md)

Independent tools for domestic SMS qualifications, signatures, templates, sending, ordinary batch tasks and delivery results. Business rules are adapted from the official Skill at `master@c7c49836dff727ca7a2ab297dc9d1ad62c5aec15` (1.4.4), without changing the SMS backend.

Supports **MCP 2026-07-28**, stdio and stateless Streamable HTTP with the MCP Python SDK 2.x. Package version: **0.1.0**. Package, protocol and SMS API versions are independent.

## Capabilities

- Check service availability and query message groups. Only `RE:0001` means the service has not been enabled. Customers accept the service agreement in the existing SMS console themselves.
- Query qualification requirements; create and update drafts; upload and recognize documents; save customer-reviewed information; check enterprise/person information; verify mobile numbers when required; preview, submit and query applications.
- Query, preview and apply for signatures and templates; match approved templates and validate exact variables before sending.
- Send domestic SMS and query delivery results. Ordinary notification/marketing batches support CSV validation, creation, separate launch confirmation, cancellation and status queries.
- Report customer-visible send counts, delivery statistics and failure reasons.

Special notification batches, OTP batches, international SMS and Hong Kong/Macao/Taiwan are excluded. This package contains **no HTML UI, MCP App, browser login or local form server**. Hosts own material collection, private review and customer confirmation.

Sending currently uses customer-approved signatures and templates. `SPT_` public templates are not supported and must not be passed through the customer-template validation workflow.

Use `get_template(template_id, signature, sub_account)` to retrieve a selected template's content and variables before preparing a send. `contentRedacted=true` means the text has been redacted or truncated and is not the complete original. Reading details does not send SMS.

## Qualification workflow

1. Call `get_qualification_requirements` for account rules and `privateInputSchemas`, then `create_qualification_draft(name, purpose)` (`1` own use, `2` third-party use). No application is submitted and no webpage URL is needed.
2. Stage files through the private exchange below. `upload_qualification_document` uploads a `qualification_image` file to the existing SMS material service and attaches it to a draft.
3. `recognize_qualification_document` returns a private `reviewFileId`. The host retrieves it outside model context for customer review. OCR never automatically confirms input. The host stages reviewed fields as a `qualification_data` JSON file and calls `update_qualification_information`. The account-specific JSON schemas describe those fields.
4. Check saved information with `check_qualification_information`. Use `set_qualification_responsible` to explicitly choose whether to reuse the operator. Legal-person supplemental information is optional and can be removed with `clear_qualification_legal`.
5. Where mobile verification is required, `prepare_qualification_verification_code` previews the recipient. After customer confirmation, `execute_sms_operation` sends the code. The host privately stages a `verification_code` file and calls `verify_qualification_code`. The server's staged copy is deleted after the verification attempt; the host manages the source file.
6. `prepare_qualification_application` returns a frozen preview and `operationId`. After customer confirmation, `execute_sms_operation` submits it. Information changes invalidate the old preview. Use `get_qualification_draft` for the submission result and `list_qualifications` for review status.

Cancellation clears an unsubmitted draft; it does not withdraw an existing or uncertain application. Qualification tickets, uploaded-image addresses and upload credentials never appear in model tool results.

## Private file exchange

MCP tool arguments carry file references, not document Base64, personal fields or verification-code text. A host must provide a controlled path outside model context; ordinary chat attachments are not automatically such a path.

| Kind | Content and limit |
| --- | --- |
| `qualification_image` | JPEG/PNG, 1 byte to 2 MB |
| `qualification_data` | UTF-8 JSON object, up to 64 KB; schemas from the requirements tool |
| `verification_code` | JSON object with a four-digit string `code`, up to 1 KB |
| `batch_csv` | UTF-8 CSV, up to 50 MB |

**stdio:** explicitly configure an absolute `SMS_MCP_INPUT_ROOT`. The host places customer-provided files there and calls `import_input_file(relative_path, kind, content_type)`. Absolute input paths, traversal, symlinks and non-regular files are rejected. `export_qualification_review` writes private review JSON to a new file under the same root without overwriting files. The host must not read its contents into model context.

**HTTP:** the host sends file bytes to `POST /files?kind=...` with the MCP bearer token and appropriate `Content-Type`, receiving an owned `fileId`. It privately retrieves review data through authenticated `GET /files/{fileId}`. These are host integration endpoints, not a standard MCP upload protocol. Remote tool calls cannot read the server's local import directory. Host support must be tested separately for each client.

Ordinary batches use the same exchange: stage `batch_csv`, call `check_batch_file`, prepare and confirm creation, then separately prepare and confirm launch. API acceptance, task completion and delivered messages are separate states.

## Configuration

Common required variables:

- `SMS_MCP_DATABASE_URL`: SQLAlchemy URL. SQLite is suitable for a single local process; replicas use the same PostgreSQL database.
- `SMS_MCP_ENCRYPTION_KEY`: shared Fernet key for encrypted drafts, files and execution records.
- `SMS_MCP_FLOW_TTL`: file/draft/preview lifetime, default 1800 seconds, at least 60.
- `SMS_MCP_OPERATION_TTL`: mutation record retention, default 86400 seconds, no shorter than draft lifetime.

stdio additionally requires `SMS_MCP_LOCAL_SUBJECT`, `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY`, and optionally `VOLCENGINE_SESSION_TOKEN`. Configure `SMS_MCP_INPUT_ROOT` only when importing/exporting files.

After the package is published:

```bash
uvx --from 'mcp-server-sms==0.1.0' mcp-server-sms --transport stdio
```

Development installations can use source or an explicit wheel before merging or publishing. Local paths cannot be copied into a cloud client's configuration.

HTTP additionally requires `SMS_MCP_PUBLIC_URL` (HTTPS origin), `SMS_MCP_OIDC_ISSUER` (existing token issuer with discovery/JWKS), and `SMS_MCP_TOKEN_AUDIENCE`.

```bash
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000
```

Connect to `/mcp`. Requests authenticate independently without initialize or Mcp-Session-Id. The deployment platform provides HTTPS, its existing authorization service and database; this package creates none of those resources.

- `Authorization: Bearer <MCP access token>` validates signature, issuer, audience, expiry and subject using RS256 or ES256.
- `X-Volcengine-Credentials` contains Base64 JSON `{AccessKeyId, SecretAccessKey, SessionToken?}`, injected by a trusted client/gateway for that SMS request. Never log it or expose it to the model. Base64 is encoding only; use HTTPS. File endpoints require the MCP token only.

Platform-specific authorization still needs integration verification. HTTP never falls back to process SMS credentials. Browser client IDs/secrets, session-signing keys and login callbacks are not required.

See [.env.example](.env.example); inject actual secrets outside source control. `/health` is a liveness endpoint and `/.well-known/oauth-protected-resource/mcp` publishes resource metadata.

## State and confirmation

Stateless MCP transport does not remove business state. Explicit `draftId`, `fileId` and `operationId` records are owned, encrypted and expire. Completing/cancelling a draft clears its materials. HTTP periodically cleans expired records; stdio cleans them on subsequent calls. Hosts manage source files.

An operation ID binds a preview, not customer consent. Hosts must display the current preview and enforce confirmation. Credential changes require a new preview; qualification drafts are bound to the credentials used when created.

Unknown writes are never automatically replayed. Query `get_sms_operation_result` or `get_qualification_draft`; absent conclusive evidence, preserve `outcome_unknown`. Local deduplication is not an upstream idempotency guarantee.

Started operations remain queryable for `SMS_MCP_OPERATION_TTL`, independently of the shorter preview lifetime. Expired previews still cannot execute again.

## Development and acceptance

```bash
uv sync --extra test
uv run pytest
uv run ruff check src tests --select F,E9
uv build
uv run python -m twine check dist/*
```

Tests mock SMS responses and exercise the headless qualification workflow, stale previews, duplicate writes, crash recovery, code verification, file isolation, ordinary batches and transport. CI separately checks PostgreSQL sharing.

`tests/live_readonly.py` and `tests/desktop_launcher.py` optionally reuse the designated master Skill's supported credential resolver and run an exact wheel. Credentials remain in process memory. Desktop launcher state is temporary and unsuitable for persistent deployment. Successful queries do not constitute acceptance of document uploads, verification messages, submissions or sends; those require separate customer authorization.

Local TraeWork acceptance on 2026-09-14 covered resource queries, qualification draft creation/cancellation, invalid-material rejection, and one customer-confirmed SMS submission. The send API returned success and a Message ID; delivery was not yet confirmed. Real document/OCR, mobile verification, qualification/signature/template submissions, ordinary batches and cloud-host integration remain pending.

The repository workflow builds packages for PRs and publishes new/version-changed packages after merging to main, using maintainer PyPI permissions. It does not deploy cloud services.

## License

Apache-2.0, retaining the official master Skill's copyright and business rules. Frontend assets, special notification batches, local login flows and the original local MCP App implementation are excluded.
