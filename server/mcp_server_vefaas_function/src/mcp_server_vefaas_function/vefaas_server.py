import pathspec
import io
from pdb import run
from socket import timeout
from typing import Union, Optional, List
import datetime
import volcenginesdkcore
import volcenginesdkvefaas
from volcenginesdkcore.rest import ApiException
import random
import string
import logging
import time

from volcenginesdkvefaas import VEFAASApi

from .sign import request, get_authorization_credentials
import json
from mcp.server.fastmcp import Context, FastMCP
import os
import subprocess
import zipfile
from io import BytesIO
from typing import Tuple
import requests
import shutil

from .vefaas_cli_sdk.deploy import package_directory

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("veFaaS MCP Server",
              host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
              port=int(os.getenv("MCP_SERVER_PORT", "8000")),
              stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))


def validate_and_set_region(region: str = None) -> str:
    """
    Validates the provided region and returns a valid region string.
    If no region is provided, it tries to detect it from local configuration.

    Priority:
    1. Provided region parameter
    2. Region from .vefaas/config.json or vefaas.yaml in current directory
    3. Default to "cn-beijing"
    """
    valid_regions = ["ap-southeast-1", "cn-beijing", "cn-shanghai", "cn-guangzhou"]

    if region:
        if region not in valid_regions:
            # We allow it but log a warning, just in case a new region is added
            logger.warning(f"Region '{region}' is not in the known valid regions list: {valid_regions}")
        return region

    # Try to detect from local config
    try:
        from .vefaas_cli_sdk.config import read_config
        config = read_config(os.getcwd())
        if config and config.function.region:
            detected_region = config.function.region
            if detected_region not in valid_regions:
                logger.warning(f"Auto-detected region '{detected_region}' from config is not in the known list: {valid_regions}")
            else:
                logger.info(f"Auto-detected region from config: {detected_region}")
            return detected_region
    except Exception as e:
        logger.debug(f"Failed to auto-detect region from config: {e}")

    # Default
    return "cn-beijing"


def append_random_suffix(name: str, length: int = 6) -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{name}-{suffix}"


def is_name_conflict_error(exception: ApiException) -> bool:
    message = str(exception).lower()
    if "already exists" in message:
        return True

    body = getattr(exception, "body", None)
    if body:
        if isinstance(body, (bytes, bytearray)):
            body_text = body.decode("utf-8", errors="ignore").lower()
        else:
            body_text = str(body).lower()
        if "already exists" in body_text:
            return True

    return False


@mcp.tool(description="""Update veFaaS function code and configuration.

**Use Cases**:
- Upload local code changes to online function
- Update function command, environment variables, etc.
- Sync code after local development

**Parameters**:
- function_id: Function ID (required)
- region: Region (default cn-beijing)
- project_path: Local project path (required for code update, absolute path)
- command: Startup command (optional)
- envs: Environment variables dict (optional)

**File Filtering**:
- Uses `.vefaasignore` file in project root (gitignore syntax)
- Auto-creates default `.vefaasignore` if not exists

**Workflow**:
1. If project_path provided, zip and upload code (respecting .vefaasignore)
2. If command/envs provided, update function config
3. Return upload/update result

**Note**:
- After updating code, call release_function to publish changes
- release_function will auto-handle dependency installation and release
""")
def update_function(function_id: str, region: Optional[str] = None,
                    project_path: Optional[str] = None,
                    command: Optional[str] = None,
                    envs: Optional[dict] = None):

    region = validate_and_set_region(region)
    api_instance = init_client(region, mcp.get_context())

    result = {"function_id": function_id, "region": region}

    # Upload code if project_path is provided
    if project_path:
        if not os.path.isabs(project_path):
            raise ValueError(f"project_path must be an absolute path, got: {project_path}")
        if not os.path.exists(project_path):
            raise ValueError(f"project_path does not exist: {project_path}")

        try:
            ak, sk, token = get_authorization_credentials(mcp.get_context())
        except ValueError as e:
            raise ValueError(f"Authorization failed: {str(e)}")

        # Zip code using .vefaasignore
        data, size, error = zip_and_encode_folder(project_path)
        if error:
            raise ValueError(f"Error zipping folder: {error}")
        if not data or size == 0:
            raise ValueError("Zipped folder is empty, nothing to upload")

        # Upload code
        upload_code_zip_for_function(
            api_instance=api_instance,
            function_id=function_id,
            code_zip_size=size,
            zip_bytes=data,
            ak=ak,
            sk=sk,
            token=token,
            region=region,
        )
        result["code_uploaded"] = True
        # Use KB for small files, MB for larger files
        if size < 1024 * 1024:
            result["upload_size"] = f"{round(size / 1024, 1)} KB"
        else:
            result["upload_size"] = f"{round(size / 1024 / 1024, 2)} MB"
        logger.info(f"Code uploaded successfully, size: {result['upload_size']}")

    # Update function config (command, envs)
    update_request = volcenginesdkvefaas.UpdateFunctionRequest(id=function_id)
    has_config_update = False

    if command is not None and command != "":
        update_request.command = command
        has_config_update = True
        result["command_updated"] = command

    if envs:
        env_list = [{"key": key, "value": value} for key, value in envs.items()]
        update_request.envs = env_list
        has_config_update = True
        result["envs_updated"] = list(envs.keys())

    if has_config_update:
        try:
            api_instance.update_function(update_request)
            result["config_updated"] = True
        except ApiException as e:
            raise ValueError(f"Failed to update function config: {str(e)}")

    # Save config to vefaas.yaml if project_path is provided
    if project_path:
        try:
            from .vefaas_cli_sdk import write_config, VefaasConfig, FunctionConfig

            # Get function info for config
            try:
                func_req = volcenginesdkvefaas.GetFunctionRequest(id=function_id)
                func_resp = api_instance.get_function(func_req)
                runtime = func_resp.runtime
                func_name = func_resp.name
            except Exception:
                runtime = None
                func_name = None

            save_config = VefaasConfig(
                function=FunctionConfig(
                    id=function_id,
                    runtime=runtime,
                    region=region,
                ),
                name=func_name,
                command=command,
            )
            write_config(project_path, save_config)
            result["config_saved"] = True
        except Exception as e:
            logger.warning(f"Failed to save config: {e}")

    result["next_step"] = "Code updated. If you want to publish changes, call release_function. Note: release_function will trigger dependency installation and deploy to production."
    result["platform_url"] = f"https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}"

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool(description="""Release (deploy) a veFaaS function to production.

**Use Cases**:
- Publish code changes after update_function
- Deploy new version to production

**Parameters**:
- function_id: Function ID (required)
- region: Region (default cn-beijing)
- skip_dependency: Skip dependency installation step (default False). Use when dependencies are already installed.

**Workflow**:
1. Trigger dependency installation (if requirements.txt/package.json exists, unless skip_dependency=True)
2. Wait for dependency installation to complete
3. Submit release request
4. Poll release status until succeeded/failed
5. Return final status with access link and revision info

**Returns**:
- release_status: succeeded/failed
- stable_revision_number: Current stable revision number
- new_revision_number: New revision number after release
- access_link: Function access URL
- platform_url: Console link
- error_message: Error details (if failed)
""")
def release_function(function_id: str, region: Optional[str] = None, skip_dependency: bool = False) -> str:
    region = validate_and_set_region(region)
    api_instance = init_client(region, mcp.get_context())

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    result = {"function_id": function_id, "region": region}

    # Early check: if release is already in progress, return immediately with guidance
    try:
        req = volcenginesdkvefaas.GetReleaseStatusRequest(function_id=function_id)
        current_status = api_instance.get_release_status(req)
        if current_status.status == "inprogress":
            return json.dumps({
                "function_id": function_id,
                "region": region,
                "release_status": "inprogress",
                "next_action": "Release is already in progress. Wait for completion, or call get_function_detail to check status.",
                "platform_url": f"https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}"
            }, ensure_ascii=False, indent=2)
    except Exception:
        pass  # If status check fails, proceed with release

    # Step 1: Trigger dependency installation (unless skipped)
    if skip_dependency:
        logger.info("Skipping dependency installation as requested.")
        result["dependency_triggered"] = False
        result["dependency_status"] = "skipped"
    else:
        logger.info("Triggering dependency installation...")
        # Use SDK client for dependency operations
        from .vefaas_cli_sdk import VeFaaSClient, wait_for_dependency_install
        client = VeFaaSClient(ak, sk, token, region)

        try:
            client.create_dependency_install_task(function_id)
            logger.info("Dependency install task created, waiting for completion...")
            result["dependency_triggered"] = True

            # Step 2: Wait for dependency installation using SDK logic
            dep_result = wait_for_dependency_install(client, function_id, timeout_seconds=300)
            result["dependency_status"] = dep_result.get("status", "succeeded")
            logger.info(f"Dependency installation completed: {result['dependency_status']}")

        except ValueError as e:
            # Dependency installation failed
            result["dependency_triggered"] = True
            result["dependency_status"] = "failed"
            raise ValueError(f"Dependency installation failed: {e}")
        except Exception as e:
            # Dependency install may fail if no requirements.txt/package.json, that's OK
            logger.info(f"Dependency install skipped or not needed: {str(e)}")
            result["dependency_triggered"] = False
            result["dependency_status"] = "skipped"

    # Step 3: Submit release request
    logger.info("Submitting release request...")
    try:
        req = volcenginesdkvefaas.ReleaseRequest(
            function_id=function_id, revision_number=0
        )
        api_instance.release(req)
        logger.info("Release request submitted, polling status...")
    except ApiException as e:
        raise ValueError(f"Failed to submit release: {str(e)}")

    # Step 4: Poll release status
    timeout = 120
    interval = 5
    start_time = time.time()
    release_status = None
    status_message = ""

    while time.time() - start_time < timeout:
        try:
            req = volcenginesdkvefaas.GetReleaseStatusRequest(function_id=function_id)
            response = api_instance.get_release_status(req)
            release_status = response.status
            status_message = response.status_message or ""

            if release_status == "inprogress":
                time.sleep(interval)
            else:
                break
        except Exception as e:
            logger.warning(f"Failed to get release status: {e}")
            break

    # Build final result
    result["release_status"] = release_status or "unknown"
    if status_message:
        result["status_message"] = status_message

    result["platform_url"] = f"https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}"

    # Get revision info from final status
    try:
        req = volcenginesdkvefaas.GetReleaseStatusRequest(function_id=function_id)
        final_status = api_instance.get_release_status(req)
        if getattr(final_status, 'stable_revision_number', None) is not None:
            result["stable_revision_number"] = final_status.stable_revision_number
        if getattr(final_status, 'new_revision_number', None) is not None:
            result["new_revision_number"] = final_status.new_revision_number
    except Exception:
        pass

    # Get access link
    try:
        access_link = get_function_access_link(function_id, region)
        if access_link:
            result["access_link"] = access_link
    except Exception:
        pass

    if release_status == "failed":
        result["error_message"] = status_message
        raise ValueError(json.dumps(result, ensure_ascii=False, indent=2))

    return json.dumps(result, ensure_ascii=False, indent=2)


def get_function_release_status(function_id: str, region: Optional[str] = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    req = volcenginesdkvefaas.GetReleaseStatusRequest(
        function_id=function_id
    )
    response = api_instance.get_release_status(req)
    if response.status == "inprogress":
        time.sleep(10)
    return response


def poll_function_release_status(function_id: str, region: Optional[str] = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    req = volcenginesdkvefaas.GetReleaseStatusRequest(
        function_id=function_id
    )
    start_time = time.time()
    timeout: int = 120
    interval: int = 5
    while time.time() - start_time < timeout:
        response = api_instance.get_release_status(req)
        if response.status == "inprogress":
            time.sleep(interval)
        else:
            break

    responseInfo = {
        "function_id": function_id,
        "region": region,
        "release_status": response.status or "unknown",
        "status_message": response.status_message or '',
        "target_traffic_weight": response.target_traffic_weight or -1,
        "current_traffic_weight": response.current_traffic_weight or -1,
        "new_revision_number": response.new_revision_number or -1,
        "old_revision_number": response.old_revision_number or -1,
        "start_time": response.start_time or '',
        "vefaas_function_platform_url": f"https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}",
        "vefaas_function_access_link": get_function_access_link(function_id, region),
    }
    return responseInfo


def get_function_access_link(function_id: str, region: Optional[str] = None):
    region = validate_and_set_region(region)

    triggers = list_function_triggers(function_id, region).get("Result", {}).get("Items", [])
    upstream_id = ''
    try:
        for trigger in triggers:
            if trigger.get("Type") == "apig":
                upstream_id = json.loads(trigger.get("DetailedConfig", '')).get("UpstreamId", '')
                break
    except Exception as e:
        logger.error(f"Failed to parse trigger config: {str(e)}")
        raise ValueError(f"Failed to parse trigger config: {str(e)}")

    if upstream_id == '':
        return ''

    try:
        body = {
            'PageNumber': 1,
            'PageSize': 100,
            'UpstreamId': upstream_id,
        }

        now = datetime.datetime.utcnow()
        try:
            ak, sk, token = get_authorization_credentials(mcp.get_context())
        except ValueError as e:
            raise ValueError(f"Authorization failed: {str(e)}")

        response = request("POST", now, {}, {}, ak, sk, token, "ListRoutes", json.dumps(body), region)
        items = response.get("Result", {}).get("Items", [])
        if len(items) == 0:
            return ''
        domains = items[0].get("Domains", [])
        if len(domains) == 0:
            return ''
        for domainInfo in domains:
            if domainInfo.get("Domain").startswith("https://"):
                return domainInfo.get("Domain")
    except Exception as e:
        logger.error(f"Failed to parse route config: {str(e)}")
        return f"Failed to parse route config: {str(e)}"

    return ''


def generate_random_name(prefix="mcp", length=8):
    """Generate a random string for function name"""
    random_str = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{prefix}-{random_str}"


def init_client(region: str = None, ctx: Context = None):
    """
    Initializes the veFaaS API client with credentials and region.

    Args:
        region: The region to use for the client
        ctx: The server context object

    Returns:
        VEFAASApi: Initialized veFaaS API client

    Raises:
        ValueError: If authorization fails
    """
    try:
        ak, sk, session_token = get_authorization_credentials(ctx)
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    configuration = volcenginesdkcore.Configuration()
    configuration.ak = ak
    configuration.sk = sk
    if session_token:
        configuration.session_token = session_token

    # Set region with default if needed
    region = validate_and_set_region(region)
    logger.info("Using region: %s", region)
    configuration.region = region

    # set default configuration
    volcenginesdkcore.Configuration.set_default(configuration)
    return volcenginesdkvefaas.VEFAASApi()


def list_existing_api_gateways(region: str = None):
    now = datetime.datetime.utcnow()

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    response_body = request("GET", now, {"Limit": "20"}, {}, ak, sk, token, "ListGateways", None, region)
    try:
        exist_gateways = response_body.get("Result", {}).get("Items", [])
        result = []
        for gateway in exist_gateways:
            if gateway.get("Region") == region and gateway.get("Status") in ["Running", "Creating"]:
                result.append({
                    "Name": gateway.get("Name", ""),
                    "Region": gateway.get("Region", ""),
                    "Type": gateway.get("Type", ""),
                    "Status": gateway.get("Status", ""),
                })
        return result
    except Exception as e:
        return f"Failed to list API Gateways: {str(e)}"


def create_api_gateway(name: str = None, region: Optional[str] = None):
    """
    Creates a new VeApig gateway.

    Args:
        name (str): The name of the gateway. If not provided, a random name will be generated.
        region (str): The region where the gateway will be created. Default is cn-beijing.

    Returns:
        str: The response body of the request.
    """
    gateway_name = name if name else generate_random_name()
    region = validate_and_set_region(region)
    body = {
        "Name": gateway_name,
        "Region": region,
        "Type": "serverless",
        "ResourceSpec": {
            "Replicas": 2,
            "InstanceSpecCode": "1c2g",
            "CLBSpecCode": "small_1",
            "PublicNetworkBillingType": "traffic",
            "NetworkType": {"EnablePublicNetwork": True, "EnablePrivateNetwork": False},
        },
    }

    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateGateway", json.dumps(body), region)
        return json.dumps(response_body, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Failed to create VeApig gateway with name {gateway_name}: {str(e)}"


def ensure_executable_permissions(folder_path: str):
    for root, _, files in os.walk(folder_path):
        for fname in files:
            full_path = os.path.join(root, fname)
            if fname.endswith('.sh') or fname in ('run.sh',):
                os.chmod(full_path, 0o755)


def zip_and_encode_folder(folder_path: str) -> Tuple[bytes, int, Exception]:
    """
    Zips a folder using .vefaasignore patterns for filtering.
    Delegates to cli_sdk.deploy.package_directory.

    Returns (zip_data, size_in_bytes, error) tuple.
    """
    logger.info("Zipping folder: %s", folder_path)
    try:
        # Use package_directory with include_gitignore=False (function code upload)
        data = package_directory(folder_path, include_gitignore=False)
        size = len(data)
        logger.info("Zip finished, size: %.2f MB", size / 1024 / 1024)
        return data, size, None
    except Exception as e:
        logger.error("Zip error: %s", str(e))
        return None, 0, e


def upload_code(function_id: str, region: Optional[str] = None, local_folder_path: Optional[str] = None,
                file_dict: Optional[dict[str, Union[str, bytes]]] = None) -> str:
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    if local_folder_path:
        data, size, error = zip_and_encode_folder(local_folder_path)
        if error:
            raise ValueError(f"Error zipping folder: {error}")
        if not data or size == 0:
            raise ValueError("Zipped folder is empty, nothing to upload")
    elif file_dict:
        data = build_zip_bytes_for_file_dict(file_dict)
        size = len(data)
        if not data:
            raise ValueError("No files provided in file_dict, upload aborted.")
    else:
        raise ValueError("Either local_folder_path or file_dict must be provided.")
    response_body = upload_code_zip_for_function(
        api_instance=api_instance,
        function_id=function_id,
        code_zip_size=size,
        zip_bytes=data,
        ak=ak,
        sk=sk,
        token=token,
        region=region,
    )

    dep_info = handle_dependency(
        api_instance=api_instance,
        function_id=function_id,
        local_folder_path=local_folder_path,
        file_dict=file_dict,
        ak=ak,
        sk=sk,
        token=token,
        region=region,
    )

    result = {
        "code_upload_callback": response_body,
        "dependency": dep_info,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


def handle_dependency(
    api_instance: VEFAASApi,
    function_id: str,
    local_folder_path,
    file_dict,
    ak: str,
    sk: str,
    token: str,
    region: str = None,
):
    req = volcenginesdkvefaas.GetFunctionRequest(
        id=function_id
    )

    try:
        response = api_instance.get_function(req)
        runtime = response.runtime
        logger.debug("Runtime detected: %s", runtime)
    except ApiException as e:
        raise ValueError(f"Failed to get veFaaS function: {str(e)}")

    # Treat any Python/Node runtime as eligible
    is_python = 'python' in runtime
    is_nodejs = 'node' in runtime

    has_requirements = (
        (local_folder_path is not None and os.path.exists(os.path.join(local_folder_path, "requirements.txt")))
        or (file_dict is not None and "requirements.txt" in file_dict)
    )

    has_package_json = (
        (local_folder_path is not None and os.path.exists(os.path.join(local_folder_path, "package.json")))
        or (file_dict is not None and "package.json" in file_dict)
    )

    has_node_modules = (
        (local_folder_path is not None and os.path.exists(os.path.join(local_folder_path, "node_modules")))
        or (file_dict is not None and "node_modules" in file_dict)
    )

    # Minimal decision surface for the agent
    if is_python and not has_requirements:
        logger.info("Python runtime detected, but no requirements.txt found. Skipping dependency install.")
        return {"dependency_task_created": False, "should_check_dependency_status": False, "skip_reason": "No requirements.txt"}
    if is_nodejs and not has_package_json:
        logger.info("Node.js runtime detected, but no package.json found. Skipping dependency install.")
        return {"dependency_task_created": False, "should_check_dependency_status": False, "skip_reason": "No package.json"}
    if is_nodejs and has_package_json and has_node_modules:
        logger.info("Node.js runtime detected, package.json found, but has node_modules. Skipping dependency install.")
        return {"dependency_task_created": False, "should_check_dependency_status": False, "skip_reason": "node_modules present"}
    if not is_python and not is_nodejs:
        logger.info("Runtime is not Python or Node.js. Skipping dependency install.")
        return {"dependency_task_created": False, "should_check_dependency_status": False, "skip_reason": "Unsupported runtime"}

    body = {"FunctionId": function_id}
    now = datetime.datetime.utcnow()

    try:
        create_resp = request(
            "POST", now, {}, {}, ak, sk, token, "CreateDependencyInstallTask", json.dumps(body), region
        )
        logger.debug("Dependency install response: %s", create_resp)
        return {
            "dependency_task_created": True,
            "should_check_dependency_status": True,
        }
    except Exception as e:
        # Keep behavior consistent with previous implementation: surface as an error
        raise ValueError(f"Error creating dependency install task: {str(e)}")


def poll_dependency_install_task_status(
    function_id: str,
    region: Optional[str] = None,
):
    region = validate_and_set_region(region)
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    body = {"FunctionId": function_id}
    now = datetime.datetime.utcnow()

    timeout_seconds = 120
    poll_interval_seconds = 5
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        try:
            status_resp = request(
                "POST", now, {}, {}, ak, sk, token, "GetDependencyInstallTaskStatus", json.dumps(body), region, 5,
            )
            result = {"status": status_resp}
            status = status_resp.get("Result", {}).get("Status")
        except Exception as ex:
            result = {"fetch_status_error": str(ex)}
            status = None

        if status == "InProgress" or status == None:
            time.sleep(poll_interval_seconds)
            continue
        else:
            break
    if status == "Failed":
        try:
            log_resp = request("POST", now, {}, {}, ak, sk, token, "GetDependencyInstallTaskLogDownloadURI", json.dumps(body), region, 5)
            url = log_resp.get("Result", {}).get("DownloadURL")
            if isinstance(url, str):
                url = url.replace("\\u0026", "&")
            result["log_download_url"] = url

            try:
                resp = requests.get(url, timeout=30)  # noqa: security
                result["log_content"] = resp.text
            except Exception as ex:
                result["log_content_error"] = str(ex)
        except Exception as ex:
            result["log_download_error"] = str(ex)
    return result


def upload_code_zip_for_function(api_instance: VEFAASApi(object), function_id: str, code_zip_size: int, zip_bytes,
                                 ak: str, sk: str, token: str, region: str,) -> bytes:
    req = volcenginesdkvefaas.GetCodeUploadAddressRequest(
        function_id=function_id,
        content_length=code_zip_size
    )

    response = api_instance.get_code_upload_address(req)
    upload_url = response.upload_address

    headers = {
        "Content-Type": "application/zip",
    }

    response = requests.put(url=upload_url, data=zip_bytes, headers=headers)  # noqa: security
    if 200 <= response.status_code < 300:
        logger.info("Upload successful. Size: %.2f MB", code_zip_size / 1024 / 1024)
    else:
        error_message = f"Upload failed to {upload_url} with status code {response.status_code}: {response.text}"
        raise ValueError(error_message)

    now = datetime.datetime.utcnow()

    # Generate a random suffix for the trigger name
    suffix = generate_random_name(prefix="", length=6)

    body = {
        "FunctionId": function_id
    }

    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CodeUploadCallback", json.dumps(body), region)
        return response_body
    except Exception as e:
        error_message = f"Error creating upstream: {str(e)}"
        raise ValueError(error_message)


def build_zip_bytes_for_file_dict(file_dict):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in file_dict.items():
            info = zipfile.ZipInfo(filename)
            info.date_time = datetime.datetime.now().timetuple()[:6]
            info.external_attr = 0o755 << 16
            zip_file.writestr(info, content)
    zip_bytes = zip_buffer.getvalue()
    return zip_bytes

# Get function revision information from veFaaS.
# Use this to retrieve revision information for a veFaaS function. This function returns the revision details
# Params:
# - function_id (required): the ID of the function
# - region (optional): deployment region, defaults to cn-beijing
# - revision_number (optional): specific revision number to query. If not provided, defaults to version 0.


def get_function_revision(function_id: str, region: Optional[str] = None, revision_number: Optional[int] = 0):

    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    req = volcenginesdkvefaas.GetRevisionRequest(
        function_id=function_id,
        revision_number=revision_number,
    )

    try:
        revision_resp = api_instance.get_revision(req)
        logger.debug("GetRevision response: %s", revision_resp)
        return revision_resp
    except Exception as e:
        raise ValueError(f"Failed to get function revision: {str(e)}")

# Get function detail information from veFaaS.


@mcp.tool(description="""Get veFaaS function details.

**Use Cases**:
- View function configuration (runtime, command, envs)
- Check function status before update
- Get function info for local development

**Parameters**:
- function_id: Function ID (required)
- region: Region (default cn-beijing)

**Returns**:
- id, name, runtime, command, status
- envs: Environment variables list
- source_type: Code source type
- platform_url: Console link
""")
def get_function_detail(function_id: str, region: Optional[str] = None):
    """Get function information including configuration details."""
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    req = volcenginesdkvefaas.GetFunctionRequest(id=function_id)

    try:
        response = api_instance.get_function(req)

        # Build user-friendly result based on actual API response fields
        result = {
            "id": response.id,
            "name": response.name,
            "runtime": response.runtime,
            "command": getattr(response, 'command', '') or '',
            "port": getattr(response, 'port', None),
            "source_type": getattr(response, 'source_type', '') or '',
            "region": region,
            "platform_url": f"https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}",
        }

        # Add optional fields if present
        if getattr(response, 'description', None):
            result["description"] = response.description

        if getattr(response, 'envs', None):
            result["envs"] = [{"key": env.key, "value": env.value} for env in response.envs]

        if getattr(response, 'build_config', None):
            build_config = response.build_config
            result["build_config"] = {
                "command": getattr(build_config, 'command', '') or '',
                "output_path": getattr(build_config, 'output_path', '') or '',
            }

        # Check release status to detect in-progress deployments
        try:
            release_req = volcenginesdkvefaas.GetReleaseStatusRequest(function_id=function_id)
            release_resp = api_instance.get_release_status(release_req)
            if release_resp.status:
                result["release_status"] = release_resp.status
                if release_resp.status == "inprogress":
                    result["next_action"] = "Release is in progress. Wait for completion or check status again later."
        except Exception:
            pass  # Release status check is optional, don't fail if unavailable

        return json.dumps(result, ensure_ascii=False, indent=2)
    except ApiException as e:
        if "not found" in str(e).lower() or "does not exist" in str(e).lower():
            raise ValueError(f"Function {function_id} does not exist in region {region}")
        else:
            raise ValueError(f"Failed to get function: {str(e)}")


@mcp.tool(description="""Download function code for veFaaS function.

Args:
 - function_id: ID of the function.
 - region: Region of the function (defaults to `cn-beijing`).
 - dest_dir: absolute path to the folder where the code should be downloaded and unzipped (required).
 - revision_number: Specific revision to fetch (defaults to 0 when omitted).
 - use_stable_revision: Set to True only when online/released/stable code is required; overrides `revision_number`.

Note:
 - If your current working directory is empty, pass its absolute path so the files land directly there—avoid nesting unless necessary.
 - Only create a dedicated subfolder (e.g., `/path/to/project/vefaas_{function_id}/`) when the working directory already contains files; the server will create it if missing.
""")
def pull_function_code(function_id: str, region: Optional[str] = "", dest_dir: str = None, revision_number: Optional[int] = None, use_stable_revision: Optional[bool] = False):
    region = validate_and_set_region(region)

    # First check if function exists
    try:
        function_detail = get_function_detail(function_id, region)
        logger.info(f"Function {function_id} found in region {region}")
    except Exception as e:
        raise ValueError(f"Function {function_id} not found in region {region}: {str(e)}")

    # Determine which revision number to use
    target_revision = None
    if revision_number is not None:
        target_revision = revision_number
    elif use_stable_revision:
        # Get stable revision number from release status
        try:
            release_status = get_function_release_status(function_id, region)
            if release_status.stable_revision_number is not None:
                target_revision = release_status.stable_revision_number
                logger.info(f"Using stable revision number: {target_revision}")
        except Exception as e:
            raise ValueError(f"Failed to get stable revision number: {str(e)}")

    if target_revision is None:
        target_revision = 0

    # Get revision information
    try:
        revision_info = get_function_revision(function_id, region, target_revision)
        logger.info(f"Revision {target_revision} information retrieved")
    except Exception as e:
        raise ValueError(f"Failed to get revision {target_revision} information: {str(e)}")

    # Extract source_location from revision info
    source_location = None
    try:
        source_location = revision_info.source_location
        if source_location is None or source_location == "":
            raise ValueError("Could not find source_location in revision information")

        logger.info(f"Source location: {source_location}")

        # Download the code zip file
        response = requests.get(source_location)  # noqa: security
        response.raise_for_status()

        if not dest_dir:
            raise ValueError("dest_dir must be provided so the server knows where to extract the function code.")

        # Create destination directory if it doesn't exist
        os.makedirs(dest_dir, exist_ok=True)

        # Unzip the file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(dest_dir)

        # generate vefaas.yaml
        vefaas_yml_path = os.path.join(dest_dir, "vefaas.yaml")
        try:
            function_detail_str = get_function_detail(function_id, region)
            function_detail = json.loads(function_detail_str)
            triggers = list_function_triggers(function_id, region).get("Result", {}).get("Items", [])
            with open(vefaas_yml_path, "w") as f:
                f.write(f"function_id: {function_id}\n")
                f.write(f"name: {function_detail.get('name', '')}\n")
                f.write(f"region: {region}\n")
                f.write(f"runtime: {function_detail.get('runtime', '')}\n")
                f.write(f"command: {function_detail.get('command', '')}\n")
                f.write(f"vefaas_function_platform: https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}\n")
                f.write(f"vefaas_access_link: {get_function_access_link(function_id, region)}\n")
                f.write(f"triggers:\n")
                for trigger in triggers:
                    f.write(f"  - id: {trigger.get('Id', '')}\n")
                    f.write(f"    type: {trigger.get('Type', '')}\n")
                    f.write(f"    name: {trigger.get('Name', '')}\n")
        except Exception as e:
            logger.error(f"Failed to write vefaas.yaml for function {function_id}: {str(e)}")
            # Continue even if vefaas.yaml generation fails

        return json.dumps({
            "success": True,
            "function_id": function_id,
            "region": region,
            "revision": "latest" if not target_revision else target_revision,
            "dest_dir": dest_dir,
            "message": f"Function code extracted to {dest_dir}",
            "files_generated": ["vefaas.yaml"],
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        raise ValueError(f"Failed to download and extract function code: {str(e)}")


def list_function_triggers(function_id: str, region: Optional[str] = None):
    region = validate_and_set_region(region)

    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    body = {
        "FunctionId": function_id,
    }

    try:
        response = request(
            "POST", now, {}, {}, ak, sk, token, "ListTriggers", json.dumps(body), None, 5,
        )
        return response
    except Exception as e:
        raise ValueError(f"Failed to list function triggers: {str(e)}")


# ==================== Application Deployment Tools ====================

@mcp.tool(description="""Detect project configuration for veFaaS deployment.

**RECOMMENDED**: Call this BEFORE `deploy_application` to ensure correct configuration!

**Supported Runtimes**:
- **Node.js**: Next.js, Nuxt, Vite, VitePress, Rspress, Astro, Express, SvelteKit, Remix, CRA, Angular, Gatsby, etc.
- **Python**: FastAPI, Flask, Streamlit, Django, etc.
- **Static Sites**: HTML, Hugo, MkDocs, etc.

> **Note**: Other runtimes (e.g., Go, Java, Rust, PHP) are NOT currently supported. If your project uses an unsupported runtime, you will need to deploy manually via the veFaaS console.

This tool analyzes the project structure and automatically detects:
- Framework (Next.js, Vite, FastAPI, Flask, Streamlit, etc.)
- Runtime and startup command
- Build command and output path
- Service port

Args:
 - project_path: Absolute path to the project root directory

Returns:
 - framework: Detected framework
 - runtime: veFaaS runtime (e.g., "native-python3.12/v1", "native-node20/v1")
 - build_command: Build command (for Node.js projects)
 - start_command: **Startup command** - use this value in `deploy_application`!
 - port: Service port
 - output_path: Build output directory
 - is_static: Whether it's a static site

**Workflow**:
1. Call `detect_project` with project_path
2. Review the detected configuration (especially `start_command`)
3. Call `deploy_application` with `start_command` from step 1

**Example**:
```
detect_project("/path/to/fastapi-app")
→ {"framework": "fastapi", "start_command": "python -m uvicorn main:app --host 0.0.0.0 --port 8080", ...}

deploy_application(project_path="/path/to/fastapi-app", name="my-app", start_command="python -m uvicorn main:app --host 0.0.0.0 --port 8080")
```
""")
def detect_project(project_path: str):
    from .vefaas_cli_sdk import auto_detect

    if not os.path.isabs(project_path):
        raise ValueError(f"project_path must be an absolute path, got: {project_path}")
    if not os.path.exists(project_path):
        raise ValueError(f"project_path does not exist: {project_path}")

    result = auto_detect(project_path)

    return {
        "framework": result.framework,
        "runtime": result.runtime,
        "build_command": result.build_command,
        "start_command": result.start_command,
        "port": result.port,
        "install_command": result.install_command,
        "output_path": result.output_path,
        "is_static": result.is_static,
    }


@mcp.tool(description="""**PRIMARY DEPLOYMENT TOOL** - Deploy a project to veFaaS with one command.

This is the **recommended tool** for deploying applications. It handles the entire workflow automatically:
1. Detect project configuration
2. Build project (for Node.js/static sites only, Python projects automatically skip this step)
3. Package and upload code to cloud storage
4. Create/update function with code
5. Wait for dependencies (Python)
6. Create application with API gateway
7. Deploy and wait for completion

**Configuration Files (Auto-handled)**:
- If `.vefaas/config.json` exists, the tool will use `function_id` and `application_id` from it automatically.
- **Cross-region deployment**: Config IDs are only used if the config's region matches the target region. Deploying to a different region creates a new application.
- On successful deployment, both `.vefaas/config.json` (vefaas-cli compatible) and `vefaas.yaml` are updated.
- This means subsequent deployments only need `project_path` - no need to specify IDs again.

**Scenarios**:
- **New Python app**: Provide `project_path` + `name` + `start_command` + `port`
- **New Node.js app**: Provide `project_path` + `name` + `start_command` + `build_command` + `port`
- **Update existing app**: Just provide `project_path` (IDs read from config automatically)
- **Update by ID**: Use `application_id` to update an existing application
- **Deploy to different region**: Provide `project_path` + `name` + `region` (existing config for other regions is ignored)

Args:
 - project_path: Absolute path to the project root directory (required)
 - name: Application name (required for NEW apps, will auto-generate from folder name if not provided)
 - application_id: Application ID for updates (auto-read from config if exists)
 - region: Region (cn-beijing, cn-shanghai, cn-guangzhou, ap-southeast-1)
 - build_command: Build command (e.g., "npm run build"). Required for non-Python runtimes.
 - start_command: Startup command. **REQUIRED**. Use detect_project to auto-detect.
 - port: Service port. **IMPORTANT: Must match the actual listening port in start_command** (e.g., if start_command has --port 3000, then port must be 3000)
 - skip_build: Skip build step (default False). **Note: Python projects automatically skip build, this parameter is ignored for Python.**
 - gateway_name: API gateway name (optional, auto-selects first available gateway if not specified)

Returns:
 - application_id: Application ID
 - function_id: Function ID
 - access_url: **User can visit this URL to access the deployed app**
 - console_url: veFaaS console link for management

**Common Errors**:
- "start_command is required": Call `detect_project` first or provide start_command
- "build_command is required": For non-Python projects, provide build_command or set skip_build=True
- "Name already exists (NAME_CONFLICT)": **YOU MAY ASK THE USER** whether to update existing or create new. Present these options:
  1. Update existing: retry with `application_id` parameter (ID is in error message)
  2. Create new: retry with a different `name` parameter
- "deploy_fail": The returned error will include detailed error_message and error_logs_uri

**Retry/Redeployment**:
- If deployment fails, fix the code and call `deploy_application` again.
- Do NOT use `create_function`, `update_function`, `upload_code`, or `release_function` as workarounds.
""")
def deploy_application(
    project_path: str,
    name: Optional[str] = None,
    application_id: Optional[str] = None,
    region: Optional[str] = None,
    build_command: Optional[str] = None,
    start_command: Optional[str] = None,
    port: Optional[int] = None,
    skip_build: bool = False,
    gateway_name: Optional[str] = None,
):
    from .vefaas_cli_sdk import (
        DeployConfig,
        VeFaaSClient,
        deploy_application as sdk_deploy_application,
    )

    region = validate_and_set_region(region)

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authentication failed: {str(e)}")

    # Initialize SDK client
    client = VeFaaSClient(ak, sk, token, region)

    # Build config
    config = DeployConfig(
        project_path=project_path,
        name=name,
        application_id=application_id,
        region=region,
        gateway_name=gateway_name,
        build_command=build_command,
        start_command=start_command,
        port=port,
        skip_build=skip_build,
    )

    # Call SDK deploy_application (only needs client!)
    result = sdk_deploy_application(config, client)

    if not result.success:
        # Build a clean, readable error message
        error_msg = result.error or "Unknown error"

        # Format error for better readability with guidance for retry
        error_response = {
            "success": False,
            "error": error_msg,
            "logs": result.logs[-5:] if result.logs else [],  # Last 5 log entries for context
            "next_action": "Check the error message and recent logs, fix the issue, then call deploy_application again with the corrected parameters.",
        }

        # Raise with a clean message
        raise ValueError(json.dumps(error_response, ensure_ascii=False, indent=2))

    return json.dumps({
        "success": True,
        "application_id": result.application_id,
        "function_id": result.function_id,
        "access_url": result.access_url,
        "console_url": result.app_console_url,
        "logs": result.logs,  # Deployment progress logs
    }, ensure_ascii=False, indent=2)


@mcp.tool(description="""Get detailed information about a specific application.

**When to use**:
- Check deployment status after `deploy_application`
- Get access_url for a deployed application
- Debug deployment issues

Args:
 - application_id: Application ID (from deploy_application result, `.vefaas/config.json`, or console)
 - region: Region (default cn-beijing)

Returns:
 - id, name, status, config, access_url, console_url
""")
def get_application_detail(application_id: str, region: Optional[str] = None):
    region = validate_and_set_region(region)

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authentication failed: {str(e)}")

    now = datetime.datetime.utcnow()
    body = {"Id": application_id}

    try:
        response = request("POST", now, {}, {}, ak, sk, token, "GetApplication", json.dumps(body), region)
        result = response.get("Result", {})

        # Extract access URL (same logic as deploy.py's extract_access_url_from_cloud_resource)
        access_url = None
        try:
            cloud_resource_str = result.get("CloudResource", "")
            if cloud_resource_str:
                cloud_resource = json.loads(cloud_resource_str)
                keys = list(cloud_resource.keys())
                if keys:
                    # Get first key's value (e.g., 'framework', 'custom', etc.)
                    data = cloud_resource[keys[0]]
                    url_obj = data.get('url', {})
                    # Prefer system_url, fallback to inner_url
                    access_url = url_obj.get('system_url') or url_obj.get('inner_url')
        except:
            pass

        # Build base response
        app_detail = {
            "id": result.get("Id"),
            "name": result.get("Name"),
            "status": result.get("Status"),
            "config": result.get("Config"),
            "region": result.get("Region"),
            "access_url": access_url,
            "console_url": f"https://console.volcengine.com/vefaas/region:vefaas+{region}/application/detail/{application_id}",
        }

        # When deployment failed, try to get detailed error info from function release status
        status = result.get("Status", "").lower()

        # Add guidance for in-progress deployments
        if status in ("deploying", "releasing", "deploy_pendding"):
            app_detail["next_action"] = "Deployment is in progress. Wait for completion or check status again later."

        if status in ("deploy_fail", "deleted", "delete_fail"):
            error_details = {}
            try:
                # Try to get function_id from CloudResource first
                function_id = None
                cloud_resource_str = result.get("CloudResource", "")
                if cloud_resource_str:
                    try:
                        cloud_resource = json.loads(cloud_resource_str)
                        keys = list(cloud_resource.keys())
                        if keys:
                            first_key = keys[0]
                            function_id = cloud_resource.get(first_key, {}).get("function_id")
                    except:
                        pass

                # Fallback: try Config
                if not function_id:
                    config_str = result.get("Config", "")
                    if config_str:
                        try:
                            config_data = json.loads(config_str)
                            function_id = config_data.get("function", {}).get("function_id")
                        except:
                            pass

                if function_id:
                    # Call GetReleaseStatus to get detailed error info
                    rel_body = {"FunctionId": function_id}
                    rel_result = request("POST", now, {}, {}, ak, sk, token, "GetReleaseStatus", json.dumps(rel_body), region)
                    rel = rel_result.get("Result", {})

                    status_msg = rel.get("StatusMessage", "").strip()
                    if status_msg:
                        error_details["error_message"] = status_msg

                    log_url = rel.get("FailedInstanceLogs", "").strip()
                    if log_url:
                        error_details["error_logs_url"] = log_url

                    error_details["function_id"] = function_id
            except Exception as ex:
                logger.debug(f"Failed to get release status error details: {ex}")

            if error_details:
                app_detail["error_details"] = error_details

        return app_detail
    except Exception as e:
        raise ValueError(f"Failed to get application details: {str(e)}")


# ==================== MCP Resources ====================

@mcp.resource("vefaas://prompts", mime_type="application/json")
def get_prompts_resource():
    return json.dumps({
        "prompts": [
            {
                "name": "vefaas_deploy_guide",
                "description": "veFaaS application deployment guide"
            },
            {
                "name": "vefaas_dev_guide",
                "description": "veFaaS function local development guide"
            }
        ],
        "usage": "Use prompts/get with the prompt name to get the full content"
    }, ensure_ascii=False, indent=2)


# ==================== MCP Prompts ====================

@mcp.prompt(description="veFaaS application deployment guide")
def vefaas_deploy_guide():
    return """# veFaaS Application Deployment Guide

## Applicable Scenarios
- Deploy local project to veFaaS cloud
- Update code for deployed applications
- First-time deployment of new applications

## Recommended Workflow

### First Deployment
1. **Detect project configuration**
   ```
   detect_project(project_path="/path/to/project")
   ```
   Get framework, runtime, start_command, port info

2. **Execute deployment**
   ```
   deploy_application(
       project_path="/path/to/project",
       name="my-app",
       start_command="<from detect_project>",
       port=<from detect_project>,
       build_command="<from detect_project, required for non-Python>"
   )
   ```

3. **View deployment result**
   On success, access_url is returned for direct access

### Redeployment/Update
If application_id exists in .vefaas/config.json, simply call:
```
deploy_application(project_path="/path/to/project")
```
The tool will auto-read config and update the application

### Common Issues
- **NAME_CONFLICT (Name exists)**: **Ask the user** to choose: 1) Update existing (use application_id) or 2) Create new (use different name)
- **start_command error**: Use detect_project to get correct command
- **Deployment failed**: Check error_details for error message and logs

## Available Tools
- detect_project: Detect project configuration
- deploy_application: One-click deployment
- get_application_detail: Get application details
"""


@mcp.prompt(description="veFaaS function local development guide")
def vefaas_dev_guide():
    return """# veFaaS Function Local Development Guide

## Applicable Scenarios
- Pull online function code to local for development
- Sync code changes to online
- Publish new function version

## Recommended Workflow

### Pull Code to Local
1. **Get function info**
   ```
   get_function_detail(function_id="xxx", region="cn-beijing")
   ```

2. **Pull code**
   ```
   pull_function_code(
       function_id="xxx",
       dest_dir="/path/to/local/folder",
       region="cn-beijing"
   )
   ```
   Code will be downloaded to specified directory with vefaas.yaml config generated

### Publish After Code Changes
1. **Upload code to function**
   ```
   update_function(
       function_id="xxx",
       project_path="/path/to/local/folder",
       region="cn-beijing"
   )
   ```

2. **Release function**
   ```
   release_function(function_id="xxx", region="cn-beijing")
   ```
   Will auto-trigger dependency installation, wait for completion, and release. Returns access link.

### Update Config Only
```
update_function(
    function_id="xxx",
    command="python -m uvicorn main:app --host 0.0.0.0 --port 8000",
    envs={"DEBUG": "true"}
)
release_function(function_id="xxx")
```

## Available Tools
- get_function_detail: Get function details
- pull_function_code: Pull function code
- update_function: Update function code/config
- release_function: Release function (auto dependency install + status polling)

## Notes
- function_id can be found in vefaas.yaml or console
- To delete functions, use console: https://console.volcengine.com/vefaas
"""
