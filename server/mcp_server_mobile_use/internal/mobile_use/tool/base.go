package tool

import (
	"context"
	"fmt"

	"mcp_server_mobile_use/internal/mobile_use/config"
	"mcp_server_mobile_use/internal/mobile_use/consts"
	"mcp_server_mobile_use/internal/mobile_use/service"

	"github.com/mark3labs/mcp-go/mcp"
)

func CheckAuth(ctx context.Context) error {
	authResult := ctx.Value(consts.AuthResult{})
	if authResult == nil || authResult.(string) != consts.AuthResultOk {
		return fmt.Errorf("auth failed")
	}
	return nil
}

func GetMobileUseConfig(ctx context.Context) (*config.MobileUseConfig, error) {
	mobileUseConfig := ctx.Value(consts.MobileUseConfigKey{})
	if mobileUseConfig == nil {
		return nil, fmt.Errorf("mobile use config not found")
	}
	conf := mobileUseConfig.(config.MobileUseConfig)
	return &conf, nil
}

func CallResultError(err error) (*mcp.CallToolResult, error) {
	toolResult := &mcp.CallToolResult{
		Content: []mcp.Content{},
		IsError: true,
	}
	if err != nil {
		toolResult.Content = append(toolResult.Content, mcp.NewTextContent(err.Error()))
	}
	return toolResult, nil
}

func CallResultSuccess(content string) (*mcp.CallToolResult, error) {
	return mcp.NewToolResultText(content), nil
}

func InitMobileUseService(ctx context.Context, mobileUseConfig *config.MobileUseConfig) (service.MobileUseProvider, error) {
	if mobileUseConfig == nil {
		return nil, fmt.Errorf("mobile use config is nil")
	}
	if mobileUseConfig.AuthInfo.AccessKeyId == "" || mobileUseConfig.AuthInfo.SecretAccessKey == "" {
		return nil, fmt.Errorf("get acep auth info failed")
	}
	if mobileUseConfig.BizInfo.ProductId == "" || mobileUseConfig.BizInfo.DeviceId == "" {
		return nil, fmt.Errorf("get acep biz info failed")
	}

	opts := []service.Option{
		service.WithAccessKey(mobileUseConfig.AuthInfo.AccessKeyId),
		service.WithSecretKey(mobileUseConfig.AuthInfo.SecretAccessKey),
		service.WithProductID(mobileUseConfig.BizInfo.ProductId),
		service.WithDeviceID(mobileUseConfig.BizInfo.DeviceId),
	}

	if mobileUseConfig.BizInfo.ACEPHost != "" {
		opts = append(opts, service.WithHost(mobileUseConfig.BizInfo.ACEPHost))
	}

	if mobileUseConfig.AuthInfo.SessionToken != "" {
		opts = append(opts, service.WithSessionToken(mobileUseConfig.AuthInfo.SessionToken))
	}
	if mobileUseConfig.TosInfo.TosBucket != "" {
		opts = append(opts, service.WithBucket(mobileUseConfig.TosInfo.TosBucket))
	}
	if mobileUseConfig.TosInfo.TosRegion != "" {
		opts = append(opts, service.WithRegion(mobileUseConfig.TosInfo.TosRegion))
	}
	if mobileUseConfig.TosInfo.TosEndpoint != "" {
		opts = append(opts, service.WithEndpoint(mobileUseConfig.TosInfo.TosEndpoint))
	}
	if mobileUseConfig.TosInfo.TosAccessKey != "" {
		opts = append(opts, service.WithTosAccessKey(mobileUseConfig.TosInfo.TosAccessKey))
	}
	if mobileUseConfig.TosInfo.TosSecretKey != "" {
		opts = append(opts, service.WithTosSecretKey(mobileUseConfig.TosInfo.TosSecretKey))
	}
	if mobileUseConfig.TosInfo.TosSessionToken != "" {
		opts = append(opts, service.WithTosSessionToken(mobileUseConfig.TosInfo.TosSessionToken))
	}

	handler := service.NewMobileUseImpl(opts...)
	return handler, nil
}

func GetInt64Param(args map[string]interface{}, key string) (int64, error) {
	val, exists := args[key]
	if !exists {
		return 0, fmt.Errorf("%s is required", key)
	}

	switch v := val.(type) {
	case int:
		return int64(v), nil
	case int64:
		return v, nil
	case float64:
		return int64(v), nil
	default:
		return 0, fmt.Errorf("%s must be an integer, got %T", key, val)
	}
}

func CheckArgs(args any) (map[string]interface{}, error) {
	if args == nil {
		return nil, fmt.Errorf("args is nil")
	}
	res, ok := args.(map[string]interface{})
	if !ok {
		return nil, fmt.Errorf("args is invalid")
	}
	return res, nil
}
