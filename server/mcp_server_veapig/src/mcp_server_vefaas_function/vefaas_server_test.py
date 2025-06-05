import base64
import io
import unittest
import os
import zipfile

from vefaas_server import does_function_exist, create_zip_base64


class TestVeFaaSServerIntegration(unittest.TestCase):
    def setUp(self):
        # Check if credentials are available
        self.ak = os.environ.get("VOLCENGINE_ACCESS_KEY")
        self.sk = os.environ.get("VOLCENGINE_SECRET_KEY")
        if not self.ak or not self.sk:
            self.assertFalse(
                "VOLCENGINE_ACCESS_KEY or VOLCENGINE_SECRET_KEY environment variables not set"
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


if __name__ == "__main__":
    unittest.main()
