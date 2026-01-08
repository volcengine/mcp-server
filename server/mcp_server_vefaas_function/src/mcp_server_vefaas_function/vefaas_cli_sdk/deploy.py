# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""
Deploy Flow Module

This module encapsulates the core deployment logic for veFaaS applications,
ported from vefaas-cli.

Correct flow:
1. Detect project configuration
2. Build project (if needed, for Node.js/static sites)
3. Package output directory
4. Upload to TOS (GenTempTosObjectUrl)
5. Create/Update function with Source pointing to TOS location
6. Wait for dependency installation (Python)
7. Create and release application (includes function release)
"""

from dataclasses import dataclass, field
from typing import Optional, List
import time
import logging
import json
import os
import datetime
import subprocess
import io
import zipfile
import pathspec

from .detector import auto_detect, DetectionResult
from .config import (
    VefaasConfig,
    FunctionConfig,
    TriggerConfig,
    read_config,
    write_config,
    get_linked_ids,
)

logger = logging.getLogger(__name__)

# Default timeout and polling interval
DEFAULT_TIMEOUT_SECONDS = 240  # 4 minutes
DEPLOY_TIMEOUT_SECONDS = 360  # 6 minutes for full deployment
DEFAULT_POLL_INTERVAL_SECONDS = 3

# Default .vefaasignore file content (aligned with vefaas-cli)
DEFAULT_VEFAASIGNORE = """# veFaaS default ignore patterns
# Files and directories that will not be packaged and uploaded

# Version control
.git/
.svn/
.hg/

# Python virtual environments and dependencies (installed by function runtime)
.venv/
site-packages/
__pycache__/

# IDE and editors
.idea/
.vscode/
*.swp
*.swo

# System files
.DS_Store
Thumbs.db

# veFaaS CLI config
.vefaas/
"""

# Default Caddyfile name for static sites
DEFAULT_CADDYFILE_NAME = "DefaultCaddyFile"


def read_gitignore_patterns(base_dir: str) -> List[str]:
    """Read .gitignore file patterns. Ported from vefaas-cli."""
    gitignore_path = os.path.join(base_dir, ".gitignore")
    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            raw = f.read()
        return [line.strip() for line in raw.splitlines() if line.strip() and not line.strip().startswith("#")]
    except Exception:
        return []


def read_vefaasignore_patterns(base_dir: str) -> List[str]:
    """Read .vefaasignore file patterns. Create default file if not exists. Ported from vefaas-cli."""
    vefaasignore_path = os.path.join(base_dir, ".vefaasignore")
    try:
        with open(vefaasignore_path, "r", encoding="utf-8") as f:
            raw = f.read()
        return [line.strip() for line in raw.splitlines() if line.strip() and not line.strip().startswith("#")]
    except FileNotFoundError:
        # File doesn't exist, create default .vefaasignore
        try:
            with open(vefaasignore_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_VEFAASIGNORE)
            logger.debug(f"[package] Created default .vefaasignore at {vefaasignore_path}")
        except Exception as e:
            logger.debug(f"[package] Failed to create .vefaasignore: {e}")
        # Return default patterns
        return [line.strip() for line in DEFAULT_VEFAASIGNORE.splitlines() if line.strip() and not line.strip().startswith("#")]
    except Exception:
        return []


def create_ignore_filter(
    gitignore_patterns: List[str],
    vefaasignore_patterns: List[str],
    additional_patterns: Optional[List[str]] = None
) -> pathspec.PathSpec:
    """Create a pathspec filter from gitignore/vefaasignore patterns. Ported from vefaas-cli."""
    all_patterns = gitignore_patterns + vefaasignore_patterns + (additional_patterns or [])
    return pathspec.PathSpec.from_lines("gitwildmatch", all_patterns)


def render_default_caddyfile_content() -> str:
    """
    Generate default Caddyfile content for static site hosting.
    Ported from vefaas-cli renderDefaultCaddyfileContent().
    """
    return """:8000 {
    root * .
    # Block access to sensitive paths
    @unsafePath {
      path /.git/* /node_modules/* /vendor/* /.venv/*
    }
    respond @unsafePath 404
    # Configure cache policies for different file types
    @staticAssets {
      path *.css *.js *.png *.jpg *.jpeg *.gif *.svg *.ico *.webp
    }
    @htmlFiles {
      path *.html
    }
    # Long cache for static assets (1 year), browser updates when filename changes
    header @staticAssets Cache-Control "public, max-age=31536000, immutable"
    # No cache for HTML
    header @htmlFiles Cache-Control "no-cache, no-store, must-revalidate"
    header @htmlFiles Pragma "no-cache"
    header @htmlFiles Expires "0"
    # Default cache header for unmatched files
    header Cache-Control "public, max-age=3600"
    file_server
    try_files {path} {path}.html {path}/index.html 404.html index.html
    log {
      output stderr
    }
}"""


def ensure_caddyfile_in_output(
    dest_dir: str,
    output_path: str,
    filename: str = DEFAULT_CADDYFILE_NAME
) -> str:
    """
    Create DefaultCaddyFile in the output directory for static site hosting.
    Ported from vefaas-cli ensureCaddyfileInOutput().

    Args:
        dest_dir: Project root directory
        output_path: Build output directory (relative to dest_dir)
        filename: Caddyfile filename (default: DefaultCaddyFile)

    Returns:
        Path to the created Caddyfile
    """
    out_dir = os.path.join(dest_dir, output_path) if output_path and output_path != "./" else dest_dir
    os.makedirs(out_dir, exist_ok=True)

    content = render_default_caddyfile_content()
    target = os.path.join(out_dir, filename)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"[deploy] Caddyfile generated: {target}")
    return target


@dataclass
class DeployResult:
    """Deployment result containing IDs and URLs"""
    success: bool = False
    application_id: Optional[str] = None
    function_id: Optional[str] = None
    function_name: Optional[str] = None
    access_url: Optional[str] = None
    console_url: Optional[str] = None
    app_console_url: Optional[str] = None
    error: Optional[str] = None
    logs: List[str] = field(default_factory=list)  # Status messages


@dataclass
class DeployConfig:
    """Deployment configuration"""
    project_path: str                           # Required: project root path
    name: Optional[str] = None                  # App name (required for new apps)
    application_id: Optional[str] = None        # Existing app ID (for updates)
    region: str = "cn-beijing"                  # Region
    gateway_name: Optional[str] = None          # Gateway name (auto-detect if not specified)
    build_command: Optional[str] = None         # Override build command
    output_path: Optional[str] = None           # Override output path
    start_command: Optional[str] = None         # Override start command
    port: Optional[int] = None                  # Override port
    skip_build: bool = False                    # Skip build step


class VeFaaSClient:
    """
    veFaaS API client - provides all operations needed for deployment.

    Usage:
        client = VeFaaSClient(ak, sk, token, region)
        result = deploy_application(config, client)
    """

    def __init__(self, ak: str, sk: str, token: str, region: str = "cn-beijing"):
        self.ak = ak
        self.sk = sk
        self.token = token
        self.region = region

    def call(self, action: str, body: dict, timeout: int = None) -> dict:
        """Make a raw API call"""
        from ..sign import request
        now = datetime.datetime.utcnow()
        return request("POST", now, {}, {}, self.ak, self.sk, self.token, action, json.dumps(body), self.region, timeout)

    def _check_api_error(self, result: dict, action: str) -> None:
        """Check API response for errors and raise with detailed message."""
        error = result.get("ResponseMetadata", {}).get("Error", {})
        if error:
            code = error.get("Code", "")
            message = error.get("Message", "Unknown error")
            request_id = result.get("ResponseMetadata", {}).get("RequestId", "")

            # Check for common error patterns and provide clear guidance
            if "already exists" in message.lower() or "duplicate" in message.lower():
                raise ValueError(
                    f"[{action}] Name already exists: {message}\n"
                    "To update an existing application, get the application_id from `.vefaas/config.json` or console, "
                    "then call deploy_application with application_id parameter. "
                    "Do NOT use function_id directly - always use application_id for updates."
                )
            elif "not found" in message.lower():
                raise ValueError(f"[{action}] Resource not found: {message}")
            elif "permission" in message.lower() or "auth" in message.lower():
                raise ValueError(
                    f"[{action}] Permission denied: {message}\n"
                    "Please visit https://console.volcengine.com/iam/service/attach_role/?ServiceName=vefaas to authorize and retry"
                )
            else:
                raise ValueError(f"[{action}] API error ({code}): {message} (RequestId: {request_id})")

    def _call_with_check(self, action: str, body: dict, timeout: int = None) -> dict:
        """Make API call and check for errors."""
        result = self.call(action, body, timeout)
        self._check_api_error(result, action)
        return result

    # ========== TOS Operations ==========

    def gen_temp_tos_url(self) -> dict:
        """Generate temporary TOS upload URL"""
        return self._call_with_check("GenTempTosObjectUrl", {})

    def upload_to_tos(self, zip_bytes: bytes) -> str:
        """
        Upload zip bytes to TOS and return inner source location.

        Returns:
            Inner source location string for use in CreateFunction/UpdateFunction
        """
        import requests

        # Get temporary upload URL
        result = self.gen_temp_tos_url()
        temp = result.get("Result", {})
        outer_url = temp.get("OuterSourceLocation")
        inner_location = temp.get("InnerSourceLocation")

        if not outer_url or not inner_location:
            raise ValueError("Failed to get TOS upload URL")

        # Upload to TOS
        response = requests.put(outer_url, data=zip_bytes, headers={
            "Content-Type": "application/octet-stream",
        })

        if response.status_code not in (200, 201):
            raise ValueError(f"Failed to upload to TOS: {response.status_code}")

        logger.info(f"[deploy] Uploaded to TOS: {len(zip_bytes)} bytes")
        return inner_location

    # ========== Function Operations ==========

    def create_function(
        self,
        name: str,
        runtime: str,
        command: str,
        port: int = 8080,
        source: Optional[str] = None,
        build_command: Optional[str] = None,
        output_path: Optional[str] = None,
    ) -> dict:
        """Create a new function with optional TOS source"""
        body = {
            "Name": name,
            "Runtime": runtime,
            "Command": command,
            "Port": port,
            "Description": "Created by veFaaS MCP",
            "ExclusiveMode": False,
            "RequestTimeout": 300,
            "MaxConcurrency": 100,
            "MemoryMB": 1024,
        }

        if source:
            body["SourceType"] = "tos"
            body["Source"] = source

        # Always include BuildConfig for application source
        # Use 'echo skip' as no-op command if build_command is empty (API requires non-empty)
        body["BuildConfig"] = {
            "Command": build_command or "echo skip",
            "OutputPath": output_path or "./",
        }

        return self._call_with_check("CreateFunction", body)

    def update_function(
        self,
        function_id: str,
        source: Optional[str] = None,
        command: Optional[str] = None,
        port: Optional[int] = None,
        runtime: Optional[str] = None,
    ) -> dict:
        """Update function with new source/config"""
        body = {"Id": function_id}

        if source:
            body["SourceType"] = "tos"
            body["Source"] = source
        if command:
            body["Command"] = command
        if port:
            body["Port"] = port
        if runtime:
            body["Runtime"] = runtime

        return self._call_with_check("UpdateFunction", body)

    def get_function(self, function_id: str) -> dict:
        """Get function details"""
        return self.call("GetFunction", {"Id": function_id})

    def release_function(self, function_id: str, revision_number: int = 0) -> dict:
        """Release/deploy a function"""
        return self._call_with_check("Release", {
            "FunctionId": function_id,
            "RevisionNumber": revision_number,
            "Description": "Triggered by veFaaS MCP",
        })

    def get_release_status(self, function_id: str) -> dict:
        """Get function release status"""
        return self.call("GetReleaseStatus", {"FunctionId": function_id})

    def get_dependency_install_status(self, function_id: str) -> dict:
        """Get dependency installation task status"""
        return self.call("GetDependencyInstallTaskStatus", {"FunctionId": function_id})

    # ========== Application Operations ==========

    def get_application(self, app_id: str) -> dict:
        """Get application details"""
        return self.call("GetApplication", {"Id": app_id})

    def create_application(self, name: str, function_id: str, gateway_name: str) -> dict:
        """Create a new application"""
        return self._call_with_check("CreateApplication", {
            "Name": name,
            "FunctionId": function_id,
            "Description": "Created by veFaaS MCP",
            "Reference": "mcp",
            "EndpointConfig": {"GatewayName": gateway_name},
        })

    def release_application(self, app_id: str) -> dict:
        """Release/deploy an application"""
        return self._call_with_check("ReleaseApplication", {
            "Id": app_id,
            "SkipPipeline": True,
            "Description": "Triggered by veFaaS MCP",
        })

    def list_applications(self, page_number: int = 1, page_size: int = 100, filters: Optional[List[dict]] = None) -> dict:
        """List applications"""
        body = {"PageNumber": page_number, "PageSize": page_size}
        if filters:
            body["Filters"] = filters
        return self.call("ListApplications", body)

    def find_application_by_name(self, name: str) -> Optional[str]:
        """Find application ID by name (using API level filter)"""
        try:
            # Format: Filters: [{ Item: { Key: 'Name', Value: [name] } }]
            filters = [{"Item": {"Key": "Name", "Value": [name]}}]
            result = self.list_applications(page_size=50, filters=filters)
            items = result.get("Result", {}).get("Items", [])

            # Client-side verification
            target_name = name.lower()
            for item in items:
                if item.get("Name", "").lower() == target_name:
                    return item.get("Id")
            return None
        except:
            return None

    # ========== Gateway Operations ==========

    def list_gateways(self) -> dict:
        """List API gateways"""
        return self.call("ListGateways", {"PageNumber": 1, "PageSize": 100})

    def get_usable_gateway(self) -> Optional[str]:
        """Get the name of an available (Running) gateway"""
        try:
            result = self.list_gateways()
            gateways = result.get("Result", {}).get("Items", [])
            for gw in gateways:
                if gw.get("Status") == "Running":
                    return gw.get("Name")
            return None
        except:
            return None


def get_console_url(function_id: str, region: str) -> str:
    """Get function console URL"""
    return f"https://console.volcengine.com/vefaas/region:vefaas+{region}/function/detail/{function_id}"


def get_application_console_url(application_id: str, region: str) -> str:
    """Get application console URL"""
    return f"https://console.volcengine.com/vefaas/region:vefaas+{region}/application/detail/{application_id}"


def extract_access_url_from_cloud_resource(cloud_resource: str) -> Optional[str]:
    """
    Extract access URL from CloudResource JSON string.
    Matches vefaas-cli's parseCloudResource + sanitizeUrl logic.
    """
    try:
        if not cloud_resource:
            return None
        parsed = json.loads(cloud_resource)
        # Get first key's value (e.g., 'framework' or other)
        keys = list(parsed.keys())
        if not keys:
            return None
        data = parsed[keys[0]]
        url_obj = data.get('url', {})
        # Prefer system_url, fallback to inner_url
        system_url = url_obj.get('system_url', '')
        inner_url = url_obj.get('inner_url', '')
        if system_url and isinstance(system_url, str) and system_url.strip():
            return system_url.strip()
        if inner_url and isinstance(inner_url, str) and inner_url.strip():
            return inner_url.strip()
        return None
    except:
        return None


def wait_for_function_release(
    client: VeFaaSClient,
    function_id: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS
) -> dict:
    """Wait for function release to complete."""
    start_time = time.time()
    last_status = ""

    while time.time() - start_time < timeout_seconds:
        try:
            result = client.get_release_status(function_id)
            status = result.get("Result", {}).get("Status", "")

            if status != last_status:
                logger.info(f"[release] Function release status: {status}")
                last_status = status

            if status.lower() == "done":
                return {"success": True, "status": status}

            if status.lower() == "failed":
                msg = result.get("Result", {}).get("StatusMessage", "")
                raise ValueError(f"Function release failed: {msg}")

        except ValueError:
            raise
        except Exception as e:
            logger.warning(f"[release] Error checking status: {e}")

        time.sleep(poll_interval_seconds)

    raise ValueError(f"Function release timed out after {timeout_seconds} seconds")


def wait_for_application_deploy(
    client: VeFaaSClient,
    application_id: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS
) -> dict:
    """Wait for application deployment to complete."""
    start_time = time.time()
    last_status = ""

    while time.time() - start_time < timeout_seconds:
        try:
            result = client.get_application(application_id)
            app = result.get("Result", {})
            status = app.get("Status", "")

            if status != last_status:
                logger.info(f"[deploy] Application status: {status}")
                last_status = status

            if status.lower() == "deploy_success":
                access_url = extract_access_url_from_cloud_resource(app.get("CloudResource"))
                return {"success": True, "access_url": access_url}

            if status.lower() in ("deploy_fail", "deleted", "delete_fail"):
                # Try to get detailed error from GetReleaseStatus (like vefaas-cli)
                error_details = {}
                function_id = None
                try:
                    # Try to get function_id from CloudResource first (like get_application_detail)
                    cloud_resource_str = app.get("CloudResource", "")
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
                        config_str = app.get("Config", "")
                        if config_str:
                            try:
                                config_data = json.loads(config_str)
                                function_id = config_data.get("function", {}).get("function_id")
                            except:
                                pass

                    if function_id:
                        rel_result = client.get_release_status(function_id)
                        rel = rel_result.get("Result", {})
                        status_msg = rel.get("StatusMessage", "").strip()
                        if status_msg:
                            error_details["error_message"] = status_msg
                        log_url = rel.get("FailedInstanceLogs", "").strip()
                        if log_url:
                            error_details["error_logs_uri"] = log_url
                        error_details["function_id"] = function_id
                except Exception as ex:
                    logger.debug(f"Failed to get release status error details: {ex}")

                console_url = f"https://console.volcengine.com/vefaas/region:vefaas+{client.region}/application/detail/{application_id}"

                # Build detailed error message
                error_parts = [f"Application deployment failed ({status})"]
                if error_details.get("error_message"):
                    error_parts.append(f"Error: {error_details['error_message']}")
                if error_details.get("error_logs_uri"):
                    error_parts.append(f"Logs: {error_details['error_logs_uri']}")
                error_parts.append(f"Console: {console_url}")

                raise ValueError(". ".join(error_parts))

        except ValueError:
            raise
        except Exception as e:
            logger.warning(f"[deploy] Error checking status: {e}")

        time.sleep(poll_interval_seconds)

    raise ValueError(f"Deployment timed out after {timeout_seconds} seconds")


def wait_for_dependency_install(
    client: VeFaaSClient,
    function_id: str,
    timeout_seconds: int = 300,
    poll_interval_seconds: int = 5
) -> dict:
    """Wait for Python dependency installation to complete."""
    start_time = time.time()
    last_status = ""

    while time.time() - start_time < timeout_seconds:
        try:
            result = client.get_dependency_install_status(function_id)
            status = result.get("Result", {}).get("Status", "")

            if status != last_status:
                logger.info(f"[dependency] Installation status: {status}")
                last_status = status

            if status.lower() in ("succeeded", "success", "done"):
                return {"success": True, "status": status}

            if status.lower() == "failed":
                raise ValueError("Dependency installation failed")

        except ValueError:
            raise
        except Exception as e:
            logger.warning(f"[dependency] Error checking status: {e}")

        time.sleep(poll_interval_seconds)

    raise ValueError(f"Dependency installation timed out after {timeout_seconds} seconds")


def _run_build_command(project_path: str, build_command: str):
    """Run build command in project directory."""
    logger.info(f"[build] Running: {build_command}")
    result = subprocess.run(
        build_command,
        shell=True,
        cwd=project_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ValueError(f"Build failed: {result.stderr or result.stdout}")
    logger.info("[build] Build completed successfully")


def package_directory(directory: str, base_dir: Optional[str] = None, include_gitignore: bool = True) -> bytes:
    """
    Package directory into a zip file using pathspec for gitignore-style filtering.

    Args:
        directory: Directory to package
        base_dir: Project root for reading ignore files (defaults to directory)
        include_gitignore: Whether to include .gitignore patterns
            - True: Python projects (source code deployment)
            - False: Built output or function code upload (only .vefaasignore)

    Returns:
        Zip file bytes
    """
    if base_dir is None:
        base_dir = directory

    # Load ignore patterns based on scenario
    gitignore_patterns = read_gitignore_patterns(base_dir) if include_gitignore else []
    vefaasignore_patterns = read_vefaasignore_patterns(base_dir)
    spec = create_ignore_filter(gitignore_patterns, vefaasignore_patterns)

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(directory):
            rel_root = os.path.relpath(root, directory)
            if rel_root == ".":
                rel_root = ""

            # Filter directories in-place to prevent descending into ignored dirs
            dirs[:] = [
                d for d in dirs
                if not spec.match_file(f"{rel_root}/{d}" if rel_root else d)
                and not spec.match_file(f"{rel_root}/{d}/" if rel_root else f"{d}/")
            ]

            for file in files:
                arcname = f"{rel_root}/{file}" if rel_root else file

                # Skip files matching ignore patterns
                if spec.match_file(arcname):
                    continue

                file_path = os.path.join(root, file)
                zf.write(file_path, arcname)

    buffer.seek(0)
    zip_bytes = buffer.read()
    return zip_bytes


def deploy_application(config: DeployConfig, client: VeFaaSClient) -> DeployResult:
    """
    Deploy an application to veFaaS.

    Correct flow (from vefaas-cli):
    1. Detect project configuration
    2. Build project (if build_command exists and not skip_build)
    3. Package output directory
    4. Upload to TOS
    5. Create/Update function with Source pointing to TOS
    6. Wait for dependency installation (Python)
    7. Release function
    8. Create application (if needed)
    9. Release application

    Args:
        config: Deployment configuration
        client: VeFaaSClient instance

    Returns:
        DeployResult with IDs and URLs
    """
    result = DeployResult()

    def log(msg: str):
        """Add message to result logs"""
        result.logs.append(msg)
        logger.info(f"[deploy] {msg}")

    try:
        # Validate
        if not os.path.isabs(config.project_path):
            raise ValueError(f"project_path must be absolute, got: {config.project_path}")
        if not os.path.exists(config.project_path):
            raise ValueError(f"project_path does not exist: {config.project_path}")

        # Read existing config if application_id not provided
        # Only use config's application_id if regions match (cross-region deployment needs new app)
        existing_config = read_config(config.project_path)
        if existing_config:
            config_region = existing_config.function.region or "cn-beijing"
            if config_region == client.region:
                if not config.application_id and existing_config.function.application_id:
                    config.application_id = existing_config.function.application_id
                    log(f"[config] Using application_id from config: {config.application_id}")
            else:
                log(f"[config] Config region ({config_region}) differs from target region ({client.region}), will create new application")

        if not config.name and not config.application_id:
            raise ValueError("Must provide name or application_id")

        # 0. Early check for duplicate application name
        if config.name and not config.application_id:
            existing_app_id = client.find_application_by_name(config.name)
            if existing_app_id:
                raise ValueError(
                    f"Application name '{config.name}' already exists (ID: {existing_app_id}). "
                    f"To update this application, pass application_id='{existing_app_id}' parameter."
                )

        # 0.5 Early check: if updating existing app and deployment is in progress, return early
        if config.application_id:
            try:
                app_status = client.get_application(config.application_id).get("Result", {})
                current_status = app_status.get("Status", "").lower()
                if current_status in ("deploying", "releasing", "deploy_pendding"):
                    result.application_id = config.application_id
                    result.app_console_url = get_application_console_url(config.application_id, client.region)
                    result.error = (
                        f"Deployment is already in progress (status: {current_status}). "
                        "Wait for completion, or call get_application_detail to check status."
                    )
                    return result

                # Early check: validate Application SourceType (only 'function' type is supported)
                source_type = app_status.get("SourceType", "")
                if source_type and source_type != "function":
                    raise ValueError(
                        f"Application {config.application_id} has SourceType '{source_type}' which is not compatible with code deployment via MCP. "
                        "Only 'function' type applications are supported. "
                        "Please delete the .vefaas/config.json and vefaas.yaml files, then use 'name' parameter to create a new custom application."
                    )
            except ValueError:
                raise
            except Exception as e:
                log(f"[warning] Could not check application status: {e}")

        # 1. Detect project
        log("[1/7] Detecting project configuration...")
        detection = auto_detect(config.project_path)
        log(f"  → Detected: framework={detection.framework}, runtime={detection.runtime}")

        # Apply user overrides
        build_command = config.build_command or detection.build_command
        output_path = config.output_path or detection.output_path or "."
        start_command = config.start_command or detection.start_command
        port = config.port or detection.port
        is_python = "python" in detection.runtime.lower()

        # Validate start_command is required
        if not start_command:
            raise ValueError(
                "start_command is required but not provided. "
                "Please provide start_command parameter, e.g.:\n"
                "  - Python FastAPI: 'python -m uvicorn main:app --host 0.0.0.0 --port 8080'\n"
                "  - Python Flask: 'python -m flask run --host 0.0.0.0 --port 8080'\n"
                "  - Node.js: 'node server.js'\n"
                "  - Static site: 'npx serve . -l 8080' (serves current dir after build)\n"
                "Or call detect_project first to auto-detect the configuration."
            )

        # Validate build_command is required for non-Python runtimes (unless skip_build)
        if not is_python and not build_command and not config.skip_build:
            raise ValueError(
                "build_command is required for non-Python runtimes but not provided. "
            )

        # Validate port is required and remind about alignment with start_command
        if not port:
            raise ValueError(
                "port is required but not provided. "
                "Please provide port parameter.\n"
                "IMPORTANT: The port must match the actual listening port in your start_command.\n"
            )

        # 2. Build project (if needed)
        if not config.skip_build and build_command and not is_python:
            log(f"[2/7] Building project: {build_command}")
            _run_build_command(config.project_path, build_command)
            log("  → Build completed")

            # For static sites, generate DefaultCaddyFile in output directory
            if detection.is_static:
                root_caddy = os.path.join(config.project_path, DEFAULT_CADDYFILE_NAME)
                out_dir = os.path.join(config.project_path, output_path) if output_path and output_path != "./" and output_path != "." else config.project_path
                target_caddy = os.path.join(out_dir, DEFAULT_CADDYFILE_NAME)

                if os.path.exists(root_caddy):
                    # Copy existing Caddyfile from project root to output
                    import shutil
                    os.makedirs(out_dir, exist_ok=True)
                    shutil.copy2(root_caddy, target_caddy)
                    log(f"  → Existing {DEFAULT_CADDYFILE_NAME} copied to output")
                else:
                    # Generate new Caddyfile
                    ensure_caddyfile_in_output(config.project_path, output_path)
                    log(f"  → {DEFAULT_CADDYFILE_NAME} generated for static site")
        else:
            log("[2/7] Build skipped")
            # Even if build is skipped, static sites still need Caddyfile
            if detection.is_static:
                out_dir = os.path.join(config.project_path, output_path) if output_path and output_path != "./" and output_path != "." else config.project_path
                target_caddy = os.path.join(out_dir, DEFAULT_CADDYFILE_NAME)
                if not os.path.exists(target_caddy):
                    ensure_caddyfile_in_output(config.project_path, output_path)
                    log(f"  → {DEFAULT_CADDYFILE_NAME} generated for static site")

        # 3. Package output directory
        # Python: include .gitignore (source code deployment)
        # Non-Python: only .vefaasignore (built output doesn't need gitignore)
        log("[3/7] Packaging code...")
        package_path = os.path.join(config.project_path, output_path) if output_path != "." else config.project_path
        if not os.path.exists(package_path):
            package_path = config.project_path  # Fallback to project root

        zip_bytes = package_directory(package_path, base_dir=config.project_path, include_gitignore=is_python)
        log(f"  → Packaged: {len(zip_bytes) / 1024:.1f} KB")

        # 4. Upload to TOS
        log("[4/7] Uploading to cloud storage...")
        source_location = client.upload_to_tos(zip_bytes)
        log("  → Upload completed")

        # 5. Create or Update function
        target_function_id = None
        target_application_id = config.application_id
        function_name = None

        # If application_id is provided, get the function_id from app details
        if config.application_id:
            log(f"[5/7] Getting function from application: {config.application_id}")
            try:
                app_detail = client.get_application(config.application_id)
                app_data = app_detail.get("Result", {})

                # Try to get function_id from CloudResource first (like vefaas-cli)
                cloud_resource_str = app_data.get("CloudResource", "")
                if cloud_resource_str:
                    try:
                        cloud_resource = json.loads(cloud_resource_str)
                        # CloudResource format: {"framework": {"function_id": "xxx", ...}}
                        keys = list(cloud_resource.keys())
                        if keys:
                            first_key = keys[0]
                            target_function_id = cloud_resource.get(first_key, {}).get("function_id")
                    except json.JSONDecodeError:
                        pass

                # Fallback: try to get from Config
                if not target_function_id:
                    config_str = app_data.get("Config", "")
                    if config_str:
                        try:
                            config_data = json.loads(config_str)
                            target_function_id = config_data.get("function", {}).get("function_id")
                        except json.JSONDecodeError:
                            pass

                if not target_function_id:
                    raise ValueError(
                        f"Could not find function_id in application {config.application_id}. "
                        "This application may not have a function associated with it, or it was created without a function. "
                        "Please use 'name' parameter to create a new application instead."
                    )

                log(f"  → Found function: {target_function_id}")
            except json.JSONDecodeError:
                raise ValueError(f"Could not parse application data for {config.application_id}")

        if config.application_id:
            # Update existing function
            log(f"[5/7] Updating function: {target_function_id}")
            client.update_function(
                function_id=target_function_id,
                source=source_location,
                command=start_command,
                port=port,
                runtime=detection.runtime,
            )
            log("  → Function updated")
        elif config.name:
            log(f"[5/7] Creating function: {config.name}")
            create_resp = client.create_function(
                name=config.name,
                runtime=detection.runtime,
                command=start_command,
                port=port,
                source=source_location,
                build_command=build_command if not is_python else None,
                output_path=output_path if not is_python else None,
            )
            func_result = create_resp.get("Result", {})
            target_function_id = func_result.get("Id")
            function_name = func_result.get("Name")
            log(f"  → Function created: {target_function_id}")

        if not target_function_id:
            raise ValueError("Unable to determine target function ID")

        result.function_id = target_function_id
        result.function_name = function_name

        # 6. Wait for dependency installation (Python)
        if is_python:
            log("[6/7] Waiting for dependency installation...")
            try:
                wait_for_dependency_install(client, target_function_id)
                log("  → Dependencies installed")
            except Exception as e:
                log(f"  → Dependency check: {e}")
        else:
            log("[6/7] Dependency installation skipped")

        # 7. Create application and deploy
        access_url = None

        if config.name and not config.application_id:
            # New application
            log("[7/7] Creating and deploying application...")
            gateway_name = config.gateway_name or client.get_usable_gateway()
            if not gateway_name:
                raise ValueError(
                    "No available API gateway found. "
                    "Please visit https://console.volcengine.com/veapig to create a running gateway, then retry."
                )

            app_name = f"{config.name}".lower()
            create_app_resp = client.create_application(app_name, target_function_id, gateway_name)
            target_application_id = create_app_resp.get("Result", {}).get("Id")
            log(f"  → Application created: {target_application_id}")

            # Release application
            if target_application_id:
                log("  → Releasing application...")
                client.release_application(target_application_id)
                log("  → Waiting for deployment...")
                deploy_status = wait_for_application_deploy(client, target_application_id, timeout_seconds=DEPLOY_TIMEOUT_SECONDS)
                access_url = deploy_status.get("access_url")

                # If access_url not from deploy status, fetch from app details
                if not access_url:
                    try:
                        app_detail = client.get_application(target_application_id)
                        cloud_resource = app_detail.get("Result", {}).get("CloudResource", "")
                        access_url = extract_access_url_from_cloud_resource(cloud_resource)
                    except:
                        pass

                log("  → Deployment completed!")
        elif config.application_id:
            # Update existing application - re-release it
            log("[7/7] Re-deploying existing application...")
            client.release_application(target_application_id)
            log("  → Waiting for deployment...")
            deploy_status = wait_for_application_deploy(client, target_application_id, timeout_seconds=DEPLOY_TIMEOUT_SECONDS)
            access_url = deploy_status.get("access_url")

            if not access_url:
                try:
                    app_detail = client.get_application(target_application_id)
                    cloud_resource = app_detail.get("Result", {}).get("CloudResource", "")
                    access_url = extract_access_url_from_cloud_resource(cloud_resource)
                except:
                    pass

            log("  → Deployment completed!")
        else:
            log("[7/7] Application deployment skipped")

        result.application_id = target_application_id
        result.function_id = target_function_id
        result.access_url = access_url
        if target_application_id:
            result.app_console_url = get_application_console_url(target_application_id, client.region)

        result.success = True

        # Save config to .vefaas/config.json and vefaas.yaml
        try:
            save_config = VefaasConfig(
                function=FunctionConfig(
                    id=target_function_id or "",
                    runtime=detection.runtime,
                    region=client.region,
                    application_id=target_application_id,
                ),
                name=config.name or function_name,
                command=start_command,
            )
            if access_url:
                save_config.triggers = TriggerConfig(
                    type="apig",
                    system_url=access_url,
                )
            write_config(config.project_path, save_config)
            log("[config] Saved .vefaas/config.json and vefaas.yaml")
        except Exception as e:
            log(f"[config] Warning: Failed to save config: {e}")

        log("Deployed successfully!")
    except Exception as e:
        result.error = str(e)
        result.success = False
        log(f"Deployment failed: {e}")

    return result
