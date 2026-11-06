"""已发布短信材料契约的安装配置，前端构建与服务端共享；不从用户输入覆盖。"""

import json
from importlib.resources import files

FORM_CONFIG = json.loads(
    files("mcp_server_sms").joinpath("form_config.json").read_text(encoding="utf-8")
)
