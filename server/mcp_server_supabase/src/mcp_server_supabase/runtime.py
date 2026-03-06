from dataclasses import dataclass
from typing import Optional

from .platform import AidapClient
from .tools import DatabaseTools, EdgeFunctionTools, StorageTools, WorkspaceTools


@dataclass(slots=True)
class SupabaseRuntime:
    aidap_client: AidapClient
    default_workspace_id: Optional[str]
    edge_tools: EdgeFunctionTools
    storage_tools: StorageTools
    database_tools: DatabaseTools
    workspace_tools: WorkspaceTools


def create_runtime(
    default_workspace_id: Optional[str] = None,
    aidap_client: Optional[AidapClient] = None,
) -> SupabaseRuntime:
    client = aidap_client or AidapClient()
    return SupabaseRuntime(
        aidap_client=client,
        default_workspace_id=default_workspace_id,
        edge_tools=EdgeFunctionTools(client, default_workspace_id),
        storage_tools=StorageTools(client, default_workspace_id),
        database_tools=DatabaseTools(client, default_workspace_id),
        workspace_tools=WorkspaceTools(client, default_workspace_id),
    )
