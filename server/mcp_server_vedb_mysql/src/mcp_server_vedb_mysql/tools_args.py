from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk


@mcp_server.tool(
    description="将指定实例的参数配置保存为参数模板。触发示例：将实例vedbm-r3xq0zdl****的当前参数配置保存为新的参数模板，模板名称为custom_template"
)
def save_as_parameter_template(instance_id: str,
                               template_name: str,
                               template_description: Optional[str] = None) -> dict[str, Any]:
    """
       Returns: template_id (str): 参数模板 ID。示例值：vedbmpt-5j37992t****
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
    Returns: template_id (str): 参数模板 ID。示例值：vedbmpt-5j37992t****
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
    description="应用参数模板。触发示例：将参数模板vedbmpt-5j37992t应用到实例vedbm-r3xq0zdl，在可维护时间内执行"
)
def apply_parameter_template(template_id: Annotated[str, Field(examples=['vedbmpt-5j37992t****'])],
                             instance_ids: list[str],
                             schedule_type: Annotated[str, Field(examples=['Immediate','MaintainTime'])]) -> dict[str, Any]:
    req = {
        "template_id": template_id,
        "instance_ids": instance_ids,
        "schedule_type": schedule_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.apply_parameter_template(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询参数模板列表。触发示例：查询所有MySQL 8.0版本的参数模板"
)
def describe_parameter_templates(template_category: Optional[Annotated[str,Field(examples=['DBEngine'])]] = None,
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
    description="查询实例参数修改历史。触发示例：查询实例vedbm-r3xq0zdl****的参数修改历史记录"
)
def list_parameter_change_history(instance_id: str,
                                end_time: Optional[Annotated[str,Field(description='UTC时间', examples=['2020-03-01T00:00:00Z'])]] = None,
                                parameter_name: Optional[Annotated[str,Field(examples=['auto_increment_increment'])]] = None,
                                page_size: int = 1000,
                                page_number: int = 1,
                                start_time: str = None) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "page_size": page_size,
        "page_number": page_number,
        "end_time": end_time,
        "parameter_name": parameter_name,
        "start_time": start_time,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_parameter_change_history(req)
    return resp.to_dict()

@mcp_server.tool(
    description="删除参数模板。触发示例：删除自定义参数模板vedbmpt-5j37992t****"
)
def delete_parameter_template(template_id: str) -> dict[str, Any]:
    req = {
        "template_id": template_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_parameter_template(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询参数模板详情。触发示例：查询参数模板vedbmpt-5j37992t****的详细参数配置"
)
def describe_parameter_template_detail(template_id: str) -> dict[str, Any]:
    req = {
        "template_id": template_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_parameter_template_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询目标实例的参数列表。触发示例：查询实例vedbm-r3xq0zdl****的所有参数配置，包括可修改参数"
)
def describe_db_instance_parameters(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_parameters(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改实例mysqld内核参数（非管控面属性修改）。触发示例：修改实例vedbm-r3xq0zdl****的参数，将innodb_buffer_pool_size设置为2147483648，在可维护时间内执行"
)
def modify_db_instance_parameters(instance_id: str,
                                  parameters: Annotated[list[dict[str, Any]], Field(examples=['[{"ParameterName":"table_definition_cache","ParameterValue":"524288"}]'])],
                                  schedule_type: Annotated[str, Field(examples=['Immediate','MaintainTime'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "parameters": parameters,
        "schedule_type": schedule_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_instance_parameters(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询可修改的参数列表。触发示例：查询实例vedbm-r3xq0zdl****可修改的参数列表"
)
def describe_modifiable_parameters(template_category: str = 'DBEngine',
                                   template_type: str = 'MySQL',
                                   template_type_version: str = 'MySQL_8_0') -> dict[str, Any]:
    req = {
        "template_category": template_category,
        "template_type": template_type,
        "template_type_version": template_type_version,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_modifiable_parameters(req)
    return resp.to_dict()