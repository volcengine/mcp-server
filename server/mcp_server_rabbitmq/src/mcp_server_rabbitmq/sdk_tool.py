from __future__ import annotations

from volcenginesdkcore import ApiClient, Configuration, UniversalApi, UniversalInfo


def create_universal_info(
    service: str,
    action: str,
    version: str = "2021-09-01",
    method: str = "POST",
    content_type: str | None = "application/json",
):
    if content_type is None:
        content_type = "application/json"
    if method == "GET":
        content_type = "text/plain"

    return UniversalInfo(
        method=method,
        service=service,
        version=version,
        action=action,
        content_type=content_type,
    )


def create_api_client(
    ak: str,
    sk: str,
    session_token: str = "",
    region: str = "cn-beijing",
    host: str = "open.volcengineapi.com",
    scheme: str = "https",
):
    config = Configuration()
    # volcenginesdkcore 的类型标注不完整，这里用 setattr 保持运行时行为不变。
    setattr(config, "ak", ak)
    setattr(config, "sk", sk)
    setattr(config, "host", host)
    setattr(config, "scheme", scheme)
    setattr(config, "region", region)
    if session_token:
        setattr(config, "session_token", session_token)

    return UniversalApi(ApiClient(config))


__all__ = [
    "create_api_client",
    "create_universal_info",
]
