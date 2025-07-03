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

func TestStreamableHTTPClient(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0:8080/mcp"
	cli, err := NewMobileUseStreamableHTTPClient(ctx, baseUrl, map[string]string{
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

	terminateReq := mcp.CallToolRequest{}
	terminateReq.Params.Name = "test"
	terminateReq.Params.Arguments = map[string]interface{}{
		"reason": "test1",
	}
	result, err := cli.CallTool(ctx, terminateReq)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(result)
}

func TestStreamableHTTPClientListTools(t *testing.T) {
	ctx := context.Background()
	baseUrl := "http://0.0.0.0:8080/mcp"
	cli, err := NewMobileUseStreamableHTTPClient(ctx, baseUrl, map[string]string{
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

	req := mcp.ListToolsRequest{}
	resp, err := cli.ListTools(ctx, req)
	if err != nil {
		t.Fatal(err)
	}
	t.Log(resp)
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
