# APMPlus MCP Server

应用性能监控服务官方推出的 MCP Server，可以将自然语言精准转化为可观测分析语句，高效分析包含指标、链路和日志在内的可观测数据，助您全面保障应用的全生命周期，提升异常问题排查与解决的效率。

| 版本 |              v0.2.0               |
| :-: |:---------------------------------:|
| 描述 | APMPlus MCP Server 助您全面保障应用的全生命周期 |
| 分类 |                可观测                |
| 标签 |         可观测，链路，指标，日志，性能监控         |

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### 1. apmplus_server_list_alert_rule
查询应用性能监控-服务端监控在指定区域下的告警规则
- 参数:
  - `region`: [str, optional] 地域 ID。默认为 cn-beijing。
  - `keyword`: [str, optional] 搜索关键词。默认为空。
  - `page_number`: [int, optional] 分页页码。默认为1。
  - `page_size`: [int, optional] 分页大小。默认为10。

### 2. apmplus_server_list_notify_group
查询应用性能监控-服务端监控在指定区域下的通知组信息
- 参数:
  - `region`: [str, optional] 地域 ID。默认为 cn-beijing。
  - `keyword`: [str, optional] 搜索关键词。默认为空。
  - `page_number`: [int, optional] 分页页码。默认为1。
  - `page_size`: [int, optional] 分页大小。默认为10。

### 3. apmplus_server_query_metrics
查询应用性能监控-服务端监控在指定区域下的指标
- 参数:
  - `region`: [str, optional] 地域 ID。默认为 cn-beijing。
  - `query`: [str] 指标表达式，PromQL格式。
  - `start_time`: [int] 开始时间，单位为秒。
  - `end_time`: [int] 结束时间，单位为秒。

### 4. apmplus_server_get_trace_detail
查询应用性能监控-服务端监控在指定区域下的链路详情信息
- 参数:
  - `trace_id`: [str, optional] 链路 ID。
  - `suggest_time`: [int, optional] 链路发生的大致时间（秒）。
  - `region`: [str, optional] 地域 ID。默认为 cn-beijing。

### 5. apmplus_server_list_span
查询应用性能监控-服务端监控在指定区域下的链路Span列表
- 参数:
  - `start_time`: [int] 开始时间（秒），例如：1693536000。
  - `end_time`: [int] 结束时间（秒），例如：1693546000。
  - `filters`: [list[dict], optional] 过滤表达式。每个字典包含：
                                  - 'Op' (str): in, not_in
                                  - 'Key' (str): 过滤键
                                  - 'Values' (list[str]): 过滤值
  - `order`: [str, optional] 排序方向。默认为 DESC。
  - `order_by`: [str, optional] 排序字段。默认为空字符串。
  - `offset`: [int, optional] 分页偏移量。默认为 0。
  - `limit`: [int, optional] 分页限制。默认为 10。
  - `min_call_cost_millisecond`: [int, optional] 最小调用耗时（毫秒）。默认为 0。
  - `max_call_cost_millisecond`: [int, optional] 最大调用耗时（毫秒）。默认为 0。
  - `project_name`: [str, optional] 项目名称。
  - `tag_filters`: [list[dict], optional] 标签过滤列表。每个字典包含：
                                             - 'Key' (str): 标签键
                                             - 'Value' (list[str]): 标签值
                                             Max 10 tag pairs.
                                             最多 10 个标签对。空值表示对标签值无限制。
  - `region`: [str, optional] 地域 ID。默认为 cn-beijing。

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