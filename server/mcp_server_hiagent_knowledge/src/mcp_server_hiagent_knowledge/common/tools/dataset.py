"""Dataset detail capability shared by every version."""
from fastmcp import FastMCP
from ._common import OPENAPI_SERVICE, OPENAPI_VERSION, OpenAPIClient

def get_dataset(client: OpenAPIClient, *, workspace_id: str, dataset_id: str) -> dict[str, object]:
    if not workspace_id:
        raise ValueError("workspace_id is required")
    if not dataset_id:
        raise ValueError("dataset_id is required")
    return client.call(action="GetDataset", version=OPENAPI_VERSION, service=OPENAPI_SERVICE,
                       body={"WorkspaceID": workspace_id, "Id": dataset_id})

def register_get_dataset(mcp: FastMCP, client: OpenAPIClient) -> None:
    @mcp.tool(name="get_dataset")
    def get_dataset_tool(workspace_id: str, dataset_id: str) -> dict[str, object]:
        """Get one knowledge base, including default retrieval parameters."""
        return get_dataset(client, workspace_id=workspace_id, dataset_id=dataset_id)
