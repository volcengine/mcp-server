#MCP Server 产品名称：[MCP Server 产品名称]
[![产品Logo]([产品Logo的URL或本地路径])]

## 版本信息

[请在此处填写版本信息，例如 v1，v2，小写。]

## 产品描述

###短描述（建议 20 个字）
[请在此处填写简略、准确、吸引人的产品描述，突出产品在 MCP 广场上的独特价值。主要用于官网卡片与详情页]

### 长描述（建议 50 字，不超过 100 字）

[请在此处填写详细、准确、吸引人的产品描述，包括核心功能、优势、适用场景等。突出产品在 MCP 广场上的独特价值。主要用于官网卡片与详情页]

## 分类

[请在此处填写准确的产品分类，方便用户浏览和查找。例如，存储，计算，数据库]

## 标签

[请在此处填写便于用户搜索和发现产品的关键词标签，多个标签请用逗号分隔，建议不超过 4 个。例如：搜索，位置，安全，数据清洗等]

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: [Tool 1 名称]

#### 类型

[请在此处填写此 Tool 是 saas ？还是实例型？]

#### 详细描述

[请在此处填写 Tool 1 的详细描述，包括其功能、特点、解决的问题等。 不超过 100 个字]

#### 调试所需的输入参数:

输入：

```json
{
  "inputSchema": {
    "type": "object",
    "required": ["location"],
    "properties": {
      "location": {
        "description": "经纬度",
        "type": "string"
      }
    }
  },
  "name": "maps_regeocode",
  "description": "将一个高德经纬度坐标转换为行政区划地址信息"
}
```

输出： - 输出结果描述 - Current status of working directory as text output

#### 最容易被唤起的 Prompt 示例

[请在此处填写最容易触发 Tool 1 功能的 Prompt 示例]

## 可适配平台

[请在此处列出该 MCP Server 产品可以适配的平台或环境。例如：方舟，python，cursor]

## 服务开通链接 (整体产品)

[请在此处填写该 MCP Server 产品的整体服务开通链接]

## 鉴权方式

[请在此处说明该 MCP Server 产品使用的鉴权方式。例如：API Key，OAuth 2.0，Token 等，并简要说明如何获取和使用凭证。]

## 安装部署

[请在此处提供详细的安装和部署说明，根据您的产品特性选择合适的描述方式。]
[示例如下]

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run _mcp-server-git_.

### Using PIP

Alternatively you can install `mcp-server-git` via pip:

```
pip install mcp-server-git
```

After installation, you can run it as a script using:

```
python -m mcp_server_git
```

##在不同平台的配置

### 方舟

#### 体验中心

[示例如下]

1. 查看 MCP Server 详情
   在大模型生态广场，选择合适的 MCP Server，并查看详情
2. 选择 MCP Server 即将运行的平台
   检查当前 MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的 Tools
   仔细查看可用的 Tools 的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的 URL 或代码示例
   检查账号登录状态与服务开通情况，生成唯一 URL
5. 去对应的 Client 的平台进行使用
   点击快捷跳转按钮，前往方舟平台的体验中心进行对应 MCP Server 的体验

## 资源列表 - optional

## 商业化 - optional

## 产品截图/视频 - optional

### Cursor

## 部署

[常见的部署方式，例如 docker 和 uvx]
[示例如下]

### Docker

```json
{
  "mcpServers": {
    "git": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--mount",
        "type=bind,src=/Users/username/Desktop,dst=/projects/Desktop",
        "--mount",
        "type=bind,src=/path/to/other/allowed/dir,dst=/projects/other/allowed/dir,ro",
        "--mount",
        "type=bind,src=/path/to/file.txt,dst=/projects/path/to/file.txt",
        "mcp/git"
      ]
    }
  }
}
```

### UVX

```json
{
"mcpServers": {
  "git": {
    "command": "uv",
    "args": [
      "--directory",
      "/<path to mcp-servers>/mcp-servers/src/git",
      "run",
      "mcp-server-git"
    ]
  }
}
```

## License
