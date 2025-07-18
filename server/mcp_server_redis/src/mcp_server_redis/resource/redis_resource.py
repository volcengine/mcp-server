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
    DisassociateAllowListRequest, DisassociateAllowListResponse

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