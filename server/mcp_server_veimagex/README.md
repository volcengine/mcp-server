# MCP Server Product Name: veImageX MCP Server

The MCP Server implementation for veImageX provides clients with the capability to interact with Volcano Engine's veImageX service. It enables natural language-based management of veImageX cloud resources, service information queries, and integrates various image processing capabilities including text-to-image generation, AIGC quality enhancement, image expansion, and more.

| Version | v0.1.0                   | 
|---------|--------------------------|
| Description | Manage veImageX resources and process images via MCP |
| Category | Video Cloud               |
| Tags | Image Processing, Asset Hosting |

## Tools

This MCP Server product provides the following Tools (capabilities):
### Tool1: get_all_image_services
 - Description: Retrieve all service information.
 - Trigger Example: Call get_all_image_services to obtain relevant data
### Tool2: get_all_image_templates
 - Description: Retrieve all template information.
 - Trigger Example: Call get_all_image_templates to obtain template information
### Tool3: get_image_storage_files
 - Description: Retrieve all asset information.
 - Trigger Example: Call get_image_storage_files to obtain relevant data
### Tool4: get_image_url_by_store_uri
 - Description: Retrieve access URLs for specified assets.
 - Trigger Example: Call get_image_url_by_store_uri to obtain access URLs for specified assets
### Tool5: upload_image
 - Description: Upload images.
 - Trigger Example: Call upload_image to upload images
### Tool6: generate_image_by_text
 - Description: Generate images from text.
 - Trigger Example: Call generate_image_by_text to generate images from text
### Tool7: enhance_image_quality
 - Description: Enhance image quality based on image URLs.
 - Trigger Example: Call enhance_image_quality to enhance image quality based on image URLs
### Tool8: convert_image_to_comic_style
 - Description: Convert images to comic style based on image URLs.
 - Trigger Example: Call convert_image_to_comic_style to convert images to comic style based on image URLs
### Tool9: image_ocr
 - Description: Perform OCR recognition on images based on image URLs.
 - Trigger Example: Call image_ocr to perform OCR recognition on images based on image URLs
### Tool10: expand_image
 - Description: Expand images based on image URLs.
 - Trigger Example: Call expand_image to expand images based on image URLs


## Compatible Platforms

Ark, Python, Cursor

## Service Activation Link (Full Product)

<https://console.volcengine.cn/imagex?utm_source=tdgfha&utm_medium=oesbpg&utm_term=mcp-pr-01&utm_campaign=&utm_content=ImageX>

## Authentication Method

Volcano Engine: Obtain the access key ID, secret access key, and region from the Volcano Engine management console. Please set the relevant environment variables in the .env file.

### Environment Variables

The following environment variables can be used to configure the MCP server:

| Environment Variable      | Description                  | Default Value |
|---------------------------|------------------------------|---------------|
| `VOLCENGINE_ACCESS_KEY` | Volcano Engine account ACCESS KEY | -   |
| `VOLCENGINE_SECRET_KEY` | Volcano Engine account SECRET KEY | -   |
| `SERVICE_ID`    | veImageX service ID         | -   |
| `DOMAIN_NAME`    | veImageX domain        | -   |

## Installation & Deployment

### System Requirements

- Install Python 3.11 or higher
- Install uv
    - For Linux systems
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
    - For Windows systems
    ```
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    - Synchronize dependencies and update uv.lock:
    ```bash
    uv sync
    ```
    - Build MCP server:
    ```bash
    uv build
    ```

## Using uvx
### Local Configuration
- Add the following configuration to your MCP settings file
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
        "DOMAIN_NAME": "Your Domain"
      }
    }
  }
}
```


# License
MIT
    