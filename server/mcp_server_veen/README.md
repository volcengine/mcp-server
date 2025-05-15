# VEEN MCP Server

基于覆盖全国各省市和运营商的边缘节点，火山引擎边缘计算节点产品为用户就近提供计算、网络、存储等资源，帮助用户将业务快速部署到边缘层。边缘计算节点提供不同粒度的算力服务，满足多样化场景中的用户需求。包含边缘计算节点、边缘容器、边缘托管和边缘函数等子产品。

| | |
|------|------|
| 版本 | v0.0.1 |
| 描述 | 申请、配置、查阅在边缘计算节点，包括虚拟机、镜像、裸金属，及对应的网络配置。 |
| 分类 | CDN与边缘 |
| 标签 | 边缘云，虚拟机，镜像，存储 |

## Tools

### Tool 1: start_cloud_server

根据边缘服务的 ID 启动边缘服务。

### Tool 2: delete_cloud_server

根据边缘服务 ID 删除边缘服务。

### Tool 3: stop_cloud_server

根据边缘服务的 ID 停止边缘服务。

### Tool 4: reboot_cloud_server

根据边缘服务的 ID 重启边缘服务。

### Tool 5: create_cloud_server

创建边缘服务。

### Tool 6: update_cloud_server

修改边缘服务配置。

### Tool 7: get_cloud_server

根据边缘服务的 ID 获取边缘服务的详细信息。

### Tool 8: reboot_instances

根据边缘实例 ID 重启实例。

### Tool 9: start_instances

根据边缘实例 ID 启动实例。

### Tool 10: stop_instances

根据边缘实例 ID 停止实例。

### Tool 11: list_instances

列出指定的边缘服务或所有边缘服务下的边缘实例。

### Tool 12: get_instance

根据边缘实例 ID 获取实例详细信息。

### Tool 13: reset_login_credential

重置重置边缘实例的密码。密码类型允许修改。

### Tool 14: set_instance_name

设置边缘实例的名称。

### Tool 15: batch_reset_system

重置指定边缘实例的操作系统或更换边缘实例的镜像。

### Tool 16: set_instances_bandwidth_peak

批量设置边缘实例的带宽峰值。

### Tool 17: enable_instances_i_pv6

批量开启边缘实例的 IPv6 功能。

### Tool 18: get_instances_i_pv6_upgrade_status

获取边缘实例的 IPv6 开启状态。

### Tool 19: update_instances_spec

变更边缘实例的实例规格。

### Tool 20: list_instance_internal_ips

获取边缘实例的私网 IP 地址的列表。

### Tool 21: set_bound_eip_share_bandwidth_peak

设置弹性公网 IP 的共享带宽峰值。共享带宽峰值指的是绑定在边缘实例私网 IP 地址（含主私网 IP 地址和辅助私网 IP 地址）上的所有弹性公网 IP 的共享公网带宽限速值。

### Tool 22: batch_bind_eip_to_internal_ips_randomly

批量随机绑定弹性公网 IP 到私网 IP 地址。

### Tool 23: batch_delete_internal_ips

批量删除边缘实例的辅助私网 IP 地址。

### Tool 24: get_instance_cloud_disk_info

获取边缘实例的云盘信息。

### Tool 25: set_cloud_server_delete_protection

为边缘服务配置删除保护。您可以通过该接口开启或关闭删除保护功能。
删除保护功能可以防止您的边缘服务被误删除，保障数据安全。

### Tool 26: set_instance_delete_protection

为一个或多个边缘实例配置删除保护。您可以通过该接口开启或关闭删除保护功能。
删除保护功能可以防止您的边缘实例被误删除，保障数据安全。

### Tool 27: list_cloud_servers

列出账号下的所有边缘服务信息。

### Tool 28: list_instance_types

获取边缘服务下可开通的实例规格。

### Tool 29: list_available_resource_info

获取边缘服务下某实例规格支持的地域和运营商。

### Tool 30: create_instance

创建边缘实例。

### Tool 31: create_secondary_internal_ip_and_reboot

为边缘实例新增辅助私网 IP 地址并重启该边缘实例。

### Tool 32: bind_eip_to_internal_ip

绑定单个弹性公网 IP 到私网 IP 地址。

### Tool 33: list_images

获取某一实例规格支持的镜像列表，包括公共镜像和自定义镜像。

### Tool 34: get_image

获取镜像详情。

### Tool 35: build_image_by_vm

通过边缘实例创建镜像。

### Tool 36: upload_url_image

导入镜像。

### Tool 37: update_image

编辑镜像的名称。

### Tool 38: delete_image

删除镜像。

### Tool 39: get_veen_instance_usage

获取指定时间范围内的算力用量。

### Tool 40: get_veew_instance_usage

获取指定时间范围内的边缘网络的用量。

### Tool 41: get_bandwidth_usage

获取指定时间范围内的带宽用量。

### Tool 42: get_billing_usage_detail

获取日用量趋势。

### Tool 43: list_vpc_instances

获取私有网络列表。

### Tool 44: set_vpc_instance_desc

修改私有网络的描述。

### Tool 45: list_route_tables

查询路由表的列表。

### Tool 46: get_route_table

查询路由表的详情。

### Tool 47: set_route_table_name_and_desc

修改路由表的名称和描述信息。

### Tool 48: list_route_entries

查询路由条目列表。

### Tool 49: create_route_entries

批量增加自定义路由条目。

### Tool 50: delete_route_entry

删除路由条目。

### Tool 51: enable_route_entry

启用路由条目。

### Tool 52: disable_route_entry

禁用路由条目。

### Tool 53: set_route_entry_desc

修改路由条目的描述信息。
