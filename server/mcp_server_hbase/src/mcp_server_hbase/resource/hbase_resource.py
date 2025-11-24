import volcenginesdkcore
from volcenginesdkhbase.api.hbase_api import HBASEApi
from volcenginesdkhbase.models import ModifyDBInstanceNameRequest, ModifyDBInstanceNameResponse, \
    CreateDBInstanceRequest, CreateDBInstanceResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse, \
    DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
ModifyInstanceDeletionProtectionPolicyRequest, ModifyInstanceDeletionProtectionPolicyResponse

class HBASESDK:
    """初始化 volc hbase 客户端"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None, header_name=None, header_value=None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host
        self.client = HBASEApi(volcenginesdkcore.ApiClient(configuration, header_name, header_value))

    def modify_db_instance_name(self, args: dict) -> ModifyDBInstanceNameResponse:
        return self.client.modify_db_instance_name(ModifyDBInstanceNameRequest(**args))

    def create_db_instance(self, args: dict) -> CreateDBInstanceResponse:
        return self.client.create_db_instance(CreateDBInstanceRequest(**args))

    def describe_db_instance_detail(self, args: dict) -> DescribeDBInstanceDetailResponse:
        return self.client.describe_db_instance_detail(DescribeDBInstanceDetailRequest(**args))

    def describe_db_instances(self, args: dict) -> DescribeDBInstancesResponse:
        return self.client.describe_db_instances(DescribeDBInstancesRequest(**args))

    def modify_instance_deletion_protection_policy(self, args: dict) -> ModifyInstanceDeletionProtectionPolicyResponse:
        return self.client.modify_instance_deletion_protection_policy(ModifyInstanceDeletionProtectionPolicyRequest(**args))
