func_available_params_map = {
    "describe_regions": r"""Query available regions for Redis instances
       Args:
           region_id (str, optional): The region ID. If not specified, returns information about all available regions
                                    for the current account.""",
    "describe_zones": r"""Query the list of available zone resources for Redis in the specified region
       Args:
           region_id (str): The region ID. You can call describe_regions to query all available region information for Redis instances.""",
    "describe_vpcs": r"""Query VPC information
       Args:
           vpc_name (str, optional): The VPC name.
           project_name (str, optional): The project name that VPC belongs to.
           is_default (bool, optional): Whether the VPC is default VPC.
                                      True: System auto-created VPC for ECS instances
                                      False: User manually created VPC
           vpc_owner_id (int, optional): The ID of main account that owns the VPC.
           page_number (int, optional): The page number, starting from 1. Default: 1.
                                      Note: This parameter will be deprecated,
                                      use next_token and max_results instead.
           page_size (int, optional): The number of records per page.
                                    Range: 1-100, Default: 20.
                                    Note: This parameter will be deprecated,
                                    use next_token and max_results instead.
           next_token (str, optional): The pagination token.
                                     Leave empty to query from beginning.
                                     Use token from previous response to continue query.
           max_results (int, optional): The number of records to return.
                                      Range: 1-100, Default: 10.""",
    "describe_subnets": r"""Query subnet information
       Args:
           zone_id (str, optional): The availability zone ID.
           vpc_id (str, optional): The VPC ID.
                                 You can call describe_vpcs to query VPC information.
           subnet_name (str, optional): The subnet name.
           subnet_owner_id (str, optional): The ID of account that owns the subnet.
           route_table_id (str, optional): The route table ID.
           project_name (str, optional): The project name that subnet belongs to.
                                       Default: 'default'
           is_default (bool, optional): Whether the subnet is default subnet.
                                      True: System auto-created subnet
                                      False: User manually created subnet
           page_number (int, optional): The page number, starting from 1. Default: 1.
                                      Note: This parameter will be deprecated,
                                      use next_token and max_results instead.
           page_size (int, optional): The number of records per page.
                                    Range: 1-100, Default: 20.
                                    Note: This parameter will be deprecated,
                                    use next_token and max_results instead.
           next_token (str, optional): The pagination token.
                                     Leave empty to query from beginning.
                                     Use token from previous response to continue query.
           max_results (int, optional): The number of records to return.
                                      Range: 1-100, Default: 10.""",
    "describe_db_instances": r"""Query basic information of Redis instances
       Args:
           region_id (str, optional): The region ID.
                                    If not specified, uses the region from signature.
                                    Call describe_regions to query available regions.
           page_number (int, optional): The page number, starting from 1. Default: 1.
           page_size (int, optional): The number of records per page, range: 1-1000. Default: 10.
           zone_id (str, optional): The availability zone ID (supports fuzzy search).
                                  Call DescribeZones to query available zones.
           instance_id (str, optional): The instance ID (exact match).
           instance_name (str, optional): The instance name (supports fuzzy search).
           sharded_cluster (int, optional): Whether sharding is enabled.
                                          Values: 0 (disabled), 1 (enabled)
           status (str, optional): The instance status.
           engine_version (str, optional): The database version.
                                         Values: '5.0', '6.0', '7.0'
           vpc_id (str, optional): The VPC ID (supports fuzzy search).
                                 Call describe_vpcs to query VPC information.
           charge_type (str, optional): The billing method.
                                      Values: 'PostPaid' (pay-as-you-go),
                                             'PrePaid' (subscription)
           tag_filters (list[dict], optional): List of tag filters. Each dict contains:
                                             - 'Key' (str): Tag key (required)
                                             - 'Value' (str, optional): Tag value
                                             Max 10 tag pairs.
                                             Empty value means no restriction on tag value.
           project_name (str, optional): The project name.
           service_type (str, optional): The service type.
                                       Values: 'Basic' (default, community edition),
                                              'Enterprise' (enterprise edition)
           data_layout (str, optional): The data storage format.
                                      Only meaningful for enterprise edition.
                                      Fixed as 'RAM' for community edition.""",
    "describe_db_instance_detail": r"""Query the details of a Redis instance
       Args:
           instance_id (str): The instance ID""",
    "describe_db_instance_specs": r"""Query the list of instance specifications supported by Redis
       Args:
           arch_type (str, optional): The architecture type of Redis instance.
                                    Values: 'Cluster' (enabled sharding), 'Standard' (disabled sharding)
           instance_class (str, optional): The instance class type.
                                         Values: 'PrimarySecondary' (master-slave), 'Standalone' (single node)""",
    "describe_slow_logs": r"""Query slow log details of the target Redis instance within specified time period
       Args:
           instance_id (str): The instance ID. You can call describe_db_instances to query basic information of all Redis instances.
           page_size (int): The number of records per page, range: 1-1000.
           node_ids (list[str], optional): The node IDs to query slow logs.
                                         If not specified, queries slow logs of all nodes.
                                         Multiple node IDs should be separated by commas.
                                         Total length should not exceed 1024 bytes, recommended no more than 8 nodes.
           slow_log_type (str, optional): The type of slow log.
                                        Values: 'Server' (Server node slow log), 'Proxy' (Proxy node slow log).
                                        If not specified, returns slow logs of all node types.
           query_start_time (str, optional): The start time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                           If not specified, defaults to 3 days before current time.
           query_end_time (str, optional): The end time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                         If not specified, defaults to current time.
                                         Must be later than query_start_time.
           db_name (str, optional): The database where slow logs are located.
                                  For Proxy node: integers between 0-256
                                  For Server node: only '-' is supported
                                  If not specified, returns slow logs from all databases.
           context (str, optional): The context for pagination.
                                  Used when loading more slow log records based on ListOver value in response.""",
    "describe_hot_keys": r"""Query hot key details of the target Redis instance within specified time period
       Args:
           instance_id (str): The instance ID.
                             You can call DescribeDBInstances to query basic information of all Redis instances.
           page_size (int): The number of records per page, range: 1-1000.
           query_start_time (str, optional): The start time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                           If not specified, defaults to 1 hour before current time.
                                           Can query up to 15 days of historical data.
           query_end_time (str, optional): The end time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                         If not specified, defaults to current time.
                                         Must be later than query_start_time.
                                         Time interval cannot exceed 15 days.
           key_type (str, optional): The data type to filter hot keys.
                                   Values: 'string', 'list', 'set', 'zset', 'hash'
                                   If not specified, no filtering by data type.
           shard_ids (list[str], optional): The list of shard IDs to filter results.
                                          Maximum 40 shard IDs, separated by commas.
                                          If not specified, no filtering by shard ID.
                                          You can call DescribeDBInstanceShards to query shard details.""",
    "describe_big_keys": r"""Query big key details of the target Redis instance within specified time period
       Args:
           instance_id (str): The instance ID.
                             You can call DescribeDBInstances to query basic information of all Redis instances.
           page_size (int): The number of records per page, range: 1-100.
           query_start_time (str, optional): The start time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                           If not specified, defaults to 24 hours before current time.
                                           Can query up to 15 days of historical data.
                                           Time interval cannot exceed 24 hours.
           query_end_time (str, optional): The end time of the query in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                         If not specified, defaults to current time.
                                         Must be later than query_start_time.
                                         Time interval cannot exceed 24 hours.
           key_type (str, optional): The data type to filter big keys.
                                   Values: 'string', 'list', 'set', 'zset', 'hash'
                                   If not specified, no filtering by data type.
           order_by (str, optional): The sorting condition for query results.
                                   Values: 'ValueSize' (sort by memory usage, default),
                                          'ValueLen' (sort by number of elements)""",
    "describe_backups": r"""Query the backup set list of Redis instances
       Args:
           scope (str, optional): The backup query scope.
                                Values: 'OneInstance' (default, query single instance),
                                       'AccountInstances' (query current account)
           instance_id (str, optional): The instance ID.
                                      Required when scope is 'OneInstance'.
                                      You can call DescribeDBInstances to query instance information.
           start_time (str, optional): The start time in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                     If specified, end_time is required.
           end_time (str, optional): The end time in format yyyy-MM-ddTHH:mm:ssZ (UTC).
                                   Required if start_time is specified.
                                   Must be later than start_time.
           backup_strategy_list (list[str], optional): The list of backup strategies.
                                                     Values: 'ManualBackup', 'AutomatedBackup'
                                                     Multiple strategies separated by commas.
           backup_point_name (str, optional): The backup name (supports fuzzy search).
                                            Only effective when scope is 'AccountInstances'.
           project_name (str, optional): The project name of the backup.
                                       Only effective when scope is 'AccountInstances'.
           page_size (int, optional): The number of records per page, range: 1-1000.
                                    Required if page_number is specified.
           page_number (int, optional): The page number, starting from 1.
                                      Required if page_size is specified.
           backup_point_id (str, optional): The backup ID (supports fuzzy search).
                                          Only effective when scope is 'AccountInstances'.""",
    "describe_db_instance_params": r"""Query the list of parameters supported by the target Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information of all Redis instances.
           page_number (int): The page number of parameter list, starting from 1.
                             Must not exceed the maximum value of Integer type.
           page_size (int): The number of records per page, range: 1-1000.""",
    "describe_parameter_groups": r"""Query the basic information of parameter templates under the current account and region
       Args:
           page_number (int): The page number of parameter template list, starting from 1.
                             Must not exceed the maximum value of Integer type.
           page_size (int): The number of records per page, range: 1-100.
           engine_version (str, optional): The Redis database version for the parameter template.
                                         Values: '7.0' (Redis 7.0), '6.0' (Redis 6.0), '5.0' (Redis 5.0)
           source (str, optional): The source of parameter template creation.
                                 Values: 'User' (user-created custom template),
                                        'System' (system-created template)""",
    "describe_parameter_group_detail": r"""Query detailed information of the target parameter template
       Args:
           parameter_group_id (str): The parameter template ID.
                                   You can call describe_parameter_groups to query basic information
                                   of all parameter templates under the current account and region.""",
    "describe_allow_lists": r"""Query the IP whitelist list in the specified region
       Args:
           region_id (str): The region ID.
                           You can call describe_regions to query all available region information.
           instance_id (str, optional): The instance ID.
                                      You can call describe_db_instances to query instance information.
           query_default (bool, optional): Whether to query only default whitelists.
                                         Values: True (query only default whitelists),
                                                False (query only normal whitelists)
                                         If not specified, returns all types of whitelists.
           ip_address (list[str], optional): Filter whitelists by IP addresses.
                                           Matches exact IP addresses and IP segments containing these addresses.
                                           Maximum 50 IP addresses, separated by commas.
           ip_segment (list[str], optional): Filter whitelists by IP segments.
                                           Matches exact IP segments.
                                           Maximum 50 IP segments, separated by commas.
           project_name (str, optional): The project name of the whitelist.""",
    "describe_allow_list_detail": r"""Query detailed information of the target whitelist
       Args:
           allow_list_id (str): The whitelist ID.
                               You can call describe_allow_lists to query all whitelist information
                               under the current account in the specified region.""",
    "list_db_account": r"""Query account information in Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information
                             of all Redis instances.
           account_name (str, optional): The account name.
                                       If not specified, no filtering by account name.""",
    "create_db_instance": r"""Create a Redis instance
       Args:
           region_id (str): The region ID.
                           You can call DescribeRegions to query available regions.
           engine_version (str): Redis version.
                               Values: '5.0', '6.0', '7.0'
           sharded_cluster (int): Whether to enable sharding cluster.
                                Values:
                                - 0: disabled
                                - 1: enabled
                                See product architecture documentation for details.
           node_number (int): Number of nodes per shard.
                            Range: 1-6
                            Note:
                            - Default quota: 4 nodes of 256MiB per region
                            - Node=1: single node instance
                            - Node>1: master-replica instance
                            See feature differences documentation.
           shard_capacity (int): Memory capacity per shard in MiB.
                               Without sharding (sharded_cluster=0):
                               [256,512,1024,2048,4096,8192,16384,32768,24576,65536]
                               With sharding (sharded_cluster=1):
                               [1024,2048,4096,8192,16384]
                               Note: 256MiB not available for single node instances.
           multi_az (str): Availability zone deployment type.
                          Values:
                          - 'disabled': single zone
                          - 'enabled': multi zone
                          Note: Must be 'disabled' for single node instances.
           configure_nodes (list[dict]): Node zone configuration list.
                           Format depends on node_number and multi_az:
                           1. For single node (node_number=1):
                              multi_az must be 'disabled'
                              Example:
                              {
                                  "ConfigureNodes": [
                                      {
                                          "AZ": "cn-beijing-a"
                                      }
                                  ]
                              }

                           2. For master-replica (node_number>=2):
                              With multi_az='enabled':
                              - Must specify different zones for nodes
                              - Number of configure_nodes must match node_number
                              Example for 3 nodes across zones A and C:
                              {
                                  "ConfigureNodes": [
                                      {
                                          "AZ": "cn-beijing-a"
                                      },
                                      {
                                          "AZ": "cn-beijing-c"
                                      },
                                      {
                                          "AZ": "cn-beijing-c"
                                      }
                                  ]
                              }

                              With multi_az='disabled':
                              - All nodes must be in same zone
                              - Number of configure_nodes must match node_number
                              Example for 3 nodes in same zone:
                              {
                                  "ConfigureNodes": [
                                      {
                                          "AZ": "cn-beijing-a"
                                      },
                                      {
                                          "AZ": "cn-beijing-a"
                                      },
                                      {
                                          "AZ": "cn-beijing-a"
                                      }
                                  ]
                              }
                              
                           Note:
                           - You can call describe_zones to query available zones
                           - AZ format must match the zone ID format, e.g. "cn-beijing-a"

           vpc_id (str): The VPC ID.
                        Recommend using same VPC as target ECS instances.
                        You can call describe_vpcs to query VPCs.
           subnet_id (str): The subnet ID.
                          Must be in same zone as instance.
                          You can call describe_subnets to query subnets.
           shard_number (int, optional): Number of shards.
                                       Range: 2-256
                                       Required when sharded_cluster=1
           instance_name (str, optional): Instance name.
                                        Rules:
                                        - Cannot start with number or hyphen
                                        - Can contain Chinese chars, letters, numbers, underscore, hyphen
                                        - Length: 1-128 chars
                                        Default: instance ID
           password (str, optional): Password for default account.
                                   Rules:
                                   - Length: 8-32 chars
                                   - Must contain 2 types from: upper/lower/digits/special
                                   - Special chars: ()`~!@#$%^&*-+=_|{}[];<>,.?
                                   Default: random password
           port (int, optional): Private network port.
                               Range: 1024-65535
                               Default: 6379
           project_name (str, optional): Project name.
                                       Default: 'default'
           allow_list_ids (list[str], optional): List of whitelist IDs.
                                               Max 100 whitelists per instance.
                                               Max 1000 IPs/CIDRs total.
           tags (list[dict], optional): List of tags.
                                      Each dict:
                                      - 'Key' (str, required): tag key
                                      - 'Value' (str, optional): tag value
                                      Max 20 tags per request.
                                      Max 50 tags per instance.
           charge_type (str, optional): Billing method.
                                      Values:
                                      - 'PostPaid': pay-as-you-go (default)
                                      - 'PrePaid': subscription
           purchase_months (int, optional): Subscription period in months.
                                         Monthly: [1-9]
                                         Yearly: [12,24,36]
                                         Required for PrePaid
           auto_renew (bool, optional): Enable auto-renewal.
                                      Default: False
                                      Only valid for PrePaid
           deletion_protection (str, optional): Instance deletion protection.
                                              Values:
                                              - 'disabled': off (default)
                                              - 'enabled': on
           no_auth_mode (str, optional): Password-free access.
                                       Values:
                                       - 'close': disabled (default)
                                       - 'open': enabled
                                       Case insensitive
           parameter_group_id (str, optional): Parameter template ID.
                                             Default: system template for engine version
           client_token (str, optional): Idempotency token.
                                       Max 127 ASCII chars.
                                       Must be unique between requests.""",
    "modify_db_instance_params": r"""Modify parameter configurations of the target Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information
                             of all Redis instances.
           param_values (list[dict]): List of parameter configurations to modify.
                                    Each dict contains:
                                    - 'Name' (str): Parameter name
                                    - 'Value' (str): Parameter value
                                    You can call describe_db_instance_params to query supported
                                    parameters and their valid values.
                                    Example for modify slowlog-max-len parameter:
                                    "param_values": [
                                        {
                                            "name": "slowlog-max-len", 
                                            "value": "256"
                                        }
                                    ]
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.""",
    "create_db_account": r"""Create an account for the target Redis instance
       Args:
           instance_id (str): The instance ID.
                             You can call describe_db_instances to query basic information
                             of all Redis instances.
           account_name (str): The account name.
                              Requirements:
                              - Start with lowercase letter
                              - End with lowercase letter or number
                              - Length: 2-16 characters
                              - Can contain lowercase letters, numbers, underscore(_)
           role_name (str): The role name. Available roles:
                           - 'Administrator': Allow all commands on all keys
                           - 'ReadWrite': Allow all non-admin commands on all keys
                           - 'ReadOnly': Allow all read commands on all keys
                           - 'NotDangerous': Allow all non-dangerous commands on all keys
                           You can call DescribeDBInstanceAclCategories and
                           DescribeDBInstanceAclCommands to query supported commands.
           password (str): The account password.
                          Requirements:
                          - Length: 8-32 characters
                          - Must contain at least 2 types from: uppercase letters,
                            lowercase letters, numbers, special characters
                          - Supported special characters: ()`~!@#$%^&*-+=_{}[];,.?
           description (str, optional): Account description, max 256 characters.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.""",
    "create_allow_list": r"""Create a new IP whitelist
       Args:
           allow_list_name (str): The whitelist name.
                                 Requirements:
                                 - Cannot start with number or dash(-)
                                 - Can contain Chinese characters, letters, numbers, underscore(_), dash(-)
                                 - Length: 1-32 characters
           allow_list (str, optional): IP addresses or CIDR blocks, separated by commas.
                                     Special values:
                                     - '0.0.0.0/0': allow all addresses
                                     - '127.0.0.1': deny all addresses
                                     - CIDR format like '192.168.1.0/24': allow IP range
                                     - Single IP like '192.168.1.1': allow specific IP
                                     Cannot be empty if security_group_bind_infos is not provided.
           allow_list_desc (str, optional): Whitelist description, max 200 characters.
           allow_list_category (str, optional): Whitelist type.
                                              Values: 'Ordinary' (default), 'Default'
                                              Only one default whitelist allowed per region.
           security_group_bind_infos (list[dict], optional): List of ECS security groups to associate.
                                                           Each dict contains:
                                                           - 'BindMode' (str): 'IngressDirectionIp' or 'AssociateEcsIp'
                                                           - 'SecurityGroupId' (str): Security group ID
                                                           Cannot be empty if allow_list is not provided.
                                                           Max 10 security groups per whitelist.
           project_name (str, optional): Project name for the whitelist.
                                       If not specified, joins the 'default' project.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.""",
    "associate_allow_list": r"""Bind Redis instances to specified IP whitelists
       Args:
           instance_ids (list[str]): List of instance IDs to bind.
                                    You can call describe_db_instances to query instance information.
                                    Multiple IDs separated by commas.
                                    Note: Cannot bind multiple instances and multiple whitelists simultaneously.
           allow_list_ids (list[str]): List of whitelist IDs to bind.
                                      You can call describe_allow_lists to query whitelist information.
                                      Multiple IDs separated by commas.
                                      Note: Cannot bind multiple instances and multiple whitelists simultaneously.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.

       Note:
           You can only:
           - Bind multiple instances to one whitelist, OR
           - Bind one instance to multiple whitelists
           You cannot bind multiple instances to multiple whitelists in a single request.""",
    "disassociate_allow_list": r"""Unbind Redis instances from specified IP whitelists
       Args:
           instance_ids (list[str]): List of instance IDs to unbind.
                                    You can call describe_db_instances to query instance information.
                                    Multiple IDs separated by commas.
                                    Note: Cannot unbind multiple instances and multiple whitelists simultaneously.
           allow_list_ids (list[str]): List of whitelist IDs to unbind.
                                      You can call describe_allow_lists to query whitelist information.
                                      Multiple IDs separated by commas.
                                      Note: Cannot unbind multiple instances and multiple whitelists simultaneously.
           client_token (str, optional): Idempotency token, max 127 ASCII chars.
                                       Must be unique between different requests.

       Note:
           You can only:
           - Unbind multiple instances from one whitelist, OR
           - Unbind one instance from multiple whitelists
           You cannot unbind multiple instances from multiple whitelists in a single request."""
}