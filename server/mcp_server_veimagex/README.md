# MCP Server 产品名称：veImageX MCP Server

veImageX的MCP Server实现，为MCP客户端提供与火山引擎veImageX服务交互的能力。可以基于自然语言管理veImageX云端资源，查询服务信息，集成了包括文生图、AIGC画质修复、图像扩展等图像处理能力。

| 版本 | v0.1.0                   | 
|----|--------------------------|
| 描述 | 基于 MCP 管理 veImageX 资源，处理图片 |
| 分类 | 视频云                       |
| 标签 | 图像处理，素材托管              |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):
### Tool1: get_all_image_services
 - 详细描述：获取所有服务信息。
 - 触发示例：调用 get_all_image_services 获取相关数据
### Tool2: get_service_domains
 - 详细描述：获取服务下所有域名信息。
 - 触发示例：调用 get_service_domains 获取相关数据
### Tool3: get_all_image_templates
 - 详细描述：获取所有模板信息。
 - 触发示例：调用 get_all_image_templates 获取模板信息
### Tool4: get_image_storage_files
 - 详细描述：获取所有资源信息。
 - 触发示例：调用 get_image_storage_files 获取相关数据
### Tool5: delete_image_upload_files
 - 详细描述：删除指定的图片资源。
 - 触发示例：调用 delete_image_upload_files 删除指定的图片资源
### Tool6: get_image_url_by_store_uri
 - 详细描述：获取指定资源的访问链接。
 - 触发示例：调用 get_image_url_by_store_uri 获取指定资源的访问链接
### Tool7: upload_image
 - 详细描述：上传图片。
 - 触发示例：调用 upload_image 上传图片
### Tool8: generate_image_by_text
 - 详细描述：根据文本生成图片。
 - 触发示例：调用 generate_image_by_text 根据文本生成图片
### Tool9: enhance_image_quality
 - 详细描述：根据图片URL，对图片进行画质增强。
 - 触发示例：调用 enhance_image_quality 根据图片URL，对图片进行画质增强
### Tool10: convert_image_to_comic_style
 - 详细描述：根据图片URL，对图片进行漫画风格转换。
 - 触发示例：调用 convert_image_to_comic_style 根据图片URL，对图片进行漫画风格转换
### Tool11: image_ocr
 - 详细描述：根据图片URL，对图片进行OCR识别。
 - 触发示例：调用 image_ocr 根据图片URL，对图片进行OCR识别
### Tool12: expand_image
 - 详细描述：根据图片URL，对图片进行扩展。
 - 触发示例：调用 expand_image 根据图片URL，对图片进行扩展
### Tool13: evaluate_image_quality
 - 详细描述：根据图片URL，对图片进行质量评估。
 - 触发示例：调用 evaluate_image_quality 根据图片URL，对图片进行质量评估
### Tool14: describe_imagex_summary
 - 详细描述：查询本月用量概览。
 - 触发示例：调用 describe_imagex_summary 查询本月用量概览
### Tool15: describe_imagex_bandwidth_data
 - 详细描述：查询带宽用量。
 - 触发示例：调用 describe_imagex_bandwidth_data 查询带宽用量
### Tool16: describe_imagex_traffic_data
 - 详细描述：查询流量用量。
 - 触发示例：调用 describe_imagex_traffic_data 查询流量用量
### Tool17: describe_imagex_billing_request_cnt_usage
 - 详细描述：获取该时间段的附加组件通用请求次数。
 - 触发示例：调用 describe_imagex_billing_request_cnt_usage 查询请求次数
### Tool18: describe_imagex_request_cnt_usage
 - 详细描述：获取该时间段的请求次数。
 - 触发示例：调用 describe_imagex_request_cnt_usage 查询请求次数
### Tool19: describe_imagex_base_op_usage
 - 详细描述：获取该时间段的基础图像处理量。
 - 触发示例：调用 describe_imagex_base_op_usage 查询基础图像处理量
### Tool20: describe_imagex_compress_usage
 - 详细描述：获取该时间段的图像高效压缩量。
 - 触发示例：调用 describe_imagex_compress_usage 查询图像高效压缩量
### Tool21: describe_imagex_screenshot_usage
 - 详细描述：获取该时间段的截帧用量。
 - 触发示例：调用 describe_imagex_screenshot_usage 查询截帧用量
### Tool22: describe_imagex_video_clip_duration_usage
 - 详细描述：获取该时间段的小视频转动图的视频转换时长用量。
 - 触发示例：调用 describe_imagex_video_clip_duration_usage 查询小视频转动图的视频转换时长用量
### Tool23: describe_imagex_multi_compress_usage
 - 详细描述：查询该时间段的多文件压缩用量。
 - 触发示例：调用 describe_imagex_multi_compress_usage 查询多文件压缩用量
### Tool24: describe_imagex_edge_request
 - 详细描述：查询该时间段的边缘请求次数。
 - 触发示例：调用 describe_imagex_edge_request 查询边缘请求次数
### Tool25: describe_imagex_edge_request_bandwidth
 - 详细描述：查询该时间段的边缘请求带宽。
 - 触发示例：调用 describe_imagex_edge_request_bandwidth 查询边缘请求带宽
### Tool26: describe_imagex_edge_request_traffic
 - 详细描述：查询该时间段的边缘请求流量。
 - 触发示例：调用 describe_imagex_edge_request_traffic 查询边缘请求流量
### Tool27: describe_imagex_edge_request_regions
 - 详细描述：查询该时间段的边缘请求区域。
 - 触发示例：调用 describe_imagex_edge_request_regions 查询边缘请求区域
### Tool28: describe_imagex_server_qps_usage
 - 详细描述：查询该时间段的当前账号的数据处理服务 QPS 用量。
 - 触发示例：调用 describe_imagex_server_qps_usage 查询当前账号的数据处理服务 QPS 用量
### Tool29: describe_imagex_hit_rate_traffic_data
 - 详细描述：查询该时间段的域名的 CDN 流量命中率用量数据。
 - 触发示例：调用 describe_imagex_hit_rate_traffic_data 查询域名的 CDN 流量命中率用量数据
### Tool30: describe_imagex_hit_rate_request_data
 - 详细描述：查询该时间段的域名的 CDN 流量命中率请求数据。
 - 触发示例：调用 describe_imagex_hit_rate_request_data 查询域名的 CDN 流量命中率请求数据
### Tool31: describe_imagexcdn_top_request_data
 - 详细描述：获取按照流量/请求次数排序的数据列表，即按流量或请求次数由大到小排序后，访问量最靠前的域名/URL/Refer/客户端IP/UA/访问区域/运营商等数据。
 - 触发示例：调用 describe_imagexcdn_top_request_data 获取按照流量/请求次数排序的数据列表
### Tool32: describe_imagex_domain_bandwidth_ninety_five_data
 - 详细描述：查询该时间段的域名的 95 带宽。
 - 触发示例：调用 describe_imagex_domain_bandwidth_ninety_five_data 查询域名的 95 带宽
### Tool33: describe_imagex_bucket_retrieval_usage
 - 详细描述：查询该时间段的每天资源占用量。
 - 触发示例：调用 describe_imagex_bucket_retrieval_usage 查询该时间段的每天资源占用量
### Tool34: describe_imagex_source_request
 - 详细描述：查询该时间段的回源请求次数。
 - 触发示例：调用 describe_imagex_source_request 查询该时间段的回源请求次数
### Tool35: describe_imagex_source_request_bandwidth
 - 详细描述：查询该时间段的回源带宽用量。
 - 触发示例：调用 describe_imagex_source_request_bandwidth 查询该时间段的回源带宽用量
### Tool36: describe_imagex_source_request_traffic
 - 详细描述：查询该时间段的回源流量用量。
 - 触发示例：调用 describe_imagex_source_request_traffic 查询该时间段的回源流量用量
### Tool37: describe_vpc_access_config
 - 详细描述：获取指定服务的内网访问功能的配置详情。
 - 触发示例：调用 describe_vpc_access_config 获取指定服务的内网访问功能的配置详情


## 可适配平台

方舟，python，cursor

## 服务开通链接 (整体产品)

<https://console.volcengine.cn/imagex?utm_source=tdgfha&utm_medium=oesbpg&utm_term=mcp-pr-01&utm_campaign=&utm_content=ImageX>

## 鉴权方式

火山引擎，从 volcengine 管理控制台获取 volcengine 访问密钥 ID、秘密访问密钥和区域，请在.env文件中设置相关环境变量

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量             | 描述                     | 默认值 |
|------------------|------------------------|-----|
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 ACCESS KEY      | -   |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 SECRET KEY      | -   |
| `SERVICE_ID`    | veImageX 服务 ID         | -   |
| `DOMAIN`    | veImageX 域名        | -   |

## 安装部署

### 系统依赖

- 安装 Python 3.11 或者更高版本
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
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_veimagex",
        "mcp-server-veimagex"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK",
        "SERVICE_ID": "Your Service ID",
        "DOMAIN": "Your Domain"
      }
    }
  }
}
```


# License
MIT