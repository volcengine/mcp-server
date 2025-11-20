import json
import logging

from mcp_server_flink.resources.job_development import list_gws_directory_api
from mcp_server_flink.utils.open_api_client import DEFAULT_OPENAPI_CONTEXT
from mcp_server_flink.utils.utils import get_project_id

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_list_gws_directory_api():
    project_id = get_project_id(DEFAULT_OPENAPI_CONTEXT, DEFAULT_OPENAPI_CONTEXT.project_name)
    response = list_gws_directory_api(DEFAULT_OPENAPI_CONTEXT, project_id=project_id)
    logger.info(json.dumps(response))
