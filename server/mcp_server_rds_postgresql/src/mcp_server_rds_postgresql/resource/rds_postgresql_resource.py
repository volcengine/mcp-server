import volcenginesdkcore
from volcenginesdkrdspostgresql.api.rds_postgresql_api import RDSPOSTGRESQLApi
from volcenginesdkrdspostgresql.models import DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse,\
    DescribeDatabasesRequest, DescribeDatabasesResponse, \
    DescribeDBAccountsRequest, DescribeDBAccountsResponse, \
    DescribeSchemasRequest, DescribeSchemasResponse, \
    DescribeDBInstanceParametersRequest, DescribeDBInstanceParametersResponse,\
    DescribeAllowListsRequest, DescribeAllowListsResponse,\
    DescribeAllowListDetailRequest, DescribeAllowListDetailResponse, \
    DescribeBackupsRequest, DescribeBackupsResponse, \
    DescribeBackupPolicyRequest, DescribeBackupPolicyResponse, \
    CreateDBInstanceRequest, CreateDBInstanceResponse, \
    CreateDatabaseRequest, CreateDatabaseResponse, \
    CreateDBAccountRequest, CreateDBAccountResponse, \
    CreateSchemaRequest, CreateSchemaResponse

class RDSPostgreSQLSDK:
    """初始化 volc RDS PostgreSQL client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = RDSPOSTGRESQLApi(volcenginesdkcore.ApiClient(configuration, "X-PGMgr-Source", "local_mcp"))

    def describe_db_instances(self, args: dict) -> DescribeDBInstancesResponse:
        return self.client.describe_db_instances(DescribeDBInstancesRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def describe_databases(self, args: dict) -> DescribeDatabasesResponse:
        return self.client.describe_databases(DescribeDatabasesRequest(**args))
    
    def describe_db_accounts(self, args: dict) -> DescribeDBAccountsResponse:
        return self.client.describe_db_accounts(DescribeDBAccountsRequest(**args))
    
    def describe_schemas(self, args: dict) -> DescribeSchemasResponse:
        return self.client.describe_schemas(DescribeSchemasRequest(**args))

    def describe_db_instance_parameters(self, args: dict) -> DescribeDBInstanceParametersResponse:
        return self.client.describe_db_instance_parameters(DescribeDBInstanceParametersRequest(**args))

    def describe_allow_lists(self, args: dict) -> DescribeAllowListsResponse:
        return self.client.describe_allow_lists(DescribeAllowListsRequest(**args))

    def describe_allow_list_detail(self, args: dict) -> DescribeAllowListDetailResponse:
        return self.client.describe_allow_list_detail(DescribeAllowListDetailRequest(**args))

    def describe_backups(self, args: dict) -> DescribeBackupsResponse:
        return self.client.describe_backups(DescribeBackupsRequest(**args))

    def describe_backup_policy(self, args: dict) -> DescribeBackupPolicyResponse:
        return self.client.describe_backup_policy(DescribeBackupPolicyRequest(**args))

    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))
    
    def create_database(self, args: dict) -> CreateDatabaseResponse:
        return self.client.create_database(CreateDatabaseRequest(**args))
    
    def create_db_account(self, args: dict) -> CreateDBAccountResponse:
        return self.client.create_db_account(CreateDBAccountRequest(**args))
    
    def create_schema(self, args: dict) -> CreateSchemaResponse:
        return self.client.create_schema(CreateSchemaRequest(**args))
