#!/usr/bin/env python3
"""
veFaaS MCP Server Test Script

This script tests the full workflow of veFaaS function and application deployment.

Test Scenarios:
1. Application Deployment (Python/Node.js)
   - Deploy new application
   - Update and redeploy

Usage:
    # Run all tests
    python test_e2e.py

    # Run specific scenario
    python test_e2e.py --scenario app-python
    python test_e2e.py --scenario app-node

Environment Variables:
    VOLCENGINE_ACCESS_KEY_ID: Access Key ID (required)
    VOLCENGINE_SECRET_ACCESS_KEY: Secret Access Key (required)
    VOLCENGINE_SECURITY_TOKEN: Security Token (optional, for STS)
    TEST_REGION: Region to test (default: cn-beijing)
"""

from mcp_server_vefaas_function.vefaas_cli_sdk import (
    VeFaaSClient,
    DeployConfig,
    deploy_application,
    auto_detect,
)
import os
import sys
import json
import time
import shutil
import tempfile
import argparse
import logging

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ========== Test Project Templates ==========

PYTHON_PROJECT = {
    "app.py": '''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Python!"}

@app.get("/health")
def health():
    return {"status": "ok"}
''',
    "requirements.txt": "fastapi\nuvicorn\n",
    "run.sh": '''#!/bin/bash
exec python -m uvicorn app:app --host 0.0.0.0 --port 8000
''',
}

PYTHON_PROJECT_UPDATED = {
    "app.py": '''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Python! (Updated)"}

@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0"}
''',
    "requirements.txt": "fastapi\nuvicorn\n",
    "run.sh": '''#!/bin/bash
exec python -m uvicorn app:app --host 0.0.0.0 --port 8000
''',
}

NODE_PROJECT = {
    "index.js": '''const http = require('http');

const server = http.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({status: 'ok'}));
    } else {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({message: 'Hello from Node.js!'}));
    }
});

server.listen(8000, '0.0.0.0', () => {
    console.log('Server running on port 8000');
});
''',
    "package.json": '''{
  "name": "test-node-app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  }
}
''',
}

NODE_PROJECT_UPDATED = {
    "index.js": '''const http = require('http');

const server = http.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({status: 'ok', version: '2.0'}));
    } else {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({message: 'Hello from Node.js! (Updated)'}));
    }
});

server.listen(8000, '0.0.0.0', () => {
    console.log('Server running on port 8000');
});
''',
    "package.json": '''{
  "name": "test-node-app",
  "version": "2.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  }
}
''',
}


# ========== Helper Functions ==========

def get_credentials():
    """Get credentials from environment variables"""
    ak = os.environ.get("VOLCENGINE_ACCESS_KEY_ID")
    sk = os.environ.get("VOLCENGINE_SECRET_ACCESS_KEY")
    token = os.environ.get("VOLCENGINE_SECURITY_TOKEN")

    if not ak or not sk:
        raise ValueError(
            "Missing credentials. Set VOLCENGINE_ACCESS_KEY_ID and VOLCENGINE_SECRET_ACCESS_KEY"
        )

    return ak, sk, token


def create_temp_project(files: dict, name: str) -> str:
    """Create a temporary project directory with given files"""
    temp_dir = tempfile.mkdtemp(prefix=f"vefaas_test_{name}_")

    for filename, content in files.items():
        filepath = os.path.join(temp_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)

        # Make .sh files executable
        if filename.endswith(".sh"):
            os.chmod(filepath, 0o755)

    logger.info(f"Created temp project: {temp_dir}")
    return temp_dir


def update_project(project_path: str, files: dict):
    """Update project files"""
    for filename, content in files.items():
        filepath = os.path.join(project_path, filename)
        with open(filepath, "w") as f:
            f.write(content)
    logger.info(f"Updated project files in: {project_path}")


def cleanup_project(project_path: str):
    """Remove temporary project directory"""
    if project_path and os.path.exists(project_path):
        shutil.rmtree(project_path)
        logger.info(f"Cleaned up: {project_path}")


def generate_unique_name(prefix: str) -> str:
    """Generate unique name for testing"""
    import random
    import string
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}-{suffix}"


# ========== Test Scenarios ==========

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.steps = []
        self.success = True
        self.error = None
        self.function_id = None
        self.application_id = None
        self.access_url = None

    def add_step(self, step: str, success: bool, details: str = ""):
        self.steps.append({
            "step": step,
            "success": success,
            "details": details
        })
        if not success:
            self.success = False

    def summary(self) -> str:
        lines = [f"\n{'='*60}", f"Test: {self.name}", f"Result: {'✅ PASSED' if self.success else '❌ FAILED'}", ""]

        for step in self.steps:
            icon = "✅" if step["success"] else "❌"
            lines.append(f"  {icon} {step['step']}")
            if step["details"]:
                lines.append(f"      {step['details']}")

        if self.function_id:
            lines.append(f"\n  Function ID: {self.function_id}")
        if self.application_id:
            lines.append(f"  Application ID: {self.application_id}")
        if self.access_url:
            lines.append(f"  Access URL: {self.access_url}")

        lines.append("=" * 60)
        return "\n".join(lines)


def test_application_workflow(runtime: str, region: str) -> TestResult:
    """
    Test application deployment workflow using deploy_application:
    1. Deploy new application
    2. Update and redeploy
    """
    result = TestResult(f"Application Workflow ({runtime})")
    project_path = None

    try:
        ak, sk, token = get_credentials()
        client = VeFaaSClient(ak, sk, token, region)

        # Select project template
        if runtime == "python":
            initial_files = PYTHON_PROJECT
            updated_files = PYTHON_PROJECT_UPDATED
            start_command = "./run.sh"
        else:
            initial_files = NODE_PROJECT
            updated_files = NODE_PROJECT_UPDATED
            start_command = "node index.js"

        # Step 1: Create temp project
        project_path = create_temp_project(initial_files, runtime)
        result.add_step("Create temp project", True, project_path)

        # Step 2: Detect project
        detection = auto_detect(project_path)
        result.add_step("Detect project", True, f"Framework: {detection.framework}, Runtime: {detection.runtime}")

        # Step 3: Deploy application (uses deploy_application from SDK)
        app_name = generate_unique_name(f"app-{runtime}")
        logger.info(f"Deploying application: {app_name}")

        config = DeployConfig(
            project_path=project_path,
            name=app_name,
            start_command=start_command,
            port=8000,
            skip_build=True,
        )

        deploy_result = deploy_application(config, client)

        if not deploy_result.success:
            raise ValueError(f"Deployment failed: {deploy_result.error}")

        result.function_id = deploy_result.function_id
        result.application_id = deploy_result.application_id
        result.access_url = deploy_result.access_url
        result.add_step("Deploy application (v1)", True, f"URL: {deploy_result.access_url}")

        # Step 4: Update project files
        update_project(project_path, updated_files)
        result.add_step("Update project files", True)

        # Step 5: Redeploy application (uses deploy_application with application_id)
        config2 = DeployConfig(
            project_path=project_path,
            application_id=deploy_result.application_id,
            start_command=start_command,
            port=8000,
            skip_build=True,
        )

        deploy_result2 = deploy_application(config2, client)

        if not deploy_result2.success:
            raise ValueError(f"Redeployment failed: {deploy_result2.error}")

        result.add_step("Redeploy application (v2)", True)

        logger.info(result.summary())

    except Exception as e:
        result.error = str(e)
        result.add_step("Test execution", False, str(e))
        logger.error(f"Test failed: {e}")

    finally:
        if project_path:
            cleanup_project(project_path)

    return result


def test_function_local_dev_workflow(runtime: str, region: str) -> TestResult:
    """
    Test function local development workflow using MCP tools:
    1. Deploy initial application (to get a function)
    2. Update function code (simulate local development)
    3. Release function

    This simulates the scenario where a developer creates a function,
    then makes local code changes and uses update_function + release_function
    to iterate without going through full deploy_application flow.
    """
    result = TestResult(f"Function Local Dev ({runtime})")
    project_path = None

    # Import the MCP tool functions
    from mcp_server_vefaas_function.vefaas_server import (
        zip_and_encode_folder,
    )
    from mcp_server_vefaas_function.vefaas_cli_sdk import (
        wait_for_function_release,
        wait_for_dependency_install,
    )

    try:
        ak, sk, token = get_credentials()
        client = VeFaaSClient(ak, sk, token, region)

        # Select project template
        if runtime == "python":
            initial_files = PYTHON_PROJECT
            updated_files = PYTHON_PROJECT_UPDATED
            start_command = "./run.sh"
        else:
            initial_files = NODE_PROJECT
            updated_files = NODE_PROJECT_UPDATED
            start_command = "node index.js"

        # Step 1: Create temp project
        project_path = create_temp_project(initial_files, runtime)
        result.add_step("Create temp project", True, project_path)

        # Step 2: Create initial function via deploy_application
        func_name = generate_unique_name(f"func-{runtime}")
        logger.info(f"Creating function via deploy_application: {func_name}")

        config = DeployConfig(
            project_path=project_path,
            name=func_name,
            start_command=start_command,
            port=8000,
            skip_build=True,
        )
        deploy_result = deploy_application(config, client)

        if not deploy_result.success:
            raise ValueError(f"Initial deployment failed: {deploy_result.error}")

        function_id = deploy_result.function_id
        result.function_id = function_id
        result.application_id = deploy_result.application_id
        result.access_url = deploy_result.access_url
        result.add_step("Create function (initial deploy)", True, f"Function ID: {function_id}")

        # Step 3: Update project files (simulate local development)
        update_project(project_path, updated_files)
        result.add_step("Update local files", True, "Simulating code changes")

        # Step 4: Upload new code using update_function pattern
        # (Similar to what MCP update_function tool does internally)
        logger.info(f"Updating function code: {function_id}")

        # Package and upload code
        zip_bytes, size, err = zip_and_encode_folder(project_path)
        if err:
            raise ValueError(f"Failed to package code: {err}")

        source_location = client.upload_to_tos(zip_bytes)
        client.update_function(function_id, source=source_location)
        result.add_step("Update function code", True, f"Uploaded {size} bytes")

        # Step 5: Install dependencies (Python only)
        if runtime == "python":
            try:
                client.create_dependency_install_task(function_id)
                wait_for_dependency_install(client, function_id, timeout_seconds=300)
                result.add_step("Install dependencies", True)
            except Exception as e:
                result.add_step("Install dependencies", False, str(e))

        # Step 6: Release function
        logger.info(f"Releasing function: {function_id}")
        try:
            client.release_function(function_id)
            wait_for_function_release(client, function_id, timeout_seconds=180)
            result.add_step("Release function", True)
        except Exception as e:
            result.add_step("Release function", False, str(e))

        logger.info(result.summary())

    except Exception as e:
        result.error = str(e)
        result.add_step("Test execution", False, str(e))
        logger.error(f"Test failed: {e}")

    finally:
        if project_path:
            cleanup_project(project_path)

    return result


# ========== Main ==========

def main():
    parser = argparse.ArgumentParser(description="veFaaS MCP Server E2E Tests")
    parser.add_argument(
        "--scenario",
        choices=["all", "app-python", "app-node", "func-python", "func-node"],
        default="all",
        help="Test scenario to run"
    )
    parser.add_argument(
        "--region",
        default=os.environ.get("TEST_REGION", "cn-beijing"),
        help="Region to test"
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("veFaaS MCP Server E2E Tests")
    print(f"Region: {args.region}")
    print(f"Scenario: {args.scenario}")
    print("=" * 60 + "\n")

    results = []

    # Application deployment tests
    if args.scenario in ("all", "app-python"):
        results.append(test_application_workflow("python", args.region))

    if args.scenario in ("all", "app-node"):
        results.append(test_application_workflow("node", args.region))

    # Function local development tests
    if args.scenario in ("all", "func-python"):
        results.append(test_function_local_dev_workflow("python", args.region))

    if args.scenario in ("all", "func-node"):
        results.append(test_function_local_dev_workflow("node", args.region))

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r.success)
    failed = len(results) - passed

    for r in results:
        icon = "✅" if r.success else "❌"
        print(f"  {icon} {r.name}")

    print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")
    print("=" * 60 + "\n")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
