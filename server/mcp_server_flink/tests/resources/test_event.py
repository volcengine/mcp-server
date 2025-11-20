import json
import logging
import os

from mcp_server_flink.resources.event import get_gws_event_list_api
from mcp_server_flink.utils.open_api_client import DEFAULT_OPENAPI_CONTEXT
from mcp_server_flink.utils.utils import get_project_id, get_application_uniqued_id
from tests.resources.constants import ENV_TEST_JOB_NAME

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_list_gws_event_api():
    project_id = get_project_id(DEFAULT_OPENAPI_CONTEXT, DEFAULT_OPENAPI_CONTEXT.project_name)
    job_name = os.getenv(ENV_TEST_JOB_NAME)
    application_unique_id = get_application_uniqued_id(DEFAULT_OPENAPI_CONTEXT, job_name, project_id)
    response = get_gws_event_list_api(openapi_context=DEFAULT_OPENAPI_CONTEXT, project_id=project_id,
                                      id=application_unique_id)
    logger.info(json.dumps(response))
