
import json
import logging
from pathlib import Path
from os import environ
from pydantic import BaseModel
from typing import Optional, Dict, Any
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession
from starlette.requests import Request
from src.base.constant import (
    VOLCENGINE_ACCESS_KEY_HEADER,
    VOLCENGINE_SECRET_KEY_HEADER,
    VOLCENGINE_SESSION_TOKEN_HEADER,
    VOLCENGINE_HOST_HEADER,
    VOLCENGINE_REGION_HEADER,
    
    VOLCENGINE_ACCESS_KEY_ENV,
    VOLCENGINE_SECRET_KEY_ENV,
    VOLCENGINE_SESSION_TOKEN_ENV,
    VOLCENGINE_HOST_ENV,
    VOLCENGINE_REGION_ENV,
)

VEFAAS_IAM_CRIDENTIAL_PATH = "/var/run/secrets/iam/credential"

class VeIAMCredential(BaseModel):
    access_key_id: str
    secret_access_key: str
    session_token: str

# VOLCENGINE_ACCESS_KEY_ENV = 'VOLCENGINE_ACCESS_KEY'
# VOLCENGINE_SECRET_KEY_ENV = 'VOLCENGINE_SECRET_KEY'
# VOLCENGINE_SESSION_TOKEN_ENV = 'VOLCENGINE_SESSION_TOKEN'
# VOLCENGINE_HOST_ENV = 'VOLCENGINE_HOST'
# VOLCENGINE_REGION_ENV = 'VOLCENGINE_REGION'

def get_volcengine_credentials_from_context(ctx: Optional[Context[ServerSession, object]] = None) -> Optional[Dict[str, Any]]:
    """Get Volcengine credentials from MCP context headers.
    
    Args:
        ctx: MCP context object
        
    Returns:
        Dict containing credentials and config if found in headers, None otherwise.
        Keys: access_key_id, secret_access_key, session_token, host, region
    """
    print("get_volcengine_credentials_from_context: ctx", ctx.request_context.request)
    if ctx is None:
        return None
    
    try:
        raw_request: Optional[Request] = ctx.request_context.request
        if not raw_request:
            return None
        
        headers = raw_request.headers
        
        # 从 header 中读取凭证信息（使用与环境变量一致的命名，同时支持连字符和下划线格式）
        # 优先使用下划线格式（与环境变量一致），也支持连字符格式和 x- 前缀
        access_key = (
            headers.get(VOLCENGINE_ACCESS_KEY_HEADER) or
            None
        )
        secret_key = (
            headers.get(VOLCENGINE_SECRET_KEY_HEADER) or
            None
        )
        session_token = (
            headers.get(VOLCENGINE_SESSION_TOKEN_HEADER) or
            None
        )
        host = (
            headers.get(VOLCENGINE_HOST_HEADER) or
            None
        )
        region = (
            headers.get(VOLCENGINE_REGION_HEADER) or
            None
        )
        
        # 如果 header 中有 ak 和 sk，返回凭证信息
        if access_key and secret_key:
            result = {
                "access_key_id": access_key,
                "secret_access_key": secret_key,
                "session_token": session_token,
            }
            if host:
                result["host"] = host
            if region:
                result["region"] = region
            return result
        
        return None
    except Exception as e:
        logging.warning(f"Failed to get credentials from context: {e}")
        return None


def get_volcengine_credentials_base(ctx: Optional[Context[ServerSession, object]] = None) -> VeIAMCredential:
    """Get Volcengine credentials from context headers, environment variables, or VeFaaS IAM.
    
    Args:
        ctx: Optional MCP context object
        
    Returns:
        VeIAMCredential object
    """
    # 优先从 MCP 上下文 header 读取
    if ctx:
        context_cred = get_volcengine_credentials_from_context(ctx)
        print("context_cred",context_cred)
        if context_cred:
            return VeIAMCredential(
                access_key_id=context_cred.get("access_key_id", ""),
                secret_access_key=context_cred.get("secret_access_key", ""),
                session_token=context_cred.get("session_token", ""),
            )
    
    # 如果上下文没有，则从环境变量读取
    access_key = environ.get(VOLCENGINE_ACCESS_KEY_ENV, '')
    secret_key = environ.get(VOLCENGINE_SECRET_KEY_ENV, '')
    session_token = environ.get(VOLCENGINE_SESSION_TOKEN_ENV, '')

    # 如果环境变量未完整配置，则尝试从 VeFaaS IAM 文件获取
    if not (access_key or secret_key or session_token):
        vefaas_cred = get_credential_from_vefaas_iam()
        access_key = vefaas_cred.access_key_id
        secret_key = vefaas_cred.secret_access_key
        session_token = vefaas_cred.session_token

    # 如果仍未获取到有效凭证，仅打印警告（支持通过 Header 动态传递凭证）
    if not (access_key and secret_key):
        logging.warning("未检测到 Volcengine 凭证（环境变量/IAM），服务将以无凭证模式启动。请确保在请求 Header 中传递凭证。")
    return VeIAMCredential(
        access_key_id=access_key,
        secret_access_key=secret_key,
        session_token=session_token,
    )

def get_credential_from_vefaas_iam() -> VeIAMCredential:
    """Get credential from VeFaaS IAM file"""

    path = Path(VEFAAS_IAM_CRIDENTIAL_PATH)

    if not path.exists():

        return VeIAMCredential(
            access_key_id="",
            secret_access_key="",
            session_token="",
        )

    with open(VEFAAS_IAM_CRIDENTIAL_PATH, "r") as f:
        cred_dict = json.load(f)
        access_key = cred_dict["access_key_id"]
        secret_key = cred_dict["secret_access_key"]
        session_token = cred_dict["session_token"]

        return VeIAMCredential(
            access_key_id=access_key,
            secret_access_key=secret_key,
            session_token=session_token,
        )