from typing import Optional


async def resolve_target(aidap_client, target_id: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    if not target_id:
        return None, None
    return await aidap_client.resolve_workspace_and_branch(target_id)
