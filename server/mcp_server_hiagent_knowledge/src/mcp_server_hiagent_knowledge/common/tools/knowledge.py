"""HiAgent Knowledge Engine OpenAPI tools.

The HiAgent OpenAPI exposes knowledge-engine capabilities through a single
``CallKnowledgeEngineTool`` action whose ``ToolName`` field selects a sub-tool
and whose request carries a same-named PascalCase parameter object (e.g.
``KnowledgeSearch``, ``GrepChunks``).

This module maps each ``(ToolName, parameter-object)`` combination to a
**separate MCP tool named after the user-facing capability**, with a flat
argument schema; the handler assembles the request body with field names kept
strictly identical to the OpenAPI contract.

Capability tool  -> ToolName            -> parameter object
  search_knowledge      -> knowledge_search      -> KnowledgeSearch
  grep_knowledge_chunks -> grep_chunks           -> GrepChunks
  list_document_infos   -> list_doc_infos         -> ListDocInfos
  list_document_chunks  -> list_knowledge_chunks -> ListKnowledgeChunks
  search_wiki           -> wiki_search           -> WikiSearch
  read_wiki_page        -> wiki_read_page        -> WikiReadPage
  read_wiki_source_chunk -> wiki_read_source_chunk -> WikiReadSourceChunk
  read_wiki_source_doc  -> list_knowledge_chunks -> ListKnowledgeChunks

The two Wiki source read-back capabilities are complementary:
``read_wiki_source_chunk`` resolves a Wiki page's referenced chunks by ``slug``
(wiki_read_source_chunk), while ``read_wiki_source_doc`` reads one referenced
source document's chunks in order by ``resource_id`` (dispatched through
list_knowledge_chunks).

Every sub-tool also accepts an optional ``user_info`` (the OpenAPI ``UserInfo``
end-user identity, ``{"UserID": ..., "UserChannel": ...}``) forwarded verbatim.
The backend applies knowledge-base / document-level permission filtering to it
only when ``UserChannel`` is ``"IAM"`` (or a ``"Lark"`` identity it can map to an
IAM user) and ``UserID`` is a real user in the tenant; other channels are treated
as guest. Pass it to make retrieval honor an end user's own access rights.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from fastmcp import FastMCP

from mcp_server_hiagent_knowledge.common.tools._common import (
    OPENAPI_SERVICE,
    OPENAPI_VERSION,
    OpenAPIClient,
)


# The OpenAPI action every knowledge-engine capability dispatches through by
# default: the platform entry, which also validates runtime context.
KNOWLEDGE_ENGINE_ACTION = "CallKnowledgeEngineTool"

# The user-scoped entry for standalone AK/SK callers. Request body and wire
# version are identical; only authorization differs — it uses the caller's own
# knowledge-base ACL instead of a platform session.
KNOWLEDGE_USER_ACTION = "CallKnowledgeTool"

# MCP tool names registered by ``register_knowledge_tools`` (single source of
# truth for tool-scope filtering). Distinct from ``KNOWN_TOOL_NAMES`` below,
# which are the raw OpenAPI ``ToolName`` values these capabilities dispatch to.
KNOWLEDGE_TOOL_NAMES = (
    "search_knowledge",
    "grep_knowledge_chunks",
    "list_document_infos",
    "list_document_chunks",
    "search_wiki",
    "read_wiki_page",
    "read_wiki_source_chunk",
    "read_wiki_source_doc",
)

# All v3.1.0/v3.2.1 knowledge-engine sub-tools, keyed by OpenAPI ``ToolName``.
KNOWN_TOOL_NAMES = (
    "knowledge_search",
    "grep_chunks",
    "list_doc_infos",
    "list_knowledge_chunks",
    "wiki_search",
    "wiki_read_page",
    "wiki_read_source_chunk",
)

# v3.3.0 adds the dedicated ``wiki_read_source_doc`` sub-tool.
KNOWN_TOOL_NAMES_V330 = (
    *KNOWN_TOOL_NAMES,
    "wiki_read_source_doc",
)


class _ActionScopedClient:
    """Forward capability calls through one fixed OpenAPI action."""

    def __init__(self, client: OpenAPIClient, action: str) -> None:
        self._client = client
        self._action = action

    def call(self, **kwargs: object) -> dict[str, object]:
        kwargs["action"] = self._action
        return self._client.call(**kwargs)


def _call_knowledge_engine(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    tool_name: str,
    parameter_field: str | None = None,
    parameter_object: dict[str, object] | None = None,
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
    known_tool_names: tuple[str, ...] = KNOWN_TOOL_NAMES,
) -> dict[str, object]:
    """Assemble and send a knowledge-engine tool request.

    Shared by every capability handler. ``parameter_object`` is placed under the
    PascalCase ``parameter_field`` (e.g. ``KnowledgeSearch``); callers pass the
    already-built object so field names stay strictly aligned with the OpenAPI
    contract. ``user_info`` is forwarded verbatim as the top-level ``UserInfo``
    end-user identity when provided.

    Argument *values* are not validated here: field ranges, enums and
    cross-field rules are the backend service's responsibility and are
    version-specific, so the server's ``InvalidParameter.*`` errors are passed
    through to the caller rather than duplicated locally.
    """

    if require_workspace and not workspace_id:
        raise ValueError("workspace_id is required")
    if not dataset_ids:
        raise ValueError("dataset_ids must contain at least one dataset id")
    if tool_name not in known_tool_names:
        raise ValueError(
            f"unknown tool_name {tool_name!r}; known tools: {known_tool_names}"
        )

    body: dict[str, object] = {
        "DatasetIDs": list(dataset_ids),
        "ToolName": tool_name,
    }
    if require_workspace:
        body["WorkspaceID"] = workspace_id
    elif workspace_id is not None and workspace_id.strip():
        body["WorkspaceID"] = workspace_id
    if parameter_field is not None and parameter_object is not None:
        body[parameter_field] = parameter_object
    if user_info:
        body["UserInfo"] = dict(user_info)

    return client.call(
        action=KNOWLEDGE_ENGINE_ACTION,
        version=OPENAPI_VERSION,
        service=OPENAPI_SERVICE,
        body=body,
    )


# --- capability handlers ----------------------------------------------------

def search_knowledge(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    queries: Sequence[str],
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
) -> dict[str, object]:
    """Semantic knowledge retrieval (knowledge_search)."""

    if not queries:
        raise ValueError("queries must contain at least one query")

    search: dict[str, object] = {"Queries": list(queries)}

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="knowledge_search",
        parameter_field="KnowledgeSearch",
        parameter_object=search,
        user_info=user_info,
        require_workspace=require_workspace,
    )


def grep_knowledge_chunks(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    pattern: str,
    queries: Sequence[str] | None = None,
    limit: int | None = None,
    grep_type: str | None = None,
    resource_ids: Sequence[str] | None = None,
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
) -> dict[str, object]:
    """Match knowledge chunks by RE2 regex (grep_chunks)."""

    if not pattern:
        raise ValueError("pattern is required")

    grep: dict[str, object] = {"Pattern": pattern}
    if queries:
        grep["Queries"] = list(queries)
    if limit is not None:
        grep["Limit"] = limit
    if grep_type:
        grep["GrepType"] = grep_type
    if resource_ids:
        grep["ResourceIDs"] = list(resource_ids)

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="grep_chunks",
        parameter_field="GrepChunks",
        parameter_object=grep,
        user_info=user_info,
        require_workspace=require_workspace,
    )


def list_document_infos(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    resource_ids: Mapping[str, Sequence[str]],
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
) -> dict[str, object]:
    """Read metadata for documents, batched by dataset (list_doc_infos)."""

    if not resource_ids:
        raise ValueError("resource_ids must contain at least one dataset entry")
    normalized: dict[str, list[str]] = {}
    for dataset_id, ids in resource_ids.items():
        if not dataset_id:
            raise ValueError("resource_ids keys (dataset ids) must be non-empty")
        id_list = list(ids)
        if not id_list:
            raise ValueError(
                f"resource_ids[{dataset_id!r}] must contain at least one resource id"
            )
        normalized[dataset_id] = id_list

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="list_doc_infos",
        parameter_field="ListDocInfos",
        parameter_object={"ResourceIDs": normalized},
        user_info=user_info,
        require_workspace=require_workspace,
    )


def list_document_chunks(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    resource_id: str,
    limit: int | None = None,
    cursor_segment_id: str | None = None,
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
) -> dict[str, object]:
    """List one document's chunks in reading order (list_knowledge_chunks)."""

    if not resource_id:
        raise ValueError("resource_id is required")

    chunks: dict[str, object] = {"ResourceID": resource_id}
    if limit is not None:
        chunks["Limit"] = limit
    if cursor_segment_id:
        chunks["CursorSegmentID"] = cursor_segment_id

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="list_knowledge_chunks",
        parameter_field="ListKnowledgeChunks",
        parameter_object=chunks,
        user_info=user_info,
        require_workspace=require_workspace,
    )


def search_wiki(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    queries: Sequence[str],
    limit: int | None = None,
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
) -> dict[str, object]:
    """Search generated Wiki pages (wiki_search)."""

    if not queries:
        raise ValueError("queries must contain at least one query")

    wiki: dict[str, object] = {"Queries": list(queries)}
    if limit is not None:
        wiki["Limit"] = limit

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="wiki_search",
        parameter_field="WikiSearch",
        parameter_object=wiki,
        user_info=user_info,
        require_workspace=require_workspace,
    )


def read_wiki_page(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    slug: str,
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
) -> dict[str, object]:
    """Read one generated Wiki page by slug (wiki_read_page)."""

    if not slug:
        raise ValueError("slug is required")

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="wiki_read_page",
        parameter_field="WikiReadPage",
        parameter_object={"Slug": slug},
        user_info=user_info,
        require_workspace=require_workspace,
    )


def read_wiki_source_chunk(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    slug: str,
    limit: int | None = None,
    overlap: int | None = None,
    cursor_segment_id: str | None = None,
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
) -> dict[str, object]:
    """Read a Wiki page's referenced source chunks, resolved by page slug
    (wiki_read_source_chunk).
    """

    if not slug:
        raise ValueError("slug is required")

    src: dict[str, object] = {"Slug": slug}
    if limit is not None:
        src["Limit"] = limit
    if overlap is not None:
        src["Overlap"] = overlap
    if cursor_segment_id:
        src["CursorSegmentID"] = cursor_segment_id

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="wiki_read_source_chunk",
        parameter_field="WikiReadSourceChunk",
        parameter_object=src,
        user_info=user_info,
        require_workspace=require_workspace,
    )


def read_wiki_source_doc(
    client: OpenAPIClient,
    *,
    workspace_id: str | None = None,
    dataset_ids: Sequence[str],
    resource_id: str,
    limit: int | None = None,
    cursor_segment_id: str | None = None,
    user_info: Mapping[str, object] | None = None,
    require_workspace: bool = True,
    use_wiki_source_doc_tool: bool = False,
) -> dict[str, object]:
    """Read one Wiki source document's chunks in order, by resource id.

    In v3.1.0 / v3.2.1 (``use_wiki_source_doc_tool=False``) this dispatches
    through ``list_knowledge_chunks``. In v3.3.0 (``use_wiki_source_doc_tool=True``)
    this dispatches through the dedicated ``wiki_read_source_doc`` sub-tool
    with the ``WikiReadSourceDoc`` argument object.
    """

    if not use_wiki_source_doc_tool:
        return list_document_chunks(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            resource_id=resource_id,
            limit=limit,
            cursor_segment_id=cursor_segment_id,
            user_info=user_info,
            require_workspace=require_workspace,
        )

    if not resource_id:
        raise ValueError("resource_id is required")

    doc: dict[str, object] = {"ResourceID": resource_id}
    if limit is not None:
        doc["Limit"] = limit
    if cursor_segment_id:
        doc["CursorSegmentID"] = cursor_segment_id

    return _call_knowledge_engine(
        client,
        workspace_id=workspace_id,
        dataset_ids=dataset_ids,
        tool_name="wiki_read_source_doc",
        parameter_field="WikiReadSourceDoc",
        parameter_object=doc,
        user_info=user_info,
        require_workspace=require_workspace,
        known_tool_names=KNOWN_TOOL_NAMES_V330,
    )


def _register_user_scoped_knowledge_tools(
    mcp: FastMCP,
    client: OpenAPIClient,
    *,
    use_wiki_source_doc_tool: bool,
) -> None:
    """Register v3.3.0 standalone knowledge tools (CallKnowledgeTool).

    Differences from the v3.1.0/v3.2.1 platform contract:
    - ``workspace_id`` is optional: omit or leave blank to authorize against the
      caller's visible datasets across joined workspaces and legacy personal space.
    - ``user_info`` is optional and, when provided, must name the TOP-authenticated
      IAM user itself (``{"UserID": "<caller>", "UserChannel": "IAM"}``); other
      identities or channels (e.g. Lark) are rejected with 403 by the backend.
    - ``read_wiki_source_doc`` dispatches through ``wiki_read_source_doc`` /
      ``WikiReadSourceDoc`` when ``use_wiki_source_doc_tool`` is enabled.
    """

    @mcp.tool(name="search_knowledge")
    def search_knowledge_tool(
        dataset_ids: list[str],
        queries: list[str],
        workspace_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Semantic retrieval for concepts, explanations, overviews and
        paraphrased questions. Returns candidate chunk segments for navigation;
        deep-read the original text via ``list_document_chunks`` before answering
        with facts.

        Discover dataset ids with ``list_datasets``. Often paired with
        ``grep_knowledge_chunks`` (exact anchoring) to widen recall.

        Parameters:
        - dataset_ids: dataset ids to search, at least one.
        - queries: 1-5 short, independent natural-language questions or concept
          phrases; don't pass raw dialogue or long paragraphs.
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"}.
          Under CallKnowledgeTool it may only name the authenticated IAM user
          itself; omitting uses the credential identity, and other users or
          channels (such as Lark) are rejected with 403.
        """

        return search_knowledge(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            queries=queries,
            user_info=user_info,
            require_workspace=False,
        )

    @mcp.tool(name="grep_knowledge_chunks")
    def grep_knowledge_chunks_tool(
        dataset_ids: list[str],
        pattern: str,
        workspace_id: str | None = None,
        queries: list[str] | None = None,
        limit: int | None = None,
        grep_type: str | None = None,
        resource_ids: list[str] | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Locate exact text with one RE2 regex — best for identifiers, fixed
        phrases, field/API names, version strings or error codes. Narrows
        recalled candidates then applies the pattern; deep-read via
        ``list_document_chunks`` for full context.

        Parameters:
        - dataset_ids: dataset ids to search, at least one.
        - pattern: one RE2 regular expression (use ``|`` to combine; no
          backreferences/lookarounds).
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - queries: optional 1-5 plain-text terms to recall candidates before the
          regex is applied.
        - limit: max number of candidate matches to return.
        - grep_type: scan scope, ``dataset_ids`` (default) or ``resource_ids``.
        - resource_ids: document/resource ids to restrict the scan to; required
          when ``grep_type`` is ``resource_ids``.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"};
          must match the authenticated IAM user itself (other users/channels 403).
        """

        return grep_knowledge_chunks(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            pattern=pattern,
            queries=queries,
            limit=limit,
            grep_type=grep_type,
            resource_ids=resource_ids,
            user_info=user_info,
            require_workspace=False,
        )

    @mcp.tool(name="list_document_infos")
    def list_document_infos_tool(
        dataset_ids: list[str],
        resource_ids: dict[str, list[str]],
        workspace_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read document metadata in batch (title, type, size, status, segment
        count, timestamps). Metadata catalog only — read body text with
        ``list_document_chunks``.

        Parameters:
        - dataset_ids: dataset ids involved, at least one.
        - resource_ids: map of dataset id -> list of document/resource ids to
          describe (keys must be within ``dataset_ids``).
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"};
          must match the authenticated IAM user itself (other users/channels 403).
        """

        return list_document_infos(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            resource_ids=resource_ids,
            user_info=user_info,
            require_workspace=False,
        )

    @mcp.tool(name="list_document_chunks")
    def list_document_chunks_tool(
        dataset_ids: list[str],
        resource_id: str,
        workspace_id: str | None = None,
        limit: int | None = None,
        cursor_segment_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Deep-read one document's original chunks in reading order.

        Parameters:
        - dataset_ids: dataset ids the resource belongs to, at least one.
        - resource_id: the document/resource whose chunks to read.
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - limit: max number of ordered chunks per page.
        - cursor_segment_id: paging cursor; omit on first read and reuse only
          for the same document.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"};
          must match the authenticated IAM user itself (other users/channels 403).
        """

        return list_document_chunks(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            resource_id=resource_id,
            limit=limit,
            cursor_segment_id=cursor_segment_id,
            user_info=user_info,
            require_workspace=False,
        )

    @mcp.tool(name="search_wiki")
    def search_wiki_tool(
        dataset_ids: list[str],
        queries: list[str],
        workspace_id: str | None = None,
        limit: int | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Find entry-point Wiki pages by BM25 keyword match. Returns page
        candidates (with ``Slug``) for navigation only; read a chosen page with
        ``read_wiki_page``.

        Parameters:
        - dataset_ids: dataset ids to search, at least one.
        - queries: 1-5 short keyword queries.
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - limit: max number of Wiki page candidates to return.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"};
          must match the authenticated IAM user itself (other users/channels 403).
        """

        return search_wiki(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            queries=queries,
            limit=limit,
            user_info=user_info,
            require_workspace=False,
        )

    @mcp.tool(name="read_wiki_page")
    def read_wiki_page_tool(
        dataset_ids: list[str],
        slug: str,
        workspace_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read one Wiki page's full content (e.g. from ``search_wiki``,
        related links, or ``index``). Trace to original evidence with
        ``read_wiki_source_chunk`` or ``read_wiki_source_doc``.

        Parameters:
        - dataset_ids: dataset ids the page belongs to, at least one.
        - slug: the Wiki page slug.
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"};
          must match the authenticated IAM user itself (other users/channels 403).
        """

        return read_wiki_page(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            slug=slug,
            user_info=user_info,
            require_workspace=False,
        )

    @mcp.tool(name="read_wiki_source_chunk")
    def read_wiki_source_chunk_tool(
        dataset_ids: list[str],
        slug: str,
        workspace_id: str | None = None,
        limit: int | None = None,
        overlap: int | None = None,
        cursor_segment_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read the source chunks a Wiki page cites, in ``chunk_refs`` order,
        resolved by page ``slug``.

        Parameters:
        - dataset_ids: dataset ids the page belongs to, at least one.
        - slug: the Wiki page slug whose cited chunks to read.
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - limit: max number of cited anchors consumed per page.
        - overlap: neighbouring segments expanded around each anchor (0 = anchor only).
        - cursor_segment_id: paging cursor; omit on first read.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"};
          must match the authenticated IAM user itself (other users/channels 403).
        """

        return read_wiki_source_chunk(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            slug=slug,
            limit=limit,
            overlap=overlap,
            cursor_segment_id=cursor_segment_id,
            user_info=user_info,
            require_workspace=False,
        )

    @mcp.tool(name="read_wiki_source_doc")
    def read_wiki_source_doc_tool(
        dataset_ids: list[str],
        resource_id: str,
        workspace_id: str | None = None,
        limit: int | None = None,
        cursor_segment_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read a whole referenced Wiki source document sequentially by resource id
        (e.g. from a Wiki page's ``SourceRefs``). ``dataset_ids`` must contain
        exactly one dataset id.

        Parameters:
        - dataset_ids: single-element list containing the dataset id the resource
          belongs to.
        - resource_id: the referenced source document/resource id.
        - workspace_id: optional consuming workspace id; omit/blank to authorize
          across the caller's visible datasets.
        - limit: max number of ordered chunks per page (backend default 20, range 1..200).
        - cursor_segment_id: paging cursor; omit on first read.
        - user_info: optional caller identity, {"UserID": ..., "UserChannel": "IAM"};
          must match the authenticated IAM user itself (other users/channels 403).
        """

        return read_wiki_source_doc(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            resource_id=resource_id,
            limit=limit,
            cursor_segment_id=cursor_segment_id,
            user_info=user_info,
            require_workspace=False,
            use_wiki_source_doc_tool=use_wiki_source_doc_tool,
        )


def register_knowledge_tools(
    mcp: FastMCP,
    client: OpenAPIClient,
    *,
    action: str = KNOWLEDGE_ENGINE_ACTION,
    workspace_optional: bool = False,
    use_wiki_source_doc_tool: bool = False,
) -> None:
    """Register the knowledge-engine capability tools on a FastMCP server.

    Each capability of the knowledge-engine action is exposed as a distinct,
    capability-named MCP tool rather than one generic tool keyed by a raw
    OpenAPI ``ToolName``. ``action`` selects the OpenAPI entry: the platform
    action by default, ``CallKnowledgeTool`` for standalone callers whose
    permission subject is the AK/SK identity itself.
    """

    if action != KNOWLEDGE_ENGINE_ACTION:
        client = _ActionScopedClient(client, action)

    if workspace_optional:
        _register_user_scoped_knowledge_tools(
            mcp, client, use_wiki_source_doc_tool=use_wiki_source_doc_tool
        )
        return

    @mcp.tool(name="search_knowledge")
    def search_knowledge_tool(
        workspace_id: str,
        dataset_ids: list[str],
        queries: list[str],
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Semantic retrieval for concepts, explanations, overviews and
        paraphrased questions ("what is" / "why" / "how" / "summary" /
        "comparison"), i.e. when the answer may be worded differently from the
        question. Returns candidate chunk segments for navigation — treat them
        as *where to look*, not as final evidence; before answering with facts
        it's recommended to deep-read the original text via ``list_document_chunks``.

        Discover dataset ids with ``list_datasets``. Often paired with
        ``grep_knowledge_chunks`` (exact anchoring) to widen recall.

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids to search, at least one.
        - queries: 1-5 short, independent natural-language questions or concept
          phrases; don't pass raw dialogue or long paragraphs.
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return search_knowledge(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            queries=queries,
            user_info=user_info,
        )

    @mcp.tool(name="grep_knowledge_chunks")
    def grep_knowledge_chunks_tool(
        workspace_id: str,
        dataset_ids: list[str],
        pattern: str,
        queries: list[str] | None = None,
        limit: int | None = None,
        grep_type: str | None = None,
        resource_ids: list[str] | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Locate exact text with one RE2 regex — best for identifiers, fixed
        phrases, field/API names, version strings or error codes when wording
        matters. Narrows recalled candidates then applies the pattern; it does
        NOT guarantee exhaustive coverage of the whole dataset. Returns candidate
        chunk segments (where to look), not final evidence; before answering
        it's recommended to deep-read via ``list_document_chunks``.

        Tips: pack close variants into ONE alternation like
        ``alias_a|alias_b|alias_c`` instead of repeated calls; when ``pattern``
        contains regex operators, put plain retrievable wording in ``queries`` so
        candidate chunks get recalled first. Often used before ``search_knowledge``
        for entity anchoring.

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids to search, at least one.
        - pattern: one RE2 regular expression (use ``|`` to combine; no
          backreferences/lookarounds).
        - queries: optional 1-5 plain-text terms to recall candidates before the
          regex is applied.
        - limit: max number of candidate matches to return.
        - grep_type: scan scope, ``dataset_ids`` (default) or ``resource_ids``.
        - resource_ids: document/resource ids to restrict the scan to; required
          when ``grep_type`` is ``resource_ids``.
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return grep_knowledge_chunks(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            pattern=pattern,
            queries=queries,
            limit=limit,
            grep_type=grep_type,
            resource_ids=resource_ids,
            user_info=user_info,
        )

    @mcp.tool(name="list_document_infos")
    def list_document_infos_tool(
        workspace_id: str,
        dataset_ids: list[str],
        resource_ids: dict[str, list[str]],
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read document metadata in batch (title, type, size, status, segment
        count, timestamps). This is a *catalog* for identifying or comparing
        documents — it is NOT evidence for body facts, rules, figures or
        quotations; read the actual text with ``list_document_chunks`` for that.

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids involved, at least one.
        - resource_ids: map of dataset id -> list of document/resource ids to
          describe (keys must be within ``dataset_ids``), e.g.
          {"dataset-1": ["resource-1", "resource-2"]}. Merge ids of the same
          dataset into one batched call.
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return list_document_infos(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            resource_ids=resource_ids,
            user_info=user_info,
        )

    @mcp.tool(name="list_document_chunks")
    def list_document_chunks_tool(
        workspace_id: str,
        dataset_ids: list[str],
        resource_id: str,
        limit: int | None = None,
        cursor_segment_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Deep-read one document's original chunks in reading order — the
        recommended follow-up after ``search_knowledge`` / ``grep_knowledge_chunks``
        surface a relevant document, whenever the answer depends on full context
        rather than a standalone snippet. Search tools tell you *where*; this
        tells you *what the document actually says*.

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids the resource belongs to, at least one.
        - resource_id: the document/resource whose chunks to read (from a prior
          search/grep result).
        - limit: max number of ordered chunks per page.
        - cursor_segment_id: paging cursor; omit on the first read. Only reuse the
          cursor returned by the immediately previous call **for the same
          document** — don't carry a cursor across documents or tools.
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return list_document_chunks(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            resource_id=resource_id,
            limit=limit,
            cursor_segment_id=cursor_segment_id,
            user_info=user_info,
        )

    @mcp.tool(name="search_wiki")
    def search_wiki_tool(
        workspace_id: str,
        dataset_ids: list[str],
        queries: list[str],
        limit: int | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Find entry-point Wiki pages by BM25 keyword match. Returns page
        candidates (with ``Slug``) for navigation only — results are summaries,
        NOT evidence; you can't answer from search results alone. Read a chosen
        page with ``read_wiki_page`` to get the actual content.

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids to search, at least one.
        - queries: 1-5 short keyword queries; keep distinctive entities, product
          names, abbreviations and precise terms. Put aliases / alternative
          phrasings as separate queries.
        - limit: max number of Wiki page candidates to return.
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return search_wiki(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            queries=queries,
            limit=limit,
            user_info=user_info,
        )

    @mcp.tool(name="read_wiki_page")
    def read_wiki_page_tool(
        workspace_id: str,
        dataset_ids: list[str],
        slug: str,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read one Wiki page's full content — the primary tool for reading Wiki
        material, for pages found via ``search_wiki``, linked from other pages,
        or the special ``index`` page (read ``index`` first for a
        knowledge-base overview). The result also surfaces related pages
        (in/out links) you can follow 1-2 hops to gather context.

        Wiki pages are generated navigation material, not final evidence; for
        precise facts, numbers, rules, quotes or code, trace to originals with
        ``read_wiki_source_chunk`` (by this page's slug) or ``read_wiki_source_doc``
        (by a referenced source document's resource id).

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids the page belongs to, at least one.
        - slug: the Wiki page slug (from ``search_wiki``, a related page, or ``index``).
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return read_wiki_page(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            slug=slug,
            user_info=user_info,
        )

    @mcp.tool(name="read_wiki_source_chunk")
    def read_wiki_source_chunk_tool(
        workspace_id: str,
        dataset_ids: list[str],
        slug: str,
        limit: int | None = None,
        overlap: int | None = None,
        cursor_segment_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read the source chunks a Wiki page cites, in ``chunk_refs`` order,
        resolved by the page ``slug`` — the recommended way to get evidence
        that a specific Wiki page relies on (facts, numbers, quotes, code). Set
        ``overlap`` > 0 to include neighbouring context around each cited chunk.
        To instead read a whole referenced source document sequentially by its
        resource id, use ``read_wiki_source_doc``.

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids the page belongs to, at least one.
        - slug: the Wiki page slug whose cited chunks to read.
        - limit: max number of cited anchors consumed per page (anchors, not
          final returned chunks).
        - overlap: neighbouring segments expanded around each anchor (0 = anchor
          only).
        - cursor_segment_id: paging cursor; omit on first read. Only reuse the
          cursor from the immediately previous call for the same page.
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return read_wiki_source_chunk(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            slug=slug,
            limit=limit,
            overlap=overlap,
            cursor_segment_id=cursor_segment_id,
            user_info=user_info,
        )

    @mcp.tool(name="read_wiki_source_doc")
    def read_wiki_source_doc_tool(
        workspace_id: str,
        dataset_ids: list[str],
        resource_id: str,
        limit: int | None = None,
        cursor_segment_id: str | None = None,
        user_info: dict[str, object] | None = None,
    ) -> dict[str, object]:
        """Read a whole referenced source document sequentially, by resource id
        — the recommended way to read a source document directly (e.g. a
        ``resource_id`` taken from a Wiki page's ``SourceRefs``) when you want
        its chunks in order rather than only the chunks a page cites. Companion
        to ``read_wiki_source_chunk`` (which resolves cited chunks by page slug).

        Parameters:
        - workspace_id: workspace the datasets belong to.
        - dataset_ids: dataset ids the resource belongs to, at least one.
        - resource_id: the referenced source document/resource to read (e.g. from
          a Wiki page's SourceRefs).
        - limit: max number of ordered chunks per page.
        - cursor_segment_id: paging cursor; omit on first read. Only reuse the
          cursor from the immediately previous call for the same document.
        - user_info: optional end-user identity, {"UserID": ..., "UserChannel": ...},
          forwarded verbatim; only IAM / mappable Lark channels drive permission
          filtering (see module docstring).
        """

        return read_wiki_source_doc(
            client,
            workspace_id=workspace_id,
            dataset_ids=dataset_ids,
            resource_id=resource_id,
            limit=limit,
            cursor_segment_id=cursor_segment_id,
            user_info=user_info,
        )
