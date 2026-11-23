"""Original v3.1.0 ListDatasets contract; no shared discovery changes."""
from fastmcp import FastMCP
from mcp_server_hiagent_knowledge.common.tools._common import OPENAPI_SERVICE, OPENAPI_VERSION, OpenAPIClient
from mcp_server_hiagent_knowledge.common.tools.dataset import get_dataset, register_get_dataset
DATASET_TOOL_NAMES = ("list_datasets", "get_dataset")
def list_datasets(client: OpenAPIClient, *, workspace_id: str, name: str | None = None,
                  page_number: int = 1, page_size: int = 20) -> dict[str, object]:
    if not workspace_id:
        raise ValueError("workspace_id is required")
    body = {"WorkspaceID": workspace_id, "PageNumber": page_number, "PageSize": page_size}
    if name is not None:
        body["Filter"] = {"Name": name}
    return client.call(action="ListDatasets", version=OPENAPI_VERSION, service=OPENAPI_SERVICE, body=body)
def register_dataset_tools(mcp: FastMCP, client: OpenAPIClient) -> None:
    @mcp.tool(name="list_datasets")
    def list_datasets_tool(workspace_id: str, name: str | None = None, page_number: int = 1, page_size: int = 20) -> dict[str, object]:
        """List knowledge bases in a workspace using the original page-number API. workspace_id is required; name filters name/description."""
        return list_datasets(client, workspace_id=workspace_id, name=name, page_number=page_number, page_size=page_size)
    register_get_dataset(mcp, client)
