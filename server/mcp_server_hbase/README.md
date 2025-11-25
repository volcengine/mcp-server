# > HBase MCP Server

 > 火山引擎表格数据库 HBase 版是基于 Apache HBase 提供的全托管 NoSQL 服务，兼容标准 HBase 访问协议，具备低成本存储、高扩展吞吐等优势
---

| 项目 | 详情                                                                                 |
|----|------------------------------------------------------------------------------------|
| 版本 | v1.0.0                                                                             |
| 描述 | 火山引擎表格数据库 HBase 版是基于 Apache HBase 提供的全托管 NoSQL 服务，兼容标准 HBase 访问协议，具备低成本存储、高扩展吞吐等优势 |
| 分类 | 数据库                                                                                |
| 标签 | HBase, NoSQL, 非关系型数据库, 表格数据库                                                       |


---

## 支持的Tools

### 1. `create_db_instance`
- **详细描述**: 创建实例


### 2. `modify_db_instance_name`
- **详细描述**: 调用 ModifyDBInstanceName 接口修改实例名称。


### 3. `describe_db_instance_detail`
- **详细描述**: 调用 DescribeDBInstanceDetail 接口查询指定实例的详细信息。


### 4. `describe_db_instances`
- **详细描述**: 调用 DescribeDBInstances 接口查询 HBase 实例列表信息。


### 5. `modify_instance_deletion_protection_policy`
- **详细描述**: 调用 ModifyInstanceDeletionProtectionPolicy 接口开启或关闭实例删除保护功能。


---

## 服务开通链接
> [点击前往火山引擎 HBase 服务开通页面](https://console.volcengine.com/db/hbase)


---

## 鉴权方式
在火山引擎管理控制台获取访问密钥 ID、秘密访问密钥和区域，采用 API Key 鉴权。
需要在配置文件中设置 `VOLCENGINE_ACCESS_KEY` 和 `VOLCENGINE_SECRET_KEY`。


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

## 安装部署

### 系统依赖
- 安装 Python 3.10 或者更高版本
- 安装 uv
  - 如果是linux/macOS系统
  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  - 如果是window系统
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- 同步依赖项并更uv.lock:
  ```bash
  uv sync
  ```
- 构建mcp server:
  ```bash
  uv build
  ```

### 使用 UVX

```json
{
    "mcpServers": {
        "mcp-server-hbase": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_hbase",
            "mcp-server-hbase"
          ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your-access-key-id",
                "VOLCENGINE_SECRET_KEY": "your-access-key-secret",
                "VOLCENGINE_REGION": "VOLC_REGION"
            }
        }
    }
}
```

---


## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
