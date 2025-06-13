import base64
import io
import tempfile
import unittest
import os
import zipfile

import pyzipper

from vefaas_server import does_function_exist, create_zip_base64, python_zip_implementation


class TestVeFaaSServerIntegration(unittest.TestCase):
    def setUp(self):
        # Check if credentials are available
        self.ak = os.environ.get("VOLCENGINE_ACCESS_KEY")
        self.sk = os.environ.get("VOLCENGINE_SECRET_KEY")
        self.alt_ak = os.environ.get("VOLC_ACCESSKEY")
        self.alt_sk = os.environ.get("VOLC_SECRETKEY")
        if not self.ak or not self.sk or not self.alt_ak or not self.alt_sk:
            self.assertFalse(
                "VOLCENGINE_ACCESS_KEY or VOLCENGINE_SECRET_KEY or VOLC_ACCESSKEY or VOLC_SECRETKEY environment variables not set"
            )

    def test_does_function_exist_with_real_credentials(self):
        # Test with a known non-existent function ID
        non_existent_id = "non-existent-function-123"
        result = does_function_exist(non_existent_id, "cn-beijing")
        self.assertFalse(result)

        # Note: To test a positive case, you would need a real function ID
        # that exists in your account. You could add something like:
        # known_function_id = "your-real-function-id"
        # result = does_function_exist(known_function_id, "cn-beijing")
        # self.assertTrue(result)

    def test_create_zip_base64(self):
        test_files = {
            "hello.txt": "Hello, world!",
            "data.json": b'{"key": "value"}'
        }

        zip_b64 = create_zip_base64(test_files)

        zip_bytes = base64.b64decode(zip_b64)

        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_file:
            names = zip_file.namelist()
            assert "hello.txt" in names
            assert "data.json" in names

            assert zip_file.read("hello.txt").decode("utf-8") == "Hello, world!"
            assert zip_file.read("data.json") == b'{"key": "value"}'

            for info in zip_file.infolist():
                self.assertEqual((info.external_attr >> 16), 0o777)

    def test_python_zip_implementation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test.sh")
            with open(file_path, "w") as f:
                f.write("#!/bin/bash\necho hello\n")
            os.chmod(file_path, 0o644)

            zip_bytes = python_zip_implementation(tmpdir)

            zip_path = os.path.join(tmpdir, "test.zip")
            with open(zip_path, "wb") as fzip:
                fzip.write(zip_bytes)

            with pyzipper.AESZipFile(zip_path, 'r') as zipf:
                namelist = zipf.namelist()
                assert "test.sh" in namelist

                info = zipf.getinfo("test.sh")
                perm = (info.external_attr >> 16) & 0o777
                assert perm == 0o755, f"Expected 755 permission but got {oct(perm)}"

                content = zipf.read("test.sh").decode()
                assert "echo hello" in content


if __name__ == "__main__":
    unittest.main()
