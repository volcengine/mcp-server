
import json
from pathlib import Path
from os import environ
from pydantic import BaseModel

VEFAAS_IAM_CRIDENTIAL_PATH = "/var/run/secrets/iam/credential"

class VeIAMCredential(BaseModel):
    access_key_id: str
    secret_access_key: str
    session_token: str

VOLCENGINE_ACCESS_KEY_ENV = 'VOLCENGINE_ACCESS_KEY'
VOLCENGINE_SECRET_KEY_ENV = 'VOLCENGINE_SECRET_KEY'
VOLCENGINE_SESSION_TOKEN_ENV = 'VOLCENGINE_SESSION_TOKEN'

def get_volcengine_credentials_base() -> VeIAMCredential:
    """Get Volcengine credentials from environment variables."""
    # 优先从环境变量读取
    access_key = environ.get(VOLCENGINE_ACCESS_KEY_ENV, '')
    secret_key = environ.get(VOLCENGINE_SECRET_KEY_ENV, '')
    session_token = environ.get(VOLCENGINE_SESSION_TOKEN_ENV, '')

    # 如果环境变量未完整配置，则尝试从 VeFaaS IAM 文件获取
    if not (access_key or secret_key or session_token):
        vefaas_cred = get_credential_from_vefaas_iam()
        access_key = vefaas_cred.access_key_id
        secret_key = vefaas_cred.secret_access_key
        session_token = vefaas_cred.session_token

    # 如果仍未获取到有效凭证，则抛出异常
    if not (access_key and secret_key):
        raise RuntimeError("无法获取有效的 Volcengine 凭证，请检查环境变量或 VeFaaS IAM 配置")
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