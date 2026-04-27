import logging
import asyncio
import random
from collections.abc import Callable
from typing import Any, Optional
from urllib.parse import urlsplit
from ..config import VOLCENGINE_REGION
from ..credentials import resolve_volcengine_credentials
from ..utils import pick_value

logger = logging.getLogger(__name__)
<<<<<<< main
=======
ENDPOINT_SCHEME_FALLBACK = os.getenv("SUPABASE_ENDPOINT_SCHEME", "http").strip().lower() or "http"
>>>>>>> main

try:
    import volcenginesdkcore
    from volcenginesdkaidap import AIDAPApi
    from volcenginesdkaidap.models import (
        DescribeBranchesRequest,
        DescribeWorkspaceEndpointRequest,
        DescribeAPIKeysRequest,
        BranchRestoreRequest,
        RestoreSettingsForBranchRestoreInput,
        CreateBranchRequest,
        DeleteBranchRequest,
        BranchSettingsForCreateBranchInput,
        CreateWorkspaceRequest,
        WorkspaceSettingsForCreateWorkspaceInput,
        BranchSettingsForCreateWorkspaceInput,
        ComputeSettingsForCreateWorkspaceInput,
        StartWorkspaceRequest,
        StopWorkspaceRequest,
    )
except ImportError:
    logger.error("volcenginesdkaidap client dependencies not installed")
    raise


class AidapClient:
    def __init__(self, context_getter: Callable[[], Any] | None = None) -> None:
        self._context_getter = context_getter

    def _get_credentials(self):
        return resolve_volcengine_credentials(self._context_getter)

    def _create_client(self) -> AIDAPApi:
        credentials = self._get_credentials()
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = credentials.access_key
        configuration.sk = credentials.secret_key
        configuration.region = VOLCENGINE_REGION
        if credentials.session_token:
            configuration.session_token = credentials.session_token
        api_client = volcenginesdkcore.ApiClient(configuration)
        return AIDAPApi(api_client)

    @property
    def client(self) -> AIDAPApi:
        return self._create_client()

    def _branch_error_code(self, error_text: str) -> str:
        if "OperationDenied_BranchNotReady" in error_text:
            return "OperationDenied_BranchNotReady"
        if "BranchStatusNotMatch" in error_text:
            return "BranchStatusNotMatch"
        if "BranchNotFound" in error_text:
            return "BranchNotFound"
        return "AIDAPError"

    def _pick_value(self, source: Any, *field_names: str) -> Any:
        return pick_value(source, *field_names)

<<<<<<< main
    def _normalize_port(self, port: Any) -> Optional[int]:
        if port is None:
            return None
        try:
            return int(port)
        except (TypeError, ValueError):
            logger.warning("Invalid endpoint port from AIDAP: %s", port)
            return None

    def _normalize_scheme(self, scheme: Any) -> Optional[str]:
        if not isinstance(scheme, str):
            return None
        normalized = scheme.strip().lower()
        if normalized in {"http", "https"}:
            return normalized
        return None

    def _scheme_from_port(self, port: Optional[int]) -> str:
        return "https" if port == 443 else "http"

    def _host_has_port(self, host: str) -> bool:
        try:
            return urlsplit(f"//{host}").port is not None
        except ValueError:
            return ":" in host.rsplit("]", 1)[-1]

    def _endpoint_url(self, address: dict[str, Any]) -> str:
        domain = address["domain"]
        parsed_scheme = None
        host = domain.strip().rstrip("/")
        if "://" in host:
            parsed = urlsplit(host)
            parsed_scheme = self._normalize_scheme(parsed.scheme)
            host = parsed.netloc or parsed.path

        port = self._normalize_port(address.get("port"))
        scheme = address.get("scheme") or parsed_scheme or self._scheme_from_port(port)
        if port is not None and not self._host_has_port(host):
            host = f"{host}:{port}"
        return f"{scheme}://{host}"

    def _endpoint_address_payload(self, addr: Any) -> Optional[dict[str, Any]]:
        domain = self._pick_value(addr, "address_domain", "AddressDomain", "domain", "Domain")
        if not domain:
            return None
        return {
            "domain": domain,
            "port": self._pick_value(addr, "address_port", "AddressPort", "port", "Port"),
            "scheme": self._normalize_scheme(
                self._pick_value(
                    addr,
                    "address_scheme",
                    "AddressScheme",
                    "scheme",
                    "Scheme",
                    "protocol",
                    "Protocol",
                )
            ),
            "address_type": self._pick_value(addr, "address_type", "AddressType"),
        }

    def _is_public_address(self, address: dict[str, Any]) -> bool:
        address_type = address.get("address_type")
        if isinstance(address_type, str) and address_type.lower() == "public":
            return True
        domain = address["domain"]
        return "volces.com" in domain and "ivolces.com" not in domain
=======
    def _build_endpoint_from_address(self, address: Any) -> Optional[str]:
        domain = self._pick_value(address, "address_domain", "AddressDomain")
        if not domain:
            return None

        raw_port = self._pick_value(address, "address_port", "AddressPort")
        try:
            port = int(raw_port) if raw_port is not None else None
        except (TypeError, ValueError):
            port = None

        if port == 80:
            scheme = "http"
        elif port == 443:
            scheme = "https"
        else:
            scheme = ENDPOINT_SCHEME_FALLBACK

        if port is None:
            return f"{scheme}://{domain}"
        return f"{scheme}://{domain}:{port}"

    def _endpoint_priority(self, endpoint: Any, address: Any) -> tuple[int, int, int]:
        endpoint_type = str(self._pick_value(endpoint, "endpoint_type", "EndpointType") or "").lower()
        address_type = str(self._pick_value(address, "address_type", "AddressType") or "").lower()
        domain = str(self._pick_value(address, "address_domain", "AddressDomain") or "").lower()

        is_public = address_type == "public" or ("volces.com" in domain and "ivolces.com" not in domain)
        is_dashboard = endpoint_type == "dashboard"
        has_domain = bool(domain)

        return (
            0 if is_public else 1,
            0 if is_dashboard else 1,
            0 if has_domain else 1,
        )
>>>>>>> main

    def _branch_payload(self, branch: Any, fallback_name: Optional[str] = None) -> dict:
        parent_branch = self._pick_value(branch, "parent_branch")
        parent_id = self._pick_value(parent_branch, "branch_id", "parent_id")
        payload = {
            "branch_id": self._pick_value(branch, "branch_id"),
            "name": self._pick_value(branch, "name", "branch_name") or fallback_name,
            "status": self._pick_value(branch, "status", "branch_status"),
            "default": bool(self._pick_value(branch, "default", "is_default") or False),
            "parent_id": parent_id or self._pick_value(branch, "parent_id", "parent_branch_id"),
            "workspace_id": self._pick_value(branch, "workspace_id"),
            "archived": self._pick_value(branch, "archived"),
            "protected": self._pick_value(branch, "protected"),
            "created_at": self._pick_value(branch, "create_time", "created_at"),
            "updated_at": self._pick_value(branch, "update_time", "updated_at"),
        }
        return {key: value for key, value in payload.items() if value is not None}

    async def _find_branch(
        self,
        workspace_id: str,
        branch_id: Optional[str] = None,
        name: Optional[str] = None,
        max_attempts: int = 6,
        ) -> Optional[dict]:
        for attempt in range(1, max_attempts + 1):
            branches = await self.list_branches(workspace_id)
            for branch in branches:
                if branch_id and branch.get("branch_id") == branch_id:
                    return branch
                if name and branch.get("name") == name:
                    return branch
            if attempt < max_attempts:
                await self._sleep_backoff(attempt, base_seconds=0.5, max_seconds=3.0)
        return None

    async def get_branch(self, workspace_id: str, branch_id: str) -> Optional[dict]:
        return await self._find_branch(workspace_id, branch_id=branch_id, max_attempts=1)

    async def _sleep_backoff(
        self,
        attempt: int,
        base_seconds: float = 1.0,
        max_seconds: float = 10.0,
    ) -> None:
        delay = min(max_seconds, base_seconds * (2 ** max(attempt - 1, 0)))
        jitter = random.uniform(0.0, delay * 0.2)
        await asyncio.sleep(delay + jitter)
    
    async def get_default_branch_id(self, workspace_id: str) -> Optional[str]:
        try:
            request = DescribeBranchesRequest(workspace_id=workspace_id)
            response = self.client.describe_branches(request)
            
            if hasattr(response, 'branches') and response.branches:
                for branch in response.branches:
                    if getattr(branch, 'default', False):
                        return branch.branch_id
                
                first_branch = response.branches[0]
                return first_branch.branch_id
            
            return None
        except Exception as e:
            logger.error(f"Error getting default branch: {e}")
            return None
    
    async def list_branches(self, workspace_id: str) -> list[dict]:
        try:
            request = DescribeBranchesRequest(workspace_id=workspace_id)
            response = self.client.describe_branches(request)

            branches = []
            if hasattr(response, 'branches') and response.branches:
                for branch in response.branches:
                    branches.append(self._branch_payload(branch))
            return branches
        except Exception as e:
            logger.error(f"Error listing branches: {e}")
            raise RuntimeError(str(e))

    async def create_branch(self, workspace_id: str, name: str = "develop") -> dict:
        try:
            request = CreateBranchRequest(
                workspace_id=workspace_id,
                branch_settings=BranchSettingsForCreateBranchInput(name=name),
            )
            response = self.client.create_branch(request)

            branch_id = getattr(response, 'branch_id', None)
            if not branch_id and hasattr(response, 'branch'):
                branch_id = getattr(response.branch, 'branch_id', None)

            branch_payload = None
            if branch_id or name:
                try:
                    branch_payload = await self._find_branch(workspace_id, branch_id, name)
                except Exception as lookup_error:
                    logger.warning(f"Error loading created branch details: {lookup_error}")

            result = {
                "success": True,
                "branch_id": branch_id,
                "workspace_id": workspace_id,
                "name": name,
            }
            if branch_payload:
                result.update(branch_payload)
            return result
        except Exception as e:
            logger.error(f"Error creating branch: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def create_workspace(
        self,
        workspace_name: str,
        engine_type: str = "Supabase",
        engine_version: str = "Supabase_1_24",
    ) -> dict:
        try:
            request = CreateWorkspaceRequest(
                workspace_name=workspace_name,
                engine_type=engine_type,
                engine_version=engine_version,
                branch_settings=BranchSettingsForCreateWorkspaceInput(branch_name="main"),
                compute_settings=ComputeSettingsForCreateWorkspaceInput(
                    auto_scaling_limit_min_cu=0.25,
                    auto_scaling_limit_max_cu=1,
                    suspend_timeout_seconds=300
                ),
                workspace_settings=WorkspaceSettingsForCreateWorkspaceInput(
                    public_connection="Disabled",
                    deletion_protection="Disabled"
                ),
            )
            response = self.client.create_workspace(request)

            workspace_id = getattr(response, 'workspace_id', None)
            if not workspace_id and hasattr(response, 'workspace'):
                workspace_id = getattr(response.workspace, 'workspace_id', None)

            return {
                "success": True,
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
                "engine_type": engine_type,
                "engine_version": engine_version,
            }
        except Exception as e:
            logger.error(f"Error creating workspace: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    async def start_workspace(self, workspace_id: str) -> dict:
        try:
            request = StartWorkspaceRequest(workspace_id=workspace_id)
            self.client.start_workspace(request)
            return {"success": True, "workspace_id": workspace_id, "status": "starting"}
        except Exception as e:
            logger.error(f"Error starting workspace: {e}")
            return {"success": False, "error": str(e)}

    async def stop_workspace(self, workspace_id: str) -> dict:
        try:
            request = StopWorkspaceRequest(workspace_id=workspace_id)
            self.client.stop_workspace(request)
            return {"success": True, "workspace_id": workspace_id, "status": "stopping"}
        except Exception as e:
            logger.error(f"Error stopping workspace: {e}")
            return {"success": False, "error": str(e)}

    async def delete_branch(self, workspace_id: str, branch_id: str) -> dict:
        max_attempts = 8
        for attempt in range(1, max_attempts + 1):
            try:
                request = DeleteBranchRequest(
                    workspace_id=workspace_id,
                    branch_id=branch_id,
                )
                self.client.delete_branch(request)
                return {"success": True}
            except Exception as e:
                error_text = str(e)
                code = self._branch_error_code(error_text)
                retriable = code in {"OperationDenied_BranchNotReady", "BranchStatusNotMatch"}
                if retriable and attempt < max_attempts:
                    await self._sleep_backoff(attempt)
                    continue
                logger.error(f"Error deleting branch: {e}")
                return {
                    "success": False,
                    "error": error_text,
                    "code": code,
                    "retriable": retriable,
                }
        return {
            "success": False,
            "error": "delete_branch failed after retries",
            "code": "OperationDenied_BranchNotReady",
            "retriable": True,
        }

    async def get_endpoint(self, workspace_id: str, branch_id: Optional[str] = None) -> Optional[str]:
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
<<<<<<< main
                addresses = []
                for endpoint in response.endpoints:
                    if hasattr(endpoint, 'addresses') and endpoint.addresses:
                        for addr in endpoint.addresses:
                            address = self._endpoint_address_payload(addr)
                            if address:
                                addresses.append(address)

                for address in addresses:
                    if self._is_public_address(address):
                        return self._endpoint_url(address)

                if addresses:
                    return self._endpoint_url(addresses[0])
=======
                candidates: list[tuple[tuple[int, int, int], str]] = []
                for endpoint in response.endpoints:
                    if hasattr(endpoint, 'addresses') and endpoint.addresses:
                        for addr in endpoint.addresses:
                            resolved_endpoint = self._build_endpoint_from_address(addr)
                            if not resolved_endpoint:
                                continue
                            candidates.append((self._endpoint_priority(endpoint, addr), resolved_endpoint))

                if candidates:
                    candidates.sort(key=lambda item: item[0])
                    return candidates[0][1]
>>>>>>> main

            return None
        except Exception as e:
            logger.error(f"Error getting endpoint: {e}")
            return None
    
    async def restore_branch(
        self,
        workspace_id: str,
        branch_id: str,
        source_branch_id: Optional[str] = None,
        time: Optional[str] = None,
    ) -> dict:
        max_attempts = 8
        for attempt in range(1, max_attempts + 1):
            try:
                request = BranchRestoreRequest(
                    workspace_id=workspace_id,
                    branch_id=branch_id,
                    restore_settings=RestoreSettingsForBranchRestoreInput(
                        source_branch_id=source_branch_id or branch_id,
                        time=time,
                    ),
                )
                response = self.client.branch_restore(request)
                return {
                    "success": True,
                    "workspace_id": workspace_id,
                    "branch_id": branch_id,
                    "source_branch_id": source_branch_id or branch_id,
                    "time": time,
                    "backup_branch_id": self._pick_value(response, "backup_branch_id", "BackupBranchID"),
                }
            except Exception as e:
                error_text = str(e)
                code = self._branch_error_code(error_text)
                retriable = code in {"OperationDenied_BranchNotReady", "BranchStatusNotMatch"}
                if retriable and attempt < max_attempts:
                    await self._sleep_backoff(attempt)
                    continue
                logger.error(f"Error restoring branch: {e}")
                return {
                    "success": False,
                    "error": error_text,
                    "code": code,
                    "retriable": retriable,
                }
        return {
            "success": False,
            "error": "restore_branch failed after retries",
            "code": "OperationDenied_BranchNotReady",
            "retriable": True,
        }

    async def get_api_key(self, workspace_id: str, key_type: str = "service_role",
                         branch_id: Optional[str] = None) -> Optional[str]:
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
                        return key.key if hasattr(key, 'key') else None

            return None
        except Exception as e:
            logger.error(f"Error getting API key: {e}")
            return None

    async def get_api_keys(
        self,
        workspace_id: str,
        branch_id: Optional[str] = None,
        use_default_branch: bool = False,
    ) -> list[dict]:
        if use_default_branch and not branch_id:
            branch_id = await self.get_default_branch_id(workspace_id)
            if not branch_id:
                raise RuntimeError(f"Could not get default branch for workspace {workspace_id}")

        request_kwargs = {"workspace_id": workspace_id}
        if branch_id:
            request_kwargs["branch_id"] = branch_id

        request = DescribeAPIKeysRequest(**request_kwargs)
        response = self.client.describe_api_keys(request)

        keys = []
        if hasattr(response, 'api_keys') and response.api_keys:
            for key in response.api_keys:
                keys.append({
                    "type": getattr(key, "type", None),
                    "key": getattr(key, "key", None),
                    "description": getattr(key, "description", None),
                })
        return keys
