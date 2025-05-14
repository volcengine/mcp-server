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
### Tool2: get_all_image_templates
 - 详细描述：获取所有模板信息。
 - 触发示例：调用 get_all_image_templates 获取模板信息
### Tool3: get_image_storage_files
 - 详细描述：获取所有资源信息。
 - 触发示例：调用 get_image_storage_files 获取相关数据
### Tool4: get_image_url_by_store_uri
 - 详细描述：获取指定资源的访问链接。
 - 触发示例：调用 get_image_url_by_store_uri 获取指定资源的访问链接
### Tool5: upload_image
 - 详细描述：上传图片。
 - 触发示例：调用 upload_image 上传图片
### Tool6: generate_image_by_text
 - 详细描述：根据文本生成图片。
 - 触发示例：调用 generate_image_by_text 根据文本生成图片
### Tool7: enhance_image_quality
 - 详细描述：根据图片URL，对图片进行画质增强。
 - 触发示例：调用 enhance_image_quality 根据图片URL，对图片进行画质增强
### Tool8: convert_image_to_comic_style
 - 详细描述：根据图片URL，对图片进行漫画风格转换。
 - 触发示例：调用 convert_image_to_comic_style 根据图片URL，对图片进行漫画风格转换
### Tool9: image_ocr
 - 详细描述：根据图片URL，对图片进行OCR识别。
 - 触发示例：调用 image_ocr 根据图片URL，对图片进行OCR识别
### Tool10: expand_image
 - 详细描述：根据图片URL，对图片进行扩展。
 - 触发示例：调用 expand_image 根据图片URL，对图片进行扩展


## 可适配平台

方舟，Trae，cursor

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
| `DOMAIN_NAME`    | veImageX 域名        | -   |

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
    "veimagex-mcp": {
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
        "DOMAIN_NAME": "Your Domain"
      }
    }
  }
}
```


# License
MIT