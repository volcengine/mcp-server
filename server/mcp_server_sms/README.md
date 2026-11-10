# Volcengine SMS MCP Server

[简体中文](README_zh.md)

An independent adapter for Volcengine SMS APIs. Business tools receive complete API input and call the corresponding upstream API. It supports MCP **2026-07-28**, stdio, **stateless Streamable HTTP** and standard **MCP Apps**. Opening a form performs no mutation; file upload performs its authorization, transfer and confirmation on the server.

There is no database, business cache, server-side draft, stored preview, generic execution ticket or local filesystem service. It does not load or depend on a Skill. Four forms keep current input in the host sandbox; the client owns confirmation, and the SMS service owns business validation, applications, tasks and delivery records.

## Tools

| Capability | Tools |
| --- | --- |
| Account and message groups | `list_message_groups`, `get_message_group`, `get_account_information` |
| Qualifications | `get_qualification_requirements`, `list_qualifications`, `recognize_qualification_document`, `check_qualification_enterprise`, `check_qualification_person`, `apply_qualification` |
| Mobile verification | `send_verification_code`, `verify_code` |
| Signatures and templates | `list_signatures`, `apply_signature`, `list_templates`, `list_second_templates`, `apply_template` |
| Sending and reports | `send_sms`, `list_send_logs`, `get_send_statistics` |
| Batches | `get_batch_upload_url`, `get_batch_csv_template`, `create_batch_task`, `get_batch_task`, `list_batch_tasks`, `start_batch_task`, `cancel_batch_task` |
| Supplemental queries | `query_sms_resources` |
| Service activation | `manage_sms_service` |
| Traffic resources | `register_traffic_resource` |
| App-only file upload | `upload_sms_file` |

There are **30 tools covering 40 business Actions**; the upload component additionally calls `GetMUploadParam` internally. Batch discovery and CSV templates support ordinary templates and special notifications. OTP batches and international SMS are outside this server's scope.

The three grouped tools accept a typed `request` with `action` and its corresponding `params`. They do not expose arbitrary API execution:

| Tool | Allowed Actions |
| --- | --- |
| `query_sms_resources` | `GetSubAccountListForAgent`, `ListSignaturesForAgent`, `ListBatchTemplatesForAgent`, `GetTobTrafficDrivingLinkListForAgent`, `GetTobTrafficDrivingPhoneListForAgent`, `ListRelationTemplateForAgent`, `CheckTrafficDrivingExist`, `ListThirdTemplate`, `AgentGetSignatureTemplateReportStatus`, `ValidateBatchTaskContentForAgent` |
| `manage_sms_service` | `ConfirmProtocolDocument`, `ActivateSmsProductInOneStep` |
| `register_traffic_resource` | `BulkCreateTobTrafficDrivingLinkForAgent`, `BulkCreateTobTrafficDrivingPhoneForAgent` |

Example arguments for querying batch templates:

```json
{
  "request": {
    "action": "ListBatchTemplatesForAgent",
    "params": {"SubAccounts": ["<message-group-id>"], "Page": 1, "PageSize": 20}
  }
}
```

For service activation (`RE:0001` means inactive), first obtain current documents and product state with `get_account_information`. After the customer reads and accepts the documents, call `manage_sms_service` with `ConfirmProtocolDocument` and `{"product":"sms","documents":[1,2]}`. Replace example IDs with the actual queried IDs. Inspect `fail`, and only after it is empty and the customer authorizes activation, separately call `ActivateSmsProductInOneStep` with `{"product":["sms"]}`. Query account state again to confirm completion. The server never chains the two operations automatically.

Traffic registration uses `params.data`, with at most 10 links or 100 phone numbers per call. `tools/list` supplies the full typed fields. URLs, paths, query parameters and numbers retain their original values. Personal identity data must use the client's private input channel.

Service results are checked against the submitted targets: signed/failed document IDs must cover the request without overlap, and activation results must match exactly the requested products. Incomplete or mismatched results return `outcome_unknown`. Valid partial signing failures and activation business failures retain their original values for the client to inspect.

Tools preserve the upstream result structure and IDs. They do not select a template, rewrite content, deduplicate recipients, synthesize qualification-check tickets or decide whether a human approved an operation. A `ticket` returned by a qualification check is an upstream business receipt, not MCP state; the caller provides it when submitting the complete application. Client configuration must provide the application/scene/template values required by mobile verification APIs.

The Apps forms can upload materials through host-proxied tool calls; the server acquires customer-scoped material credentials and completes the ImageX upload. Existing SMS material references remain supported. There is no filesystem path access, caller-selected remote download URL, persistent file storage or `/files` route. Plain chat attachments are not automatically converted into material references. For clients with an existing upload channel, `get_batch_upload_url` still returns the signed URL and `file` key: upload the original CSV, then pass that key as `fileUrl` to `create_batch_task`. Creating a task does not start it.

Signature applications support `appIcp.appIcpFileList`, `trademark.trademarkFileList`, `uploadFileList` and message-group bindings. `GetMUploadParam` is not a model-callable tool and its entire result is suppressed at the ordinary API output boundary; temporary credentials are consumed only by the server-side uploader.

## MCP Apps forms

Calling the following existing tools without `request` opens a form. A complete `request` retains the original direct API behavior and requires prior user authorization:

| Tool | Form |
| --- | --- |
| `apply_qualification` | Account requirements, company/people/materials, OCR, information and mobile checks, confirmation and review status |
| `apply_signature` | Qualification/source/group selection, APP/trademark/other attachments, confirmation and review status |
| `register_traffic_resource` | Links or phone numbers, preview and explicit registration |
| `create_batch_task` | Group/signature/template selection, native CSV sample, recipient validation/upload, content precheck, creation and separately confirmed launch/cancel |

Example `tools/call` params: `{"name":"apply_signature","arguments":{}}`. All four tools declare `_meta.ui.resourceUri: "ui://sms/forms.html"`. `resources/read` returns self-contained HTML with MIME `text/html;profile=mcp-app`, using Python's official `Apps` extension and the official `@modelcontextprotocol/ext-apps` browser SDK.

Styles are copied from the byted-sms-sender 1.4.6 React/Arco forms and maintained within this package's `ui/` directory. The Skill is unchanged and is not a build/runtime dependency. Dedicated overrides handle card widths and dark mode. Scripts/styles are inlined; no external connections or resource domains are declared, and the View does not fetch business APIs directly.

- The App-only `upload_sms_file` receives files through the host and returns file references in `_meta["sms/form"]`. OCR uses this channel by default (`private=true`); company/person checks can opt in with `private=true`. Ordinary content contains operation status only. Set OCR `private=false` only with explicit customer agreement: names, identity numbers and other recognized fields then enter model-visible `content` and `structuredContent`. Host handling, retention and logging of metadata still need integration verification: this is not end-to-end encryption or an independent authorization boundary.
- Material uploads allow only the configured ImageX service's documented regional/accelerated hosts and the official legacy upload hosts; other hosts are rejected before files or upload authorization are sent. CSV uploads retain their separate TOS URL policy.
- `visibility=["app"]` asks compliant hosts to omit the uploader from the model's tools. Visibility does not replace SMS/IAM authorization; every request uses its caller's credentials.
- Files are limited to **10 MiB** each, with at most **2** uploads per server instance. Busy requests are rejected before decoding rather than queued. Qualification images support JPG/JPEG/PNG; signature attachments support the corresponding image/PDF/ZIP/DOC/DOCX categories. CSV headers come from the selected template; original bytes are uploaded unchanged and duplicates are counted, not removed. Larger files can use existing upload channels. Actual host/gateway body limits require verification.
- `form_config.json` is the shared frontend/backend source for upload limits and existing SMS upload/verification identifiers. It must never contain customer keys or tokens.
- Preview and checked confirmation precede submission. Duplicate clicks are blocked; uncertain writes stay locked. Batch launch separately queries task identity/state/content and requires another confirmation of real sending and fees. History restoration displays results without replaying writes.
- Backend requirements remain authoritative. The form does not synthesize bypass tickets. Unsubmitted input, material references and check tickets are not persisted across closing the View; there is no cross-window/restart deduplication guarantee. Use the SMS console for manual review when company verification cannot complete.
- Non-Apps clients retain the business tools with complete arguments; use the SMS console when private interaction is unavailable. Local Skill CLI/draft/heartbeat behavior and its separate test-send panel are not copied into the View; existing tools such as `send_sms` remain available.

See [UI development and preview](ui/README.md) and the [MCP Apps standard](https://modelcontextprotocol.io/extensions/apps/overview).

## Migrating to 0.2.0

The original 26 tool names remain. Clients must update these input/output contracts:

- `apply_template` uses `ApplySmsTemplateV2ForAgent`. Each `templateParams` entry requires an explicit `paramType`: 1 ordinary, 2 link, 3 phone, 4 Path, 5 super variable. There is no implicit ordinary-variable default. `templateTrafficDriving` is a two-dimensional array of entries containing `name`, `paramType` and a resource `id` or `content`.
- `create_batch_task` uses `SetBatchTaskForAgent`. Required fields are `subAccount/name/signature/templateId/fileUrl/scheduled/sendTime/idempotencyKey`. Special notifications may require task-level `content` according to `TaskFields`; call the content precheck first. The old `templateName/channelType/extra` fields are no longer accepted because the service resolves template metadata. Immediate tasks use `scheduled=false, sendTime=0`; scheduled tasks use Unix seconds. Keep a stable client-generated `idempotencyKey` for the same confirmed task. The API timeout is 60 seconds. A valid `taskId/totalCount/dupCount` result confirms creation acceptance; zero counts are valid.
- `get_batch_csv_template` uses `TemplateUploadDemoForAgent`, no longer accepts `force_update`, and returns actual CSV in `result.value` for either JSON or raw CSV responses. Use its columns instead of inventing headers.
- `get_send_statistics` uses `GetTotalSendCountStatV4ForAgent`. It supports project/message-group filters, arrays of channels/signatures/templates, standard error codes, split-count selection and grouping flags, with `IsDomestic=1`. Existing scalar channel/signature/template arguments are still accepted and encoded as native API arrays.
- `list_send_logs` allows account-wide queries without a message group and removes complete `mobile/content` from model-visible results. Resource queries also remove private identity/material fields while retaining unknown business fields.

Tool schemas are generated from the same typed models and inlined using standard `oneOf/anyOf`, without `$ref/$defs/definitions`. There is no Doubao-specific protocol or client branch. The forms reuse the original styles with AppBridge in place of localhost endpoints. Plugin metadata, gateway OAuth and listing remain separate operations. API failures and argument-validation failures expose structured error results; the View does not parse error prose to determine write outcomes.

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
mcp-server-sms --transport streamable-http --host 0.0.0.0 --port 8000
```

Connect to `/mcp`. The deployment supplies HTTPS and access policy. Every HTTP request carries either `Authorization: <Base64 JSON>` or `Authorization: Bearer <Base64 JSON>` with the following credential fields:

```json
{"AccessKeyId":"<access-key>","SecretAccessKey":"<secret-key>","SessionToken":"<optional-session-token>"}
```

This follows the repository's credential-passing convention; it is **not an OAuth access token** and Base64 is not encryption. The client or trusted gateway must construct the header outside model context. HTTP never falls back to process credentials. Each SMS call uses these credentials for official V4 signing, and SMS/IAM enforces resource access. The server has no OAuth login flow or persistent caller identity.

When using the shared MCP gateway, the gateway owns OAuth login and authorization and forwards each customer's STS credentials. Do not pass ordinary OAuth tokens directly to this service or substitute the deployment account's credentials for customer credentials.

The MCP SDK applies its default transport security for `--host`. The legacy `--public-url` flag is accepted for startup compatibility. Requests do not require a protocol session or shared process state. Replicas can serve requests independently.

The HTTP connection pool is owned by the MCP server lifespan and closed at shutdown. Credentials and signed headers remain per-request, and response cookies are not retained between callers. Connection reuse does not introduce business state or a database.

## Outcomes and confirmation

- The client must obtain user authorization before calling tools with side effects. Tool annotations describe behavior; they do not prove user consent.
- SMS API acceptance and delivery are separate. Use the returned Message ID with `list_send_logs`; an empty result does not prove failure.
- Application creation is not audit approval. Query qualification, signature or template state separately.
- No API calls are automatically retried. A timeout or unconfirmed write returns `outcome_unknown`; do not blindly repeat it. This adapter does not provide durable request deduplication or an exactly-once guarantee.
- Unstructured HTTP 400/401/403/404/405/413/415/422/429 responses are explicit rejections. Other unstructured statuses, server errors, and malformed or incomplete successful write responses remain uncertain. API-response errors include `http_status` without echoing the response body.
- The upload API's top-level `url` is returned byte-for-byte, including its signed credential parameters. Other fields still undergo credential redaction. Treat the complete URL as a temporary capability; do not redact it before upload or expose it in logs.
- A successful API call can contain a failed business check, such as an invalid verification code, `Approved=false`, or nonempty protocol `fail`. Inspect the upstream fields. Carrier registration is not delivery proof. A batch list may omit status 2; query known task IDs directly.
- Application, activation and traffic-registration errors such as `1999/SY:0500` can have uncertain write outcomes. These operations are not automatically retried.
- Upstream error text is not echoed. Authentication fields and the private fields described above are removed; other business values retain their original content. Clients and deployment platforms must also configure their own logging and private-data handling.

Tool and physical API calls emit paired start/end events with correlation ID, Action, duration, outcome, public error code and RequestId. Logs go to stderr. OpenTelemetry uses the host's tracer provider; no exporter is configured by this package. Neither logging nor tracing failures change the business result. Events omit arguments, SMS content, phone numbers and authorization headers.

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

Tests exercise MCP, API mapping, credential isolation, uncertain writes, CSV, inline schemas, privacy, observations, UI resources and confirmation behavior. Python tests verify frontend source fingerprints against bundled HTML. Node.js is needed only for development builds; the wheel serves prebuilt resources. Upstream HTTP is mocked: no real qualifications or SMS are submitted. Actual write tests require separate customer authorization. Local results do not prove gateway OAuth, real ImageX/TOS upload, cloud deployment or a Doubao client integration.

API fields are checked against the [official SMS SDK](https://github.com/volcengine/volcengine-python-sdk/tree/3b116781c5b8bb648f215b29587f2ec74d9e5d02/volcenginesdkvolcsms). V4 signing uses the [official Python SDK](https://github.com/volcengine/volc-sdk-python). Qualification extension APIs use the existing SMS service contract; SDK coverage and account availability must be verified for the deployment.

The source version is 0.2.0. The repository's package workflow builds PRs and publishes new versions after merge, with maintainer PyPI permissions. Package publication, veFaaS upgrades and ATS/Plugin listing are separate operations. Licensed under Apache-2.0.
