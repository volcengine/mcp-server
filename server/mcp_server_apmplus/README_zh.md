# APMPlus MCP Server

应用性能监控服务官方推出的 MCP Server，可以将自然语言精准转化为可观测分析语句，高效分析包含指标、链路和日志在内的可观测数据，助您全面保障应用的全生命周期，提升异常问题排查与解决的效率。

| 版本 | v0.1.0 |
| :-: |:----------------:|
| 描述 | APMPlus MCP Server 助您全面保障应用的全生命周期 |
| 分类 | 可观测 |
| 标签 | 可观测，链路，指标，日志，性能监控 |

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### 1. apmplus_server_list_alert_rule
查询应用性能监控-服务端监控在指定区域下的告警规则
- 参数:
  - `region_id`: [str] 地域 id
  - `keyword`: [str] 搜索关键词
  - `page_number`: [int] 分页页码
  - `page_size`: [int] 分页大小

### 2. apmplus_server_list_notify_group
查询应用性能监控-服务端监控在指定区域下的通知组信息
- 参数:
  - `region_id`: [str] 地域 id
  - `keyword`: [str] 搜索关键词
  - `page_number`: [int] 分页页码
  - `page_size`: [int] 分页大小

### 3. apmplus_server_query_metrics
查询应用性能监控-服务端监控在指定区域下的指标
- 参数:
  - `region_id`: [str] 地域 id
  - `query`: [str] 指标表达式，PromQL格式
  - `start_time`: [int] 开始时间，单位为秒
  - `end_time`: [int] 结束时间，单位为秒

## 可适配平台  
可以使用cline、cursor、claude desktop或支持MCP server调用的其它终端

## 服务开通链接
https://console.volcengine.com/apmplus-server

## 安装部署  
从 [volcengine](https://www.volcengine.com/docs/6291/65568) 获取 ak/sk, 然后将 ak/sk 添加到 mcp server 配置中, 或者在工作目录下的 `.env` 文件中配置, 格式如下:
```shell
VOLCENGINE_ACCESS_KEY=your_volcengine_ak
VOLCENGINE_SECRET_KEY=your_volcengine_sk
```

## 使用 uv
添加以下配置到你的 mcp settings 文件中
```json
{
  "mcpServers": {
    "mcp-server-apmplus": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server.git#subdirectory=server/mcp_server_apmplus",
        "mcp-server-apmplus"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```
或者克隆仓库到本地, 从本地代码仓库中启动
```json
{
  "mcpServers": {
    "mcp-server-apmplus": {
      "command": "uv",
      "args": [
        "--directory",
        "path/to/src/mcp_server_apmplus",
        "run",
        "server.py"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your_volcengine_ak",
        "VOLCENGINE_SECRET_KEY": "your_volcengine_sk"
      }
    }
  }
}
```

## License
[MIT](https://github.com/volcengine/mcp-server/blob/main/LICENSE)