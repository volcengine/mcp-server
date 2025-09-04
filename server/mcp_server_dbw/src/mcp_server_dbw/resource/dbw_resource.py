import volcenginesdkcore
import volcenginesdkdbw
from volcenginesdkdbw.models import GenerateSQLFromNLRequest, GenerateSQLFromNLResponse


class DBWClient:
    """初始化 volc DBW client"""

    def __init__(self, region: str = None, ak: str = None, sk: str = None, host: str = None,
                 instance_id: str = None, instance_type: str = None, database: str = None):
        configuration = volcenginesdkcore.Configuration()
        configuration.ak = ak
        configuration.sk = sk
        configuration.region = region
        if host is not None:
            configuration.host = host

        self.client = volcenginesdkdbw.DBWApi(volcenginesdkcore.ApiClient(configuration))

        self.instance_id = instance_id
        self.instance_type = instance_type
        self.database = database

    def nl2sql(self, args: dict) -> GenerateSQLFromNLResponse:
        return self.client.generate_sql_from_nl(GenerateSQLFromNLRequest(**args))
