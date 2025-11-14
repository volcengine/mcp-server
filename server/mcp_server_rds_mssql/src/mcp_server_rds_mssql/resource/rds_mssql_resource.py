import volcenginesdkcore
from volcenginesdkrdsmssql.api.rds_mssql_api import RDSMSSQLApi
from volcenginesdkrdsmssql.models import DescribeAvailableCrossRegionRequest, DescribeAvailableCrossRegionResponse, \
    DescribeCrossBackupPolicyRequest, DescribeCrossBackupPolicyResponse, \
    ModifyCrossBackupPolicyRequest, ModifyCrossBackupPolicyResponse, \
    DescribeBackupDetailRequest, DescribeBackupDetailResponse, \
    RestoreToExistedInstanceRequest, RestoreToExistedInstanceResponse, \
    DescribeTosRestoreTasksRequest, DescribeTosRestoreTasksResponse, \
    DescribeTosRestoreTaskDetailRequest, DescribeTosRestoreTaskDetailResponse, \
    CreateTosRestoreRequest, CreateTosRestoreResponse, \
    DescribeDBInstanceParametersRequest, DescribeDBInstanceParametersResponse, \
    ModifyBackupPolicyRequest, ModifyBackupPolicyResponse, \
    DescribeBackupsRequest, DescribeBackupsResponse, \
    CreateBackupRequest, CreateBackupResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse, \
    DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
    ModifyDBInstanceNameRequest, ModifyDBInstanceNameResponse, \
    DescribeDBInstanceSpecsRequest, DescribeDBInstanceSpecsResponse, \
    DescribeAvailabilityZonesRequest, DescribeAvailabilityZonesResponse, \
    DescribeRegionsRequest, DescribeRegionsResponse, \
CreateDBInstanceRequest, CreateDBInstanceResponse

class RDSMSSQLSDK:
    """初始化 volc rds_mssql 客户端"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None, header_name=None, header_value=None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = RDSMSSQLApi(volcenginesdkcore.ApiClient(configuration, header_name, header_value))

    def describe_available_cross_region(self, args: dict) -> DescribeAvailableCrossRegionResponse:
        return self.client.describe_available_cross_region(DescribeAvailableCrossRegionRequest(**args))

    def describe_cross_backup_policy(self, args: dict) -> DescribeCrossBackupPolicyResponse:
        return self.client.describe_cross_backup_policy(DescribeCrossBackupPolicyRequest(**args))

    def modify_cross_backup_policy(self, args: dict) -> ModifyCrossBackupPolicyResponse:
        return self.client.modify_cross_backup_policy(ModifyCrossBackupPolicyRequest(**args))

    def describe_backup_detail(self, args: dict) -> DescribeBackupDetailResponse:
        return self.client.describe_backup_detail(DescribeBackupDetailRequest(**args))

    def restore_to_existed_instance(self, args: dict) -> RestoreToExistedInstanceResponse:
        return self.client.restore_to_existed_instance(RestoreToExistedInstanceRequest(**args))

    def describe_tos_restore_tasks(self, args: dict) -> DescribeTosRestoreTasksResponse:
        return self.client.describe_tos_restore_tasks(DescribeTosRestoreTasksRequest(**args))

    def describe_tos_restore_task_detail(self, args: dict) -> DescribeTosRestoreTaskDetailResponse:
        return self.client.describe_tos_restore_task_detail(DescribeTosRestoreTaskDetailRequest(**args))

    def create_tos_restore(self, args: dict) -> CreateTosRestoreResponse:
        return self.client.create_tos_restore(CreateTosRestoreRequest(**args))

    def describe_db_instance_parameters(self, args: dict) -> DescribeDBInstanceParametersResponse:
        return self.client.describe_db_instance_parameters(DescribeDBInstanceParametersRequest(**args))

    def modify_backup_policy(self, args: dict) -> ModifyBackupPolicyResponse:
        return self.client.modify_backup_policy(ModifyBackupPolicyRequest(**args))

    def describe_backups(self, args: dict) -> DescribeBackupsResponse:
        return self.client.describe_backups(DescribeBackupsRequest(**args))

    def create_backup(self, args: dict) -> CreateBackupResponse:
        return self.client.create_backup(CreateBackupRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def describe_db_instances(self, args: dict) -> DescribeDBInstancesResponse:
        return self.client.describe_db_instances(DescribeDBInstancesRequest(**args))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def describe_db_instance_specs(self, args: dict) -> DescribeDBInstanceSpecsResponse:
        return self.client.describe_db_instance_specs(DescribeDBInstanceSpecsRequest(**args))

    def describe_availability_zones(self, args: dict) -> DescribeAvailabilityZonesResponse:
        return self.client.describe_availability_zones(DescribeAvailabilityZonesRequest(**args))

    def describe_regions(self, args: dict) -> DescribeRegionsResponse:
        return self.client.describe_regions(DescribeRegionsRequest(**args))

    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))
