# Model Context Protocol Marketplace

火山引擎大模型生态广场的 MCP Server 共享仓库，支持用户探索与体验大模型丰富生态服务，轻松集成全面且易用的工具，同时享受企业级稳定、高效、安全的技术支持，充分释放模型潜力，赋能创新应用开发。

[火山引擎大模型生态广场](https://www.volcengine.com/mcp-marketplace) 目前已上线 100+ MCP Server，集成丰富的火山引擎官方云服务及优质三方生态工具。同时支持用户结合火山方舟大模型服务，快速跳转至火山方舟或其他支持 MCP 协议的平台（如 Trae、Cursor、Python 等），助力企业开发者精准打造符合自身业务场景的 AI 大模型应用，打通大模型应用落地的 “最后一公里”。

## 产品优势

- **丰富的资源集成：** 整合了丰富的云上资源及优质的三方服务，提供火山引擎官方云服务 MCP Server，如数据库、存储等，同时集成了各类三方生态工具，从而为客户提供更多生产可用且高价值的各类工具及资源。
- **灵活的部署模式：** 提供 Local 及 Remote 的MCP服务部署模式，灵活适配企业客户的多样化应用场景。
- **端到端应用的生态打通：** 依托字节系生态资源，轻松构建端到端的 AI 应用。用户可在生态广场选择所需的 MCP服务，结合[火山方舟](https://console.volcengine.com/ark/region:ark+cn-beijing/overview?briefPage=0&briefType=introduce&projectName=default&type=new)提供的大模型服务，跳转至火山方舟或支持 MCP 协议的Trae等平台快速开发构建应用。

## 使用指引

1. **查看 MCP Server 详情**

​	在火山引擎[大模型生态广场](https://www.volcengine.com/mcp-marketplace)，选择合适的 MCP Server，并查看详情。

2. **选择 MCP Server 即将运行的平台**

​	检查当前 MCP Server 已适配的平台，并选择合适的平台。

3. **查看并对比可用的 Tools**

​	仔细查看可用的 Tools 的功能描述与所需的输入参数，并尝试试运行对应的功能。

4. **获取专属的URL或代码示例**

​	检查账号登录状态与服务开通情况，生成唯一 URL 或代码示例。

5. **前往MCP Client 中进行安装与使用**

​	复制 URL 或 JSON，前往支持的MCP Client中进行安装与使用 MCP Server。

## MCP Client 支持列表

- **火山方舟**：目前 MCP 服务已支持体验中心与高代码应用
- **Trae**
- **Cursor**
- **Python**

## MCP Server 列表

MCP Server列表 与 **[火山引擎大模型生态广场](https://www.volcengine.com/mcp-marketplace)** 同步。

### 计算

- **[ECS MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_ecs)**：自然语言驱动对云服务器实例和镜像进行资源管理
- **[云助手 MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_cloud_assistant)**：自然语言驱动向云服务器实例发送和执行自定义命令

### 存储

- **[TOS MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_tos)**：基于 MCP 管理 TOS 资源，智能化探索数据
- **[TLS MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_tls)**：自然语言驱动日志分析新体验
- **[EBS MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_ebs)**：提供火山引擎 EBS (弹性块存储) 服务的 MCP 接口，支持查询云盘和快照信息，帮助开发者快速集成 EBS 存储管理能力到 AI 应用中

### 数据库

- **[RDS MySQL MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_rds_mysql)**：云数据库 MySQL 版是即开即用、稳定可靠、灵活弹性、易于使用的关系型数据库服务
- **[MongoDB MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_mongodb)**：自然语言驱动向火山引擎文档数据库 MongoDB 版实例发送和执行自定义命令
- **[CloudSearch MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_cloudsearch)**：云搜索服务（Cloud Search）是火山引擎提供的全托管一站式信息检索和分析平台
- **[veDB MySQL MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_vedb_mysql)**：云数据库 veDB MySQL 版采用计算存储分离架构，100% 兼容 MySQL，最多支持 200TiB 的超大容量结构化数据存储，单个数据库集群最多可扩展至 16 个计算节点

### 容器与中间件

- **[veFaaS MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_vefaas_function)**：veFaaS MCP Server 助你轻松管理函数和触发器生命周期
- **[veFaaS Sandbox MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_vefaas_sandbox)**：面向 LLM 的代码沙箱
- **[veFaaS browser-use MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_vefaas_browser_use)**：基于 Browser-use 的 MCP 浏览器工具

### 大数据

- **[LAS MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_las)**：LAS 提供多模态数据集管理及清洗能力
- **[ByteHouse MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_bytehouse)**：ByteHouse MCP Server 实现大语言模型与 ByteHouse 的高效协同，支持数据开发（生成代码并应用）、查询优化（分析建议转化为策略）、集群运维（风险预测与处理）

### 安全

- **[安全智能体 MCP](https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_sec_agent)**：AI 驱动的安全运营代理，整合火山安全自有工具及第三方生态的一站式智能安全运营服务

### 搜索工具

- **[汉得 - 精准营销](https://github.com/koudaiDemon/mcp-server-hand)**：通过分析用户对话，精准提取多维度标签，与行业数据库中的商品标签智能匹配，精准推荐商品，提升购物体验与转化率
- **[水滴信用 - 企业大数据](https://github.com/shuididata/mcp-server)**：用好数据服务好企业，企业信用信息服务商
- **[飞常准 - Aviation](https://github.com/variflight/variflight-mcp)**：飞友科技推出的民航数据服务平台，适配 MCP 协议，提供 7 个核心 API 接口（航班动态、OD 查询、中转方案、乘机舒适度、飞机定位、机场天气、机票运价），降低 AI Agent 开发门槛
- **[Brave Search](https://github.com/modelcontextprotocol/servers/tree/main/src/brave-search)**：Web and local search using Brave's Search API
- **[Fetch](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)**：Web content fetching and conversion for efficient LLM usage
- **[Tavily search](https://github.com/RamXX/mcp-tavily)**：An MCP server for Tavily's search & news API, with explicit site inclusions/exclusions
- **[AWS KB Retrieval](https://github.com/modelcontextprotocol/servers/tree/main/src/aws-kb-retrieval-server)**：Retrieval from AWS Knowledge Base using Bedrock Agent Runtime
- **[Youtube](https://github.com/ZubeidHendricks/youtube-mcp-server)**：Comprehensive YouTube API integration for video management, Shorts creation, and analytics.
- **[FireCrawl](https://github.com/vrknetha/mcp-server-firecrawl)**：Advanced web scraping with JavaScript rendering, PDF support, and smart rate limiting
- **[Exa](https://github.com/exa-labs/exa-mcp-server)**：Search Engine made for AIs by Exa
- **[Kagi Search](https://github.com/kagisearch/kagimcp)**：Search the web using Kagi's search API
- **[Meilisearch](https://github.com/meilisearch/meilisearch-mcp)**：Interact & query with Meilisearch (Full-text & semantic search API)
- **[Qdrant](https://github.com/qdrant/mcp-server-qdrant/)**：Implement semantic memory layer on top of the Qdrant vector search engine
- **[Search1API](https://github.com/fatwang2/search1api-mcp)**：One API for Search, Crawling, and Sitemaps
- **[Glean](https://github.com/longyi1207/glean-mcp-server)**：A server that uses Glean API to search and chat
- **[Pinecone](https://github.com/sirmews/mcp-pinecone)**：MCP server for searching and uploading records to Pinecone
- **[Elasticsearch](https://github.com/cr7258/elasticsearch-mcp-server)**：MCP server implementation that provides Elasticsearch interaction

### 位置服务

- **高德地图**：高德地图官方 MCP Server
- **[百度地图](https://github.com/baidu-maps/mcp)**：百度地图核心 API 现已全面兼容 MCP 协议，是国内首家兼容 MCP 协议的地图服务商
- **[Google Maps](https://github.com/modelcontextprotocol/servers/tree/main/src/google-maps)**：Location services, directions, and place details
- **[FlightRadar24](https://github.com/sunsetcoder/flightradar24-mcp-server)**：A Claude Desktop MCP server that helps you track flights in real-time using Flightradar24 data

### 内容生成

- **[咔片 - 智能生成 PPT](https://github.com/cappt-team/mcp-server)**：咔片，轻量化在线演示设计
- **[必优 - ChatPPT](https://github.com/YOOTeam/chatppt-mcp)**：必优科技智能文档 MCP Server 覆盖 18 个智能文档接口能力，支持 PPT 创作、美化、生成及简历处理等
- **[Figma](https://github.com/GLips/Figma-Context-MCP)**：为 Agent 提供 Figma 文件的布局和样式信息，增强它们准确生成设计的能力
- **[EverArt](https://github.com/modelcontextprotocol/servers/tree/main/src/everart)**：AI image generation using various models

### 开发者工具

- **[云登 - 云端指纹浏览器](https://github.com/clpublic/mcp-server-cloudbrowser-go)**：提供云端浏览器自动化交互
- **[Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)**：Dynamic and reflective problem-solving through thought sequences
- **[Everything](https://github.com/modelcontextprotocol/servers/tree/main/src/everything)**：Reference / test server with prompts, resources, and tools
- **[Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)**：Knowledge graph-based persistent memory system
- **[Puppeteer](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer)**：Browser automation and web scraping
- **[Browserbase](https://github.com/browserbase/mcp-server-browserbase)**：Automate browser interactions in the cloud (e.g. web navigation, data extraction, form filling, and more)
- **[JetBrains](https://github.com/JetBrains/mcp-jetbrains)**：Work on your code with JetBrains IDEs
- **[Raygun](https://github.com/MindscapeHQ/mcp-server-raygun)**：Interact with your crash reporting and real using monitoring data on your Raygun account
- **[Dify](https://github.com/YanxingLiu/dify-mcp-server)**：A simple implementation of an MCP server for dify workflows
- **[Docker](https://github.com/ckreiling/mcp-server-docker)**：Integrate with Docker to manage containers, images, volumes, and networks
- **[Drupal](https://github.com/Omedia/mcp-server-drupal)**：Server for interacting with Drupal using STDIO transport layer
- **[HuggingFace Spaces](https://github.com/evalstate/mcp-hfspace)**：Server for using HuggingFace Spaces, supporting Open Source Image, Audio, Text Models and more
- **[mcp-k8s-go](https://github.com/strowk/mcp-k8s-go)**：Golang-based Kubernetes server for MCP to browse pods and their logs, events, namespaces and more
- **[Minima](https://github.com/dmayboroda/minima)**：MCP server for RAG on local files
- **[oatpp-mcp](https://github.com/oatpp/oatpp-mcp)**：C++ MCP integration for Oat++
- **[OpenAPI](https://github.com/snaggle-ai/openapi-mcp-server)**：Interact with OpenAPI APIs
- **[OpenCTI](https://github.com/Spathodea-Network/opencti-mcp)**：Interact with OpenCTI platform to retrieve threat intelligence data
- **[OpenRPC](https://github.com/shanejonas/openrpc-mpc-server)**：Interact with and discover JSON-RPC APIs via OpenRPC

### 源码管理

- **[GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/github)**：Repository management, file operations, and GitHub API integration
- **[E2B](https://github.com/e2b-dev/mcp-server)**：Run code in secure sandboxes hosted by E2B
- **[Git](https://github.com/modelcontextprotocol/servers/tree/main/src/git)**：Tools to read, search, and manipulate Git repositories
- **[GitLab](https://github.com/modelcontextprotocol/servers/tree/main/src/gitlab)**：GitLab API, enabling project management
- **[Sentry](https://github.com/modelcontextprotocol/servers/tree/main/src/sentry)**：Retrieving and analyzing issues from Sentry.io

### 数据查询

- **[Neon](https://github.com/neondatabase/mcp-server-neon)**：Interact with the Neon serverless Postgres platform
- **[PostgreSQL](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)**：Read-only database access with schema inspection
- **[Sqlite](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)**：Database interaction and business intelligence capabilities
- **[Axiom](https://github.com/axiomhq/mcp-server-axiom)**：Query and analyze your Axiom logs, traces, and all other event data in natural language
- **[Cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)**：Deploy, configure & interrogate your resources on the Cloudflare developer platform (e.g. Workers/KV/R2/D1)
- **[Metoro](https://github.com/metoro-io/metoro-mcp-server)**：Query and interact with kubernetes environments monitored by Metoro
- **[MotherDuck](https://github.com/motherduckdb/mcp-server-motherduck)**：Query and analyze data with MotherDuck and local DuckDB
- **[Neo4j](https://github.com/neo4j-contrib/mcp-neo4j/)**：Neo4j graph database server (schema + read/write-cypher) and separate graph database backed memory
- **[Tinybird](https://github.com/tinybirdco/mcp-tinybird)**：Interact with Tinybird serverless ClickHouse platform
- **[Chroma](https://github.com/privetin/chroma)**：Vector database server for semantic document search and metadata filtering, built on Chroma
- **[MySQL](https://github.com/designcomputer/mysql_mcp_server)**：MySQL database integration in Python with configurable access controls and schema inspection
- **[Data Exploration](https://github.com/reading-plus-ai/mcp-server-data-exploration)**：MCP server for autonomous data exploration on csv-based datasets, providing intelligent insights with minimal effort
- **[Dataset Viewer](https://github.com/privetin/dataset-viewer)**：Browse and analyze Hugging Face datasets with features like search, filtering, statistics, and data export
- **[MongoDB](https://github.com/volcengine/mcp-server.git/tree/master/server/mcp_server_mongodb)**：A Model Context Protocol Server for MongoDB
- **[MSSQL](https://github.com/RichardHan/mssql_mcp_server)**：MSSQL database integration with configurable access controls and schema inspection

### 文件管理

- **[Excel](https://github.com/negokaz/excel-mcp-server)**：A Model Context Protocol (MCP) server that reads and writes MS Excel data.
- **[XMind](https://github.com/apeyroux/mcp-xmind)**：Read and search through your XMind directory containing XMind files.
- **[Filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)**：Secure file operations with configurable access controls
- **[Google Drive](https://github.com/modelcontextprotocol/servers/tree/main/src/gdrive)**：File access and search capabilities for Google Drive
- **[Fireproof](https://github.com/fireproof-storage/mcp-database-server)**：Immutable ledger database with live synchronization
- **[Needle](https://github.com/needle-ai/needle-mcp)**：Production-ready RAG out of the box to search and retrieve data from your own documents
- **[Cloudinary](https://github.com/felores/cloudinary-mcp-server)**：Cloudinary Model Context Protocol Server to upload media to Cloudinary and get back the media link and details
- **[Pandoc](https://github.com/vivekVells/mcp-pandoc)**：MCP server for seamless document format conversion using Pandoc

### 协作沟通

- **[ChatSum](https://github.com/mcpso/mcp-server-chatsum)**：Query and Summarize chat messages with LLM
- **[Notion](https://github.com/v-3/notion-server)**：Notion MCP integration. Search, Read, Update, and Create pages through Claude chat
- **[ChatMCP](https://github.com/AI-QL/chat-mcp)**：An Open Source Cross-platform GUI Desktop application compatible with Linux, macOS, and Windows, enabling seamless interaction with MCP servers across dynamically selectable LLMs
- **[Google Calendar](https://github.com/v-3/google-calendar)**：Integration with Google Calendar to check schedules, find time, and add/delete events
- **[Slack](https://github.com/modelcontextprotocol/servers/tree/main/src/slack)**：Channel management and messaging capabilities
- **[Google Tasks](https://github.com/zcaceres/gtasks-mcp)**：Google Tasks API Model Context Protocol Server

### 金融财务

- **[coin_api_mcp](https://github.com/longmans/coin_api_mcp)**：Provides access to coinmarketcap cryptocurrency data

### 其他

- **[Time](https://github.com/modelcontextprotocol/servers/tree/main/src/time)**：Time and timezone conversion capabilities
- **[Spotify](https://github.com/varunneal/spotify-mcp)**：This MCP allows an LLM to play and use Spotify
- **[cognee-mcp](https://github.com/topoteretes/cognee/tree/main/cognee-mcp)**：GraphRAG memory server with customizable ingestion, data processing and search
- **[Contentful-mcp](https://github.com/ivo-toby/contentful-mcp)**：Read, update, delete, publish content in your Contentful space(s) from this MCP Server
- **[Home Assistant](https://github.com/tevonsb/homeassistant-mcp)**：Interact with Home Assistant including viewing and controlling lights, switches, sensors, and all other Home Assistant entities
- **[Placid.app](https://github.com/felores/placid-mcp-server)**：Generate image and video creatives using Placid.app templates
- **[Playwright](https://github.com/executeautomation/mcp-playwright)**：This MCP Server will help you run browser automation and webscraping using Playwright

## MCP Protocol 支持

- [Typescript MCP SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP intro](https://modelcontextprotocol.io/introduction)

  AKTP0Va2TjJS7QbIFd422OsDxBPZnX0ZAjLD4InOuqPs33

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
