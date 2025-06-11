# IoT MCP Server
火山引擎物联网平台官方推出的 MCP Server，支持基于自然语言来管理物联网实例下的资源。

## Tools

实例管理
- `get_instance_list`: [根据指定条件查询实例列表，包括名称、状态、实例组信息]()
- `get_instance_detail`: [根据实例ID查询指定实例的详细信息]()
- `get_instance_endpoints`: [查询实例的开发配置]()

产品管理
- `get_product_list`: [产品列表页查询，包含产品的基本信息]()
- `get_product_detail`: [除了基本信息外还会返回物模型、历史版本等数据]()
- `get_custom_topic_list`: [查询自定义Topic列表]()

物模型管理
- `get_thing_model`: [获取产品当前物模型]()

物模型使用
- `get_property_values_by_time`: [返回指定时间区间内的数值，对于数值型数据支持聚合计算]()
- `get_last_device_property_value`: [获取单个模块下指定属性的最新上报值]()
- `get_all_last_device_property_value`: [获取所有模块，所有属性的最新上报值]()
- `get_device_service_call_record_list`: [获取设备服务调用记录]()
- `get_device_event_record_list`: [获取设备物模型事件上报记录]()
- `call_service`: [向设备主动发起调用服务]()
- `set_property`: [向设备主动设置属性]()

设备管理
- `get_device_list`: [根据指定条件查询设备列表，比如名称(模糊)、状态、产品、位置(暂不支持)等]()
- `get_device_detail`: [根据设备标识查询设备信息]()
- `get_device_status`: [设备状态查询，如果有异常默认返回Disable，状态枚举：Online/Offline/NeverConnected/Disable，在线/离线/未激活/禁用]()
- `get_device_overview`: [获取设备总览信息，包括当前有多少设备，多少离线，多少在线，多少未激活，多少禁用]()

## 鉴权方式
从[ 火山引擎控制台-访问控制 ](https://console.volcengine.com/iam/keymanage)获取 AccessKey 和 SecretKey。

**注：AccessKey 和 SecretKey 需要具备上述 OpenAPI（可用工具）的权限。**


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

### 在 MCP Client 中集成
```json
{
  "mcpServers": {
    "iot": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_iot",
        "mcp-server-iot"
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

## License
MIT
