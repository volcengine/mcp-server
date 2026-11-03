from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class FieldRelationError(ValueError):
    pass


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int | float):
        return float(value)
    return None


def _operator_text(operator: str) -> str:
    return {
        "greater_than": "大于",
        "greater_than_or_equal": "大于等于",
        "less_than": "小于",
        "less_than_or_equal": "小于等于",
    }.get(operator, operator)


def validate_field_relations(schema: Mapping[str, Any], value: Any, path: str = "parameters") -> None:
    if not isinstance(value, dict):
        return
    for index, relation in enumerate(schema.get("x-field-relations") or []):
        if not isinstance(relation, dict):
            raise FieldRelationError(f"{path}.x-field-relations[{index}] 配置无效")
        operator = relation.get("operator")
        left = relation.get("left")
        right = relation.get("right")
        if not isinstance(operator, str) or not isinstance(left, str) or not isinstance(right, str):
            raise FieldRelationError(f"{path}.x-field-relations[{index}] 配置无效")
        if left not in value or right not in value:
            continue
        left_number = _number(value[left])
        right_number = _number(value[right])
        if left_number is None or right_number is None:
            raise FieldRelationError(f"{path}.{left} 与 {path}.{right} 必须是数字")
        ok = {
            "greater_than": left_number > right_number,
            "greater_than_or_equal": left_number >= right_number,
            "less_than": left_number < right_number,
            "less_than_or_equal": left_number <= right_number,
        }.get(operator)
        if ok is None:
            raise FieldRelationError(f"{path}.x-field-relations[{index}] operator {operator!r} 不支持")
        if not ok:
            raise FieldRelationError(f"{path}.{left} 必须{_operator_text(operator)} {path}.{right}")
    properties = schema.get("properties")
    if isinstance(properties, dict):
        for name, child_schema in properties.items():
            if name not in value or not isinstance(child_schema, dict):
                continue
            child_value = value[name]
            child_path = f"{path}.{name}"
            if isinstance(child_value, dict):
                validate_field_relations(child_schema, child_value, child_path)
            elif isinstance(child_value, list):
                items = child_schema.get("items")
                if isinstance(items, dict):
                    for index, item in enumerate(child_value):
                        if isinstance(item, dict):
                            validate_field_relations(items, item, f"{child_path}[{index}]")
