from __future__ import annotations
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class ChargeType(str, Enum):
    post_paid = "PostPaid" # 按量计费
    pre_paid = "PrePaid" # 包年包月

class TrafficSpec(str, Enum):
    compact = "Compact" # 紧凑规格
    standard = "Standard" # 标准规格

class PreOrderType(str, Enum):
    new = "New"
    modify = "Modify"

class ObjectType(str, Enum):
    database = "Database"   # 数据库
    table = "Table"   # 表
    view = "View"   # 视图
    column = "Column"   # 列
    function = "Function"   # 函数
    procedure = "Procedure"   # 存储过程
    trigger = "Trigger"   # 触发器
    type = "Type"   # 类型(PG)
    domain = "Domain"   # 域
    sequence = "Sequence"   # 序列
    rule = "Rule"   # 规则
    operator = "Operator"   # 运算符
    aggregate = "Aggregate"   # 聚合函数
    extension = "Extension"   # 扩展
    constraint = "Constraint"   # 约束
    postsequence = "PostSequence"   # 后置序列
    schema = "Schema"   # 模式
    event = "Event"   # 事件
    domainconstraint = "DomainConstraint"   # 域约束

class SolutionType(str, Enum):
    mysql2mysql = "MySQL2MySQL" # MySQL到MySQL传输类型
    mysql2es = "MySQL2ES" # MySQL到ES传输类型
    mysql2kafka = "MySQL2Kafka" # MySQL到Kafka传输类型
    mysql2rocketmq = "MySQL2RocketMQ" # MySQL到RocketMQ传输类型
    pg2pg = "PG2PG" # PostgreSQL到PostgreSQL传输类型
    pg2kafka = "PG2Kafka" # PostgreSQL到Kafka传输类型
    pg2rocketmq = "PG2RocketMQ" # PostgreSQL到RocketMQ传输类型
    mongo2mongo = "Mongo2Mongo" # MongoDB到MongoDB传输类型
    redis2redis = "Redis2Redis" # Redis到Redis传输类型 
    mongo2rocketmq = "Mongo2RocketMQ" # MongoDB到RocketMQ传输类型
    redis2rocketmq = "Redis2RocketMQ" # Redis到RocketMQ传输类型
    mssql2mssql = "MSSQL2MSSQL" # SQLServer到SQLServer传输类型
    mysql2mysql_rowcompare = "MySQL2MySQLRowCompare" # MySQL全量校验
    mysql2mysql_incrdatavalidation = "MySQL2MySQLIncrDataValidation" # MySQL增量校验 
    mysql2mysql_metacompare = "MySQL2MySQLMetaCompare" # MySQL结构校验
    mysql2mysql_rowcountcompare = "MySQL2MySQLRowCountCompare" # MySQL行数校验
    pg2pg_rowcompare = "PG2PGRowCompare" # PG全量校验
    mongo2mongo_rowcompare = "Mongo2MongoRowCompare" # Mongo全量校验
    mongo2mongo_pkcompare = "Mongo2MongoPkCompare" # Mongo主键校验
    mongo2mongo_incrdatavalidation = "Mongo2MongoIncrDataValidation" # Mongo增量校验
    mongo2mongo_rowcountcompare = "Mongo2MongoRowCountCompare" # Mongo行数校验
    redis2redis_rowcompare = "Redis2RedisRowCompare" # Redis全量校验
    mssql2mssql_rowcompare = "MSSQL2MSSQLRowCompare" # MSSQL全量校验
    mssql2mssql_rowcountcompare = "MSSQL2MSSQLRowCountCompare" # MSSQL行数校验


class ChargeStatus(str, Enum):
    init = "Init"
    normal = "Normal"
    overdue = "Overdue"
    unpaid = "Unpaid"
    closed = "Closed"

class ProgressType(str, Enum):
    account = "Account"  # 账号同步进度
    meta = "Meta"  # 结构同步进度
    full = "Full"  # 全量同步进度
    incr = "Incr"  # 增量同步进度
    post_meta = "PostMeta"  # 后置结构同步进度

class TransmissionState(str, Enum):
    none = "None"
    transmitting =  "Transmitting"  # 传输中
    completed = "Completed"  # 已完成
    removed = "Removed"  # 已移除，表示该对象已不再同步范围中

class ObjectTransType(str, Enum):
    meta = "Meta"
    full = "Full"
    incr = "Incr"

class MigrationType(str, Enum):
    logical = "Logical"
    physical = "Physical"
    physical_logical = "PhysicalLogical"

class UploadMethod(str, Enum):
    auto = "Auto"
    manual = "Manual"

class TablePolicyForPrimaryKeyConflict(str, Enum):
    table_throw_error = "TableThrowError"
    table_ignore = "TableIgnore"
    table_override = "TableOverride"

class PolicyForMongoPrimaryKeyConflict(str, Enum):
    override = "Override"
    last_write_win = "LastWriteWin"
    ignore = "Ignore"

class MongoTransferDDLScope(str, Enum):
    ddl_all = "DDLAll"
    ddl_index = "DDLIndex"
    ddl_none = "DDLNone"

class MongoConflictRecordMode(str, Enum):
    local = "Local"
    remote = "Remote"

class SynchronizeType(str, Enum):
    dml_insert = "DMLInsert"
    dml_update = "DMLUpdate"
    dml_delete = "DMLDelete"
    ddl = "DDL"

class MetaType(str, Enum):
    table = "Table"
    view = "View"
    procedure = "Procedure"
    function = "Function"
    trigger = "Trigger"
    type = "Type"
    domain = "Domain"
    sequence = "Sequence"
    rule = "Rule"
    operator = "Operator"
    aggregate = "Aggregate"
    extension = "Extension"
    constraint = "Constraint"
    postsequence = "PostSequence"
    schema = "Schema"
    events = "Events"

class ESNameRule(str, Enum):
    table = "Table"  # 表名
    db_and_table = "DBAndTable"  # 数据库名+表名

class InsertMode(str, Enum):
    replace = "Replace"  # 覆盖
    update = "Update"  # 更新

class FilterType(str, Enum):
    server_filter = "ServerFilter"
    regex_filter = "RegexFilter"

class ChargeConfig(BaseModel):
    charge_type: Optional['ChargeType'] = Field(default=None, description="计费类型")
    times: Optional[int] = Field(default=1, description="包月数，仅预付费计费类型下生效")
    one_step: Optional[bool] = Field(default=True, description="是否单步订单，即创建任务时同时创建订单")

class MongoDeployType(str, Enum):
    standalone = "Standalone"   # 单节点
    replicaset = "ReplicaSet"   # 副本集
    shardedcluster = "ShardedCluster"   # 分片集群

class MongoIncrPullMethod(str, Enum):
    changestream = "ChangeStream"
    oplog = "Oplog"

class TaskType(str, Enum):
    """任务类型,包含数据迁移、数据订阅、数据同步"""
    data_migration = "DataMigration"  # 数据迁移 
    data_subscription = "DataSubscription"  # 数据订阅
    data_synchronization = "DataSynchronization"  # 数据同步
    data_validation = "DataValidation"  # 数据校验

class TaskSubType(str, Enum):
    """任务子类型"""
    full_row_compare = "FullRowCompare"  # 全量内容校验
    full_pk_compare = "FullPkCompare"  # 全量主键校验
    full_row_count_compare = "FullRowCountCompare"  # 全量行数校验
    meta_compare = ""  # 结构校验
    incr_data_validation = "IncrDataValidation"  # 增量校验

class TaskStatus(str, Enum):
    success = "Success" # 成功
    failed = "Failed"   # 失败
    running = "Running" # 运行中
    suspend = "Suspend" # 暂停中
    init = "Init"       # 初始化
    canceled = "Canceled"   # 已终止
    terminating = "Terminating" # 终止中

class EndpointType(str, Enum):
    builtin_kafka = "Builtin_Kafka" # 内置Kafka
    volc_mysql = "Volc_MySQL" # 火山引擎RDS MySQL
    volc_vedb_mysql = "Volc_veDB_MySQL" # 火山VeDB MySQL
    volc_sharding_mysql = "Volc_Sharding_MySQL" # 火山引擎分库分表RDS MySQL
    volc_postgresql = "Volc_PostgreSQL" # 火山引擎PostgreSQL
    volc_mongo = "Volc_Mongo" # 火山引擎MongoDB
    volc_elasticsearch = "Volc_ElasticSearch" # 火山引擎Elasticsearch
    volc_kafka = "Volc_Kafka" # 火山引擎Kafka
    volc_rocketmq = "Volc_RocketMQ" # 火山引擎RocketMQ
    volc_redis = "Volc_Redis" # 火山引擎Redis
    volc_mssql = "Volc_MSSQL" # 火山引擎MSSQL 
    public_mysql = "Public_MySQL" # 公网MySQL
    public_postgresql = "Public_PostgreSQL" # 公网PostgreSQL
    public_mongo = "Public_Mongo" # 公网MongoDB 
    public_elasticsearch = "Public_ElasticSearch" # 公网Elasticsearch
    public_redis = "Public_Redis" # 公网Redis
    public_mssql = "Public_MSSQL" # 公网MSSQL 
    express_mysql = "Express_MySQL" # 专有网络MySQL
    express_postgresql = "Express_PostgreSQL" # 表达式PostgreSQL
    express_mongo = "Express_Mongo" # 专有网络MongoDB
    express_redis = "Express_Redis" # 专有网络Redis
    express_mssql = "Express_MSSQL" # 专有网络MSSQL
    express_elasticsearch = "Express_ElasticSearch" # 专有网络Elasticsearch
    express_kafka = "Express_Kafka" # 专有网络Kafka 

class Statement(str, Enum):
    stmt_dml_insert          = "StmtDMLInsert" 
    stmt_dml_update          = "StmtDMLUpdate" 
    stmt_dml_delete          = "StmtDMLDelete" 
    stmt_ddl_all             = "StmtDDLAll" 
    stmt_ddl_alter_table      = "StmtDDLAlterTable" 
    stmt_ddl_alter_view       = "StmtDDLAlterView"
    stmt_ddl_create_function  = "StmtDDLCreateFunction"
    stmt_ddl_create_index     = "StmtDDLCreateIndex"
    stmt_ddl_create_procedure = "StmtDDLCreateProcedure"
    stmt_ddl_create_table     = "StmtDDLCreateTable"
    stmt_ddl_create_view      = "StmtDDLCreateView"
    stmt_ddl_drop_index       = "StmtDDLDropIndex"
    stmt_ddl_drop_table       = "StmtDDLDropTable"
    stmt_ddl_drop_function    = "StmtDDLDropFunction"
    stmt_ddl_drop_procedure   = "StmtDDLDropProcedure"
    stmt_ddl_truncate_table   = "StmtDDLTruncateTable"
    stmt_ddl_rename_table     = "StmtDDLRenameTable"
    stmt_ddl_drop_view        = "StmtDDLDropView"

class MongoDMLStatement(str, Enum):
    stmt_dml_all    = "StmtDMLAll"
    stmt_dml_insert = "StmtDMLInsert"
    stmt_dml_update = "StmtDMLUpdate"
    stmt_dml_delete = "StmtDMLDelete"

class MongoTransferDDLScope(str, Enum):
    ddl_all = "DDL_All"
    ddl_index = "DDL_Index"
    ddl_None = "DDL_None"

class MongoConflictRecordMode(str, Enum):
    local = "Local"
    remote = "Remote"

class SubscriptionProtocol(str, Enum):
    volc         = "Volc"
    dbus         = "Dbus"
    canal        = "Canal"
    canal_json   = "CanalJSON"
    dbus_bd      = "DbusBd"
    bson         = "Bson"
    redis_bd     = "RedisBd"
    canal_bd     = "CanalBd"
    avro         = "Avro"
    debezium_json= "DebeziumJSON"

class RedisArchType(str, Enum):
    standalone = "Standalone"
    cluster = "Cluster"

class PartitionPolicy(str, Enum):
    p0        = "P0" # 统一投递到分区0
    table     = "Table" # 按库表名联合hash值投递到不同分区
    key       = "Key"   # 按主键hash值投递到不同分区
    slot      = "Slot" # 按Redis分片槽位hash值投递到不同分区
    timestamp = "Timestamp" # 按时间戳hash值投递到不同分区
    custom_column = "CustomColumn" # 按用户自定义列hash值投递到不同分区

class ValidationStatus(str, Enum):
    no_diff = "NoDiff"  # 不存在不一致
    has_diff = "HasDiff"  # 存在不一致

class PolicyForPrimaryKeyConflict(str, Enum):
    throw_error = "ThrowError"  # 冲突报错
    ignore = "Ignore"           # 冲突忽略
    override = "Override"       # 冲突覆盖

class RedisCompareMode(str, Enum):
    compare_key_and_value = "CompareKeyAndValue"
    compare_key = "CompareKey"
    compare_key_value_length = "CompareKeyValueLength"

class DataSourceCategory(str, Enum):
    mysql = "MySQL"
    redis = "Redis"
    mongodb = "MongoDB"
    postgresql = "PostgreSQL"
    sqlserver = "SQLServer"
    elasticsearch = "ElasticSearch"
    kafka = "Kafka"
    rocketmq = "RocketMQ"

class ListDataSourceOrderBy(str, Enum):
    order_by_create_time_asc = "OrderByCreateTimeAsc"
    order_by_create_time_desc = "OrderByCreateTimeDesc"
    order_by_modify_time_asc = "OrderByModifyTimeAsc"
    order_by_modify_time_desc = "OrderByModifyTimeDesc"

class SSLSettings(BaseModel):
    enable_ssl: bool
    cert: str

class ServerRoomSetting(BaseModel):
    server_room: Optional[str] = None

class RegionSettings(BaseModel):
    region: str = Field(default="cn-guilin-boe", description="地域", alias="Region")

class CrossAccountSettings(BaseModel):
    AccountId: Optional[str] = Field(default=None, description="账号ID", alias="AccountId")
    AccountName: Optional[str] = Field(default=None, description="账号名称", alias="AccountName")
    SourceAccount: str = Field(description="源账号", alias="SourceAccount")
    Role: str = Field(description="角色", alias="Role")

class BuiltinKafkaSettings(BaseModel):
    vpc_id: str = Field(default=None, description="VPC ID", alias="VPCId")
    vpc_subnet_id: str = Field(default=None, description="子网ID", alias="VPCSubnetId")

class VolcMySQLSettings(BaseModel):
    db_instance_id: str = Field(description="火山引擎RDS MySQL实例ID,例如：mysql-f9srjf9f", alias="DBInstanceId")
    username: str = Field(description="火山引擎RDS MySQL实例用户名", alias="Username")
    password: str = Field(description="火山引擎RDS MySQL实例密码", alias="Password")
    region_settings: 'RegionSettings' = Field(description="火山引擎RDS MySQL实例区域", alias="RegionSettings")
    db_instance_node_id: Optional[str] = Field(default=None, description="火山引擎RDS MySQL实例只读节点ID", alias="DBInstanceNodeId")
    cross_account_settings:  Optional['CrossAccountSettings'] = Field(default=None, description="跨账号设置", alias="CrossAccountSettings")

class VolcveDBMySQLSettings(BaseModel):
    db_instance_id: str = Field(description="火山引擎RDS MySQL实例ID,例如：mysql-f9srjf9f", alias="DBInstanceId")
    username: str = Field(description="火山引擎RDS MySQL实例用户名", alias="Username")
    password: str = Field(description="火山引擎RDS MySQL实例密码", alias="Password")
    region_settings: 'RegionSettings' = Field(description="火山引擎RDS MySQL实例区域", alias="RegionSettings")
    cross_account_settings: Optional['CrossAccountSettings'] = Field(default=None, description="跨账号设置", alias="CrossAccountSettings")
    db_instance_node_id: Optional[str] = Field(default=None, description="火山引擎RDS MySQL实例只读节点ID", alias="DBInstanceNodeId")

class VolcRedisSettings(BaseModel):
    db_instance_id: str = Field(description="火山引擎RDS Redis实例ID,例如：redis-f9srjf9f", alias="DBInstanceId")
    username: str = Field(description="火山引擎RDS Redis实例用户名", alias="Username")
    password: str = Field(description="火山引擎RDS Redis实例密码", alias="Password")
    db_name: str = Field(description="火山引擎RDS Redis实例数据库名称", alias="DBName")
    region_settings: 'RegionSettings' = Field(description="火山引擎RDS Redis实例区域", alias="RegionSettings")
    cross_account_settings: Optional['CrossAccountSettings'] = Field(default=None, description="跨账号设置", alias="CrossAccountSettings")

class VolcPostgreSQLSettings(BaseModel):
    db_instance_id: str = Field(description="火山引擎RDS PostgreSQL实例ID,例如：postgresql-f9srjf9f", alias="DBInstanceId")
    username: str = Field(description="火山引擎RDS PostgreSQL实例用户名", alias="Username")
    password: str = Field(description="火山引擎RDS PostgreSQL实例密码", alias="Password")
    db_name: str = Field(description="火山引擎RDS PostgreSQL实例数据库名称", alias="DBName")
    region_settings: 'RegionSettings' = Field(description="火山引擎RDS PostgreSQL实例区域", alias="RegionSettings")
    cross_account_settings: Optional['CrossAccountSettings'] = Field(default=None, description="跨账号设置", alias="CrossAccountSettings")

class VolcMongoSettings(BaseModel):
    db_instance_id: str = Field(description="火山引擎MongoDB实例ID,例如：mongodb-f9srjf9f", alias="DBInstanceId")
    username: str = Field(description="火山引擎MongoDB实例用户名", alias="Username")
    password: str = Field(description="火山引擎MongoDB实例密码", alias="Password")
    deploy_type: 'MongoDeployType' = Field(description="火山引擎MongoDB实例架构", alias="DeployType")
    mongo_auth_source_db: Optional[str] = Field(default=None, description="火山引擎MongoDB实例认证数据库", alias="MongoAuthSourceDB")
    region_settings: 'RegionSettings' = Field(description="火山引擎MongoDB实例区域", alias="RegionSettings")
    pull_method: Optional['MongoIncrPullMethod'] = Field(default=MongoIncrPullMethod.oplog, description="火山引擎MongoDB分片集群实例增量拉取方法", alias="PullMethod")
    use_new_sharding_datasource: Optional[bool] = Field(default=True, description="是否使用新版分片数据源", alias="UseNewShardingDatasource")
    cross_account_settings: Optional['CrossAccountSettings'] = Field(default=None, description="跨账号设置", alias="CrossAccountSettings")

class VolcElasticSearchSettings(BaseModel):
    db_instance_id: str = Field(description="火山引擎ElasticSearch实例ID", alias="DBInstanceId")
    username: str = Field(description="火山引擎ElasticSearch实例用户名", alias="Username")
    password: str = Field(description="火山引擎ElasticSearch实例密码", alias="Password")
    region_settings: 'RegionSettings' = Field(description="火山引擎ElasticSearch实例区域", alias="RegionSettings")


class VolcKafkaSettings(BaseModel):
    instance_id: str = Field(description="火山引擎Kafka实例ID", alias="InstanceId")
    auth_type: str = Field(default="PLAIN", description="火山引擎Kafka实例认证类型", alias="AuthType")
    username: str = Field(description="火山引擎Kafka实例用户名", alias="Username")
    password: str = Field(description="火山引擎Kafka实例密码", alias="Password")
    topic: str = Field(description="火山引擎Kafka实例Topic", alias="Topic")
    region_settings: 'RegionSettings' = Field(description="火山引擎Kafka实例区域", alias="RegionSettings")

class VolcRocketMQSettings(BaseModel):
    instance_id: str = Field(description="火山引擎RocketMQ实例ID", alias="InstanceId")
    auth_type: str = Field(default="PLAIN", description="火山引擎RocketMQ实例认证类型", alias="AuthType")
    username: str = Field(description="火山引擎RocketMQ实例用户名", alias="Username")
    password: str = Field(description="火山引擎RocketMQ实例密码", alias="Password")
    topic: str = Field(description="火山引擎RocketMQ实例Topic", alias="Topic")
    region_settings: 'RegionSettings' = Field(description="火山引擎RocketMQ实例区域", alias="RegionSettings")

class VolcMSSQLSettings(BaseModel):
    db_instance_id: str = Field(description="火山引擎RDS MSSQL实例ID", alias="DBInstanceId")
    username: str = Field(description="火山引擎RDS MSSQL实例用户名", alias="Username")
    password: str = Field(description="火山引擎RDS MSSQL实例密码", alias="Password")
    region_settings: 'RegionSettings' = Field(description="火山引擎RDS MSSQL实例区域", alias="RegionSettings")
    cross_account_settings: Optional['CrossAccountSettings'] = Field(default=None, description="跨账号设置", alias="CrossAccountSettings")
    full_backup_id: Optional[str] = Field(default=None, description="火山引擎RDS MSSQL实例全量备份ID", alias="FullBackupId") 
    migration_type: Optional['MigrationType'] = Field(default=None, description="迁移类型", alias="MigrationType")
    upload_method: Optional['UploadMethod'] = Field(default=None, description="上传方法", alias="UploadMethod")

class PublicMySQLSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")
    ssl_settings: Optional['SSLSettings'] = Field(default=None, description="SSL 配置", alias="SSLSettings")

class PublicPostgreSQLSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    db_name: str = Field(description="数据库名", alias="DBName")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")


class MongoShardSetting(BaseModel):
    address: str = Field(description="地址", alias="Address")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    auth_db: str = Field(description="认证数据库", alias="AuthDB")
    extra_dsn: Optional[dict[str, str]] = Field(default=None, description="额外的 DSN 参数", alias="ExtraDSN")

class PublicMongoSettings(BaseModel):
    endpoints: List[str] = Field(description="地址列表", alias="Endpoints")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    mongo_auth_source_db: str = Field(description="认证数据库", alias="UseNewShardingDatasource")
    deploy_type: 'MongoDeployType' = Field(description="MongoDB架构", alias="DeployType")
    pull_method: Optional[MongoIncrPullMethod] = Field(default=None, description="增量拉取方法", alias="PullMethod")
    shards: Optional[List[MongoShardSetting]] = Field(default=None, description="分片配置", alias="Shards")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class PublicElasticSearchSettings(BaseModel): 
    endpoints: List[str] = Field(description="地址列表", alias="Endpoints")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class PublicRedisSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    db_name: Optional[str] = Field(default=None, description="数据库名", alias="DBName")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class PublicMSSQLSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    migration_type: Optional[MigrationType] = Field(default=None, description="迁移类型", alias="MigrationType")
    upload_method: Optional[UploadMethod] = Field(default=None, description="上传方法", alias="UploadMethod") 
    region_settings: Optional['RegionSettings'] = Field(default=None, description="区域配置", alias="RegionSettings")

class PrivateNetworkSettings(BaseModel):
    vpc_id: str = Field(description="VPC ID", alias="VpcId")
    subnet_id: str = Field(description="子网 ID", alias="SubnetId")

class ExpressMySQLSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    private_network_settings: PrivateNetworkSettings = Field(description="私有网络配置", alias="PrivateNetworkSettings")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class ExpressPostgreSQLSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    db_name: str = Field(description="数据库名", alias="DBName")
    private_network_settings: PrivateNetworkSettings = Field(description="私有网络配置", alias="PrivateNetworkSettings")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class ExpressMongoSettings(BaseModel):
    endpoints: List[str] = Field(description="地址列表", alias="Endpoints")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    mongo_auth_source_db: str = Field(description="认证数据库", alias="MongoAuthSourceDB")
    deploy_type: 'MongoDeployType' = Field(description="MongoDB架构", alias="DeployType")
    private_network_settings: PrivateNetworkSettings = Field(description="私有网络配置", alias="PrivateNetworkSettings")
    pull_method: Optional[MongoIncrPullMethod] = Field(default=None, description="增量拉取方法", alias="PullMethod")
    shards: Optional[List[MongoShardSetting]] = Field(default=None, description="分片配置", alias="Shards")
    use_new_sharding_datasource: Optional[bool] = Field(default=True, description="是否使用新的分片数据源", alias="UseNewShardingDatasource")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class ExpressRedisSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    db_name: str = Field(description="数据库名", alias="DBName")
    private_network_settings: PrivateNetworkSettings = Field(description="私有网络配置", alias="PrivateNetworkSettings")
    arch_type: RedisArchType = Field(description="架构类型", alias="ArchType")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class ExpressMSSQLSettings(BaseModel):
    host: str = Field(description="地址", alias="Host")
    port: int = Field(description="端口", alias="Port")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    db_name: str = Field(description="数据库名", alias="DBName")
    private_network_settings: PrivateNetworkSettings = Field(description="私有网络配置", alias="PrivateNetworkSettings")
    migration_type: Optional['MigrationType'] = Field(default=None, description="迁移类型", alias="MigrationType")
    upload_method: Optional['UploadMethod'] = Field(default=None, description="上传方法", alias="UploadMethod")
    region_settings: Optional['RegionSettings'] = Field(default=None, description="区域配置", alias="RegionSettings")

class ExpressElasticSearchSettings(BaseModel):
    endpoints: List[str] = Field(description="地址列表", alias="Endpoints")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    private_network_settings: PrivateNetworkSettings = Field(description="私有网络配置", alias="PrivateNetworkSettings")
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class ExpressKafkaSettings(BaseModel):
    broker_endpoints: List[str] = Field(description="地址列表", alias="BrokerEndpoints")
    auth_type: str = Field(default="PLAIN", description="认证类型", alias="AuthType")
    username: str = Field(description="用户名", alias="Username")
    password: str = Field(description="密码", alias="Password")
    topic: str = Field(description="主题", alias="Topic")
    private_network_settings: PrivateNetworkSettings = Field(description="私有网络配置", alias="PrivateNetworkSettings") 
    region_settings: 'RegionSettings' = Field(description="区域配置", alias="RegionSettings")

class DataSource(BaseModel):
    """
    数据源配置，根据用户提供的信息，确定数据源类型和对应的配置。如专网MySQL对应EndpointType.Express_MySQL
    """
    datasource_id: Optional[str] = Field(default=None, description="数据源ID", alias="DataSourceId")
    endpoint_type: Optional[EndpointType] = Field(default=None, description="数据源类型", alias="EndpointType")
    category: Optional[DataSourceCategory] = Field(default=None, description="数据源分类", alias="Category")
    name: Optional[str] = Field(default=None, description="数据源名称", alias="Name")
    volc_mysql_settings: Optional[VolcMySQLSettings] = Field(default=None, description="火山MySQL数据源配置,对应EndpointType.volc_mysql", alias="VolcMySQLSettings")
    volc_vedb_mysql_settings: Optional[VolcveDBMySQLSettings] = Field(default=None, description="火山veDBMySQL数据源配置,对应EndpointType.volc_ve_db_mysql", alias="VolcveDBMySQLSettings")
    volc_postgresql_settings: Optional[VolcPostgreSQLSettings] = Field(default=None, description="火山PostgreSQL数据源配置,对应EndpointType.volc_postgresql", alias="VolcPostgreSQLSettings")
    volc_mongo_settings: Optional[VolcMongoSettings] = Field(default=None, description="火山Mongo数据源配置,对应EndpointType.volc_mongo", alias="VolcMongoSettings")
    volc_elastic_search_settings: Optional[VolcElasticSearchSettings] = Field(default=None, description="火山ElasticSearch数据源配置,对应EndpointType.volc_elasticsearch", alias="VolcElasticSearchSettings")
    volc_kafka_settings: Optional[VolcKafkaSettings] = Field(default=None, description="火山Kafka数据源配置,对应EndpointType.volc_kafka", alias="VolcKafkaSettings")
    builtin_kafka_settings: Optional[BuiltinKafkaSettings] = Field(default=None, description="内置Kafka数据源配置,对应EndpointType.builtin_kafka", alias="BuiltinKafkaSettings")
    volc_rocket_mq_settings: Optional[VolcRocketMQSettings] = Field(default=None, description="火山RocketMQ数据源配置,对应EndpointType.volc_rocketmq", alias="VolcRocketMQSettings")
    volc_redis_settings: Optional[VolcRedisSettings] = Field(default=None, description="火山Redis数据源配置,对应EndpointType.volc_redis", alias="VolcRedisSettings") 
    volc_mssql_settings: Optional[VolcMSSQLSettings] = Field(default=None, description="火山MSSQL数据源配置,对应EndpointType.volc_mssql", alias="VolcMSSQLSettings")           
    public_mysql_settings: Optional[PublicMySQLSettings] = Field(default=None,description="公共MySQL数据源配置,对应EndpointType.public_mysql", alias="PublicMySQLSettings") 
    public_postgresql_settings: Optional[PublicPostgreSQLSettings] = Field(default=None,description="公共PostgreSQL数据源配置,对应EndpointType.public_postgresql", alias="PublicPostgreSQLSettings")
    public_mongo_settings: Optional[PublicMongoSettings] = Field(default=None,description="公共Mongo数据源配置,对应EndpointType.public_mongo", alias="PublicMongoSettings")
    public_elasticsearch_settings: Optional[PublicElasticSearchSettings] = Field(default=None,description="公共ElasticSearch数据源配置,对应EndpointType.public_elasticsearch", alias="PublicElasticSearchSettings")
    public_redis_settings: Optional[PublicRedisSettings] = Field(default=None,description="公共Redis数据源配置,对应EndpointType.public_redis", alias="PublicRedisSettings")
    public_mssql_settings: Optional[PublicMSSQLSettings] = Field(default=None,description="公共MSSQL数据源配置,对应EndpointType.public_mssql", alias="PublicMSSQLSettings") 
    express_mysql_settings: Optional[ExpressMySQLSettings] = Field(default=None,description="火山MySQL数据源配置,对应EndpointType.express_mysql", alias="ExpressMySQLSettings")
    express_postgresql_settings: Optional[ExpressPostgreSQLSettings] = Field(default=None,description="火山PostgreSQL数据源配置,对应EndpointType.express_postgresql", alias="ExpressPostgreSQLSettings")
    express_mongo_settings: Optional[ExpressMongoSettings] = Field(default=None,description="火山Mongo数据源配置,对应EndpointType.express_mongo", alias="ExpressMongoSettings")
    express_redis_settings: Optional[ExpressRedisSettings] = Field(default=None,description="火山Redis数据源配置,对应EndpointType.express_redis", alias="ExpressRedisSettings")
    express_mssql_settings: Optional[ExpressMSSQLSettings] = Field(default=None,description="火山MSSQL数据源配置,对应EndpointType.express_mssql", alias="ExpressMSSQLSettings") 
    express_elasticsearch_settings: Optional[ExpressElasticSearchSettings] = Field(default=None,description="火山ElasticSearch数据源配置,对应EndpointType.express_elasticsearch", alias="ExpressElasticSearchSettings")
    express_kafka_settings: Optional[ExpressKafkaSettings] = Field(default=None,description="火山Kafka数据源配置,对应EndpointType.express_kafka", alias="ExpressKafkaSettings")

class AccountMapping(BaseModel):
    account: Optional[str] = Field(default=None, description="账号", alias="Account")
    password: Optional[str] = Field(default=None, description="密码", alias="Password")
    reset_password: Optional[bool] = Field(default=False, description="是否重置密码", alias="ResetPassword")

class ESMetaMappingSettings(BaseModel):
    pid_col: Optional[List[str]] = Field(default=None, description="主键列", alias="PidCol")
    enable_routing: Optional[bool] = Field(default=False, description="是否开启路由", alias="EnableRouting")
    routing_col: Optional[List[str]] = Field(default=None, description="路由列", alias="RoutingCol")
    type_name: Optional[str] = Field(default=None, description="类型名称", alias="TypeName")

class ObjectMappingSettings(BaseModel):
    es_meta_mapping_settings: Optional['ESMetaMappingSettings'] = Field(default=None, description="ES元数据映射配置", alias="ESMetaMappingSettings")
    set_object_trans_type: bool = Field(default=False, description="是否设置对象传输类型", alias="SetObjectTransType")
    object_trans_types: Optional[List['ObjectTransType']] = Field(default=None, description="对象传输类型", alias="ObjectTransTypes")
    policy_for_key_conflict: Optional['TablePolicyForPrimaryKeyConflict'] = Field(default=None, description="主键冲突策略", alias="PolicyForKeyConflict")
    partition_column: Optional[str] = Field(default=None, description="订阅根据列hash进行投递的列名", alias="PartitionColumn")

class ObjectMapping(BaseModel):
    object_type: Optional[ObjectType] = Field(default=None, description="对象类型", alias="ObjectType")
    src_obj_name: Optional[str] = Field(default=None, description="源端对象名字", alias="SrcObjName")
    dest_obj_name: Optional[str] = Field(default=None, description="目的端对象名字", alias="DestObjName") 
    mapping_list: Optional[List['ObjectMapping']] = Field(default=None, description="子对象映射列表", alias="MappingList")
    object_mapping_settings: Optional['ObjectMappingSettings'] = Field(default=None, description="对象映射配置", alias="ObjectMappingSettings")

class MySQLPosition(BaseModel):
    gtid: Optional[str] = Field(default=None, description="gtid")
    gset: Optional[str] = Field(default=None, description="gset")
    timestamp: Optional[str] = Field(default=None, description="时间戳")

class AccountTransmissionSettings(BaseModel):
    enable_account: Optional[bool] = Field(default=None, description="是否开启账号传输", alias="EnableAccount")

class MetaTransmissionSettings(BaseModel):
    enable_meta: Optional[bool] = Field(default=None, description="是否开启结构传输", alias="EnableMeta")

class FullExtraCondition(BaseModel):
    db: Optional[str] = Field(default=None, description="数据库")
    table: Optional[str] = Field(default=None, description="表")
    where_sql: Optional[str] = Field(default=None, description="where条件")

class FullTransmissionSettings(BaseModel):
    enable_full: Optional[bool] = Field(default=None, description="是否开启全量同步", alias="EnableFull")
    snapshot: Optional[bool] = Field(default=None, description="是否开启快照同步", alias="Snapshot")
    rps_limit: Optional[int] = Field(default=None, description="rps限制", alias="RpsLimit")
    bps_limit: Optional[int] = Field(default=None, description="bps限制", alias="BpsLimit")
    full_sync_parallel: Optional[int] = Field(default=None, description="全量同步并行度", alias="FullSyncParallel")
    extra_conditions: Optional[FullExtraCondition] = Field(default=None, description="全量同步额外条件", alias="ExtraConditions")

class IncrTransmissionSettings(BaseModel):
    enable_incr: bool = Field(default=False, description="是否开启增量同步", alias="EnableIncr")
    statements: Optional[List[Statement]] = Field(default=None, description="增量同步语句", alias="Statements")
    bps_limit: Optional[int] = Field(default=None, description="bps限制", alias="BpsLimit")
    mongo_dml_statements: Optional[List[MongoDMLStatement]] = Field(default=None, description="mongo增量同步语句", alias="MongoDMLStatements")

class ETLSettings(BaseModel):
    script: str = Field(default=None, description="ETL脚本", alias="Script")

class ErrorBehaviorSettings(BaseModel):
    max_retry_seconds: int = Field(default=None, description="最大重试时间", alias="MaxRetrySeconds")

class ValidationSettings(BaseModel):
    parallel_num: int = Field(default=None, description="并发数", alias="ParallelNum")
    rps_limit: int = Field(default=None, description="rps限制", alias="RpsLimit")

class MySQL2MySQLSettings(BaseModel):
    account_transmission_settings: Optional['AccountTransmissionSettings'] = Field(default=None, description="账号传输配置")
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="同步对象映射配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    mysql_position: Optional['MySQLPosition'] = Field(default=None, description="mysql位点", alias="MySQLPosition")
    policy_for_primary_key_conflict: Optional['PolicyForPrimaryKeyConflict'] = Field(default=None, description="主键冲突策略", alias="PolicyForPrimaryKeyConflict")
    account_mapping: Optional[List['AccountMapping']] = Field(default=None, description="账号映射配置", alias="AccountMapping")
    enable_foreign_key_checks: Optional[bool] = Field(default=None, description="是否开启外键检查", alias="EnableForeignKeyChecks")
    enable_full_incr: Optional[bool] = Field(default=None, description="是否开启全量增量同步", alias="EnableFullIncr")
    enable_trx_rewrite: Optional[bool] = Field(default=None, description="是否开启事务重写", alias="EnableTrxRewrite")
    enable_full_trx_partition_by_chunk: Optional[bool] = Field(default=None, description="是否开启全量事务分chunk", alias="EnableFullTrxPartitionByChunk")

class ESExtraArgs(BaseModel):
    shard_num: int = Field(default=None, description="分片数", alias="ShardNum")
    replica_num: int = Field(default=None, description="副本数", alias="ReplicaNum")
    tz: str = Field(default=None, description="时区", alias="TZ") 
    retry_times: int = Field(default=None, description="重试次数", alias="RetryTimes")
    analyzer: str = Field(default=None, description="分析器", alias="Analyzer")
    insert_mode: Optional[InsertMode] = Field(default=None, description="插入模式", alias="InsertMode")
    custom_index_type: str = Field(default=None, description="自定义索引类型", alias="CustomIndexType")
    replace_target_index: Optional[Dict[str, str]] = Field(default=None, description="替换目标索引", alias="ReplaceTargetIndex")
    es_name_rule: Optional['ESNameRule'] = Field(default=None, description="ES名称规则", alias="ESNameRule")

class PreferredMapping(BaseModel):
    src: Optional[str] = Field(default=None, description="源端库表匹配规则")
    dst: Optional[str] = Field(default=None, description="目的端Topic")
    priority: Optional[int] = Field(default=None, description="优先级")

 
class SubscriptionSettings(BaseModel):
    protocol: Optional[SubscriptionProtocol] = Field(default=None, description="订阅格式", alias="Protocol")
    partition_policy: Optional[PartitionPolicy] = Field(default=None, description="分区投递策略", alias="PartitionPolicy")
    vpc_id: Optional[str] = Field(default=None, description="VPC ID，仅目的端是内置Kafka时需要指定", alias="VPCId")
    vpc_subnet_id: Optional[str] = Field(default=None, description="VPC子网ID，仅目的端是内置Kafka时需要指定", alias="VPCSubnetId")
    enable_begin_commit_message: Optional[bool] = Field(default=None, description="是否订阅Begin和Commit消息", alias="EnableBeginCommitMessage")
    enable_multi_topic: Optional[bool] = Field(default=None, description="是否开始订阅到多个Topic", alias="EnableMultiTopic")
    preferred_mappings: Optional[List['PreferredMapping']] = Field(default=None, description="库表自动投递规则", alias="PreferredMappings")
    
class MySQL2ESSettings(BaseModel):
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="同步对象映射配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    es_extra_args: Optional['ESExtraArgs'] = Field(default=None, description="ES额外参数", alias="ESExtraArgs")
    policy_for_primary_key_conflict: Optional['PolicyForPrimaryKeyConflict'] = Field(default=None, description="冲突策略", alias="PolicyForPrimaryKeyConflict")
    mysql_position: Optional['MySQLPosition'] = Field(default=None, description="MySQL位点", alias="MySQLPosition")

class MySQL2KafkaSettings(BaseModel):
    subscription_settings: Optional['SubscriptionSettings'] = Field(default=None, description="订阅配置", alias="SubscriptionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="订阅对象配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    mysql_position: Optional['MySQLPosition'] = Field(default=None, description="MySQL位点", alias="MySQLPosition")

class MySQL2RocketMQSettings(BaseModel):
    subscription_settings: Optional['SubscriptionSettings'] = Field(default=None, description="订阅配置", alias="SubscriptionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="订阅对象配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    mysql_position: Optional['MySQLPosition'] = Field(default=None, description="MySQL位点", alias="MySQLPosition")

class PG2PGSettings(BaseModel):
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="订阅对象配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class PG2KafkaSettings(BaseModel):
    subscription_settings: Optional['SubscriptionSettings'] = Field(default=None, description="订阅配置", alias="SubscriptionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="订阅对象配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")

class PG2RocketMQSettings(BaseModel):
    subscription_settings: Optional['SubscriptionSettings'] = Field(default=None, description="订阅配置", alias="SubscriptionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="订阅对象配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")

class MongoPosition(BaseModel):
    timestamp: Optional[int] = Field(default=None, description="时间戳")
    resume_token: Optional[str] = Field(default=None, description="resume token")

class Mongo2MongoSettings(BaseModel):
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="结构传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="订阅对象配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    mongo_position: Optional['MongoPosition'] = Field(default=None, description="Mongo位点", alias="MongoPosition")
    policy_for_mongo_primary_key_conflict: Optional['PolicyForMongoPrimaryKeyConflict'] = Field(default=None, description="Mongo主键冲突策略", alias="PolicyForMongoPrimaryKeyConflict")
    mongo_transfer_ddl_scope: Optional['MongoTransferDDLScope'] = Field(default=None, description="Mongo DDL 作用范围", alias="MongoTransferDDLScope")
    mongo_conflict_record_mode: Optional['MongoConflictRecordMode'] = Field(default=None, description="Mongo 冲突记录模式", alias="MongoConflictRecordMode")
    mongo_conflict_record_db: Optional[str] = Field(default=None, description="Mongo 冲突记录数据库", alias="MongoConflictRecordDB")

class Mongo2RocketMQSettings(BaseModel):
    subscription_settings: Optional['SubscriptionSettings'] = None
    object_mappings: Optional[List['ObjectMapping']] = None
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = None
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = None
    full_transmission_settings: Optional['FullTransmissionSettings'] = None
    mongo_position: Optional['MongoPosition'] = None

class Redis2RedisSettings(BaseModel):
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="传输对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    filter_rules: Optional[List['FilterRule']] = Field(default=None, description="过滤规则", alias="FilterRules")

class Redis2RocketMQSettings(BaseModel):
    subscription_settings: Optional['SubscriptionSettings'] = Field(default=None, description="订阅配置", alias="SubscriptionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="传输对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")

class MSSQL2MSSQLSettings(BaseModel):
    meta_transmission_settings: Optional['MetaTransmissionSettings'] = Field(default=None, description="元数据传输配置", alias="MetaTransmissionSettings")
    full_transmission_settings: Optional['FullTransmissionSettings'] = Field(default=None, description="全量传输配置", alias="FullTransmissionSettings")
    incr_transmission_settings: Optional['IncrTransmissionSettings'] = Field(default=None, description="增量传输配置", alias="IncrTransmissionSettings")
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="传输对象配置", alias="ObjectMappings")
    etl_settings: Optional['ETLSettings'] = Field(default=None, description="ETL配置", alias="ETLSettings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class MySQL2MySQLRowCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    sample_rate: Optional[int] = Field(default=None, description="全量校验时的采样率", alias="SampleRate")
    validation_settings: Optional['ValidationSettings'] = Field(default=None, description="校验配置", alias="ValidationSettings")

class MySQL2MySQLRowCountCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class MySQL2MySQLMetaCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class MySQL2MySQLIncrDataValidationSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class PG2PGRowCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    validation_settings: Optional['ValidationSettings'] = Field(default=None, description="校验配置", alias="ValidationSettings")

class Mongo2MongoRowCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    validation_settings: Optional['ValidationSettings'] = Field(default=None, description="校验配置", alias="ValidationSettings")

class Mongo2MongoPkCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class Mongo2MongoIncrDataValidationSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class Mongo2MongoRowCountCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class Redis2RedisRowCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    sample_rate: Optional[int] = Field(default=None, description="全量校验时的采样率", alias="SampleRate")
    validation_settings: Optional['ValidationSettings'] = Field(default=None, description="校验配置", alias="ValidationSettings")
    redis_compare_mode: Optional['RedisCompareMode'] = Field(default=None, description="Redis校验模式", alias="CompareMode")

class MSSQL2MSSQLRowCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")
    sample_rate: Optional[int] = Field(default=None, description="全量校验时的采样率", alias="SampleRate")
    validation_settings: Optional['ValidationSettings'] = Field(default=None, description="校验配置", alias="ValidationSettings")

class MSSQL2MSSQLRowCountCompareSettings(BaseModel):
    object_mappings: Optional[List['ObjectMapping']] = Field(default=None, description="校验对象配置", alias="ObjectMappings")
    error_behavior_settings: Optional['ErrorBehaviorSettings'] = Field(default=None, description="错误行为配置", alias="ErrorBehaviorSettings")

class ServerItem(BaseModel):
    id: Optional[str] = None
    location: Optional[str] = None
    type: Optional['EndpointType'] = None

class FilterRule(BaseModel):
    filter_type: Optional['FilterType'] = None
    pass_: Optional[bool] = None
    server_filter_rule: Optional[List['ServerItem']] = None
    regex_filter_rule: Optional[List[str]] = None

class SolutionSettings(BaseModel):
    solution_type: Optional['SolutionType'] = Field(default=None, description="解决方案类型,`数据源类型`到`目标数据源类型`的解决方案,如Mysql到Mysql传输类型", alias="SolutionType")
    auto_start:       bool = Field(default=False, description="是否自动启动")
    mysql2mysql_settings: Optional['MySQL2MySQLSettings'] = Field(default=None, description="MySQL2MySQL解决方案配置", alias="MySQL2MySQLSettings")
    mysql2es_settings: Optional['MySQL2ESSettings'] = Field(default=None, description="MySQL2ES解决方案配置", alias="MySQL2ESSettings")
    mysql2kafka_settings: Optional['MySQL2KafkaSettings'] = Field(default=None, description="MySQL2Kafka解决方案配置", alias="MySQL2KafkaSettings")
    mysql2rocketmq_settings: Optional['MySQL2RocketMQSettings'] = Field(default=None, description="MySQL2RocketMQ解决方案配置", alias="MySQL2RocketMQSettings")
    pg2pg_settings: Optional['PG2PGSettings'] = Field(default=None, description="PG2PG解决方案配置", alias="PG2PGSettings")
    pg2kafka_settings: Optional['PG2KafkaSettings'] = Field(default=None, description="PG2Kafka解决方案配置", alias="PG2KafkaSettings")
    pg2rocketmq_settings: Optional['PG2RocketMQSettings'] = Field(default=None, description="PG2RocketMQ解决方案配置", alias="PG2RocketMQSettings")
    mongo2_mongo_settings: Optional['Mongo2MongoSettings'] = Field(default=None, description="Mongo2Mongo解决方案配置", alias="Mongo2MongoSettings")
    redis2_redis_settings: Optional['Redis2RedisSettings'] = Field(default=None, description="Redis2Redis解决方案配置", alias="Redis2RedisSettings")
    mongo2rocketmq_settings: Optional['Mongo2RocketMQSettings'] = Field(default=None, description="Mongo2RocketMQ解决方案配置", alias="Mongo2RocketMQSettings")
    redis2rocketmq_settings: Optional['Redis2RocketMQSettings'] = Field(default=None, description="Redis2RocketMQ解决方案配置", alias="Redis2RocketMQSettings")
    mssql2mssql_settings: Optional['MSSQL2MSSQLSettings'] = Field(default=None, description="MSSQL2MSSQL解决方案配置", alias="MSSQL2MSSQLSettings")
    mysql2mysql_rowcompare_settings: Optional['MySQL2MySQLRowCompareSettings'] = Field(default=None, description="MySQL2MySQLRowCompare解决方案配置", alias="MySQL2MySQLRowCompareSettings")
    mysql2mysql_rowcountcompare_settings: Optional['MySQL2MySQLRowCountCompareSettings'] = Field(default=None, description="MySQL2MySQLRowCountCompare解决方案配置", alias="MySQL2MySQLRowCountCompareSettings")
    mysql2mysql_metacompare_settings: Optional['MySQL2MySQLMetaCompareSettings'] = Field(default=None, description="MySQL2MySQLMetaCompare解决方案配置", alias="MySQL2MySQLMetaCompareSettings")
    mysql2mysql_incrdata_validation_settings: Optional['MySQL2MySQLIncrDataValidationSettings'] = Field(default=None, description="MySQL2MySQLIncrDataValidation解决方案配置", alias="MySQL2MySQLIncrDataValidationSettings")
    pg2pg_rowcompare_settings: Optional['PG2PGRowCompareSettings'] = Field(default=None, description="PG2PGRowCompare解决方案配置", alias="PG2PGRowCompareSettings")
    mongo2mongo_rowcompare_settings: Optional['Mongo2MongoRowCompareSettings'] = Field(default=None, description="Mongo2MongoRowCompare解决方案配置", alias="Mongo2MongoRowCompareSettings")
    mongo2mongo_pkcompare_settings: Optional['Mongo2MongoPkCompareSettings'] = Field(default=None, description="Mongo2MongoPkCompare解决方案配置", alias="Mongo2MongoPkCompareSettings")
    mongo2mongo_incrdata_validation_settings: Optional['Mongo2MongoIncrDataValidationSettings'] = Field(default=None, description="Mongo2MongoIncrDataValidation解决方案配置", alias="Mongo2MongoIncrDataValidationSettings")
    mongo2mongo_rowcountcompare_settings: Optional['Mongo2MongoRowCountCompareSettings'] = Field(default=None, description="Mongo2MongoRowCountCompare解决方案配置", alias="Mongo2MongoRowCountCompareSettings")
    redis2redis_rowcompare_settings: Optional['Redis2RedisRowCompareSettings'] = Field(default=None, description="Redis2RedisRowCompare解决方案配置", alias="Redis2RedisRowCompareSettings")
    mssql2mssql_rowcompare_settings: Optional['MSSQL2MSSQLRowCompareSettings'] = Field(default=None, description="MSSQL2MSSQLRowCompare解决方案配置", alias="MSSQL2MSSQLRowCompareSettings")
    mssql2mssql_rowcountcompare_settings: Optional['MSSQL2MSSQLRowCountCompareSettings'] = Field(default=None, description="MSSQL2MSSQLRowCountCompare解决方案配置", alias="MSSQL2MSSQLRowCountCompareSettings")

class TagObject(BaseModel):
    key: str = Field(description="标签键", alias="Key")
    value: Optional[str] = Field(default=None, description="标签值", alias="Value")

class TagFilterObject(BaseModel):
    key: str = Field(description="标签键", alias="Key")
    value: Optional[str] = Field(default=None, description="标签值", alias="Value")

class ConvertPostPaidToPrePaid(BaseModel):
    times: int = Field(description="包年包月购买月数", alias="Times")
    auto_renew: bool = Field(description="是否自动续费", alias="AutoRenew")

class ModifyInstanceSpec(BaseModel):
    traffic_spec: TrafficSpec = Field(description="任务规格", alias="TrafficSpec")