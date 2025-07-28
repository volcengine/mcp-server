# VPC MCP Server

## 版本信息

v1.0.0

## 产品描述

VPC MCP Server 是一个模型上下文协议 (Model Context Protocol) 服务器，
为 MCP 客户端 (如 Trae) 提供与火山引擎 VPC 服务交互的能力。
它支持基于自然语言的 VPC 资源管理，
支持包括对私有网络、子网、路由表、网卡、安全组等资源的查询操作。

## 分类

网络

## 标签

私有网络, VPC

## Tools

### 私有网络

- `describe_vpcs`: [查询满足指定条件的VPC](https://www.volcengine.com/docs/6401/70495)
- `describe_vpc_attributes`: [查看指定VPC的详情](https://www.volcengine.com/docs/6401/70744)

### 子网

- `describe_subnets`: [查询满足指定条件的子网](https://www.volcengine.com/docs/6401/70497)
- `describe_subnet_attributes`: [查看指定子网的详细信息](https://www.volcengine.com/docs/6401/70498)

### 路由表

- `describe_route_table_list`: [查询满足指定条件的路由表](https://www.volcengine.com/docs/6401/70768)
- `describe_route_entry_list`: [在指定路由表内查询满足指定条件的路由条目](https://www.volcengine.com/docs/6401/70774)

### 网卡

- `describe_network_interfaces`: [查询满足指定条件的网卡](https://www.volcengine.com/docs/6401/70761)
- `describe_network_interface_attributes`: [查看指定网卡的详情](https://www.volcengine.com/docs/6401/70762)

### 安全组

- `describe_security_groups`: [查询满足指定条件的安全组](https://www.volcengine.com/docs/6401/70753)
- `describe_security_group_attributes`: [在指定安全组内查询满足指定条件的安全组规则](https://www.volcengine.com/docs/6401/70752)

### 前缀列表

- `describe_prefix_lists`: [查询满足指定条件的前缀列表](https://www.volcengine.com/docs/6401/1124629)
- `describe_prefix_list_associations`: [查询指定前缀列表关联的资源](https://www.volcengine.com/docs/6401/1124630)
- `describe_prefix_list_entries`: [查看指定前缀列表的前缀条目](https://www.volcengine.com/docs/6401/1124631)

### 高可用虚拟IP

- `describe_ha_vips`: [查询满足指定条件的高可用虚拟IP（HAVIP）](https://www.volcengine.com/docs/6401/100305)

### 网络ACL

- `describe_network_acls`: [查询满足指定条件的网络ACL](https://www.volcengine.com/docs/6401/108592)
- `describe_network_acl_attributes`: [查看指定网络ACL的详情](https://www.volcengine.com/docs/6401/108593)

## 可适配平台

可以使用方舟、 Trae 、 Cursor 等支持 MCP server 调用的客户端。

## 服务开通链接

[私有网络](https://console.volcengine.com/vpc)

## 鉴权方式

从火山引擎管理控制台获取账号 access key 和 secret key 。

## 配置示例

### uvx

```json
{
  "mcpServers": {
    "mcp-server-vpc": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_vpc",
        "mcp-server-vpc"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "火山引擎账号 access key",
        "VOLCENGINE_SECRET_KEY": "火山引擎账号 secret key",
        "VOLCENGINE_REGION": "火山引擎 region"
      }
    }
  }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
