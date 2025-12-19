import volcenginesdkcore
from volcenginesdkrdspostgresql.api.rds_postgresql_api import RDSPOSTGRESQLApi
from volcenginesdkrdspostgresql.models import DescribeSlotsRequest, DescribeSlotsResponse, \
    DescribeAllowListDetailRequest, DescribeAllowListDetailResponse, \
    DescribeAllowListsRequest, DescribeAllowListsResponse, \
    RevokeDBAccountPrivilegeRequest, RevokeDBAccountPrivilegeResponse, \
    ModifyDBEndpointNameRequest, ModifyDBEndpointNameResponse, \
    DescribeDetachedBackupsRequest, DescribeDetachedBackupsResponse, \
    DescribeBackupPolicyRequest, DescribeBackupPolicyResponse, \
    DescribeBackupsRequest, DescribeBackupsResponse, \
    ModifyDBInstanceNameRequest, ModifyDBInstanceNameResponse, \
    DescribeDBInstanceParametersRequest, DescribeDBInstanceParametersResponse, \
    ModifyDBInstanceParametersRequest, ModifyDBInstanceParametersResponse, \
    ModifyDBInstanceChargeTypeRequest, ModifyDBInstanceChargeTypeResponse, \
    DescribeDBInstancePriceDifferenceRequest, DescribeDBInstancePriceDifferenceResponse, \
    ModifyDBEndpointDNSRequest, ModifyDBEndpointDNSResponse, \
    RemoveTagsFromResourceRequest, RemoveTagsFromResourceResponse, \
    AddTagsToResourceRequest, AddTagsToResourceResponse, \
    DescribeDBInstancePriceDetailRequest, DescribeDBInstancePriceDetailResponse, \
    CreateDBEndpointRequest, CreateDBEndpointResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse, \
    ModifyDBInstanceSpecRequest, ModifyDBInstanceSpecResponse, \
    RestoreToNewInstanceRequest, RestoreToNewInstanceResponse, \
    CreateDBInstanceRequest, CreateDBInstanceResponse, \
    DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
    DescribeDBInstanceSpecsRequest, DescribeDBInstanceSpecsResponse, \
    DescribeRecoverableTimeRequest, DescribeRecoverableTimeResponse, \
    ModifyDBEndpointAddressRequest, ModifyDBEndpointAddressResponse, \
    DescribeFailoverLogsRequest, DescribeFailoverLogsResponse, \
    ResetDBAccountRequest, ResetDBAccountResponse, \
    ModifyDBAccountPrivilegeRequest, ModifyDBAccountPrivilegeResponse, \
    CreateSchemaRequest, CreateSchemaResponse, \
    ModifySchemaOwnerRequest, ModifySchemaOwnerResponse, \
    DescribeSchemasRequest, DescribeSchemasResponse, \
    ModifyDatabaseOwnerRequest, ModifyDatabaseOwnerResponse, \
    CreateDatabaseRequest, CreateDatabaseResponse, \
    DescribeDatabasesRequest, DescribeDatabasesResponse, \
    CreateDBAccountRequest, CreateDBAccountResponse, \
    DescribeDBAccountsRequest, DescribeDBAccountsResponse, \
    DescribeWALLogBackupsRequest, DescribeWALLogBackupsResponse, \
    DescribeDBInstanceSSLRequest, DescribeDBInstanceSSLResponse, \
    DescribeTasksRequest, DescribeTasksResponse, \
    DescribeDBEngineVersionParametersRequest, DescribeDBEngineVersionParametersResponse, \
    DescribePlannedEventsRequest, DescribePlannedEventsResponse, \
    GetBackupDownloadLinkRequest, GetBackupDownloadLinkResponse, \
CloneDatabaseRequest, CloneDatabaseResponse

class RDSPOSTGRESQLSDK:
    """初始化 volc rds_postgresql 客户端"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, token: str = None,
                 host: str = None, header_name: str = None, header_value: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        configuration.session_token = token
        if host is not None:
            configuration.host = host
        self.client = RDSPOSTGRESQLApi(volcenginesdkcore.ApiClient(configuration, header_name, header_value))

    def describe_slots(self, args: dict) -> DescribeSlotsResponse:
        return self.client.describe_slots(DescribeSlotsRequest(**args))

    def describe_allow_list_detail(self, args: dict) -> DescribeAllowListDetailResponse:
        return self.client.describe_allow_list_detail(DescribeAllowListDetailRequest(**args))

    def describe_allow_lists(self, args: dict) -> DescribeAllowListsResponse:
        return self.client.describe_allow_lists(DescribeAllowListsRequest(**args))

    def revoke_db_account_privilege(self, args: dict) -> RevokeDBAccountPrivilegeResponse:
        return self.client.revoke_db_account_privilege(RevokeDBAccountPrivilegeRequest(**args))

    def modify_db_endpoint_name(self, args: dict) -> ModifyDBEndpointNameResponse:
        return self.client.modify_db_endpoint_name(ModifyDBEndpointNameRequest(**args))

    def describe_detached_backups(self, args: dict) -> DescribeDetachedBackupsResponse:
        return self.client.describe_detached_backups(DescribeDetachedBackupsRequest(**args))

    def describe_backup_policy(self, args: dict) -> DescribeBackupPolicyResponse:
        return self.client.describe_backup_policy(DescribeBackupPolicyRequest(**args))

    def describe_backups(self, args: dict) -> DescribeBackupsResponse:
        return self.client.describe_backups(DescribeBackupsRequest(**args))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def describe_db_instance_parameters(self, args: dict) -> DescribeDBInstanceParametersResponse:
        return self.client.describe_db_instance_parameters(DescribeDBInstanceParametersRequest(**args))

    def modify_db_instance_parameters(self, args: dict) -> ModifyDBInstanceParametersResponse:
        return self.client.modify_db_instance_parameters(ModifyDBInstanceParametersRequest(**args))

    def modify_db_instance_charge_type(self, args: dict) -> ModifyDBInstanceChargeTypeResponse:
        return self.client.modify_db_instance_charge_type(ModifyDBInstanceChargeTypeRequest(**args))

    def describe_db_instance_price_difference(self, args: dict) -> DescribeDBInstancePriceDifferenceResponse:
        return self.client.describe_db_instance_price_difference(DescribeDBInstancePriceDifferenceRequest(**args))

    def modify_db_endpoint_dns(self, args: dict) -> ModifyDBEndpointDNSResponse:
        return self.client.modify_db_endpoint_dns(ModifyDBEndpointDNSRequest(**args))

    def remove_tags_from_resource(self, args: dict) -> RemoveTagsFromResourceResponse:
        return self.client.remove_tags_from_resource(RemoveTagsFromResourceRequest(**args))

    def add_tags_to_resource(self, args: dict) -> AddTagsToResourceResponse:
        return self.client.add_tags_to_resource(AddTagsToResourceRequest(**args))

    def describe_db_instance_price_detail(self, args: dict) -> DescribeDBInstancePriceDetailResponse:
        return self.client.describe_db_instance_price_detail(DescribeDBInstancePriceDetailRequest(**args))

    def create_db_endpoint(self, args: dict) -> CreateDBEndpointResponse:
        return self.client.create_db_endpoint(CreateDBEndpointRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def modify_db_instance_spec(self, args: dict) -> ModifyDBInstanceSpecResponse:
        return self.client.modify_db_instance_spec(ModifyDBInstanceSpecRequest(**args))

    def restore_to_new_instance(self, args: dict) -> RestoreToNewInstanceResponse:
        return self.client.restore_to_new_instance(RestoreToNewInstanceRequest(**args))

    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))

    def describe_db_instances(self, args: dict) -> DescribeDBInstancesResponse:
        return self.client.describe_db_instances(DescribeDBInstancesRequest(**args))

    def describe_db_instance_specs(self, args: dict) -> DescribeDBInstanceSpecsResponse:
        return self.client.describe_db_instance_specs(DescribeDBInstanceSpecsRequest(**args))

    def describe_recoverable_time(self, args: dict) -> DescribeRecoverableTimeResponse:
        return self.client.describe_recoverable_time(DescribeRecoverableTimeRequest(**args))

    def modify_db_endpoint_address(self, args: dict) -> ModifyDBEndpointAddressResponse:
        return self.client.modify_db_endpoint_address(ModifyDBEndpointAddressRequest(**args))

    def describe_failover_logs(self, args: dict) -> DescribeFailoverLogsResponse:
        return self.client.describe_failover_logs(DescribeFailoverLogsRequest(**args))

    def reset_db_account(self, args: dict) -> ResetDBAccountResponse:
        return self.client.reset_db_account(ResetDBAccountRequest(**args))

    def modify_db_account_privilege(self, args: dict) -> ModifyDBAccountPrivilegeResponse:
        return self.client.modify_db_account_privilege(ModifyDBAccountPrivilegeRequest(**args))

    def create_schema(self, args: dict) -> CreateSchemaResponse:
        return self.client.create_schema(CreateSchemaRequest(**args))

    def modify_schema_owner(self, args: dict) -> ModifySchemaOwnerResponse:
        return self.client.modify_schema_owner(ModifySchemaOwnerRequest(**args))

    def describe_schemas(self, args: dict) -> DescribeSchemasResponse:
        return self.client.describe_schemas(DescribeSchemasRequest(**args))

    def modify_database_owner(self, args: dict) -> ModifyDatabaseOwnerResponse:
        return self.client.modify_database_owner(ModifyDatabaseOwnerRequest(**args))

    def create_database(self, args: dict) -> CreateDatabaseResponse:
        return self.client.create_database(CreateDatabaseRequest(**args))

    def describe_databases(self, args: dict) -> DescribeDatabasesResponse:
        return self.client.describe_databases(DescribeDatabasesRequest(**args))

    def create_db_account(self, args: dict) -> CreateDBAccountResponse:
        return self.client.create_db_account(CreateDBAccountRequest(**args))

    def describe_db_accounts(self, args: dict) -> DescribeDBAccountsResponse:
        return self.client.describe_db_accounts(DescribeDBAccountsRequest(**args))

    def describe_wal_log_backups(self, args: dict) -> DescribeWALLogBackupsResponse:
        return self.client.describe_wal_log_backups(DescribeWALLogBackupsRequest(**args))

    def describe_db_instance_ssl(self, args: dict) -> DescribeDBInstanceSSLResponse:
        return self.client.describe_db_instance_ssl(DescribeDBInstanceSSLRequest(**args))

    def describe_tasks(self, args: dict) -> DescribeTasksResponse:
        return self.client.describe_tasks(DescribeTasksRequest(**args))

    def describe_db_engine_version_parameters(self, args: dict) -> DescribeDBEngineVersionParametersResponse:
        return self.client.describe_db_engine_version_parameters(DescribeDBEngineVersionParametersRequest(**args))

    def describe_planned_events(self, args: dict) -> DescribePlannedEventsResponse:
        return self.client.describe_planned_events(DescribePlannedEventsRequest(**args))

    def get_backup_download_link(self, args: dict) -> GetBackupDownloadLinkResponse:
        return self.client.get_backup_download_link(GetBackupDownloadLinkRequest(**args))

    def clone_database(self, args: dict) -> CloneDatabaseResponse:
        return self.client.clone_database(CloneDatabaseRequest(**args))
