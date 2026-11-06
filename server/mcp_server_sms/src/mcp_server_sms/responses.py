"""需要确认写入终态的响应契约；只校验，不重建或丢弃上游业务字段。"""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, model_validator


class ApiResult(BaseModel):
    model_config = ConfigDict(strict=True, extra="allow", hide_input_in_errors=True)


class BatchTaskCreated(ApiResult):
    task_id: str = Field(alias="taskId", min_length=1)
    total_count: int = Field(alias="totalCount", ge=0)
    dup_count: int = Field(alias="dupCount", ge=0)


class BatchTemplateDemo(ApiResult):
    value: Annotated[str, Field(min_length=1)]


class BatchContentChecked(ApiResult):
    approved: bool = Field(alias="Approved")


class ConfirmedProtocols(ApiResult):
    success: list[int]
    fail: list[int]

    @model_validator(mode="after")
    def match_requested_documents(self, info: ValidationInfo):
        documents = info.context.get("documents") if isinstance(info.context, dict) else None
        if not documents:
            raise ValueError("协议签署结果缺少本次请求的协议清单")
        succeeded, failed = set(self.success), set(self.fail)
        if succeeded | failed != set(documents) or succeeded & failed:
            raise ValueError("协议签署结果未完整对应本次请求")
        return self


class ActivationOrder(ApiResult):
    product: str
    order_status: int = Field(alias="orderStatus")
    order_detail: str | None = Field(None, alias="orderDetail")


class ActivationResult(ApiResult):
    list: Annotated[list[ActivationOrder], Field(min_length=1)]

    @model_validator(mode="after")
    def match_requested_products(self, info: ValidationInfo):
        products = info.context.get("product") if isinstance(info.context, dict) else None
        if not products or sorted(order.product for order in self.list) != sorted(products):
            raise ValueError("开通结果未完整对应本次请求的商品")
        return self
