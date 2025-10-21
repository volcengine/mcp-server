import os
import argparse
import logging
import json
import volcenginesdkcore 
import volcenginesdkdts
import volcenginesdkdts20180101 
from typing import Optional, Final, Any, List
from pydantic import Field
from mcp_server_dts.config import load_config
from mcp.server.fastmcp import FastMCP
from mcp_server_dts import model

openapi_cli = None
openapi_20180101_cli = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # filename="/tmp/mcp.dts.log"
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("DTS MCP Server", port=int(os.getenv("PORT", "8000")))

def main():
    parser = argparse.ArgumentParser(description="Run the DTS MCP Server")
    parser.add_argument("--config", "-c", help="Path to config file")  # 新增config参数
    parser.add_argument("--transport", "-t", choices=["streamable-http","stdio"], default="stdio")

    args = parser.parse_args()
    try:
        # 修改配置加载方式
        if args.config:
            config = load_config(args.config)
        else:
            config = load_config()
        logger.info(f"Initialized DTS Base Service, config={config}")

        # Initialize SDK
        configuration = volcenginesdkcore.Configuration()
        configuration.host = config.endpoint
        configuration.ak = config.access_key_id
        configuration.sk = config.access_key_secret
        configuration.region = config.region

        global openapi_cli, openapi_20180101_cli
        volcenginesdkcore.Configuration.set_default(configuration)
        openapi_cli = volcenginesdkdts.DTSApi()
        openapi_20180101_cli = volcenginesdkdts20180101.DTS20180101Api()

        # Run the MCP Server
        logger.info(
            f"Starting DTS MCP Server with {args.transport} transport"
        )
        mcp.run(transport=args.transport)

    except Exception as e:
        logger.error(f"Error starting DTS MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()

@mcp.tool(
    description="查询用户DTS迁移/订阅/同步任务列表（支持分页查询）,查询时需指定任务类型。根据任务名称查询任务时，支持模糊匹配，不支持正则表达式"
)
def describe_transmission_tasks(
    task_type: model.TaskType=Field(description="任务类型，可选值：DataMigration(数据迁移)、DataSubscription(数据订阅/订阅任务)、DataSynchronization(数据同步)、DataValidation(数据校验)"), 
    task_name: Optional[str]=Field(default=None, description="任务名称"),
    task_ids: Optional[List[str]]=Field(default=None, description="任务ID列表"),
    task_status: Optional[model.TaskStatus]=Field(default=None, description="任务状态"), 
    project: Optional[str]=Field(default=None, description="项目名称"),
    charge_type: Optional[model.ChargeType]=Field(default=None, description="计费类型"),
    page_number: int=Field(default= 1, description="分页页码"),  
    page_size: int=Field(default= 10, description="分页大小"),    
) -> dict[str, Any]:
    logger.info(f"Describe DTS tasks, task_type={task_type}, page_number={page_number}, page_size={page_size}")
    MAX_PAGE_SIZE: Final = 100
    page_size = min(page_size, MAX_PAGE_SIZE)

    req = volcenginesdkdts.models.DescribeTransmissionTasksRequest(
        task_type=task_type,
        name=task_name,
        task_status=task_status,
        ids=task_ids,
        project_name=project,
        charge_type=charge_type,
        page_number=page_number,
        page_size=page_size,
    )

    try:
        rsp = openapi_cli.describe_transmission_tasks(req)
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in describe_transmission_tasks: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""创建迁移/订阅/同步任务。
    Note: 创建时如果用户没有指定任务类型（迁移/订阅/同步），需询问用户创建的任务类型，如果是同步任务，需询问用户是单向同步还是双向同步，如果是双向同步,create_backward_sync_task参数设置为True。
    Note: 如果目的端是内置Kafka，需要询问用户VPC ID和VPC子网ID，在创建任务后调用modify_transmission_task修改任务配置。
    """
)
def create_transmission_task(
    task_type: model.TaskType=Field(description="任务类型，可选值：DataMigration(数据迁移)、DataSubscription(数据订阅)、DataSynchronization(数据同步)"),
    src_config: model.DataSource=Field(description="源端数据源配置"),
    dest_config: model.DataSource=Field(description="目的端数据源配置"),
    object_mappings: List[model.ObjectMapping]  = Field(description='''要迁移/订阅/同步的对象, 
                                          示例1: 整库选中, object_mappings 应该为 [ { "ObjectType": "Database", "SrcObjName": "database1", "DestObjName": "database1", "MappingList": [ { "ObjectType": "Table", "SrcObjName": "*", "DestObjName": "*" } ] } ];
                                          示例2: 选中库中部分表, object_mappings 应该为 [ { "ObjectType": "Database", "SrcObjName": "database1", "DestObjName": "database1", "MappingList": [ { "ObjectType": "Table", "SrcObjName": "tabl1", "DestObjName": "table1" }, { "ObjectType": "Table", "SrcObjName": "tabl2", "DestObjName": "table2" } ] } ]; 
                                          '''),
    task_name: str=Field(default='', description="任务名称"),
    create_backward_sync_task: bool=Field(default= False, description="是否创建反向同步任务"),
    traffic_spec: model.TrafficSpec=Field(default= model.TrafficSpec.standard, description="任务规格"),
    project_name: str=Field(default= "default", description="项目名称"),
) -> dict[str, Any]:
    logger.info(f"Create DTS transmission task")
    try:
        src_endpoint_type = src_config.endpoint_type
        dest_endpoint_type = dest_config.endpoint_type
        src_type_str = str(src_endpoint_type).lower()
        dest_type_str = str(dest_endpoint_type).lower()

        logger.info(f"src_endpoint_type={src_endpoint_type}, dest_endpoint_type={dest_endpoint_type}, object_mappings={object_mappings}")
        
        if "mysql" in src_type_str and "mysql" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.mysql2mysql,
                MySQL2MySQLSettings = model.MySQL2MySQLSettings(
                    MetaTransmissionSettings= model.MetaTransmissionSettings( 
                        EnableMeta = True,
                    ),
                    FullTransmissionSettings= model.FullTransmissionSettings(
                        EnableFull = True,
                    ), 
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    PolicyForPrimaryKeyConflict=model.PolicyForPrimaryKeyConflict.override,
                    ObjectMappings=object_mappings, 
                )
            ) 
        elif "mysql" in src_type_str and "elasticsearch" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.mysql2es,
                MySQL2ESSettings = model.MySQL2ESSettings(
                    MetaTransmissionSettings= model.MetaTransmissionSettings( 
                        EnableMeta = True,
                    ),
                    FullTransmissionSettings= model.FullTransmissionSettings(
                        EnableFull = True,
                    ), 
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    PolicyForPrimaryKeyConflict=model.PolicyForPrimaryKeyConflict.override,
                    ObjectMappings=object_mappings, 
                )
            ) 
        elif "mysql" in src_type_str and "kafka" in dest_type_str:
            vpc_id = dest_config.builtin_kafka_settings.vpc_id if dest_endpoint_type == model.EndpointType.builtin_kafka else None
            subnet_id = dest_config.builtin_kafka_settings.vpc_subnet_id if dest_endpoint_type == model.EndpointType.builtin_kafka else None
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.mysql2kafka,
                MySQL2KafkaSettings = model.MySQL2KafkaSettings(
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                    SubscriptionSettings=model.SubscriptionSettings(
                        Protocol=model.SubscriptionProtocol.volc,
                        PartitionPolicy=model.PartitionPolicy.table,
                        VPCId=vpc_id,
                        VPCSubnetId=subnet_id,
                    ),
                )
            )
        elif "mysql" in src_type_str and "rocketmq" in dest_type_str:
           solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.mysql2rocketmq,
                MySQL2RocketMQSettings = model.MySQL2RocketMQSettings(
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                    SubscriptionSettings=model.SubscriptionSettings(
                        Protocol=model.SubscriptionProtocol.volc,
                        PartitionPolicy=model.PartitionPolicy.table,
                    ),
                )
            )  
        elif "postgresql" in src_type_str and "postgresql" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.pg2pg,
                PG2PGSettings = model.PG2PGSettings(
                    MetaTransmissionSettings= model.MetaTransmissionSettings( 
                        EnableMeta = True,
                    ),
                    FullTransmissionSettings= model.FullTransmissionSettings(
                        EnableFull = True,
                    ), 
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                )
            ) 
        elif "postgresql" in src_type_str and "kafka" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.pg2kafka,
                PG2KafkaSettings = model.PG2KafkaSettings(
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                    SubscriptionSettings=model.SubscriptionSettings(
                        Protocol=model.SubscriptionProtocol.volc,
                        PartitionPolicy=model.PartitionPolicy.table,
                    ),
                )
            ) 
        elif "postgresql" in src_type_str and "rocketmq" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.pg2rocketmq,
                PG2RocketMQSettings = model.PG2RocketMQSettings(
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                    SubscriptionSettings=model.SubscriptionSettings(
                        Protocol=model.SubscriptionProtocol.volc,
                        PartitionPolicy=model.PartitionPolicy.table,
                    ),
                )
            ) 
        elif "mongo" in src_type_str and "mongo" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.mongo2mongo,
                Mongo2MongoSettings = model.Mongo2MongoSettings(
                    MetaTransmissionSettings= model.MetaTransmissionSettings( 
                        EnableMeta = True,
                    ),
                    FullTransmissionSettings= model.FullTransmissionSettings(
                        EnableFull = True,
                    ),
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    PolicyForMongoPrimaryKeyConflict=model.PolicyForMongoPrimaryKeyConflict.override,
                    ObjectMappings=object_mappings, 
                )
            ) 
        elif "mongo" in src_type_str and "rocketmq" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.mongo2rocketmq,
                Mongo2RocketMQSettings = model.Mongo2RocketMQSettings(
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                    SubscriptionSettings=model.SubscriptionSettings(
                        Protocol=model.SubscriptionProtocol.volc,
                        PartitionPolicy=model.PartitionPolicy.table,
                    ),
                )
            )    
        elif "redis" in src_type_str and "redis" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.redis2redis,
                Redis2RedisSettings = model.Redis2RedisSettings(
                    FullTransmissionSettings= model.FullTransmissionSettings(
                        EnableFull = True,
                    ),
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                )
            ) 
        elif "redis" in src_type_str and "rocketmq" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.redis2rocketmq,
                Redis2RocketMQSettings = model.Redis2RocketMQSettings(
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                    SubscriptionSettings=model.SubscriptionSettings(
                        Protocol=model.SubscriptionProtocol.volc,
                        PartitionPolicy=model.PartitionPolicy.table,
                    ),
                )
            ) 
        elif "mssql" in src_type_str and "mssql" in dest_type_str:
            solution_settings = model.SolutionSettings(
                SolutionType = model.SolutionType.mssql2mssql,
                MSSQL2MSSQLSettings = model.MSSQL2MSSQLSettings(
                    MetaTransmissionSettings= model.MetaTransmissionSettings( 
                        EnableMeta = True,
                    ),
                    FullTransmissionSettings= model.FullTransmissionSettings(
                        EnableFull = True,
                    ),
                    IncrTransmissionSettings= model.IncrTransmissionSettings(
                        EnableIncr = True,
                        Statements = [
                            model.Statement.stmt_ddl_all,
                            model.Statement.stmt_dml_insert,
                            model.Statement.stmt_dml_update,
                            model.Statement.stmt_dml_delete
                        ]
                    ),
                    ObjectMappings=object_mappings, 
                )
            ) 
        else:
            raise ValueError(f"不支持的数据源类型组合: {src_endpoint_type} -> {dest_endpoint_type}")

        charge_config_obj = volcenginesdkdts.models.ChargeConfigForCreateTransmissionTaskInput(charge_type=model.ChargeType.post_paid, one_step=True)
        req = volcenginesdkdts.models.CreateTransmissionTaskRequest(
            task_name=task_name,
            task_type=task_type,
            src_config=src_config.dict(exclude_none=True, by_alias=True),
            dest_config=dest_config.dict(exclude_none=True, by_alias=True),
            solution_settings=solution_settings.dict(exclude_none=True, by_alias=True),
            traffic_spec=traffic_spec,
            project_name=project_name,
            charge_config=charge_config_obj,
            create_backward_sync_task=create_backward_sync_task,
        )

        rsp = openapi_cli.create_transmission_task(req)
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in create_transmission_task: {str(e)}")
        return {"error": str(e)}

def get_subscription_settings(
        subscription_settings: Optional[model.SubscriptionSettings],
) -> model.SubscriptionSettings:
    if subscription_settings is None:
        return model.SubscriptionSettings(
            Protocol=model.SubscriptionProtocol.volc,
            PartitionPolicy=model.PartitionPolicy.table,
        )
    if subscription_settings.protocol is None:
        subscription_settings.protocol = model.SubscriptionProtocol.volc  
    if subscription_settings.partition_policy is None:
        subscription_settings.partition_policy = model.PartitionPolicy.table
    return subscription_settings

@mcp.tool(
    description="查询VPC列表，在创建源端/目的端是专网类型时，需要指定VPC和子网，可以调用该tool查询VPC列表",
)
def list_vpc() -> dict[str, Any]:
    try:
        rsp = openapi_20180101_cli.list_vpc(volcenginesdkdts20180101.models.ListVPCRequest())
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in list_vpc: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询VPC下的子网列表，在创建源端/目的端是专网类型时，需要指定VPC和子网，可以调用该tool查询VPC下的子网列表",
)
def list_vpc_subnets(vpc_id: str) -> dict[str, Any]:
    try:
        rsp = openapi_20180101_cli.list_vpc_subnets(volcenginesdkdts20180101.models.ListVPCSubnetsRequest(vpc_id=vpc_id))
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in list_vpc_subnets: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询 DTS 迁移/订阅/同步任务的详细信息，查询校验任务调用describe_validation_task_info"
)
def describe_transmission_task_info(
    task_id: str = Field(description="任务ID"),
) -> dict[str, Any]:
    logger.info(f"Describe DTS transmission task info")

    req = volcenginesdkdts.models.DescribeTransmissionTaskInfoRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.describe_transmission_task_info(req)
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in describe_transmission_task_info: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""查询传输任务的详细进度，如查询全量阶段各个表的同步进度，支持分别查询账号、结构、全量、增量阶段的传输进度
    NOTE: 如果用户没有明确指定进度类型，先通过describe_transmission_tasks根据任务ID查询任务当前处于哪个同步阶段（账号、结构、全量、增量），确定进度类型
    """
)
def describe_transmission_task_progress(
    task_id: str=Field(description="任务ID"),
    progress_type: model.ProgressType=Field(description="进度类型"),
    name: Optional[str]=Field(default=None, description="同步对象名称，不支持通配符。示例1：查询包含score的进度，name应为score；示例2：仅查询business库中score表的进度，name应为business.score"),
    transmission_state: Optional[model.TransmissionState]=Field(default=None, description="传输状态,可以筛选某个传输状态(如传输中)的进度信息"),
    object_type: Optional[model.ObjectType]=Field(default=None, description="同步对象类型"),
    latency_desc: bool=Field(default=False, description="是否按照表的延迟降序排列"),
    transfer_estimate_rows_desc: bool=Field(default=False, description="是否按照表的预估数据行数降序排列"),
    page_number: int = Field(default=1, description="页码"),
    page_size: int = Field(default=20, description="每页数量"),
) -> dict[str, Any]:
    logger.info(f"Describe DTS transmission task progress with task_id: {task_id}")

    req = volcenginesdkdts.models.DescribeTransmissionTaskProgressRequest(
        task_id=task_id,
        name=name,
        progress_type=progress_type,
        transmission_state=transmission_state,
        object_type=object_type,
        latency_desc=latency_desc,
        transfer_estimate_rows_desc=transfer_estimate_rows_desc,
        page_number=page_number,
        page_size=page_size,
    )

    try:
        rsp = openapi_cli.describe_transmission_task_progress(req)
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in describe_transmission_task_progress: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""修改传输/订阅/同步任务
    Note: 在调用该tool前，需要先调用describe_transmission_task_info获取任务的详细信息，根据用户要求修改请求
    Note: describe_transmission_task_info返回的任务源端和目的端密码做了脱敏处理，如果任务状态是Init，修改任务时需要回填密码
    Note: 修改任务后立即生效，不用重新启动任务
    """
)
def modify_transmission_task(
    task_id: str,
    src_config: model.DataSource=Field(description="源端数据源配置，字段需符合DataSource alias名称要求"),
    dest_config: model.DataSource=Field(description="目的端数据源配置，字段需符合DataSource alias名称要求"), 
    solution_settings: model.SolutionSettings=Field(description="解决方案配置"),
    task_name: Optional[str]=Field(default=None, description="任务名称"),
    traffic_spec: Optional[model.TrafficSpec]=Field(default=None, description="任务规格"),
) -> str:
    logger.info(f"Modify DTS transmission task with task_id: {task_id}")
    if src_config.endpoint_type is None or dest_config.endpoint_type is None:
        return "src_config or dest_config format is invalid"

    req = volcenginesdkdts.models.ModifyTransmissionTaskRequest(
        task_id=task_id,
        task_name=task_name,
        src_config=src_config.dict(exclude_none=True, by_alias=True),
        dest_config=dest_config.dict(exclude_none=True, by_alias=True),
        solution_settings=solution_settings.dict(exclude_none=True, by_alias=True),
        traffic_spec=traffic_spec,
    )

    try:
        rsp = openapi_cli.modify_transmission_task(req)
        return json.dumps(rsp) 
    
    except Exception as e:
        logger.error(f"Error in modify_transmission_task: {str(e)}")
        return str(e)

@mcp.tool(
    description="启动传输任务，启动校验任务使用start_validation_task"
)
def start_transmission_task(
    task_id: str
) -> dict[str, Any]:
    """Start a DTS transmission task.

    Args:
        task_id: The ID of the DTS transmission task to start.
    """
    logger.info(f"Start DTS transmission task with task_id: {task_id}")

    req = volcenginesdkdts.models.StartTransmissionTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.start_transmission_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in start_transmission_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="暂停迁移/同步/订阅任务，暂停校验任务使用suspend_vildation_task"
)
def suspend_transmission_task(
    task_id: str
) -> dict[str, Any]:
    logger.info(f"Suspend DTS transmission task with task_id: {task_id}")

    req = volcenginesdkdts.models.SuspendTransmissionTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.suspend_transmission_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in suspend_transmission_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="恢复传输任务，任务暂停后可以通过该tool恢复任务。恢复校验任务使用resume_validation_task"
)
def resume_transmission_task(
    task_id: str = Field(description="任务ID")
) -> dict[str, Any]:
    logger.info(f"Resume DTS transmission task with task_id: {task_id}")

    req = volcenginesdkdts.models.ResumeTransmissionTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.resume_transmission_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in resume_transmission_task: {str(e)}")
        return {"error": str(e)}
        
@mcp.tool(
    description="重试迁移/同步/订阅任务，重试校验任务使用retry_validation_task"
)
def retry_transmission_task(
    task_id: str = Field(description="任务ID")
) -> dict[str, Any]:
    logger.info(f"Retry DTS transmission task with task_id: {task_id}")

    req = volcenginesdkdts.models.RetryTransmissionTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.retry_transmission_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in retry_transmission_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="批量启动迁移/同步/订阅任务"
)
def start_transmission_tasks(
    task_ids: list[str]
) -> dict[str, Any]:
    logger.info(f"Start DTS transmission tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.StartTransmissionTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.start_transmission_tasks(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in start_transmission_tasks: {str(e)}")
        return {"error": str(e)}
    
@mcp.tool(
    description="批量暂停迁移/同步/订阅任务"
)
def suspend_transmission_tasks(
    task_ids: list[str]
) -> dict[str, Any]:
    logger.info(f"Suspend DTS transmission tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.SuspendTransmissionTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.suspend_transmission_tasks(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in suspend_transmission_tasks: {str(e)}")
        return {"error": str(e)}
    
@mcp.tool(
    description="批量恢复迁移/同步/订阅任务"
)
def resume_transmission_tasks(
    task_ids: list[str]
) -> dict[str, Any]:
    logger.info(f"Resume DTS transmission tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.ResumeTransmissionTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.resume_transmission_tasks(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in resume_transmission_tasks: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="批量重试迁移/同步/订阅任务"
)
def retry_transmission_tasks(
    task_ids: list[str]
) -> str:
    logger.info(f"Retry DTS transmission tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.RetryTransmissionTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.retry_transmission_tasks(req)
        return json.dumps(rsp)
    except Exception as e:
        logger.error(f"Error in retry_transmission_tasks: {str(e)}")
        return str(e)

@mcp.tool(
        description="配置任务多泳道，支持配置表级别泳道，将延迟表拆分到独立泳道进行同步，降低整体延迟。"
)
def spawn_swimming_lane(
    task_id: str = Field(description="任务ID"),
    database: str = Field(description="数据库名称"),
    tables: list[str] = Field(description="表名称列表"),
) -> dict[str, Any]:
    logger.info(f"Spawn swimming lane for DTS transmission task with task_id: {task_id}, database: {database}, tables: {tables}")
    req = volcenginesdkdts.models.SpawnSwimmingLaneRequest(
        task_id=task_id,
        database=database,
        tables=tables
    )
    try:
        rsp = openapi_cli.spawn_swimming_lane(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in spawn_swimming_lane: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="创建订阅任务消费组，仅支持目的端是内置Kafka的订阅任务"
)
def create_subscription_group(
    task_id: str = Field(description="任务ID"),
    group_name: str = Field(description="消费组名称"),
    username: str = Field(description="用户名"),
    password: str = Field(description="密码"),
) -> dict[str, Any]:
    logger.info(f"Create subscription group for DTS transmission task with task_id: {task_id}, group_name: {group_name}, username: {username}, password: {password}")
    req = volcenginesdkdts.models.CreateSubscriptionGroupRequest(
        task_id=task_id,
        group_name=group_name,
        username=username,
        password=password
    )
    try:
        rsp = openapi_cli.create_subscription_group(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in create_subscription_group: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询订阅任务消费组列表，仅支持目的端是内置Kafka的订阅任务"
)
def describe_subscription_groups(
    task_id: str = Field(description="任务ID")
) -> dict[str, Any]:
    logger.info(f"Describe subscription groups for DTS transmission task with task_id: {task_id}")
    req = volcenginesdkdts.models.DescribeSubscriptionGroupsRequest(
        task_id=task_id
    )
    try:
        rsp = openapi_cli.describe_subscription_groups(req)
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in describe_subscription_groups: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="更新订阅任务消费组，仅支持目的端是内置Kafka的订阅任务"
)
def update_subscription_group(
    task_id: str = Field(description="任务ID"),
    group_name: str = Field(description="消费组名称"),
    username: str = Field(description="用户名"),
    password: str = Field(description="密码"),
) -> dict[str, Any]:
    logger.info(f"Update subscription group for DTS transmission task with task_id: {task_id}, group_name: {group_name}, username: {username}, password: {password}")
    req = volcenginesdkdts.models.UpdateSubscriptionGroupRequest(
        task_id=task_id,
        group_name=group_name,
        username=username,
        password=password
    )
    try:
        rsp = openapi_cli.update_subscription_group(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in update_subscription_group: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
        description="""创建预检查任务，创建后会返回预检查ID，根据预检查ID查询预检查结果"""
)
def precheck_async(
    task_id: str = Field(description="任务ID"),
) -> dict[str, Any]:
    logger.info(f"Precheck DTS transmission task with task_id: {task_id}")
    req = volcenginesdkdts20180101.models.PreCheckAsyncRequest(
        task_id=task_id,
    )
    try:
        rsp = openapi_20180101_cli.pre_check_async(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in precheck_async: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""根据预检查ID查询预检查结果，预检查ID为precheck_async接口返回的预检查ID"""
)
def get_async_pre_check_result(
    precheck_id: str = Field(description="预检查ID"),
) -> dict[str, Any]:
    logger.info(f"Get async pre check result for DTS transmission task with precheck_id: {precheck_id}")
    req = volcenginesdkdts20180101.models.GetAsyncPreCheckResultRequest(
        id=precheck_id,
    )
    try:
        rsp = openapi_20180101_cli.get_async_pre_check_result(req)
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in get_async_pre_check_result: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""绑定标签到DTS任务"""
)
def add_tags_to_resource(
    task_ids: list[str] = Field(description="任务ID列表"),
    tags: list[model.TagObject] = Field(description="标签列表"),
) -> str:
    logger.info(f"Add tags to DTS transmission task with task_ids: {task_ids}, tags: {tags}")
    req = volcenginesdkdts.models.AddTagsToResourceRequest(
        resource_type="Task",
        task_ids=task_ids,
        tags=[tag.dict(exclude_none=True, by_alias=True) for tag in tags],
    )
    try:
        rsp = openapi_cli.add_tags_to_resource(req)
        return json.dumps(rsp)
    except Exception as e:
        logger.error(f"Error in add_tags_to_resource: {str(e)}")
        return str(e)
    
@mcp.tool(
    description="""解绑DTS任务的标签"""
)
def remove_tags_from_resource(
    task_ids: list[str] = Field(description="任务ID列表"),
    tag_keys: list[str] = Field(description="标签键列表"),
) -> str:
    logger.info(f"Remove tags from DTS transmission task with task_ids: {task_ids}, tag_keys: {tag_keys}")
    req = volcenginesdkdts.models.RemoveTagsFromResourceRequest(
        task_ids=task_ids,
        tag_keys=tag_keys,
    )
    try:
        rsp = openapi_cli.remove_tags_from_resource(req)
        return json.dumps(rsp)
    except Exception as e:
        logger.error(f"Error in remove_tags_from_resource: {str(e)}")
        return str(e)

@mcp.tool(
    description="""查询DTS任务的标签"""
)
def describe_tags_by_resource(
    task_ids: list[str] = Field(description="任务ID列表"),
    tag_filters: Optional[list[model.TagFilterObject]] = Field(default=None, description="标签过滤列表"),
    page_number: int=Field(default= 1, description="分页页码"),  
    page_size: int=Field(default= 10, description="分页大小"), 
) -> dict[str, Any]:
    logger.info(f"Describe tags by DTS transmission task with task_ids: {task_ids}")
    req = volcenginesdkdts.models.DescribeTagsByResourceRequest(
        task_ids=task_ids,
        tag_filters=tag_filters,
        page_number=page_number,
        page_size=page_size,
    )
    try:
        rsp = openapi_cli.describe_tags_by_resource(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in describe_tags_by_resource: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""将任务计费类型由按量计费转为包年包月计费；或修改DTS任务规格（仅迁移任务和同步任务支持）
    Note:在调用该tool修改任务规格前，需要先调用escribe_transmission_task_info获取当前规格，如果不同才需要修改
    Note：在调用该tool修改任务计费类型为包年包月前，需要先查询任务详情获取当前计费类型，如果是按量计费才允许修改
    """
)
def modify_instance_order(
    task_id: str = Field(description="任务ID"),
    convert_post_paid_to_pre_paid: Optional[model.ConvertPostPaidToPrePaid] = Field(default=None, description="是否将按量计费转为包年包月计费"),
    modify_instance_spec: Optional[model.ModifyInstanceSpec] = Field(default=None, description="修改实例规格"),
) -> dict[str, Any]:
    logger.info(f"Modify DTS transmission task order with task_id: {task_id}, convert_post_paid_to_pre_paid: {convert_post_paid_to_pre_paid}, modify_instance_spec: {modify_instance_spec}")
    req = volcenginesdkdts.models.ModifyInstanceOrderRequest(
        task_id=task_id,
        convert_post_paid_to_pre_paid=convert_post_paid_to_pre_paid.dict(exclude_none=True, by_alias=True) if convert_post_paid_to_pre_paid else None,
        modify_instance_spec=modify_instance_spec.dict(exclude_none=True, by_alias=True) if modify_instance_spec else None,
        one_step=True,
    )
    try:
        rsp = openapi_cli.modify_instance_order(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in modify_instance_order: {str(e)}")
        return {"error": str(e)}


@mcp.tool(
    description="""创建DTS校验任务"""
)
def create_validation_task(
    parent_task_id: str = Field(description="校验任务关联的父任务ID"),
    solution_type: model.SolutionType = Field(description="校验任务解决方案类型"),
    object_mappings: List[model.ObjectMapping]  = Field(description='''要校验的对象, 
                                          示例1: 整库选中, object_mappings 应该为 [ { "ObjectType": "Database", "SrcObjName": "database1", "DestObjName": "database1", "MappingList": [ { "ObjectType": "Table", "SrcObjName": "*", "DestObjName": "*" } ] } ];
                                          示例2: 选中库中部分表, object_mappings 应该为 [ { "ObjectType": "Database", "SrcObjName": "database1", "DestObjName": "database1", "MappingList": [ { "ObjectType": "Table", "SrcObjName": "tabl1", "DestObjName": "table1" }, { "ObjectType": "Table", "SrcObjName": "tabl2", "DestObjName": "table2" } ] } ]; 
                                          '''),
    task_name: str=Field(default='', description="任务名称"),
    sample_rate: int=Field(default=100, description="全量校验任务采样率"),
) -> dict[str, Any]:
    default_error_behavior_settings = model.ErrorBehaviorSettings(
        MaxRetrySeconds=600,
    )
    default_validation_settings = model.ValidationSettings(
        ParallelNum=8,
    )
    match solution_type:
        case model.SolutionType.mysql2mysql_rowcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                MySQL2MySQLRowCompareSettings = model.MySQL2MySQLRowCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                    SampleRate=sample_rate,
                    ValidationSettings=default_validation_settings,
                )
            ) 
        case model.SolutionType.mysql2mysql_incrdatavalidation:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                MySQL2MySQLIncrDataValidationSettings = model.MySQL2MySQLIncrDataValidationSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                )
            ) 
        case model.SolutionType.mysql2mysql_rowcountcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                MySQL2MySQLRowCountCompareSettings = model.MySQL2MySQLRowCountCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                )
            ) 
        case model.SolutionType.mysql2mysql_metacompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                MySQL2MySQLSettings = model.MySQL2MySQLMetaCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                )
            ) 
        case model.SolutionType.pg2pg_rowcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                PG2PGRowCompareSettings = model.PG2PGRowCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                    ValidationSettings=default_validation_settings,
                )
            )
        case model.SolutionType.mongo2mongo_rowcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                Mongo2MongoRowCompareSettings = model.Mongo2MongoRowCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                    ValidationSettings=default_validation_settings,
                )
            ) 
        case model.SolutionType.mongo2mongo_pkcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                Mongo2MongoPkCompareSettings = model.Mongo2MongoPkCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                )
            ) 
        case model.SolutionType.mongo2mongo_incrdatavalidation:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                Mongo2MongoIncrDataValidationSettings = model.Mongo2MongoIncrDataValidationSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                )
            ) 
        case model.SolutionType.mongo2mongo_rowcountcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                Mongo2MongoRowCountCompareSettings = model.Mongo2MongoRowCountCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                )
            ) 
        case model.SolutionType.redis2redis_rowcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                Redis2RedisRowCompareSettings = model.Redis2RedisRowCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                    ValidationSettings=default_validation_settings,
                )
            ) 
        case model.SolutionType.mssql2mssql_rowcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                MSSQL2MSSQLRowCompareSettings = model.MSSQL2MSSQLRowCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                    SampleRate=sample_rate,
                    ValidationSettings=default_validation_settings,
                )
            ) 
        case model.SolutionType.mssql2mssql_rowcountcompare:
            solution_settings = model.SolutionSettings(
                SolutionType = solution_type,
                MSSQL2MSSQLRowCountCompareSettings = model.MSSQL2MSSQLRowCountCompareSettings(
                    ObjectMappings=object_mappings, 
                    ErrorBehaviorSettings=default_error_behavior_settings,
                )
            ) 
        case _:
            raise ValueError(f"Unsupported solution type: {solution_type}")
       
    charge_config_obj = volcenginesdkdts.models.ChargeConfigForCreateTransmissionTaskInput(charge_type=model.ChargeType.post_paid, one_step=True) 
    req = volcenginesdkdts.models.CreateValidationTaskRequest(
        task_type=model.TaskType.data_validation,
        parent_task_id=parent_task_id,
        task_name=task_name,
        charge_config=charge_config_obj,
        solution_settings=solution_settings.dict(exclude_none=True, by_alias=True),
        
    )
    try:
        rsp = openapi_cli.create_validation_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in create_validation_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询用户DTS校验任务列表（支持分页查询）,查询时需指定任务类型。根据任务名称查询任务时，支持模糊匹配，不支持正则表达式"
)
def describe_validation_tasks(
    name: Optional[str]=Field(default=None, description="任务名称/任务ID"),
    task_status: Optional[model.TaskStatus]=Field(default=None, description="任务状态"), 
    task_sub_type: Optional[model.TaskSubType]=Field(default=None, description="任务子类型"),
    validation_status: Optional[model.ValidationStatus]=Field(default=None, description="校验结果"),
    page_number: int=Field(default= 1, description="分页页码"),  
    page_size: int=Field(default= 10, description="分页大小"),    
) -> dict[str, Any]:
    MAX_PAGE_SIZE: Final = 100
    page_size = min(page_size, MAX_PAGE_SIZE)

    req = volcenginesdkdts.models.DescribeValidationTasksRequest(
        task_type=model.TaskType.data_validation,
        name=name,
        task_status=task_status,
        task_sub_type=task_sub_type,
        validation_status=validation_status,
        page_number=page_number,
        page_size=page_size,
    )

    try:
        rsp = openapi_cli.describe_validation_tasks(req)
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in describe_validation_tasks: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询 DTS 校验任务的详细信息"
)
def describe_validation_task_info(
    task_id: str = Field(description="校验任务ID"),
) -> dict[str, Any]:
    req = volcenginesdkdts.models.DescribeValidationTaskInfoRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.describe_validation_task_info(req)
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in describe_validation_task_info: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="启动校验任务"
)
def start_validation_task(
    task_id: str = Field(description="校验任务ID")
) -> dict[str, Any]:
    logger.info(f"Start DTS transmission task with task_id: {task_id}")

    req = volcenginesdkdts.models.StartValidationTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.start_validation_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in start_validation_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="暂停校验任务"
)
def suspend_validation_task(
    task_id: str = Field(description="校验任务ID")
) -> dict[str, Any]:
    logger.info(f"Suspend DTS validation task with task_id: {task_id}")

    req = volcenginesdkdts.models.SuspendValidationTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.suspend_validation_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in suspend_transmission_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="恢复校验任务，任务暂停后可以通过该tool恢复任务"
)
def resume_validation_task(
    task_id: str = Field(description="校验任务ID")
) -> dict[str, Any]:
    logger.info(f"Resume DTS validation task with task_id: {task_id}")

    req = volcenginesdkdts.models.ResumeValidationTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.resume_validation_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in resume_validation_task: {str(e)}")
        return {"error": str(e)}
        
@mcp.tool(
    description="重试校验任务"
)
def retry_validation_task(
    task_id: str = Field(description="校验任务ID")
) -> dict[str, Any]:
    logger.info(f"Retry DTS validation task with task_id: {task_id}")

    req = volcenginesdkdts.models.RetryValidationTaskRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.retry_validation_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in retry_validation_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="批量启动校验任务"
)
def start_validation_tasks(
    task_ids: list[str]
) -> dict[str, Any]:
    logger.info(f"Start DTS validation tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.StartValidationTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.start_validation_tasks(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in start_validation_tasks: {str(e)}")
        return {"error": str(e)}
    
@mcp.tool(
    description="批量暂停校验任务"
)
def suspend_validation_tasks(
    task_ids: list[str]
) -> dict[str, Any]:
    logger.info(f"Suspend DTS validation tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.SuspendValidationTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.suspend_validation_tasks(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in suspend_validation_tasks: {str(e)}")
        return {"error": str(e)}
    
@mcp.tool(
    description="批量恢复校验任务"
)
def resume_validation_tasks(
    task_ids: list[str]
) -> dict[str, Any]:
    logger.info(f"Resume DTS validation tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.ResumeValidationTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.resume_validation_tasks(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    except Exception as e:
        logger.error(f"Error in resume_validation_tasks: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="批量重试校验任务"
)
def retry_validation_tasks(
    task_ids: list[str]
) -> str:
    logger.info(f"Retry DTS validation tasks with task_ids: {task_ids}")
    req = volcenginesdkdts.models.RetryValidationTasksRequest(
        task_ids=task_ids
    )
    try:
        rsp = openapi_cli.retry_validation_tasks(req)
        return json.dumps(rsp)
    except Exception as e:
        logger.error(f"Error in retry_validation_tasks: {str(e)}")
        return str(e)

@mcp.tool(
    description="下载校验结果"
)
def download_validation_task_result(
    task_id: str = Field(description="校验任务ID")
) -> dict[str, Any]:
    logger.info(f"Download DTS validation task result with task_id: {task_id}")

    req = volcenginesdkdts.models.DownloadValidationTaskResultRequest(
        task_id=task_id
    )

    try:
        rsp = openapi_cli.download_validation_task_result(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in download_validation_task_result: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询校验任务结果"
)
def describe_validation_task_result(
    task_id: str = Field(description="校验任务ID"),
    page_number: int = Field(description="分页页码", default=1),
    page_size: int = Field(description="分页大小", default=10)
) -> dict[str, Any]:
    logger.info(f"Describe DTS validation task result with task_id: {task_id}")

    req = volcenginesdkdts.models.DescribeValidationTaskResultRequest(
        task_id=task_id,
        page_number=page_number,
        page_size=page_size
    )

    try:
        rsp = openapi_cli.describe_validation_task_result(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in describe_validation_task_result: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询增量校验任务库表不一致详情"
)
def get_db_table_diff_details(
    task_id: str = Field(description="校验任务ID"),
    db_name: str = Field(description="数据库名"),
    table_name: str = Field(description="表名"),
    page_number: int = Field(description="分页页码", default=1),
    page_size: int = Field(description="分页大小", default=10)
) -> dict[str, Any]:
    req = volcenginesdkdts.models.GetDBTableDiffDetailsRequest(
        task_id=task_id,
        page_number=page_number,
        page_size=page_size,
        db=db_name,
        table=table_name
    )

    try:
        rsp = openapi_cli.get_db_table_diff_details(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in get_db_table_diff_details: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="增量校验任务生成校验结果文件"
)
def generate_validation_result_file(
    task_id: str = Field(description="校验任务ID"),
) -> str:
    logger.info(f"Generate DTS validation task result file with task_id: {task_id}")
    req = volcenginesdkdts.models.GenerateValidationResultFileRequest(
        task_id=task_id,
    )

    try:
        rsp = openapi_cli.generate_validation_result_file(req)
        return json.dumps(rsp) 
    
    except Exception as e:
        logger.error(f"Error in generate_validation_result_file: {str(e)}")
        return str(e)

@mcp.tool(
    description="""查询任务支持的校验任务类型
    Note: 在调用该tool前，需要先调用describe_transmission_task_info获取任务的详细信息，传入describe_transmission_task_info的返回值中的源端和目的端数据源信息
    """
)
def describe_supported_validation_types(
    src_datasource: model.DataSource = Field(description="源端数据源信息,字段需符合DataSource alias名称要求"),
    dst_datasource: model.DataSource = Field(description="目的端数据源信息,字段需符合DataSource alias名称要求"),
) -> dict[str, Any]:
    logger.info(f"Describe supported validation types with src_datasource: {src_datasource}, dst_datasource: {dst_datasource}")
    if src_datasource.endpoint_type is None or dst_datasource.endpoint_type is None:
        return {"error": "endpoint type of datasource must be specified"}
    req = volcenginesdkdts.models.DescribeSupportedValidationTypesRequest(
        src_data_source=src_datasource.dict(exclude_none=True, by_alias=True),
        dest_data_source=dst_datasource.dict(exclude_none=True, by_alias=True), 
    )

    try:
        rsp = openapi_cli.describe_supported_validation_types(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in generate_validation_result_file: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""修改校验任务
    Note: 在调用该tool前，需要先调用describe_validation_task_info获取任务的详细信息，根据用户要求修改请求，对于没有改变的请求部分，传入describe_validation_task_info的返回值
    Note: 修改任务后立即生效，不用重新启动任务"""
)   
def modify_validation_task(
    task_id: str = Field(description="校验任务ID"),
    solution_settings: model.SolutionSettings=Field(description="解决方案配置"),
) -> dict[str, Any]:
    logger.info(f"Update DTS validation task with task_id: {task_id}")

    req = volcenginesdkdts.models.ModifyValidationTaskRequest(
        task_id=task_id,
        solution_settings=solution_settings.dict(exclude_none=True, by_alias=True),
    )

    try:
        rsp = openapi_cli.modify_validation_task(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in modify_validation_task: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="创建数据源"
)
def create_data_source(
    name: str = Field(description="数据源名称"),
    data_source: model.DataSource = Field(description="数据源配置")
) -> dict[str, Any]:
    logger.info(f"Create DTS data source with name: {name}, data_source: {data_source}")
    data_source.name = name
    req = volcenginesdkdts.models.CreateDataSourceRequest(
        data_source=data_source.dict(exclude_none=True, by_alias=True),
    )

    try:
        rsp = openapi_cli.create_data_source(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in create_data_source: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="查询数据源列表"
)
def list_data_source(
    categories: Optional[list[model.DataSourceCategory]] = Field(default=None, description="数据源类型列表"),
    endpoint_types: Optional[list[model.EndpointType]] = Field(default=None, description="数据源接入方式列表"),
    name_prefix: Optional[str] = Field(default=None, description="数据源名称前缀"),
    order_by: Optional[model.ListDataSourceOrderBy] = Field(default=model.ListDataSourceOrderBy.order_by_create_time_desc, description="排序规则"),
    page_size: Optional[int] = Field(default=10, description="每页数量"),
    page_number: Optional[int] = Field(default=1, description="页码"),
) -> dict[str, Any]:
    logger.info(f"List DTS data source with categories: {categories}, endpoint_types: {endpoint_types}, name_prefix: {name_prefix}, order_by: {order_by}, page_size: {page_size}, page_number: {page_number}")

    req = volcenginesdkdts.models.ListDataSourceRequest(
        categories=categories,
        endpoint_types=endpoint_types,
        name_prefix=name_prefix,
        order_by=order_by,
        page_size=page_size,
        page_num=page_number,
    )

    try:
        rsp = openapi_cli.list_data_source(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in list_data_source: {str(e)}")
        return {"error": str(e)}
    
@mcp.tool(
    description="查询数据源详情"
)
def describe_data_source(
    data_source_id: str = Field(description="数据源ID"),
) -> dict[str, Any]:
    logger.info(f"Describe DTS data source with data_source_id: {data_source_id}")

    req = volcenginesdkdts.models.DescribeDataSourceRequest(
        data_source_id=data_source_id,
    )

    try:
        rsp = openapi_cli.describe_data_source(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in describe_data_source: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="""修改数据源信息
    Note: 在调用该tool前，需要先调用describe_data_source获取数据源的详细信息，根据用户要求修改请求，对于没有改变的请求部分，传入describe_data_source的返回值"""
)
def modify_data_source(
    data_source_id: str = Field(description="数据源ID"),
    data_source: model.DataSource = Field(description="数据源配置")
) -> dict[str, Any]:
    logger.info(f"Modify DTS data source with data_source_id: {data_source_id}")
    data_source.datasource_id = data_source_id 
    req = volcenginesdkdts.models.ModifyDataSourceRequest(
        data_source_id=data_source_id,
        data_source=data_source.dict(exclude_none=True, by_alias=True),
    )

    try:
        rsp = openapi_cli.modify_data_source(req)
        if rsp is None:
            return {}
        return rsp.to_dict()
    
    except Exception as e:
        logger.error(f"Error in modify_data_source: {str(e)}")
        return {"error": str(e)}

@mcp.tool(
    description="删除数据源"
)
def delete_data_source(
    data_source_id: str = Field(description="数据源ID"),
) -> str:
    logger.info(f"Delete DTS data source with data_source_id: {data_source_id}")
    req = volcenginesdkdts.models.DeleteDataSourceRequest(
        data_source_id=data_source_id,
    )

    try:
        rsp = openapi_cli.delete_data_source(req)
        return json.dumps(rsp)
    
    except Exception as e:
        logger.error(f"Error in delete_data_source: {str(e)}")
        return str(e)