import json
import logging

from mcp_server_flink.resources.project import list_gms_project_api, get_gms_project_detail_api
from mcp_server_flink.utils.open_api_client import DEFAULT_OPENAPI_CONTEXT

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_list_gms_project_api():
    response = list_gms_project_api(openapi_context=DEFAULT_OPENAPI_CONTEXT,
                                    search_key=DEFAULT_OPENAPI_CONTEXT.project_name)
    logger.info(json.dumps(response))


def test_get_gms_project_detail_api():
    response = get_gms_project_detail_api(openapi_context=DEFAULT_OPENAPI_CONTEXT,
                                          project_name=DEFAULT_OPENAPI_CONTEXT.project_name)
    logger.info(json.dumps(response))
