# Volcengine SMS MCP App

[简体中文](README_zh.md)

An interactive SMS application for MCP Apps hosts. The model queries resources and opens prefilled forms; the user reviews and submits operations in the embedded UI. No Skill is loaded by the server. MCP 2026-07-28, stdio and stateless Streamable HTTP remain supported.

The server is not yet open to external customers. This tool surface replaces the earlier API-style tools without aliases or compatibility profiles. Hosts without MCP Apps can use read-only queries; business changes require a supported host or the SMS console. App-only visibility is a host presentation boundary, not authorization: every request still uses the customer's credentials and SMS/IAM checks.

## Model-visible tools: 17

| Purpose | Tools |
| --- | --- |
| Account, requirements, qualifications | `get_account_information`, `get_qualification_requirements`, `list_qualifications` |
| Resources and carrier reports | `query_sms_resources` |
| Templates and binding details | `list_templates`, `list_second_templates` |
| Sending records and statistics | `list_send_logs`, `get_send_statistics` |
| Batch discovery and CSV example | `query_batch_tasks`, `get_batch_csv_template` |
| Open forms | `open_sms_service_onboarding`, `open_qualification_form`, `open_signature_form`, `open_traffic_form`, `open_template_form`, `open_batch_task_form` |

All query and open-form tools declare `readOnlyHint=true`. Opening a form never submits a business operation. A single conversational send uses `preview_sms_send` first, shows the masked recipient and rendered content, then passes the unchanged request and returned confirmation to `send_sms` after explicit user approval. The submit step rechecks template and account scope; changed input or resources require a new preview. Multiple recipients, scheduled sends and per-recipient variables use the batch form. `prefill` contains editable values only; it cannot carry verification tickets, acceptance flags or a submission request. Unknown fields stay empty. File prefills remain subject to host limits; prefer selecting documents in the form.

`open_batch_task_form({"task":{"subAccount":"<group>","taskId":"<task>"}})` opens an existing task for review/launch/cancel. `task` and `prefill` cannot be supplied together. Querying or opening an existing task never creates another task.

`query_sms_resources` uses `request.action` plus typed `request.params`:

- Message groups: `GetSubAccountListForAgent`, `GetSubAccountDetail`.
- Signatures and batch templates: `ListSignaturesForAgent`, `ListBatchTemplatesForAgent`.
- Traffic: `GetTobTrafficDrivingLinkListForAgent`, `GetTobTrafficDrivingPhoneListForAgent`, `ListRelationTemplateForAgent`, `CheckTrafficDrivingExist`.
- Carrier registration: `ListThirdTemplate`, `AgentGetSignatureTemplateReportStatus`.
- Batch task body validation: `ValidateBatchTaskContentForAgent` (only for templates declaring task-level fields).

`query_batch_tasks` selects `GetBatchTaskDetail` (`subAccount/taskId`) or `GetBatchTaskList` (`subAccount/taskName/signature/templateId/pageIndex/pageSize`). A missing list entry does not replace an exact detail query.

The signature form uses `query_sms_resources` with `GetApplySignatureBind` to retrieve approved qualification candidates in one unpaginated array. The optional `purpose` filter accepts 1 (self-use), 2 (third-party use), or 0 (all); omitting it also returns both purposes. The form consumes only `id/purpose/materialName/businessCertificateName`, without per-item lookups. After customer confirmation it submits directly to `ApplySmsSignatureV2`; SMS validates qualification ownership and approval status. `list_qualifications` remains available for full qualification list queries.

## App-only tools: 22

| Purpose | Tools |
| --- | --- |
| File upload | `prepare_material_upload`, `complete_material_upload`, `prepare_recipients_upload`, `complete_recipients_upload` |
| Service activation | `get_sms_service_onboarding`, `submit_sms_service_onboarding` |
| Qualification checks | `recognize_qualification_document`, `check_qualification_enterprise`, `check_qualification_person`, `send_verification_code`, `verify_code` |
| Business applications | `submit_qualification`, `submit_signature`, `preview_template`, `submit_template`, `preview_traffic_resource`, `submit_traffic_resources` |
| Sending and batch management | `preview_sms_send`, `send_sms`, `send_batch_test_sms`, `create_batch_task`, `start_batch_task`, `cancel_batch_task` |

These tools declare `visibility=["app"]` and must not be offered to the model by a compliant host. Qualification OCR and identity checks always return details through `_meta["sms/form"]`; there is no model-visible override. Metadata still passes through the host and is not end-to-end encrypted.

## Forms and confirmation

Seven forms share `ui://sms/forms.html`. Layout and Arco styles are maintained in this package; the original SMS Skill is not a build or runtime dependency.

- Qualification, signature and traffic forms preserve their existing upload, validation and review flows.
- Template applications support editable text, parameter types, signature/group scope, traffic binding combinations and short-link options. Placeholder names and definitions must agree; SMS owns dynamic policy and final review.
- Ordinary sends accept 1–200 numbers with identical parameter values. The UI renders the selected template. Ordinary sends and batch test sends call the sending API directly after confirmation; SMS owns template eligibility and parameter validation. Numbers and values are preserved, not deduplicated or rewritten. Per-recipient content belongs in a CSV batch.
- Traffic registration reports acceptance from the native API response without per-item ID lookups. Use resource queries when IDs are needed.
- One confirmation in the new batch form authorizes creation and sending: the page creates the task, then starts that same task. The internal create/start tools remain independent; creation alone is not sending. Accepted starts do not require another confirmation, even if the following status query fails or returns stale data. Existing task management reads current identity/state/content before user confirmation. Unknown writes stay locked rather than being repeated.
- UI submit/send/cancel is the user's confirmation for that displayed action; the model does not add another chat confirmation after the click. A receipt is not audit approval, carrier readiness, or delivery proof.

## File transfer and privacy

Batch query results include task summaries only; storage keys, download URLs and internal extra fields are excluded.

File bytes do not enter App tool arguments. The page requests an upload plan with metadata, sends original bytes directly to an approved ImageX/TOS URL, then confirms through MCP. SMS AK/SK and ImageX STS remain on the server. The page receives only the per-file upload capability.

CSV checks run when the customer reviews the batch task. `complete_recipients_upload` uses `GetFilePublicTosURL` with account authorization, reads bounded raw bytes without compression, verifies size/SHA-256 and validates rows against the CSV columns already loaded by the page, then reuses those bytes for optional traffic checks. Template text and column definitions are reused within the review without additional template queries; optional traffic checks still query the resources referenced in rendered content. The page may reuse a complete successful check for unchanged input until the upload confirmation expires; partial or missing-resource reports are checked again. Task creation still validates the stored file in the SMS backend. Missing API permission fails explicitly.

Files are limited to 10 MiB; at most two buffered CSV read/validation operations per instance. Material size is checked in the UI and request metadata; actual storage limits are owned by ImageX. Upload references are signed with the current caller credentials, with material expiry at 10 minutes and CSV at one hour. Credential refresh requires a new upload. Upload failure preserves form inputs and permits explicit reselection; it does not submit an application/task or automatically retry.

CSP declares configured ImageX upload hosts and the complete TOS bucket origin `https://batch-sms-bucket.tos-cn-beijing.volces.com`, with no external scripts/styles. Explicit origins avoid hosts percent-encoding wildcard `*` as `%2A`, which browsers reject as an invalid CSP source. Host CSP support and storage CORS must be verified in the real client. There is no `/files` route, caller-provided download URL, filesystem access, persistent upload state or server-side draft. Ordinary chat attachments are not automatically material references.

## Outcomes and observations

Read structured outcomes and business statuses. A failed read is not an empty resource list; an accepted send is not delivery. MCP issues each physical API request once without automatic retries.

SMS errors preserve the original code, message, RequestId and HTTP status, with the complete response in `error.backend_response`. MCP does not infer a final business outcome from error codes or HTTP status, or replace backend errors with an unknown-outcome message. The host agent decides what to do next. Transport failures expose the actual exception type and message. Forms display the original error; aggregate workflows retain the individual API failures.

Tool and physical API boundaries emit start/end logs and OpenTelemetry events with correlation, duration, public error code and request ID. They omit file bytes, message content, phone numbers and credentials; logging failures do not change business results. Client upload logs likewise omit names, URLs and authorization.

## Install and configure

Python 3.11 or later is required. From source:

```bash
cd ui
npm ci
npm test
npm run build
cd ..
uv sync --extra test
uv run mcp-server-sms --transport stdio
```

For stdio, supply `VOLCENGINE_ACCESS_KEY`, `VOLCENGINE_SECRET_KEY` and optionally `VOLCENGINE_SESSION_TOKEN` in the client process environment. No local subject, encryption key or database URL is required. Do not place credentials in prompts or source control.

Alternatively, build and run the local wheel for this version:

```bash
uv build
uvx --from ./dist/mcp_server_sms-0.2.0-py3-none-any.whl mcp-server-sms --transport stdio
```

Features depend on the installed version. Updating repository code does not update a deployed function.

## Streamable HTTP

```bash
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000 \
  --public-url https://sms-mcp.example.com
```

Connect to `/mcp`. The deployment supplies HTTPS and access policy. Every HTTP request carries either `Authorization: <Base64 JSON>` or `Authorization: Bearer <Base64 JSON>` with the following credential fields:

```json
{"AccessKeyId":"<access-key>","SecretAccessKey":"<secret-key>","SessionToken":"<optional-session-token>"}
```

This follows the repository's credential-passing convention; it is **not an OAuth access token** and Base64 is not encryption. The client or trusted gateway must construct the header outside model context. HTTP never falls back to process credentials. Each SMS call uses these credentials for official V4 signing, and SMS/IAM enforces resource access. The server has no OAuth login flow or persistent caller identity.

When using the shared MCP gateway, the gateway owns OAuth login and authorization and forwards each customer's STS credentials. Do not pass ordinary OAuth tokens directly to this service or substitute the deployment account's credentials for customer credentials.

The MCP SDK checks `Host` and any supplied `Origin` header. Set `--public-url` to the service's HTTPS origin to allow its host and same-origin requests. Pass `--allowed-origin https://app.example.com` once for each additional trusted browser origin. For cross-origin browser access, the deployment entry point must also handle CORS preflights and response headers. Clients that omit `Origin` can connect with valid credentials and an allowed `Host`. Requests do not require a protocol session or shared process state. Replicas can serve requests independently.

The HTTP connection pool is owned by the MCP server lifespan and closed at shutdown. Credentials and signed headers remain per-request, and response cookies are not retained between callers. Connection reuse does not introduce business state or a database.

## Development

```bash
cd ui
npm ci
npm test
npm run build
cd ..
uv sync --extra test
uv run ruff check src tests
uv run pytest -q
uv build
uv run python -m twine check dist/*
```

Tests exercise MCP, API mapping, credential isolation, uncertain writes, CSV, inline schemas, privacy, observations, UI resources and confirmation behavior. Python tests verify frontend source fingerprints against bundled HTML. Node.js is needed only for development builds; the wheel serves prebuilt resources. Upstream HTTP is mocked: no real qualifications or SMS are submitted. Actual write tests require separate customer authorization. This unreleased tool surface intentionally removes the previous names and direct model-write paths. Local results do not prove gateway OAuth, real ImageX/TOS upload, cloud deployment or a Doubao client integration.

API fields are checked against the [official SMS SDK](https://github.com/volcengine/volcengine-python-sdk/tree/3b116781c5b8bb648f215b29587f2ec74d9e5d02/volcenginesdkvolcsms). V4 signing uses the [official Python SDK](https://github.com/volcengine/volc-sdk-python). Qualification extension APIs use the existing SMS service contract; SDK coverage and account availability must be verified for the deployment.

The source version is 0.2.0. The repository's package workflow builds PRs and publishes new versions after merge, with maintainer PyPI permissions. Package publication, veFaaS upgrades and ATS/Plugin listing are separate operations. Licensed under Apache-2.0.
