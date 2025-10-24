# DTS MCP Server
火山引擎数据库传输服务 DTS（Database Transmission Service）是集数据迁移、数据同步和数据订阅于一体的数据库数据传输管理服务，支持关系型数据库、非关系型数据库数据源间的数据传输，降低数据库之间数据流通复杂性，可在业务不停服的前提下轻松完成数据库迁移上云。

## Tools

### 1. `describe_transmission_tasks`
#### 详细描述：
查询用户DTS迁移/订阅/同步任务列表（支持分页查询）,查询时需指定任务类型。根据任务名称查询任务时，支持模糊匹配，不支持正则表达式。

#### 调试所需的输入参数:
- 输入:
    - `task_type`: 任务类型，可选值：DataMigration(数据迁移)、DataSubscription(数据订阅/订阅任务)、DataSynchronization(数据同步)、DataValidation(数据校验)
    - `task_name`: 任务名称
    - `task_ids`: 任务ID列表
    - `task_status`: 任务状态
    - `project`: 项目名称
    - `charge_type`: 计费类型
    - `page_number`: 分页页码
    - `page_size`: 分页大小
- 输出:
    - 任务列表
#### 触发示例：
`"列出我的 DTS 同步任务"`

### 2. `create_transmission_task`
#### 详细描述：
创建迁移/订阅/同步任务。

#### 调试所需的输入参数:
- 输入:
    - `task_type`: 任务类型，可选值：DataMigration(数据迁移)、DataSubscription(数据订阅)、DataSynchronization(数据同步)
    - `src_config`: 源端数据源配置
    - `dest_config`: 目的端数据源配置
    - `object_mappings`: 要迁移/订阅/同步的对象 
    - `task_name`: 任务名称
    - `create_backward_sync_task`: 是否创建反向同步任务
    - `traffic_spec`: 任务规格
    - `project_name`: 项目名称
- 输出:
    - 创建任务的响应结果
#### 触发示例：
`"创建一个DTS同步任务， 源端是专有网络mysql，私网是信息是vpc-3rebt5uf5fr405zsk2if9i3md subnet-2bznv8i16voqo2dx0efg0tngw，地址是192.168.0.65 3306，用户是username，密码是password;目的端是火山mysql mysql-12345，用户是username，密码是password,同步test这个库下面的所有表"`

### 3. `list_vpc`
#### 详细描述：
查询VPC列表.
#### 调试所需的输入参数:
- 输入:
    - 无
- 输出:
    - VPC列表
#### 触发示例：
`"查询VPC列表"`

### 4. `list_vpc_subnets`
#### 详细描述：
查询VPC下的子网列表。
#### 调试所需的输入参数:
- 输入:
    - `vpc_id`: VPC ID
- 输出:
    - VPC下的子网列表
#### 触发示例：
`"查询VPC vpc-12345 下的子网列表"`

### 5. `describe_transmission_task_info`
#### 详细描述：
查询 DTS 迁移/订阅/同步任务的详细信息。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
- 输出:
    - 任务详细信息
#### 触发示例：
`"查询任务 12345 的详细信息"`

### 6. `describe_transmission_task_progress`
#### 详细描述：
查询传输任务的详细进度。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
    - `progress_type`: 进度类型
    - `name`: 同步对象名称，不支持通配符。示例1：查询包含score的进度，name应为score；示例2：仅查询business库中score表的进度，name应为business.score
    - `transmission_state`: 传输状态,可以筛选某个传输状态(如传输中)的进度信息
    - `object_type`: 同步对象类型
    - `latency_desc`: 是否按照表的延迟降序排列
    - `transfer_estimate_rows_desc`: 是否按照表的预估数据行数降序排列
    - `page_number`: 页码
    - `page_size`: 每页数量
- 输出:
    - 传输任务详细进度
#### 触发示例：
`"查询任务 12345 全量阶段的同步进度"`

### 7. `modify_transmission_task`
#### 详细描述：
修改传输/订阅/同步任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
    - `src_config`: 源端数据源配置
    - `dest_config`: 目的端数据源配置
    - `solution_settings`: 解决方案配置
    - `task_name`: 任务名称
    - `traffic_spec`: 任务规格
- 输出:
    - 修改后的任务信息
#### 触发示例：
`"修改指定任务的源端数据源配置"`

### 8. `start_transmission_task`
#### 详细描述：
启动传输任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
#### 触发示例：
`"启动任务 12345"`

### 9. `suspend_transmission_task`
#### 详细描述：
暂停迁移/同步/订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
#### 触发示例：
`"暂停任务 12345"`

### 10. `resume_transmission_task`
#### 详细描述：
恢复传输任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
#### 触发示例：
`"恢复任务 12345"`

### 11. `retry_transmission_task`
#### 详细描述：
重试迁移/同步/订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
#### 触发示例：
`"重试任务 12345"`

### 12. `start_transmission_tasks`
#### 详细描述：
批量启动迁移/同步/订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 任务ID列表
#### 触发示例：
`"启动任务 123 和 456"`

### 13. `suspend_transmission_tasks`
#### 详细描述：
批量暂停迁移/同步/订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 任务ID列表
#### 触发示例：
`"暂停任务 123 和 456"`

### 14. `resume_transmission_tasks`
#### 详细描述：
批量恢复迁移/同步/订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 任务ID列表
#### 触发示例：
`"恢复任务 123 和 456"`

### 15. `retry_transmission_tasks`
#### 详细描述：
批量重试迁移/同步/订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 任务ID列表
#### 触发示例：
`"重试任务 123 和 456"`

### 16. `spawn_swimming_lane`
#### 详细描述：
配置任务多泳道，支持配置表级别泳道，将延迟表拆分到独立泳道进行同步，降低整体延迟。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
    - `database`: 数据库名称
    - `tables`: 表名称列表
#### 触发示例：
`"为任务 1234，business.task表配置泳道"`

### 17. `create_subscription_group`
#### 详细描述：
创建订阅任务消费组，仅支持目的端是内置Kafka的订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
    - `group_name`: 消费组名称
    - `username`: 用户名
    - `password`: 密码
#### 触发示例：
`"为任务 1234 创建消费组 sub，用户密码是 username 和 password"`

### 18. `describe_subscription_groups`
#### 详细描述：
查询订阅任务消费组列表，仅支持目的端是内置Kafka的订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
#### 触发示例：
`"查询任务 1234 的消费组列表"`

### 19. `update_subscription_group`
#### 详细描述：
更新订阅任务消费组，仅支持目的端是内置Kafka的订阅任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
    - `group_name`: 消费组名称
    - `username`: 用户名
    - `password`: 密码
#### 触发示例：
`"更新任务 1234 的消费组 sub，用户密码是 username 和 password2"`

### 20. `precheck_async`
#### 详细描述：
创建预检查任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
- 输出:
    - 预检查任务响应结果，包含预检查ID
#### 触发示例：
`"为任务 1234 创建预检查任务"`

### 21. `get_async_pre_check_result`
#### 详细描述：
根据预检查ID查询预检查结果。
#### 调试所需的输入参数:
- 输入:
    - `precheck_id`: 预检查ID
- 输出:
    - 预检查结果
#### 触发示例：
`"查询预检查任务 1234 的结果"`

### 22. `add_tags_to_resource`
#### 详细描述：
绑定标签到DTS任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 任务ID列表
    - `tags`: 标签列表
#### 触发示例：
`"为任务 12345 添加标签 key1:value1"`

### 23. `remove_tags_from_resource`
#### 详细描述：
解绑DTS任务的标签。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 任务ID列表
    - `tag_keys`: 标签键列表
- 输出:
    - 解绑标签的响应结果
#### 触发示例：
`"为任务 12345 解绑标签 key1"`

### 24. `describe_tags_by_resource`
#### 详细描述：
查询DTS任务的标签。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 任务ID列表
    - `tag_filters`: 标签过滤列表
    - `page_number`: 分页页码
    - `page_size`: 分页大小
- 输出:
    - DTS任务标签信息
#### 触发示例：
`"查询任务 12345 的标签"`

### 25. `modify_instance_order`
#### 详细描述：
将任务计费类型由按量计费转为包年包月计费；或修改DTS任务规格（仅迁移任务和同步任务支持）。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 任务ID
    - `convert_post_paid_to_pre_paid`: 是否将按量计费转为包年包月计费
    - `modify_instance_spec`: 修改实例规格
#### 触发示例：
`"将任务 12345 的计费类型转为包年包月"`

### 26. `create_validation_task`
#### 详细描述：
创建DTS校验任务。
#### 调试所需的输入参数:
- 输入:
    - `parent_task_id`: 校验任务关联的父任务ID
    - `solution_type`: 校验任务解决方案类型
    - `object_mappings`: 要校验的对象 
    - `task_name`: 任务名称
    - `sample_rate`: 全量校验任务采样率
- 输出:
    - 校验任务ID
#### 触发示例：
`"为任务 12345 创建MySQL全量内容校验任务validation1，校验business库下的所有表"`

### 27. `describe_validation_tasks`
#### 详细描述：
查询用户DTS校验任务列表（支持分页查询）,查询时需指定任务类型。根据任务名称查询任务时，支持模糊匹配，不支持正则表达式。
#### 调试所需的输入参数:
- 输入:
    - `name`: 任务名称/任务ID
    - `task_status`: 任务状态
    - `task_sub_type`: 任务子类型
    - `validation_status`: 校验结果
    - `page_number`: 分页页码
    - `page_size`: 分页大小
- 输出:
    - DTS校验任务列表
#### 触发示例：
`"我有哪些DTS校验任务"`

### 28. `describe_validation_task_info`
#### 详细描述：
查询 DTS 校验任务的详细信息。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
- 输出:
    - DTS校验任务详细信息
#### 触发示例：
`"查询校验任务 12345 的详细信息"`

### 29. `start_validation_task`
#### 详细描述：
启动校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
#### 触发示例：
`"启动校验任务 12345"`

### 30. `suspend_validation_task`
#### 详细描述：
暂停校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
#### 触发示例：
`"暂停校验任务 12345"`

### 31. `resume_validation_task`
#### 详细描述：
恢复校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
#### 触发示例：
`"恢复校验任务 12345"`

### 32. `retry_validation_task`
#### 详细描述：
重试校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
#### 触发示例：
`"重试校验任务 12345"`

### 33. `start_validation_tasks`
#### 详细描述：
批量启动校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 校验任务ID列表
#### 触发示例：
`"启动校验任务 12345和67890"`

### 34. `suspend_validation_tasks`
#### 详细描述：
批量暂停校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 校验任务ID列表
#### 触发示例：
`"暂停校验任务 12345和67890"`

### 35. `resume_validation_task`
#### 详细描述：
批量恢复校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 校验任务ID列表
#### 触发示例：
`"恢复校验任务 12345和67890"`

### 36. `retry_validation_tasks`
#### 详细描述：
批量重试校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_ids`: 校验任务ID列表
#### 触发示例：
`"重试校验任务 12345和67890"`

### 37. `download_validation_task_result`
#### 详细描述：
下载校验结果。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
#### 触发示例：
`"下载校验任务 12345 的结果"`

### 38. `describe_validation_task_result`
#### 详细描述：
查询校验任务结果。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
    - `page_number`: 分页页码
    - `page_size`: 分页大小
- 输出:
    - DTS校验任务结果
#### 触发示例：
`"查询校验任务 12345 的结果"`

### 39. `get_db_table_diff_details`
#### 详细描述：
查询增量校验任务库表不一致详情。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
    - `db_name`: 数据库名
    - `table_name`: 表名
    - `page_number`: 分页页码
    - `page_size`: 分页大小
#### 触发示例：
`"查询校验任务 12345 中 business 库下表task的不一致详情"`

### 40. `generate_validation_result_file`
#### 详细描述：
增量校验任务生成校验结果文件。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
#### 触发示例：
`"生成校验任务 12345 的校验结果文件"`

### 41. `describe_supported_validation_types`
#### 详细描述：
查询任务支持的校验任务类型。
#### 调试所需的输入参数:
- 输入:
    - `src_datasource`: 源端数据源信息
    - `dst_datasource`: 目标端数据源信息
#### 触发示例：
`"查询任务 12345 支持的校验任务类型"`

### 42. `modify_validation_task`
#### 详细描述：
修改校验任务。
#### 调试所需的输入参数:
- 输入:
    - `task_id`: 校验任务ID
    - `solution_settings`: 解决方案配置
#### 触发示例：
`"修改校验任务 12345，校验对象改为business2库下的所有表"`

### 43. `create_data_source`
#### 详细描述：
创建数据源。
#### 调试所需的输入参数:
- 输入:
    - `name`: 数据源名称
    - `datasource`: 数据源配置
#### 触发示例：
`"创建DTS数据源mig_src，火山引擎MySQL mysql-abcde，用户名和密码:username password"`

### 44. `list_data_source`
#### 详细描述：
查询数据源列表。
#### 调试所需的输入参数:
- 输入:
    - `categories`: 数据源类型列表
    - `endpoint_types`: 数据源接入方式列表
    - `name_prefix`: 数据源名称前缀
    - `order_by`: 排序规则
    - `page_number`: 分页页码
    - `page_size`: 分页大小
#### 触发示例：
`"我有哪些DTS数据源"`

### 45. `describe_data_source`
#### 详细描述：
查询数据源详细信息。
#### 调试所需的输入参数:
- 输入:
    - `data_source_id`: 数据源ID
#### 触发示例：
`"查询数据源 19458 的详细信息"`

### 46. `modify_data_source`
#### 详细描述：
修改数据源。
#### 调试所需的输入参数:
- 输入:
    - `data_source_id`: 数据源ID
    - `data_source`: 数据源配置
#### 触发示例：
`"修改数据源 19458，实例ID改为 mysql-19754"`

### 47. `delete_data_source`
#### 详细描述：
删除数据源。
#### 调试所需的输入参数:
- 输入:
    - `data_source_id`: 数据源ID
#### 触发示例：
`"删除数据源 19458"`

## 服务开通链接 (整体产品)  
<https://console.volcengine.com/dts>

## 可适配平台  
可以使用 cline, cursor, claude desktop 或支持MCP server调用的的其他终端

## 鉴权方式  
从 volcengine 管理控制台获取 volcengine 访问密钥 ID、秘密访问密钥和区域

### UVX

```json
{
    "mcpServers": {
        "mcp-server-dts": {
            "command": "uvx",
            "args": [
            "--from",
            "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_dts",
            "mcp-server-dts"
          ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your-access-key-id",
                "VOLCENGINE_SECRET_KEY": "your-access-key-secret",
                "VOLCENGINE_REGION": "volcengine region",
                "VOLCENGINE_ENDPOINT": "volcengine endpoint",
            }
        }
    }
}
```

## License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).


