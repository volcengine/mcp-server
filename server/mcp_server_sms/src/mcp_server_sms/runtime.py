"""SMS workflows, frozen previews, owned drafts and mutation guards."""

import dataclasses
import hashlib
import json
import os
import pathlib
import tempfile
import time
import uuid
from contextlib import contextmanager

from .auth import AuthenticationError, Authenticator, sms_credentials
from .core import qualification, workflows
from .core.qualification_upload import (
    QualificationUploadError,
    _diagnostic_value,
    _diagnostic_replacements,
)
from .core.action_contracts import ACTION_REGISTRY
from .core.api_client import SmsApiClient
from .core.api_protocol import sanitize_output
from .store import Store, StoreError
from .inputs import InputFiles


class GuardedClient:
    """Deduplicate actual SMS mutations before dispatch, including qualification submission."""

    def __init__(self, client, store, owner, operation_id, ttl):
        self.client, self.store, self.owner = client, store, owner
        self.operation_id, self.ttl = operation_id, ttl
        self._timeout = client._timeout

    def call(self, action, params, **kwargs):
        if ACTION_REGISTRY[action].read_only:
            return self.client.call(action, params, **kwargs)
        return self.store.once(
            self.owner,
            self.operation_id + ":" + action,
            params,
            self.ttl,
            lambda: self.client.call(action, params, **kwargs),
        )


class Runtime:
    def __init__(self, settings, *, store=None):
        self.settings = settings
        self.store = store or Store(settings.database_url, settings.encryption_key)
        self.auth = Authenticator(settings)
        self.inputs = InputFiles(self.store, settings.flow_ttl, settings.input_root)

    def caller(self, ctx):
        self.store.cleanup()
        headers = ctx.headers
        if headers is None:
            owner = os.environ.get("SMS_MCP_LOCAL_SUBJECT")
            if not owner:
                raise AuthenticationError("stdio 模式需要 SMS_MCP_LOCAL_SUBJECT")
        else:
            owner = self.auth.owner(headers)
        return owner, sms_credentials(headers)

    @staticmethod
    def arguments(command, options):
        argv = [command]
        for key, value in options.items():
            if value is None or value is False:
                continue
            flag = "--" + key.replace("_", "-")
            if value is True:
                argv.append(flag)
            else:
                for item in value if isinstance(value, list) else [value]:
                    encoded = (
                        json.dumps(item, ensure_ascii=False)
                        if isinstance(item, dict)
                        else str(item)
                    )
                    argv.append(flag + "=" + encoded)

        return workflows.build_parser().parse_args(argv)

    def query(self, command, options, owner, credentials):
        client = SmsApiClient(credentials)
        result = workflows.execute(self.arguments(command, options), client)
        return self.safe(result, credentials)

    def template_detail(self, template_id, signature, sub_account, owner, credentials):
        detail = workflows._direct_send_template_detail(
            SmsApiClient(credentials), template_id, signature, sub_account
        )
        content = detail["Content"]
        safe_content = self.safe({"content": content}, credentials)["content"]
        return {
            "templateId": template_id,
            "subAccount": sub_account,
            "signature": signature,
            "channelType": workflows._template_value(
                detail, "ChannelType", "channelType"
            ),
            "content": safe_content,
            "contentRedacted": safe_content != content,
            "contentSha256": hashlib.sha256(content.encode("utf-8")).hexdigest(),
            "variables": workflows._template_param_names(detail),
            "status": workflows._template_value(detail, "Status", "status"),
        }

    @staticmethod
    def safe(result, credentials):
        return sanitize_output(
            result, secrets=tuple(dataclasses.asdict(credentials).values())
        )

    def prepare(self, kind, options, owner, credentials):
        command = {
            "signature": "signature-preview",
            "template": "template-preview",
            "send": "send-preview",
            "batch_launch": "batch-launch-preview",
        }[kind]
        result = workflows.execute(
            self.arguments(command, options), SmsApiClient(credentials)
        )
        if not result.get("success"):
            return self.safe(result, credentials)
        result_data = result["result"]
        digest = result_data["digest"]
        operation_id = self.store.create(
            owner,
            "preview",
            {
                "kind": kind,
                "options": options,
                "digest": digest,
                "credential_fingerprint": self.credential_fingerprint(credentials),
            },
            self.settings.flow_ttl,
        )
        return {
            "operationId": operation_id,
            "preview": self.safe(result_data, credentials),
            "requiresConfirmation": True,
            "expiresInSeconds": self.settings.flow_ttl,
        }

    @staticmethod
    def credential_fingerprint(credentials):
        # A preview remains attached to the exact delegated identity; changing a
        # credential requires a new preview instead of sending on another account.
        return hashlib.sha256(
            json.dumps(dataclasses.asdict(credentials), sort_keys=True).encode()
        ).hexdigest()

    def execute(self, operation_id, owner, credentials):
        stored_preview = self.store.get(operation_id, owner, "preview")
        record = stored_preview["data"]
        operation_ttl = max(
            self.settings.operation_ttl,
            int(stored_preview["expires"] - time.time()) + 1,
        )
        if record["credential_fingerprint"] != self.credential_fingerprint(credentials):
            raise StoreError("调用凭据已变化，请重新生成预览")

        def run():
            options, kind = dict(record["options"]), record["kind"]
            client = GuardedClient(
                SmsApiClient(credentials),
                self.store,
                owner,
                operation_id,
                operation_ttl,
            )
            try:
                if kind in ("qualification", "qualification_code"):
                    return self._execute_qualification(
                        kind, options, record["digest"], owner, credentials
                    )
                if kind == "batch_create":
                    return self._create_batch(options, record["digest"], client, owner)
                if kind == "batch_cancel":
                    result = workflows.execute(
                        self.arguments("batch-cancel", options), client
                    )
                else:
                    options["preview_digest"] = record["digest"]
                    if kind == "send":
                        options["authorization_digest"] = record["digest"]
                    if kind == "batch_launch":
                        options["authorization_text"] = (
                            "确认启动任务 " + options["task_id"]
                        )
                    command = {
                        "signature": "signature-submit",
                        "template": "template-submit",
                        "send": "send-submit",
                        "batch_launch": "batch-launch-submit",
                    }[kind]
                    result = workflows.execute(self.arguments(command, options), client)
                return self.safe(result, credentials)
            except workflows.CliError as exc:
                return self.safe(
                    {
                        "success": False,
                        "error": {"code": exc.code, "message": str(exc)},
                    },
                    credentials,
                )

        return self.store.once(
            owner, "execute:" + operation_id, record, operation_ttl, run
        )

    def operation_result(self, operation_id, owner, credentials):
        operation = self.store.operation(owner, "execute:" + operation_id)
        if operation is None:
            self.store.get(operation_id, owner, "preview")
            return {"operationId": operation_id, "status": "not_executed"}
        if operation["status"] != "completed":
            return {
                "operationId": operation_id,
                "status": "outcome_unknown",
                "outcomeUnknown": True,
            }
        return self.safe(operation["data"]["result"], credentials)

    def qualification_requirements(self, owner, credentials):
        return qualification.requirements(
            qualification.new_state(SmsApiClient(credentials))
        )

    def create_qualification_draft(self, name, purpose, owner, credentials):
        client = SmsApiClient(credentials)
        state = qualification.new_state(client)
        qualification.QualificationDraft(client, state).set_base(name, purpose)
        draft_id = self.store.create(
            owner,
            "qualification",
            {
                "state": state,
                "credential_fingerprint": self.credential_fingerprint(credentials),
            },
            self.settings.flow_ttl,
        )
        return {
            "draftId": draft_id,
            "expiresInSeconds": self.settings.flow_ttl,
            **qualification.public_state(state),
            "requirements": qualification.requirements(state),
        }

    def _recover_qualification(self, draft_id, owner, state):
        if state["done"]:
            return
        operation = self.store.operation(
            owner,
            f"qualification:{draft_id}:submit:{state['revision']}:ApplySignatureIdentificationForAgent",
        )
        if operation is None:
            return
        result = operation["data"].get("result")
        if operation["status"] == "completed" and result and result.get("success"):
            value = result.get("result")
            if type(value) is int and value > 0:
                state.update(
                    done=True,
                    result={
                        "status": "submitted_for_review",
                        "qualificationId": value,
                        "requestId": result.get("request_id"),
                        "revision": state["revision"],
                    },
                )
                return
        if (
            result
            and result.get("success") is False
            and not (result.get("error") or {}).get("outcome_unknown")
        ):
            return
        state.update(
            done=True,
            result={
                "status": "qualification_submission_outcome_unknown",
                "outcomeUnknown": True,
                "requestId": (result or {}).get("request_id"),
            },
        )

    @contextmanager
    def _draft(self, draft_id, owner, credentials, *, operation_id=None):
        with self.store.locked(draft_id, owner, "qualification") as (record, lease):
            data = record["data"]
            if data["credential_fingerprint"] != self.credential_fingerprint(
                credentials
            ):
                raise StoreError("调用凭据已变化，请在原授权有效期内处理草稿或重新创建")
            state = data["state"]
            self._recover_qualification(draft_id, owner, state)
            client = SmsApiClient(credentials)
            if operation_id:
                client = GuardedClient(
                    client,
                    self.store,
                    owner,
                    operation_id,
                    max(
                        self.settings.operation_ttl,
                        int(record["expires"] - time.time()) + 1,
                    ),
                )
            try:
                yield qualification.QualificationDraft(client, state)
            finally:
                if state["done"]:
                    data["state"] = {"done": True, "result": state["result"]}
                self.store.save(draft_id, owner, data, lease=lease)

    def qualification_status(self, draft_id, owner, credentials):
        with self._draft(draft_id, owner, credentials) as draft:
            return {"draftId": draft_id, **qualification.public_state(draft.state)}

    def cancel_qualification(self, draft_id, owner, credentials):
        with self._draft(draft_id, owner, credentials) as draft:
            if not draft.state["done"]:
                draft.state.update(
                    done=True, result={"status": "qualification_application_abandoned"}
                )
            return {"draftId": draft_id, **qualification.public_state(draft.state)}

    def change_qualification(
        self, draft_id, action, owner, credentials, *, operation_id=None
    ):
        with self._draft(
            draft_id, owner, credentials, operation_id=operation_id
        ) as draft:
            if draft.state["done"]:
                raise StoreError("资质草稿已结束，请查询结果")
            try:
                detail = action(draft) or {}
                return {
                    "draftId": draft_id,
                    **qualification.public_state(draft.state),
                    **detail,
                }
            except QualificationUploadError as error:
                return self._qualification_error(error, draft.state)
            except (ValueError, KeyError, TypeError) as error:
                message = (
                    str(error)
                    if isinstance(error, ValueError) and str(error)
                    else "材料字段不完整或格式不正确"
                )
                return {
                    "success": False,
                    "error": {
                        "code": "invalid_qualification_input",
                        "message": message,
                    },
                }

    @staticmethod
    def _qualification_error(error, state):
        return {
            "success": False,
            "error": {
                "code": error.code,
                "message": _diagnostic_value(
                    str(error),
                    field="message",
                    replacements=_diagnostic_replacements(state),
                ),
                "requestId": error.request_id,
                "logId": error.log_id,
                "outcome_unknown": error.outcome_unknown,
            },
        }

    def update_qualification_information(
        self, draft_id, target, file_id, owner, credentials
    ):
        document = self.inputs.document(file_id, owner)
        return self.change_qualification(
            draft_id,
            lambda draft: draft.set_information(target, document),
            owner,
            credentials,
        )

    def upload_qualification_document(
        self, draft_id, file_id, options, owner, credentials
    ):
        content, content_type = self.inputs.read(file_id, owner, "qualification_image")
        return self.change_qualification(
            draft_id,
            lambda draft: draft.upload_document(content, content_type, **options),
            owner,
            credentials,
        )

    def recognize_qualification_document(self, draft_id, target, owner, credentials):
        def recognize(draft):
            result = draft.recognize_document(target)
            uploaded = self.inputs.stage(
                owner,
                "qualification_data",
                json.dumps(result, ensure_ascii=False).encode(),
                "application/json",
            )
            return {
                "reviewFileId": uploaded["fileId"],
                "recognitionStatus": "requires_customer_review",
            }

        return self.change_qualification(draft_id, recognize, owner, credentials)

    def prepare_qualification(self, draft_id, role, owner, credentials):
        with self._draft(draft_id, owner, credentials) as draft:
            if draft.state["done"]:
                raise StoreError("资质草稿已结束")
            options = {"draft_id": draft_id, "revision": draft.state["revision"]}
            if role is None:
                preview = draft.preview()
                kind = "qualification"
                digest = workflows.canonical_digest(
                    qualification._submission_payload(draft.state)
                )
            else:
                mobile = draft.code_recipient(role)
                options["role"] = role
                preview = {
                    "role": role,
                    "mobile": mobile,
                    "action": "send_verification_code",
                }
                kind = "qualification_code"
                digest = workflows.canonical_digest({**options, "mobile": mobile})
            operation_id = self.store.create(
                owner,
                "preview",
                {
                    "kind": kind,
                    "options": options,
                    "digest": digest,
                    "credential_fingerprint": self.credential_fingerprint(credentials),
                },
                self.settings.flow_ttl,
            )
            return {
                "operationId": operation_id,
                "preview": self.safe(_diagnostic_value(preview), credentials),
                "requiresConfirmation": True,
                "expiresInSeconds": self.settings.flow_ttl,
            }

    def _execute_qualification(self, kind, options, digest, owner, credentials):
        draft_id, revision = options["draft_id"], options["revision"]
        action = "submit" if kind == "qualification" else "code:" + options["role"]
        with self._draft(
            draft_id,
            owner,
            credentials,
            operation_id=f"qualification:{draft_id}:{action}:{revision}",
        ) as draft:
            if draft.state["done"]:
                if (
                    draft.state["result"].get("status")
                    == "qualification_application_abandoned"
                ):
                    return {
                        "success": False,
                        "error": {
                            "code": "qualification_draft_cancelled",
                            "message": "资质草稿已取消，不能提交",
                        },
                    }
                return {
                    "success": not draft.state["result"].get("outcomeUnknown", False),
                    "result": draft.state["result"],
                }
            try:
                if draft.state["revision"] != revision:
                    raise ValueError("申请信息已变化，请重新生成并确认预览")
                if kind == "qualification":
                    if (
                        workflows.canonical_digest(
                            qualification._submission_payload(draft.state)
                        )
                        != digest
                    ):
                        raise ValueError("申请内容与预览不一致")
                    result = draft.submit(revision)
                else:
                    mobile = draft.code_recipient(options["role"])
                    if (
                        workflows.canonical_digest({**options, "mobile": mobile})
                        != digest
                    ):
                        raise ValueError("验证码收件人与预览不一致")
                    result = draft.send_code(options["role"])
                return {"success": True, "result": result}
            except QualificationUploadError as error:
                return self._qualification_error(error, draft.state)
            except ValueError as error:
                return {
                    "success": False,
                    "error": {
                        "code": "stale_qualification_preview",
                        "message": str(error),
                    },
                }

    def verify_qualification_code(
        self, draft_id, role, file_id, request_id, owner, credentials
    ):
        uuid.UUID(request_id)
        document = self.inputs.document(file_id, owner, "verification_code")
        try:
            return self.change_qualification(
                draft_id,
                lambda draft: draft.verify_code(role, document["code"]),
                owner,
                credentials,
                operation_id=f"qualification:{draft_id}:verify:{request_id}",
            )
        finally:
            self.store.delete_file(file_id, owner)

    def check_batch_file(
        self, file_id, sub_account, signature, template_id, owner, credentials
    ):
        content, _ = self.inputs.read(file_id, owner, "batch_csv")
        _, variables = workflows._batch_resources(
            SmsApiClient(credentials), sub_account, signature, template_id
        )
        return workflows.precheck_batch_csv(content, variables)

    def _batch_preview(self, options, client, owner):
        content, _ = self.inputs.read(options["file_id"], owner, "batch_csv")
        template, variables = workflows._batch_resources(
            client, options["sub_account"], options["signature"], options["template_id"]
        )
        report = workflows.precheck_batch_csv(content, variables)
        digest = workflows.canonical_digest(
            {
                "options": options,
                "template": template,
                "fileSha256": report["fileSha256"],
            }
        )
        return content, report, digest

    def prepare_batch(self, options, owner, credentials):
        _, report, digest = self._batch_preview(
            options, SmsApiClient(credentials), owner
        )
        operation_id = self.store.create(
            owner,
            "preview",
            {
                "kind": "batch_create",
                "options": options,
                "digest": digest,
                "credential_fingerprint": self.credential_fingerprint(credentials),
            },
            self.settings.flow_ttl,
        )
        return {
            "operationId": operation_id,
            "preview": {**options, **report},
            "requiresConfirmation": True,
            "note": "创建群发任务后还需要单独确认启动",
        }

    def _create_batch(self, options, expected_digest, client, owner):
        content, _, digest = self._batch_preview(options, client, owner)
        if digest != expected_digest:
            raise workflows.CliError("文件或模板已变化，请重新预览", "digest_mismatch")
        with tempfile.TemporaryDirectory(prefix="sms-mcp-batch-") as directory:
            path = pathlib.Path(directory) / "recipients.csv"
            path.write_bytes(content)
            os.chmod(path, 0o600)
            args = {k: v for k, v in options.items() if k != "file_id"}
            args["file"] = str(path)
            return workflows.execute(self.arguments("batch-create", args), client)

    def prepare_cancel(self, options, owner, credentials):
        result = self.query("batch-detail", options, owner, credentials)
        if not result.get("success"):
            return result
        operation_id = self.store.create(
            owner,
            "preview",
            {
                "kind": "batch_cancel",
                "options": options,
                "credential_fingerprint": self.credential_fingerprint(credentials),
            },
            self.settings.flow_ttl,
        )
        return {
            "operationId": operation_id,
            "preview": result["result"],
            "requiresConfirmation": True,
        }
