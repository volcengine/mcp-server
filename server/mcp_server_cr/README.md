# CR MCP Server

## 版本信息
v1.0.0

## 产品描述

CR MCP Server 是一个 Model Context Protocol 服务器，为 MCP 客户端
（如 Cursor、Claude Desktop 等）提供与火山引擎 CR 服务交互的能力。 
通过自然语言即可对 CR 镜像仓库实例，命名空间，OCI 制品仓库 等资源进行管理，
支持镜像仓库实例，命名空间，OCI 制品仓库等资源的查询和创建操作，
帮助用户高效管理云上镜像仓库。

## 分类

容器与中间件 - 容器服务

## 功能

- 创建镜像仓库实例
- 查询镜像仓库实例列表
- 创建命名空间
- 查询命名空间列表
- 创建 OCI 制品仓库
- 查询 OCI 制品仓库列表
- 查询镜像仓库 tag 列表
- 查询镜像仓库域名列表
- 获取镜像仓库临时密码

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力)，对应的说明也可以参考 https://www.volcengine.com/docs/6420/79198 
对应 API 的信息描述

### Tool 1: list_registries

#### 详细描述

查询镜像仓库实例列表

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "description": "参数对象"
      },
      "body": {
        "type": "object",
        "properties": {
          "Filter": {
            "type": "object",
            "description": "待查询镜像仓库实例的过滤条件",
            "properties": {
              "Names": {
                "type": "array",
                "description": "指定镜像仓库实例或远端代理仓名称，支持精确匹配和模糊匹配",
                "items": {
                  "type": "string"
                }
              },
              "Types": {
                "type": "array",
                "description": "镜像仓库实例类型，可选值：Basic、Trial、Enterprise、Micro",
                "items": {
                  "type": "string"
                }
              },
              "Projects": {
                "type": "array",
                "description": "关联的项目名称",
                "items": {
                  "type": "string"
                }
              },
              "Statuses": {
                "type": "array",
                "description": "镜像仓库实例的状态",
                "items": {
                  "type": "object",
                  "properties": {
                    "Phase": {
                      "type": "string",
                      "description": "实例状态阶段"
                    },
                    "Condition": {
                      "type": "string",
                      "description": "实例状态条件"
                    }
                  }
                }
              }
            }
          },
          "ResourceTagFilters": {
            "type": "array",
            "description": "查询镜像仓库实例标签的过滤条件",
            "items": {
              "type": "object",
              "required": [
                "Key",
                "Values"
              ],
              "properties": {
                "Key": {
                  "type": "string",
                  "description": "标签的 Key 值"
                },
                "Values": {
                  "type": "array",
                  "description": "标签的 Value 值",
                  "items": {
                    "type": "string"
                  }
                }
              }
            }
          },
          "PageSize": {
            "type": "integer",
            "description": "单页展示的镜像仓库实例数量，默认为 10 个，取值范围为 [1,100] 的整数"
          },
          "PageNumber": {
            "type": "integer",
            "description": "开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647] 的整数"
          }
        }
      }
    }
  },
  "name": "list_registries",
  "description": "查询一个或多个镜像仓库实例"
}
```
输出
- 镜像仓库实例查询结果

#### 最容易被唤起的 Prompt示例

创建镜像仓库实例

### Tool 2: create_registry

#### 详细描述

创建镜像仓库实例列表

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Name": {
            "type": "string",
            "description": "标准版实例名称，支持小写英文字母、数字、短划线（-），长度限制为 3～30 个字符"
          },
          "Type": {
            "type": "string",
            "description": "实例类型，默认创建标准版实例"
          },
          "Project": {
            "type": "string",
            "description": "实例需要关联的项目"
          },
          "ResourceTags": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "Key": {
                  "type": "string",
                  "description": "标签的 Key 值"
                },
                "Value": {
                  "type": "string",
                  "description": "标签的 Value 值"
                }
              },
              "required": ["Key", "Value"]
            }
          },
          "ClientToken": {
            "type": "string",
            "description": "用于保证请求幂等性的字符串，最大值不超过 64 个 ASCII 字符"
          },
          "ProxyCacheEnabled": {
            "type": "boolean",
            "description": "是否为远端代理仓"
          },
          "ProxyCache": {
            "type": "object",
            "properties": {
              "Type": {
                "type": "string",
                "description": "远端代理仓支持的类型"
              },
              "Endpoint": {
                "type": "string",
                "description": "源镜像的访问地址"
              },
              "Password": {
                "type": "string",
                "description": "访问源镜像所需的用户名或者 SecretAccessKey"
              },
              "Username": {
                "type": "string",
                "description": "访问源镜像所需的密码或者 AccessKeyID"
              },
              "SkipSSLVerify": {
                "type": "boolean",
                "description": "是否忽略 SSL 证书验证"
              }
            },
            "required": ["Type"]
          }
        },
        "required": ["Name"]
      }
    }
  },
  "name": "create_registry",
  "description": "创建镜像仓库标准版实例"
}
```
输出
- 无

#### 最容易被唤起的 Prompt示例

请帮我创建一个名为 xxx 的镜像仓库标准版实例

### Tool 3: create_namespace

#### 详细描述

在镜像仓库实例下创建命名空间

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Registry": {
            "type": "string",
            "description": "指定的镜像仓库实例名称"
          },
          "Name": {
            "type": "string",
            "description": "命名空间名称，支持小写英文、数字、英文句号（.）、短划线（-）、下划线（_），长度限制为 2～90 个字符"
          },
          "ClientToken": {
            "type": "string",
            "description": "用于保证请求幂等性的字符串，最大值不超过 64 个 ASCII 字符"
          },
          "Project": {
            "type": "string",
            "description": "命名空间所属项目的名称，不超过 64 个字符"
          },
          "RepositoryDefaultAccessLevel": {
            "type": "string",
            "description": "命名空间下新建 OCI 制品仓库的默认公开属性，默认 Private"
          }
        },
        "required": ["Registry", "Name"]
      }
    }
  },
  "name": "create_namespace",
  "description": "在指定的镜像仓库实例下创建命名空间"
}
```
输出
- 无

#### 最容易被唤起的 Prompt示例

请帮我在镜像仓库实例 xxx 下创建一个名为 xxx 的命名空间

### Tool 4: get_authorization_token

#### 详细描述

获取镜像仓库登录的临时访问秘钥

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Registry": {
            "type": "string",
            "description": "镜像仓库实例的名称"
          }
        },
        "required": ["Registry"]
      }
    }
  },
  "name": "get_authorization_token",
  "description": "获取登录镜像仓库实例的临时访问密钥"
}
```

输出
- 镜像仓库临时访问秘钥

#### 最容易被唤起的 Prompt示例

请输出镜像仓库实例 xxx 的临时访问秘钥

### Tool 5: list_domains

#### 详细描述

获取镜像仓库实例的域名列表

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Registry": {
            "type": "string",
            "description": "要查询域名的镜像仓库实例名称"
          },
          "PageSize": {
            "type": "number",
            "description": "单页展示的域名信息数量，默认为 10 个，取值范围为 [1,100]"
          },
          "PageNumber": {
            "type": "number",
            "description": "开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647]"
          }
        },
        "required": ["Registry"]
      }
    }
  },
  "name": "list_domains",
  "description": "查询镜像仓库实例域名"
}
```
输出
- 镜像仓库域名列表

#### 最容易被唤起的 Prompt示例

请帮我查询一下 XX 镜像仓库的域名

### Tool 6: list_tags

#### 详细描述

查询镜像仓库实例下的 tag 列表

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Registry": {
            "type": "string",
            "description": "指定 OCI 制品仓库所属的镜像仓库实例名称"
          },
          "Namespace": {
            "type": "string",
            "description": "指定 OCI 制品仓库所属的命名空间名称"
          },
          "Repository": {
            "type": "string",
            "description": "指定 OCI 制品仓库名称"
          },
          "Filter": {
            "type": "object",
            "properties": {
              "Names": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "指定 Tag，支持精确匹配和模糊匹配，最多 20 个"
              },
              "Types": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "OCI 制品 Tag 类型，取值为 Image 或 Chart"
              }
            }
          },
          "PageSize": {
            "type": "number",
            "description": "单页展示的 OCI 制品版本数量，默认为 10 个，取值范围为 [1,100]"
          },
          "PageNumber": {
            "type": "number",
            "description": "开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647]"
          },
          "SortBy": {
            "type": "string",
            "description": "搜索制品版本的排序条件"
          }
        },
        "required": ["Registry", "Namespace", "Repository"]
      }
    }
  },
  "name": "list_tags",
  "description": "查询指定 OCI 制品仓库下的一个或多个 OCI 制品（镜像、Helm Chart）版本"
}
```
输出
- tag 列表信息

#### 最容易被唤起的 Prompt示例

请帮我查询一下镜像仓库实例 xxx 的 xxx 命名空间 xxx 制品仓库下的 tags 

### Tool 7: create_repository

#### 详细描述

创建镜像仓库制品仓库

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Registry": {
            "type": "string",
            "description": "指定命名空间所属的镜像仓库实例名称"
          },
          "Namespace": {
            "type": "string",
            "description": "目标命名空间名称"
          },
          "Name": {
            "type": "string",
            "description": "OCI 制品仓库名称，支持小写英文、数字、分隔符，长度限制为 1～128 个字符"
          },
          "Description": {
            "type": "string",
            "description": "OCI 制品仓库描述信息，长度不超过 300 个字符"
          },
          "AccessLevel": {
            "type": "string",
            "description": "OCI 制品仓库的类型，默认值为 Private"
          },
          "ClientToken": {
            "type": "string",
            "description": "用于保证请求幂等性的字符串，最大值不超过 64 个 ASCII 字符"
          }
        },
        "required": ["Registry", "Namespace", "Name"]
      }
    }
  },
  "name": "create_repository",
  "description": "在指定命名空间下创建 OCI 制品仓库"
}
```
输出
- 无

#### 最容易被唤起的 Prompt示例

请帮我在 xxx 镜像仓库实例 xxx 命名空间下创建 xxx OCI制品仓库

### Tool 8: list_repositories

#### 详细描述

查询镜像仓库实例下的制品仓库列表

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Registry": {
            "type": "string",
            "description": "指定镜像仓库实例名称"
          },
          "Filter": {
            "type": "object",
            "properties": {
              "Namespaces": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "指定 OCI 制品仓库所属的命名空间，最多 20 个"
              },
              "Names": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "指定 OCI 制品仓库名称，最多 20 个"
              },
              "AccessLevels": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "访问等级，取值为 Private 或 Public"
              }
            }
          },
          "PageSize": {
            "type": "number",
            "description": "单页展示的 OCI 制品仓库数量，默认为 10 个，取值范围为 [1,100]"
          },
          "PageNumber": {
            "type": "number",
            "description": "开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647]"
          }
        },
        "required": ["Registry"]
      }
    }
  },
  "name": "list_repositories",
  "description": "查询指定镜像仓库实例下的一个或多个 OCI 制品仓库"
}
```
输出
- 制品仓库列表信息

#### 最容易被唤起的 Prompt示例

请列出我在 xxx 镜像仓库实例 xxx 命名空间下的制品仓库

### Tool 9: list_namespaces

#### 详细描述

查询镜像仓库实例下的命名空间列表

#### 调试所需的输入参数:
输入：
```json 
{
  "inputSchema": {
    "type": "object",
    "properties": {
      "params": {
        "type": "object",
        "properties": {}
      },
      "body": {
        "type": "object",
        "properties": {
          "Registry": {
            "type": "string",
            "description": "指定的镜像仓库实例名称"
          },
          "Filter": {
            "type": "object",
            "properties": {
              "Names": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "指定命名空间名称，最多 20 个"
              },
              "Projects": {
                "type": "array",
                "items": {
                  "type": "string"
                },
                "description": "筛选用户所属的项目"
              },
              "InProject": {
                "type": "boolean",
                "description": "筛选 namespace 是否在项目中"
              }
            }
          },
          "PageSize": {
            "type": "number",
            "description": "单页展示的命名空间数量，默认为 10 个，取值范围为 [1,100]"
          },
          "PageNumber": {
            "type": "number",
            "description": "开始显示返回结果的页码，从 1 开始，默认为 1，取值范围为 [1,2147483647]"
          }
        },
        "required": ["Registry"]
      }
    }
  },
  "name": "list_namespaces",
  "description": "查询指定镜像仓库实例下的单个或多个命名空间"
}
```
输出
- 命名空间列表信息

#### 最容易被唤起的 Prompt示例

请列出我在 xxx 镜像仓库实例下的命名空间列表

## 鉴权方式  

API Key (<a href="https://www.volcengine.com/docs/6731/942192">签名机制</a>)

## 安装部署  

### 系统依赖
- 安装 Python3.10或更高版本
- 安装uv
  - MacOS/Linux
  ```text
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  - Windows
  ```text
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 环境变量
| 环境变量名 | 描述 | 默认值 | 获取方式 |
| --- | --- | --- | --- |
| VOLCENGINE_ACCESS_KEY | 火山引擎账号 ACCESS KEY | - | [火山引擎访问控制台](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_SECRET_KEY | 火山引擎账号 SECRET KEY | - | [火山引擎访问控制台](https://console.volcengine.com/iam/keymanage/) |
| VOLCENGINE_REGION | 火山引擎 地域 | cn-beijing | - |

### 部署

UV
```json
{
  "mcpServers": {
    "mcp_server_cr": {
      "command": "uv",
      "env": {
        "VOLCENGINE_ACCESS_KEY":"Your Volcengine access key",
        "VOLCENGINE_SECRET_KEY":"Your Volcengine secret key"
      },
      "args": [
        "--directory",
        "/<your local path to mcp-servers>/server/mcp_server_cr",
        "run",
        "mcp-cr"
      ]
    }
  }
}
```
UVX
```json
{
  "mcpServers": {
    "mcp_server_cr": {
      "command": "uvx",
      "env": {
        "VOLCENGINE_ACCESS_KEY":"Your Volcengine access key",
        "VOLCENGINE_SECRET_KEY":"Your Volcengine secret key"
      },
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_cr",
        "mcp-cr"
      ]
    }
  }
}
```

# License
volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)
