
# MCP Server 产品名称：
视频直播 MCP Server

## 版本信息
v1

## 产品描述
火山引擎视频直播提供的MCP Server 提供强大的查询能力，支持通过自然语言对话交互的方式，实现多种APPI的调用,完成数据查询、地址生成、故障排查等功能,方便使用大语言模型搭建自己的工作流。

## 分类
企业应用

## 标签
视频直播，直播

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### Tool1: list_domain_detail
 - 详细描述：调用本接口查询账号下的域名列表信息，需要有分页信息
 - 触发示例：调用 ListDomainDetail 接口，根据域名状态、类别等信息，查询当前账号下的的域名列表信息。
### Tool2: describe_domain
 - 详细描述：调用本接口查询指定域名的详细信息。
 - 触发示例：调用 DescribeDomain 接口，查询域名的详细信息，包括但不限于域名所属域名空间、CNAME、类型、域名状态。
### Tool3: generate_push_url
 - 详细描述：调用本接口根据Vhost、Domain、App、Stream、ValidDuration等参数，生成直播推流地址。
 - 触发示例：调用 GeneratePushURL 接口，生成直播推流地址。
### Tool4: generate_play_url
 - 详细描述：调用本接口根据Domain、App、Stream、Type、Suffix、ValidDuration等参数，生成直播拉流地址。
 - 触发示例：调用 GeneratePlayURL 接口，生成直播拉流地址。
### Tool5: describe_live_stream_count_data
 - 详细描述：调用本接口查询指定时间范围内的直播流峰值数量。
 - 触发示例：调用 DescribeLiveStreamCountData 接口，查询时间范围内指定推流、回源流或转码流的峰值数量。
### Tool6: describe_live_batch_stream_traffic_data
 - 详细描述：调用本接口查询指定时间范围内的上下行流量数据及其详细数据。
 - 触发示例：调用 DescribeLiveBatchStreamTrafficData 接口，查询指定时间范围内的上下行流量数据及其详细数据。

### Tool7: describe_live_stream_session_data
 - 详细描述：调用本接口查询请求数和最大在线人数
 - 触发示例：调用 DescribeLiveStreamSessionData 接口，查询指定时间范围内域名下所有直播流或指定直播流的请求数和最大在线人数。
### Tool8: describe_live_push_stream_metrics
 - 详细描述：调用本接口查询单路直播推流的音视频帧率、码率等监控数据。
 - 触发示例：调用 DescribeLivePushStreamMetrics 接口，查询指定时间范围内单路直播推流的音视频帧率、码率等监控数据，用于判断直播流的健康程度。

### Tool9: describe_ip_info
 - 详细描述：调用本接口查询查询 IP 地址是否为火山引擎归属的 CDN 节点，以及节点的区域和运营商信息。
 - 触发示例：调用 DescribeIpInfo 接口，查询 IP 地址是否为火山引擎归属的 CDN 节点，以及节点的区域和运营商信息。

### Tool10: describe_live_push_stream_info_data
 - 详细描述：调用本接口查询断开的推流流信息以及推流断开的原因。
 - 触发示例：调用 DescribeLivePushStreamInfoData 接口，查询已断开的推流流信息以及推流断开的原因。
### Tool11: describe_live_transcode_info_data
 - 详细描述：调用本接口查询转码任务 ID、流名称、转码后缀、转码开始时间和结束时间数据等明细数据。
 - 触发示例：调用 DescribeLiveTranscodeInfoData 接口，查询指定时间范围内直播域名或直播流的转码任务 ID、流名称、转码后缀、转码开始时间和结束时间数据等明细数据。
### Tool12: describe_live_top_play_data
 - 详细描述：调用本接口查询TOPN 直播流或 TOPN 域名的流量和带宽信息。
 - 触发示例：调用 DescribeLiveTopPlayData 接口，查询指定时间范围内 TOPN 直播流或 TOPN 域名的流量和带宽信息。


## 最容易被唤起的 Prompt示例
### list_domain_detail
帮我查询当前账号下前10个域名信息列表。
### describe_domain
帮我查询一下 xxx.xxx.com 这个域名的详细信息
### describe_live_stream_session_data
帮我查询一下 XXX 域名今天的在线人数
### describe_live_push_stream_info_data
查询一下xxx域名，app是xx，流名是xx，今天的推流信息，并列出推流断开的原因


# 可适配平台  
可以使用 cline, cursor, Trae, claude desktop 或支持MCP server调用的的其他终端

## 服务开通链接 (整体产品)
<https://console.volcengine.com/live>


## 鉴权方式
从 volcengine 管理控制台获取 volcengine 访问密钥 ID、秘密访问密钥和区域

## 安装部署

### 系统依赖
- 安装 Python 3.10 或者更高版本
- 安装 uv
    - 如果是linux系统
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

## Using uv (recommended)
## 使用 uv（推荐）
使用 uv 时无需特别安装，我们将直接通过 uvx 运行 mcp-server-live。

### 本地配置
- 添加以下配置到你的 mcp settings 文件中

```json
{
    "mcpServers": {
      "mcp-server": {
        "command": "uv",
        "args": [
          "--directory",
          "/ABSOLUTE/PATH/TO/PARENT/mcp_server_live/src/live",
          "run",
           "mcp-server-live"
        ],
        "env": {
          "VOLCENGINE_ACCESS_KEY": "your access-key-id",
          "VOLCENGINE_SECRET_KEY": "your access-key-secret",
          "VOLCENGINE_REGION": "your region",
        }
      }
    }
  }
```

OR

- 添加以下配置到你的 mcp settings 文件中
```json
{
  "mcpServers": {
    "mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/mcp_server_live/src/live",
        "run",
        "server.py"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your access-key-id",
        "VOLCENGINE_SECRET_KEY": "your access-key-secret",
        "VOLCENGINE_REGION": "your region"
      }
    }
  }
}
```

## Using uvx
### 本地配置
- 添加以下配置到你的 mcp settings 文件中
```json
{
  "mcp-server": {
    "tos-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_live",
        "mcp-server-live"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your access-key-id",
        "VOLCENGINE_SECRET_KEY": "your access-key-secret",
        "VOLCENGINE_REGION": "your region",
      }
    }
  }
}
```
or

```json
{
  "mcpServers": {
    "mcp-live": {
      "command": "uvx",
      "args": [
        "--from",
        "/ABSOLUTE/PATH/TO/PARENT/mcp-server/server/mcp_server_live",
        "mcp-server-live"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your access-key-id",
        "VOLCENGINE_SECRET_KEY": "your access-key-secret",
        "VOLCENGINE_REGION": "your region"
      },
    }
  }
}
```

# License
MIT