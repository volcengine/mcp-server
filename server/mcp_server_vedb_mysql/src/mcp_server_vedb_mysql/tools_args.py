from typing import Any, Annotated, Optional
from pydantic import Field
from mcp_server_vedb_mysql.config import mcp as mcp_server, openapi_cli as vedbm_resource_sdk


@mcp_server.tool()
def save_as_parameter_template(instance_id: str,
                               template_name: Annotated[str, Field(description='参数模板名称。规则如下：- 只能包含中文、字母、数字、下划线（_）或中划线（-）。- 长度为 8~64 个字符。- 不能以数字、中划线（-）或下划线（_）开头', examples=['template_test'])],
                               template_description: Optional[Annotated[str,Field(description='参数模板描述，描述内容长度为 0~200 个字符。', examples=['描述信息'])]] = None) -> dict[str, Any]:
    """将指定实例的参数配置保存为参数模板
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

@mcp_server.tool()
def create_parameter_template(template_name: Annotated[str, Field(description='参数模板名称。规则如下：- 只能包含中文、字母、数字、下划线（_）或中划线（-）。- 长度为 8~64 个字符。- 不能以数字、中划线（-）或下划线（_）开头', examples=['template_test'])],
                              template_category: Annotated[str, Field(description='参数模板分类，默认值为 `DBEngine`')],
                              template_type: Annotated[str, Field(description='参数模板的数据库类型，默认值为 `MySQL`')],
                              template_type_version: Annotated[str, Field(description='参数模板适用的数据库引擎版本，取值范围：`MySQL_5_7`,`MySQL_8_0`')],
                              template_parameters: Annotated[list[dict[str, Any]], Field(description='参数模板包含的参数和参数值信息', examples=['[{"ParameterName":"table_definition_cache","ParameterValue":"524288"},{"ParameterName":"table_open_cache","ParameterValue":"{MAX(DBNodeClassMemory/1073741824*256,8192)}"}]'])],
                              template_description: Optional[Annotated[str,Field(description='参数模板描述，描述内容长度为 0~200 个字符')]] = None) -> dict[str, Any]:
    """创建参数模板
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

@mcp_server.tool()
def apply_parameter_template(template_id: Annotated[str, Field(examples=['vedbmpt-5j37992t****'])],
                             instance_ids: list[str],
                             schedule_type: Annotated[str, Field(description='执行方式，取值：`Immediate`/`MaintainTime`')]) -> dict[str, Any]:
    """应用参数模板"""
    req = {
        "template_id": template_id,
        "instance_ids": instance_ids,
        "schedule_type": schedule_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.apply_parameter_template(req)
    return resp.to_dict()

@mcp_server.tool()
def describe_parameter_templates(page_size: Annotated[int, Field(description='每页记录数。取值范围 1~1000')],
                                 page_number: Annotated[int, Field(examples=['1'])],
                                 template_category: Optional[Annotated[str,Field(description='参数模板分类，默认值为 `DBEngine`。', examples=['DBEngine枚举值：DBEngine'])]] = None,
                                 template_id: Optional[Annotated[str,Field(description='参数模板 ID。', examples=['vedbmpt-5j37992t****'])]] = None,
                                 template_name: Optional[Annotated[str,Field(description='参数模板名称。', examples=['Template_test'])]] = None,
                                 template_source: Optional[Annotated[str,Field(description='参数模板的类型。取值：- `System`：系统模板。- `User`：用户模板。', examples=['User枚举值：System,User'])]] = None,
                                 template_type: Optional[Annotated[str,Field(description='参数模板的数据库类型，默认值为 `MySQL`。', examples=['MySQL枚举值：MySQL'])]] = None,
                                 template_type_version: Optional[Annotated[str,Field(description='参数模板适用的数据库引擎版本，取值范围：- `MySQL_5_7`：MySQL 5.7 版本。- `MySQL_8_0`：MySQL 8.0 版本。', examples=['MySQL_8_0枚举值：MySQL_5_7,MySQL_8_0'])]] = None) -> dict[str, Any]:
    """查询参数模板列表"""
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
    description="查询实例参数修改历史"
)
def list_parameter_change_history(instance_id: str,
                                                  page_size: Annotated[int, Field(description='每页记录数。取值范围 1~1000，默认值为 10。', examples=['10'])],
                                                  page_number: Annotated[int, Field(description='页码，取值大于等于 1，且不超过 Integer 的最大值，默认值为 1。', examples=['1'])],
                                                  end_time: Optional[Annotated[str,Field(description='查询结束时间。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。', examples=['2020-03-01T00:00:00Z'])]] = None,
                                                  parameter_name: Optional[Annotated[str,Field(description='参数名称。', examples=['auto_increment_increment'])]] = None,
                                                  start_time: Optional[Annotated[str,Field(description='查询开始时间。格式：yyyy-MM-ddTHH:mm:ssZ（UTC 时间）。', examples=['2020-03-01T00:00:00Z'])]] = None) -> dict[str, Any]:
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
    description="删除参数模板"
)
def delete_parameter_template(template_id: Annotated[str, Field(description='参数模板 ID。', examples=['vedbmpt-5j37992t****'])]) -> dict[str, Any]:
    req = {
        "template_id": template_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.delete_parameter_template(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询参数模板详情"
)
def describe_parameter_template_detail(template_id: Annotated[str, Field(description='参数模板 ID。', examples=['vedbmpt-5j37992t****'])]) -> dict[str, Any]:
    req = {
        "template_id": template_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_parameter_template_detail(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询目标实例的参数列表"
)
def describe_db_instance_parameters(instance_id: str) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_db_instance_parameters(req)
    return resp.to_dict()

@mcp_server.tool(
    description="修改实例mysqld数据面参数"
)
def modify_db_instance_parameters(instance_id: str,
                                  parameters: Annotated[list[dict[str, Any]], Field(description='需要修改的参数和参数值。', examples=['[{"ParameterName":"table_definition_cache","ParameterValue":"524288"}]'])],
                                  schedule_type: Annotated[str, Field(description='执行方式，取值：- `Immediate`：立即执行（默认）。- `MaintainTime`：可维护时间段执行。', examples=['Immediate枚举值：Immediate,MaintainTime,SpecifiedTime'])]) -> dict[str, Any]:
    req = {
        "instance_id": instance_id,
        "parameters": parameters,
        "schedule_type": schedule_type,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.modify_db_instance_parameters(req)
    return resp.to_dict()

@mcp_server.tool(
    description="查询可修改的参数列表"
)
def describe_modifiable_parameters(template_category: Annotated[str, Field(description='参数模板分类，默认值为 `DBEngine`。', examples=['DBEngine枚举值：DBEngine'])],
                                   template_type: Annotated[str, Field(description='参数模板的数据库类型，默认值为 `MySQL`。', examples=['MySQL枚举值：MySQL'])],
                                   template_type_version: Annotated[str, Field(description='参数模板适用的数据库引擎版本，取值范围：- `MySQL_5_7`：MySQL 5.7 版本。- `MySQL_8_0`：MySQL 8.0 版本。', examples=['MySQL_8_0枚举值：MySQL_5_7,MySQL_8_0'])]) -> dict[str, Any]:
    req = {
        "template_category": template_category,
        "template_type": template_type,
        "template_type_version": template_type_version,
    }
    req = {k: v for k, v in req.items() if v is not None}
    resp = vedbm_resource_sdk.describe_modifiable_parameters(req)
    return resp.to_dict()