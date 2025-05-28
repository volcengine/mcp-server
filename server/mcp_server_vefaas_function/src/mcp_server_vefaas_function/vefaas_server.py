from __future__ import print_function

import io
from typing import Union

from mcp.server.fastmcp import FastMCP
import datetime
import volcenginesdkcore
import volcenginesdkvefaas
from volcenginesdkcore.rest import ApiException
import random
import string
import os
import base64
import logging
import tempfile
import zipfile
from .sign import request, get_authorization_credentials
import json
from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context, FastMCP
from starlette.requests import Request

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

mcp = FastMCP("VeFaaS")

@mcp.tool(description="""Lists all supported runtimes for veFaaS functions.
Use this when you need to list all supported runtimes for veFaaS functions.""")
def supported_runtimes():
    return ["python3.8/v1", "python3.9/v1", "python3.10/v1", "python3.12/v1", "native-python3.12/v1",
            "golang/v1",
            "node14/v1", "node20/v1",
            "nodeprime14/v1",
            "native-node14/v1", "native-node20/v1"]

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

@mcp.tool(description="""Creates a new VeFaaS function with a random name if no name is provided.
region is the region where the function will be created, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
          `cn-shanghai`, `cn-guangzhou` as well.
Note: 
1. The runtime parameter must be one of the values returned by the supported_runtimes. Please ensure you call that tool first to get the valid options.
2.	If the function is intended to serve as a web service, you must:
	•	Write code to start an HTTP server that listens on port 8000 (e.g., using Python’s http.server, Node’s http, or Flask)).
	•	Provide a launch script such as run.sh that starts the server (e.g., python3 server.py) and keeps it running.
	•	Set the Command parameter to point to this script (e.g., ./run.sh) in the function config.
	•	Only native runtimes support the Command field. Use supported_runtimes to ensure the chosen runtime allows it.
""")
def create_function(name: str = None, region: str = None, runtime: str = None, command: str = None, source: str = None,
                    image: str = None, envs: dict = None, description: str = None) -> str:
    # Validate region
    region = validate_and_set_region(region)
    
    api_instance = init_client(region, mcp.get_context())
    function_name = name if name else generate_random_name()
    create_function_request = volcenginesdkvefaas.CreateFunctionRequest(
        name=function_name,
        runtime=runtime if runtime else "python3.8/v1",
    )

    if image:
        create_function_request.source = image
        create_function_request.source_type = "image"

    if command:
        create_function_request.command = command

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

        create_function_request.source = source
        create_function_request.source_type = source_type

    if envs:
        env_list = []
        for key, value in envs.items():
            env_list.append({
                "key": key,
                "value": value
            })
        create_function_request.envs = env_list

    if description:
        create_function_request.description = description

    try:
        response = api_instance.create_function(create_function_request)
        return f"Successfully created VeFaaS function with name {function_name} and id {response.id}"
    except ApiException as e:
        error_message = f"Failed to create VeFaaS function: {str(e)}"
        raise ValueError(error_message)

@mcp.tool(description="""Updates a VeFaaS function's code.
Use this when asked to update a VeFaaS function's code.
Region is the region where the function will be updated, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
`cn-shanghai`, `cn-guangzhou` as well.
After updating the function, you need to release it again for the changes to take effect.
No need to ask user for confirmation, just update the function.""")
def update_function(function_id: str, source: str = None, region: str = None, command: str = None,
                    envs: dict = None):
    
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

    try:
        response = api_instance.update_function(update_request)
        return f"Successfully updated function {function_id} with source type {source_type}"
    except ApiException as e:
        error_message = f"Failed to update VeFaaS function: {str(e)}"
        raise ValueError(error_message)

@mcp.tool(description="""Releases a VeFaaS function to make it available for production use.
Use this when asked to release, publish, or deploy a VeFaaS function.
Region is the region where the function will be released, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
`cn-shanghai`, `cn-guangzhou` as well.
After releasing, you should call list_release_records to check the release status.
No need to ask user for confirmation, just release the function.
If you want the function to be accessible from the public internet, you also need to call create_api_gateway_trigger after releasing to create an API Gateway trigger.""")
def release_function(function_id: str, region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

    try:
        req = volcenginesdkvefaas.ReleaseRequest(
            function_id=function_id, revision_number=0
        )
        response = api_instance.release(req)
        return f"Successfully released function {function_id} for production use"
    except ApiException as e:
        error_message = f"Failed to release VeFaaS function: {str(e)}"
        raise ValueError(error_message)

@mcp.tool(description="""Deletes a VeFaaS function.
Use this when asked to delete, remove, or uninstall a VeFaaS function.
Region is the region where the function will be deleted, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
`cn-shanghai`, `cn-guangzhou` as well.
No need to ask user for confirmation, just delete the function.""")
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
        error_message = f"Failed to delete VeFaaS function: {str(e)}"
        raise ValueError(error_message)

@mcp.tool(description="""Checks the release status of a VeFaaS function.
Use this when you need to check the release status of a VeFaaS function.
Region is the region where the function exists, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`, 
`cn-shanghai`, `cn-guangzhou` as well.
No need to ask user for confirmation, just check the release status of the function.""")
def get_function_release_status(function_id: str, region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    req = volcenginesdkvefaas.GetReleaseStatusRequest(
        function_id=function_id
    )
    response = api_instance.get_release_status(req)
    return response

@mcp.tool(description="""Checks if a VeFaaS function exists.
Use this when you need to check if a VeFaaS function exists.
No need to ask user for confirmation, just check if the function exists.""")
def does_function_exist(function_id: str, region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    req = volcenginesdkvefaas.GetFunctionRequest(
        id=function_id
    )
    try:
        response = api_instance.get_function(req)
        return True
    except ApiException as e:
        return False

@mcp.tool(description="""Lists all VeFaaS functions.
Use this when you need to list all VeFaaS functions.
No need to ask user for confirmation, just list the functions.""")
def get_latest_functions(region: str = None):
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())
    req = volcenginesdkvefaas.ListFunctionsRequest(
        page_number=1,
        page_size=5
    )
    response = api_instance.list_functions(req)
    return response

def generate_random_name(prefix="mcp", length=8):
    """Generate a random string for function name"""
    random_str = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )
    return f"{prefix}-{random_str}"


def init_client(region: str = None, ctx: Context = None):
    """
    Initializes the VeFaaS API client with credentials and region.
    
    Args:
        region: The region to use for the client
        ctx: The server context object
        
    Returns:
        VEFAASApi: Initialized VeFaaS API client
        
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
    print(f"Using region: {region}")
    configuration.region = region
    
    # set default configuration
    volcenginesdkcore.Configuration.set_default(configuration)
    return volcenginesdkvefaas.VEFAASApi()


@mcp.tool(description="""Compresses multiple in-memory files into a single ZIP archive and returns its base64-encoded string.
Use this when you need to package multiple files and pass them to other interfaces (e.g., function creation or update) in a base64-encoded ZIP format.
The input should be a dictionary where keys are filenames and values are file contents in str. No files are written to disk.""")
def create_zip_base64(file_dict: dict[str, Union[str, bytes]]) -> str:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in file_dict.items():
            info = zipfile.ZipInfo(filename)
            info.date_time = datetime.datetime.now().timetuple()[:6]
            info.external_attr = 0o777 << 16
            zip_file.writestr(info, content)

    zip_bytes = zip_buffer.getvalue()
    zip_base64 = base64.b64encode(zip_bytes).decode("utf-8")

    return zip_base64


@mcp.tool(description="""Creates a new api gateway trigger for a veFaaS function.
Use this when you need to create a new api gateway trigger for a veFaaS function.
It is recommended that each gateway service is used for only one function.
No need to ask user for confirmation, just create the gateway.""")
def create_api_gateway_trigger(function_id: str, api_gateway_id: str, service_id: str, region: str = None):
    region = validate_and_set_region(region)
    
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    now = datetime.datetime.utcnow()
    
    # Generate a random suffix for the trigger name
    suffix = generate_random_name(prefix="", length=6)

    body = {
        "Name":f"{function_id}-trigger-{suffix}",
        "GatewayId":api_gateway_id,
        "SourceType":"VeFaas",
        "UpstreamSpec": {
            "VeFaas": {"FunctionId":function_id}}}

    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateUpstream", json.dumps(body))
        # Print the full response for debugging
        print(f"Response: {json.dumps(response_body)}")
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
        "Name":"router1",
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
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateRoute", json.dumps(body))
    except Exception as e:
        error_message = f"Error creating route: {str(e)}"
        raise ValueError(error_message)
    return response_body

@mcp.tool(description="""Lists all API gateways.
Use this when you need to list all API gateways.
No need to ask user for confirmation, just list the gateways.""")
def list_api_gateways(region: str = None):
    now = datetime.datetime.utcnow()
   
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    response_body = request("GET", now, {"Limit": "10"}, {}, ak, sk, token, "ListGateways", None)
    return response_body

@mcp.tool(description="""Lists all services of an API gateway.
Use this when you need to list all services of an API gateway.
No need to ask user for confirmation, just list the services.""")
def list_api_gateway_services(gateway_id: str, region: str = None):
    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")
    
    body = {
        "GatewayId": gateway_id,
        "Limit": 10,
        "Offset": 0,
    }

    response_body = request("POST", now, {}, {}, ak, sk, token, "ListGatewayServices", json.dumps(body))
    return response_body

@mcp.tool(description="""Lists all routes of an upstream.
Use this when you need to list all routes of an upstream.
No need to ask user for confirmation, just list the routes.""")
def list_routes(upstream_id: str, region: str = None):
    now = datetime.datetime.utcnow()
    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    body = {
        "UpstreamId": upstream_id
    }

    response_body = request("POST", now, {}, {}, ak, sk, token, "ListRoutes", json.dumps(body))
    return response_body


