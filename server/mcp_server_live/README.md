
# MCP Server Product Name:
Live  MCP Server

## Version Information
v1

## Product Description
The MCP Server provided by Volcengine Live offers powerful query capabilities, supporting natural language dialogue interactions to implement various API calls for data querying, URL generation, troubleshooting, and more, facilitating workflow construction with large language models.

## Category
Enterprise Application

## Tags
Live Streaming

## Tools
This MCP Server provides the following tools/capabilities:
### Tool1: list_domain_detail
 - Description: Query paginated domain list information under the account
 - Trigger Example: Call ListDomainDetail interface to query domain list information under current account based on domain status and category.

### Tool2: describe_domain
 - Description: Query detailed information of a specific domain
 - Trigger Example: Call DescribeDomain interface to query domain details including domain namespace, CNAME, type, and status.

### Tool3: generate_push_url
 - Description: Generate live streaming push URLs based on parameters including Vhost, Domain, App, Stream, and ValidDuration.
 - Example: Invoke the GeneratePushURL interface to create live streaming push addresses.

### Tool4: generate_play_url
 - Description: Generate live streaming pull URLs based on parameters including Domain, App, Stream, Type, Suffix, and ValidDuration.
 - Example: Use the GeneratePlayURL interface to produce live streaming playback addresses.

### Tool5: describe_live_stream_count_data
 - Description: Query statistical information of live streaming data within specified time ranges.
 - Example: Call DescribeLiveStreamCountData to retrieve peak counts of push streams, back-to-source streams, or transcoded streams.

### Tool6: describe_live_batch_stream_traffic_data
 - Description: Obtain upstream/downstream traffic metrics and detailed data for specified time periods.
 - Example: Utilize DescribeLiveBatchStreamTrafficData to analyze traffic patterns across multiple streams.

### Tool7: describe_live_source_traffic_data
 - Description: Monitor back-to-source traffic and bandwidth metrics for pull domain names or streams.
 - Example: Access DescribeLiveSourceTrafficData to track source server traffic consumption.

### Tool8: describe_live_stream_session_data
 - Description: Retrieve request counts and peak concurrent users for live streams.
 - Example: Employ DescribeLiveStreamSessionData to monitor viewer engagement metrics.

### Tool9: describe_live_play_status_code_data
 - Description: Analyze status code distributions for streaming requests (push/pull/back-to-source).
 - Example: Use DescribeLivePlayStatusCodeData for HTTP status code monitoring and troubleshooting.

### Tool10: describe_live_push_stream_metrics
 - Description: Monitor audio/video frame rates and bitrates for individual push streams.
 - Example: Implement DescribeLivePushStreamMetrics for real-time stream health checks.

### Tool11: describe_live_source_stream_metrics
 - Description: Track performance metrics for individual back-to-source streams.
 - Example: Apply DescribeLiveSourceStreamMetrics to ensure source stream stability.

### Tool12: describe_live_batch_stream_transcode_data
 - Description: Aggregate transcoding metrics including duration, resolution profiles, and codecs.
 - Example: Query DescribeLiveBatchStreamTranscodeData for transcoding workload analysis.

### Tool13: describe_live_batch_push_stream_metrics
 - Description: Batch monitor push stream performance across domains or specific streams.
 - Example: Use DescribeLiveBatchPushStreamMetrics for multi-stream quality assurance.

### Tool14: describe_live_batch_source_stream_metrics
 - Description: Collect metrics for multiple back-to-source streams simultaneously.
 - Example: Leverage DescribeLiveBatchSourceStreamMetrics for comprehensive source monitoring.

### Tool15: describe_ip_info
 - Description: Verify CDN node attribution and obtain regional/ISP details for IP addresses.
 - Example: Check DescribeIpInfo to validate Volcano Engine CDN node status.

### Tool16: describe_live_isp_data
 - Description: Retrieve ISP identifiers for network provider-specific analytics.
 - Example: Access DescribeLiveISPData to filter metrics by internet service provider.

### Tool17: describe_live_region_data
 - Description: Obtain regional identifiers for geographical-based data segmentation.
 - Example: Use DescribeLiveRegionData for location-specific performance insights.

### Tool18: describe_live_push_stream_info_data
 - Description: Investigate disconnected push streams and termination causes.
 - Example: Analyze DescribeLivePushStreamInfoData for stream interruption diagnostics.

### Tool19: describe_live_transcode_info_data
 - Description: Access detailed transcoding job records including timelines and configurations.
 - Example: Query DescribeLiveTranscodeInfoData for transcoding operation audits.

### Tool20: describe_live_batch_stream_session_data
 - Description: Invoke this API to query request count and maximum concurrent users.
 - Example: Call DescribeLiveBatchStreamSessionData API to query request count and maximum concurrent users for all live streams under specified domains within a time range.

### Tool21: describe_live_top_play_data
 - Description: Use this API to retrieve traffic and bandwidth metrics for TopN live streams or TopN domains.
 - Example: Invoke DescribeLiveTopPlayData API to query traffic and bandwidth information of TopN live streams/domains within specified time ranges.

### Tool22: describe_live_edge_stat_data
 - Description: Query upstream/downstream traffic, peak bandwidth, and request count data for live streams by protocol, ISP, region, and time range.
 - Example: Call DescribeLiveEdgeStatData API to retrieve edge statistics including upstream/downstream traffic, peak bandwidth, and request counts based on protocol, ISP, region, and time parameters.

## Most Frequently Used Prompt Examples
### list_domain_detail
List the first 10 domain information under the current account.
### describe_domain
Query detailed information for the domain xxx.xxx.com
### describe_live_region_data
Query region identifiers covered by the live streaming service

# Supported Platforms  
Compatible with cline, cursor, Trae, claude desktop or other terminals supporting MCP server invocation

## Service Activation Link (Full Product Suite)
<https://console.volcengine.com/live>

## Authentication Method
Obtain Volcengine Access Key ID, Secret Access Key, and Region from the Volcengine Management Console

## Installation & Deployment

### System Requirements
- Install Python 3.10 or higher
- Install uv
    - For Linux systems:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    - For Windows systems:
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    - Synchronize dependencies and update uv.lock:
    ```bash
    uv sync
    ```
    - Build the MCP server:
    ```bash
    uv build
    ```
## Using uv (recommended)
When using uv no specific installation is needed. We will
use uvx to directly run mcp-server-live.


### Local Configuration
- Add the following configuration to your mcp settings file


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
          "VOLCENGINE_REGION": "your region"
        }
      }
    }
  }
```

OR

- Add the following configuration to your mcp settings file
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
### Local Configuration
- Add the following configuration to your mcp settings file
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
        "VOLCENGINE_REGION": "your region"
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

## License
MIT