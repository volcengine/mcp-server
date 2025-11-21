# EMR Python MCP Server

## 运行环境
- 服务监听 `0.0.0.0:8000`
- 协议 `streamable-http`
- 平台通过 `run.sh` 启动

## 本地开发（基于 venv）
- 在项目根目录执行：
  - `python -m venv .venv`
  - `source .venv/bin/activate`
  - `python -m pip install -U pip`
  - `pip install -r requirements.txt`
- 运行：
  - `python main.py` 或 `./run.sh`

## 关键文件
- `run.sh`：启动入口（会在本地自动激活 `.venv`）
- `zip.sh`：打包脚本（排除 `.venv/`、`site-packages/`、`.wheels/`）

## 测试
- 运行 `run.sh` 本地启动emr mcp server
- 运行 `http_client_test.py` 测试emr mcp server
