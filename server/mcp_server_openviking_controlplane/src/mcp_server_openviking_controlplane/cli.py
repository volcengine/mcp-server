import json
import logging
from typing import Any, Dict, List, Optional

import typer

from mcp_server_openviking_controlplane.client import ControlPlaneClient, ControlPlaneError
from mcp_server_openviking_controlplane.config import build_config

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
    label: str,
) -> Dict[str, Any]:
    if not api_key_id and not api_key:
        raise typer.BadParameter(f"{label} needs --{label}-api-key-id or --{label}-api-key")
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
    host: Optional[str] = typer.Option(None, "--host", help="Gateway host (overrides VIKING_HOST)."),
    schema: Optional[str] = typer.Option(None, "--schema", help="http or https (overrides VIKING_SCHEMA)."),
    project: Optional[str] = typer.Option(None, "--project", help="Default project (overrides OPENVIKING_PROJECT)."),
    headers_file: Optional[str] = typer.Option(
        None, "--headers-file", "-H",
        help="Path to a headers file: JSON object, or raw 'Key: Value' lines copied from the browser.",
    ),
    header: Optional[List[str]] = typer.Option(
        None, "--header",
        help="Inline header 'Key: Value' (repeatable). Overrides --headers-file.",
    ),
):
    """Stash a client factory on the context; commands build it on demand."""
    inline_headers: Optional[Dict[str, str]] = None
    if header:
        inline_headers = {}
        for h in header:
            key, sep, value = h.partition(":")
            if not sep:
                raise typer.BadParameter(f"--header must be 'Key: Value', got: {h}")
            inline_headers[key.strip()] = value.strip()

    def _factory() -> ControlPlaneClient:
        config = build_config(
            host=host,
            schema=schema,
            project=project,
            headers=inline_headers,
            headers_file=headers_file,
        )
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
    """Get the plaintext data-plane API Key of a collection."""
    client = _client(ctx)
    try:
        _print(client.get_user_access(resource_id))
    except Exception as e:
        raise _fail(e)


@app.command("create")
def create_cmd(
    ctx: typer.Context,
    name: str = typer.Option(..., help="Library name ^[a-zA-Z][a-zA-Z0-9_]*$, <=64."),
    source: str = typer.Option("volcengine", help="Model source: volcengine | codeplan."),
    version: str = typer.Option("developer", help="Library version (currently only 'developer')."),
    vlm_model: str = typer.Option(..., help="VLM ModelName (must start with 'doubao')."),
    vlm_api_key_id: Optional[str] = typer.Option(None, help="VLM ApiKeyID (exclusive with --vlm-api-key)."),
    vlm_api_key: Optional[str] = typer.Option(None, help="VLM ApiKey (exclusive with --vlm-api-key-id)."),
    vlm_endpoint_id: Optional[str] = typer.Option(None, help="VLM EndpointID (optional)."),
    emb_model: str = typer.Option(..., help="Embedding ModelName (must start with 'doubao')."),
    emb_api_key_id: Optional[str] = typer.Option(None, help="Embedding ApiKeyID (exclusive with --emb-api-key)."),
    emb_api_key: Optional[str] = typer.Option(None, help="Embedding ApiKey (exclusive with --emb-api-key-id)."),
    emb_endpoint_id: Optional[str] = typer.Option(None, help="Embedding EndpointID (optional)."),
    project: Optional[str] = typer.Option(None, help="Project name (defaults to configured)."),
    description: Optional[str] = typer.Option(None, help="Description, <=65535 chars."),
    openviking_version: Optional[str] = typer.Option(None, help="Image version (optional)."),
):
    """Create a new collection (consumes paid quota; max 20 per account)."""
    client = _client(ctx)
    vlm = _model_cfg(vlm_model, vlm_api_key_id, vlm_api_key, vlm_endpoint_id, "vlm")
    embedding = _model_cfg(emb_model, emb_api_key_id, emb_api_key, emb_endpoint_id, "emb")
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
