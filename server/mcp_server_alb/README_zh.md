# 应用型负载均衡 MCP Server

## 版本信息

v0.1

## 产品描述

### 短描述

查阅应用型负载均衡实例的信息，包括实例关联的监听器、后端服务器组以及证书等相关信息。

### 长描述

火山引擎 ALB 支持 HTTP、HTTPS、HTTP/2、WebSocket、WebSocket Secure、QUIC等多种应用层协议，满足不同场景的需求。火山引擎 ALB 可以对后端服务器的健康状态进行监测、提供证书管理功能。

## 分类

CDN与边缘

## 标签

应用型负载均衡

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: describe_acl_attributes

查询指定访问控制策略组的详细信息。

### Tool 2: describe_ca_certificates

查询 CA 证书列表。

### Tool 3: describe_acls

查询访问控制策略组列表。

### Tool 4: describe_certificates

查询服务器证书列表。

### Tool 5: describe_customized_cfgs

查询个性化配置列表。

### Tool 6: describe_all_certificates

查询所有证书列表。

### Tool 7: describe_listener_attributes

查询指定监听器的详细信息。

### Tool 8: describe_listeners

查询监听器列表。

### Tool 9: describe_load_balancer_attributes

查询 应用型负载均衡实例的详细信息。

### Tool 10: describe_customized_cfg_attributes

查询指定个性化配置详细信息。

### Tool 11: describe_health_check_templates

获取健康检查模板列表。

### Tool 12: describe_listener_health

查询指定监听器关联后端服务器的健康检查信息。

### Tool 13: describe_load_balancers

查询应用型负载均衡实例列表。

### Tool 14: describe_server_group_attributes

查询服务器组的详细信息。

### Tool 15: describe_rules

获取指定监听器转发规则列表。

### Tool 16: describe_zones

查询 ALB 支持部署的可用区列表。

### Tool 17: describe_server_groups

查询服务器组列表。

### Tool 18: describe_server_group_backend_servers

查询服务器组的后端服务器信息。

## 可适配平台

- Python

## 服务开通链接

需要先为火山引擎账号开通应用型负载均衡服务。

https://console.volcengine.com/alb

## 鉴权方式

AK&amp;SK

### 获取 AK&amp;SK

从[火山引擎控制台](https://console.volcengine.com/iam/identitymanage/user)获取 Access Key ID 和 Secret Access Key。

注：此 Access Key ID 和 Secret Access Key 须具有相关 OpenAPIs 访问权限。

### 环境变量配置

| 变量名 | 值 |
| ---------- | ---------- |
| `VOLCENGINE_ACCESS_KEY` | 火山引擎账号 Access Key ID |
| `VOLCENGINE_SECRET_KEY` | 火山引擎账号 Secret Access Key |

## Python 版 MCP server

### 依赖项

运行 MCP server 的设备需要安装以下依赖项。

- [Python](https://www.python.org/downloads/) 3.11 或更高版本。
- [`uv`](https://docs.astral.sh/uv/) &amp; [`uvx`](https://docs.astral.sh/uv/guides/tools/)。
- 对于 Windows 操作系统，还需要参考 [PyCryptodome 文档](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#windows-from-sources) 配置该库编译环境。

### 部署与配置

```json
{
  "mcpServers": {
    "mcp-server-alb": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_alb/python",
        "mcp-server-alb"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

> 注：请将上方 `Your Volcengine AK` 和 `Your Volcengine SK` 分别替换为火山引擎账号对应的 Access Key ID 和 Secret Access Key。


## 使用客户端

支持通过以下客户端与 MCP Server 交互，具体配置可查阅该客户端文档。

- Cursor
- [Trae](https://www.trae.com.cn/)
- Claude Desktop
- 方舟

支持 [Cline](https://cline.bot/) 插件。

## 对话发起示例

- 列出所有ALB实例。
- 获取私网地址为192.168.1.16的ALB实例信息以及所关联的监听器信息

## 许可

[MIT](../../LICENSE)
