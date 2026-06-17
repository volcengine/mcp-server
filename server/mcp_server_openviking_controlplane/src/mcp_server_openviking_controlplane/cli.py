import json
import logging
from typing import Any, Dict, Optional

import typer

from mcp_server_openviking_controlplane.client import ControlPlaneClient, ControlPlaneError
from mcp_server_openviking_controlplane.config import (
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_VLM_MODEL,
    build_config,
)

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = typer.Typer(
    help=(
        "OpenViking control plane (topapi) CLI — manage OV collections. "
        "Shares the same core (client.py) as the MCP server."
    ),
    no_args_is_help=True,
    add_completion=True,
)


def _print(result: Any) -> None:
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))


def _fail(e: Exception) -> "typer.Exit":
    if isinstance(e, ControlPlaneError):
        suffix = f" (RequestId={e.request_id})" if e.request_id else ""
        typer.echo(f"Error [{e.code}]: {e.message}{suffix}", err=True)
    else:
        typer.echo(f"Error: {e}", err=True)
    raise typer.Exit(code=1)


def _client(ctx: typer.Context) -> ControlPlaneClient:
    """Build the shared client lazily so `--help` never needs valid config."""
    try:
        return ctx.obj()
    except Exception as e:
        raise _fail(e)


def _model_cfg(
    model_name: str,
    api_key_id: Optional[str],
    api_key: Optional[str],
    endpoint_id: Optional[str],
) -> Dict[str, Any]:
    """Assemble a VLM/Embedding model config from whatever the caller supplied.

    No key is required here: for the ``agentplan`` source the client fills in the
    configured AgentPlan ApiKey; other sources are validated server-side."""
    cfg: Dict[str, Any] = {"ModelName": model_name}
    if api_key_id:
        cfg["ApiKeyID"] = api_key_id
    if api_key:
        cfg["ApiKey"] = api_key
    if endpoint_id:
        cfg["EndpointID"] = endpoint_id
    return cfg


@app.callback()
def main_callback(
    ctx: typer.Context,
    endpoint: Optional[str] = typer.Option(
        None, "--endpoint", "-e",
        help="Control-plane base URL (overrides VIKING_ENDPOINT). "
             "For local testing point at a port-forward, e.g. http://localhost:18080",
    ),
    api_key: Optional[str] = typer.Option(
        None, "--api-key", "-k",
        help="Ark AgentPlan ApiKey, sent as 'Authorization: Bearer' (overrides AGENTPLAN_API_KEY).",
    ),
    project: Optional[str] = typer.Option(
        None, "--project", help="Default project (overrides OPENVIKING_PROJECT)."
    ),
):
    """Stash a client factory on the context; commands build it on demand."""

    def _factory() -> ControlPlaneClient:
        config = build_config(endpoint=endpoint, project=project, api_key=api_key)
        return ControlPlaneClient(config)

    ctx.obj = _factory


@app.command("list")
def list_cmd(
    ctx: typer.Context,
    project: Optional[str] = typer.Option(None, "--project", help="Filter by project."),
):
    """List collections under the account."""
    client = _client(ctx)
    try:
        _print(client.list_collections(project=project))
    except Exception as e:
        raise _fail(e)


@app.command("get")
def get_cmd(ctx: typer.Context, resource_id: str = typer.Argument(..., help="Target library ResourceID.")):
    """Get basic info of a collection."""
    client = _client(ctx)
    try:
        _print(client.get_collection(resource_id))
    except Exception as e:
        raise _fail(e)


@app.command("usage")
def usage_cmd(ctx: typer.Context, resource_id: str = typer.Argument(..., help="Target library ResourceID.")):
    """Get overall usage / file counts of a collection."""
    client = _client(ctx)
    try:
        _print(client.get_usage(resource_id))
    except Exception as e:
        raise _fail(e)


@app.command("api-key")
def api_key_cmd(ctx: typer.Context, resource_id: str = typer.Argument(..., help="Target library ResourceID.")):
    """Get the plaintext data-plane API Key of a collection (default user)."""
    client = _client(ctx)
    try:
        _print(client.get_user_access(resource_id))
    except Exception as e:
        raise _fail(e)


@app.command("create")
def create_cmd(
    ctx: typer.Context,
    name: str = typer.Option(..., help="Library name ^[a-zA-Z][a-zA-Z0-9_]*$, <=64."),
    source: str = typer.Option("agentplan", help="Model source: agentplan | volcengine | codeplan."),
    version: str = typer.Option("developer", help="Library version (currently only 'developer')."),
    vlm_model: str = typer.Option(DEFAULT_VLM_MODEL, help="VLM ModelName."),
    vlm_api_key_id: Optional[str] = typer.Option(None, help="VLM ApiKeyID (exclusive with --vlm-api-key)."),
    vlm_api_key: Optional[str] = typer.Option(None, help="VLM ApiKey (defaults to --api-key when source=agentplan)."),
    vlm_endpoint_id: Optional[str] = typer.Option(None, help="VLM EndpointID (volcengine source only)."),
    emb_model: str = typer.Option(DEFAULT_EMBEDDING_MODEL, help="Embedding ModelName."),
    emb_api_key_id: Optional[str] = typer.Option(None, help="Embedding ApiKeyID (exclusive with --emb-api-key)."),
    emb_api_key: Optional[str] = typer.Option(None, help="Embedding ApiKey (defaults to --api-key when source=agentplan)."),
    emb_endpoint_id: Optional[str] = typer.Option(None, help="Embedding EndpointID (volcengine source only)."),
    project: Optional[str] = typer.Option(None, help="Project name (defaults to configured)."),
    description: Optional[str] = typer.Option(None, help="Description, <=65535 chars."),
    openviking_version: Optional[str] = typer.Option(None, help="Image version (optional)."),
):
    """Create a new collection (consumes paid quota; max 20 per account).

    For source=agentplan you can pass just --name: the model names default to the
    AgentPlan models and the model ApiKey falls back to --api-key / AGENTPLAN_API_KEY.
    """
    client = _client(ctx)
    vlm = _model_cfg(vlm_model, vlm_api_key_id, vlm_api_key, vlm_endpoint_id)
    embedding = _model_cfg(emb_model, emb_api_key_id, emb_api_key, emb_endpoint_id)
    try:
        _print(
            client.create_collection(
                name=name,
                source=source,
                vlm=vlm,
                embedding=embedding,
                version=version,
                project=project,
                description=description,
                openviking_version=openviking_version,
            )
        )
    except Exception as e:
        raise _fail(e)


@app.command("delete")
def delete_cmd(
    ctx: typer.Context,
    resource_id: str = typer.Argument(..., help="Target library ResourceID."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip the confirmation prompt."),
):
    """Delete a collection (irreversible; uninstalls its Helm release)."""
    client = _client(ctx)
    if not yes:
        typer.confirm(
            f"Irreversibly delete collection {resource_id} (uninstalls its Helm release)?",
            abort=True,
        )
    try:
        _print(client.delete_collection(resource_id))
    except Exception as e:
        raise _fail(e)


def main():
    app()


if __name__ == "__main__":
    main()
