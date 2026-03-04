from typing import Optional, List
import logging
import json
import html
from .base import BaseTools
from ..utils import handle_errors, read_only_check
from ..models import EdgeFunction

logger = logging.getLogger(__name__)

# 运行时配置
RUNTIME_CONFIG = {
    "native-node20/v1": {
        "entrypoint": "index.ts",
        "extensions": [".ts", ".js"],
        "description": "Node.js 20 runtime"
    },
    "native-python3.9/v1": {
        "entrypoint": "app.py",
        "extensions": [".py"],
        "description": "Python 3.9 runtime"
    },
    "native-python3.10/v1": {
        "entrypoint": "app.py",
        "extensions": [".py"],
        "description": "Python 3.10 runtime"
    },
    "native-python3.12/v1": {
        "entrypoint": "app.py",
        "extensions": [".py"],
        "description": "Python 3.12 runtime"
    }
}

# 保留的函数名
RESERVED_SLUGS = {"deploy", "body", "health", "metrics"}
MAX_SLUG_LENGTH = 127
MAX_CODE_SIZE = 10 * 1024 * 1024  # 10MB


class EdgeFunctionTools(BaseTools):
    def _validate_function_name(self, function_name: str) -> None:
        """验证函数名称"""
        if not function_name:
            raise ValueError("Function name cannot be empty")

        if len(function_name) > MAX_SLUG_LENGTH:
            raise ValueError(f"Function name too long (max {MAX_SLUG_LENGTH} characters)")

        if function_name in RESERVED_SLUGS:
            raise ValueError(f"Function name '{function_name}' is reserved")

    def _validate_runtime(self, runtime: str) -> None:
        """验证运行时"""
        if runtime not in RUNTIME_CONFIG:
            available = ", ".join(RUNTIME_CONFIG.keys())
            raise ValueError(f"Unsupported runtime '{runtime}'. Available: {available}")

    def _get_entrypoint(self, runtime: str) -> str:
        """获取运行时的入口文件"""
        return RUNTIME_CONFIG[runtime]["entrypoint"]

    def _validate_code_size(self, source_code: str) -> None:
        """验证代码大小"""
        code_size = len(source_code.encode('utf-8'))
        if code_size > MAX_CODE_SIZE:
            raise ValueError(f"Source code too large: {code_size} bytes (max {MAX_CODE_SIZE} bytes)")

    def _validate_runtime_compatibility(self, runtime: str, source_code: str) -> None:
        """验证运行时和代码的兼容性"""
        if runtime.startswith("native-node"):
            # 检查是否使用了 Deno 特有的 API
            if "Deno." in source_code:
                raise ValueError(
                    f"Code contains Deno-specific APIs (Deno.*) but runtime is {runtime}. "
                    "Please use Node.js compatible code or switch to a Deno runtime."
                )
        elif runtime.startswith("native-python"):
            # 基本的 Python 语法检查
            if not any(keyword in source_code for keyword in ["def ", "import ", "from "]):
                logger.warning("Python code may be invalid - no function definitions or imports found")

    @handle_errors
    async def list_edge_functions(self, workspace_id: Optional[str] = None) -> List[EdgeFunction]:
        ws_id = self._get_workspace_id(workspace_id)
        logger.info(f"Listing edge functions for workspace {ws_id}")

        client = await self._get_client(ws_id)
        # AIDAP 使用不同的 API 路径
        result = await client.call_api("/v1/projects/default/functions")

        functions = [EdgeFunction(**func) for func in result]
        logger.info(f"Found {len(functions)} edge functions")
        return functions
    
    @handle_errors
    async def get_edge_function(self, function_name: str, workspace_id: Optional[str] = None) -> EdgeFunction:
        ws_id = self._get_workspace_id(workspace_id)
        logger.info(f"Getting edge function '{function_name}' from workspace {ws_id}")

        client = await self._get_client(ws_id)
        # AIDAP 使用不同的 API 路径
        result = await client.call_api(f"/v1/projects/default/functions/{function_name}")
        return EdgeFunction(**result)
    
    @handle_errors
    @read_only_check
    async def deploy_edge_function(
        self,
        function_name: str,
        source_code: str,
        verify_jwt: bool = True,
        runtime: str = "native-node20/v1",
        import_map: Optional[str] = None,
        workspace_id: Optional[str] = None
    ) -> dict:
        """
        部署边缘函数

        Args:
            function_name: 函数名称
            source_code: 源代码
            verify_jwt: 是否验证 JWT
            runtime: 运行时环境 (native-node20/v1, native-python3.9/v1, etc.)
            import_map: 可选的 import map JSON
            workspace_id: 工作空间 ID

        Returns:
            部署结果字典

        Raises:
            ValueError: 参数验证失败
        """
        # 验证输入
        self._validate_function_name(function_name)

        if not source_code or not source_code.strip():
            raise ValueError("Source code cannot be empty")

        # HTML 反转义，防止代码中的特殊字符被转义
        source_code = html.unescape(source_code)

        self._validate_code_size(source_code)

        ws_id = self._get_workspace_id(workspace_id)
        # AIDAP 默认使用 Deno 运行时，entrypoint 固定为 index.ts
        entrypoint = "index.ts"

        logger.info(
            "Deploying edge function",
            extra={
                "function_name": function_name,
                "workspace_id": ws_id,
                "runtime": runtime,
                "verify_jwt": verify_jwt,
                "entrypoint": entrypoint,
                "code_size": len(source_code)
            }
        )

        client = await self._get_client(ws_id)

        # AIDAP 使用不同的请求格式和 API 路径
        # URL 编码 function_name 防止特殊字符问题
        from urllib.parse import quote
        encoded_name = quote(function_name)

        data = {
            "metadata": {
                "name": function_name,
                "slug": function_name,
                "entrypoint_path": entrypoint,
                "verify_jwt": verify_jwt
            },
            "files": [
                {
                    "name": entrypoint,
                    "content": source_code
                }
            ]
        }

        if import_map:
            try:
                import_map_data = json.loads(import_map)
                data["metadata"]["import_map_path"] = "import_map.json"
                data["files"].append({
                    "name": "import_map.json",
                    "content": json.dumps(import_map_data)
                })
                logger.debug("Added import map to deployment")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid import map JSON: {e}")

        # AIDAP 部署 API 路径
        result = await client.call_api(
            f"/v1/projects/default/functions/deploy?slug={encoded_name}",
            method="POST",
            json_data=data
        )

        logger.info(
            f"Successfully deployed edge function '{function_name}'",
            extra={"function_id": result.get("id"), "version": result.get("version")}
        )

        return result
    
    @handle_errors
    @read_only_check
    async def delete_edge_function(self, function_name: str, workspace_id: Optional[str] = None) -> dict:
        ws_id = self._get_workspace_id(workspace_id)
        logger.info(f"Deleting edge function '{function_name}' from workspace {ws_id}")

        client = await self._get_client(ws_id)
        # AIDAP 使用不同的 API 路径
        await client.call_api(f"/v1/projects/default/functions/{function_name}", method="DELETE")

        logger.info(f"Successfully deleted edge function '{function_name}'")
        return {"success": True, "message": "Edge function deleted successfully"}
    
    @handle_errors
    async def invoke_edge_function(
        self,
        function_name: str,
        payload: Optional[str] = None,
        method: str = "POST",
        workspace_id: Optional[str] = None
    ) -> dict:
        ws_id = self._get_workspace_id(workspace_id)
        logger.info(
            f"Invoking edge function '{function_name}'",
            extra={"method": method, "has_payload": payload is not None}
        )

        client = await self._get_client(ws_id)

        json_data = None
        if payload:
            try:
                json_data = json.loads(payload)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid payload JSON: {e}")

        # AIDAP 调用 edge function 使用 /functions/v1/{slug} 路径
        result = await client.call_api(
            f"/functions/v1/{function_name}",
            method=method,
            json_data=json_data,
            timeout=60.0
        )

        logger.debug(f"Edge function '{function_name}' invoked successfully")
        return result
