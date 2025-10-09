import fnmatch
import io
from pdb import run
from typing import Required, Union, Optional, List
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

SUPPORTED_RUNTIMES = [
    "native-python3.12/v1",
    "native-node20/v1",
    "native/v1",
]

TemplateIdForRegion = {
    "ap-southeast-1": "68d24592162cb40008217d6f",
    "cn-beijing": "68d24592162cb40008217d6f",
    "cn-shanghai": "68d24592162cb40008217d6f",
    "cn-guangzhou": "68d24592162cb40008217d6f",
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
 - function_name: vefaas function name.
 - gateway_name: vefaas function api gateway name (gateway_name from create_api_gateway or list_api_gateways).
 - gateway_service_name: vefaas function api gateway service name (service_name from create_api_gateway_service).
 - upstream_name: vefaas function api gateway trigger name (upstream_name from create_api_gateway_trigger).

Note:
 - veFaaS Application is the top-level collection that contains veFaaS function, api-gateway and other production.
 - After all steps done, provide veFaaS Application infos like application_id, name, region and platform link if these info can get from context directly.
    - veFaaS platform link template: https://console.volcengine.com/vefaas/region:vefaas+`region`/application/detail/`application_id`?tab=detail

Error Handle Tips:
 - If there is **any authentication** error about vefaas application(create/release/get), let user apply auth by link: https://console.volcengine.com/iam/service/attach_custom_role?ServiceName=vefaas&policy1_1=APIGFullAccess&policy1_2=VeFaaSFullAccess&role1=ServerlessApplicationRole, then retry.

**CRITICAL REQUIREMENT**
- This tool **CAN ONLY** be called if `create_function` tool be called in previous step.
- If user want to create a veFaaS Application, **MUST** follow the steps:
 1. Use `list_vefaas_application_templates` to get all available templates.
 2. Find most suitable template from all the templates and use `get_application_template_detail` to get template code.
 3. Create/Release vefaas function and create api-gateway trigger.
 4. Create/Release vefaas application.
- MUST EDIT vefaas.yml: Add application_id to `vefaas.yml` immediately after application created successfully.

""")
def create_vefaas_application(function_name: Required[str], gateway_name: Required[str], gateway_service_name: Optional[str] = None, 
        upstream_name: Optional[str] = None, region: Optional[str] = None):
    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    region = validate_and_set_region(region)

    applicationName = append_random_suffix(function_name, 3) + "-app"

    body = {
        "Name": applicationName,
        "Config": {
            "FunctionName": function_name,
            "GatewayName": gateway_name,
            "ServiceName": gateway_service_name,
            "UpstreamName": upstream_name,
        },
        "TemplateId": TemplateIdForRegion.get(region, "68d24592162cb40008217d6f"),
    }

    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateApplication", json.dumps(body), region)
    except Exception as e:
        raise ValueError(f"Failed to create application: {str(e)}")

    return response_body

@mcp.tool(description="""Release a veFaaS Application.

Args:
 - application_id: vefaas application_id.

Note:
 - After release succeed, start poll `get_vefaas_application` tool to check application deployment status.
 - If release failed, let user check the error log from `get_vefaas_application`.

**CRITICAL REQUIREMENT**
  - Stop poll `get_vefaas_application` tool when deploy_success or deploy_fail
  - Poll every 3 seconds to avoid loop detection, up to 3 minutes.
""")
def release_vefaas_application(application_id: Required[str], region: Optional[str] = None):
    region = validate_and_set_region(region)

    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")
    
    body = {
        "Id": application_id,
    }
    
    try:
        response = request("POST", now, {}, {}, ak, sk, token, "ReleaseApplication", json.dumps(body), region)
        return response
    except Exception as e:
        raise ValueError(f"Failed to release application: {str(e)}")

@mcp.tool(description="""Get veFaaS Application information.

Args:
 - application_id: vefaas application_id.

Note:
 - veFaaS Application status **NOT** related to veFaaS function release status.
 - Usually use this tool to check application deployment status after release.

""")
def get_vefaas_application(application_id: Required[str], region: Optional[str] = None):
    region = validate_and_set_region(region)

    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")
    
    body = {
        "Id": application_id,
    }
    
    try:
        response = request("POST", now, {}, {}, ak, sk, token, "GetApplication", json.dumps(body), region)
    except Exception as e:
        raise ValueError(f"Failed to get application: {str(e)}")
    
    try:
        if response["Result"] is not None:
            result = response["Result"]
            errLogs: list[str] = []
            hasAuthError = False
            if result.get("Status") == "deploy_fail":
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
                except Exception as e:
                    logger.error(f"Failed to get application log: {str(e)}")

            if result.get("Status") == "deploying":
                time.sleep(3)
            
            if hasAuthError:
                raise ValueError("Failed to release application due to an authentication error. Please visit https://console.volcengine.com/iam/service/attach_custom_role?ServiceName=vefaas&policy1_1=APIGFullAccess&policy1_2=VeFaaSFullAccess&role1=ServerlessApplicationRole to grant the required permissions and then try again.")    

            responseInfo = {
                "Id": result["Id"],
                "Name": result["Name"],
                "Status": result["Status"],
                "Config": result["Config"],
                "Region": result["Region"],
                "NewRevisionNumber": result.get("NewRevisionNumber"),
            }
            if len(errLogs) > 0:
                responseInfo["DeployFailedLogs"] = errLogs

            return responseInfo
        else:
            raise ValueError(f"Get Application {application_id} failed, result is empty")
    except Exception as e:
        raise ValueError(f"Failed to parse application response: {str(e)}")

@mcp.tool(description="""Create a veFaaS function.

Args:
 - name: function name (unique, with a 6 length random string).
 - runtime: function runtime.
 - command: function startup script (./run.sh by default).
 - region: function region. (`cn-beijing` by default)

Note:
 - runtime **MUST** be `native-python3.12/v1`, `native-node20/v1`, or `native/v1`.
 - command **MUST** be a runnable script, e.g., `./run.sh`.
 - region **MUST** be `cn-beijing`, `cn-shanghai`, `cn-guangzhou`, or `ap-southeast-1`.
 - Supplying `enable_vpc=true` requires `vpc_id`, `subnet_ids`, and `security_group_ids`.
 - Declare every framework/server dependency in `requirements.txt` / `package.json`; do not bundle virtualenvs.
 - Module CLIs are not on PATH. Invoke them with `python -m module_name ...` or start the server in code—running `gunicorn ...` or `uvicorn ...` directly will fail.
 - Keep startup scripts focused on launching the app; skip extra installs/build once `upload_code` has run.
 - Store templates/static assets as files and sanity-check imports before uploading.
 - After all steps done, provide veFaaS function infos like function_id, name, region, runtime and platfrom link if these infos can get from context directly.
    - veFaaS platform link template: https://console.volcengine.com/vefaas/region:vefaas+`region`/function/detail/`function_id`?tab=config

Error Handle Tips:
 - If there is **any authentication** error about vefaas function(like create/release/get), let user to apply auth by this link https://console.volcengine.com/iam/service/attach_role/?ServiceName=vefaas, then retry.

**CRITICAL REQUIREMENT**:
 - Before create function, check whether there is vefaas.yml exist, if it does, use the validate function_id in it and SKIP create_function.
 - After function created success:
    - Create and Edit vefaas.yml: add `function_id`, `name`, `region`, `runtime`, `command` to file immediately once function created.
    - **Do follow steps sequentially**:
     - 1. Upload code to veFaaS function. (Do If source is TOS object)
     - 2. Release function, if user need release/deploy function and upload_code done.
     - 3. Create a api gateway trigger after function create and release success.
     - 4. Create and release an vefaas Application after function created/released succeed and api_gateway_trigger created succeed.

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
            runtime=runtime if runtime else "python3.8/v1",
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
- Swap the function to an existing artifact (base64 zip, TOS object, container image) or adjust command/env/VPC fields.
- If `source` is provided, ensure the artifact already exists and matches the inferred source_type (zip/tos/image).
- Do **NOT** use this for fresh local code edits—run 'upload_code' so the platform rebuilds the package correctly.
- For VPC changes set `enable_vpc=true` and include `vpc_id`, `subnet_ids`, `security_group_ids`.

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
 - This tool only submits the release job; it does **NOT** mean the function is live or releaseing finished

**CRITICAL REQUIREMENT**:
- Call this tool when function code or config has been updated and need to release.
    - If code changed, **must** wait code uploaded and dependency install task completed.
    - If only config changed, no need to wait.
- After this tool called success, start poll `get_function_release_status` to check release status, stop poll if release succeed or failed. Poll every 3 seconds to avoid loop detection, up to 5 minutes.

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
            f"{function_id}. Poll 'get_function_release_status' until it reports Succeeded/Failed."
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

@mcp.tool(description="""Check release status.

Args:
- function_id: ID of the function to check release status.
- region: The region of the veFaaS function.

Note:
 - If failed: inspect status/errors, resolve, then rerun 'upload_code' -> 'release_function' procedure once fixes are in place. 
    - A frequent issue is `bash: <tool>: command not found`; ensure startup scripts call Python modules via `python -m ...` or launch the server in code (see `create_function` guidance) before retrying.

**CRITICAL REQUIREMENT**:
 - Can **only** use this tool to check vefaas function release status, release may take a while, should wait and check many times until status become Succeeded or Failed. **NEVER** try to get release status by other ways.
""")
def get_function_release_status(function_id: str, region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    req = volcenginesdkvefaas.GetReleaseStatusRequest(
        function_id=function_id
    )
    response = api_instance.get_release_status(req)
    if response.status == "inprogress":
        time.sleep(5)
    return response

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


@mcp.tool(description="""Create an API Gateway Trigger for a veFaaS function.

Args:
- function_id: ID of the function to create trigger for.
- api_gateway_id: ID of the API Gateway to use.
- service_id: ID of the API Gateway Service to use.
- region: The region of the veFaaS function.

Note:
- Use `list_api_gateways` to find an existing gateway to use, if not exist, create one via `create_api_gateway`.
- **MUST** use `create_api_gateway_service` to create a new gateway service for function.
- This tool links the function to that service (creates upstream + route). After success, reuse the service details returned by `create_api_gateway_service` to present the public domain to the user.

**CRITICAL REQUIREMENT**:
- This tool **CAN ONLY** be called if `create_function` tool be called in previous step.
 - After trigger created:
    - Add `public_access_domain` to `vefaas.yml`.
    - Add trigger info to `vefaas.yml` immediately. Follow the fomat:
        triggers:
        - id: `trigger_id` (from create_api_gateway_trigger response)
            type: apig
            name: `trigger_name` (from create_api_gateway_trigger response)

""")
def create_api_gateway_trigger(function_id: str, api_gateway_id: str, service_id: str, region: str = None):
    region = validate_and_set_region(region)

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    now = datetime.datetime.utcnow()

    # Generate a random suffix for the trigger name
    suffix = generate_random_name(prefix="", length=6)
    upstream_name = f"{function_id}-trigger-{suffix}"
    body = {
        "Name":upstream_name,
        "GatewayId":api_gateway_id,
        "SourceType":"VeFaas",
        "UpstreamSpec": {
            "VeFaas": {"FunctionId":function_id}}}

    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateUpstream", json.dumps(body), region)
        logger.debug("CreateUpstream response: %s", json.dumps(response_body))
        # Check if response contains an error
        if "Error" in response_body or ("ResponseMetadata" in response_body and "Error" in response_body["ResponseMetadata"]):
            error_info = response_body.get("Error") or response_body["ResponseMetadata"].get("Error")
            error_message = f"API Error: {error_info.get('Message', 'Unknown error')}"
            raise ValueError(error_message)

        # Check if Result exists in the response
        if "Result" not in response_body:
            raise ValueError(f"API call did not return a Result field: {response_body}")

        upstream_id = response_body["Result"]["Id"]
    except Exception as e:
        error_message = f"Error creating upstream: {str(e)}"
        raise ValueError(error_message)

    body = {
        "Name":"default",
        "UpstreamList":[{
                "Type":"VeFaas",
                "UpstreamId":upstream_id,
                "Weight":100
                }
                ],
                "ServiceId":service_id,
                "MatchRule":{"Method":["POST","GET","PUT","DELETE","HEAD","OPTIONS"],
                             "Path":{"MatchType":"Prefix","MatchContent":"/"}},
                "AdvancedSetting":{"TimeoutSetting":{
                    "Enable":False,
                    "Timeout":30},
                "CorsPolicySetting":{"Enable":False}
                }
    }
    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateRoute", json.dumps(body), region)
    except Exception as e:
        error_message = f"Error creating route: {str(e)}"
        raise ValueError(error_message)
    
    respInfo = {
        "UpstreamId": upstream_id,
        "UpstreamName": upstream_name,
        "CreateRouteResponse": response_body
    }
    return respInfo

@mcp.tool(description="""List API Gateways.

Args:
 - region: The region to find API Gateways.

Note:
 - Use this tool to confirm a gateway exists before creating one.

""")
def list_api_gateways(region: str = None):
    now = datetime.datetime.utcnow()

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    response_body = request("GET", now, {"Limit": "10"}, {}, ak, sk, token, "ListGateways", None, region)
    return response_body


@mcp.tool(description="""Create an API Gateway when no reusable gateway exists.

Args:
 - name: The name of the API Gateway.
 - region: The region to create the API Gateway. (supported: `cn-beijing`, `cn-shanghai`, `cn-guangzhou`, `ap-southeast-1`)

Note:
 - Operation is asynchronous (≤~5 minutes). After invoking, poll `list_api_gateways` until the gateway with this name/region reports `Running`. **Poll every ~5s for up to ~5 minutes**.
 - If the API responds that the account balance is below the required threshold (for example, balance < 100) or quota has been exceeded, surface the message and instruct the user to resolve it via the console or contact API gateway OnCall; retries are not useful.

""")
def create_api_gateway(name: str = None, region: str = "cn-beijing") -> str:
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

@mcp.tool(description="""Create a VeApig gateway service (one per public domain).

Args:
 - gateway_id: The ID of the API Gateway where the service will be created.
 - name: The name of the gateway service. If not provided, a random value is used.
 - region: The region of the API Gateway Service will be created. Default is cn-beijing.

Note:
 - Requires an existing Running gateway (`gateway_id`). Can use `list_api_gateways` and `create_api_gateway` to get one.
 - Always reuse an existing Running gateway and add services per function/domain.
 - Returns the raw creation response plus a follow-up `GetGatewayService` result so you can capture the service ID and domain. After binding routes (`create_api_gateway_trigger`), reuse those details when presenting the public URL.

""")
def create_api_gateway_service(
    gateway_id: str, name: str = None, region: str = "cn-beijing"
) -> str:
    if name:
        service_name = append_random_suffix(name)
    else:
        service_name = generate_random_name()
    region = validate_and_set_region(region)
    body = {
        "ServiceName": service_name,
        "GatewayId": gateway_id,
        "Protocol": ["HTTP", "HTTPS"],
        "AuthSpec": {"Enable": False},
    }

    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    try:
        creation_response = request("POST", now, {}, {}, ak, sk, token, "CreateGatewayService", json.dumps(body), region)
    except Exception as e:
        return f"Failed to create VeApig gateway service with name {service_name}: {str(e)}"

    try:
        result = creation_response.get("Result", {}) if isinstance(creation_response, dict) else {}
    except Exception:
        result = {}

    service_id = result.get("Id") or result.get("ServiceId")
    if not service_id:
        raise ValueError(f"CreateGatewayService response missing service ID: {creation_response}")

    detail_body = {"Id": service_id}
    detail_now = datetime.datetime.utcnow()
    service_details = request(
        "POST", detail_now, {}, {}, ak, sk, token, "GetGatewayService", json.dumps(detail_body), region
    )

    combined = {
        "service_id": service_id,
        "create_response": creation_response,
        "service_details": service_details,
    }
    return json.dumps(combined, ensure_ascii=False, indent=2)

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
        " - local_folder_exclude: Optional list of patterns to exclude from the upload.\n"
        " - file_dict: {filename -> content}\n\n"

        "Returns:\n"
        "- 'code_upload_callback'\n"
        "- 'dependency': {dependency_task_created, should_check_dependency_status, skip_reason?}\n\n"
    
        "**CRITICAL REQUIREMENT:**\n"
        " - **MUST** respect veFaaS Develop Rules.(**edit code to satisfied the rules before uploading**)\n"
        "  - Rule 1: Process must be startup by an executeble script.\n"
        "  - Rule 2: For Golang/C++/other compiled languages: veFaaS **CANNOT** compile code. Must compile a Linux-compatible binary locally and upload it with all the source code, the startup script must execute this pre-compiled binary directly.\n"
        "  - Rule 3: Startup script must not contain any compile command or dependency install command. (like: go build or pip install)\n"
        "  - Rule 4: Python/Node deps: put them in 'requirements.txt'/'package.json'; veFaaS installs them as needed.\n"
        "  - Rule 5: HTTP server **MUST** listen on IP: 0.0.0.0, PORT: 8000.\n"
        "  - Rule 6: Store templates/static assets as files and sanity-check imports before uploading.\n"
        "  - Rule 7: When uploading code, exclude local deps and noise (e.g., `.venv`, `site-packages`, `node_modules`, `.git`, build artifacts) via `local_folder_exclude`.\n\n"
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
        "After upload: dependency install (if any) runs asynchronously; if triggered, you MUST call 'get_dependency_install_task_status' to poll until Succeeded/Failed."
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
- function_id: The ID of the veFaaS function.
- fetch_log_content: Whether to fetch log content when the task is Failed. Default is False.

Note:
 - Use when 'upload_code' reported a task or your code has 'requirements.txt' (Python) / 'package.json' (Node.js).
 - Stop on Succeeded/Failed; if it stays InProgress beyond ~5min, escalate instead of hammering the API.
 - On Failed: inspect logs. If dependency spec issue, fix and 'upload_code' again; if transient, retry.

**CRITICAL REQUIREMENT**:
 - Poll every 3s to avoid loop detection, up to 5min timeout.

Returns:
- 'status' (raw API response)
- If Failed: 'log_download_url', when 'fetch_log_content' is True: 'log_content'.

""")
def get_dependency_install_task_status(
    function_id: str,
    region: Optional[str] = None,
    fetch_log_content: bool = False,
):
    region = validate_and_set_region(region)

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    body = {"FunctionId": function_id}
    now = datetime.datetime.utcnow()

    try:
        status_resp = request(
            "POST", now, {}, {}, ak, sk, token, "GetDependencyInstallTaskStatus", json.dumps(body), region, 5,
        )
        result = {"status": status_resp}

        try:
            status = status_resp.get("Result", {}).get("Status")
        except Exception:
            status = None

        if status == "Failed":
            try:
                log_resp = request(
                    "POST",
                    now,
                    {},
                    {},
                    ak,
                    sk,
                    token,
                    "GetDependencyInstallTaskLogDownloadURI",
                    json.dumps(body),
                    region,
                    5,
                )
                url = log_resp.get("Result", {}).get("DownloadURL")
                if isinstance(url, str):
                    url = url.replace("\\u0026", "&")
                result["log_download_url"] = url

                if fetch_log_content and url:
                    try:
                        resp = requests.get(url, timeout=30)
                        result["log_content"] = resp.text
                    except Exception as ex:
                        result["log_content_error"] = str(ex)
            except Exception as ex:
                result["log_download_error"] = str(ex)

        if status == "InProgress":
            time.sleep(3)
        return result
    except Exception as e:
        raise ValueError(f"Failed to get dependency install task status: {str(e)}")

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
 - function_id (required): the ID of the function
 - revision_number (optional): specific code revision number to query. If not provided, defaults to version 0.
 - use_stable_revision (optional): default False. Only when user ask the online/released/stable revision code set use_stable_revision to True.
 - dest_dir: the path where the code to download and unzip. default is local opened path.


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

        # Create destination directory if it doesn't exist
        os.makedirs(dest_dir, exist_ok=True)

        # Unzip the file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(dest_dir)

        # generate vefaas.yml
        vefaas_yml_path = os.path.join(dest_dir, "vefaas.yml")
        try:
            function_detail = get_function_detail(function_id, region)
            triggers = list_function_triggers(function_id, region).get("Result", {}).get("Items", [])
            with open(vefaas_yml_path, "w") as f:
                f.write(f"function_id: {function_id}\n")
                f.write(f"name: {function_detail.name}\n")
                f.write(f"region: {region}\n")
                f.write(f"runtime: {function_detail.runtime}\n")
                f.write(f"command: {function_detail.command}\n")
                f.write(f"triggers:\n")
                for trigger in triggers:
                    f.write(f"  - id: {trigger.get('Id', '')}\n")
                    f.write(f"    type: {trigger.get('Type', '')}\n")
                    f.write(f"    name: {trigger.get('Name', '')}\n")
        except Exception as e:
            logger.error(f"Failed to write vefaas.yml for function {function_id}: {str(e)}")
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

@mcp.tool(description="""List veFaaS Application templates for creating new applications.

This tool helps you find appropriate veFaaS application templates based on your specific requirements when creating new veFaaS applications. Each template in the response includes a 'description' field that explains the template's functionality and use case.

NOTE:
 - Use this tool to:
  - 1. Discover available templates for different application types and use cases
  - 2. Review template descriptions to find the most suitable one for your needs
  - 3. Get template details and source code for further development using the template ID

 - Each template returned contains:
  - ID: Template ID for get detail.
  - Description: A brief explanation of the template's functionality and use case.

After finding a suitable template, use tool get_vefaas_application_template with the template ID to get the template's source code and detailed information for development.""")
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
        #print(f"list_templates resp: {resp}")
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
    return result

@mcp.tool(description="""Get veFaaS Application template source code.

Args:
 - template_id (required): the ID of the template to fetch, the ID can get from tool 'list_vefaas_application_templates'.
 - destination_dir (required): user specified the directory where the template zip file should be saved. If not provided, the destination_dir should be saved in the current folder path.
 
Note: 
- Never save the template.zip file. If need to save the code, extract the files from the zip archive.

""")
def get_vefaas_application_template(template_id: str, destination_dir: str):
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    now = datetime.datetime.utcnow()
    body = {"Id": template_id}

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