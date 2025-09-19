note = {
    "start_cloud_server": r""" 
    """,
    "delete_cloud_server": r""" 
    """,
    "stop_cloud_server": r""" 
    """,
    "reboot_cloud_server": r""" 
    """,
    "create_cloud_server": r""" 
   Args: 
       body: A JSON structure
            cloudserver_name ( String ): 是  边缘服务名称。命名规则如下： 
                  - 允许 5~20 个字符。 
                  - 支持中文、大写字母、小写字母、数字。 
                  - 支持特殊字符 ()`~!@#$%^&*-+=_{}[]:;',.?/。  
                  - 不能包含双引号（"）、反斜线（ ）和空格，且不能以正斜线（/）开头。 
            spec_name ( String ): 是  边缘实例规格名称。您可以通过 ListInstanceTypes 接口查询可开通的实例规格。如果您需要的规格不在可开通实例规格列表，请提交工单申请。 
            storage_config ( Object of StorageConfig ): 是  存储配置，包括系统盘和数据盘的类型和容量信息。 
                  详情请参见 StorageConfig。 
            network_config ( Object of NetworkConfig ): 是  网络配置。 
                  详情请参见 NetworkConfigReq。 
            secret_config ( Object of SecretConfig ): 是  边缘实例的登录密码设置。 
                  详情请参见 SecretConfig。 
            instance_area_nums ( Array of InstanceAreaNums ): 是  边缘实例的地域信息，包括地域的名称、运营商和边缘实例的个数等。 
                  详情请参见 InstanceAreaNum。 
                  如果不指定该参数，代表不创建边缘实例。 
            schedule_strategy ( Object of ScheduleStrategy ): 是  调度策略。 
                  不设置该参数时，默认按照城市分散、低价优先策略。 
                  服务层级为城市级时，无需设置该参数，按照城市分散、低价优先策略。如果该参数设置为其他值，策略将不生效。建议您将该参数留空。 
                  服务层级为大区级时，按照设置的策略生效。 
            custom_data ( Object of CustomData ): 否  自定义数据。自定义数据为边缘实例的定制信息。最大可输入 16 KB 的自定义数据。 
            billing_config ( Object of BillingConfig ): 否  计费方式，包括算力和带宽的计费方式。 
                  详情请参见 CreateCloudServerBillingConfigs。 
            advanced_configuration ( Object of AdvancedConfiguration ): 否  高级配置，用于自定义边缘实例名称、实例描述信息、主机名称。批量创建边缘实例时，将按照自定义名称顺序生成边缘实例名和主机名。 
            project ( String ): 否  通过边缘服务创建的实例所属的项目。 
                  如果不设置该参数或参数值为空字符串，采用默认值 default。 
            disable_vga ( Boolean ): 否  是否禁用 VGA。取值范围： 
                  - true：禁用VGA。 
                  - false：启用VGA。 
            cloud_server_desc ( String ): 否  边缘服务的描述信息。最多可输入 80 个字符。 
            create_instance_timeout ( Long ): 否  边缘实例的创建超时时间。单位：秒。最小值：120。 
                  当边缘实例的创建时长超过设置的值时，边缘实例创建失败，其状态变为 open_fail。您可以通过控制台或 API 接口来删除相关实例。 
                  如果不指定该参数的值，代表不限制实例创建时长。 
            client_token ( String ): 否   
            req_params_hash ( String ): 否   
           "字段"： StorageConfig
            system_disk ( Object of SystemDisk ): 是  系统盘。 
                  详情请参见 DiskSpec。 
            data_disk ( Object of DataDisk ): 否  数据盘。该参数用于添加单块数据盘。 
                  详情请参见 DiskSpec。 
            data_disk_list ( Array of DataDiskList ): 否  数据盘列表。该参数用于添加一块或多块数据盘。 
                  详情请参见 DiskSpec。 
           "字段"： NetworkConfig
            bandwidth_peak ( String ): 否  公网带宽峰值。取值范围：[5,实例规格支持的带宽上限]。取值须是 5 的倍数。单位：Mbps。 
                  当您选择 IPv4/IPv6 双栈边缘实例时，所设的带宽峰值将被 IPv4 和 IPv6 公网 IP 地址共享。 
                  disable_ipv4 设置为 true 时，无需配置 bandwidth_peak 参数。 
            enable_ipv6 ( Boolean ): 否  是否启用 IPv6。取值范围： 
                  - true ：启用 IPv6。 
                  - false（默认值）：禁用 IPv6。 
                  默认分配 IPv4 地址。当您启用 IPv6 时，系统会为边缘实例分配 IPv4 和 IPv6 两个公网 IP 地址。 
            disable_ipv4 ( Boolean ): 否  是否禁用 IPv4。取值范围： 
                  - true ：禁用 IPv4。 
                  - false（默认值）：启用 IPv4。 
            custom_internal_interface_name ( String ): 否  私网网卡的名称。目前仅 VLANVF 规格实例的私网网卡的名称可以被修改。 
            custom_external_interface_name ( String ): 否  公网网卡的名称。目前仅 VLANVF 规格实例的公网网卡的名称可以被修改。 
            dns_type ( Object of DnsType ): 否  DNS 类型： 
                  - default：默认 DNS。 
                  - custom：自定义 DNS。 
                  如果不设置该参数，代表使用默认的 DNS 配置，即首选 DNS 为 114.114.114.114，备用 DNS 为 223.6.6.6。 
                  暂不支持为裸金属实例配置 DNS。当实例规格为裸金属时，无需设置 dns_type 和 dns_list 参数。 
            dns_list ( Array of String ): 否  DNS 列表。前面的 IP 地址代表首选 DNS，后面的 IP 地址代表备用 DNS。 
                  - 当前最多支持一条首选 DNS 和一条备用 DNS。 
                  - 当 dns_type 设置为 default 时，不允许设置 dns_list。此时，采用默认的 DNS 配置，即首选 DNS 为 114.114.114.114，备用 DNS 为223.6.6.6。 
                  - 当 dns_type 设置为 custom 时，必须设置 dns_list。至少需要配置一条首选 DNS。可按需配置一条备用 DNS。 
            secondary_internal_ip_num ( Integer ): 否  辅助私网 IP 的个数。 
            bound_eip_share_bandwidth_peak ( String ): 否  弹性公网 IP 的共享带宽峰值。 
           "字段"： SecretConfig
            secret_type ( Object of SecretType ): 是  边缘实例的登录密码的类型。取值范围： 
                  - 2：自定义密码。 
                  - 3：SSH Key 类型密码。 
                  - 4: 代表不注入登录凭证。 
            secret_data ( String ): 否  登录密码。 
                  - 自定义密码：密码输入规则如下： 
                  	- 允许 8 ~ 30个字符。密码须至少包含以下类型中的3种：大写字母、小写字母、数字和特殊字符。 
                  	- 支持特殊字符 ()`~!@#$%^&*-+=_{}[]:;',.?/。  
                  	- 不能包含双引号（"）、反斜线（ ）和空格，且不能以正斜线（/）开头。 
                  - SSH Key 类型密码：输入SSH 密钥对的 ID。您可以通过 ListSSHKey 接口查询密钥对 ID。 
           "字段"： InstanceAreaNums
            area_name ( String ): 是  区域名称。您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            isp ( String ): 是  运营商。您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            cluster_name ( String ): 否  节点名称。指定希望部署边缘服务的节点。您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            vpc_identity ( String ): 否  私有网络的 ID。该参数用于指定边缘服务部署到的私有网络。如果设置了 vpc_identity，必须同时设置 cluster_name。 
            num ( Integer ): 是  实例的个数。 
            host_name_list ( Array of String ): 否  主机名的列表。系统按顺序将主机名赋给创建的边缘实例。系统允许您同时使用 host_name_list 和 instance_host_name 参数。 这两个参数会同时生效，但是 host_name_list 的优先级高于 instance_host_name。举例：如果您批量创建了 3 个边缘实例，将 instance_host_name 指定为了 host，将 host_name_list 指定为了 "hosta","hostb"，那么这 3 个边缘实例的名称将分别为 hosta，hostb 和 host-3。 
            default_isp ( String ): 否  默认运营商。该参数仅适用于三线节点。 
                  取值范围： 
                  - CMCC 
                  - CUCC 
                  - CTCC 
                  注意： 
                  - 当 external_network_mode 值为 single_interface_cmcc_ip、single_interface_cucc_ip、single_interface_ctcc_ip 时，default_isp 中指定的运营商须与 external_network_mode 中指定的运营商相同。 
                  - 当 external_network_mode 值为 single_interface_multi_ip 或 multi_interface_multi_ip 时，default_isp 参数必须指定，参数值可按需设置。 
                  - 当 external_network_mode 值为 single_interface_single_ip 或 no_interface 时，default_isp 无需指定。 
            external_network_mode ( Object of ExternalNetworkMode ): 否  公网配置。该参数仅适用于三线节点。 
                  取值范围： 
                  - single_interface_multi_ip：单网卡多 IP。如果您是三线节点的新用户，那么需提交工单开通相关权限。 
                  - single_interface_cmcc_ip：单网卡移动 IP。需提交工单开通相关权限。 
                  - single_interface_cucc_ip：单网卡联通 IP。需提交工单开通相关权限。 
                  - single_interface_ctcc_ip：单网卡电信 IP。需提交工单开通相关权限。 
                  - multi_interface_multi_ip：多网卡多 IP。需提交工单开通相关权限。 
                  - single_interface_single_ip：单网卡单 IP。该模式下，系统将根据库存随机分配一个运营商的公网 IP 地址。 
                  - no_interface：无公网网卡。需提交工单开通相关权限。 
                  默认值： 
                  - 当有公网网卡时： 
                  	- 单网卡多IP权限开启：默认采用single_interface_multi_ip（单网卡多 IP）。 
                  	- 单网卡多IP权限关闭：默认采用single_interface_single_ip（单网卡单 IP）。  
                  - 无公网网卡时，默认采用 no_interface。 
           "字段"： ScheduleStrategy
            schedule_strategy ( String ): 是  调度策略： 
                  - dispersion：城市分散。当您在多个区域创建多个边缘实例时，该策略表示系统优先选择不同城市的节点来下发边缘实例。 
                  - concentration：城市集中。当您在多个区域创建多个边缘实例时，该策略表示系统优先选择相同城市的节点来下发边缘实例。 
            price_strategy ( String ): 是  价格策略： 
                  - high_priority：优先高价。当您在多个区域创建多个边缘实例时，该策略表示系统优先选择带宽价格较高的城市的节点来下发边缘实例。 
                  - low_priority：优先低价。当您在多个区域创建多个边缘实例时，该策略表示系统优先选择带宽价格较低的城市的节点来下发边缘实例。 
           "字段"： CustomData
            data ( String ): 是  自定义数据。自定义数据为边缘实例的定制信息。 
           "字段"： BillingConfig
            computing_billing_method ( Object of ComputingBillingMethod ): 是  算力计费方式，取值范围： 
                  - MonthlyPeak：按月峰值计费。 
                  - DailyPeak：按日峰值计费。 
            bandwidth_billing_method ( Object of BandwidthBillingMethod ): 是  带宽计费方式，取值范围： 
                  - MonthlyP95：按月 95 峰值计费。 
                  - DailyPeak：按日峰值计费。 
            auto_prepay ( Boolean ): 否   
           "字段"： AdvancedConfiguration
            instance_name ( String ): 否  边缘实例的名称。当您批量创建边缘实例时，系统将为自定义实例名称添加数字后缀。举例：-1，-2。 
            instance_desc ( String ): 否  边缘实例的描述。当您批量创建边缘实例时，系统将为每个实例添加相同的描述。 
            instance_host_name ( String ): 否  自定义的主机名。当您批量创建边缘实例时，系统将为自定义主机名称添加数字后缀。举例：-1，-2。 
           "字段"： SystemDisk
            storage_type ( String ): 是  磁盘类型。取值范围： 
                  - CloudBlockHDD：HDD 型云盘。 
                  - CloudBlockSSD：SSD 型云盘。 
            capacity ( String ): 是  磁盘容量。单位：GB。容量范围： 
                  - 系统云盘：40 ~ 100。 
                  - 数据云盘：20 ~ 1000。 
                  取值须是 10 的倍数。如需更大磁盘容量，请提交工单申请。 
           "字段"： DataDisk
            storage_type ( String ): 是  磁盘类型。取值范围： 
                  - CloudBlockHDD：HDD 型云盘。 
                  - CloudBlockSSD：SSD 型云盘。 
            capacity ( String ): 是  磁盘容量。单位：GB。容量范围： 
                  - 系统云盘：40 ~ 100。 
                  - 数据云盘：20 ~ 1000。 
                  取值须是 10 的倍数。如需更大磁盘容量，请提交工单申请。 
           "字段"： DataDiskList
            storage_type ( String ): 是  磁盘类型。取值范围： 
                  - CloudBlockHDD：HDD 型云盘。 
                  - CloudBlockSSD：SSD 型云盘。 
            capacity ( String ): 是  磁盘容量。单位：GB。容量范围： 
                  - 系统云盘：40 ~ 100。 
                  - 数据云盘：20 ~ 1000。 
                  取值须是 10 的倍数。如需更大磁盘容量，请提交工单申请。 
    """,
    "update_cloud_server": r""" 
   Args: 
       body: A JSON structure
            cloud_server_identity ( String ): 是  边缘服务 ID。您可以通过 ListCloudServers 接口查询边缘服务 ID。 
            cloud_server_desc ( String ): 否  边缘服务的描述信息，最多可输入 80 个字符。 
                  如果不指定该项参数值，代表不修改描述信息。 
            image_identity ( String ): 否  镜像 ID。您可以通过 ListImages 接口查询镜像 ID。 
            storage_config ( Object of StorageConfig ): 否  存储配置，包括系统盘和数据盘的类型和容量信息。 
                  详情请参见 StorageConfig。 
            secret_config ( Object of SecretConfig ): 否  边缘实例的登录密码设置，支持自定义类型和 SSH Key 类型的密码。 
                  详情请参见 SecretConfig。 
                  如果不指定该项参数值，代表不修改登录密码设置。 
            network_config ( Object of NetworkConfig ): 否  网络配置。 
                  详情请参见 NetworkConfigUpdateReq。 
            custom_data ( Object of CustomData ): 否  自定义数据。自定义数据为边缘实例的定制信息。最大可输入 16 KB 的自定义数据。 
                  如果不指定该项参数值，代表不修改自定义数据。 
                  说明：  
                  - 自定义数据只支持Shell脚本。您需要使用明文方式输入脚本，平台将自动对脚本进行Base64编码。请勿直接输入Base64编码后的脚本。对于Linux系统，脚本通常以 !/bin/bash 开头；对于Windows系统，脚本可以直接输入。 
                  - 输入的脚本将在边缘实例首次启动时执行。 
            instance_project ( String ): 否  新增的边缘实例所属的项目。如果不设置该参数，将保留原来的取值。如果参数值为空字符串，采用默认值 default。 
            advanced_configuration ( Object of AdvancedConfiguration ): 否   
            billing_config ( Object of BillingConfig ): 否   
            disable_vga ( Boolean ): 否   
           "字段"： StorageConfig
            system_disk ( Object of SystemDisk ): 是  系统盘。 
                  详情请参见 DiskSpec。 
            data_disk ( Object of DataDisk ): 否  数据盘。该参数用于添加单块数据盘。 
                  详情请参见 DiskSpec。 
            data_disk_list ( Array of DataDiskList ): 否  数据盘列表。该参数用于添加一块或多块数据盘。 
                  详情请参见 DiskSpec。 
           "字段"： SecretConfig
            secret_type ( Object of SecretType ): 是  边缘实例的登录密码的类型。取值范围： 
                  - 2：自定义密码。 
                  - 3：SSH Key 类型密码。 
                  - 4: 代表不注入登录凭证。 
            secret_data ( String ): 否  登录密码。 
                  - 自定义密码：密码输入规则如下： 
                  	- 允许 8 ~ 30个字符。密码须至少包含以下类型中的3种：大写字母、小写字母、数字和特殊字符。 
                  	- 支持特殊字符 ()`~!@#$%^&*-+=_{}[]:;',.?/。  
                  	- 不能包含双引号（"）、反斜线（ ）和空格，且不能以正斜线（/）开头。 
                  - SSH Key 类型密码：输入SSH 密钥对的 ID。您可以通过 ListSSHKey 接口查询密钥对 ID。 
           "字段"： NetworkConfig
            bandwidth_peak ( String ): 否  公网带宽峰值。取值范围：[5,实例规格支持的带宽上限]。取值须是 5 的倍数。单位：Mbps。 
                  当您选择 IPv4/IPv6 双栈边缘实例时，所设的带宽峰值将被 IPv4 和 IPv6 公网 IP 地址共享。 
                  disable_ipv4 设置为 true 时，无需配置 bandwidth_peak 参数。 
            enable_ipv6 ( Boolean ): 否  是否启用 IPv6。取值范围： 
                  - true ：启用 IPv6。 
                  - false（默认值）：禁用 IPv6。 
                  默认分配 IPv4 地址。当您启用 IPv6 时，系统会为边缘实例分配 IPv4 和 IPv6 两个公网 IP 地址。 
            disable_ipv4 ( Boolean ): 否  是否禁用 IPv4。取值范围： 
                  - true ：禁用 IPv4。 
                  - false（默认值）：启用 IPv4。 
            custom_internal_interface_name ( String ): 否  私网网卡的名称。目前仅 VLANVF 规格实例的私网网卡的名称可以被修改。 
            custom_external_interface_name ( String ): 否  公网网卡的名称。目前仅 VLANVF 规格实例的公网网卡的名称可以被修改。 
            dns_type ( Object of DnsType ): 否  DNS 类型： 
                  - default：默认 DNS。 
                  - custom：自定义 DNS。 
                  如果不设置该参数，代表使用默认的 DNS 配置，即首选 DNS 为114.114.114.114，备用 DNS 为 223.6.6.6。 
                  暂不支持为裸金属实例配置 DNS。当实例规格为裸金属时，无需设置 dns_type 和 dns_list 参数。 
            dns_list ( Array of String ): 否  DNS 列表。前面的 IP 地址代表首选 DNS，后面的 IP 地址代表备用 DNS。 
                  - 当前最多支持一条首选 DNS 和一条备用 DNS。 
                  - 当 dns_type 设置为 default 时，不允许设置 dns_list。此时，采用默认的 DNS 配置，即首选 DNS 为 114.114.114.114，备用 DNS 为223.6.6.6。 
                  - 当 dns_type 设置为 custom 时，必须设置 dns_list。至少需要配置一条首选 DNS。可按需配置一条备用 DNS。 
           "字段"： CustomData
            data ( String ): 是  自定义数据。自定义数据为边缘实例的定制信息。 
           "字段"： AdvancedConfiguration
            instance_name ( String ): 否   
            instance_desc ( String ): 否   
            instance_host_name ( String ): 否   
            delete_protection ( Boolean ): 否   
           "字段"： BillingConfig
            computing_billing_method ( Object of ComputingBillingMethod ): 是   
            bandwidth_billing_method ( Object of BandwidthBillingMethod ): 是   
            pre_paid_period ( Object of PrePaidPeriod ): 否   
            pre_paid_period_number ( Long ): 否   
            auto_renew ( Boolean ): 否   
            auto_prepay ( Boolean ): 否   
           "字段"： SystemDisk
            storage_type ( String ): 是  磁盘类型。取值范围： 
                  - CloudBlockHDD：HDD 型云盘。 
                  - CloudBlockSSD：SSD 型云盘。 
            capacity ( String ): 是  磁盘容量。单位：GB。容量范围： 
                  - 系统云盘：40 ~ 100。 
                  - 数据云盘：20 ~ 1000。 
                  取值须是 10 的倍数。如需更大磁盘容量，请提交工单申请。 
           "字段"： DataDisk
            storage_type ( String ): 是  磁盘类型。取值范围： 
                  - CloudBlockHDD：HDD 型云盘。 
                  - CloudBlockSSD：SSD 型云盘。 
            capacity ( String ): 是  磁盘容量。单位：GB。容量范围： 
                  - 系统云盘：40 ~ 100。 
                  - 数据云盘：20 ~ 1000。 
                  取值须是 10 的倍数。如需更大磁盘容量，请提交工单申请。 
           "字段"： DataDiskList
            storage_type ( String ): 是  磁盘类型。取值范围： 
                  - CloudBlockHDD：HDD 型云盘。 
                  - CloudBlockSSD：SSD 型云盘。 
            capacity ( String ): 是  磁盘容量。单位：GB。容量范围： 
                  - 系统云盘：40 ~ 100。 
                  - 数据云盘：20 ~ 1000。 
                  取值须是 10 的倍数。如需更大磁盘容量，请提交工单申请。 
    """,
    "get_cloud_server": r""" 
   Args: 
       params: A JSON structure
            cloud_server_id ( String ): 是  边缘服务 ID。您可以通过 ListCloudServers 接口查询边缘服务 ID。 
    """,
    "reboot_instances": r""" 
   Args: 
       body: A JSON structure
            instance_identities ( Array of String ): 是  边缘实例 ID 列表。您可以通过 list_instances 工具查询边缘实例 ID。 
    """,
    "start_instances": r""" 
   Args: 
       body: A JSON structure
            instance_identities ( Array of String ): 是  边缘实例 ID 列表。您可以通过 list_instances 工具查询边缘实例 ID。 
    """,
    "stop_instances": r""" 
   Args: 
       body: A JSON structure
            instance_identities ( Array of String ): 是  边缘实例 ID 列表。您可以通过 list_instances 工具查询边缘实例 ID。 
    """,
    "list_instances": r""" 
   Args: 
       params: A JSON structure
            countries ( String ): 否  国家。 
            regions ( String ): 否  区域。区域之间用半角逗号（,）分隔。 
                  您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            cities ( String ): 否  城市代码。城市之间用半角逗号（,）分隔。 
                  您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            isps ( String ): 否  运营商。运营商之间用半角逗号（,）分隔。 
                  您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            status ( String ): 否  边缘实例的状态。实例状态之间用半角逗号（,）分隔。取值范围： 
                  - opening：创建中。 
                  - starting：启动中。 
                  - running：运行中。 
                  - stopping：停止中。 
                  - stop：已停止。 
                  - rebooting：重启中。 
                  - terminating：删除中。 
                  - open_fail：创建失败。 
            cluster_names ( String ): 否  节点名称的列表。名称之间用半角逗号（,）分隔。 
            ips ( String ): 否  IP 地址列表。IP 之间用半角逗号（,）分隔。 
            cidrs ( String ): 否  子网 CIDR 地址列表。CIDR 地址之间用半角逗号（,）分隔。 
            cloud_server_identities ( String ): 否  边缘服务 ID 列表。ID 之间用半角逗号（,）分隔。 
            spec_names ( String ): 否  边缘实例规格名称。实例规格之间用半角逗号（,）分隔。 
            instance_identities ( String ): 否  边缘实例 ID。ID 之间用半角逗号（,）分隔。 
            instance_uuids ( String ): 否  边缘实例 UUID。UUID 之间用半角逗号（,）分隔。 
            instance_names ( String ): 否  边缘实例名称。名称之间用半角逗号（,）分隔。 
            fuzzy_ip_with_dots ( String ): 否  IPv4 地址。支持模糊查询。IP 地址采用点分十进制格式。 
            vpc_identities ( String ): 否  私有网络 ID。ID 之间用半角逗号（,）分隔。 
            page ( Integer ): 否  边缘实例列表的页码。 
                  如果 page 和 limit 参数都不指定，将返回全量数据；如果仅指定 limit，不指定 page ，将返回第 1 页数据；如果仅指定 page，不指定 limit，将返回全量数据；如果 page 和 limit 都指定，将返回符合条件的数据。 
            limit ( Integer ): 否  分页查询时设置的每页行数。 
                  如果 page 和 limit 参数都不指定，将返回全量数据；如果仅指定 limit，不指定 page ，将返回第 1 页数据；如果仅指定 page，不指定 limit，将返回全量数据；如果 page 和 limit 都指定，将返回符合条件的数据。 
            order_by ( Integer ): 否  查询出来的边缘实例的排列顺序，按照创建时间排序。取值范围： 
                  - 1（默认值）：按照降序排列。 
                  - 2：按照升序排列。 
    """,
    "get_instance": r""" 
   Args: 
       params: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具获取边缘实例 ID。 
    """,
    "reset_login_credential": r""" 
   Args: 
       body: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
    """,
    "set_instance_name": r""" 
   Args: 
       body: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
            instance_name ( String ): 是  实例名称。命名规则如下： 
                  - 允许5~80个字符。 
                  - 支持中文、大写字母、小写字母、数字。 
                  - 支持特殊字符()`~!@#$%^&*-+=_{}[]:;',.?/。 
                  - 不能包含双引号（"）、反斜线（ ）和空格，且不能以正斜线（/）开头。 
    """,
    "batch_reset_system": r""" 
   Args: 
       body: A JSON structure
            instance_identities ( Array of String ): 是  边缘实例 ID 列表。您可以通过 list_instances 工具查询边缘实例 ID。 
            image_identity ( String ): 否  新镜像的 ID。您可以通过 ListImages 接口查询镜像 ID。 
                  该参数用于为边缘实例更换镜像。如果您不指定该参数的值，代表不更换边缘实例的镜像。 
    """,
    "set_instances_bandwidth_peak": r""" 
   Args: 
       body: A JSON structure
            instance_bandwidth_peak_map ( JSON Map ): 是  边缘实例的带宽峰值。 
            with_reboot ( Boolean ): 是  是否重启实例。取值范围： 
                  - true：重启实例。 
                  - false：不重启实例。 
                  - 对于私有网络型实例，您在为其修改带宽峰值后无需重启实例。新的带宽峰值会直接生效。因此，建议您将 with_reboot 参数设置为 false。 
                  - 对于直通型实例，您在为其修改带宽峰值后必须重启实例。这样，新的带宽峰值才会生效。您可以将 with_reboot 参数设置为 true，系统将自动重启实例。 如需使用直通型实例，请提交工单。 
                  - 如果您指定的实例中既包含私有网络型实例又包含直通型实例，且您将 with_reboot 参数设置为 true，系统仅会重启直通型实例。 
    """,
    "enable_instances_i_pv6": r""" 
   Args: 
       body: A JSON structure
            instance_identities ( Array of String ): 是  边缘实例 ID 列表。您可以通过 list_instances 工具查询边缘实例 ID。 
            with_reboot ( Boolean ): 是  是否重启实例。取值范围： 
                  - true：重启实例。 
                  - false：不重启实例。 
                  说明：  
                  重启实例后，IPv6 的配置才能生效。 
    """,
    "get_instances_i_pv6_upgrade_status": r""" 
   Args: 
       params: A JSON structure
            instance_identities ( String ): 是  边缘实例 ID 列表。ID 之间用半角逗号（,）分隔。 
    """,
    "update_instances_spec": r""" 
   Args: 
       body: A JSON structure
            instance_identities ( Array of String ): 是  边缘实例 ID 列表。您可以通过 list_instances 工具查询边缘实例 ID。 
            new_spec_name ( String ): 是  新的实例规格的名称。您可以通过 ListInstanceTypes 接口查询可开通的实例规格。 
    """,
    "list_instance_internal_ips": r""" 
   Args: 
       params: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
    """,
    "set_bound_eip_share_bandwidth_peak": r""" 
   Args: 
       body: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
            bound_eip_share_bandwidth_peak ( String ): 是  弹性公网 IP 的共享带宽峰值。取值范围与弹性公网 IP 绑定的边缘实例的公网带宽峰值的范围一致。取值须是 5 的倍数。单位：Mbps。 
    """,
    "batch_bind_eip_to_internal_ips_randomly": r""" 
   Args: 
       body: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
            internal_ips ( Array of String ): 是  需要绑定的私网 IP 地址的列表。您可以通过 ListInstanceInternalIps 接口查询边缘实例的私网 IP 地址。 
    """,
    "batch_delete_internal_ips": r""" 
   Args: 
       body: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
            internal_ips ( Array of String ): 是  私网 IP 地址列表。您可以通过 ListInstanceInternalIps 接口查询边缘实例的私网 IP 地址。 
    """,
    "get_instance_cloud_disk_info": r""" 
   Args: 
       params: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
    """,
    "set_cloud_server_delete_protection": r""" 
   Args: 
       body: A JSON structure
            cloud_server_identity ( String ): 是  边缘服务的 ID。您可以通过 ListCloudServers 接口查询边缘服务的 ID。 
            cloud_server_delete_protection ( Boolean ): 否  是否为边缘服务开启删除保护。取值范围： 
                  - true：开启删除保护。 
                  - false：关闭删除保护。 
    """,
    "set_instance_delete_protection": r""" 
   Args: 
       body: A JSON structure
            instance_ids ( Array of String ): 是  边缘实例 ID 列表。您可以通过 list_instances 工具查询边缘实例 ID。 
            instance_delete_protection ( Boolean ): 否  是否为边缘实例开启删除保护。取值范围： 
                  - true：开启删除保护。 
                  - false：关闭删除保护。 
    """,
    "list_cloud_servers": r""" 
   Args: 
       params: A JSON structure
            fuzzy_name ( String ): 否  边缘服务名称。支持模糊查询。 
            page ( Integer ): 否  边缘服务列表的页码。 
                  如果 page 和 limit 参数都不指定，将返回全量数据；如果仅指定 limit，不指定 page ，将返回第 1 页数据；如果仅指定 page，不指定 limit，将返回全量数据；如果 page 和 limit 都指定，将返回符合条件的数据。 
            limit ( Integer ): 否  分页查询时设置的每页行数。 
                  默认值：10。 
                  如果 page 和 limit 参数都不指定，将返回全量数据；如果仅指定 limit，不指定 page ，将返回第 1 页数据；如果仅指定 page，不指定 limit，将返回全量数据；如果 page 和 limit 都指定，将返回符合条件的数据。 
            order_by ( Integer ): 否  查询出来的边缘服务的排列顺序，按照创建时间排序。取值范围： 
                  - 1（默认值）：按照降序排列。 
                  - 2：按照升序排列。 
    """,
    "list_instance_types": r""" 
    """,
    "list_available_resource_info": r""" 
   Args: 
       params: A JSON structure
            instance_type ( String ): 是  实例规格。您可以通过 ListInstanceTypes 接口获取可开通的实例规格。 
            cloud_disk_type ( String ): 是  磁盘类型。取值范围： 
                  - CloudHDD：HDD 型云盘。 
                  - CloudSSD：SSD 型云盘。 
    """,
    "create_instance": r""" 
   Args: 
       body: A JSON structure
            cloud_server_identity ( String ): 是  边缘实例所属的边缘服务的 ID。您可以通过 ListCloudServers 接口查询边缘服务的 ID。 
            instance_area_nums ( Array of InstanceAreaNums ): 是  边缘实例的地域信息。 
           "字段"： InstanceAreaNums
            area_name ( String ): 否  区域名称。您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            isp ( String ): 否  运营商。您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            cluster_name ( String ): 否  节点名称。指定希望部署边缘服务的节点。您可以通过 ListAvailableResourceInfo 接口查询实例规格支持的区域、城市、运营商、节点信息。 
            vpc_identity ( String ): 否  私有网络的 ID。该参数用于指定边缘服务部署到的私有网络。如果设置了 vpc_identity，必须同时设置 cluster_name。 
            num ( Integer ): 是  实例的个数。 
            host_name_list ( Array of String ): 否  主机名的列表。系统按顺序将主机名赋给创建的边缘实例。系统允许您同时使用 host_name_list 和 instance_host_name 参数。 这两个参数会同时生效，但是 host_name_list 的优先级高于 instance_host_name。举例：如果您批量创建了 3 个边缘实例，将 instance_host_name 指定为了 host，将 host_name_list 指定为了 "hosta","hostb"，那么这 3 个边缘实例的名称将分别为 hosta，hostb 和 host-3。 
            default_isp ( String ): 否  默认运营商。该参数仅适用于三线节点。 
                  取值范围： 
                  - CMCC 
                  - CUCC 
                  - CTCC 
                  注意： 
                  - 当 external_network_mode 值为 single_interface_cmcc_ip、single_interface_cucc_ip、single_interface_ctcc_ip 时，default_isp 中指定的运营商须与 external_network_mode 中指定的运营商相同。 
                  - 当 external_network_mode 值为 single_interface_multi_ip 或 multi_interface_multi_ip 时，default_isp 参数必须指定，参数值可按需设置。 
                  - 当 external_network_mode 值为 single_interface_single_ip 或 no_interface 时，default_isp 无需指定。 
            external_network_mode ( String ): 否  公网配置。该参数仅适用于三线节点。 
                  取值范围： 
                  - single_interface_multi_ip：单网卡多 IP。如果您是三线节点的新用户，那么需提交工单开通相关权限。 
                  - single_interface_cmcc_ip：单网卡移动 IP。需提交工单开通相关权限。 
                  - single_interface_cucc_ip：单网卡联通 IP。需提交工单开通相关权限。 
                  - single_interface_ctcc_ip：单网卡电信 IP。需提交工单开通相关权限。 
                  - multi_interface_multi_ip：多网卡多 IP。需提交工单开通相关权限。 
                  - single_interface_single_ip：单网卡单 IP。该模式下，系统将根据库存随机分配一个运营商的公网 IP 地址。 
                  - no_interface：无公网网卡。需提交工单开通相关权限。 
                  默认值： 
                  - 当有公网网卡时： 
                  	- 单网卡多IP权限开启：默认采用single_interface_multi_ip（单网卡多 IP）。 
                  	- 单网卡多IP权限关闭：默认采用single_interface_single_ip（单网卡单 IP）。  
                  - 无公网网卡时，默认采用 no_interface。 
    """,
    "create_secondary_internal_ip_and_reboot": r""" 
   Args: 
       body: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
            num ( Integer ): 是  新增的辅助私网 IP 地址的数量。您可以通过 ListInstanceInternalIps 接口获取私网 IP 地址列表。 
    """,
    "bind_eip_to_internal_ip": r""" 
   Args: 
       body: A JSON structure
            instance_identity ( String ): 是  边缘实例 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
            eip_identity ( String ): 是  弹性公网 IP 的 ID。 
            internal_ip ( String ): 是  私网 IP 地址列表。您可以通过 ListInstanceInternalIps 接口查询边缘实例的私网 IP 地址。 
    """,
    "list_images": r""" 
   Args: 
       params: A JSON structure
            instance_type ( String ): 是  实例规格。您可以通过 list_instance_types 接口获取可开通的实例规格。 
            system_arch ( String ): 否  操作系统的架构。取值范围： 
                  - Linux：Linux 操作系统。 
                  - Windows：Windows 操作系统。 
            system_bit ( String ): 否  操作系统的位数。取值范围： 
                  - 32：32位操作系统。 
                  - 64：64位操作系统。 
            system_type ( String ): 否  操作系统的类型。取值范围： 
                  Linux： 
                  - CentOS 
                  - Ubuntu 
                  - Debian 
                  Windows： 
                  - Windows 
            system_version ( String ): 否  操作系统的版本。取值范围： 
                  CentOS： 
                  - 6.9 
                  - 7.2 
                  - 7.3 
                  - 7.4 
                  - 7.5 
                  - 7.6 
                  - 7.8 
                  - 7.9 
                  - 8.3 
                  Debian： 
                  - 9 
                  - 10 
                  Ubuntu： 
                  - Server 16.04 LTS 
                  - Server 18.04 LTS 
                  - Server 20.04 LTS 
                  Windows： 
                  - 10 
                  - 2012 R2 STD 标准版 
                  - 2016 STD 标准版 
                  - 2019 STD 标准版 
            disk_size ( Integer ): 否  镜像的系统盘的大小。单位：GB。 
            label ( String ): 否  镜像标签，取值范围： 
                  - IPV6：IPv6。 
                  - MultiIPPriNet：辅助私网 IP。 
                  镜像标签之间用半角逗号（,）分隔。 
                  说明： 
                  - label 参数仅在 property 参数的值为 PublicBaseImage生效。 
                  - 如果您没有开通 IPv6、辅助私网 IP 功能，无法通过指定 label 参数来列出相关镜像。如需开通相关功能，请提交工单申请。 
            property ( String ): 否  镜像属性，取值范围： 
                  - BENBuildImage：通过边缘实例创建的镜像。 
                  - LocalImage：本地镜像。 
                  - PublicBaseImage：公共镜像。 
                  - UrlImage：通过 URL 上传的镜像。 
    """,
    "get_image": r""" 
   Args: 
       params: A JSON structure
            image_id ( String ): 是  镜像 ID。您可以通过 list_images 接口查询镜像 ID。 
    """,
    "build_image_by_vm": r""" 
   Args: 
       body: A JSON structure
            veen_vm_id ( String ): 是  用于创建镜像的边缘实例的 ID。您可以通过 list_instances 工具查询边缘实例 ID。 
            image_name ( String ): 是  镜像名称。命名规则如下： 
                  - 允许 5~80 个字符。 
                  - 支持中文、大写字母、小写字母、数字。 
                  - 支持特殊字符 ()`~!@#$%^&*-+=_{}[]:;',.?/。 
                  - 不能包含双引号（"）、反斜线（ ）和空格，且不能以正斜线（/）开头。 
            description ( String ): 否  镜像的描述信息。 
    """,
    "upload_url_image": r""" 
   Args: 
       body: A JSON structure
            image_name ( String ): 是  镜像名称。命名规则如下： 
                  - 允许 5~80 个字符。 
                  - 支持中文、大写字母、小写字母、数字。 
                  - 支持特殊字符 ()`~!@#$%^&*-+=_{}[]:;',.?/。 
                  - 不能包含双引号（"）、反斜线（ ）和空格，且不能以正斜线（/）开头。 
            url ( String ): 是  上传的镜像的地址。 
            system_arch ( String ): 是  操作系统。取值范围： 
                  - Linux：Linux操作系统。 
                  - Windows：Windows操作系统。 
            system_bit ( String ): 是  系统架构。取值范围： 
                  - 32：32位操作系统。 
                  - 64：64位操作系统。 
            system_type ( String ): 是  系统平台。取值范围： 
                  Linux： 
                  - CentOS 
                  - Ubuntu 
                  - Debian 
                  Windows： 
                  - Windows 
            system_version ( String ): 是  镜像系统版本。取值范围： 
                  CentOS： 
                  - 6.9 
                  - 7.2 
                  - 7.3 
                  - 7.4 
                  - 7.5 
                  - 7.6 
                  - 7.8 
                  - 7.9 
                  - 8.3 
                  Debian： 
                  - 9 
                  - 10 
                  Ubuntu： 
                  - Server 16.04 LTS 
                  - Server 18.04 LTS 
                  - Server 20.04 LTS 
                  Windows： 
                  - 10 
                  - 2012 R2 STD 标准版 
                  - 2016 STD 标准版 
                  - 2019 STD 标准版 
            disk_size ( Integer ): 是  系统盘大小。该参数值代表您在使用该镜像创建边缘实例时，系统盘可选的最小值。单位：GB。取值范围：50~100。该参数值须为 10 的倍数。 
            description ( String ): 否  镜像的描述信息。 
    """,
    "update_image": r""" 
   Args: 
       body: A JSON structure
            image_id ( String ): 是  镜像 ID。 
            image_name ( String ): 否  镜像名称。 
            description ( String ): 否  镜像的描述信息。 
    """,
    "delete_image": r""" 
   Args: 
       body: A JSON structure
            image_id ( String ): 是  镜像 ID。您可以通过 ListImages 接口查询镜像 ID。 
    """,
    "get_veen_instance_usage": r""" 
   Args: 
       params: A JSON structure
            start_bill_cycle ( String ): 是  账单的起始时间。格式为 YYYY-MM。 
            end_bill_cycle ( String ): 是  账单的结束时间。格式为 YYYY-MM。 
            bill_method ( String ): 否  计费方式，取值范围： 
                  - MonthlyPeak（默认值）：按月峰值计费。 
                  - DailyPeak：按日峰值计费。如您有日峰值计费或其他方式计费需求，请提交工单。 
    """,
    "get_veew_instance_usage": r""" 
   Args: 
       params: A JSON structure
            start_bill_cycle ( String ): 是  账单的起始时间。格式为 YYYY-MM。 
            end_bill_cycle ( String ): 是  账单的结束时间。格式为 YYYY-MM。 
            bill_method ( String ): 否  计费方式，取值范围： 
                  - MonthlyPeak（默认值）：按月峰值计费。 
                  - DailyPeak：按日峰值计费。如您有日峰值计费或其他方式计费需求，请提交工单。 
    """,
    "get_bandwidth_usage": r""" 
   Args: 
       params: A JSON structure
            start_bill_cycle ( String ): 是  账单的起始时间。格式为 YYYY-MM。 
            end_bill_cycle ( String ): 是  账单的结束时间。格式为 YYYY-MM。 
            bill_method ( String ): 否  计费方式，取值范围： 
                  - MonthlyP95（默认值 ）：按月 95 峰值计费。 
                  - DailyPeak：按日峰值计费。如您有日峰值计费或其他方式计费需求，请提交工单。 
    """,
    "get_billing_usage_detail": r""" 
   Args: 
       params: A JSON structure
            start_date ( String ): 是  统计起始时间。格式为 YYYY-MM-DD。 
            end_date ( String ): 是  统计结束时间。格式为 YYYY-MM-DD。 
            charge_item ( String ): 是  查询的计费项，取值范围： 
                  - CPU：CPU 核数。 
                  - MEM：内存，单位：GB。 
                  - InstanceCount：实例数量。 
                  - Storage：存储，单位：GB。 
            bill_method ( String ): 否  计费方式，取值范围： 
                  - *MonthlyPeak *（默认值）：按月峰值计费。 
                  - DailyPeak：按日峰值计费。如您有日峰值计费或其他方式计费需求，请提交工单。 
    """,
    "list_vpc_instances": r""" 
   Args: 
       params: A JSON structure
            page ( String ): 否  私有网络列表的页码。 
            limit ( Integer ): 否  分页查询时设置的每页行数。 
            order_by ( Integer ): 否  查询出来的私有网络的排列顺序，按照创建时间排序。取值范围： 
                  - 1：按照降序排列。 
                  - 2（默认值）：按照升序排列。 
            cluster_names ( String ): 否  节点名称的列表。多个节点之间用半角逗号（,）分隔。 
            vpc_identity_list ( String ): 否  私有网络 ID 的列表。多个私有网络之间用半角逗号（,）分隔。 
            fuzzy_vpc_id_or_name ( String ): 否  私有网络 ID 或者名称。支持模糊查询。 
            with_resource_statistic ( Boolean ): 否  是否返回私有网络下的资源的统计数据。取值范围： 
                  - true：返回资源的统计数据。 
                  - false：不返回资源的统计数据。 
    """,
    "set_vpc_instance_desc": r""" 
   Args: 
       body: A JSON structure
            vpc_identity ( String ): 是  私有网络的 ID。 
            desc ( String ): 否  私有网络的描述。如果不指定该参数或参数值为空字符串，原来的描述将被清空。 
    """,
    "list_route_tables": r""" 
   Args: 
       params: A JSON structure
            route_table_list ( String ): 否  路由表 ID 列表。ID 之间用半角逗号（,）分隔。 
            status_list ( String ): 否  路由表状态列表。路由表状态之间用半角逗号（,）分隔。取值范围： 
                  - updating：变更中。 
                  - running：运行中。 
                  	如果不指定该参数，系统将查询所有状态的路由表。 
            type_list ( String ): 否  路由表类型列表。路由表类型之间用半角逗号（,）分隔。取值范围： 
                  - default：默认路由表。 
                  	如果不指定该参数，系统将查询所有类型的路由表。 
            fuzzy_route_table_id ( String ): 否  路由表 ID。支持模糊查询。 
            fuzzy_route_table_name ( String ): 否  路由表名称。支持模糊查询。 
            fuzzy_vpc_id ( String ): 否  私有网络 ID。支持模糊查询。 
            cluster_name_list ( String ): 否  节点列表。节点之间用半角逗号（,）分隔。 
            page ( Integer ): 否  路由表列表的页码。如果不填，将返回第 1 页的数据。 
            limit ( Integer ): 否  分页查询时设置的每页行数。 
                  默认值：10。 
            order_by ( Integer ): 否  查询出来的路由表的排列顺序，按照创建时间排序。取值范围： 
                  - 1（默认值）：按照降序排列。 
                  - 2：按照升序排列。 
    """,
    "get_route_table": r""" 
   Args: 
       params: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
    """,
    "set_route_table_name_and_desc": r""" 
   Args: 
       body: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
            name ( String ): 否  路由表名称。命名规则如下： 
                  - 允许 5~50 个字符。 
                  - 支持中文、大写字母、小写字母、数字。 
                  - 支持特殊字符 ()`~!@#$%^&*-+=_{}[]:;',.?/。 
                  - 不能包含双引号（"）、反斜线（ ）和 空格，且不能以正斜线（/）开头。 
                  	如果不指定该参数，系统将保留原来的名称。 
            desc ( String ): 否  路由表描述。 
                  如果不指定该参数，系统将保留原来的描述。 
    """,
    "list_route_entries": r""" 
   Args: 
       params: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
            route_entry_type_list ( String ): 是  路由条目类型。取值范围： 
                  - system：系统路由。 
                  - custom：自定义路由。 
            route_entry_next_hop_list ( String ): 否  路由条目的下一跳列表。下一跳之间用半角逗号（,）分隔。 
                  如果不指定该参数，系统将查询所有相关的路由条目。 
            page ( Integer ): 否  路由条目列表的页码。如果不指定该参数，系统将返回第 1 页的数据。 
            limit ( Integer ): 否  分页查询时设置的每页行数。 
                  默认值：10。 
            order_by ( Integer ): 否  查询出来的路由条目的排列顺序，按照创建时间排序。取值范围： 
                  - 1（默认值）：按照降序排列。 
                  - 2：按照升序排列。 
    """,
    "create_route_entries": r""" 
   Args: 
       body: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
            route_entry_list ( Array of RouteEntryList ): 是  要增加的路由条目的列表。 
           "字段"： RouteEntryList
            type ( String ): 是  路由条目的类型。取值范围： 
                  - custom：自定义路由条目。 
            dest_cidr ( String ): 是  目的地址。目的地址使用 CIDR 格式。不支持 IPv6 地址。 
            next_hop_type ( String ): 是  下一跳类型。取值范围： 
                  - veen：边缘实例。 
                  - vpc_vgw：边缘云网关。 
            next_hop ( String ): 是  下一跳。 
            desc ( String ): 否  路由条目的描述。最多可输入 80 个字符。 
            is_enable ( Boolean ): 是  是否启用路由条目。取值范围： 
                  - true：启用路由条目。 
                  - false：不启用路由条目。 
    """,
    "delete_route_entry": r""" 
   Args: 
       body: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
            route_entry_identity ( String ): 是  路由条目 ID。您可以通过 ListRouteEntries 接口获取路由条目 ID。 
    """,
    "enable_route_entry": r""" 
   Args: 
       body: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
            route_entry_identity ( String ): 是  路由条目 ID。您可以通过 ListRouteEntries 接口获取路由条目 ID。 
    """,
    "disable_route_entry": r""" 
   Args: 
       body: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
            route_entry_identity ( String ): 是  路由条目 ID。您可以通过 ListRouteEntries 接口获取路由条目 ID。 
    """,
    "set_route_entry_desc": r""" 
   Args: 
       body: A JSON structure
            route_table_identity ( String ): 是  路由表 ID。您可以通过 ListRouteTables 接口获取路由表 ID。 
            route_entry_identity ( String ): 是  路由条目 ID。您可以通过 ListRouteEntries 接口获取路由条目 ID。 
            desc ( String ): 是  路由条目的描述。最多可输入 80 个字符。 
    """,
}
