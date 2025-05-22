from dataclasses import dataclass, field
from typing import List, Optional, Literal

from pydantic import BaseModel, ConfigDict

CredentialType = Literal["env", "token"]
TransportType = Literal["sse", "stdio"]
AuthType = Literal["none", "oauth"]


@dataclass
class OAuthConfig:
    client_id: str
    client_secret: str
    authorize_url: str
    token_url: str
    scope: List[str]


@dataclass
class Config:
    service_code: str
    sse_port: int
    transport: TransportType  # 支持 "sse" 或 "stdio"
    auth: AuthType  # 支持 "oauth" 或 "none"
    credential: CredentialType  # 支持 "env" 或 "token"
    oauth: Optional[OAuthConfig] = None
    ak: Optional[str] = None
    sk: Optional[str] = None
    sts_token: Optional[str] = None

    def check(self):
        # 验证 service_code
        if self.service_code is None:
            raise ValueError("service_code must have been initialized")
        # 验证 auth 和 oauth 的一致性
        if self.auth == "oauth" and (self.oauth is None or self.oauth.client_id is None):
            raise ValueError("OAuth configuration required when auth is set to oauth")

        if self.auth == "oauth" and self.credential == "token":
            raise ValueError("credential can not be token when auth is set to oauth")

        if self.transport == "sse" and self.sse_port == 0:
            raise ValueError("sse port can not be 0")


class OAuthClientRegistration(BaseModel):
    """OAuth客户端注册信息模型"""
    redirect_uris: List[str]
    client_name: str
    grant_types: List[str]
    response_types: List[str]
    token_endpoint_auth_method: str


# 定义返回类型
class TopResponseModel(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        from_attributes=True,
        arbitrary_types_allowed=True  # 允许任意类型
    )

    def __init__(self, **data):
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = TopResponseModel(**value)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                data[key] = [TopResponseModel(**item) for item in value]
        super().__init__(**data)
