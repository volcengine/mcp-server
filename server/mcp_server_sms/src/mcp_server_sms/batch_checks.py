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
from .upload_models import SmsRequestError
from .uploads import recipient_rows

_VARIABLE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
_MAX_CHECK_CONTENTS = 100
_CHECK_WORKERS = 6
_CHECK_SECONDS = 25
_ROW_SAMPLE_LIMIT = 20
_TRAFFIC_ACTION = "CheckTrafficDrivingExist"


class BatchSelection(ApiModel):
    sub_account: Text
    signature: Text
    template_id: Text


class BatchTestSend(BatchSelection):
    mobile: Mobile = Field(repr=False)
    template_params: dict[str, str] = Field(default_factory=dict, repr=False)


class BatchTrafficCheck(BatchSelection):
    content: Text = Field(repr=False, description="页面已核对的实际正文，包含待按名单展开的变量")


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


def _group_rendered_contents(
    columns: list[str], text: str, data: bytes
):
    variables = _VARIABLE.findall(text)
    if text.count("${") != len(variables) or not set(variables).issubset(columns[1:]):
        raise SmsAPIError(failure(
            _TRAFFIC_ACTION, "invalid_batch_content", "正文变量不完整或与名单模板表头不一致"
        ))
    groups: dict[str, ContentGroup] = {}
    try:
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


async def check_batch_traffic(
    call, request: BatchTrafficCheck, *, data: bytes, columns: list[str]
) -> dict:
    """check_batch_traffic 按正文去重核对，保留覆盖数量、行号和原始调用错误。"""
    total, groups = _group_rendered_contents(columns, request.content, data)
    try:
        use_volc_link = await _short_link_mode(call, request)
    except SmsAPIError as exc:
        with observe_call("form", "batch", path="traffic_config_unavailable") as observation:
            observation.record(exc.result)
        return {
            "totalRows": total, "checkedRows": 0, "failedRows": 0, "uncheckedRows": total,
            "missingResourceRows": 0, "missingRowNumbers": [], "reason": "short_link_mode_unavailable",
            "failures": [exc.result],
        }
    checked = failed = missing = 0
    missing_lines = []
    failures = []
    work = iter(groups.items())

    async def worker():
        nonlocal checked, failed, missing
        for content, group in work:
            try:
                envelope = await call(_TRAFFIC_ACTION, {"content": content, "useVolcLink": use_volc_link})
                result = TrafficMatches.model_validate(envelope["result"])
            except SmsAPIError as exc:
                failures.append(exc.result)
                failed += group.count
                continue
            except ValidationError:
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
            **({"failures": failures} if failures else {}),
        }
