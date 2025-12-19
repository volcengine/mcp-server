import volcenginesdkcore
import volcenginesdkdbw
from volcenginesdkdbw.models import *


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
        self.region = region
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.database = database

    def nl2sql(self, args: dict) -> GenerateSQLFromNLResponse:
        return self.client.generate_sql_from_nl(GenerateSQLFromNLRequest(**args))

    def execute_sql(self, args: dict) -> ExecuteSQLResponse:
        return self.client.execute_sql(ExecuteSQLRequest(**args))

    def list_databases(self, args: dict) -> ListDatabasesResponse:
        return self.client.list_databases(ListDatabasesRequest(**args))

    def list_tables(self, args: dict) -> ListTablesResponse:
        return self.client.list_tables(ListTablesRequest(**args))

    def get_table_info(self, args: dict) -> GetTableInfoResponse:
        return self.client.get_table_info(GetTableInfoRequest(**args))

    def describe_slow_logs(self, args: dict) -> DescribeSlowLogsResponse:
        return self.client.describe_slow_logs(DescribeSlowLogsRequest(**args))

    def list_slow_query_advice_api(self, args: dict) -> ListSlowQueryAdviceApiResponse:
        return self.client.list_slow_query_advice_api(ListSlowQueryAdviceApiRequest(**args))

    def slow_query_advice_task_history_api(self, args: dict) -> SlowQueryAdviceTaskHistoryApiResponse:
        return self.client.slow_query_advice_task_history_api(SlowQueryAdviceTaskHistoryApiRequest(**args))

    def create_dml_sql_change_ticket(self, args: dict) -> CreateDmlSqlChangeTicketResponse:
        return self.client.create_dml_sql_change_ticket(CreateDmlSqlChangeTicketRequest(**args))

    def create_ddl_sql_change_ticket(self, args: dict) -> CreateDdlSqlChangeTicketResponse:
        return self.client.create_ddl_sql_change_ticket(CreateDdlSqlChangeTicketRequest(**args))

    def describe_tickets(self, args: dict) -> DescribeTicketsResponse:
        return self.client.describe_tickets(DescribeTicketsRequest(**args))

    def describe_ticket_detail(self, args: dict) -> DescribeTicketDetailResponse:
        return self.client.describe_ticket_detail(DescribeTicketDetailRequest(**args))

    def describe_workflow(self, args: dict) -> DescribeWorkflowResponse:
        return self.client.describe_workflow(DescribeWorkflowRequest(**args))

    def manual_execute_ticket(self, args: dict) -> ManualExecuteTicketResponse:
        return self.client.manual_execute_ticket(ManualExecuteTicketRequest(**args))
