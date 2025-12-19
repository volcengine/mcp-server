import fnmatch
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

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("veFaaS MCP Server",
              host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
              port=int(os.getenv("MCP_SERVER_PORT", "8000")),
              stateless_http=os.getenv("STATLESS_HTTP", "true").lower() == "true",
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))

TemplateIdForRegion = {
    "ap-southeast-1": "6943ba21735f270008330d1c",
    "cn-beijing": "68d24592162cb40008217d6f",
    "cn-shanghai": "6943b9de4fa45c0008ea04e1",
    "cn-guangzhou": "6943b95bc69585000819d70f",
}

def validate_and_set_region(region: str = None) -> str:
    """
    Validates the provided region and returns the default if none is provided.

    Args:
        region: The region to validate

    Returns:
        A valid region string

    Raises:
        ValueError: If the provided region is invalid
    """
    valid_regions = ["ap-southeast-1", "cn-beijing", "cn-shanghai", "cn-guangzhou"]
    if region:
        if region not in valid_regions:
            raise ValueError(f"Invalid region. Must be one of: {', '.join(valid_regions)}")
    else:
        region = "cn-beijing"
    return region

@mcp.tool(description="""Create a veFaaS Application.

Args:
 - function_id: vefaas function id.
 - function_name: vefaas function name.
 - gateway_name: api gateway name (Name from tool `fetch_running_api_gateway`).

Note:
 - Applications bind the function to an API gateway as the top-level delivery unit.
 - Creation automatically submits an application release; capture the returned `application_id`.
 - On success, append `application_id` to `vefaas.yaml` immediately.

**CRITICAL REQUIREMENT**:
 - Invoke **ONLY AFTER** the current workflow has just run `create_function`; otherwise reuse the existing application.
 - If need to create a new application, follow these steps:
   - Step 1: List templates via `list_vefaas_application_templates`.
   - Step 2: Pull details/code with `get_vefaas_application_template` if a template fits.
   - Step 3: Create the veFaaS function and confirm its release succeeded.
   - Step 4: Ensure a running API gateway is ready.
   - Step 5: Create the application with `create_vefaas_application`.
 - On success, immediately call `poll_vefaas_application_status` until deployment finishes (success or fail, max three polls). If creation fails or raises, stop and surface the error instead of polling.

Error Handle Tips:
 - If there is **any authentication** error about vefaas application(create/release/get), let user apply auth by link: https://console.volcengine.com/iam/service/attach_custom_role?ServiceName=vefaas&policy1_1=APIGFullAccess&policy1_2=VeFaaSFullAccess&role1=ServerlessApplicationRole, then retry.

""")
def create_vefaas_application(function_id: str, function_name: str, gateway_name: str, region: Optional[str] = None):
    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    # check apig trigger whether exist
    try:
        triggers = list_function_triggers(function_id, region).get("Result", {}).get("Items", [])
        if any(trigger.get("Type") == "apig" for trigger in triggers):
            return f"APIGateway trigger already exists for function {function_name}, skip create application"
    except Exception as e:
        raise ValueError(f"Failed to list function triggers: {str(e)}")

    region = validate_and_set_region(region)

    applicationName = (append_random_suffix(function_name, 3) + "-app").lower()

    body = {
        "Name": applicationName,
        "Config": {
            "FunctionName": function_name,
            "GatewayName": gateway_name,
            "Region": region,
        },
        "TemplateId": TemplateIdForRegion.get(region, "68d24592162cb40008217d6f"),
    }

    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateApplication", json.dumps(body), region)
    except Exception as e:
        raise ValueError(f"Failed to create application: {str(e)}")

    result = {}
    if isinstance(response_body, dict):
        result = response_body.get("Result") or {}
    application_id = result.get("Id")
    if not application_id:
        raise ValueError(f"Failed to determine application ID from create response. response_body: {response_body}")

    release_body = {"Id": application_id}
    try:
        release_response = request("POST", datetime.datetime.utcnow(), {}, {}, ak, sk, token, "ReleaseApplication", json.dumps(release_body), region)
    except Exception as e:
        raise ValueError(f"Failed to release application: {str(e)}")

    payload = {
        "application_id": application_id,
        "create_application": response_body,
        "release_application": release_response,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)

@mcp.tool(description="""Get veFaaS Application deployment status.

Args:
 - application_id: vefaas application_id.

Note:
 - Application deployment status is independent of function releases.
 - Call after `create_vefaas_application` (which auto-submits release) to monitor progress.
 - When it finishes, **MUST** report application_id, region, status, access_url, and app_platform_url derived from the response.

**CRITICAL REQUIREMENT**:
 - Do not use alternative methods to check application deployment status—only this tool.
 - Poll immediately after `create_vefaas_application` returns (release is auto-submitted) and stop once you see `deploy_success` or `deploy_fail`, with at most three attempts.
 - If it is a **streamlit type** application (will contain "streamlit" in the function_name or application_name), **MUST** update the `access_url` to function envs and release function again after application deployment finished.
    - Detail step:
        - 1. Use tool `update_function`, add environment STREAMLIT_BROWSER_SERVER_ADDRESS=`access_url` to param envs.
        - 2. Call tool `release_function` and `poll_function_release_status` to check if the streamlit application is redeployed successfully.

""")
def poll_vefaas_application_status(application_id: str, region: Optional[str] = None):
    region = validate_and_set_region(region)
    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    body = {
        "Id": application_id,
    }
    timeout = 120
    polling_interval = 5
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = request("POST", now, {}, {}, ak, sk, token, "GetApplication", json.dumps(body), region)
            if response["Result"] is not None:
                result = response["Result"]
                status = result.get("Status")
        except Exception as e:
            status = None

        if status == "deploying" or status == None:
            time.sleep(polling_interval)
            continue
        else:
            break

    errLogs: list[str] = []
    hasAuthError = False
    if status == "deploy_fail":
        try:
            revision_number = result.get("NewRevisionNumber")
            if revision_number:
                logQueryBody = {
                    "Id": application_id,
                    "Limit": 99999,
                    "RevisionNumber": revision_number,
                }
                logResponse = request("POST", now, {}, {}, ak, sk, token, "GetApplicationRevisionLog", json.dumps(logQueryBody), region)
                log_result = logResponse.get("Result")
                if log_result:
                    logLines = log_result.get("LogLines", [])
                    for logLine in logLines:
                        if "warn" in logLine.lower() or "error" in logLine.lower() or "fail" in logLine.lower():
                            errLogs.append(logLine)
                        if "not authorized" in logLine.lower() or "cannot get sts token" in logLine.lower():
                            errLogs.append(logLine)
                            hasAuthError = True
            if hasAuthError:
                errLogs.append("Failed to release application due to an authentication error. Please visit https://console.volcengine.com/iam/service/attach_custom_role?ServiceName=vefaas&policy1_1=APIGFullAccess&policy1_2=VeFaaSFullAccess&role1=ServerlessApplicationRole to grant the required permissions and then try again.")
        except Exception as e:
            logger.error(f"Failed to get application log: {str(e)}")

    # get system_url
    system_url = ""
    try:
        cloud_resource = json.loads(result["CloudResource"])
        system_url = cloud_resource['framework']['url']['system_url']
    except Exception as e:
        logger.error(f"Failed to get system_url: {str(e)}")

    responseInfo = {
        "Id": result["Id"],
        "Name": result["Name"],
        "Status": result["Status"],
        "Config": result["Config"],
        "Region": result["Region"],
        "AccessUrl": system_url,
        "AppPlatformUrl": f"https://console.volcengine.com/vefaas/region:vefaas+{region}/application/detail/{application_id}?tab=detail",
        "NewRevisionNumber": result.get("NewRevisionNumber"),
    }
    if len(errLogs) > 0:
        responseInfo["DeployFailedLogs"] = errLogs

    return responseInfo


@mcp.tool(description="""Create a veFaaS function.

Args:
 - name: function name (unique, with a 6 length lowercase random string).
 - runtime: function runtime.
 - command: function startup script (./run.sh by default).
 - region: function region. (`cn-beijing` by default)

Note:
 - runtime must be `native-python3.12/v1`, `native-node20/v1`, or `native/v1` (defaults to `native-python3.12/v1` if omitted).
 - command must be a runnable script (default `./run.sh`).
 - region defaults to `cn-beijing` and must be one of `cn-beijing`, `cn-shanghai`, `cn-guangzhou`, `ap-southeast-1`.
 - `enable_vpc=true` requires `vpc_id`, `subnet_ids`, and `security_group_ids`.
 - Startup scripts must invoke tooling via `python -m <module>` (e.g., `python -m uvicorn ...`); direct CLI binaries such as `uvicorn` or `gunicorn` are not on PATH—apply the same rule for any missing CLI: use `python -m <module>` or launch it from code.
 - When bootstrapping a new workload (e.g., React service), review official templates via `list_vefaas_application_templates` and `get_vefaas_application_template` first so code and configs inherit veFaaS conventions.
 - Review the `upload_code` checklist before preparing artifacts or startup scripts.
 - After work completes, surface function_id, name, region, runtime, and platform link if available from context.
    - veFaaS platform link template: https://console.volcengine.com/vefaas/region:vefaas+`region`/function/detail/`function_id`?tab=config

Error Handle Tips:
 - If there is **any authentication** error about vefaas function(like create/release/get), let user to apply auth by this link https://console.volcengine.com/iam/service/attach_role/?ServiceName=vefaas, then retry.

**CRITICAL REQUIREMENT**:
 - If `vefaas.yaml` already holds a valid `function_id`, reuse it and skip this tool.
 - On success, write `function_id`, `name`, `region`, `runtime`, `command` to `vefaas.yaml`, vefaas.yaml should be created in the **project root directory**.
 - Then execute in order:
   - Step 0 (for new services without an existing template choice): call `list_vefaas_application_templates`, pick a template, and pull its source via `get_vefaas_application_template` to guide code changes before uploading.
   - Step 1: Run `upload_code` (per its checklist; required for TOS sources).
   - Step 2: Call `release_function` once upload completes when release is needed.
   - Step 3: Fetch a running API gateway.
 - Step 4: Create the veFaaS application (this tool auto-releases). Only if creation succeeds, poll deployment status via `poll_vefaas_application_status`; otherwise surface the failure.

""")
def create_function(name: str = None, region: str = None, runtime: str = None, command: str = None, source: str = None,
                    image: str = None, envs: dict = None, description: str = None, enable_vpc = False,
                    vpc_id: str = None, subnet_ids: List[str] = None, security_group_ids: List[str] = None,) -> str:
    # Validate region
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    if enable_vpc and (not vpc_id or not subnet_ids or not security_group_ids):
        raise ValueError("vpc_id or subnet_ids and security_group_ids must be provided.")

    def build_create_request(current_name: str) -> volcenginesdkvefaas.CreateFunctionRequest:
        request_obj = volcenginesdkvefaas.CreateFunctionRequest(
            name=current_name,
            runtime=runtime if runtime else "native-python3.12/v1",
        )

        if image:
            request_obj.source = image
            request_obj.source_type = "image"

        if command:
            request_obj.command = command

        if source:
            if ":" not in source:
                source_type = "zip"
            elif source.count(":") == 1 and "/" not in source:
                source_type = "tos"
            elif "/" in source and ":" in source:
                source_type = "image"
            else:
                source_type = None

            request_obj.source = source
            if source_type:
                request_obj.source_type = source_type

        if envs:
            env_list = [{"key": key, "value": value} for key, value in envs.items()]
            request_obj.envs = env_list

        if enable_vpc:
            vpc_config = volcenginesdkvefaas.VpcConfigForUpdateFunctionInput(
                enable_vpc=True, vpc_id=vpc_id, subnet_ids=subnet_ids, security_group_ids=security_group_ids,
            )
            request_obj.vpc_config = vpc_config

        if description:
            request_obj.description = description

        return request_obj

    base_name = name if name else generate_random_name()
    current_name = base_name
    used_names = {current_name}
    max_attempts = 5
    attempt = 0

    while attempt < max_attempts:
        request_obj = build_create_request(current_name)
        try:
            response = api_instance.create_function(request_obj)
            return f"Successfully created veFaaS function with name {current_name} and id {response.id}"
        except ApiException as e:
            if "need to create a service-linked role for vefaas" in str(e).lower() or "no auth" in str(e).lower() or "not authorized" in str(e).lower():
                raise ValueError("You need to create a service-linked role for veFaaS. Please visit https://console.volcengine.com/iam/service/attach_role/?ServiceName=vefaas to grant the required permissions and then try again.")
            if is_name_conflict_error(e):
                attempt += 1
                next_name = append_random_suffix(base_name)
                while next_name in used_names:
                    next_name = append_random_suffix(base_name)
                used_names.add(next_name)
                logger.info(
                    "Function name '%s' already exists. Retrying with '%s' (attempt %s/%s)",
                    current_name,
                    next_name,
                    attempt,
                    max_attempts,
                )
                current_name = next_name
                continue

            error_message = f"Failed to create veFaaS function: {str(e)}"
            raise ValueError(error_message)

    raise ValueError("Failed to create veFaaS function: exhausted name retries due to conflicts.")


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

@mcp.tool(description="""Update a veFaaS function's referenced artifact or runtime settings.

Args:
- function_id: ID of the function to update.
- source: Optional new artifact to use (base64 zip, TOS object, container image).
- region: Optional region to update the function in (supports 'ap-southeast-1', 'cn-beijing', 'cn-shanghai', 'cn-guangzhou').
- command: Optional new command to run.
- envs: Optional new environment variables as key-value pairs.
- enable_vpc: Optional flag to enable VPC networking.
- vpc_id: Optional VPC ID if VPC is enabled.
- subnet_ids: Optional list of subnet IDs if VPC is enabled.
- security_group_ids: Optional list of security group IDs if VPC is enabled.

Note:
- Use to swap in an existing artifact (base64 zip/TOS/image) or update command/env/VPC fields; for fresh local edits prefer `upload_code`.
- When passing `source`, ensure the artifact already exists and matches the inferred source_type (zip/tos/image).
- For VPC updates set `enable_vpc=true` and include `vpc_id`, `subnet_ids`, and `security_group_ids`.

""")
def update_function(function_id: str, source: str = None, region: str = None, command: str = None,
                    envs: dict = None, enable_vpc = False, vpc_id: str = None, subnet_ids: List[str] = None,
                    security_group_ids: List[str] = None,):

    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    update_request = volcenginesdkvefaas.UpdateFunctionRequest(
            id=function_id,
        )

    source_type = None

    if source:
        # Determine source type based on the format
        if ":" not in source:
            # If no colon, assume it's a base64 encoded zip
            source_type = "zip"
        elif source.count(":") == 1 and "/" not in source:
            # Format: bucket_name:object_key
            source_type = "tos"
        elif "/" in source and ":" in source:
            # Format: host/namespace/repo:tag
            source_type = "image"
        # else:
        #     raise ValueError(
        #         "Invalid source format. Must be one of: base64 zip, bucket_name:object_key, or host/namespace/repo:tag"
        #     )

        update_request.source = source
        update_request.source_type = source_type

    if command != "":
        update_request.command = command

    if envs:
        env_list = []
        for key, value in envs.items():
            env_list.append({
                "key": key,
                "value": value
            })
        update_request.envs = env_list

    if enable_vpc:
        if not vpc_id or not subnet_ids or not security_group_ids:
            raise ValueError("vpc_id or subnet_ids and security_group_ids must be provided.")
        vpc_config = volcenginesdkvefaas.VpcConfigForUpdateFunctionInput(
            enable_vpc=True, vpc_id=vpc_id, subnet_ids=subnet_ids, security_group_ids=security_group_ids,
        )
        update_request.vpc_config = vpc_config

    try:
        response = api_instance.update_function(update_request)
        return f"Successfully updated function {function_id} with source type {source_type}"
    except ApiException as e:
        error_message = f"Failed to update veFaaS function: {str(e)}"
        raise ValueError(error_message)

@mcp.tool(description="""Release(Deploy) the latest code/configs to a veFaaS Function.

Args:
- function_id: ID of the function to release.
- region: The region of the veFaaS function.

Note:
 - Submits the release job; the function is not live until polling reports success.

**CRITICAL REQUIREMENT**:
- Use only when new code or config is ready to publish. If code changed, wait for `upload_code` (including dependency install tasks) to finish; config-only changes can proceed immediately.
- After submission, call `poll_function_release_status` until it returns Succeeded/Failed, and invoke that poll tool no more than three times.

""")
def release_function(function_id: str, region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    try:
        logger.info("Release uses the last artifact uploaded via upload_code/update_function; ensure that step has completed successfully before calling release.")
        req = volcenginesdkvefaas.ReleaseRequest(
            function_id=function_id, revision_number=0
        )
        response = api_instance.release(req)
        return (
            "Release request submitted for function "
            f"{function_id}. Poll 'poll_function_release_status' until it reports Succeeded/Failed."
        )
    except ApiException as e:
        error_message = f"Failed to release veFaaS function: {str(e)}"
        raise ValueError(error_message)

@mcp.tool(description="""Delete a veFaaS function.

Args:
- function_id: ID of the function to delete.
- region: The region of the veFaaS function.

Note:
 - Use this when asked to delete, remove, or uninstall a veFaaS function.

""")
def delete_function(function_id: str, region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    try:
        req = volcenginesdkvefaas.DeleteFunctionRequest(
            id=function_id
        )
        response = api_instance.delete_function(req)
        return f"Successfully deleted function {function_id}"
    except ApiException as e:
        error_message = f"Failed to delete veFaaS function: {str(e)}"
        raise ValueError(error_message)

def get_function_release_status(function_id: str, region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    req = volcenginesdkvefaas.GetReleaseStatusRequest(
        function_id=function_id
    )
    response = api_instance.get_release_status(req)
    if response.status == "inprogress":
        time.sleep(10)
    return response


@mcp.tool(description="""Check veFaaS function release status.

Args:
- function_id: ID of the function to check release status.
- region: The region of the veFaaS function.

Note:
- If failed: inspect status/errors, resolve, then rerun 'upload_code' -> 'release_function' procedure once fixes are in place.
   - A frequent error is `bash: uvicorn: command not found`; switch startup scripts to `python -m uvicorn main:app --host 0.0.0.0 --port 8000` (or launch the server in code) per the `upload_code` guidance—apply the same rule for any missing CLI.

**CRITICAL REQUIREMENT**:
 - Can **only** use this tool to check vefaas function release status, **NEVER** try to get release status by other ways.
 - When it finishes, **MUST** report: function_id, region, release_status, vefaas_function_access_link and vefaas_function_platform_url derived from the response.
""")
def poll_function_release_status(function_id: str, region: str = None):
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
        "vefaas_function_platform_url": f"https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}?tab=config",
        "vefaas_function_access_link": get_function_access_link(function_id, region),
    }
    return responseInfo

def get_function_access_link(function_id: str, region: str = None):
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
    region = region if region is not None else "cn-beijing"
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

def create_api_gateway(name: str = None, region: str = "cn-beijing"):
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

@mcp.tool(description="""Fetch a running API Gateway ID.

Args:
 - region: The region to fetch the gateway for.

Note:
 - Returns a running API gateway to feed into `create_vefaas_application`; creates one and waits if none are ready.
 - On failure, retry up to three times before surfacing the error.
 - Use the returned gateway's `Name` directly when calling `create_vefaas_application`, and expect new gateways to take a few minutes to reach `Running`.
""")

def fetch_running_api_gateway(region: str = None):
    region = validate_and_set_region(region)

    try:
        existing_gateways = list_existing_api_gateways(region)
        running_gateways = [gw for gw in existing_gateways if gw["Status"] == "Running"]
        if len(running_gateways) > 0:
            return random.choice(running_gateways)

        timeout = 180
        interval = 5
        start_time = datetime.datetime.utcnow()
        create_api_gateway_failed_times = 0
        while (datetime.datetime.utcnow() - start_time).total_seconds() < timeout:
            existing_gateways = list_existing_api_gateways(region)
            running_gateways = [gw for gw in existing_gateways if gw["Status"] == "Running"]
            if len(running_gateways) > 0:
                return random.choice(running_gateways)

            pending_gateways = [gw for gw in existing_gateways if gw["Status"] == "Creating"]
            if len(pending_gateways) > 0:
                logger.info(f"Waiting for gateway to be running: {pending_gateways}")
                time.sleep(interval)
                continue

            try:
                create_api_gateway(region=region)
                time.sleep(interval)
            except Exception as e:
                logger.error(f"Failed to create API Gateway: {str(e)}")
                create_api_gateway_failed_times += 1
                if create_api_gateway_failed_times >= 3:
                    raise Exception(f"Failed to create API Gateway after {create_api_gateway_failed_times} times")
                time.sleep(interval)
    except Exception as e:
        raise Exception(f"Failed to fetch an running API Gateway: {str(e)}")

    raise Exception(f"Failed to fetch an running API Gateway after {timeout} seconds")

def ensure_executable_permissions(folder_path: str):
    for root, _, files in os.walk(folder_path):
        for fname in files:
            full_path = os.path.join(root, fname)
            if fname.endswith('.sh') or fname in ('run.sh',):
                os.chmod(full_path, 0o755)

def zip_and_encode_folder(folder_path: str, local_folder_exclude: List[str]) -> Tuple[bytes, int, Exception]:
    """
    Zips a folder with system zip command (if available) or falls back to Python implementation.
    Returns (zip_data, size_in_bytes, error) tuple.
    """
    # Check for system zip first
    if not shutil.which('zip'):
        logger.info("System zip command not found, using Python implementation")
        try:
            data = python_zip_implementation(folder_path, local_folder_exclude)
            return data, len(data), None
        except Exception as e:
            return None, 0, e

    logger.info("Zipping folder: %s", folder_path)
    try:
        ensure_executable_permissions(folder_path)
        # Base zip command
        cmd = ['zip', '-r', '-q', '-', '.', '-x', '*.git*', '-x', '*.venv*', '-x', '*__pycache__*', '-x', '*.pyc']

        # Append user-specified exclude patterns
        if local_folder_exclude:
            for pattern in local_folder_exclude:
                cmd.extend(['-x', pattern])
        logger.debug("Zip command: %s", cmd)

        # Create zip process with explicit arguments
        proc = subprocess.Popen(
            cmd,
            cwd=folder_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1024 * 8  # 8KB buffer
        )

        # Collect output with proper error handling
        try:
            stdout, stderr = proc.communicate(timeout=30)
            if proc.returncode != 0:
                logger.error("Zip error: %s", stderr.decode())
                data = python_zip_implementation(folder_path, local_folder_exclude)
                return data, len(data), None

            if stdout:
                size = len(stdout)
                logger.info("Zip finished, size: %.2f MB", size / 1024 / 1024)
                return stdout, size, None
            else:
                logger.warning("zip produced no data; falling back to Python implementation")
                data = python_zip_implementation(folder_path, local_folder_exclude)
                return data, len(data), None

        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)  # Give it 5 seconds to cleanup
            logger.warning("zip process timed out; falling back to Python implementation")
            try:
                data = python_zip_implementation(folder_path, local_folder_exclude)
                return data, len(data), None
            except Exception as e:
                return None, 0, e

    except Exception as e:
        logger.error("System zip error: %s", str(e))
        try:
            data = python_zip_implementation(folder_path, local_folder_exclude)
            return data, len(data), None
        except Exception as e2:
            return None, 0, e2

def python_zip_implementation(folder_path: str, local_folder_exclude: List[str] = None) -> bytes:
    """Pure Python zip implementation with permissions support"""
    buffer = BytesIO()

    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)

                # Skip excluded paths and binary/cache files
                if any(excl in arcname for excl in ['.git', '.venv', '__pycache__', '.pyc']):
                    continue
                if local_folder_exclude and any(fnmatch.fnmatch(arcname, pattern) for pattern in local_folder_exclude):
                    continue

                try:

                    st = os.stat(file_path)
                    dt = datetime.datetime.fromtimestamp(st.st_mtime)
                    date_time = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

                    info = zipfile.ZipInfo(arcname)
                    info.external_attr = (0o755 << 16)  # rwxr-xr-x
                    info.date_time = date_time

                    with open(file_path, 'rb') as f:
                        zipf.writestr(info, f.read())
                except Exception as e:
                    logger.warning("Skipping file %s due to error: %s", arcname, str(e))

    logger.info("Python zip finished, size: %.2f MB", buffer.tell() / 1024 / 1024)
    return buffer.getvalue()

def _get_upload_code_description() -> str:
    """Generate a concise, dynamic description for the `upload_code` tool."""
    base_desc = (
        "Upload function code to TOS.\n\n"
        "Args:\n"
        " - function_id: The ID of the function to upload code for.\n"
        " - region: The region of the function.\n"
        " - local_folder_path: The path to the local folder containing the code to upload.\n"
        " - local_folder_exclude: Optional list of patterns to exclude from the upload (e.g., ['.venv', 'node_modules', '.git', '*.pyc']).\n"
        " - file_dict: {filename -> content}\n\n"

        "Returns:\n"
        "- 'code_upload_callback'\n"
        "- 'dependency': {dependency_task_created, should_check_dependency_status, skip_reason?}\n\n"

        "**Code & Runtime Checklist (follow before uploading):**\n"
        " - Provide an executable startup script that launches the service; skip compile or dependency install commands.\n"
        " - Pre-build Linux-compatible binaries for compiled languages and invoke them directly from the startup script.\n"
        " - Python/Node dependencies belong in 'requirements.txt' or 'package.json'; never ship virtualenvs or 'node_modules'.\n"
        " - HTTP servers must bind to 0.0.0.0:8000 and include required templates/static assets in the package.\n"
        " - CLI tooling is not on PATH—call Python modules with 'python -m <module>' (e.g., 'python -m uvicorn main:app --host 0.0.0.0 --port 8000') or start the server directly in code; apply the same rule for any missing CLI.\n"
        " - Exclude local build artifacts and dependency folders (e.g., '.venv', 'site-packages', 'node_modules', '.git') via 'local_folder_exclude'.\n\n"
    )

    # Detect run mode via FASTMCP_* environment variables.
    is_network_transport = os.getenv("FASTMCP_STATELESS_HTTP") == "true" or os.getenv("FASTMCP_HOST") or os.getenv("FASTMCP_PORT")

    if is_network_transport:
        note = (
            "Note: Running over network transport; local file system is not accessible.\n"
            " - Use 'file_dict'; 'local_folder_path' is ignored.\n\n"
        )
    else:
        note = (
            "Note: Running locally via STDIO; 'local_folder_path' is recommended.\n\n"
        )

    tail = (
        "After upload: dependency install (if any) runs asynchronously; if triggered, you MUST call 'poll_dependency_install_task_status' to poll until Succeeded/Failed."
    )

    return base_desc + note + tail

@mcp.tool(description=_get_upload_code_description())
def upload_code(function_id: str, region: Optional[str] = None, local_folder_path: Optional[str] = None,
                local_folder_exclude: Optional[List[str]] = None,
                file_dict: Optional[dict[str, Union[str, bytes]]] = None) -> str:
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    if local_folder_path:
        data, size, error = zip_and_encode_folder(local_folder_path, local_folder_exclude)
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

@mcp.tool(description="""Check dependency install task status (paired with 'upload_code').

Args:
- function_id: ID of the veFaaS function whose dependency task you are checking.
- region: Region of the function (defaults to `cn-beijing` when omitted).

Note:
 - Call only after `upload_code` reports that a dependency install task was created.
 - If status is `Failed`, download the provided log URL, fix issues (dependency specs, etc.), then rerun `upload_code`.
""")
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
                resp = requests.get(url, timeout=30)
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

    response = requests.put(url=upload_url, data=zip_bytes, headers=headers)
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
# Use this to retrieve function detail information for a veFaaS function. This function returns the function details
# Params:
# - function_id (required): the ID of the function
# - region (optional): deployment region, defaults to cn-beijing
def get_function_detail(function_id: str, region: Optional[str] = None):
    """Get function information to check if it exists."""
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    req = volcenginesdkvefaas.GetFunctionRequest(id=function_id)

    try:
        response = api_instance.get_function(req)
        return response
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
        response = requests.get(source_location)
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
            function_detail = get_function_detail(function_id, region)
            triggers = list_function_triggers(function_id, region).get("Result", {}).get("Items", [])
            with open(vefaas_yml_path, "w") as f:
                f.write(f"function_id: {function_id}\n")
                f.write(f"name: {function_detail.name}\n")
                f.write(f"region: {region}\n")
                f.write(f"runtime: {function_detail.runtime}\n")
                f.write(f"command: {function_detail.command}\n")
                f.write(f"vefaas_function_platform: https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}?tab=config\n")
                f.write(f"vefaas_access_link: {get_function_access_link(function_id, region)}\n")
                f.write(f"triggers:\n")
                for trigger in triggers:
                    f.write(f"  - id: {trigger.get('Id', '')}\n")
                    f.write(f"    type: {trigger.get('Type', '')}\n")
                    f.write(f"    name: {trigger.get('Name', '')}\n")
        except Exception as e:
            logger.error(f"Failed to write vefaas.yaml for function {function_id}: {str(e)}")
            return e

        return {
            "function_id": function_id,
            "revision": target_revision,
            #"source_location": source_location,
        }

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

@mcp.tool(description="""List veFaaS application templates.

Args:
 - page_number: Page index (default 1).
 - page_size: Page size (default 100).

Note:
 - Run before creating an application to discover available templates and read their descriptions.
 - Returns only templates that are enabled.
 - Capture the chosen template's `id` and call `get_vefaas_application_template` to download its source.
""")
def list_vefaas_application_templates(page_number: int = 1, page_size: int = 100):
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    now = datetime.datetime.utcnow()
    body = {
        "PageNumber": page_number,
        "PageSize": page_size,
    }
    try:
        resp = request(
            "POST", now, {}, {}, ak, sk, token, "ListApplicationTemplates", json.dumps(body), None, 5,
        )

    except Exception as e:
        raise ValueError(f"Failed to list application templates: {str(e)}")

    result = []
    for item in resp.get("Result", {}).get("Items", []):
        if item.get("EnableTemplate", False):
            result.append({
            "name": item.get("Name", ""),
            "id": item.get("Id", ""),
            "description": item.get("Description", ""),
        })

    # TODO: dirty code, remove this
    # get function templates for streamlit
    try:
        func_body = {
            "PageNumber": page_number,
            "PageSize": page_size,
            "Filters": [{
                "Item": {
                    "Key": "SourceType",
                    "Value": ["function"],
                }
            }]
        }
        func_resp = request("POST", now, {}, {}, ak, sk, token, "ListTemplates", json.dumps(func_body), None, 5)
        func_items = func_resp.get("Result", {}).get("Items", [])
        for item in func_items:
            if item.get("Name", "") == "vefaas-native-streamlit":
                result.append({
                "name": item.get("Name", ""),
                "id": item.get("Id", ""),
                "description": item.get("Description", ""),
            })
    except Exception as e:
        logger.error(f"Failed to list function templates: {str(e)}")

    return result

@mcp.tool(description="""Download a veFaaS application template.

Args:
 - template_id: Template ID from `list_vefaas_application_templates`.
 - destination_dir: Directory to extract the template contents into.

Note:
 - Download the archive and extract files; do not persist the zip itself.
 - Reuse or clean `destination_dir` before repeated downloads to avoid partial overwrite issues.
""")
def get_vefaas_application_template(template_id: str, destination_dir: str):
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    now = datetime.datetime.utcnow()
    body = {"Id": template_id}

    # TODO: dirty code, remove this. Adapt streamlit template.
    if template_id == "68f9cd2474c2090008469163":
        try:
             resp = request(
                "POST", now, {}, {}, ak, sk, token, "GetTemplateDetail", json.dumps(body), None, 20,
            )
        except Exception as e:
            raise ValueError(f"Failed to get application template detail: {str(e)}")
    else:
        try:
            resp = request(
                "POST", now, {}, {}, ak, sk, token, "GetApplicationTemplateDetail", json.dumps(body), None, 20,
            )
        except Exception as e:
            raise ValueError(f"Failed to get application template detail: {str(e)}")

    try:
        source_location = resp.get("Result", {}).get("SourceLocation")
        if not source_location:
            raise ValueError("SourceLocation not found in the template detail response.")

        # Download the template zip file
        response = requests.get(source_location)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Determine the destination directory

        # Create destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Unzip the file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(destination_dir)

        return f"Template {template_id} downloaded and extracted to {destination_dir}"

    except Exception as e:
        raise ValueError(f"Failed to download and extract application template: {str(e)}")

@mcp.prompt(name="deploy_vefaas", title="""deploy veFaaS function""")
def deploy_vefaas(
    function_id: str,
    region: str = "cn-beijing",
    local_folder_path: Optional[str] = None,
    local_folder_exclude: Optional[List[str]] = None,
    code_source_hint: Optional[str] = None,
):
    """
    Generate deployment instructions for a veFaaS function.

    Args:
        function_id: Target veFaaS function ID.
        region: Deployment region (defaults to cn-beijing).
        local_folder_path: Local path to upload (if using filesystem upload).
        local_folder_exclude: Patterns to exclude during upload.
        code_source_hint: Free-form context about where updated code lives (optional).
    """
    folder_hint = f"Use `local_folder_path={local_folder_path!r}`" if local_folder_path else "Provide `local_folder_path` pointing at the prepared project root"
    exclude_hint = (
        f"`local_folder_exclude={local_folder_exclude!r}`"
        if local_folder_exclude
        else "Set `local_folder_exclude` to skip noise (e.g., ['.venv', 'node_modules', '.git', '*.pyc'])"
    )
    extra_hint = f"Context: {code_source_hint}\n" if code_source_hint else ""

    instructions = "\n".join(
        [
            f"{extra_hint}Deploy veFaaS function `{function_id}` in `{region}`.",
            "Tool names might include prefixes (e.g., `vefaas__upload_code`, `vefaas__release_function`); invoke whichever variant ends with the base name shown below.",
            f"1. Call `upload_code` ({folder_hint}; {exclude_hint}) and follow its checklist.",
            "2. If the response sets `dependency.dependency_task_created = true`, poll `poll_dependency_install_task_status` until it finishes (stop after three tries, surface logs on failure).",
            f"3. When upload (and dependency install) is done, call `release_function` for `{function_id}` / `{region}`.",
            "4. Immediately poll `poll_function_release_status` until it returns Succeeded/Failed (max three polls); report the outcome, platform URL, or errors before retrying.",
        ]
    )

    return [instructions]
