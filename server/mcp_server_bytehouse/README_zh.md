## MCP Server 产品名称
ByteHouse MCP Server
## 版本信息
v25.4
## 产品描述
ByteHouse MCP Server有着不可替代的作用。它可以实现大语言模型（LLMs）与ByteHouse的高效协同。在数据开发方面，大语言模型能够根据开发者的自然语言描述生成相应的代码，而ByteHouse MCP Server则可以将这些代码准确地应用到ByteHouse实例中，避免了开发者手动编写代码时可能出现的错误和繁琐过程，大大提高了数据开发的效率。在查询优化环节，大语言模型可以分析查询需求和数据特点，提出优化建议，ByteHouse MCP Server则能将这些建议转化为实际的优化策略应用于ByteHouse实例，从而提升查询性能。对于集群运维，大语言模型可以预测潜在的问题和风险，ByteHouse MCP Server会及时将这些信息反馈给ByteHouse实例，并协助采取相应的措施进行预防和处理。
## 分类
大数据
## 标签
企业版，云数仓版，Search，智能助手

## 产品视频
<video src="https://lf3-static.bytednsdoc.com/obj/eden-cn/lm_sth/ljhwZthlaukjlkulzlp/ark/mcpserverhub/readme_videos/bytehouse_mcp.mp4" controls>
</video>

## Tools
本 MCP Server 产品提供以下 Tools (工具/能力):
### list_database
在进行数据管理和操作时，有时我们需要了解当前 ByteHouse 实例中所包含的数据库情况。此时，可以执行特定的查询操作，该工具操作的目的是查询当前 ByteHouse 实例下的所有数据库，通过此查询，系统将会返回该实例下存在的所有数据库。
### list_tables
查询当前ByteHouse实例中指定数据库下的所有数据表，并将查询到的所有数据表信息进行返回
### run_select_query
通过交互式执行 SELECT 查询语句来进行数据分析工作。在面对各种复杂的数据环境时，该助手能够精准地依据用户所提供的 SELECT 查询语句，在相应的数据库中进行数据检索操作，最终返回精确的查询结果。而且，更为重要的是，它不会仅仅止步于返回查询结果，还会对这些查询结果进一步进行全面且深入的分析说明。它会从多个维度去剖析这些数据，例如数据的分布规律、数据之间的关联关系、数据所反映出的潜在趋势等等，从而为用户提供更为详尽且有价值的信息，帮助用户更好地理解和利用这些数据。 
### run_dml_ddl_query
能够实现可交互地执行数据操作语言（DML）以及数据定义语言（DDL）的 SQL 语句。在使用者输入相关的 DML/DDL SQL 语句后，该助手会迅速对语句进行处理并执行，之后及时反馈执行结果，同时还会对执行结果给出详细的解释，帮助使用者更好地理解操作的过程和最终产生的影响。  
## 最容易被唤起的 Prompt示例
### list_database
我想要查询当前所使用的集群环境中，都存在哪些数据库。具体来说，希望获取该集群内所有已创建数据库的名称等相关信息，以便进一步对这些数据库进行管理、分析或者使用等操作。 
### list_tables
我想要查询数据库名为 {database name} 的这个数据库中具体包含了哪些数据表。 
### run_select_query
帮忙查询一下集群存储目前的水位情况，包括各个存储节点当前的使用容量、剩余容量以及占总容量的百分比等详细信息。 
## 可适配平台  
火山方舟，Cursor，Visual Studio Code,Trae

## 服务开通链接 (整体产品)  
如下产品开通任意一个即可

企业版： `https://console.volcengine.com/bytehouse-ce`     
云数仓版： `https://console.volcengine.com/bytehouse`

## 鉴权方式  
用户开通Bytehouse企业版或Bytehouse云数仓版实例，在集群管理获取IP、端口、用户名、密码，并配置到MCP configure

## 安装部署  
如下已本地部署为例进行说明,操作系统macOS：

### Setp 1
在方舟平台开通大模型服务（豆包或DeepSeek),并获取API KEY

### Setp 2
本地安装Cursor，Visual Studio Code，Trae

### Setp 3
下载mcp-bytehouse安装包，执行如下命令运行mcp-bytehouse 服务 

<font color="red"> ***注意！Python版本需要3.12***</font>

```
export BYTEHOUSE_HOST="<your_bytehouse_host>"
export BYTEHOUSE_PORT="<your_bytehouse_port>"
export BYTEHOUSE_USER="<your_bytehouse_user>"
export BYTEHOUSE_PASSWORD="<your_bytehouse_password>"
export BYTEHOUSE_SECURE="true"
export BYTEHOUSE_VERIFY="true"
export BYTEHOUSE_CONNECT_TIMEOUT="60"
export BYTEHOUSE_SEND_RECEIVE_TIMEOUT="60"

pip install -r requirements.txt
python3 -m mcp_bytehouse.main -t sse
```
### Setp 4 
本地cursor，Visual Studio Code，Trae 安装插件Cline

### Setp 5
Cline配置大模型地址及其API KEY,同时按照如下模版配置mcp configure
```
{
  "mcpServers": {
    "mcp_bytehouse":{
        "url":"https://<your_hostname>:8000/sse"
    }
  }
}
```
## License
Apache License