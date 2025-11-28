import logging
from typing import Optional, List

from volcengine.tls.tls_exception import TLSException
from volcengine.tls.tls_requests import DescribeProjectRequest, DescribeProjectsRequest, CreateProjectRequest, DeleteProjectRequest
from volcengine.tls.tls_responses import DescribeProjectResponse, DescribeProjectsResponse, CreateProjectResponse, DeleteProjectResponse
from volcengine.tls.data import TagInfo

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

async def create_project_resource(
        auth_info: dict,
        project_name: str,
        region: str,
        description: Optional[str] = None,
        iam_project_name: Optional[str] = None,
        tags: Optional[List] = None,
) -> dict:
    """create_project resource
    """
    try:
        # 转换tags格式：将字典列表转换为TagInfo对象列表
        tag_objects = None
        if tags is not None:
            tag_objects = []
            for tag_dict in tags:
                tag_objects.append(TagInfo(key=tag_dict.get("key"), value=tag_dict.get("value")))
        
        request: CreateProjectRequest = CreateProjectRequest(
            project_name=project_name,
            region=region,
            description=description,
            iam_project_name=iam_project_name,
            tags=tag_objects,
        )

        response: CreateProjectResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="create_project",
            create_project_request=request,
        )

        return {"project_id": response.get_project_id()}

    except TLSException as e:
        logger.error("create_project_resource error")
        raise e

async def delete_project_resource(
        auth_info: dict,
        project_id: str,
) -> dict:
    """delete_project resource
    """
    try:
        request: DeleteProjectRequest = DeleteProjectRequest(
            project_id=project_id,
        )

        response: DeleteProjectResponse = await call_sdk_method(
            auth_info=auth_info,
            method_name="delete_project",
            delete_project_request=request,
        )

        return {"request_id": response.get_request_id()}

    except TLSException as e:
        logger.error("delete_project_resource error")
        raise e