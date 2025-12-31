from volcengine.vod.VodService import VodService
import json
import os
import logging
from typing import Dict, Any, Optional
from src.base.credential import get_volcengine_credentials_base, get_volcengine_credentials_from_context
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

class BaseService(VodService):

    def __init__(self):
        if os.getenv("VOLCENGINE_REGION") is None:
            region = "cn-north-1"
        else:
            region = os.getenv("VOLCENGINE_REGION")

        super().__init__(region=region)
        credentials = get_volcengine_credentials_base()
        self.set_ak(credentials.access_key_id)
        self.set_sk(credentials.secret_access_key)
        self.set_session_token(credentials.session_token)
        self.service_info.header["x-tt-mcp"] = 'volc'
        if os.getenv("VOLCENGINE_HOST"):
           self.set_host(os.getenv("VOLCENGINE_HOST"))  
        self.mcp_state = {}
        self._mcp_instance = None  # Store MCP instance for context access
        
    def update_credentials_from_mcp(self):
        """Update credentials from MCP context if mcp instance is available."""
        if self._mcp_instance is None:
            logging.debug("update_credentials_from_mcp: _mcp_instance is None, skipping")
            return
        
        try:
            ctx = self._mcp_instance.get_context()
            if ctx:
                logging.debug("update_credentials_from_mcp: got context, updating credentials")
                self.update_credentials_from_context(ctx)
            else:
                logging.debug("update_credentials_from_mcp: get_context() returned None")
        except Exception as e:
            logging.debug(f"update_credentials_from_mcp: Failed to get context from MCP instance: {e}")
            import traceback
            logging.debug(traceback.format_exc())
        
    @staticmethod
    def get_api_info():
        return api_info
    def set_api_info(self, api_info):
        self.api_info = {**self.api_info, **api_info}
        return
        
    def mcp_get(self, action, params={}, doseq=0):
        self.update_credentials_from_mcp()

        res = self.get(action, params, doseq)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json

    def mcp_post(self, action, params={}, body={}):
        self.update_credentials_from_mcp()
        res = self.json(action, params, body)
        if res == '':
            raise Exception("%s: empty response" % action)
        res_json = json.loads(json.dumps(res))
        return res_json
    def set_state(self, state: Dict[str, Any] = {}):
        self.mcp_state = {
            **self.mcp_state,
            **state
        }
    def get_state(self):
        return self.mcp_state
    
    def update_credentials_from_context(self, ctx: Optional[Context[ServerSession, object, Any]] = None):
        """Update credentials from MCP context headers.
        
        Args:
            ctx: MCP context object. If None, will try to get from current context.
        """
        if ctx is None:
            return
        
        try:
            # 从上下文获取凭证信息
            context_cred = get_volcengine_credentials_from_context(ctx)
            if context_cred:
                # 更新凭证
                if context_cred.get("access_key_id"):
                    self.set_ak(context_cred["access_key_id"])
                if context_cred.get("secret_access_key"):
                    self.set_sk(context_cred["secret_access_key"])
                if context_cred.get("session_token"):
                    self.set_session_token(context_cred["session_token"])
                
                # 更新 host
                if context_cred.get("host"):
                    self.set_host(context_cred["host"])
                
                # 更新 region
                if context_cred.get("region"):
                    # 注意：VodService 的 region 在初始化时设置，可能需要重新初始化
                    # 但为了兼容性，我们只更新 service_info 中的 region
                    if hasattr(self, 'service_info') and hasattr(self.service_info, 'region'):
                        self.service_info.region = context_cred["region"]
                
                logging.debug("Credentials updated from MCP context")
        except Exception as e:
            logging.warning(f"Failed to update credentials from context: {e}")
