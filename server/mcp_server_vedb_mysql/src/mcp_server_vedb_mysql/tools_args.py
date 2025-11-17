from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk


@mcp_server.tool(
    description="将指定实例的参数配置保存为参数模板。触发示例：将实例vedbm-instanceid的当前参数配置保存为新的参数模板，模板名称为custom_template"
)
def save_as_parameter_template(instance_id: str,
                               template_name: str,
                               template_description: Optional[str] = None) -> dict[str, Any]:
    """
       Returns: template_id (str): 参数模板 ID。示例值：vedbmpt-****
    """
    req = {
        "instance_id": instance_id,
        "template_name": template_name,
        "template_description": template_description,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.save_as_parameter_template(req)
    return resp.to_dict()

@mcp_server.tool(
    description="创建参数模板。触发示例：创建一个名为new_template的MySQL 8.0参数模板，包含参数max_connections=1000"
)
def create_parameter_template(template_name: str,
                              template_type_version: Annotated[str, Field(examples=['MySQL_5_7','MySQL_8_0'])],
                              template_parameters: Annotated[list[dict[str, Any]], Field(examples=['[{"ParameterName":"table_definition_cache","ParameterValue":"524288"},{"ParameterName":"table_open_cache","ParameterValue":"{MAX(DBNodeClassMemory/1073741824*256,8192)}"}]'])],
                              template_category: str = 'DBEngine',
                              template_type: str = 'MySQL',
                              template_description: str = None) -> dict[str, Any]:
    """
    Returns: template_id (str): 参数模板 ID。示例值：vedbmpt-****
    """
    req = {
        "template_name": template_name,
        "template_category": template_category,
        "template_type": template_type,
        "template_type_version": template_type_version,
        "template_parameters": template_parameters,
        "template_description": template_description,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.create_parameter_template(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询参数模板列表。触发示例：查询所有MySQL 8.0版本的参数模板"
)
def list_parameter_templates(template_category: Optional[Annotated[str,Field(examples=['DBEngine'])]] = None,
                                 template_id: str = None,
                                 template_name: str = None,
                                 template_source: Optional[Annotated[str,Field(examples=['System','User'])]] = None,
                                 template_type: Optional[Annotated[str,Field(examples=['MySQL'])]] = None,
                                 page_size: int = 1000,
                                 page_number: int = 1,
                                 template_type_version: Optional[Annotated[str,Field(examples=['MySQL_5_7','MySQL_8_0'])]] = None) -> dict[str, Any]:
    req = {
        "page_size": page_size,
        "page_number": page_number,
        "template_category": template_category,
        "template_id": template_id,
        "template_name": template_name,
        "template_source": template_source,
        "template_type": template_type,
        "template_type_version": template_type_version,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_parameter_templates(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询参数模板详情。触发示例：查询参数模板vedbmpt-****的详细配置"
)
def describe_parameter_template_detail(template_id: str) -> dict[str, Any]:
    req = {
        "template_id": template_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_parameter_template_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询实例的mysql参数列表（非管控面实例属性）。触发示例：查询实例vedbm-instanceid的所有内核参数"
)
def describe_db_parameters(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_parameters(req)
    return resp.to_dict()
