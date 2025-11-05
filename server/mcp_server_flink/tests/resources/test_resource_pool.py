import json
import logging

from mcp_server_flink.resources.resource_pool import list_gmcs_resource_pool_api
from mcp_server_flink.utils.open_api_client import DEFAULT_OPENAPI_CONTEXT
from mcp_server_flink.utils.utils import get_project_id

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_list_gmcs_resource_pool_api():
    project_id = get_project_id(DEFAULT_OPENAPI_CONTEXT, DEFAULT_OPENAPI_CONTEXT.project_name)
    response = list_gmcs_resource_pool_api(DEFAULT_OPENAPI_CONTEXT, project_id)
    logger.info(json.dumps(response))
