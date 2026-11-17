"""v3.3.0 unified dataset discovery contract."""
from fastmcp import FastMCP
from mcp_server_hiagent_knowledge.common.tools._common import OPENAPI_SERVICE, OPENAPI_VERSION, OpenAPIClient
from mcp_server_hiagent_knowledge.versions.v3_1_0.tools.knowledge import KNOWLEDGE_USER_ACTION
DATASET_TOOL_NAMES = ("list_datasets", "get_dataset")
def list_datasets(client: OpenAPIClient, *, workspace_id: str | None = None, user_id: str | None = None,
                  keyword: str | None = None, limit: int | None = None,
                  cursor: str | None = None, ids: list[str] | None = None) -> dict[str, object]:
    arguments = {}
    if keyword is not None:
        arguments["Filter"] = {"Keyword": keyword}
    if limit is not None:
        arguments["Limit"] = limit
    if cursor is not None:
        arguments["Cursor"] = cursor
    if ids is not None:
        arguments["IDs"] = ids
    body = {"ToolName": "list_datasets", "ListDatasets": arguments}
    if workspace_id is not None and workspace_id.strip():
        body["WorkspaceID"] = workspace_id
    if user_id is not None:
        if not user_id.strip():
            raise ValueError("user_id must be non-empty when provided")
        body["UserInfo"] = {"UserID": user_id, "UserChannel": "IAM"}
    return client.call(action=KNOWLEDGE_USER_ACTION, version=OPENAPI_VERSION, service=OPENAPI_SERVICE, body=body)
def get_dataset(client: OpenAPIClient, *, workspace_id: str, dataset_id: str) -> dict[str, object]:
    if not workspace_id:
        raise ValueError("workspace_id is required")
    if not dataset_id:
        raise ValueError("dataset_id is required")
    payload = list_datasets(client, workspace_id=workspace_id, ids=[dataset_id])
    items = ((payload.get("Result") or {}).get("ListDatasets") or {}).get("Items") or []
    for item in items:
        if item.get("DatasetID") == dataset_id:
            return {"Result": {"Dataset": item}}
    raise ValueError(f"dataset {dataset_id!r} is not visible in workspace {workspace_id!r}")
def register_dataset_tools(mcp: FastMCP, client: OpenAPIClient) -> None:
    @mcp.tool(name="list_datasets")
    def list_datasets_tool(workspace_id: str | None = None, user_id: str | None = None, keyword: str | None = None,
                           limit: int | None = None, cursor: str | None = None, ids: list[str] | None = None) -> dict[str, object]:
        """Discover own and visible shared knowledge bases (HiAgent v3.3.0). workspace_id is optional: omit/blank merges joined and legacy personal spaces; provided scopes discovery to one workspace. Optional user_id fixes identity channel to IAM and may only name the credential identity itself; omitted uses credential identity. keyword matches name/description; limit backend default 100, range 1..100. Cursor binds tenant/user/workspace/keyword/limit. ids=[] returns empty; ids conflicts with explicit limit/cursor. Result.ListDatasets.Items includes DatasetID, Name, Description, WorkspaceID, Icon, IndexingTechnique, IndexTypes; shared WorkspaceID is its source. Optional NextCursor, no Total. Discovery never replaces retrieval authorization."""
        return list_datasets(client, workspace_id=workspace_id, user_id=user_id, keyword=keyword, limit=limit, cursor=cursor, ids=ids)
    @mcp.tool(name="get_dataset")
    def get_dataset_tool(workspace_id: str, dataset_id: str) -> dict[str, object]:
        """Get one knowledge base, including default retrieval parameters."""
        return get_dataset(client, workspace_id=workspace_id, dataset_id=dataset_id)
