from __future__ import print_function

import io
from typing import Union, Optional
import datetime
import volcenginesdkcore
import volcenginesdkvefaas
from volcenginesdkcore.rest import ApiException
import random
import string
import base64
import logging
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
2. If the function is intended to serve as a web service, you must:
   • Write code to start an HTTP server that listens on port 8000 (e.g., using Python’s http.server, Node’s http, or Flask).
   • Provide a launch script such as run.sh that starts the server (e.g., python3 server.py) and keeps it running.
   • Set the Command parameter to point to this script (e.g., ./run.sh) in the function config.
   • Only native runtimes support the Command field. Use supported_runtimes to ensure the chosen runtime allows it.
3. After creating the function, you can use the `upload_code` tool to upload the function code and related files.
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
After releasing, you should call get_function_release_status to check the release status.
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


@mcp.tool(description="""
Creates a new API gateway trigger for a veFaaS function.

- Each function must use a dedicated gateway service (do not reuse services between functions).
- API gateways should be reused across different services whenever possible.

This tool only creates the trigger using the provided gateway ID and service ID.
After creation, you can use the `list_api_gateway_services` tool to retrieve the access address.
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


@mcp.tool(
    description="""
Creates a new VeApig API gateway in the specified region.

- `name`: Optional custom name for the gateway. If not provided, a random name will be auto-generated.
- `region`: Target region for gateway creation. Defaults to `cn-beijing`. Supported values include `cn-beijing`, `cn-shanghai`, `cn-guangzhou`, and `ap-southeast-1`.

Note: This is an **asynchronous** operation and may take up to **5 minutes** to complete.  
After calling this tool, you must use the `list_api_gateways` tool to check the status of the gateway.  
Only when the status is `Running` does the gateway creation complete successfully.

Recommendation: A single API gateway can be reused across multiple functions and services.  
Before creating a new gateway, consider reusing an existing one using `list_api_gateways`.
"""
)
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
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateGateway", json.dumps(body))
        return response_body
    except Exception as e:
        return f"Failed to create VeApig gateway with name {gateway_name}: {str(e)}"


@mcp.tool(
    description="""Creates a new VeApig gateway service with a random name if no name is provided.
gateway_id is the id of the gateway where the service will be created. The gateway_id is required.
region is the region where the gateway service will be created, default is cn-beijing. It accepts `ap-southeast-1`, `cn-beijing`,
`cn-shanghai`, `cn-guangzhou` as well.
"""
)
def create_gateway_service(
    gateway_id: str, name: str = None, region: str = "cn-beijing"
) -> str:
    """
    Creates a new VeApig gateway service.

    Args:
        gateway_id (str): The id of the gateway where the service will be created.
        name (str): The name of the gateway service. If not provided, a random name will be generated.
        region (str): The region where the gateway service will be created. Default is cn-beijing.

    Returns:
        str: The response body of the request.
    """

    service_name = name if name else generate_random_name()
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
        response_body = request("POST", now, {}, {}, ak, sk, token, "CreateGatewayService", json.dumps(body))
        return response_body
    except Exception as e:
        return f"Failed to create VeApig gateway service with name {service_name}: {str(e)}"


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

def ensure_executable_permissions(folder_path: str):
    for root, _, files in os.walk(folder_path):
        for fname in files:
            full_path = os.path.join(root, fname)
            if fname.endswith('.sh') or fname in ('run.sh',):
                os.chmod(full_path, 0o755)

def zip_and_encode_folder(folder_path: str) -> Tuple[bytes, int, Exception]:
    """
    Zips a folder with system zip command (if available) or falls back to Python implementation.
    Returns (zip_data, size_in_bytes, error) tuple.
    """
    # Check for system zip first
    if not shutil.which('zip'):
        print("System zip command not found, using Python implementation")
        try:
            data = python_zip_implementation(folder_path)
            return data, len(data), None
        except Exception as e:
            return None, 0, e

    print(f"Zipping folder: {folder_path}")
    try:
        ensure_executable_permissions(folder_path)
        # Create zip process with explicit arguments
        proc = subprocess.Popen(
            ['zip', '-r', '-q', '-', '.', '-x', '*.git*', '-x', '*.venv*', '-x', '*__pycache__*', '-x', '*.pyc'],
            cwd=folder_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1024 * 8  # 8KB buffer
        )

        # Collect output with proper error handling
        try:
            stdout, stderr = proc.communicate(timeout=30)
            if proc.returncode != 0:
                print(f"Zip error: {stderr.decode()}")
                data = python_zip_implementation(folder_path)
                return data, len(data), None

            if stdout:
                size = len(stdout)
                print(f"Zip finished, size: {size / 1024 / 1024:.2f} MB")
                return stdout, size, None
            else:
                print("No data from zip command, falling back to Python implementation")
                data = python_zip_implementation(folder_path)
                return data, len(data), None

        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)  # Give it 5 seconds to cleanup
            print("Zip process timed out, falling back to Python implementation")
            try:
                data = python_zip_implementation(folder_path)
                return data, len(data), None
            except Exception as e:
                return None, 0, e

    except Exception as e:
        print(f"System zip error: {str(e)}")
        try:
            data = python_zip_implementation(folder_path)
            return data, len(data), None
        except Exception as e2:
            return None, 0, e2

def python_zip_implementation(folder_path: str) -> bytes:
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
                    print(f"Warning: Skipping file {arcname} due to error: {str(e)}")

    print(f"Python zip finished, size: {buffer.tell() / 1024 / 1024:.2f} MB")
    return buffer.getvalue()

@mcp.tool(description="""
Uploads code to TOS for a veFaaS function deployment.

You may provide:
- 'local_folder_path': for uploading a local code directory (recommended for large or structured projects).
- 'file_dict': for in-memory code files, suitable for simple or lightweight use cases.

Note:
If the MCP Server is deployed remotely (e.g., via SSE), local paths are not accessible. In such cases, use 'file_dict' instead of 'local_folder_path'.

After uploading, remind the user to release the function for changes to take effect.
""")
def upload_code(region: str, function_id: str, local_folder_path: Optional[str] = None, file_dict: Optional[dict[str, Union[str, bytes]]] = None) -> bytes:
    region = validate_and_set_region(region)

    api_instance = init_client(region, mcp.get_context())

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

    return upload_code_zip_for_function(api_instance=api_instance, function_id=function_id, code_zip_size=size, zip_bytes=data)


def upload_code_zip_for_function(api_instance: object, function_id: str, code_zip_size: int, zip_bytes, ) -> bytes:
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
        print(f"Upload successful! Size: {code_zip_size / 1024 / 1024:.2f} MB")
    else:
        error_message = f"Upload failed to {upload_url} with status code {response.status_code}: {response.text}"
        raise ValueError(error_message)

    try:
        ak, sk, token = get_authorization_credentials(mcp.get_context())
    except ValueError as e:
        raise ValueError(f"Authorization failed: {str(e)}")

    now = datetime.datetime.utcnow()

    # Generate a random suffix for the trigger name
    suffix = generate_random_name(prefix="", length=6)

    body = {
        "FunctionId": function_id
    }

    try:
        response_body = request("POST", now, {}, {}, ak, sk, token, "CodeUploadCallback", json.dumps(body))
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
