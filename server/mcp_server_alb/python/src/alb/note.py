note = {
    "describe_acl_attributes": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            AclId ( String ): 是  访问控制策略组ID。 
    """,
    "describe_ca_certificates": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            CACertificateIds ( Array of String ): 否   
            CACertificateName ( String ): 否  CA 证书的名称。 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值1-100，默认为10。 
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            TagFilters ( Array of String ): 否   
            ProjectName ( String ): 否  CA 证书所属项目名称。 
    """,
    "describe_acls": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            AclIds ( Array of String ): 否   
            PageSize ( Integer ): 否  分页查询时每页的行数，取值：1 ~ 100，默认为10。 
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            AclName ( String ): 否  访问控制策略组的名称。 
            TagFilters ( Array of String ): 否   
            ProjectName ( String ): 否  访问控制所属项目名称。 
    """,
    "describe_certificates": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            CertificateName ( String ): 否  证书的名称。 
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值1-100，默认为10。 
            CertificateIds ( Array of String ): 否   
            TagFilters ( Array of String ): 否   
            ProjectName ( String ): 否  证书所属项目名称。 
    """,
    "describe_customized_cfgs": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值：1 ~ 100，默认为10。 
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            ListenerId ( String ): 否  查询指定监听器关联的个性化配置。 
            CustomizedCfgName ( String ): 否  要查询的个性化配置名称。 
            CustomizedCfgIds ( Array of String ): 否   
            TagFilters ( Array of String ): 否   
            ProjectName ( String ): 否  个性化配置所属项目名称。 
    """,
    "describe_all_certificates": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ProjectName ( String ): 否  证书所属项目名称。 
            TagFilters ( Array of String ): 否   
            CertificateIds ( Array of String ): 否   
            CertificateName ( String ): 否  证书的名称。 
            CertificateType ( String ): 否  证书的类型，取值有如下两种： 
                  - CA：CA证书。 
                  - Server：服务器证书。 
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值1-100，默认为10。 
    """,
    "describe_listener_attributes": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ListenerId ( String ): 是  监听器 ID 。 
    """,
    "describe_listeners": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            TagFilters ( Array of String ): 否   
            ListenerName ( String ): 否  监听器的名字。 
            LoadBalancerId ( String ): 否  负载均衡实例ID。 
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值1-100，默认为10。 
            ListenerIds ( Array of String ): 否   
            Protocol ( String ): 否  监听器的协议。仅支持： 
                  - HTTP。 
                  - HTTPS。 
            ProjectName ( String ): 否  监听器所属项目名称。 
    """,
    "describe_load_balancer_attributes": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            LoadBalancerId ( String ): 是  ALB 实例 ID。 
    """,
    "describe_customized_cfg_attributes": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            CustomizedCfgId ( String ): 是  要查询的个性化配置 ID。 
    """,
    "describe_health_check_templates": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            TagFilters ( Array of String ): 否   
            HealthCheckTemplateIds ( Array of String ): 否   
            HealthCheckTemplateName ( String ): 否  健康检查模板的名称。 
            PageNumber ( Integer ): 否  列表的页码，默认值为 1。 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值1-100，默认为10。 
            ProjectName ( String ): 否  健康检查模版所属项目名称。 
    """,
    "describe_listener_health": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ListenerIds ( Array of String ): 否   
            OnlyUnHealthy ( String ): 否  配置是否仅返回健康检查状态“异常”的后端服务器信息，取值： 
                  - false。 
                  - true（默认）。 
            ProjectName ( String ): 否  监听器所属项目名称。 
    """,
    "describe_load_balancers": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            EniAddress ( String ): 否  ALB 实例的私网 IP 地址。 
            LoadBalancerIds ( Array of String ): 否   
            LoadBalancerName ( String ): 否  ALB 实例的名称。 
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值范围：1 ~ 100 ， 默认值为10。 
            TagFilters ( Array of String ): 否   
            VpcId ( String ): 否  ALB 实例所属的 VPC ID。 
            EipAddress ( String ): 否  ALB 实例的公网 IP 地址。 
            ProjectName ( String ): 否  实例所属项目名称。 
    """,
    "describe_server_group_attributes": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ServerGroupId ( String ): 是  后端服务器组 ID。 
    """,
    "describe_rules": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ListenerId ( String ): 是  监听器ID。 
    """,
    "describe_zones": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
    """,
    "describe_server_groups": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ServerGroupType ( String ): 否  后端服务器组的类型。取值： 
                  - instance（默认值）：服务器类型，该类型服务器组支持添加 ecs、eni 实例作为后端服务器。 
                  - ip：IP类型，该类型服务器组支持添加 IP 地址作为后端服务器。 
            ServerGroupNames ( Array of String ): 否   
            PageNumber ( Integer ): 否  列表的页码，默认值为1。 
            PageSize ( Integer ): 否  分页查询时每页的行数，取值1~100，默认为10。 
            VpcID ( String ): 否  后端服务器组所属 Vpc 的 ID。 
            ServerGroupIds ( Array of String ): 否   
            TagFilters ( Array of String ): 否   
            ProjectName ( String ): 否  后端服务器组所属项目名称。 
    """,
    "describe_server_group_backend_servers": r""" 
   Args: 
       params: A JSON structure
            参数 ( 类型 ): 是否必选  描述 
            ---- ( ---- ): ----  ---- 
            ServerGroupId ( String ): 是  后端服务器组 ID。 
            InstanceIds ( Array of String ): 否   
            Ips ( Array of String ): 否   
            PageSize ( String ): 否  分页查询时每页的行数，取值1~100，默认为10。 
            PageNumber ( String ): 否  列表的页码，默认值为1。 
    """,
}
