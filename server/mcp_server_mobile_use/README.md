[English](README_en.md) | 简体中文

# 云手机 Mobile Use MCP Server

## 产品描述
**OS Agent - Mobile Use** 是基于火山引擎云手机与方舟大模型能力，在移动端安卓环境中完成各类自动化开放式任务的通用 AI Agent 解决方案

**Mobile Use MCP Server** 面向 Agent 任务预集成云手机常用工具，兼容标准MCP协议，提供便捷高效的云手机操作能力，可自动化执行云手机多并发和异步任务，助力企业与个人开发者探索移动端智能化业务场景

- **版本**：v0.0.1
- **分类**：视频云，云手机
- **标签**：OS-Agent，云手机，移动端
- **描述**：本工具集基于 MCP（Model Context Protocol）协议实现，具备良好的扩展性和兼容性，适配火山引擎云手机产品。所有工具均以标准接口形式对外开放，便于集成到各类自动化平台和业务系统中

## MCP Tools
### Tools 列表
| 工具名称          | 工具描述                     |
|-------------------|---------------------------------------|
| `take_screenshot` | 截图云手机屏幕           |
| `text_input`           | 输入文本到云手机           |
| `tap`             | 点击指定坐标 [x,y]                   |
| `swipe`           | 执行滑动操作           |
| `home`            | 返回云手机主屏幕                      |
| `back` | 回到云手机上一级页面                  |
| `menu` | 打开云手机菜单页面                  |
| `autoinstall_app` | 自动下载安装指定应用                  |
| `launch_app` | 启动云手机应用                  |
| `close_app` | 关闭云手机应用                  |
| `list_apps` | 列出云手机上全部应用                  |

### Tools 详细说明
### 1. take_screenshot
**描述**：对云手机屏幕进行截图，返回截图下载链接和屏幕宽高信息  

**输入参数**：
```json
{
  "type": "object",
  "properties": {}
}
```
**输出示例**：
```json
{
  "result": {
    "screenshot_url": "截图下载URL",
    "width": 1080,
    "height": 1920
  }
}
```

### 2. text_input
**描述**：在云手机屏幕上输入指定文本  

**输入参数**：
```json
{
  "type": "object",
  "properties": {
    "text": {
      "description": "The text to input", // 要输入的文本内容 
      "type": "string"
    }
  },
  "required": [
    "text"
  ]
}
```
**输出示例**：
```json
{
  "result": "Input text successfully"
}
```

### 3. tap
**描述**：在云手机屏幕上点击指定坐标

**输入参数**：
```json
{
  "type": "object",
  "properties": {
    "x": {
      "description": "The x coordinate of the tap point", // x坐标
      "type": "number"
    },
    "y": {
      "description": "The y coordinate of the tap point", // y坐标
      "type": "number"
    }
  },
  "required": [
    "x",
    "y"
  ]
}
```

**输出示例**：
```json
{
  "result": "Tap the screen successfully"
}
```

### 4. swipe
**描述**：在云手机屏幕上执行滑动操作，默认滑动时间 300毫秒 

**输入参数**：
```json
{
  "type": "object",
  "properties": {
    "from_x": {
      "description": "The x coordinate of the start point", // 起点x坐标
      "type": "number"
    },
    "from_y": {
      "description": "The y coordinate of the start point", // 起点y坐标
      "type": "number"
    },
    "to_x": {
      "description": "The x coordinate of the end point", // 终点x坐标
      "type": "number"
    },
    "to_y": {
      "description": "The y coordinate of the end point", // 终点y坐标  
      "type": "number"
    }
  },
  "required": [
    "from_x",
    "from_y",
    "to_x",
    "to_y"
  ]
}
```

**输出示例**：
```json
{
  "result": "Swipe the screen successfully"
}
```

### 5. home
**描述**：模拟按下主页Home键操作  

**输入参数**：
```json
{
  "type": "object",
  "properties": {}
}
```
**输出示例**：
```json
{
  "result": "Go home successfully"
}
```

### 6. back
**描述**：模拟按下返回键操作  

**输入参数**：
```json
{
  "type": "object",
  "properties": {}
}
```
**输出示例**：
```json
{
  "result": "Back successfully"
}
```

### 7. menu
**描述**：模拟按下菜单键操作  

**输入参数**：
```json
{
  "type": "object",
  "properties": {}
}
```
**输出示例**：
```json
{
  "result": "Open the Menu successfully"
}
```

### 8. autoinstall_app
**描述**：在云手机中下载并自动安装应用  

**输入参数**：
```json
{
  "type": "object",
  "properties": {
    "app_name": {
      "description": "The app name to be uploaded", // 应用名称 
      "type": "string"
    },
    "download_url": {
      "description": "The download url of the app", // 下载链接
      "type": "string"
    }
  },
  "required": [
    "download_url",
    "app_name"
  ]
}
```

**输出示例**：
```json
{
  "result": "Apk is being installed"
}
```

### 9. launch_app
**描述**：启动指定包名的应用  

**输入参数**：
```json
{
  "type": "object",
  "properties": {
    "package_name": {
      "description": "The package name of apk", // 应用包名  
      "type": "string"
    }
  },
  "required": [
    "package_name"
  ]
}
```

**输出示例**：
```json
{
  "result": "Launch app successfully"
}
```

### 10. close_app
**描述**：关闭运行中的应用  

**输入参数**：
```json
{
  "type": "object",
  "properties": {
    "package_name": {
      "description": "The package name of apk", // 应用包名  
      "type": "string"
    }
  },
  "required": [
    "package_name"
  ]
}
```

**输出示例**：
```json
{
  "result": "Close app successfully"
}
```

### 11. list_apps
**描述**：列出云手机上全部应用  

**输入参数**：
```json
{
  "type": "object",
  "properties": {}
}
```

**输出示例**：
```json
{
  "result": {
    "AppList": [
      {
        "app_id": "",
        "app_name": "抖音",
        "app_status": "undeployed",
        "package_name": "com.ss.android.ugc.aweme"
      }
    ]
  }
}
```
## 适配平台  
方舟，Trae，Python，Cursor

## 服务开通
[火山引擎云手机](https://www.volcengine.com/product/ACEP)       
云手机实例适配MCP的详细资源和特殊镜像要求请咨询相关对接人员

[火山引擎对象存储](https://www.volcengine.com/product/TOS)    
[火山引擎方舟大模型](https://www.volcengine.com/product/ark)

## 快速开始
### 1.编译
请确保已安装 Go 1.23 及以上版本。
```bash
./build.sh
```
编译完成后，二进制文件将输出至 `output/` 目录：
- `output/mobile_use_mcp`：MCP Server 主程序
- `output/cap_tos` 等：其他辅助工具

### 2. 本地启动
MCP Server 支持三种启动模式：`stdio` 、 `sse` 和 `streamable-http`。
#### 2.1 stdio 模式
适用于通过标准输入输出与 MCP Server 通信的场景。在启动前需设置以下**环境变量**：

| 变量名           | 说明                  |
|------------------|-----------------------|
| ACEP_ACCESS_KEY  | 云手机访问密钥        |
| ACEP_SECRET_KEY  | 云手机访问密钥 Secret |
| ACEP_PRODUCT_ID  | 云手机业务 ID         |
| ACEP_DEVICE_ID   | 云手机设备 ID         |
| TOS_ACCESS_KEY   | TOS 访问密钥          |
| TOS_SECRET_KEY   | TOS 访问密钥 Secret   |
| ACEP_TOS_BUCKET  | TOS 存储桶名称        |
| ACEP_TOS_REGION  | TOS 区域              |
| ACEP_TOS_ENDPOINT| TOS Endpoint          |

**Go 代码示例：通过 stdio 方式连接 MCP Server 并调用 take_screenshot 工具**
```go
// stdio 方式调用代码示例
func main() {
    ctx := context.Background()
    // MCP Server 可执行文件路径
    cmd := "./output/mobile_use_mcp"
    // 环境变量（需替换为实际值）
    env := []string{
        "ACEP_ACCESS_KEY=<your-access-key>",
        "ACEP_SECRET_KEY=<your-secret-key>",
        "ACEP_PRODUCT_ID=<your-product-id>",
        "ACEP_DEVICE_ID=<your-device-id>",
        "TOS_ACCESS_KEY=<tos-access-key>",
        "TOS_SECRET_KEY=<tos-secret-key>",
        "ACEP_TOS_BUCKET=<tos-bucket>",
        "ACEP_TOS_REGION=<tos-region>",
        "ACEP_TOS_ENDPOINT=<tos-endpoint>",
    }
    args := []string{"--transport", "stdio"}
    cli, err := mobile_use_client.NewMobileUseStdioClient(ctx, cmd, env, args...)
    if err != nil {
        log.Fatal(err)
    }
    defer cli.Close()
    req := mcp.CallToolRequest{}
    req.Params.Name = "take_screenshot"
    req.Params.Arguments = map[string]interface{}{}
    result, err := cli.CallTool(ctx, req)
    if err != nil {
        log.Fatal(err)
    }
    log.Println("截图结果:", result)
}
```
> 说明：请将 `<your-access-key>`、`<your-secret-key>`、`<your-product-id>`、`<your-device-id>`、`<your-auth-token>`、`<tos-access-key>`、`<tos-secret-key>`、`<tos-bucket>`、`<tos-region>`、`<tos-endpoint>` 替换为实际值。其他工具调用只需修改 `req.Params.Name` 及 `Arguments` 字段。

#### 2.2 HTTP模式
适用于通过 HTTP 协议与 MCP Server 通信的场景。
**启动命令:**
```bash
./output/mobile_use_mcp --transport (sse/streamable-http) --port 8080
```
- `--transport`/`-t`：指定启动模式，支持 `stdio` 、 `sse` 和 `streamable-http`，默认 `stdio`
- `--port`/`-p`：指定 HTTP 服务监听端口，在 `sse` 和 `streamable-http` 模式下生效，默认 `8080`

**HTTP 方式 header 字段说明:**

| Header 名称         | 说明                |
|---------------------|---------------------|
| Authorization       | 鉴权 token          |
| X-ACEP-ProductId    | 云手机业务 ID       |
| X-ACEP-DeviceId     | 云手机实例 ID       |
| X-ACEP-TosBucket    | TOS 存储桶名称      |
| X-ACEP-TosRegion    | TOS 区域            |
| X-ACEP-TosEndpoint  | TOS Endpoint        |
| X-ACEP-TosSession   | TOS Session Token   |

**SSE 方式 AuthInfo 字段说明:**

| 字段名           | 类型   | 说明                              |
|------------------|--------|-----------------------------------|
| AccessKeyId      | string | 火山访问密钥 ID（必填）           |
| SecretAccessKey  | string | 火山访问密钥 Secret（必填）       |
| CurrentTime      | string | 当前时间（RFC3339，必填）         |
| ExpiredTime      | string | 过期时间（RFC3339，必填）         |
| SessionToken     | string | 火山临时 Token（可选）            |

**Go 代码示例：通过 SSE 方式连接 MCP Server 并调用 take_screenshot 工具**

```go
// token 生成
// 假设 AuthInfo 结构体定义如下
type AuthInfo struct {
	AccessKeyId     string `json:"AccessKeyId"`
	SecretAccessKey string `json:"SecretAccessKey"`
	CurrentTime     string `json:"CurrentTime"`
	ExpiredTime     string `json:"ExpiredTime"`
	SessionToken    string `json:"SessionToken"`
}

func GenerateAuthToken(accessKey, secretKey, sessionToken string) (string, error) {
	now := time.Now().Format(time.RFC3339)
	expired := time.Now().Add(24 * time.Hour).Format(time.RFC3339)
	auth := &AuthInfo{
		AccessKeyId:     accessKey,
		SecretAccessKey: secretKey,
		CurrentTime:     now,
		ExpiredTime:     expired,
		SessionToken:    sessionToken,
	}
	authBytes, err := json.Marshal(auth)
	if err != nil {
		return "", err
	}
	authToken := base64.StdEncoding.EncodeToString(authBytes)
	return authToken, nil
}
```

**Go 代码示例：通过 SSE 方式连接 MCP Server 并调用 take_screenshot 工具**

```go
// SSE 方式调用代码示例
func main() {
    ctx := context.Background()
    baseUrl := "http://0.0.0.0:8080/sse"
    cli, err := mobile_use_client.NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
        "Authorization":      authToken,           // 鉴权token
        "X-ACEP-ProductId":   "<your-product-id>", // 云手机业务ID
        "X-ACEP-DeviceId":    "<your-device-id>",  // 云手机实例ID
        "X-ACEP-TosBucket":   "<your-tos-bucket>", // TOS 存储桶名称
        "X-ACEP-TosRegion":   "<your-tos-region>", // TOS 区域
        "X-ACEP-TosEndpoint": "<your-tos-endpoint>", // TOS Endpoint
        "X-ACEP-TosSession":  "",
    })
    if err != nil {
        log.Fatal(err)
    }
    defer cli.Close()
    req := mcp.CallToolRequest{}
    req.Params.Name = "take_screenshot"
    req.Params.Arguments = map[string]interface{}{}
    result, err := cli.CallTool(ctx, req)
    if err != nil {
        log.Fatal(err)
    }
    log.Println("截图结果:", result)
}
```
**Go 代码示例：通过 streamable-http 方式连接 MCP Server 并调用 take_screenshot 工具**

```go
func main() {
    ctx := context.Background()
    baseUrl := "http://0.0.0.0:8080/mcp"
    cli, err := mobile_use_client.NewMobileUseStreamableHTTPClient(ctx, baseUrl, map[string]string{
        "Authorization":      authToken,           // 鉴权token
        "X-ACEP-ProductId":   "<your-product-id>", // 云手机业务ID
        "X-ACEP-DeviceId":    "<your-device-id>",  // 云手机实例ID
        "X-ACEP-TosBucket":   "<your-tos-bucket>", // TOS 存储桶名称
        "X-ACEP-TosRegion":   "<your-tos-region>", // TOS 区域
        "X-ACEP-TosEndpoint": "<your-tos-endpoint>", // TOS Endpoint
        "X-ACEP-TosSession":  "",
    })
    if err != nil {
        log.Fatal(err)
    }
    defer cli.Close()
    req := mcp.CallToolRequest{}
    req.Params.Name = "take_screenshot"
    req.Params.Arguments = map[string]interface{}{}
    result, err := cli.CallTool(ctx, req)
    if err != nil {
        log.Fatal(err)
    }
    log.Println("截图结果:", result)
}
```

> 说明：请将 `<your-access-key>`、`<your-secret-key>`、`<your-product-id>`、`<your-device-id>` 等替换为实际值。其他工具调用只需修改 `req.Params.Name` 及 `Arguments` 字段。

### 3. 其他说明
- 启动后可通过 MCP 协议客户端与 Server 进行交互，具体接口和参数详见工具说明。
- 如需自定义构建参数或交叉编译，请参考 `build.sh` 脚本内容。

## License
volcengine/mcp-server is licensed under the MIT License.
