import unittest
import os

class TestCloudMonitorServerIntegration(unittest.TestCase):
    def setUp(self):
        # Check if credentials are available
        self.ak = os.environ.get("VOLC_ACCESSKEY")
        self.sk = os.environ.get("VOLC_SECRETKEY")
        if not self.ak or not self.sk:
            self.assertFalse(
                "VOLC_ACCESSKEY or VOLC_SECRETKEY environment variables not set"
            )

if __name__ == "__main__":
    unittest.main()
