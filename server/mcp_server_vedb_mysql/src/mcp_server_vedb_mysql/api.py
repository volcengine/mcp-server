from typing import Any
import volcenginesdkcore
from volcenginesdkvedbm.api.vedbm_api import VEDBMApi
from volcenginesdkvedbm.models import ModifyDBNodeConfigRequest, ModifyDBNodeConfigResponse, \
    SaveAsParameterTemplateRequest, SaveAsParameterTemplateResponse, \
    CreateParameterTemplateRequest, CreateParameterTemplateResponse, \
    ApplyParameterTemplateRequest, ApplyParameterTemplateResponse, \
    DescribeParameterTemplatesRequest, DescribeParameterTemplatesResponse, \
    DescribeDBInstanceParameterChangeHistoryRequest, DescribeDBInstanceParameterChangeHistoryResponse, \
    DeleteParameterTemplateRequest, DeleteParameterTemplateResponse, \
    DescribeParameterTemplateDetailRequest, DescribeParameterTemplateDetailResponse, \
    DescribeDBInstanceParametersRequest, DescribeDBInstanceParametersResponse, \
    ModifyDBInstanceParametersRequest, ModifyDBInstanceParametersResponse, \
    DescribeModifiableParametersRequest, DescribeModifiableParametersResponse, \
    ModifyDBAccountDescriptionRequest, ModifyDBAccountDescriptionResponse, \
    ModifyDatabaseDescriptionRequest, ModifyDatabaseDescriptionResponse, \
    DescribeInstanceAllowListsRequest, DescribeInstanceAllowListsResponse, \
    ModifyDBInstanceDeletionProtectionPolicyRequest, ModifyDBInstanceDeletionProtectionPolicyResponse, \
    DescribeStoragePayablePriceRequest, DescribeStoragePayablePriceResponse, \
    ModifyDBEndpointAddressRequest, ModifyDBEndpointAddressResponse, \
    DescribeDBInstanceVersionRequest, DescribeDBInstanceVersionResponse, \
    CancelScheduleEventsRequest, CancelScheduleEventsResponse, \
    DescribeScheduleEventsRequest, DescribeScheduleEventsResponse, \
    ModifyScheduleEventsRequest, ModifyScheduleEventsResponse, \
    ResetAccountRequest, ResetAccountResponse, \
    ModifyDBEndpointDNSRequest, ModifyDBEndpointDNSResponse, \
    DescribeDBEndpointRequest, DescribeDBEndpointResponse, \
    ModifyDBInstanceChargeTypeRequest, ModifyDBInstanceChargeTypeResponse, \
    RestoreTableRequest, RestoreTableResponse, \
    DescribeExistDBInstancePriceRequest, DescribeExistDBInstancePriceResponse, \
    AddTagsToResourceRequest, AddTagsToResourceResponse, \
    RemoveTagsFromResourceRequest, RemoveTagsFromResourceResponse, \
    DeleteDBEndpointRequest, DeleteDBEndpointResponse, \
    CreateDBEndpointRequest, CreateDBEndpointResponse, \
    ModifyDBEndpointRequest, ModifyDBEndpointResponse, \
    ModifyDBInstanceMaintenanceWindowRequest, ModifyDBInstanceMaintenanceWindowResponse, \
    ModifyAllowListRequest, ModifyAllowListResponse, \
    ModifyDBInstanceSpecRequest, ModifyDBInstanceSpecResponse, \
    RevokeDBAccountPrivilegeRequest, RevokeDBAccountPrivilegeResponse, \
    GrantDBAccountPrivilegeRequest, GrantDBAccountPrivilegeResponse, \
    ModifyBackupPolicyRequest, ModifyBackupPolicyResponse, \
    ResetDBAccountRequest, ResetDBAccountResponse, \
    ModifyDBInstanceNameRequest, ModifyDBInstanceNameResponse, \
    RestoreToNewInstanceRequest, RestoreToNewInstanceResponse, \
    RestartDBInstanceRequest, RestartDBInstanceResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse, \
    DescribeDatabasesRequest, DescribeDatabasesResponse, \
    DescribeAllowListDetailRequest, DescribeAllowListDetailResponse, \
    AssociateAllowListRequest, AssociateAllowListResponse, \
    CreateAllowListRequest, CreateAllowListResponse, \
    CreateBackupRequest, CreateBackupResponse, \
    ChangeMasterRequest, ChangeMasterResponse, \
    CreateDBAccountRequest, CreateDBAccountResponse, \
    CreateDBEndpointPublicAddressRequest, CreateDBEndpointPublicAddressResponse, \
    CreateDatabaseRequest, CreateDatabaseResponse, \
    DeleteBackupRequest, DeleteBackupResponse, \
    DeleteDBAccountRequest, DeleteDBAccountResponse, \
    DeleteAllowListRequest, DeleteAllowListResponse, \
    DeleteDBEndpointPublicAddressRequest, DeleteDBEndpointPublicAddressResponse, \
    DescribeAvailabilityZonesRequest, DescribeAvailabilityZonesResponse, \
    DeleteDatabaseRequest, DeleteDatabaseResponse, \
    DescribeBackupPolicyRequest, DescribeBackupPolicyResponse, \
    DeleteDBInstanceRequest, DeleteDBInstanceResponse, \
    CreateDBInstanceRequest, CreateDBInstanceResponse, \
    DescribeAllowListsRequest, DescribeAllowListsResponse, \
    DescribeBackupsRequest, DescribeBackupsResponse, \
    DescribeDBAccountsRequest, DescribeDBAccountsResponse, \
    DescribeDBInstanceSpecsRequest, DescribeDBInstanceSpecsResponse, \
    DescribeDBInstancePriceDetailRequest, DescribeDBInstancePriceDetailResponse, \
    DescribeRegionsRequest, DescribeRegionsResponse, \
    DescribeRecoverableTimeRequest, DescribeRecoverableTimeResponse, \
    DisassociateAllowListRequest, DisassociateAllowListResponse

class VEDBMSDK:
    """初始化 volc vedbm 客户端"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None, header_name=None, header_value=None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = VEDBMApi(volcenginesdkcore.ApiClient(configuration, header_name, header_value))

    def modify_db_node_config(self, args: dict) -> ModifyDBNodeConfigResponse:
        return self.client.modify_db_node_config(ModifyDBNodeConfigRequest(**args))

    def save_as_parameter_template(self, args: dict) -> SaveAsParameterTemplateResponse:
        return self.client.save_as_parameter_template(SaveAsParameterTemplateRequest(**args))

    def create_parameter_template(self, args: dict) -> CreateParameterTemplateResponse:
        return self.client.create_parameter_template(CreateParameterTemplateRequest(**args))

    def apply_parameter_template(self, args: dict) -> ApplyParameterTemplateResponse:
        return self.client.apply_parameter_template(ApplyParameterTemplateRequest(**args))

    def describe_parameter_templates(self, args: dict) -> DescribeParameterTemplatesResponse:
        return self.client.describe_parameter_templates(DescribeParameterTemplatesRequest(**args))

    def describe_db_instance_parameter_change_history(self, args: dict) -> DescribeDBInstanceParameterChangeHistoryResponse:
        return self.client.describe_db_instance_parameter_change_history(DescribeDBInstanceParameterChangeHistoryRequest(**args))

    def delete_parameter_template(self, args: dict) -> DeleteParameterTemplateResponse:
        return self.client.delete_parameter_template(DeleteParameterTemplateRequest(**args))

    def describe_parameter_template_detail(self, args: dict) -> DescribeParameterTemplateDetailResponse:
        return self.client.describe_parameter_template_detail(DescribeParameterTemplateDetailRequest(**args))

    def describe_db_instance_parameters(self, args: dict) -> DescribeDBInstanceParametersResponse:
        return self.client.describe_db_instance_parameters(DescribeDBInstanceParametersRequest(**args))

    def modify_db_instance_parameters(self, args: dict) -> ModifyDBInstanceParametersResponse:
        return self.client.modify_db_instance_parameters(ModifyDBInstanceParametersRequest(**args))

    def describe_modifiable_parameters(self, args: dict) -> DescribeModifiableParametersResponse:
        return self.client.describe_modifiable_parameters(DescribeModifiableParametersRequest(**args))

    def modify_db_account_description(self, args: dict) -> ModifyDBAccountDescriptionResponse:
        return self.client.modify_db_account_description(ModifyDBAccountDescriptionRequest(**args))

    def modify_database_description(self, args: dict) -> ModifyDatabaseDescriptionResponse:
        return self.client.modify_database_description(ModifyDatabaseDescriptionRequest(**args))

    def describe_instance_allow_lists(self, args: dict) -> DescribeInstanceAllowListsResponse:
        return self.client.describe_instance_allow_lists(DescribeInstanceAllowListsRequest(**args))

    def modify_db_instance_deletion_protection_policy(self, args: dict) -> ModifyDBInstanceDeletionProtectionPolicyResponse:
        return self.client.modify_db_instance_deletion_protection_policy(ModifyDBInstanceDeletionProtectionPolicyRequest(**args))

    def describe_storage_payable_price(self, args: dict) -> DescribeStoragePayablePriceResponse:
        return self.client.describe_storage_payable_price(DescribeStoragePayablePriceRequest(**args))

    def modify_db_endpoint_address(self, args: dict) -> ModifyDBEndpointAddressResponse:
        return self.client.modify_db_endpoint_address(ModifyDBEndpointAddressRequest(**args))

    def describe_db_instance_version(self, args: dict) -> DescribeDBInstanceVersionResponse:
        return self.client.describe_db_instance_version(DescribeDBInstanceVersionRequest(**args))

    def cancel_schedule_events(self, args: dict) -> CancelScheduleEventsResponse:
        return self.client.cancel_schedule_events(CancelScheduleEventsRequest(**args))

    def describe_schedule_events(self, args: dict) -> DescribeScheduleEventsResponse:
        return self.client.describe_schedule_events(DescribeScheduleEventsRequest(**args))

    def modify_schedule_events(self, args: dict) -> ModifyScheduleEventsResponse:
        return self.client.modify_schedule_events(ModifyScheduleEventsRequest(**args))

    def reset_account(self, args: dict) -> ResetAccountResponse:
        return self.client.reset_account(ResetAccountRequest(**args))

    def modify_db_endpoint_dns(self, args: dict) -> ModifyDBEndpointDNSResponse:
        return self.client.modify_db_endpoint_dns(ModifyDBEndpointDNSRequest(**args))

    def describe_db_endpoint(self, args: dict) -> DescribeDBEndpointResponse:
        return self.client.describe_db_endpoint(DescribeDBEndpointRequest(**args))

    def modify_db_instance_charge_type(self, args: dict) -> ModifyDBInstanceChargeTypeResponse:
        return self.client.modify_db_instance_charge_type(ModifyDBInstanceChargeTypeRequest(**args))

    def restore_table(self, args: dict) -> RestoreTableResponse:
        return self.client.restore_table(RestoreTableRequest(**args))

    def describe_exist_db_instance_price(self, args: dict) -> DescribeExistDBInstancePriceResponse:
        return self.client.describe_exist_db_instance_price(DescribeExistDBInstancePriceRequest(**args))

    def add_tags_to_resource(self, args: dict) -> AddTagsToResourceResponse:
        return self.client.add_tags_to_resource(AddTagsToResourceRequest(**args))

    def remove_tags_from_resource(self, args: dict) -> RemoveTagsFromResourceResponse:
        return self.client.remove_tags_from_resource(RemoveTagsFromResourceRequest(**args))

    def delete_db_endpoint(self, args: dict) -> DeleteDBEndpointResponse:
        return self.client.delete_db_endpoint(DeleteDBEndpointRequest(**args))

    def create_db_endpoint(self, args: dict) -> CreateDBEndpointResponse:
        return self.client.create_db_endpoint(CreateDBEndpointRequest(**args))

    def modify_db_endpoint(self, args: dict) -> ModifyDBEndpointResponse:
        return self.client.modify_db_endpoint(ModifyDBEndpointRequest(**args))

    def modify_db_instance_maintenance_window(self, args: dict) -> ModifyDBInstanceMaintenanceWindowResponse:
        return self.client.modify_db_instance_maintenance_window(ModifyDBInstanceMaintenanceWindowRequest(**args))

    def modify_allow_list(self, args: dict) -> ModifyAllowListResponse:
        return self.client.modify_allow_list(ModifyAllowListRequest(**args))

    def modify_db_instance_spec(self, args: dict) -> ModifyDBInstanceSpecResponse:
        return self.client.modify_db_instance_spec(ModifyDBInstanceSpecRequest(**args))

    def revoke_db_account_privilege(self, args: dict) -> RevokeDBAccountPrivilegeResponse:
        return self.client.revoke_db_account_privilege(RevokeDBAccountPrivilegeRequest(**args))

    def grant_db_account_privilege(self, args: dict) -> GrantDBAccountPrivilegeResponse:
        return self.client.grant_db_account_privilege(GrantDBAccountPrivilegeRequest(**args))

    def modify_backup_policy(self, args: dict) -> ModifyBackupPolicyResponse:
        return self.client.modify_backup_policy(ModifyBackupPolicyRequest(**args))

    def reset_db_account(self, args: dict) -> ResetDBAccountResponse:
        return self.client.reset_db_account(ResetDBAccountRequest(**args))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def restore_to_new_instance(self, args: dict) -> RestoreToNewInstanceResponse:
        return self.client.restore_to_new_instance(RestoreToNewInstanceRequest(**args))

    def restart_db_instance(self, args: dict) -> RestartDBInstanceResponse:
        return self.client.restart_db_instance(RestartDBInstanceRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def describe_databases(self, args: dict) -> DescribeDatabasesResponse:
        return self.client.describe_databases(DescribeDatabasesRequest(**args))

    def describe_allow_list_detail(self, args: dict) -> DescribeAllowListDetailResponse:
        return self.client.describe_allow_list_detail(DescribeAllowListDetailRequest(**args))

    def associate_allow_list(self, args: dict) -> AssociateAllowListResponse:
        return self.client.associate_allow_list(AssociateAllowListRequest(**args))

    def create_allow_list(self, args: dict) -> CreateAllowListResponse:
        return self.client.create_allow_list(CreateAllowListRequest(**args))

    def create_backup(self, args: dict) -> CreateBackupResponse:
        return self.client.create_backup(CreateBackupRequest(**args))

    def change_master(self, args: dict) -> ChangeMasterResponse:
        return self.client.change_master(ChangeMasterRequest(**args))

    def create_db_account(self, args: dict) -> CreateDBAccountResponse:
        return self.client.create_db_account(CreateDBAccountRequest(**args))

    def create_db_endpoint_public_address(self, args: dict) -> CreateDBEndpointPublicAddressResponse:
        return self.client.create_db_endpoint_public_address(CreateDBEndpointPublicAddressRequest(**args))

    def create_database(self, args: dict) -> CreateDatabaseResponse:
        return self.client.create_database(CreateDatabaseRequest(**args))

    def delete_backup(self, args: dict) -> DeleteBackupResponse:
        return self.client.delete_backup(DeleteBackupRequest(**args))

    def delete_db_account(self, args: dict) -> DeleteDBAccountResponse:
        return self.client.delete_db_account(DeleteDBAccountRequest(**args))

    def delete_allow_list(self, args: dict) -> DeleteAllowListResponse:
        return self.client.delete_allow_list(DeleteAllowListRequest(**args))

    def delete_db_endpoint_public_address(self, args: dict) -> DeleteDBEndpointPublicAddressResponse:
        return self.client.delete_db_endpoint_public_address(DeleteDBEndpointPublicAddressRequest(**args))

    def describe_availability_zones(self, args: dict) -> DescribeAvailabilityZonesResponse:
        return self.client.describe_availability_zones(DescribeAvailabilityZonesRequest(**args))

    def delete_database(self, args: dict) -> DeleteDatabaseResponse:
        return self.client.delete_database(DeleteDatabaseRequest(**args))

    def describe_backup_policy(self, args: dict) -> DescribeBackupPolicyResponse:
        return self.client.describe_backup_policy(DescribeBackupPolicyRequest(**args))

    def delete_db_instance(self, args: dict) -> DeleteDBInstanceResponse:
        return self.client.delete_db_instance(DeleteDBInstanceRequest(**args))

    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))

    def describe_allow_lists(self, args: dict) -> DescribeAllowListsResponse:
        return self.client.describe_allow_lists(DescribeAllowListsRequest(**args))

    def describe_backups(self, args: dict) -> DescribeBackupsResponse:
        return self.client.describe_backups(DescribeBackupsRequest(**args))

    def describe_db_accounts(self, args: dict) -> DescribeDBAccountsResponse:
        return self.client.describe_db_accounts(DescribeDBAccountsRequest(**args))

    def describe_db_instance_specs(self, args: dict) -> DescribeDBInstanceSpecsResponse:
        return self.client.describe_db_instance_specs(DescribeDBInstanceSpecsRequest(**args))

    def describe_db_instance_price_detail(self, args: dict) -> DescribeDBInstancePriceDetailResponse:
        return self.client.describe_db_instance_price_detail(DescribeDBInstancePriceDetailRequest(**args))

    def describe_regions(self, args: dict) -> DescribeRegionsResponse:
        return self.client.describe_regions(DescribeRegionsRequest(**args))

    def describe_recoverable_time(self, args: dict) -> DescribeRecoverableTimeResponse:
        return self.client.describe_recoverable_time(DescribeRecoverableTimeRequest(**args))

    def disassociate_allow_list(self, args: dict) -> DisassociateAllowListResponse:
        return self.client.disassociate_allow_list(DisassociateAllowListRequest(**args))

    def modify_global_read_only(self, args: dict) -> dict[str, Any]:
        # TODO: cannot import name 'ModifyGlobalReadOnlyRequest' and 'ModifyGlobalReadOnlyResponse' from 'volcenginesdkvedbm.models', need to check and re develop this method.
        raise NotImplementedError

    def describe_cold_data_archive_detail(self, args: dict) -> dict[str, Any]:
        # TODO: cannot import name 'DescribeColdDataArchiveDetailRequest' and 'DescribeColdDataArchiveDetailResponse' from 'volcenginesdkvedbm.models', need to check and re develop this method.
        raise NotImplementedError

    def create_online_ddl_task(self, args: dict) -> dict[str, Any]:
        # TODO: cannot import name 'CreateOnlineDDLTaskRequest' and 'CreateOnlineDDLTaskResponse' from 'volcenginesdkvedbm.models', need to check and re develop this method.
        raise NotImplementedError

    def pre_check_online_ddl_task(self, args: dict) -> dict[str, Any]:
        # TODO: cannot import name 'PreCheckOnlineDDLTaskRequest' and 'PreCheckOnlineDDLTaskResponse' from 'volcenginesdkvedbm.models', need to check and re develop this method.
        raise NotImplementedError

    def list_online_ddl_tasks(self, args: dict) -> dict[str, Any]:
        # TODO: cannot import name 'ListOnlineDDLTasksRequest' and 'ListOnlineDDLTasksResponse' from 'volcenginesdkvedbm.models', need to check and re develop this method.
        raise NotImplementedError

    def stop_online_ddl_task(self, args: dict) -> dict[str, Any]:
        # TODO: cannot import name 'StopOnlineDDLTaskRequest' and 'StopOnlineDDLTaskResponse' from 'volcenginesdkvedbm.models', need to check and re develop this method.
        raise NotImplementedError
