import volcenginesdkcore
from .configs import get_redis_service_endpoint_by_region, redis_supported_regions
from volcenginesdkredis.api.redis_api import REDISApi
from volcenginesdkredis.models import DescribeRegionsRequest, DescribeRegionsResponse, \
    DescribeZonesRequest, DescribeZonesResponse,\
    DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse, \
    DescribeDBInstanceSpecsRequest, DescribeDBInstanceSpecsResponse, \
    DescribeSlowLogsRequest, DescribeSlowLogsResponse, \
    DescribeHotKeysRequest, DescribeHotKeysResponse, \
    DescribeBigKeysRequest, DescribeBigKeysResponse, \
    DescribeDBInstanceParamsRequest, DescribeDBInstanceParamsResponse, \
    DescribeParameterGroupsRequest, DescribeParameterGroupsResponse, \
    DescribeParameterGroupDetailRequest, DescribeParameterGroupDetailResponse, \
    DescribeAllowListsRequest, DescribeAllowListsResponse,\
    DescribeAllowListDetailRequest, DescribeAllowListDetailResponse, \
    DescribeBackupsRequest, DescribeBackupsResponse, \
    ListDBAccountRequest, ListDBAccountResponse, \
    CreateDBInstanceRequest, CreateDBInstanceResponse, \
    ModifyDBInstanceParamsRequest, ModifyDBInstanceParamsResponse, \
    CreateDBAccountRequest, CreateDBAccountResponse, \
    CreateAllowListRequest, CreateAllowListResponse, \
    AssociateAllowListRequest, AssociateAllowListResponse, \
    DescribeDBInstanceShardsRequest, DescribeDBInstanceShardsResponse, \
    DisassociateAllowListRequest, DisassociateAllowListResponse, \
    DescribeNodeIdsRequest, DescribeNodeIdsResponse, \
    ModifyDBInstanceNameRequest, ModifyDBInstanceNameResponse, \
    DescribeTagsByResourceRequest, DescribeTagsByResourceResponse, \
    DescribeBackupPlanRequest, DescribeBackupPlanResponse, \
    DescribePitrTimeWindowRequest, DescribePitrTimeWindowResponse, \
    DescribeBackupPointDownloadUrlsRequest, DescribeBackupPointDownloadUrlsResponse, \
    DescribeCrossRegionBackupPolicyRequest, DescribeCrossRegionBackupPolicyResponse, \
    DescribeCrossRegionBackupsRequest, DescribeCrossRegionBackupsResponse, \
    CreateParameterGroupRequest, CreateParameterGroupResponse, \
    CreateDBEndpointPublicAddressRequest, CreateDBEndpointPublicAddressResponse, \
    DescribeDBInstanceBandwidthPerShardRequest, DescribeDBInstanceBandwidthPerShardResponse, \
    DescribeDBInstanceAclCommandsRequest, DescribeDBInstanceAclCommandsResponse, \
    DescribeDBInstanceAclCategoriesRequest, DescribeDBInstanceAclCategoriesResponse, \
    DescribePlannedEventsRequest, DescribePlannedEventsResponse, \
    DescribeKeyScanJobsRequest, DescribeKeyScanJobsResponse

class RedisSDK:
    """初始化 Volcano Redis SDK Client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if region not in redis_supported_regions:
            raise Exception(f"Redis is not supported in region {region}.")
        if host is not None:
            configuration.host = host
        else:
            configuration.host = get_redis_service_endpoint_by_region(region)
        self.client = REDISApi(volcenginesdkcore.ApiClient(configuration))

    def describe_regions(self, args:dict) -> DescribeRegionsResponse:
        return self.client.describe_regions(DescribeRegionsRequest(**args))

    def describe_zones(self, args:dict) -> DescribeZonesResponse:
        return self.client.describe_zones(DescribeZonesRequest(**args))

    def describe_db_instances(self, args: dict) -> DescribeDBInstancesResponse:
        return self.client.describe_db_instances(DescribeDBInstancesRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def describe_db_instance_specs(self, args:dict) -> DescribeDBInstanceSpecsResponse:
        return self.client.describe_db_instance_specs(DescribeDBInstanceSpecsRequest(**args))

    def describe_slow_logs(self, args: dict) -> DescribeSlowLogsResponse:
        return self.client.describe_slow_logs(DescribeSlowLogsRequest(**args))

    def describe_hot_keys(self, args: dict) -> DescribeHotKeysResponse:
        return self.client.describe_hot_keys(DescribeHotKeysRequest(**args))

    def describe_big_keys(self, args: dict) -> DescribeBigKeysResponse:
        return self.client.describe_big_keys(DescribeBigKeysRequest(**args))

    def describe_backups(self, args: dict) -> DescribeBackupsResponse:
        return self.client.describe_backups(DescribeBackupsRequest(**args))

    def describe_db_instance_params(self, args: dict) -> DescribeDBInstanceParamsResponse:
        return self.client.describe_db_instance_params(DescribeDBInstanceParamsRequest(**args))

    def describe_parameter_groups(self, args: dict) -> DescribeParameterGroupsResponse:
        return self.client.describe_parameter_groups(DescribeParameterGroupsRequest(**args))

    def describe_parameter_group_detail(self, args: dict) -> DescribeParameterGroupDetailResponse:
        return self.client.describe_parameter_group_detail(DescribeParameterGroupDetailRequest(**args))

    def describe_allow_lists(self, args: dict) -> DescribeAllowListsResponse:
        return self.client.describe_allow_lists(DescribeAllowListsRequest(**args))

    def describe_allow_list_detail(self, args: dict) -> DescribeAllowListDetailResponse:
        return self.client.describe_allow_list_detail(DescribeAllowListDetailRequest(**args))

    def list_db_account(self, args:dict) -> ListDBAccountResponse:
        return self.client.list_db_account(ListDBAccountRequest(**args))

    def create_db_instance(self, args:dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))

    def modify_db_instance_params(self, args:dict) -> ModifyDBInstanceParamsResponse:
        return self.client.modify_db_instance_params(ModifyDBInstanceParamsRequest(**args))

    def create_db_account(self, args:dict) -> CreateDBAccountResponse:
        return self.client.create_db_account(CreateDBAccountRequest(**args))

    def create_allow_list(self, args:dict) -> CreateAllowListResponse:
        return self.client.create_allow_list(CreateAllowListRequest(**args))

    def associate_allow_list(self, args:dict) -> AssociateAllowListResponse:
        return self.client.associate_allow_list(AssociateAllowListRequest(**args))

    def disassociate_allow_list(self, args:dict) -> DisassociateAllowListResponse:
        return self.client.disassociate_allow_list(DisassociateAllowListRequest(**args))

    def describe_db_instance_shards(self, args: dict) -> DescribeDBInstanceShardsResponse:
        return self.client.describe_db_instance_shards(DescribeDBInstanceShardsRequest(**args))

    def describe_node_ids(self, args: dict) -> DescribeNodeIdsResponse:
        return self.client.describe_node_ids(DescribeNodeIdsRequest(**args))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def describe_tags_by_resource(self, args: dict) -> DescribeTagsByResourceResponse:
        return self.client.describe_tags_by_resource(DescribeTagsByResourceRequest(**args))

    def describe_backup_plan(self, args: dict) -> DescribeBackupPlanResponse:
        return self.client.describe_backup_plan(DescribeBackupPlanRequest(**args))

    def describe_pitr_time_window(self, args: dict) -> DescribePitrTimeWindowResponse:
        return self.client.describe_pitr_time_window(DescribePitrTimeWindowRequest(**args))

    def describe_backup_point_download_urls(self, args: dict) -> DescribeBackupPointDownloadUrlsResponse:
        return self.client.describe_backup_point_download_urls(DescribeBackupPointDownloadUrlsRequest(**args))

    def describe_cross_region_backup_policy(self, args: dict) -> DescribeCrossRegionBackupPolicyResponse:
        return self.client.describe_cross_region_backup_policy(DescribeCrossRegionBackupPolicyRequest(**args))

    def describe_cross_region_backups(self, args: dict) -> DescribeCrossRegionBackupsResponse:
        return self.client.describe_cross_region_backups(DescribeCrossRegionBackupsRequest(**args))

    def create_parameter_group(self, args: dict) -> CreateParameterGroupResponse:
        return self.client.create_parameter_group(CreateParameterGroupRequest(**args))

    def create_db_endpoint_public_address(self, args: dict) -> CreateDBEndpointPublicAddressResponse:
        return self.client.create_db_endpoint_public_address(CreateDBEndpointPublicAddressRequest(**args))

    def describe_db_instance_bandwidth_per_shard(self, args: dict) -> DescribeDBInstanceBandwidthPerShardResponse:
        return self.client.describe_db_instance_bandwidth_per_shard(DescribeDBInstanceBandwidthPerShardRequest(**args))

    def describe_db_instance_acl_commands(self, args: dict) -> DescribeDBInstanceAclCommandsResponse:
        return self.client.describe_db_instance_acl_commands(DescribeDBInstanceAclCommandsRequest(**args))

    def describe_db_instance_acl_categories(self, args: dict) -> DescribeDBInstanceAclCategoriesResponse:
        return self.client.describe_db_instance_acl_categories(DescribeDBInstanceAclCategoriesRequest(**args))

    def describe_planned_events(self, args: dict) -> DescribePlannedEventsResponse:
        return self.client.describe_planned_events(DescribePlannedEventsRequest(**args))

    def describe_key_scan_jobs(self, args: dict) -> DescribeKeyScanJobsResponse:
        return self.client.describe_key_scan_jobs(DescribeKeyScanJobsRequest(**args))