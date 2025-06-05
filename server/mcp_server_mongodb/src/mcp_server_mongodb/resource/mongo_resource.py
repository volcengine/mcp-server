import volcenginesdkcore
from volcenginesdkmongodb.api.mongodb_api import MONGODBApi
from volcenginesdkmongodb.models import DescribeDBInstancesRequest, DescribeDBInstancesResponse, \
    DescribeDBInstanceDetailRequest, DescribeDBInstanceDetailResponse, DescribeBackupsRequest, DescribeBackupsResponse, \
    DescribeDBInstanceParametersRequest, DescribeDBInstanceParametersResponse, DescribeSlowLogsRequest, DescribeSlowLogsResponse, \
    CreateDBInstanceRequest, CreateDBInstanceResponse, DescribeAvailabilityZonesRequest, DescribeAvailabilityZonesResponse, \
    DescribeAllowListsRequest, DescribeAllowListsResponse, DescribeNodeSpecsRequest, DescribeNodeSpecsResponse


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

    def describe_node_spec(self, args: dict) -> DescribeNodeSpecsResponse:
        return self.client.describe_node_specs(DescribeNodeSpecsRequest(**args))

