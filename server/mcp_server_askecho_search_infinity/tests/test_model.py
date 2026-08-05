import unittest

from mcp_server_askecho_search_infinity.model import build_web_search_request


class BuildWebSearchRequestTest(unittest.TestCase):
    def test_web_payload_includes_custom_controls(self):
        request = build_web_search_request(
            query="  OpenAI  ",
            count=3,
            time_range="OneWeek",
            auth_level=1,
            need_content=True,
            need_url=False,
            sites="openai.com | example.com",
            block_hosts="spam.example",
            industry="finance",
            query_rewrite=True,
            content_formats="markdown",
        )

        self.assertEqual(
            request.to_payload(),
            {
                "Query": "OpenAI",
                "SearchType": "web",
                "Count": 3,
                "Filter": {
                    "AuthInfoLevel": 1,
                    "NeedContent": True,
                    "NeedUrl": False,
                    "Sites": "openai.com|example.com",
                    "BlockHosts": "spam.example",
                    "Industry": "finance",
                },
                "TimeRange": "OneWeek",
                "QueryControl": {"QueryRewrite": True},
                "ContentFormats": "markdown",
            },
        )
        self.assertNotIn("NeedSummary", request.to_payload())

    def test_image_uses_image_default_count(self):
        request = build_web_search_request(query="mountain", search_type="image")

        self.assertEqual(
            request.to_payload(),
            {"Query": "mountain", "SearchType": "image", "Count": 5},
        )

    def test_image_rejects_web_only_controls(self):
        with self.assertRaisesRegex(ValueError, "仅支持 web 搜索"):
            build_web_search_request(
                query="mountain",
                search_type="image",
                need_content=True,
            )

    def test_host_lists_enforce_documented_limits(self):
        sites = "|".join(f"site-{index}.example" for index in range(21))

        with self.assertRaisesRegex(ValueError, "Sites 最多支持 20 个域名"):
            build_web_search_request(query="OpenAI", sites=sites)

    def test_invalid_custom_values_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Industry"):
            build_web_search_request(query="OpenAI", industry="news")

        with self.assertRaisesRegex(ValueError, "ContentFormats"):
            build_web_search_request(query="OpenAI", content_formats="html")


if __name__ == "__main__":
    unittest.main()
