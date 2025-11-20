import logging
import os

from mcp_server_flink.utils.open_api_client import DEFAULT_OPENAPI_CONTEXT
from mcp_server_flink.utils.utils import get_application_id, get_project_id, get_application_uniqued_id, \
    get_resource_pool_full_name
from tests.resources.constants import ENV_TEST_JOB_NAME, ENV_TEST_RESOURCE_POOL_NAME

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_get_application_id():
    job_name = os.getenv(ENV_TEST_JOB_NAME)
    project_id = get_project_id(DEFAULT_OPENAPI_CONTEXT, DEFAULT_OPENAPI_CONTEXT.project_name)
    response = get_application_id(DEFAULT_OPENAPI_CONTEXT, job_name, project_id)
    logger.info(response)


def test_get_application_uniqued_id():
    job_name = os.getenv(ENV_TEST_JOB_NAME)
    project_id = get_project_id(DEFAULT_OPENAPI_CONTEXT, DEFAULT_OPENAPI_CONTEXT.project_name)
    response = get_application_uniqued_id(DEFAULT_OPENAPI_CONTEXT, job_name, project_id)
    logger.info(response)


def test_get_resource_pool_full_name():
    resource_pool_name = os.getenv(ENV_TEST_RESOURCE_POOL_NAME)
    project_id = get_project_id(DEFAULT_OPENAPI_CONTEXT, DEFAULT_OPENAPI_CONTEXT.project_name)
    response = get_resource_pool_full_name(DEFAULT_OPENAPI_CONTEXT, resource_pool_name, project_id)
    logger.info(response)
