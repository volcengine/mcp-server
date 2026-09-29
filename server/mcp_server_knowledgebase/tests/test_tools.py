import asyncio
import json
import logging
import os
from typing import Any

import pytest
from mcp.server.mcpserver.exceptions import ToolError

os.environ["VIKING_API_KEY"] = "test-api-key"
os.environ["KNOWLEDGE_BASE_PROJECT"] = "default"

from mcp_server_knowledgebase import server


def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = asyncio.run(server.mcp.call_tool(name, arguments))
    assert result.is_error is False
    assert result.structured_content is not None
    return result.structured_content


def empty_list_response(**overrides: Any) -> dict[str, Any]:
    data = {
        "collection_name": "product-docs",
        "total_num": 0,
        "count": 0,
        "doc_list": [],
        "has_more": False,
        "next_token": None,
    }
    data.update(overrides)
    return {"code": 0, "message": "success", "data": data}


def test_list_docs_first_page_omits_next_token(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[tuple[str, dict[str, Any]]] = []

    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        requests.append((path, params))
        return empty_list_response()

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    result = call_tool("list_docs", {"collection_name": "product-docs"})

    assert requests == [
        (
            "/api/knowledge/doc/v2/list",
            {
                "collection_name": "product-docs",
                "project": "default",
                "limit": 50,
            },
        )
    ]
    assert result["count"] == 0


def test_list_docs_next_page_sends_and_returns_cursor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[tuple[str, dict[str, Any]]] = []

    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        requests.append((path, params))
        return empty_list_response(has_more=True, next_token="page-3")

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    result = call_tool(
        "list_docs",
        {"collection_name": "product-docs", "limit": 25, "next_token": "page-2"},
    )

    assert requests[0][1]["next_token"] == "page-2"
    assert requests[0][1]["limit"] == 25
    assert result["has_more"] is True
    assert result["next_token"] == "page-3"


@pytest.mark.parametrize("limit", [1, 100])
def test_list_docs_accepts_limit_boundaries(
    monkeypatch: pytest.MonkeyPatch, limit: int
) -> None:
    received_limit: int | None = None

    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        nonlocal received_limit
        received_limit = params["limit"]
        return empty_list_response()

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    call_tool("list_docs", {"collection_name": "product-docs", "limit": limit})

    assert received_limit == limit


@pytest.mark.parametrize(
    ("response", "expected_message"),
    [
        (
            {"code": 1001, "message": "permission denied", "data": None},
            "permission denied",
        ),
        ({"code": 0, "message": "success", "data": None}, "returned no data"),
    ],
)
def test_list_docs_reports_invalid_upstream_responses(
    monkeypatch: pytest.MonkeyPatch,
    response: dict[str, Any],
    expected_message: str,
) -> None:
    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        return response

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    with pytest.raises(ToolError, match=expected_message):
        asyncio.run(
            server.mcp.call_tool("list_docs", {"collection_name": "product-docs"})
        )


def test_list_docs_wraps_transport_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        raise TimeoutError("upstream timed out")

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    with pytest.raises(ToolError, match="upstream timed out"):
        asyncio.run(
            server.mcp.call_tool("list_docs", {"collection_name": "product-docs"})
        )


def test_list_docs_preserves_whitelisted_optional_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        return empty_list_response(
            total_num=None,
            count=1,
            doc_list=[
                {
                    "collection_name": "product-docs",
                    "doc_id": "guide-1",
                    "doc_name": "Product Guide",
                    "doc_type": "pdf",
                    "url": "https://example.com/guide.pdf",
                    "add_type": "url",
                    "create_time": 1788220800,
                    "update_time": 1788220860,
                    "point_num": 53,
                    "status": {"process_status": 1, "failed_code": 7001},
                    "brief_summary": "A short guide.",
                    "total_tokens": 345,
                }
            ],
        )

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    result = call_tool("list_docs", {"collection_name": "product-docs"})
    document = result["doc_list"][0]

    assert result["total_num"] is None
    assert document["status"]["failed_code"] == 7001
    assert document["brief_summary"] == "A short guide."
    assert "total_tokens" not in document
    assert "url" not in document
    assert "add_type" not in document


def test_get_doc_accepts_numeric_failed_code_and_preserves_summary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requests: list[tuple[str, dict[str, Any]]] = []

    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        requests.append((path, params))
        return {
            "code": 0,
            "message": "success",
            "data": {
                "collection_name": "product-docs",
                "doc_id": "guide-1",
                "status": {"process_status": 1, "failed_code": 7001},
                "brief_summary": "A short guide.",
            },
        }

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    result = call_tool(
        "get_doc", {"collection_name": "product-docs", "doc_id": "guide-1"}
    )

    assert requests == [
        (
            "/api/knowledge/doc/info",
            {
                "collection_name": "product-docs",
                "project": "default",
                "doc_id": "guide-1",
            },
        )
    ]
    assert result["status"]["failed_code"] == 7001
    assert result["brief_summary"] == "A short guide."


def test_get_collection_logs_errors_under_its_own_name(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        return {"code": 1001, "message": "permission denied", "data": None}

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)

    with caplog.at_level(logging.ERROR, logger=server.__name__):
        with pytest.raises(ToolError, match="permission denied"):
            asyncio.run(
                server.mcp.call_tool(
                    "get_collection", {"collection_name": "product-docs"}
                )
            )

    assert "Error in get_collection: permission denied" in caplog.text
    assert "Error in search_knowledge" not in caplog.text


def test_search_returns_image_resource_links(monkeypatch: pytest.MonkeyPatch) -> None:
    attachments = [
        {"uuid": kind, "type": kind, "link": f"https://example.com/{kind}.png?signature=original"}
        for kind in ("image", "doc-image", "table")
    ]
    attachments.extend([
        {"type": "image"},
        {"type": "table", "link": " "},
        {"type": "video", "link": "https://example.com/video.mp4"},
    ])
    requests = []

    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        requests.append(params)
        return {"code": 0, "data": {"result_list": [{
            "id": "chunk-1", "content": "Chart description",
            "doc_info": {"doc_id": "doc-1", "doc_name": "Guide"},
            "chunk_attachment": attachments,
        }]}}

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)
    doc_filter = {"op": "must", "field": "doc_id", "conds": ["doc-1"]}
    result = asyncio.run(server.mcp.call_tool("search_knowledge", {
        "resource_id": "kb-1", "collection_name": "ignored", "query": "chart",
        "doc_filter": doc_filter,
    }))

    assert requests == [{
        "resource_id": "kb-1", "query": "chart", "limit": 10,
        "query_param": {"doc_filter": doc_filter},
        "post_processing": {"get_attachment_link": True},
    }]
    assert not result.is_error
    assert [block.type for block in result.content] == ["text"] + ["resource_link"] * 3
    assert [str(block.uri) for block in result.content[1:]] == [
        attachment["link"] for attachment in attachments[:3]
    ]
    assert all(block.mime_type == "image/*" for block in result.content[1:])
    assert result.structured_content is None
    chunk = json.loads(result.content[0].text)["result_list"][0]
    assert chunk["doc_id"] == "doc-1" and chunk["doc_name"] == "Guide"
    assert "doc_info" not in chunk
    assert all("link" not in attachment for attachment in chunk["chunk_attachment"])


def test_add_doc_returns_actual_response_without_project(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fake_request(path: str, params: dict[str, Any]) -> dict[str, Any]:
        return {"code": 0, "data": {
            "collection_name": "actual-name", "doc_id": "actual-doc",
            "resource_id": "kb-1", "project": "default",
        }}

    monkeypatch.setattr(server, "_request_knowledgebase", fake_request)
    result = call_tool("add_doc", {
        "collection_name": "requested-name", "doc_id": "requested_doc",
        "doc_name": "Guide", "doc_type": "pdf", "add_type": "url",
        "url": "https://example.com/guide.pdf",
    })
    assert result == {
        "collection_name": "actual-name", "doc_id": "actual-doc", "resource_id": "kb-1",
    }
