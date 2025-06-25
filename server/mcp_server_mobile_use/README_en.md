# Volcano Engine Cloud Phone (ACEP) - Mobile Use MCP Server

## Product Description
**OS Agent - Mobile Use** is a general AI Agent solution based on Volcano Engine's Cloud Phone (ACEP) and Ark large model capabilities, designed to complete various automated open-ended tasks in mobile Android environments.

**Mobile Use MCP Server** pre-integrates commonly used cloud phone tools for Agent tasks, compatible with standard MCP protocol. It provides convenient and efficient cloud phone operation capabilities, enabling automated execution of multi-concurrency and asynchronous tasks on cloud phones, helping enterprises and individual developers explore intelligent mobile business scenarios.

- **Version**: v0.0.1
- **Category**: Video Cloud, Cloud Phone
- **Tags**: OS-Agent, Cloud Phone, Mobile
- **Description**: This toolkit is implemented based on MCP (Model Context Protocol) protocol, featuring excellent scalability and compatibility with Volcano Engine's Cloud Phone products. All tools are exposed through standard interfaces for easy integration into various automation platforms and business systems.

## MCP Tools
### Tools List
| Tool Name          | Description                     |
|--------------------|---------------------------------|
| `take_screenshot` | Capture cloud phone screen      |
| `text_input`       | Input text to cloud phone       |
| `tap`             | Tap specified coordinates [x,y]|
| `swipe`           | Perform swipe operation         |
| `home`            | Return to home screen           |
| `back`            | Go back to previous page        |
| `menu`            | Open menu page                  |
| `autoinstall_app` | Auto download & install app     |
| `launch_app`      | Launch app                      |
| `close_app`       | Close running app               |
| `list_apps`       | List all installed apps         |

### Detailed Tool Specifications
### 1. take_screenshot
**Description**: Capture cloud phone screen and return screenshot URL with screen dimensions  

**Input Parameters**:
```json
{
  "type": "object",
  "properties": {}
}
```
**Output Example**: 
```json
{
  "result": {
    "screenshot_url": "Screenshot download URL",
    "width": 1080,
    "height": 1920
  }
}
```

### 2. text_input
**Description**: Input specified text on cloud phone screen  

**Input Parameters**:
```json
{
  "type": "object",
  "properties": {
    "text": {
      "description": "The text to input", // Text content 
      "type": "string"
    }
  },
  "required": [
    "text"
  ]
}
```

**Output Example**: 
```json
{
  "result": "Input text successfully"
}
```

### 3. tap
**Description**: Tap specified coordinates on screen  

**Input Parameters**:
```json
{
  "type": "object",
  "properties": {
    "x": {
      "description": "The x coordinate of the tap point", // X coordinate
      "type": "number"
    },
    "y": {
      "description": "The y coordinate of the tap point", // Y coordinate  
      "type": "number"
    }
  },
  "required": [
    "x",
    "y"
  ]
}
```

**Output Example**:
```json
{
  "result": "Tap the screen successfully"
}
```

### 4. swipe
**Description**: Perform swipe operation (default duration 300ms)  

**Input Parameters**:
```json
{
  "type": "object",
  "properties": {
    "from_x": {
      "description": "The x coordinate of the start point", // Start X
      "type": "number"
    },
    "from_y": {
      "description": "The y coordinate of the start point", // Start Y
      "type": "number"
    },
    "to_x": {
      "description": "The x coordinate of the end point", // End X
      "type": "number"
    },
    "to_y": {
      "description": "The y coordinate of the end point", // End Y 
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

**Output Example**: 
```json
{
  "result": "Swipe the screen successfully"
}
```

### 5. home
**Description**: Simulate Home button press  

**Input Parameters**: 
```json
{
  "type": "object",
  "properties": {}
}
```

**Output Example**: 
```json
{
  "result": "Go home successfully"
}
```

### 6. back
**Description**: Simulate Back button press  

**Input Parameters**: 
```json
{
  "type": "object",
  "properties": {}
}
```

**Output Example**: 
```json
{
  "result": "Back successfully"
}
```

### 7. menu
**Description**: Simulate Menu button press  

**Input Parameters**: 
```json
{
  "type": "object",
  "properties": {}
}
```

**Output Example**: 
```json
{
  "result": "Open the Menu successfully"
}
```

### 8. autoinstall_app
**Description**: Download and auto-install app  

**Input Parameters**:
```json
{
  "type": "object",
  "properties": {
    "app_name": {
      "description": "The app name to be uploaded", // Application name  
    },
    "download_url": {
      "description": "The download url of the app", // Download URL
      "type": "string"
    }
  },
  "required": [
    "download_url",
    "app_name"
  ]
}
```

**Output Example**: 
```json
{
  "result": "Apk is being installed"
}
```

### 9. launch_app
**Description**: Launch app by package name  

**Input Parameters**:
```json
{
  "type": "object",
  "properties": {
    "package_name": {
      "description": "The package name of apk", // Package name  
      "type": "string"
    }
  },
  "required": [
    "package_name"
  ]
}
```

**Output Example**: 
```json
{
  "result": "Launch app successfully"
}
```

### 10. close_app
**Description**: Close running app  

**Input Parameters**:
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

**Output Example**: 
```json
{
  "result": "Close app successfully"
}
```

### 11. list_apps
**Description**: List all installed apps  

**Input Parameters**: 
```json
{
  "type": "object",
  "properties": {}
}
``` 

**Output Example**:
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

## Supported Platforms
Ark，Trae，Python，Cursor

## Product Activation
[Volcano Engine Cloud Phone](https://www.volcengine.com/product/ACEP)       
Consult relevant personnel for MCP-compatible Cloud Phone resource requirements.

[Volcano Engine TOS](https://www.volcengine.com/product/TOS)    
[Volcano Engine ARK](https://www.volcengine.com/product/ark)

## Quick Start
### 1.Build
Ensure Go 1.23+ is installed.
```bash
./build.sh
```
Built binaries will be in `output/` ：
- `output/mobile_use_mcp`：MCP Server main program
- `output/cap_tos` etc.：Auxiliary tools

### 2. Local Deployment
MCP Server supports three startup modes: `stdio`, `streamable-http` and `sse`.
#### 2.1 stdio Mode
Suitable for scenarios where communication with the MCP Server is via standard input and output. Set the following **environment variables** before startup:

| Variable Name      | Description                  |
|-------------------|-----------------------|
| ACEP_ACCESS_KEY  | Cloud Phone Access Key        |
| ACEP_SECRET_KEY  | Cloud Phone Access Key Secret |
| ACEP_PRODUCT_ID  | Cloud Phone Business ID         |
| ACEP_DEVICE_ID   | Cloud Phone Device ID         |
| TOS_ACCESS_KEY   | TOS Access Key          |
| TOS_SECRET_KEY   | TOS Access Key Secret   |
| ACEP_TOS_BUCKET  | TOS Bucket Name        |
| ACEP_TOS_REGION  | TOS Region              |
| ACEP_TOS_ENDPOINT| TOS Endpoint          |

**Go Code Example: Connect to MCP Server via stdio and call take_screenshot tool**
```go
// stdio method call example
func main() {
    ctx := context.Background()
    // Path to the MCP Server executable file
    cmd := "./output/mobile_use_mcp"
    // Environment variables (replace with actual values)
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
    log.Println("Screenshot result:", result)
}
```
> Note: Replace `<your-access-key>`, `<your-secret-key>`, `<your-product-id>`, `<your-device-id>`, `<your-auth-token>`, `<tos-access-key>`, `<tos-secret-key>`, `<tos-bucket>`, `<tos-region>`, and `<tos-endpoint>` with actual values. For calling other tools, simply modify the req.Params.Name and Arguments fields.

#### 2.2 HTTP Mode
Suitable for scenarios where communication with the MCP Server is conducted via HTTP protocol.

**Startup command:**
```bash
./output/mobile_use_mcp --transport (sse/streamable-http) --port 8080
```
- `--transport`/`-t`: Specify startup mode, supports `stdio`, `sse`, and `streamable-http`, default `stdio`
- `--port`/`-p`: Specify HTTP service listening port, effective in `sse` and `streamable-http` modes, default `8080`

**SSE method header field descriptions:**

| Header Name         | Description                |
|---------------------|---------------------|
| Authorization       | Authentication token          |
| X-ACEP-ProductId    | Cloud Phone Business ID       |
| X-ACEP-DeviceId     | Cloud Phone Instance ID       |
| X-ACEP-TosBucket    | TOS Bucket Name      |
| X-ACEP-TosRegion    | TOS Region            |
| X-ACEP-TosEndpoint  | TOS Endpoint        |
| X-ACEP-TosSession   | TOS Session Token   |

**SSE method AuthInfo field descriptions:**

| Field Name         | Type   | Description                              |
|-------------------|--------|-----------------------------------|
| AccessKeyId      | string | Volcano Access Key ID (required)           |
| SecretAccessKey  | string | Volcano Access Key Secret (required)       |
| CurrentTime      | string | Current time (RFC3339, required)         |
| ExpiredTime      | string | Expiration time (RFC3339, required)         |
| SessionToken     | string | Volcano temporary Token (optional)            |

```go
// Token generation
// Assuming AuthInfo struct is defined as follows
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

**Go Code Example: Connect to MCP Server via SSE and call take_screenshot tool**

```go
// SSE method call example
func main() {
    ctx := context.Background()
    baseUrl := "http://0.0.0.0:8080/sse"
    cli, err := mobile_use_client.NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
        "Authorization":      authToken,           // Authentication token
        "X-ACEP-ProductId":   "<your-product-id>", // Cloud Phone Business ID
        "X-ACEP-DeviceId":    "<your-device-id>",  // Cloud Phone Instance ID
        "X-ACEP-TosBucket":   "<your-tos-bucket>", // TOS Bucket Name
        "X-ACEP-TosRegion":   "<your-tos-region>", // TOS Region
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
    log.Println("Screenshot result:", result)
}
```

**Go Code Example: Connect to MCP Server via streamable-http and call take_screenshot tool**

```go
func main() {
    ctx := context.Background()
    baseUrl := "http://0.0.0.0:8080/mcp"
    cli, err := mobile_use_client.NewMobileUseStreamableHTTPClient(ctx, baseUrl, map[string]string{
        "Authorization":      authToken,           // Authentication token
        "X-ACEP-ProductId":   "<your-product-id>", // Cloud Phone Business ID
        "X-ACEP-DeviceId":    "<your-device-id>",  // Cloud Phone Instance ID
        "X-ACEP-TosBucket":   "<your-tos-bucket>", // TOS Bucket Name
        "X-ACEP-TosRegion":   "<your-tos-region>", // TOS Region
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
    log.Println("Screenshot result:", result)
}
```

> Note: Replace `<your-access-key>`, `<your-secret-key>`, `<your-product-id>`, `<your-device-id>` etc. with actual values. For calling other tools, simply modify the req.Params.Name and Arguments fields.

### 3. Other Notes
- After startup, you can interact with the Server via an MCP protocol client. For specific interfaces and parameters, refer to the tool documentation.
- If you need to customize build parameters or perform cross - compilation, refer to the content of the `build.sh` script.

## License
volcengine/mcp-server is licensed under the MIT License.
