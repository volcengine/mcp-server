# 安全智能体 MCP
![产品Logo](https://lf3-beecdn.bytetos.com/obj/ies-fe-bee-upload/bee_prod/biz_950/tos_0855c1b4f81b28c3aac545acc022f484.svg)

安全智能体是火山引擎提供的AI 原生安全运营服务，提供「低成本、高效率、全兼容」的一站式智能安全运营服务，助力企业摆脱多工具割裂困境，实现「机器做流程，人做判断」的新一代安全范式。

| 版本 | v0.1.0                   | 
|----|--------------------------|
| 描述 | AI 驱动的安全运营代理，整合火山安全自有工具及第三方生态的一站式智能安全运营服务 |
| 分类 | 安全                       |
| 标签 | 安全，安全智能体，安全值守 |

## 系统依赖
1. 安装 Python 3.11 或者更高版本
2. 安装 uv
### 安装 uv 方法
**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Python >=3.10,<3.12

```bash
pip install -r requirement.txt
```

## 运行方法
```bash
uv sync # 安装依赖
uv run server.py --transport streamable-http --host 0.0.0.0 --port 8000
```
支持的命令行参数： 
- `--transport`：指定 MCP 服务器的传输协议，默认值为 `stdio`，可选项：streamable-http, sse, stdio
- `--host`：指定 MCP 服务器的主机地址，默认值为 `0.0.0.0`。
- `--port`：指定 MCP 服务器的端口号，默认值为 `8000`。

不同的传输协议的URL：
- `streamable-http`：http://<host>:<port>/mcp
- `sse`：http://<host>:<port>/sse

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: alert_investigator

#### 类型

    saas

#### 详细描述

    安全告警智能研判工具，支持结合原始告警数据、关联上下文及安全专家经验进行自动化分析。通过多维度关联分析与知识库匹配，输出研判结论与处置建议

#### 调试所需的输入参数:

输入：

```json 
{
	"inputSchema": {
		"type": "object",
		"required": [
			"alert_msg"
		],
		"properties": {
			"alert_msg": {
				"description": "告警内容：告警的详细信息，如告警时间、告警级别、告警来源、告警内容等。 ",
				"type": "string"
			},
			"data_ref": {
				"description": "关联数据：与告警相关的上下文数据，如终端日志、数据包、流量等。",
				"type": "string"
			},
			"principal": {
				"description": "专家经验：相关的安全专家经验，如安全策略、安全最佳实践、安全专家的分析等。",
				"type": "string"
			}
		}
	},
	"name": "alert_investigator",
	"description": "安全告警智能研判工具，支持结合原始告警数据、关联上下文及安全专家经验进行自动化分析。通过多维度关联分析与知识库匹配，输出研判结论与处置建议"
}
```

输出：

- 告警研判结论

#### 最容易被唤起的 Prompt示例

    使用 alert_investigator 工具，分析告警信息并给出相应的建议。

### Tool 2: pcap_analyzer

#### 类型

    saas

#### 详细描述

    用于深度分析 base64 编码的 pcap 网络流量数据包。支持协议解码、会话重组、异常行为检测和 IOC（威胁情报指标）匹配。通过流量模式分析、元数据提取与专家规则库，输出包括可疑连接统计、协议分布、潜在攻击行为及取证建议的完整报告。

#### 调试所需的输入参数:

输入：

```json 
{
	"inputSchema": {
		"type": "object",
		"required": [
			"pcap"
		],
		"properties": {
			"pcap": {
				"description": "base64 编码的 pcap 文件内容，支持包含完整网络会话的抓包数据",
				"type": "string"
			}
		}
	},
	"name": "pcap_analyzer",
	"description": "网络流量深度分析工具，提供从基础协议解析到高级威胁检测的全维度pcap分析能力"
}
```

输出：

- pcap 包分析结果

#### 最容易被唤起的 Prompt示例

    使用 pcap_analyzer 工具，深度解析此网络抓包文件，识别可疑通信行为并提供取证建议

### Tool 3: sensitive_data_detector

#### 类型

    saas

#### 详细描述

    敏感数据智能识别引擎，支持检测各类敏感数据。支持自定义识别规则与行业合规标准（GDPR/HIPAA/PCIDSS）联动，提供数据定位、风险评级等分析内容

#### 调试所需的输入参数:

输入：

```json 
{
	"inputSchema": {
		"type": "object",
		"required": [
			"file_content"
		],
		"properties": {
			"file_content": {
				"description": "待检测的原始数据内容，支持文本/文档/日志等多种文件内容",
				"type": "string"
			},
			"extract_type": {
				"description": "（可选）自定义敏感数据标准",
				"type": "string"
			}
		}
	},
	"name": "sensitive_data_detector",
	"description": "敏感数据智能识别引擎，支持检测各类敏感数据。支持自定义识别规则与行业合规标准（GDPR/HIPAA/PCIDSS）联动，提供数据定位、风险评级等分析内容"
}
```

输出：

- 敏感数据分析结果

#### 最容易被唤起的 Prompt示例

    使用 sensitive_data_detector 工具，检测此文本文件中的敏感数据

### Tool 4: threat_intel_producer

#### 类型

    saas

#### 详细描述

    威胁情报自动化生产系统，通过自然语言处理与结构化分析引擎，从非结构化安全报告中提取IOC（入侵指标）、TTP（战术技术与过程）、攻击者画像等要素。集成MITRE ATT&CK框架映射，输出符合STIX/TAXII标准的可机读威胁情报。

#### 调试所需的输入参数:

输入：

```json 
{
	"inputSchema": {
		"type": "object",
		"required": [
			"input_msg"
		],
		"properties": {
			"input_msg": {
				"description": "原始情报素材：安全报告/漏洞分析/事件通告等文本内容",
				"type": "string"
			}
		}
	},
	"name": "threat_intel_producer",
	"description": "非结构化情报结构化转换工具，实现从安全文本到可执行威胁情报的自动化生产流水线"
}
```

输出：

- 结构化情报结果

#### 最容易被唤起的 Prompt示例

    使用 threat_intel_producer 工具，解析此APT组织分析报告并生成可操作的STIX格式情报

### Tool 5: web_risk_assessor

#### 类型

    saas

#### 详细描述

    网页安全风险多维评估系统，通过视觉特征分析、备案信息核验与威胁情报交叉比对，识别钓鱼网站/仿冒页面等各类网页风险。

#### 调试所需的输入参数:

输入：

```json 
{
	"inputSchema": {
		"type": "object",
		"required": [
			"snapshot"
		],
		"properties": {
			"snapshot": {
				"description": "网页截图链接（需支持直接下载）",
				"type": "string"
			},
			"url": {
				"description": "（可选）网页原始URL",
				"type": "string"
			},
			"icp_info": {
				"description": "（可选）ICP备案信息",
				"type": "string"
			}
		}
	},
	"name": "web_risk_assessor",
	"description": "网页安全风险多维评估系统，通过视觉特征分析、备案信息核验与威胁情报交叉比对，识别钓鱼网站/仿冒页面等各类网页风险。"
}
```

输出：

- 网页风险评估结论

#### 最容易被唤起的 Prompt示例

    使用 web_risk_assessor 工具，分析该金融网站截图是否为钓鱼仿冒页面

### Tool 6: dlp_screenshot_analyzer

#### 类型

    saas

#### 详细描述

    数据防泄漏智能检测平台，识别终端截图中的敏感文档操作、数据外发等违规行为。支持检测多类高风险操作场景（含代码泄露/财务数据展示/客户信息浏览等内容）。

#### 调试所需的输入参数:

输入：

```json
{
	"inputSchema": {
		"type": "object",
		"required": [
			"snapshot"
		],
		"properties": {
			"snapshot": {
				"description": "终端屏幕截图访问链接（需支持直接下载）",
				"type": "string"
			}
		}
	},
	"name": "dlp_screenshot_analyzer",
	"description": "终端操作行为深度解析工具，通过视觉内容分析实现精准的数据防泄漏检测"
}
```

输出：

- 截图分析结果

#### 最容易被唤起的 Prompt示例

    使用 dlp_screenshot_analyzer 工具，分析研发人员终端截图是否存在源代码违规外发行为

### Tool 7: alert_formatter

#### 类型

    saas

#### 详细描述

    告警参数格式化工具，用于从原始告警信息中提取核心攻击特征。通过结构化解析和关键字段提取，将非结构化的原始告警转换为标准化的安全事件特征表示，为后续分析研判提供规范化输入。

#### 调试所需的输入参数:

输入：

```json
{
	"inputSchema": {
		"type": "object",
		"required": [
			"alert_msg"
		],
		"properties": {
			"alert_msg": {
				"description": "原始告警内容：包含完整细节的非结构化告警信息，通常包括时间戳、事件类型、源/目的IP、端口、协议等原始数据。",
				"type": "string"
			}
		}
	},
	"name": "alert_formatter",
	"description": "从原始告警中提取标准化攻击特征的工具，输出包含关键字段的结构化数据"
}
```

输出：

- 结构化特征对象

#### 最容易被唤起的 Prompt示例

    使用 alert_formatter 工具，分析该原始告警，提取关键攻击特征

## 可适配平台

    方舟和三方MCP Client

## 服务开通链接 (整体产品)

    https://console.volcengine.com/intelligent

## 鉴权方式

    火山引擎AKSK鉴权体系

### 环境变量

以下环境变量可用于配置MCP服务器:

| 环境变量             | 描述                     | 默认值 |
|------------------|------------------------|-----|
| `VOLC_ACCESSKEY` | 火山引擎账号 ACCESS KEY      | -   |
| `VOLC_SECRETKEY` | 火山引擎账号 SECRET KEY      | -   |

## 安装部署

### 系统依赖

- 安装 Python 3.10 或者更高版本
- 安装 uv
    - 如果是linux系统
  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
    - 如果是window系统
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- 同步依赖项并更uv.lock:
  ```bash
  uv sync
  ```
- 构建mcp server:
  ```bash
  uv build
  ```

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-git*.

### Using PIP

Alternatively you can install `mcp-server-git` via pip:

```
pip install mcp-server-git
```

After installation, you can run it as a script using:

```
python -m mcp_server_git
```

## 在不同平台的配置

### 方舟

#### 体验中心

[示例如下]

1. 查看MCP Server 详情
   在大模型生态广场，选择合适的MCP Server，并查看详情
2. 选择MCP Server即将运行的平台
   检查当前MCP Server 已适配的平台，并选择合适的平台
3. 查看并对比可用的Tools
   仔细查看可用的Tools的功能描述与所需的输入参数，并尝试运行对应的功能。
4. 获取专属的URL或代码示例
   检查账号登录状态与服务开通情况，生成唯一URL
5. 去对应的Client的平台进行使用
   点击快捷跳转按钮，前往方舟平台的体验中心进行对应MCP Server的体验

## 资源列表 - optional

## 商业化 - optional

## 产品截图/视频 - optional

### Cursor

## 部署

### Run Locally

#### Option1

```json
{
  "mcpServers": {
    "sec-agent-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/src/mcp_server_sec_agent",
        "run",
        "mcp-server-sec-agent"
      ]
    }
  }
}
```

#### Option2

```json
{
    "mcpServers": {
        "sec-agent": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/volcengine/ai-app-lab#subdirectory=mcp/server/mcp_server_sec_agent",
                "mcp-server-sec-agent"
            ],
            "env": {
                "VOLC_ACCESSKEY": "your ak",
                "VOLC_SECRETKEY": "your sk",
            }
        }
    }
}
```

## License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
