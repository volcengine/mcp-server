"""群发表单的单条试发和名单正文引流核对。"""

import re
from dataclasses import dataclass, field
from typing import Literal

from anyio import create_task_group, move_on_after
from pydantic import Field, ValidationError

from .client import failure
from .models import ApiModel, Mobile, Text
from .observability import observe_call
from .protocol import SmsAPIError
from .responses import ApiResult
from .upload_models import FileContent, RecipientsUpload, SmsRequestError
from .uploads import decode_file, recipient_columns, recipient_rows

_VARIABLE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
_MAX_CHECK_CONTENTS = 100
_CHECK_WORKERS = 6
_CHECK_SECONDS = 25
_ROW_SAMPLE_LIMIT = 20
_TRAFFIC_ACTION = "CheckTrafficDrivingExist"
_BATCH_ACTION = "ListBatchTemplatesForAgent"


class BatchSelection(ApiModel):
    sub_account: Text
    signature: Text
    template_id: Text


class BatchTestSend(BatchSelection):
    mobile: Mobile = Field(repr=False)
    template_content: Text = Field(repr=False)
    template_params: dict[str, str] = Field(default_factory=dict, repr=False)


class BatchTrafficCheck(BatchSelection):
    file: FileContent = Field(repr=False)
    content: str | None = Field(None, repr=False)
    template_content: str | None = Field(None, repr=False)


class TaskField(ApiResult):
    name: Literal["content"] = Field(alias="Name")
    required: bool = Field(False, alias="Required")


class BatchTemplate(ApiResult):
    id: Text = Field(alias="TemplateId")
    channel: Literal["CN_NTC", "CN_MKT"] = Field(alias="ChannelType")
    batch_only: bool = Field(False, alias="BatchOnly")
    template_content: str | None = Field(None, alias="TemplateContent")
    content: str | None = Field(None, alias="Content")
    task_fields: list[TaskField] = Field(default_factory=list, alias="TaskFields")


class TrafficResourceMatch(ApiResult):
    is_exist: bool = Field(alias="isExist")
    param_type: Literal[2, 3] = Field(alias="paramType")


class TrafficMatches(ApiResult):
    list: list[TrafficResourceMatch]


@dataclass
class ContentGroup:
    count: int = 0
    lines: list[int] = field(default_factory=list)


def _records(result: dict):
    value = result["result"]
    if not isinstance(value, dict):
        return None
    return value.get("List", value.get("list", value.get("Items", value.get("items"))))


async def _template(call, selection: BatchSelection) -> BatchTemplate:
    result = await call(_BATCH_ACTION, {
        "TemplateId": selection.template_id, "SubAccounts": [selection.sub_account],
        "Signatures": [selection.signature], "Page": 1, "PageSize": 100,
    })
    rows = _records(result)
    try:
        if not isinstance(rows, list) or len(rows) != 1:
            raise ValueError
        template = BatchTemplate.model_validate(rows[0])
        if template.id != selection.template_id:
            raise ValueError
    except (ValidationError, ValueError):
        raise SmsAPIError(failure(
            _BATCH_ACTION, "batch_template_unavailable", "未取得对应消息组和签名的明确群发模板",
            result["request_id"],
        )) from None
    return template


async def _columns(call, selection: BatchSelection) -> list[str]:
    demo = await call("TemplateUploadDemoForAgent", {
        "subAccount": selection.sub_account, "templateId": selection.template_id,
    })
    try:
        return recipient_columns(demo["result"]["value"])
    except SmsRequestError as exc:
        raise SmsAPIError(exc.result) from None


async def validate_batch_test(call, request: BatchTestSend) -> None:
    """validate_batch_test 试发前核对模板可单发，且参数与真实 CSV 变量一致。"""
    template = await _template(call, request)
    if template.batch_only or template.task_fields:
        raise SmsAPIError(failure("SendSmsForAgent", "batch_only_template", "该模板仅支持群发"))
    if request.template_content != (template.template_content or template.content):
        raise SmsAPIError(failure(
            "SendSmsForAgent", "batch_template_changed", "模板正文已变化，请重新核对后试发"
        ))
    columns = await _columns(call, request)
    if set(request.template_params) != set(columns[1:]) or not all(request.template_params.values()):
        raise SmsAPIError(failure(
            "SendSmsForAgent", "invalid_test_variables", "请按当前模板填写所有试发变量"
        ))


def batch_test_receipt(envelope: dict, requested_at: int) -> dict:
    """batch_test_receipt 用唯一有效的 Message ID 标识这次单条试发。"""
    result = envelope["result"]
    single, many = result.get("MessageId"), result.get("MessageIds")
    ids = []
    if single is not None:
        ids.append(single)
    if isinstance(many, list):
        ids.extend(many)
    if (
        not ids or (many is not None and not isinstance(many, list))
        or not all(isinstance(item, str) and item for item in ids)
        or len(set(ids)) != 1
    ):
        raise SmsAPIError(failure(
            "SendSmsForAgent", "outcome_unknown", "试发未返回明确的 Message ID，请核对发送记录",
            envelope["request_id"], outcome_unknown=True,
        ))
    return {"messageId": ids[0], "requestedAt": requested_at}


async def _short_link_mode(call, request: BatchTrafficCheck) -> bool:
    detail = await call("ListSecondTemplate", {
        "templateId": request.template_id, "signatures": request.signature,
        "subAccounts": [request.sub_account],
    })
    rows = _records(detail)
    modes = [
        row.get("useVolcLink") for row in rows if isinstance(row, dict)
        and row.get("TemplateId", row.get("templateId")) == request.template_id
    ] if isinstance(rows, list) else []
    if not modes or any(type(mode) is not bool for mode in modes) or len(set(modes)) != 1:
        raise SmsAPIError(failure(
            _TRAFFIC_ACTION, "short_link_mode_unknown", "模板短链配置未明确，请先核对模板",
            detail["request_id"],
        ))
    return modes[0]


def _group_rendered_contents(request: BatchTrafficCheck, columns: list[str], text: str):
    variables = _VARIABLE.findall(text)
    if text.count("${") != len(variables) or not set(variables).issubset(columns[1:]):
        raise SmsAPIError(failure(
            _TRAFFIC_ACTION, "invalid_batch_content", "正文变量不完整或与名单模板表头不一致"
        ))
    groups: dict[str, ContentGroup] = {}
    try:
        data, _ = decode_file(RecipientsUpload(
            kind="recipients", sub_account=request.sub_account, template_id=request.template_id,
            **request.file.model_dump(),
        ))
        total = 0
        for line, _, params in recipient_rows(data, columns):
            total += 1
            content = _VARIABLE.sub(lambda match: params[match[1]], text)
            if "${" in content:
                raise SmsAPIError(failure(
                    _TRAFFIC_ACTION, "invalid_batch_content", f"第 {line} 行正文仍含待填写变量"
                ))
            if content not in groups:
                if len(groups) >= _MAX_CHECK_CONTENTS:
                    continue
                groups[content] = ContentGroup()
            group = groups[content]
            group.count += 1
            if len(group.lines) < _ROW_SAMPLE_LIMIT:
                group.lines.append(line)
    except SmsRequestError as exc:
        raise SmsAPIError(exc.result) from None
    return total, groups


async def check_batch_traffic(call, request: BatchTrafficCheck) -> dict:
    """check_batch_traffic 渲染实际正文，按正文去重核对，仅返回覆盖数量与行号。"""
    template = await _template(call, request)
    if request.content is not None and not template.task_fields:
        raise SmsAPIError(failure(_TRAFFIC_ACTION, "invalid_batch_content", "该模板没有任务级正文"))
    text = request.content if request.content is not None else template.template_content or template.content
    if request.content is None and request.template_content is not None and request.template_content != text:
        raise SmsAPIError(failure(_TRAFFIC_ACTION, "batch_template_changed", "模板正文已变化，请重新核对"))
    if not text or (any(item.required for item in template.task_fields) and not request.content):
        raise SmsAPIError(failure(_TRAFFIC_ACTION, "invalid_batch_content", "请补齐实际短信正文"))
    columns = await _columns(call, request)
    total, groups = _group_rendered_contents(request, columns, text)
    try:
        use_volc_link = await _short_link_mode(call, request)
    except SmsAPIError as exc:
        with observe_call("form", "batch", path="traffic_config_unavailable") as observation:
            observation.record(exc.result)
        return {
            "totalRows": total, "checkedRows": 0, "failedRows": 0, "uncheckedRows": total,
            "missingResourceRows": 0, "missingRowNumbers": [], "reason": "short_link_mode_unavailable",
        }
    checked = failed = missing = 0
    missing_lines = []
    work = iter(groups.items())

    async def worker():
        nonlocal checked, failed, missing
        for content, group in work:
            try:
                envelope = await call(_TRAFFIC_ACTION, {"content": content, "useVolcLink": use_volc_link})
                result = TrafficMatches.model_validate(envelope["result"])
            except (SmsAPIError, ValidationError):
                failed += group.count
                continue
            checked += group.count
            if any(not item.is_exist for item in result.list):
                missing += group.count
                missing_lines.extend(group.lines)

    with observe_call("form", "batch", path="traffic_check") as observation:
        with move_on_after(_CHECK_SECONDS):
            async with create_task_group() as group:
                for _ in range(min(len(groups), _CHECK_WORKERS)):
                    group.start_soon(worker)
        observation.result_class = "success" if checked == total else "partial"
        return {
            "totalRows": total, "checkedRows": checked, "failedRows": failed,
            "uncheckedRows": total - checked - failed, "missingResourceRows": missing,
            "missingRowNumbers": sorted(missing_lines)[:_ROW_SAMPLE_LIMIT],
        }
