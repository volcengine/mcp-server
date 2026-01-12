import os
import shutil
import tempfile
import unittest
import zipfile
from io import BytesIO

from mcp_server_vefaas_function.vefaas_server import zip_and_encode_folder
from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import (
    package_directory,
    read_gitignore_patterns,
    read_vefaasignore_patterns,
    create_ignore_filter,
    DEFAULT_VEFAASIGNORE,
)


class TestPackageDirectory(unittest.TestCase):
    """Test directory packaging functionality - no network credentials required"""

    def setUp(self):
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()
        # Create test files and directories
        os.makedirs(os.path.join(self.temp_dir, "__pycache__"))
        os.makedirs(os.path.join(self.temp_dir, "subfolder"))
        os.makedirs(os.path.join(self.temp_dir, ".git"))
        with open(os.path.join(self.temp_dir, "file1.py"), "w") as f:
            f.write("print('hello')")
        with open(os.path.join(self.temp_dir, "file2.pyc"), "w") as f:
            f.write("compiled")
        with open(os.path.join(self.temp_dir, "__pycache__", "cached.pyc"), "w") as f:
            f.write("cached")
        with open(os.path.join(self.temp_dir, "subfolder", "file3.txt"), "w") as f:
            f.write("text content")
        with open(os.path.join(self.temp_dir, ".git", "config"), "w") as f:
            f.write("git config")
        with open(os.path.join(self.temp_dir, ".gitignore"), "w") as f:
            f.write("*.log\n")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_zip_and_encode_folder_basic(self):
        """Test zip_and_encode_folder basic functionality"""
        zip_bytes, size, err = zip_and_encode_folder(self.temp_dir)

        self.assertIsInstance(zip_bytes, bytes)
        self.assertIsInstance(size, int)
        self.assertIsNone(err)
        self.assertGreater(size, 0)

        # Verify zip content
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zipf:
            names = zipf.namelist()
            # Should contain normal files
            self.assertIn("file1.py", names)
            self.assertIn("subfolder/file3.txt", names)
            # Default ignore patterns should exclude __pycache__ and .git
            self.assertNotIn("__pycache__/cached.pyc", names)
            # .git directory should be excluded (default .vefaasignore rules)
            git_dir_files = [n for n in names if n.startswith(".git/")]
            self.assertEqual(len(git_dir_files), 0, f"Should not contain .git/ directory files, but found: {git_dir_files}")

    def test_package_directory_with_gitignore(self):
        """Test package_directory with .gitignore rules applied"""
        # Create a log file that should be ignored by .gitignore
        with open(os.path.join(self.temp_dir, "test.log"), "w") as f:
            f.write("log content")

        zip_bytes = package_directory(self.temp_dir, include_gitignore=True)

        with zipfile.ZipFile(BytesIO(zip_bytes)) as zipf:
            names = zipf.namelist()
            # *.log should be excluded by .gitignore
            self.assertNotIn("test.log", names)
            # Normal files should be retained
            self.assertIn("file1.py", names)

    def test_package_directory_without_gitignore(self):
        """Test package_directory without .gitignore rules (function code upload scenario)"""
        # Create a log file that would normally be ignored by .gitignore
        with open(os.path.join(self.temp_dir, "test.log"), "w") as f:
            f.write("log content")

        zip_bytes = package_directory(self.temp_dir, include_gitignore=False)

        with zipfile.ZipFile(BytesIO(zip_bytes)) as zipf:
            names = zipf.namelist()
            # .gitignore not applied, so *.log should be retained
            self.assertIn("test.log", names)
            # Normal files should be retained
            self.assertIn("file1.py", names)
            # But .vefaasignore default rules should still apply
            self.assertNotIn("__pycache__/cached.pyc", names)

    def test_read_gitignore_patterns(self):
        """Test reading .gitignore patterns"""
        patterns = read_gitignore_patterns(self.temp_dir)
        self.assertIn("*.log", patterns)

    def test_read_vefaasignore_patterns_creates_default(self):
        """Test that .vefaasignore default file is auto-created when not exists"""
        # Confirm .vefaasignore does not exist
        vefaasignore_path = os.path.join(self.temp_dir, ".vefaasignore")
        if os.path.exists(vefaasignore_path):
            os.remove(vefaasignore_path)

        patterns = read_vefaasignore_patterns(self.temp_dir)

        # Should create default file
        self.assertTrue(os.path.exists(vefaasignore_path))
        # Should contain default patterns
        self.assertTrue(len(patterns) > 0)

    def test_create_ignore_filter(self):
        """Test creating ignore filter"""
        gitignore_patterns = ["*.log", "temp/"]
        vefaasignore_patterns = [".git/", "__pycache__/"]

        spec = create_ignore_filter(gitignore_patterns, vefaasignore_patterns)

        # Verify filter works correctly
        self.assertTrue(spec.match_file("test.log"))
        self.assertTrue(spec.match_file(".git/config"))
        self.assertTrue(spec.match_file("__pycache__/"))
        self.assertFalse(spec.match_file("main.py"))


class TestCaddyfileGeneration(unittest.TestCase):
    """Test cases for Caddyfile generation functionality"""

    def setUp(self):
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Delete temporary directory
        shutil.rmtree(self.temp_dir)

    def test_render_default_caddyfile_content(self):
        """Test that default Caddyfile content is generated correctly"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import render_default_caddyfile_content

        content = render_default_caddyfile_content()

        # Verify content contains key configurations
        self.assertIn(":8000", content)  # Listening port
        self.assertIn("root * .", content)  # Static file root directory
        self.assertIn("file_server", content)  # File server directive
        self.assertIn("try_files", content)  # SPA routing support
        self.assertIn("@unsafePath", content)  # Secure path configuration
        self.assertIn("Cache-Control", content)  # Cache strategy

    def test_ensure_caddyfile_in_output_creates_file(self):
        """Test that ensure_caddyfile_in_output creates file in output directory"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import ensure_caddyfile_in_output, DEFAULT_CADDYFILE_NAME

        # Create output subdirectory
        output_path = "dist"
        os.makedirs(os.path.join(self.temp_dir, output_path), exist_ok=True)

        # Generate Caddyfile
        result = ensure_caddyfile_in_output(self.temp_dir, output_path)

        # Verify file creation
        expected_path = os.path.join(self.temp_dir, output_path, DEFAULT_CADDYFILE_NAME)
        self.assertEqual(result, expected_path)
        self.assertTrue(os.path.exists(expected_path))

        # Verify content
        with open(expected_path, "r") as f:
            content = f.read()
        self.assertIn(":8000", content)
        self.assertIn("file_server", content)

    def test_ensure_caddyfile_in_output_root_directory(self):
        """Test Caddyfile generation in project root (output_path = './')"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import ensure_caddyfile_in_output, DEFAULT_CADDYFILE_NAME

        # Generate to root directory
        result = ensure_caddyfile_in_output(self.temp_dir, "./")

        # Verify file creation in root directory
        expected_path = os.path.join(self.temp_dir, DEFAULT_CADDYFILE_NAME)
        self.assertEqual(result, expected_path)
        self.assertTrue(os.path.exists(expected_path))

    def test_ensure_caddyfile_creates_output_dir_if_not_exists(self):
        """Test that output directory is created if it doesn't exist"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import ensure_caddyfile_in_output, DEFAULT_CADDYFILE_NAME

        output_path = "new_output_dir"

        # Confirm directory does not exist
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, output_path)))

        # Generate Caddyfile
        result = ensure_caddyfile_in_output(self.temp_dir, output_path)

        # Verify directory and file are both created
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, output_path)))
        self.assertTrue(os.path.exists(result))


class TestDetector(unittest.TestCase):
    """Test cases for project detector"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_detect_vite_project_is_static(self):
        """Test that Vite project without SSR is detected as static"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.detector import auto_detect

        # Create Vite project structure
        pkg = {
            "name": "test-vite",
            "devDependencies": {"vite": "^5.0.0"},
            "scripts": {"build": "vite build", "preview": "vite preview"}
        }
        with open(os.path.join(self.temp_dir, "package.json"), "w") as f:
            import json
            json.dump(pkg, f)

        result = auto_detect(self.temp_dir)

        self.assertEqual(result.framework, "vite")
        self.assertEqual(result.runtime, "native-node20/v1")
        self.assertTrue(result.is_static)
        self.assertIn("caddy", result.start_command.lower())

    def test_detect_fastapi_project(self):
        """Test that FastAPI project is detected correctly"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.detector import auto_detect

        # Create FastAPI project structure
        with open(os.path.join(self.temp_dir, "requirements.txt"), "w") as f:
            f.write("fastapi\nuvicorn\n")
        with open(os.path.join(self.temp_dir, "app.py"), "w") as f:
            f.write("from fastapi import FastAPI\napp = FastAPI()\n")

        result = auto_detect(self.temp_dir)

        self.assertEqual(result.framework, "fastapi")
        self.assertEqual(result.runtime, "native-python3.12/v1")
        self.assertFalse(result.is_static)
        self.assertIn("uvicorn", result.start_command)

    def test_detect_flask_project(self):
        """Test that Flask project is detected correctly"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.detector import auto_detect

        # Create Flask project structure
        with open(os.path.join(self.temp_dir, "requirements.txt"), "w") as f:
            f.write("flask\ngunicorn\n")
        with open(os.path.join(self.temp_dir, "app.py"), "w") as f:
            f.write("from flask import Flask\napp = Flask(__name__)\n")

        result = auto_detect(self.temp_dir)

        self.assertEqual(result.framework, "flask")
        self.assertEqual(result.runtime, "native-python3.12/v1")
        self.assertFalse(result.is_static)


class TestConfig(unittest.TestCase):
    """Test cases for configuration reading/writing"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_write_and_read_config(self):
        """Test writing and reading configuration"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.config import (
            write_config, read_config, VefaasConfig, FunctionConfig
        )

        config = VefaasConfig(
            function=FunctionConfig(
                id="test-func-id",
                region="cn-beijing",
                runtime="native-python3.12/v1",
                application_id="test-app-id",
            ),
            name="test-app",
            command="./run.sh",
        )

        # Write config
        write_config(self.temp_dir, config)

        # Verify files exist
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, ".vefaas", "config.json")))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "vefaas.yaml")))

        # Read config back
        loaded_config = read_config(self.temp_dir)
        self.assertIsNotNone(loaded_config)
        self.assertEqual(loaded_config.function.id, "test-func-id")
        self.assertEqual(loaded_config.function.region, "cn-beijing")
        self.assertEqual(loaded_config.function.application_id, "test-app-id")

    def test_get_linked_ids(self):
        """Test getting linked IDs from config"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.config import (
            write_config, get_linked_ids, VefaasConfig, FunctionConfig
        )

        config = VefaasConfig(
            function=FunctionConfig(
                id="func-123",
                application_id="app-456",
            ),
        )
        write_config(self.temp_dir, config)

        func_id, app_id = get_linked_ids(self.temp_dir)
        self.assertEqual(func_id, "func-123")
        self.assertEqual(app_id, "app-456")


class TestGenerateAppName(unittest.TestCase):
    """Test cases for app name generation"""

    def test_generate_app_name_from_path(self):
        """Test generating app name from project path"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import generate_app_name_from_path

        # Test with simple path
        name = generate_app_name_from_path("/path/to/my-project")
        self.assertTrue(name.startswith("my-project-"))
        self.assertEqual(len(name), len("my-project-") + 6)  # 6 char suffix

    def test_generate_app_name_handles_special_chars(self):
        """Test that special characters are replaced"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import generate_app_name_from_path

        name = generate_app_name_from_path("/path/to/My_Project.Name")
        # Should be lowercase with hyphens
        self.assertTrue(name.startswith("my-project-name-"))

    def test_generate_app_name_truncates_long_names(self):
        """Test that long names are truncated"""
        from mcp_server_vefaas_function.vefaas_cli_sdk.deploy import generate_app_name_from_path

        name = generate_app_name_from_path("/path/to/this-is-a-very-long-project-name-that-should-be-truncated")
        # Base name should be max 20 chars + hyphen + 6 char suffix
        self.assertLessEqual(len(name), 20 + 1 + 6)


if __name__ == "__main__":
    unittest.main()
