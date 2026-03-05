import httpx
import logging
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class SupabaseClient:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client with connection pooling"""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
            )
        return self._client

    async def close(self):
        """Close HTTP client"""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def call_api(
        self,
        path: str,
        method: str = "GET",
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        content: Optional[bytes] = None,
        timeout: float = 30.0
    ) -> Any:
        url = f"{self.endpoint}{path}"
        
        logger.info(f"[DEBUG] Calling API: method={method}, url={url}, path={path}")

        default_headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
        }
        if headers:
            default_headers.update(headers)

        client = await self._get_client()
        try:
            if content:
                response = await client.request(
                    method, url, content=content, headers=default_headers,
                    params=params, timeout=timeout
                )
            else:
                response = await client.request(
                    method, url, json=json_data, headers=default_headers,
                    params=params, timeout=timeout
                )
            response.raise_for_status()

            if response.status_code == 204 or not response.content:
                return {"success": True}

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return response.json()
            return {"raw": response.text}
        except httpx.HTTPStatusError as e:
            response = e.response
            payload: Any
            try:
                payload = response.json()
            except Exception:
                payload = response.text
            error_message = json.dumps(
                {
                    "status_code": response.status_code,
                    "path": path,
                    "endpoint": self.endpoint,
                    "error": payload,
                },
                ensure_ascii=False,
            )
            raise Exception(error_message) from e
        except Exception as e:
            error_details = f"{str(e)}"
            if hasattr(e, '__cause__') and e.__cause__:
                error_details += f" | Cause: {str(e.__cause__)}"
            raise Exception(f"{error_details} [endpoint: {self.endpoint}, path: {path}]") from e
