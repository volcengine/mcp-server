import os
import shutil
import tempfile
import unittest
import zipfile
from io import BytesIO

import pyzipper

from vefaas_server import python_zip_implementation, zip_and_encode_folder, \
    does_function_exist


class TestVeFaaSServerIntegration(unittest.TestCase):
    def setUp(self):
        # Check if credentials are available
        self.ak = os.environ.get("VOLCENGINE_ACCESS_KEY")
        self.sk = os.environ.get("VOLCENGINE_SECRET_KEY")
        self.alt_ak = os.environ.get("VOLC_ACCESSKEY")
        self.alt_sk = os.environ.get("VOLC_SECRETKEY")
        if (not self.ak or not self.sk) and (not self.alt_ak or not self.alt_sk):
            self.assertFalse(
                "VOLCENGINE_ACCESS_KEY or VOLCENGINE_SECRET_KEY or VOLC_ACCESSKEY or VOLC_SECRETKEY environment variables not set"
            )

        # 创建临时目录
        self.temp_dir = tempfile.mkdtemp()
        # 创建一些测试文件和文件夹
        os.makedirs(os.path.join(self.temp_dir, "__pycache__"))
        os.makedirs(os.path.join(self.temp_dir, "subfolder"))
        with open(os.path.join(self.temp_dir, "file1.py"), "w") as f:
            f.write("print('hello')")
        with open(os.path.join(self.temp_dir, "file2.pyc"), "w") as f:
            f.write("compiled")
        with open(os.path.join(self.temp_dir, "__pycache__", "cached.pyc"),
                  "w") as f:
            f.write("cached")
        with open(os.path.join(self.temp_dir, "subfolder", "file3.txt"), "w") as f:
            f.write("text content")
        with open(os.path.join(self.temp_dir, ".gitignore"), "w") as f:
            f.write("*")

    def tearDown(self):
        # 删除临时目录
        shutil.rmtree(self.temp_dir)

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

    def test_zip_exclude_patterns_with_python_impl(self):
        # 设置排除规则
        exclude_patterns = ["*.pyc", ".gitignore", "*/__pycache__/*"]

        zip_bytes = python_zip_implementation(self.temp_dir, exclude_patterns)
        self.assertIsInstance(zip_bytes, bytes)

        # 解压验证
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zipf:
            names = zipf.namelist()
            print(names)
            # 应该包含 file1.py 和 subfolder/file3.txt
            self.assertIn("file1.py", names)
            self.assertIn("subfolder/file3.txt", names)
            # 不包含排除的文件
            self.assertNotIn("file2.pyc", names)
            self.assertNotIn(".gitignore", names)
            self.assertNotIn("__pycache__/cached.pyc", names)

    def test_zip_with_exclude_patterns_with_system_impl(self):
        exclude_patterns = ["*.pyc", ".gitignore", "*/__pycache__/*"]
        zip_bytes, size, err = zip_and_encode_folder(self.temp_dir, exclude_patterns)

        self.assertIsInstance(zip_bytes, bytes)
        self.assertIsInstance(size, int)
        self.assertIsNone(err)

        # 验证 zip 内容
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zipf:
            names = zipf.namelist()
            print(names)
            # 应该包含 file1.py 和 subfolder/file3.txt
            self.assertIn("file1.py", names)
            self.assertIn("subfolder/file3.txt", names)
            # 不应该包含排除文件
            self.assertNotIn("file2.pyc", names)
            self.assertNotIn(".gitignore", names)
            self.assertNotIn("__pycache__/cached.pyc", names)

    def test_zip_empty_exclude_with_system_impl(self):
        # 如果没有 exclude 规则，应该包含所有文件（除了默认规则）
        zip_bytes, size, err = zip_and_encode_folder(self.temp_dir, [])
        self.assertIsInstance(zip_bytes, bytes)
        self.assertGreater(size, 0)
        self.assertIsNone(err)
        with zipfile.ZipFile(BytesIO(zip_bytes)) as zipf:
            names = zipf.namelist()
            print(names)
            self.assertIn("file1.py", names)
            self.assertNotIn("file2.pyc", names)
            self.assertNotIn("__pycache__/cached.pyc", names)


if __name__ == "__main__":
    unittest.main()
