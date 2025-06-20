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
    DescribeAvailabilityZonesRequest, DescribeAvailabilityZonesResponse, \
    DescribeAllowListsRequest, DescribeAllowListsResponse

class RDSMySQLSDK:
    """初始化 volc RDSMySQL client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = RDSMYSQLV2Api(volcenginesdkcore.ApiClient(configuration))

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

    # def describe_allow_lists(self, args: dict) -> DescribeAllowListsResponse:
    #     return self.client.describe_allow_lists(DescribeAllowListsRequest(**args))

    # def describe_azs(self, args: dict) -> DescribeAvailabilityZonesResponse:
    #     return self.client.describe_availability_zones(DescribeAvailabilityZonesRequest(**args))

    # def describe_node_spec(self, args: dict) -> DescribeNodeSpecsResponse:
    #     return self.client.describe_node_specs(DescribeNodeSpecsRequest(**args))
    #
    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def modify_db_account_description(self, args: dict) -> ModifyDBAccountDescriptionResponse:
        return self.client.modify_db_account_description(ModifyDBAccountDescriptionRequest(**args))

