import json
import os
from pathlib import Path
import base64
from typing import Dict, Union, get_args

import yaml

from .model import *
from .variable import *


# 读取文件
def load_swagger(file_name):
    config_path = ''
    try:
        # 获取当前文件所在目录
        current_dir = Path(__file__).parent
        config_path = current_dir / 'config' / file_name
        with open(config_path, 'r', encoding='utf-8') as file:
            result = json.load(file)
            return result
    except FileNotFoundError:
        raise FileNotFoundError(f"swagger文件未找到: {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"无效的JSON格式: {str(e)}", e.doc, e.pos)
    except IOError as e:
        raise IOError(f"读取swagger文件时发生错误: {str(e)}")


def load_config(file_name: Union[str, Path]) -> Config:
    config_path = ''
    try:
        current_dir = Path(__file__).parent
        config_path = current_dir / 'config' / file_name
        with open(config_path, 'r', encoding='utf-8') as f:
            config_dict = yaml.safe_load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML 文件未找到: {config_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"无效的 YAML 格式: {e}")

    # 构建OAuth配置
    oauth_config = None
    if 'oauth' in config_dict:
        oauth_data = config_dict.pop('oauth')
        oauth_config = OAuthConfig(
            client_id=oauth_data.get('client_id', ''),
            client_secret=oauth_data.get('client_secret', ''),
            authorize_url=oauth_data.get('authorize_url', ''),
            token_url=oauth_data.get('token_url', ''),
            scope=oauth_data.get('scope', '')
        )

    # 创建主配置对象
    try:
        cfg = Config(
            service_code=config_dict.get('service_code', ''),
            transport=config_dict.get('transport', ''),
            auth=config_dict.get('auth', 'none'),
            credential=config_dict.get('credential', 'env'),
            sse_port=config_dict.get('sse_port', 8888),
            oauth=oauth_config
        )

        env_mapping = [
            (VOLCENGINE_ACCESS_KEY, "ak", None, None),
            (VOLCENGINE_SECRET_KEY, "sk", None, None),
            (VOLCENGINE_ACCESS_SESSION_TOKEN, "sts_token", None, None),
            (VOLCENGINE_CREDENTIAL_TYPE, "credential", None, get_args(CredentialType)),
            (MCP_SERVER_MODE, "transport", None, get_args(TransportType)),
            (MCP_SERVER_AUTH, "auth", None, get_args(AuthType)),
            (MCP_SERVER_PORT, "sse_port", int, None),
        ]

        for env_var, attr_name, converter, allowed_values in env_mapping:
            env_value_str = os.environ.get(env_var)
            if env_value_str is not None and env_value_str != "":
                # 转换类型
                value_to_set = converter(env_value_str) if converter else env_value_str
                # 验证 Literal 类型的值
                if allowed_values is not None and value_to_set not in allowed_values:
                    raise ValueError(f"Invalid value '{value_to_set}'. Allowed: {allowed_values}")
                setattr(cfg, attr_name, value_to_set)
        # 参数校验
        cfg.check()
        return cfg
    except (ValueError, TypeError) as e:
        raise ValueError(f"读取配置文件时发生错误 {e}")


def validate_auth_header(auth_header: Optional[str], server_config: Optional[Config],
                         token_store: Optional[dict]) -> Dict:
    if not auth_header:
        return {"is_valid": False, "error": "Authorization header missing"}
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return {"is_valid": False, "error": "Invalid authorization format"}
    token = parts[1]
    if not token:
        return {"is_valid": False, "error": "Empty token"}
    try:
        if server_config.auth == AUTH_TYPE_OAUTH:
            if token_store.get(token) is None:
                return {"is_valid": False, "error": "Invalid authorization token"}
            else:
                return {"is_valid": True, "credentials": {}}
        elif server_config.credential == 'token':
            sts_str = token
            decoded_str = base64.b64decode(sts_str).decode('utf-8')
            data = json.loads(decoded_str)
            credentials = {
                "ak": data.get('AccessKeyId'),
                "sk": data.get('SecretAccessKey'),
                "session_token": data.get('SessionToken')
            }
            if credentials['ak'] is None or credentials['sk'] is None:
                return {"is_valid": False, "error": "Incomplete credentials"}
            return {
                "is_valid": True,
                "credentials": credentials
            }
        else:
            return {"is_valid": False, "error": "Invalid authorization type"}

    except Exception as e:
        return {"is_valid": False, "error": f"Token validation failed: {str(e)}"}


def filter_params(params_dict):
    filtered_dict = {}
    for key, value in params_dict.items():
        # 检查值是否不是 None 并且不是空列表
        if value is not None and not (isinstance(value, list) and not value):
            filtered_dict[key] = value
    return filtered_dict
