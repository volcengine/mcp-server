import os
import logging

logger = logging.getLogger(__name__)

READ_ONLY = os.getenv("READ_ONLY", "false").lower() == "true"
VOLCENGINE_REGION = os.getenv("VOLCENGINE_REGION", "cn-beijing")

_default_branch_cache = {}
_endpoint_cache = {}
_api_key_cache = {}


def get_branch_cache():
    return _default_branch_cache


def get_endpoint_cache():
    return _endpoint_cache


def get_api_key_cache():
    return _api_key_cache


def clear_branch_cache(workspace_id: str = None):
    if workspace_id:
        _default_branch_cache.pop(workspace_id, None)
    else:
        _default_branch_cache.clear()


def clear_endpoint_cache(workspace_id: str = None, branch_id: str = None):
    if workspace_id and branch_id:
        _endpoint_cache.pop(f"{workspace_id}:{branch_id}", None)
    elif workspace_id:
        _endpoint_cache.pop(workspace_id, None)
        keys_to_delete = [key for key in _endpoint_cache if key.startswith(f"{workspace_id}:")]
        for key in keys_to_delete:
            _endpoint_cache.pop(key, None)
    else:
        _endpoint_cache.clear()


def clear_api_key_cache(workspace_id: str = None, branch_id: str = None):
    if workspace_id and branch_id:
        keys_to_delete = [key for key in _api_key_cache if key.startswith(f"{workspace_id}:") and key.endswith(f":{branch_id}")]
        for key in keys_to_delete:
            _api_key_cache.pop(key, None)
    elif workspace_id:
        keys_to_delete = [key for key in _api_key_cache if key == workspace_id or key.startswith(f"{workspace_id}:")]
        for key in keys_to_delete:
            _api_key_cache.pop(key, None)
    else:
        _api_key_cache.clear()


def clear_all_caches(workspace_id: str = None, branch_id: str = None):
    clear_branch_cache(workspace_id)
    clear_endpoint_cache(workspace_id, branch_id)
    clear_api_key_cache(workspace_id, branch_id)
