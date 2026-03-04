import logging
from typing import Optional, Dict, Any
from ..config import (
    VOLCENGINE_ACCESS_KEY,
    VOLCENGINE_SECRET_KEY,
    VOLCENGINE_REGION,
    get_branch_cache,
    get_endpoint_cache,
    get_api_key_cache
)

logger = logging.getLogger(__name__)

try:
    import volcenginesdkcore
    from volcenginesdkaidap import AIDAPApi
    from volcenginesdkaidap.models import (
        DescribeBranchesRequest,
        DescribeWorkspaceEndpointRequest,
        DescribeAPIKeysRequest,
        DescribeComputesRequest,
    )
except ImportError:
    logger.error("volcengine-python-sdk not installed")
    raise


class AidapClient:
    def __init__(self) -> None:
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = VOLCENGINE_ACCESS_KEY
        configuration.sk = VOLCENGINE_SECRET_KEY
        configuration.region = VOLCENGINE_REGION

        api_client = volcenginesdkcore.ApiClient(configuration)
        self.client = AIDAPApi(api_client)
    
    async def get_default_branch_id(self, workspace_id: str, use_cache: bool = True) -> Optional[str]:
        cache = get_branch_cache()
        if use_cache and workspace_id in cache:
            return cache[workspace_id]
        
        try:
            request = DescribeBranchesRequest(workspace_id=workspace_id)
            response = self.client.describe_branches(request)
            
            if hasattr(response, 'branches') and response.branches:
                for branch in response.branches:
                    if getattr(branch, 'default', False):
                        branch_id = branch.branch_id
                        cache[workspace_id] = branch_id
                        return branch_id
                
                first_branch = response.branches[0]
                branch_id = first_branch.branch_id
                cache[workspace_id] = branch_id
                return branch_id
            
            return None
        except Exception as e:
            logger.error(f"Error getting default branch: {e}")
            return None
    
    async def get_endpoint(self, workspace_id: str, branch_id: Optional[str] = None, use_cache: bool = True) -> Optional[str]:
        # 检查缓存
        cache_key = f"{workspace_id}:{branch_id}" if branch_id else workspace_id
        endpoint_cache = get_endpoint_cache()

        if use_cache and cache_key in endpoint_cache:
            return endpoint_cache[cache_key]

        if not branch_id:
            branch_id = await self.get_default_branch_id(workspace_id)
            if not branch_id:
                return None

        try:
            request = DescribeWorkspaceEndpointRequest(
                workspace_id=workspace_id,
                branch_id=branch_id
            )
            response = self.client.describe_workspace_endpoint(request)

            if hasattr(response, 'endpoints') and response.endpoints:
                domains = []
                for endpoint in response.endpoints:
                    if hasattr(endpoint, 'addresses') and endpoint.addresses:
                        for addr in endpoint.addresses:
                            if hasattr(addr, 'address_domain'):
                                domains.append(addr.address_domain)

                for domain in domains:
                    if 'volces.com' in domain and 'ivolces.com' not in domain:
                        result = f"http://{domain}:80"
                        endpoint_cache[cache_key] = result
                        return result

                if domains:
                    result = f"http://{domains[0]}:80"
                    endpoint_cache[cache_key] = result
                    return result

            return None
        except Exception as e:
            logger.error(f"Error getting endpoint: {e}")
            return None
    
    async def get_api_key(self, workspace_id: str, key_type: str = "service_role",
                         branch_id: Optional[str] = None, use_cache: bool = True) -> Optional[str]:
        # 检查缓存
        cache_key = f"{workspace_id}:{key_type}:{branch_id}" if branch_id else f"{workspace_id}:{key_type}"
        api_key_cache = get_api_key_cache()

        if use_cache and cache_key in api_key_cache:
            return api_key_cache[cache_key]

        if not branch_id:
            branch_id = await self.get_default_branch_id(workspace_id)
            if not branch_id:
                return None

        try:
            request = DescribeAPIKeysRequest(
                workspace_id=workspace_id,
                branch_id=branch_id
            )
            response = self.client.describe_api_keys(request)

            if hasattr(response, 'api_keys') and response.api_keys:
                type_mapping = {
                    "service_role": "Service",
                    "anon": "Public"
                }
                target_type = type_mapping.get(key_type, "Service")

                for key in response.api_keys:
                    if hasattr(key, 'type') and key.type == target_type:
                        result = key.key if hasattr(key, 'key') else None
                        if result:
                            api_key_cache[cache_key] = result
                        return result

            return None
        except Exception as e:
            logger.error(f"Error getting API key: {e}")
            return None
