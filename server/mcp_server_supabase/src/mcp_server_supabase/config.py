import os
import logging

logger = logging.getLogger(__name__)

READ_ONLY = os.getenv("READ_ONLY", "false").lower() == "true"

VOLCENGINE_ACCESS_KEY = os.getenv("VOLCENGINE_ACCESS_KEY")
VOLCENGINE_SECRET_KEY = os.getenv("VOLCENGINE_SECRET_KEY")
VOLCENGINE_REGION = os.getenv("VOLCENGINE_REGION", "cn-beijing")

# 验证必需的环境变量
if not VOLCENGINE_ACCESS_KEY:
    logger.warning("VOLCENGINE_ACCESS_KEY not set")
if not VOLCENGINE_SECRET_KEY:
    logger.warning("VOLCENGINE_SECRET_KEY not set")

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


def clear_endpoint_cache(workspace_id: str = None):
    if workspace_id:
        _endpoint_cache.pop(workspace_id, None)
    else:
        _endpoint_cache.clear()


def clear_api_key_cache(workspace_id: str = None):
    if workspace_id:
        _api_key_cache.pop(workspace_id, None)
    else:
        _api_key_cache.clear()


def clear_all_caches(workspace_id: str = None):
    """Clear all caches for a workspace or all workspaces"""
    clear_branch_cache(workspace_id)
    clear_endpoint_cache(workspace_id)
    clear_api_key_cache(workspace_id)
