import volcenginesdkcore
from volcenginesdkrdsmysqlv2.api.rds_mysql_v2_api import RDSMYSQLV2Api
from volcenginesdkrdsmysqlv2 import models

from volcenginesdkvpc.api.vpc_api import VPCApi
from volcenginesdkvpc.models import DescribeVpcsRequest, DescribeVpcsResponse, DescribeSubnetsRequest, DescribeSubnetsResponse


class RDSMySQLSDK:
    """初始化 volc RDS MySQL client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = RDSMYSQLV2Api(volcenginesdkcore.ApiClient(configuration, "X-Rdsmgr-Source", "mcp_local"))
        self.vpcClient = VPCApi(volcenginesdkcore.ApiClient(configuration))

    def describe_db_instances(self, args: dict) -> models.DescribeDBInstancesResponse:
        return self.client.describe_db_instances(models.DescribeDBInstancesRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> models.DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(models.DescribeDBInstanceDetailRequest(**args))

    def describe_db_instance_engine_minor_versions(self, args: dict) -> models.DescribeDBInstanceEngineMinorVersionsResponse:
        return self.client.describe_db_instance_engine_minor_versions(models.DescribeDBInstanceEngineMinorVersionsRequest(**args))

    def describe_db_accounts(self, args: dict) -> models.DescribeDBAccountsResponse:
        return self.client.describe_db_accounts(models.DescribeDBAccountsRequest(**args))

    def describe_databases(self, args: dict) -> models.DescribeDatabasesResponse:
        return self.client.describe_databases(models.DescribeDatabasesRequest(**args))

    def describe_db_instance_parameters(self, args: dict) -> models.DescribeDBInstanceParametersResponse:
        return self.client.describe_db_instance_parameters(models.DescribeDBInstanceParametersRequest(**args))

    def list_parameter_templates(self, args: dict) -> models.ListParameterTemplatesResponse:
        return self.client.list_parameter_templates(models.ListParameterTemplatesRequest(**args))

    def describe_parameter_template(self, args: dict) -> models.DescribeParameterTemplateResponse:
        return self.client.describe_parameter_template(models.DescribeParameterTemplateRequest(**args))

    def create_db_instance(self, args: dict) -> models.CreateDBInstanceResponse:
        return self.client.create_db_instance(models.CreateDBInstanceRequest(**args))

    def modify_db_instance_name(self, args: dict) -> models.ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(models.ModifyDBInstanceNameRequest(**args))

    def modify_db_account_description(self, args: dict) -> models.ModifyDBAccountDescriptionResponse:
        return self.client.modify_db_account_description(models.ModifyDBAccountDescriptionRequest(**args))

    def create_database(self, args: dict) -> models.CreateDatabaseResponse:
        return self.client.create_database(models.CreateDatabaseRequest(**args))

    def create_allow_list(self, args: dict) -> models.CreateAllowListResponse:
        return self.client.create_allow_list(models.CreateAllowListRequest(**args))

    def associate_allow_list(self, args: dict) -> models.AssociateAllowListResponse:
        return self.client.associate_allow_list(models.AssociateAllowListRequest(**args))

    def create_db_account(self, args: dict) -> models.CreateDBAccountResponse:
        return self.client.create_db_account(models.CreateDBAccountRequest(**args))

    def describe_db_instance_price_detail(self, args: dict) -> models.DescribeDBInstancePriceDetailResponse:
        return self.client.describe_db_instance_price_detail(models.DescribeDBInstancePriceDetailRequest(**args))

    def describe_vpcs(self, args: dict) -> DescribeVpcsResponse:
        return self.vpcClient.describe_vpcs(DescribeVpcsRequest(**args))

    def describe_subnets(self, args: dict) -> DescribeSubnetsResponse:
        return self.vpcClient.describe_subnets(DescribeSubnetsRequest(**args))


