from dataclasses import dataclass
from typing import Any, Callable

from .platform import AidapClient
from .tools import DatabaseTools, EdgeFunctionTools, StorageTools, WorkspaceTools


@dataclass(slots=True)
class SupabaseRuntime:
    aidap_client: AidapClient
    edge_tools: EdgeFunctionTools
    storage_tools: StorageTools
    database_tools: DatabaseTools
    workspace_tools: WorkspaceTools


def create_runtime(
    aidap_client: AidapClient | None = None,
    context_getter: Callable[[], Any] | None = None,
) -> SupabaseRuntime:
    client = aidap_client or AidapClient(context_getter=context_getter)
    return SupabaseRuntime(
        aidap_client=client,
        edge_tools=EdgeFunctionTools(client),
        storage_tools=StorageTools(client),
        database_tools=DatabaseTools(client),
        workspace_tools=WorkspaceTools(client),
    )
