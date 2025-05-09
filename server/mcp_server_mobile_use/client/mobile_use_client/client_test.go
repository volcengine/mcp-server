package mobile_use_client

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"errors"
	"io"
	"testing"
	"time"

	"mcp_server_mobile_use/internal/mobile_use/config"

	"github.com/mark3labs/mcp-go/mcp"
)

var authToken string

func init() {
	now := time.Now().Format(time.RFC3339)
	expired := time.Now().Add(time.Hour * 24).Format(time.RFC3339)
	auth := &config.AuthInfo{
		AccessKeyId:     "",
		SecretAccessKey: "==",
		CurrentTime:     now,
		ExpiredTime:     expired,
		SessionToken:    "",
	}
	authBytes, _ := json.Marshal(auth)
	authToken = base64.StdEncoding.EncodeToString(authBytes)
}

func TestStdioClient(t *testing.T) {
	ctx := context.Background()
	cmd := "/Users/bytedance/Code/go/bin/mobile_use"
	args := []string{}
	env := []string{
		"ACEP_ACCESS_KEY=12345678901111111",
		"ACEP_SECRET_KEY=12345678901111111",
		"ACEP_PRODUCT_ID=123455",
		"ACEP_DEVICE_ID=123455",
	}

	cli, err := NewMobileUseStdioClient(ctx, cmd, env, args...)
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	terminateReq := mcp.CallToolRequest{}
	terminateReq.Params.Name = "terminate"
	terminateReq.Params.Arguments = map[string]interface{}{
		"reason": "test1",
	}
	result, err := cli.CallTool(ctx, terminateReq)
	if errors.Is(err, io.EOF) {
		t.Log("EOF")
	} else if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClient(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization": authToken,
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()
	req := mcp.ListToolsRequest{}
	resp, err := cli.ListTools(ctx, req)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(resp)

	terminateReq := mcp.CallToolRequest{}
	terminateReq.Params.Name = "terminate"
	terminateReq.Params.Arguments = map[string]interface{}{
		"reason": "test1",
	}
	result, err := cli.CallTool(ctx, terminateReq)
	if errors.Is(err, io.EOF) {
		t.Log("EOF")
	} else if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientTakeScreenshot(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	takeScreenshotReq := mcp.CallToolRequest{}
	takeScreenshotReq.Params.Name = "take_screenshot"
	takeScreenshotReq.Params.Arguments = map[string]interface{}{}
	result, err := cli.CallTool(ctx, takeScreenshotReq)
	if err != nil {
		t.Log(err)
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientType(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	takeScreenshotReq := mcp.CallToolRequest{}
	takeScreenshotReq.Params.Name = "text_input"
	takeScreenshotReq.Params.Arguments = map[string]interface{}{
		"text": "hello",
	}
	result, err := cli.CallTool(ctx, takeScreenshotReq)
	if err != nil {
		t.Log(err)
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientKeyEvent(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	keyEventReq := mcp.CallToolRequest{}
	keyEventReq.Params.Name = "home"
	result, err := cli.CallTool(ctx, keyEventReq)
	if err != nil {
		t.Log(err)
		t.Fatal(err)
	}
	t.Log(result)

	keyEventReq.Params.Name = "menu"
	result, err = cli.CallTool(ctx, keyEventReq)
	if err != nil {
		t.Log(err)
		t.Fatal(err)
	}
	t.Log(result)

	keyEventReq.Params.Name = "back"
	result, err = cli.CallTool(ctx, keyEventReq)
	if err != nil {
		t.Log(err)
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientAutoInstallApp(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})

	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	autoInstallAppReq := mcp.CallToolRequest{}
	autoInstallAppReq.Params.Name = "autoinstall_app"
	autoInstallAppReq.Params.Arguments = map[string]interface{}{
		"download_url": "http://127.0.0.1/test.apk",
	}
	result, err := cli.CallTool(ctx, autoInstallAppReq)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientListApps(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	listAppsReq := mcp.CallToolRequest{}
	listAppsReq.Params.Name = "list_apps"
	result, err := cli.CallTool(ctx, listAppsReq)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientLaunchApp(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	launchAppReq := mcp.CallToolRequest{}
	launchAppReq.Params.Name = "launch_app"
	launchAppReq.Params.Arguments = map[string]interface{}{
		"package_name": "com.autonavi.minimap",
	}
	result, err := cli.CallTool(ctx, launchAppReq)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientCloseApp(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	closeAppReq := mcp.CallToolRequest{}
	closeAppReq.Params.Name = "close_app"
	closeAppReq.Params.Arguments = map[string]interface{}{
		"package_name": "com.autonavi.minimap",
	}
	result, err := cli.CallTool(ctx, closeAppReq)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientScreenSwipe(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	screenSwipeReq := mcp.CallToolRequest{}
	screenSwipeReq.Params.Name = "swipe"
	screenSwipeReq.Params.Arguments = map[string]interface{}{
		"from_x": 100,
		"from_y": 100,
		"to_x":   900,
		"to_y":   100,
	}
	result, err := cli.CallTool(ctx, screenSwipeReq)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestSSEClientScreenTap(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0/sse"
	cli, err := NewMobileUseSSEClient(ctx, baseUrl, map[string]string{
		"Authorization":      authToken,
		"X-ACEP-ProductId":   "",
		"X-ACEP-DeviceId":    "",
		"X-ACEP-TosBucket":   "",
		"X-ACEP-TosRegion":   "",
		"X-ACEP-TosEndpoint": "",
	})
	if err != nil {
		t.Fatal(err)
	}
	defer cli.Close()

	screenTapReq := mcp.CallToolRequest{}
	screenTapReq.Params.Name = "tap"
	screenTapReq.Params.Arguments = map[string]interface{}{
		"x": 100,
		"y": 100,
	}
	result, err := cli.CallTool(ctx, screenTapReq)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
	t.Log("1")
}
