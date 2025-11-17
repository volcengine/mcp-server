from mcp_server_flink.resources.job_operation import list_gws_application_api
from mcp_server_flink.resources.project import get_gms_project_detail_api
from mcp_server_flink.resources.resource_pool import list_gmcs_resource_pool_api
from mcp_server_flink.utils.open_api_client import OpenAPIContext


def filter_list_application_response_fields(response: dict, include_fields: list):
    """
    从响应中过滤掉指定字段
    :param response: 原始返回字典
    :param include_fields: 需要包括的字段列表
    :return: 过滤后的字典
    """
    records = response.get("Records", [])
    filtered_records = []

    for record in records:
        filtered_record = {k: v for k, v in record.items() if k in include_fields}
        filtered_records.append(filtered_record)

    # 保留分页信息等其他字段
    return {
        "Records": filtered_records,
        "Total": response.get("Total"),
        "Size": response.get("Size"),
        "Current": response.get("Current")
    }


def filter_list_resource_pool_response_fields(response: dict, include_fields: list):
    """
    从响应中过滤掉指定字段
    :param response: 原始返回字典
    :param include_fields: 需要包括的字段列表
    :return: 过滤后的字典
    """
    datalist = response.get("DataList", [])
    filtered_records = []

    for record in datalist:
        filtered_record = {k: v for k, v in record.items() if k in include_fields}
        filtered_records.append(filtered_record)

    # 保留分页信息等其他字段
    return {
        "DataList": filtered_records,
        "Total": response.get("Total"),
        "PageSize": response.get("PageSize"),
        "PageNum": response.get("PageNum")
    }


def get_project_id(openapi_context: OpenAPIContext, project_name: str) -> str:
    project_id = ""
    if project_name != "":
        project_detail_response = get_gms_project_detail_api(openapi_context, project_name)
        project_id = project_detail_response["ProjectId"]
    return project_id


def get_application_id(openapi_context: OpenAPIContext, job_name: str, project_id: str):
    """
    Retrieve the ApplicationId for a given job_name by searching through the Records list
    returned from list_gws_application_api.
    """
    application_response = list_gws_application_api(
        openapi_context=openapi_context,
        project_id=project_id,
        job_name=job_name
    )

    records = application_response.get("Records", [])
    if not records:
        raise ValueError("No records found in response")

    # Search for a record with the specified job_name
    matched_record = next((r for r in records if r.get("JobName") == job_name), None)
    if not matched_record:
        raise ValueError(f"No record found with job_name='{job_name}'")

    application_id = matched_record.get("ApplicationId")
    if not application_id:
        raise ValueError(f"ApplicationId not found for job_name='{job_name}'")

    return application_id


def get_application_uniqued_id(openapi_context: OpenAPIContext, job_name: str, project_id: str):
    """
    Retrieve the unique Id for a given job_name by searching through the Records list
    returned from list_gws_application_api.
    """
    application_response = list_gws_application_api(
        openapi_context=openapi_context,
        project_id=project_id,
        job_name=job_name
    )

    records = application_response.get("Records", [])
    if not records:
        raise ValueError("No records found in response")

    # Search for a record with the specified job_name
    matched_record = next((r for r in records if r.get("JobName") == job_name), None)
    if not matched_record:
        raise ValueError(f"No record found with job_name='{job_name}'")

    unique_id = matched_record.get("Id")
    if not unique_id:
        raise ValueError(f"Id not found for job_name='{job_name}'")

    return unique_id


def get_resource_pool_full_name(openapi_context, resource_pool: str, project_id: str):
    resource_pool_response = list_gmcs_resource_pool_api(openapi_context=openapi_context, project_id=project_id,
                                                         name=resource_pool)
    if resource_pool_response.get("Total", 0) != 1:
        raise ValueError(f"Expected Total == 1, but got {resource_pool_response.get('Total')}")

    records = resource_pool_response.get("DataList", [])
    if not records:
        raise ValueError("No dataList found in response")

    full_name = records[0].get("FullName")
    if not full_name:
        raise ValueError("Id not found in the record")
    return full_name
