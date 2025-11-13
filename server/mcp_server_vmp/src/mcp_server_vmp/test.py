import unittest

import mcp_server_vmp.models as models


class TestModels(unittest.TestCase):
    def test_list_workspaces_request(self):
        request = models.ListWorkspacesRequest()
        self.assertEqual(request.PageNumber, 1)
        self.assertEqual(request.PageSize, 100)
        self.assertEqual(request.ShowAggregateQueryWorkspaces, True)


if __name__ == '__main__':
    unittest.main()
