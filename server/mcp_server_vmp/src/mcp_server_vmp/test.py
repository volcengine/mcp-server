import unittest

import mcp_server_vmp.models as models


class TestModels(unittest.TestCase):
    def test_list_workspaces_request(self):
        request = models.ListWorkspacesRequest()
        self.assertEqual(request.filters, None)


if __name__ == '__main__':
    unittest.main()
