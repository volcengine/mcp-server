import json
import logging
import os

from mcp_server_flink.resources.log import list_gas_logs_api
from mcp_server_flink.resources.services import LogLevelEnum, ComponentEnum
from mcp_server_flink.utils.open_api_client import DEFAULT_OPENAPI_CONTEXT
from mcp_server_flink.utils.utils import get_application_id, get_project_id
from tests.resources.constants import ENV_TEST_JOB_NAME

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_list_gas_logs_api():
    job_name = os.getenv(ENV_TEST_JOB_NAME)
    project_id = get_project_id(DEFAULT_OPENAPI_CONTEXT, DEFAULT_OPENAPI_CONTEXT.project_name)
    app_id = get_application_id(DEFAULT_OPENAPI_CONTEXT, job_name, project_id)
    response = list_gas_logs_api(DEFAULT_OPENAPI_CONTEXT, app_id, project_id, 1761817890388, 1761818790388,
                                 LogLevelEnum.ALL,
                                 ComponentEnum.TASKMANAGER, "")
    logger.info(json.dumps(response))
