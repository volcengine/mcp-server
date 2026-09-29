import argparse
import logging
import os
from typing import Annotated, Any, Dict, Literal, Optional

import aiohttp
from mcp.server import MCPServer
from mcp.server.caching import CacheHint
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import CallToolResult, ResourceLink, TextContent, ToolAnnotations
from pydantic import BaseModel, Field, StringConstraints, ValidationError

from mcp_server_knowledgebase.common.auth import prepare_request
from mcp_server_knowledgebase.config import config
from mcp_server_knowledgebase.models import (
    AddDocumentResult,
    CollectionInfoResult,
    DocFilter,
    DocumentInfo,
    ListCollectionsResult,
    ListDocumentsResult,
    NonBlank,
    SearchKnowledgeResult,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# knowledge base domain
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

# paths
search_knowledge_path = "/api/knowledge/collection/search_knowledge"
list_collections_path = "/api/knowledge/collection/list"
get_collections_path = "/api/knowledge/collection/info"
doc_add_path = "/api/knowledge/doc/add"
doc_info_path = "/api/knowledge/doc/info"
list_docs_path = "/api/knowledge/doc/v2/list"

# Create MCP server
mcp = MCPServer(
    "Knowledgebase MCP Server",
    version="0.2.1",
    cache_hints={"tools/list": CacheHint(ttl_ms=300_000, scope="public")},
)


def result_model(model: type[BaseModel], data: Any) -> BaseModel:
    """Use declared fields and default Pydantic validation for upstream results."""
    try:
        return model.model_validate(data)
    except ValidationError:
        # Validation errors contain upstream values; don't expose them verbatim.
        raise ToolError("Invalid upstream response structure for " + model.__name__) from None


def _safe_error(message: object) -> str:
    text = str(message)
    for secret in (config.ak, config.sk, config.api_key):
        if secret and secret in text:
            return "Knowledge Base request failed (sensitive details omitted)"
    return text


def _transport_options(transport: str) -> Dict[str, Any]:
    """Build transport-specific options accepted by MCP SDK v2."""
    if transport == "stdio":
        return {}
    if transport != "streamable-http":
        raise ValueError(f"Unsupported transport: {transport}")
    return {
        "host": os.getenv("MCP_SERVER_HOST", "127.0.0.1"),
        "port": int(os.getenv("MCP_SERVER_PORT") or os.getenv("PORT", "8000")),
        "streamable_http_path": os.getenv("STREAMABLE_HTTP_PATH", "/mcp"),
        "stateless_http": True,
        "json_response": True,
    }


async def _request_knowledgebase(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Send one signed request without blocking the MCP event loop."""
    request = prepare_request(
        method="POST",
        path=path,
        ak=config.ak,
        sk=config.sk,
        api_key=config.api_key,
        data=data,
    )
    timeout = aiohttp.ClientTimeout(total=float(os.getenv("KNOWLEDGE_BASE_TIMEOUT", "30")))
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.request(
            method=request.method,
            url=f"https://{g_knowledge_base_domain}{request.path}",
            headers=request.headers,
            data=request.body,
        ) as response:
            response.raise_for_status()
            return await response.json()


async def _call_kb(path: str, params: Dict[str, Any], tool_name: str) -> Any:
    """Call a Knowledge Base API and return its non-empty response data."""
    try:
        result = await _request_knowledgebase(path, params)
        if result["code"] != 0:
            raise ToolError(_safe_error(result.get("message", "Knowledge Base request failed")))

        data = result.get("data")
        if not data:
            raise ToolError(f"{tool_name} returned no data")

        return data
    except ToolError as e:
        logger.error("Error in %s: %s", tool_name, _safe_error(str(e)))
        raise
    except Exception as e:
        logger.error("Error in %s: %s", tool_name, type(e).__name__)
        detail = "upstream timed out" if isinstance(e, TimeoutError) else "upstream request failed"
        raise ToolError(f"{tool_name}: {detail} ({type(e).__name__})") from None


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=True,
    )
)
async def add_doc(
    collection_name: Annotated[str, Field(min_length=1, description="Target collection name in the configured project.")],
    add_type: Annotated[Literal["url"], Field(description="Document import method; use url.")],
    doc_id: Annotated[
        str,
        Field(min_length=1, max_length=128, pattern=r"^[A-Za-z][A-Za-z0-9_]*$", description="Unique document ID, 1–128 letters, digits or underscores; must start with a letter."),
    ],
    doc_name: Annotated[str, Field(min_length=1, max_length=256, description="Document name, 1–256 characters.")],
    doc_type: Annotated[Literal[
        "xlsx",
        "csv",
        "jsonl",
        "txt",
        "doc",
        "docx",
        "pdf",
        "markdown",
        "faq.xlsx",
        "pptx",
    ], Field(description="Document format matching the source file.")],
    url: Annotated[str, Field(min_length=1, description="Document URL accessible to Viking for import.")],
) -> AddDocumentResult:
    """Add a document by URL to a collection in the configured project.

    Returns the collection name, document ID and available resource ID from Viking.
    Use get_doc to check the document's processing status after submission.
    """
    request_params = {
        "collection_name": collection_name,
        "project": config.project,
        "add_type": add_type,
        "doc_id": doc_id,
        "doc_name": doc_name,
        "doc_type": doc_type,
        "url": url,
    }

    data = await _call_kb(doc_add_path, request_params, "add_doc")
    return result_model(AddDocumentResult, data)


def _locator(
    collection_name: Optional[str], resource_id: Optional[str], name_key: str
) -> dict[str, str]:
    resource_id = resource_id.strip() if resource_id else ""
    collection_name = collection_name.strip() if collection_name else ""
    if resource_id:
        return {"resource_id": resource_id}
    if collection_name:
        return {name_key: collection_name, "project": config.project}
    raise ToolError("Provide a non-empty collection_name or resource_id")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
async def get_doc(
    collection_name: Optional[str] = Field(default=None, description="Collection name in the configured project. Provide this or resource_id."),
    doc_id: NonBlank = Field(..., description="Document ID to look up; must not be blank."),
    resource_id: Optional[str] = Field(default=None, description="Knowledge base ID. Takes precedence over collection_name when both are provided."),
) -> DocumentInfo:
    """Get document metadata, processing status, summaries and media outlines.

    Provide collection_name or resource_id; the ID takes precedence.

    doc_id is required and trimmed. Project comes from server configuration.
    Unavailable optional fields are null. JSON metadata strings are parsed where possible.
    """
    params = _locator(collection_name, resource_id, "collection_name")
    params["doc_id"] = doc_id
    return result_model(DocumentInfo, await _call_kb(doc_info_path, params, "get_doc"))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
async def list_docs(
    collection_name: Optional[str] = Field(default=None, description="Collection name in the configured project. Provide this or resource_id."),
    limit: Annotated[int, Field(ge=1, le=100, description="Maximum documents per page (1–100); defaults to 50.")] = 50,
    next_token: Optional[str] = Field(default=None, description="Cursor returned by the preceding list_docs call. Omit for the first page."),
    resource_id: Optional[str] = Field(default=None, description="Knowledge base ID. Takes precedence over collection_name when both are provided."),
) -> ListDocumentsResult:
    """List document summaries using cursor pagination (default 50, range 1–100).

    Use collection_name or resource_id; ID takes precedence. Pass next_token
    unchanged from the preceding page. Returns collection_name, total_num, count, has_more, next_token and doc_list
    summaries. total_num is null when unavailable. Name-based requests use the
    configured project.
    """
    params = _locator(collection_name, resource_id, "collection_name")
    params["limit"] = limit
    if next_token is not None:
        params["next_token"] = next_token
    data = await _call_kb(list_docs_path, params, "list_docs")
    return result_model(ListDocumentsResult, data)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
async def get_collection(
    collection_name: Optional[str] = Field(default=None, description="Collection name in the configured project. Provide this or resource_id."),
    resource_id: Optional[str] = Field(default=None, description="Knowledge base ID. Takes precedence over collection_name when both are provided."),
) -> CollectionInfoResult:
    """Get collection metadata and build status.

    Provide collection_name or resource_id; the ID takes precedence. Name-based
    requests use the configured project.

    status is the first pipeline's first index status: -1 pending, 0 building,
    1 ready, 2 failed, 3 changing. Unknown integer states are preserved.
    Returns name, description, status and available ID, counts and timestamps.
    """
    params = _locator(collection_name, resource_id, "name")
    data = await _call_kb(get_collections_path, params, "get_collection")
    try:
        status = data["pipeline_list"][0]["index_list"][0]["status"]
        if status is None:
            raise ValueError("missing status")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ToolError("Invalid upstream response structure: missing first pipeline/index status") from exc
    projected = dict(data, status=status)
    if data.get("doc_num") is None:
        for pipeline in data["pipeline_list"]:
            stat = pipeline.get("pipeline_stat") if isinstance(pipeline, dict) else None
            if isinstance(stat, dict) and stat.get("doc_num") is not None:
                projected["doc_num"] = stat["doc_num"]
                break
    return result_model(CollectionInfoResult, projected)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
async def list_collections() -> ListCollectionsResult:
    """List all collections in the configured project. No input parameters are required.

    Returns collection_list with name, description and available resource ID,
    timestamps, plus the upstream total_num when supplied.
    """
    data = await _call_kb(
        list_collections_path,
        {"project": config.project, "brief": True},
        "list_collections",
    )
    return result_model(ListCollectionsResult, data)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
async def search_knowledge(
    query: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=1, max_length=8000),
        Field(description="Search query, 1–8000 characters after trimming whitespace."),
    ],
    collection_name: Optional[str] = Field(default=None, description="Collection name in the configured project. Provide this or resource_id."),
    limit: Annotated[int, Field(ge=1, le=100, description="Maximum chunks to return (1–100); defaults to 10.")] = 10,
    doc_filter: Optional[DocFilter] = Field(default=None, description="Optional document filter to include or exclude matching field values."),
    resource_id: Optional[str] = Field(default=None, description="Knowledge base ID. Takes precedence over collection_name when both are provided."),
) -> Annotated[CallToolResult, SearchKnowledgeResult]:
    """Search for relevant chunks in a knowledge base by collection name or resource ID.

    Provide collection_name or resource_id; the ID takes precedence. Name-based
    searches use the configured project. doc_filter includes or excludes documents.
    Returns result_list with chunk text, document metadata, scores, media times
    and chunk_attachment metadata (uuid, caption, type). Unavailable optional
    fields are null. Image URLs for image, doc-image and table attachments are
    returned separately as MCP ResourceLink content blocks with uri, name,
    description and mimeType (image/*); chunk_attachment contains no link field.
    """
    params = _locator(collection_name, resource_id, "name")
    params.update(query=query, limit=limit, post_processing={"get_attachment_link": True})
    if doc_filter is not None:
        params["query_param"] = {"doc_filter": doc_filter.model_dump(mode="json")}
    data = await _call_kb(search_knowledge_path, params, "search_knowledge")
    if not isinstance(data, dict) or not isinstance(data.get("result_list"), list):
        raise ToolError("Invalid upstream response structure: expected result_list")
    chunks = []
    for chunk in data["result_list"]:
        if not isinstance(chunk, dict):
            raise ToolError("Invalid upstream response structure: expected a search chunk")
        info = chunk.get("doc_info")
        info = info if isinstance(info, dict) else {}
        item = dict(chunk, doc_id=info.get("doc_id"), doc_name=info.get("doc_name"))
        # Provenance always comes from doc_info, not similarly named chunk fields.
        for name in ("title", "doc_type"):
            item.pop(name, None)
            if name in info:
                item[name] = info[name]
        chunks.append(item)
    result = result_model(SearchKnowledgeResult, {"result_list": chunks})
    content: list[TextContent | ResourceLink] = [
        TextContent(type="text", text=result.model_dump_json())
    ]
    # Process attachments as ResourceLink blocks.
    for chunk in result.result_list:
        for index, attachment in enumerate(chunk.chunk_attachment or []):
            if attachment.type not in {"image", "doc-image", "table"}:
                continue
            if not attachment.link or not attachment.link.strip():
                continue
            # Viking supplies no MIME type; do not guess the image format.
            try:
                content.append(ResourceLink(
                    type="resource_link",
                    uri=attachment.link,
                    name=attachment.uuid or f"{chunk.id}-image-{index + 1}",
                    description=attachment.caption or chunk.chunk_title,
                    mime_type="image/*",
                ))
            except ValidationError:
                raise ToolError("Invalid upstream response structure: invalid image resource link") from None
    return CallToolResult(
        content=content,
        structured_content=result.model_dump(mode="json"),
    )


def main():
    """Main entry point for the Knowledgebase MCP server."""
    parser = argparse.ArgumentParser(description='Run the Viking Knowledgebase MCP Server')
    parser.add_argument(
        "--transport",
        "-t",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport protocol to use (stdio or streamable-http)",
    )
    args = parser.parse_args()
    logger.info(f"Starting Knowledgebase MCP Server with {args.transport} transport")

    try:
        mcp.run(transport=args.transport, **_transport_options(args.transport))
    except Exception as e:
        logger.error(f"Error starting Knowledgebase MCP Server: {str(e)}")
        raise


if __name__ == "__main__":
    main()
