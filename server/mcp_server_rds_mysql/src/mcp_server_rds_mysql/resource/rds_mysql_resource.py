import volcenginesdkcore
from volcenginesdkrdsmysqlv2.api.rds_mysql_v2_api import RDSMYSQLV2Api
from volcenginesdkrdsmysqlv2.models import DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse,\
    DescribeDBInstanceEngineMinorVersionsRequest,DescribeDBInstanceEngineMinorVersionsResponse,\
    DescribeDBAccountsRequest,DescribeDBAccountsResponse,\
    DescribeDatabasesRequest,DescribeDatabasesResponse,\
    DescribeParameterTemplateRequest, DescribeParameterTemplateResponse,\
    DescribeDBInstanceParametersRequest, DescribeDBInstanceParametersResponse, \
    ListParameterTemplatesRequest,ListParameterTemplatesResponse,\
    CreateDBInstanceRequest, CreateDBInstanceResponse,\
    ModifyDBInstanceNameRequest,ModifyDBInstanceNameResponse,\
    ModifyDBAccountDescriptionRequest,ModifyDBAccountDescriptionResponse,\
    CreateDatabaseRequest, CreateDatabaseResponse, \
    CreateAllowListRequest, CreateAllowListResponse, \
    AssociateAllowListRequest, AssociateAllowListResponse, \
    CreateDBAccountRequest, CreateDBAccountResponse

from volcenginesdkvpc.api.vpc_api import VPCApi
from volcenginesdkvpc.models import DescribeVpcsRequest, DescribeVpcsResponse, DescribeSubnetsRequest,DescribeSubnetsResponse


class RDSMySQLSDK:
    """初始化 volc RDS MySQL client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = RDSMYSQLV2Api(volcenginesdkcore.ApiClient(configuration))
        self.vpcClient = VPCApi(volcenginesdkcore.ApiClient(configuration))

    def describe_db_instances(self, args: dict) -> DescribeDBInstancesResponse:
        return self.client.describe_db_instances(DescribeDBInstancesRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def describe_db_instance_engine_minor_versions(self, args: dict) -> DescribeDBInstanceEngineMinorVersionsResponse:
        return self.client.describe_db_instance_engine_minor_versions(DescribeDBInstanceEngineMinorVersionsRequest(**args))

    def describe_db_accounts(self, args: dict) -> DescribeDBAccountsResponse:
        return self.client.describe_db_accounts(DescribeDBAccountsRequest(**args))

    def describe_databases(self, args: dict) -> DescribeDatabasesResponse:
        return self.client.describe_databases(DescribeDatabasesRequest(**args))

    def describe_db_instance_parameters(self, args: dict) -> DescribeDBInstanceParametersResponse:
        return self.client.describe_db_instance_parameters(DescribeDBInstanceParametersRequest(**args))

    def list_parameter_templates(self, args: dict) -> ListParameterTemplatesResponse:
        return self.client.list_parameter_templates(ListParameterTemplatesRequest(**args))

    def describe_parameter_template(self, args: dict) -> DescribeParameterTemplateResponse:
        return self.client.describe_parameter_template(DescribeParameterTemplateRequest(**args))

    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def modify_db_account_description(self, args: dict) -> ModifyDBAccountDescriptionResponse:
        return self.client.modify_db_account_description(ModifyDBAccountDescriptionRequest(**args))

    def create_database(self, args: dict) -> CreateDatabaseResponse:
        return self.client.create_database(CreateDatabaseRequest(**args))

    def create_allow_list(self, args: dict) -> CreateAllowListResponse:
        return self.client.create_allow_list(CreateAllowListRequest(**args))

    def associate_allow_list(self, args: dict) -> AssociateAllowListResponse:
        return self.client.associate_allow_list(AssociateAllowListRequest(**args))

    def create_db_account(self, args: dict) -> CreateDBAccountResponse:
        return self.client.create_db_account(CreateDBAccountRequest(**args))

    def describe_vpcs(self, args: dict) -> DescribeVpcsResponse:
        return self.vpcClient.describe_vpcs(DescribeVpcsRequest(**args))

    def describe_subnets(self, args: dict) -> DescribeSubnetsResponse:
        return self.vpcClient.describe_subnets(DescribeSubnetsRequest(**args))


