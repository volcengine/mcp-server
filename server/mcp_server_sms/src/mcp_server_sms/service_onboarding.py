"""国内短信表单的协议预览、授权提交和只读核对。"""

import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Annotated

from pydantic import Field, ValidationError

from .auth import Credentials
from .client import failure
from .configuration import FORM_CONFIG
from .observability import observe_call
from .protocol import SmsAPIError
from .responses import ApiResult

_ACTION = "ListAllSmsProduct"
_CONFIRM = "ConfirmProtocolDocument"
_ACTIVATE = "ActivateSmsProductInOneStep"
_CATALOG = FORM_CONFIG["smsOnboarding"]
_SUBMITTABLE = {"activation_required", "reopening_required", "protocol_confirmation_required"}
_PENDING = {"activation_pending", "protocol_confirmation_pending", "submission_outcome_unknown"}
_TERMINAL = {"available", "product_forced_closed", "account_disabled", "arrears_closed", "expired_closed"}
_MAX_UNRESOLVED = 1024
ServiceConfirmation = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class ProductState(ApiResult):
    product: str
    status: int
    user_status: int = Field(alias="userStatus")
    allowed: bool = Field(alias="isAllowed")


class AccountState(ApiResult):
    status: int
    new_account: bool = Field(alias="isNewAccount")
    business_name: str | None = Field(None, alias="businessName")
    documents: list[int]
    list: list[ProductState]


def _status(account: AccountState, product: ProductState, pending: list, unknown: set) -> str:
    if not product.allowed:
        return "product_not_allowed"
    if product.user_status == 2:
        return "product_forced_closed"
    if not account.new_account and account.status != 1:
        return "account_disabled" if account.status in (2, 3) else "service_state_unknown"
    if product.user_status not in (0, 1):
        return "service_state_unknown"
    if unknown:
        return "protocol_state_unknown"
    if product.status == 2 and product.user_status == 1 and not account.new_account:
        return "protocol_confirmation_required" if pending else "available"
    return {
        0: "activation_required", 1: "activation_pending", 3: "arrears_closed",
        4: "expired_closed", 5: "reopening_required",
    }.get(product.status, "service_state_unknown")


def _confirmation(view: dict, account: AccountState, product: ProductState, credentials) -> str:
    # 同一账号状态和协议清单才可确认。结果不携带凭据、服务端会话或持久化草稿。
    payload = json.dumps({
        "view": view, "accountStatus": account.status, "newAccount": account.new_account,
        "productStatus": product.status, "userStatus": product.user_status,
        "documents": sorted(set(account.documents)), "accessKey": credentials.access_key,
        "sessionToken": credentials.session_token,
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hmac.digest(credentials.secret_key.encode(), b"sms-onboarding\0" + payload, "sha256").hex()


async def read_service_onboarding(call, credentials: Credentials) -> dict:
    """read_service_onboarding 按实际账号状态生成当前要确认的国内短信协议。"""
    result = await call(_ACTION, {})
    try:
        account = AccountState.model_validate(result["result"])
        sms, = [item for item in account.list if item.product == "sms"]
    except (ValidationError, ValueError):
        raise SmsAPIError(failure(
            _ACTION, "service_state_unknown", "账号或国内短信商品状态不完整，请到短信控制台核对",
            result["request_id"],
        )) from None
    catalog = _CATALOG["protocols"]
    pending = [item for item in catalog if item["id"] in account.documents]
    known = {item["id"] for item in catalog} | set(_CATALOG["otherProductProtocolIds"])
    unknown = set(account.documents) - known
    status = _status(account, sms, pending, unknown)
    with observe_call("form", "service", path=status) as observation:
        protocols = []
        if status in _SUBMITTABLE:
            protocols = pending if status == "protocol_confirmation_required" else catalog
        view = {
            "status": status, "businessName": account.business_name, "protocols": protocols,
            "consoleUrl": _CATALOG["consoleUrl"], "pricingUrl": _CATALOG["pricingUrl"],
        }
        if protocols:
            view["confirmation"] = _confirmation(view, account, sms, credentials)
        observation.record(result)
        return view


async def _submit_service_onboarding(call, credentials: Credentials, current: dict) -> dict:
    status = current["status"]
    with observe_call("form", "service", path="submit_" + status) as observation:
        agreement = await call(_CONFIRM, {
            "product": "sms", "documents": [item["id"] for item in current["protocols"]],
        })
        if agreement["result"]["fail"]:
            observation.result_class = "partial"
            observation.request_id = agreement["request_id"]
            return {
                **{key: value for key, value in current.items() if key != "confirmation"},
                "status": "protocol_confirmation_failed", "requestId": agreement["request_id"],
                "failedDocuments": agreement["result"]["fail"],
            }

        submitted = agreement
        pending = "protocol_confirmation_pending"
        if status != "protocol_confirmation_required":
            try:
                submitted = await call(_ACTIVATE, {"product": ["sms"]})
            except SmsAPIError as exc:
                if exc.result["error"].get("outcome_unknown"):
                    raise
                observation.record(exc.result)
                return {
                    **{key: value for key, value in current.items() if key != "confirmation"},
                    "status": "activation_error", "requestId": exc.result["request_id"],
                    "errorCode": exc.result["error"]["code"],
                    "failure": exc.result,
                }
            order = submitted["result"]["list"][0]
            # 上游下单调用异常也可能返回非受理状态，只有回查能明确最终结果。
            pending = "activation_pending" if order["orderStatus"] == 1 else "submission_outcome_unknown"

        try:
            latest = await read_service_onboarding(call, credentials)
        except SmsAPIError as exc:
            latest = {**current, "failure": exc.result}
        if latest["status"] in _TERMINAL:
            pending = latest["status"]
        observation.result_class = "success" if pending == "available" else "partial"
        observation.request_id = submitted["request_id"]
        return {
            **{key: value for key, value in latest.items() if key != "confirmation"},
            "status": pending, "requestId": submitted["request_id"],
        }


@dataclass(frozen=True)
class _SubmissionReservation:
    status: str


class ServiceOnboarding:
    """ServiceOnboarding 防止同实例中同一登录凭据重复提交尚未核清的开通操作。"""

    def __init__(self):
        self._unresolved: dict[bytes, _SubmissionReservation] = {}

    @staticmethod
    def _scope(credentials: Credentials) -> bytes:
        return hashlib.sha256(credentials.access_key.encode()).digest()

    async def read(self, call, credentials: Credentials) -> dict:
        scope = self._scope(credentials)
        reservation_at_start = self._unresolved.get(scope)
        view = await read_service_onboarding(call, credentials)
        unresolved = self._unresolved.get(scope)
        if unresolved is None:
            return view
        status = view["status"]
        if (
            status in _TERMINAL and unresolved is reservation_at_start
            and unresolved.status != "submission_in_progress"
        ):
            self._unresolved.pop(scope, None)
            return view
        # 只允许本次回查解除它开始时的待核实占位。旧回查迟到时保留后来提交的状态。
        if status in _SUBMITTABLE or status in _TERMINAL:
            with observe_call("form", "service", path=unresolved.status) as observation:
                observation.result_class = "partial"
                return {
                    **{key: value for key, value in view.items() if key != "confirmation"},
                    "status": unresolved.status,
                }
        return view

    async def submit(self, call, credentials: Credentials, confirmation: str) -> dict:
        """submit 重新核对协议，原子占位后签署或开通，明确终态才释放占位。"""
        scope = self._scope(credentials)
        if scope in self._unresolved:
            raise SmsAPIError(failure(
                _CONFIRM, "service_submission_pending", "上次提交待核对，请刷新状态，勿重复提交",
                outcome_unknown=True,
            ))
        if len(self._unresolved) >= _MAX_UNRESOLVED:
            raise SmsAPIError(failure(
                _CONFIRM, "service_onboarding_busy", "待核对的开通操作较多，请到短信控制台查看"
            ))
        # 在读取可提交状态之前占位，避免并发请求持有同一份旧的商品状态。
        self._unresolved[scope] = _SubmissionReservation("submission_in_progress")
        write_started = False
        try:
            view = await read_service_onboarding(call, credentials)
            if view["status"] != "available":
                if not hmac.compare_digest(confirmation, view.get("confirmation", "")):
                    raise SmsAPIError(failure(
                        _CONFIRM, "service_confirmation_changed",
                        "账号状态或协议清单已变化，请刷新后重新确认",
                    ))
                write_started = True
                view = await _submit_service_onboarding(call, credentials, view)
        except SmsAPIError as exc:
            if write_started and exc.result["error"].get("outcome_unknown"):
                self._unresolved[scope] = _SubmissionReservation("submission_outcome_unknown")
            else:
                self._unresolved.pop(scope, None)
            raise
        except BaseException:
            # 宿主断开或任务取消时，也不能据此断言上游没有处理请求。
            if write_started:
                self._unresolved[scope] = _SubmissionReservation("submission_outcome_unknown")
            else:
                self._unresolved.pop(scope, None)
            raise
        if view["status"] in _PENDING:
            self._unresolved[scope] = _SubmissionReservation(view["status"])
        else:
            self._unresolved.pop(scope, None)
        return view
