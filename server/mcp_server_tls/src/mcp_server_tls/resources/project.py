import logging
from typing import Optional

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import DescribeProjectRequest, DescribeProjectsRequest
from volcengine.tls.tls_responses import DescribeProjectResponse, DescribeProjectsResponse

from mcp_server_tls.request import call_sdk_method

logger = logging.getLogger(__name__)

async def describe_project_resource(
        auth_info: dict,
        project_id: str,
) -> dict:
    """describe_project resource
    """
    try:
        request: DescribeProjectRequest = DescribeProjectRequest(
            project_id=project_id,
        )

        response: DescribeProjectResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_project",
            describe_project_request=request,
        )

        return vars(response.get_project())

    except TLSException as e:
        logger.error("describe_project_resource error")
        raise e

async def describe_projects_resource(
        auth_info: dict,
        page_number: Optional[int] = 1,
        page_size: Optional[int] = 10,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
        is_full_name: Optional[bool] = False,
        iam_project_name: Optional[str] = None,
) -> dict:
    """describe_projects resource
    """
    try:
        request: DescribeProjectsRequest = DescribeProjectsRequest(
            page_number=page_number,
            page_size=page_size,
            is_full_name=is_full_name,
            project_id=project_id,
            project_name=project_name,
            iam_project_name=iam_project_name,
        )

        response: DescribeProjectsResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="describe_projects",
            describe_projects_request=request,
        )

        return {
            "total": response.get_total(),
            "projects": [vars(project_info) for project_info in response.get_projects()]
        }

    except TLSException as e:
        logger.error("describe_projects_resource error")
        raise e
