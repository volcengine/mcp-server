import asyncio
import httpx
import logging
import json
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SupabaseApiError(Exception):
    def __init__(self, status_code: int, path: str, endpoint: str, payload: Any):
        self.status_code = status_code
        self.path = path
        self.endpoint = endpoint
        self.payload = payload
        super().__init__(
            json.dumps(
                {
                    "status_code": status_code,
                    "path": path,
                    "endpoint": endpoint,
                    "error": payload,
                },
                ensure_ascii=False,
            )
        )


class SupabaseClient:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

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
        logger.debug("Calling API method=%s url=%s path=%s", method, url, path)

        default_headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
        }
        if headers:
            default_headers.update(headers)

        for attempt in range(3):
            try:
                async with httpx.AsyncClient(
                    timeout=timeout,
                    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
                ) as client:
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
                if response.status_code in {502, 503, 504} and attempt < 2:
                    await asyncio.sleep(0.5 * (attempt + 1))
                    continue
                payload: Any
                try:
                    payload = response.json()
                except Exception:
                    payload = response.text
                raise SupabaseApiError(
                    status_code=response.status_code,
                    path=path,
                    endpoint=self.endpoint,
                    payload=payload,
                ) from e
            except httpx.TransportError as e:
                if attempt < 2:
                    await asyncio.sleep(0.5 * (attempt + 1))
                    continue
                detail = str(e) or type(e).__name__
                raise Exception(f"{detail} [endpoint: {self.endpoint}, path: {path}]") from e
            except Exception as e:
                if isinstance(e, SupabaseApiError):
                    raise
                detail = str(e) or type(e).__name__
                if hasattr(e, "__cause__") and e.__cause__:
                    cause_detail = str(e.__cause__) or type(e.__cause__).__name__
                    detail += f" | Cause: {cause_detail}"
                raise Exception(f"{detail} [endpoint: {self.endpoint}, path: {path}]") from e
