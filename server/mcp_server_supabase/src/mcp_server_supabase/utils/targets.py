from typing import Optional


def resolve_workspace_id(workspace_id: Optional[str]) -> Optional[str]:
    if not workspace_id:
        return None
    normalized_id = workspace_id.strip()
    if not normalized_id:
        return None
    if normalized_id.startswith("br-"):
        raise ValueError("workspace_id must be a workspace ID; branch IDs are not supported")
    return normalized_id
