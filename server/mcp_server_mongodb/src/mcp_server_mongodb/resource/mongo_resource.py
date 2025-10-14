import volcenginesdkcore
from volcenginesdkmongodb.api.mongodb_api import MONGODBApi
from volcenginesdkmongodb.models import DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse, DescribeBackupsRequest, DescribeBackupsResponse, \
    DescribeDBInstanceParametersRequest, DescribeDBInstanceParametersResponse, DescribeSlowLogsRequest, DescribeSlowLogsResponse, \
    CreateDBInstanceRequest, CreateDBInstanceResponse, DescribeAvailabilityZonesRequest, DescribeAvailabilityZonesResponse, \
    DescribeAllowListsRequest, DescribeAllowListsResponse, DescribeNodeSpecsRequest, DescribeNodeSpecsResponse, \
    DescribeRegionsRequest, DescribeRegionsResponse, ModifyDBInstanceNameRequest, ModifyDBInstanceNameResponse, \
    AddTagsToResourceRequest, AddTagsToResourceResponse, RemoveTagsFromResourceRequest, RemoveTagsFromResourceResponse, \
    ResetDBAccountRequest, ResetDBAccountResponse, DescribeDBAccountsRequest, DescribeDBAccountsResponse, \
    CreateDBEndpointRequest, CreateDBEndpointResponse, DescribeDBEndpointRequest, DescribeDBEndpointResponse, \
    CreateBackupRequest, CreateBackupResponse, DescribeDBInstanceBackupPolicyRequest, DescribeDBInstanceBackupPolicyResponse, \
    ModifyDBInstanceBackupURLRequest, ModifyDBInstanceBackupURLResponse, DescribeDBInstanceBackupURLRequest, DescribeDBInstanceBackupURLResponse, \
    DescribeRecoverableTimeRequest, DescribeRecoverableTimeResponse, RestoreToNewInstanceRequest, RestoreToNewInstanceResponse, \
    CreateAllowListRequest, CreateAllowListResponse, DescribeAllowListDetailRequest, DescribeAllowListDetailResponse, \
    AssociateAllowListRequest, AssociateAllowListResponse, DescribeDBInstanceSSLRequest, DescribeDBInstanceSSLResponse,\
    DescribeDBInstanceParametersLogRequest, DescribeDBInstanceParametersLogResponse, DescribeNormalLogsRequest, DescribeNormalLogsResponse


class MongoDBSDK:
    """初始化 volc Mongo client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = MONGODBApi(volcenginesdkcore.ApiClient(configuration))

    def describe_db_instances(self, args: dict) -> DescribeDBInstancesResponse:
        return self.client.describe_db_instances(DescribeDBInstancesRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def describe_backups_request(self, args: dict) -> DescribeBackupsResponse:
        return self.client.describe_backups(DescribeBackupsRequest(**args))

    def describe_db_instance_parameters(self, args: dict) -> DescribeDBInstanceParametersResponse:
        return self.client.describe_db_instance_parameters(DescribeDBInstanceParametersRequest(**args))

    def describe_db_slow_logs(self, args: dict) -> DescribeSlowLogsResponse:
        return self.client.describe_slow_logs(DescribeSlowLogsRequest(**args))

    def describe_allow_lists(self, args: dict) -> DescribeAllowListsResponse:
        return self.client.describe_allow_lists(DescribeAllowListsRequest(**args))

    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))

    def describe_azs(self, args: dict) -> DescribeAvailabilityZonesResponse:
        return self.client.describe_availability_zones(DescribeAvailabilityZonesRequest(**args))

    def describe_region(self, args: dict) -> DescribeRegionsResponse:
        return self.client.describe_regions(DescribeRegionsRequest(**args))

    def describe_node_spec(self, args: dict) -> DescribeNodeSpecsResponse:
        return self.client.describe_node_specs(DescribeNodeSpecsRequest(**args))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def add_tags_to_resource(self, args: dict) -> AddTagsToResourceResponse:
        return self.client.add_tags_to_resource(AddTagsToResourceRequest(**args))

    def remove_tags_from_resource(self, args: dict) -> RemoveTagsFromResourceResponse:
        return self.client.remove_tags_from_resource(RemoveTagsFromResourceRequest(**args))

    def reset_db_account(self, args: dict) -> ResetDBAccountResponse:
        return self.client.reset_db_account(ResetDBAccountRequest(**args))

    def describe_db_accounts(self, args: dict) -> DescribeDBAccountsResponse:
        return self.client.describe_db_accounts(DescribeDBAccountsRequest(**args))

    def create_db_endpoint(self, args: dict) -> CreateDBEndpointResponse:
        return self.client.create_db_endpoint(CreateDBEndpointRequest(**args))

    def describe_db_endpoint(self, args: dict) -> DescribeDBEndpointResponse:
        return self.client.describe_db_endpoint(DescribeDBEndpointRequest(**args))

    def create_backup(self, args: dict) -> CreateBackupResponse:
        return self.client.create_backup(CreateBackupRequest(**args))

    def describe_db_instance_backup_policy(self, args: dict) -> DescribeDBInstanceBackupPolicyResponse:
        return self.client.describe_db_instance_backup_policy(DescribeDBInstanceBackupPolicyRequest(**args))

    def modify_db_instance_backup_url(self, args: dict) -> ModifyDBInstanceBackupURLResponse:
        return self.client.modify_db_instance_backup_url(ModifyDBInstanceBackupURLRequest(**args))

    def describe_db_instance_backup_url(self, args: dict) -> DescribeDBInstanceBackupURLResponse:
        return self.client.describe_db_instance_backup_url(DescribeDBInstanceBackupURLRequest(**args))

    def describe_recoverable_time(self, args: dict) -> DescribeRecoverableTimeResponse:
        return self.client.describe_recoverable_time(DescribeRecoverableTimeRequest(**args))

    def restore_to_new_instance(self, args: dict) -> RestoreToNewInstanceResponse:
        return self.client.restore_to_new_instance(RestoreToNewInstanceRequest(**args))

    def create_allow_list(self, args: dict) -> CreateAllowListResponse:
        return self.client.create_allow_list(CreateAllowListRequest(**args))

    def describe_allow_list_detail(self, args: dict) -> DescribeAllowListDetailResponse:
        return self.client.describe_allow_list_detail(DescribeAllowListDetailRequest(**args))

    def associate_allow_list(self, args: dict) -> AssociateAllowListResponse:
        return self.client.associate_allow_list(AssociateAllowListRequest(**args))

    def describe_db_instance_ssl(self, args: dict) -> DescribeDBInstanceSSLResponse:
        return self.client.describe_db_instance_ssl(DescribeDBInstanceSSLRequest(**args))

    def describe_db_instance_parameters_log(self, args: dict) -> DescribeDBInstanceParametersLogResponse:
        return self.client.describe_db_instance_parameters_log(DescribeDBInstanceParametersLogRequest(**args))

    def describe_normal_logs(self, args: dict) -> DescribeNormalLogsResponse:
        return self.client.describe_normal_logs(DescribeNormalLogsRequest(**args))

