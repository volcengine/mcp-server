import unittest
from typing import get_origin

from mcp_server_redis.server import mcp_server


def _sample_for_required_argument(annotation):
    if annotation is str:
        return "sample"
    if annotation is int:
        return 1
    if annotation is bool:
        return False
    if get_origin(annotation) is list:
        return []
    if get_origin(annotation) is dict:
        return {}
    raise AssertionError(f"Unsupported required tool argument annotation: {annotation!r}")


class RedisOptionalToolArgumentsTests(unittest.TestCase):
    def test_registered_tools_accept_null_for_optional_arguments(self):
        tool_manager = mcp_server._tool_manager
        tested_arguments = 0

        for registered_tool in tool_manager.list_tools():
            with self.subTest(tool=registered_tool.name):
                argument_model = tool_manager.get_tool(registered_tool.name).fn_metadata.arg_model
                arguments = {}
                for name, field in argument_model.model_fields.items():
                    if field.is_required():
                        arguments[name] = _sample_for_required_argument(field.annotation)
                    else:
                        arguments[name] = field.default
                        if field.default is None:
                            tested_arguments += 1

                argument_model.model_validate(arguments)

        self.assertGreater(tested_arguments, 0)


if __name__ == "__main__":
    unittest.main()
