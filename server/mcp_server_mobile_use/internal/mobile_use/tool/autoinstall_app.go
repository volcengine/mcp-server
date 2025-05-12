package tool

import (
	"context"
	"fmt"
	"net/url"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewAppUploadTool() mcp.Tool {
	return mcp.NewTool("autoinstall_app",
		mcp.WithDescription("Download and install an app in one step on the cloud phone"),
		mcp.WithString("download_url",
			mcp.Description("The download url of the app"),
			mcp.Required(),
		),
		mcp.WithString("app_name",
			mcp.Description("The app name to be uploaded"),
			mcp.Required(),
		),
	)
}

func HandleAppUploadTool() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	return func(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		err := CheckAuth(ctx)
		if err != nil {
			return CallResultError(err)
		}
		mobileUseConfig, err := GetMobileUseConfig(ctx)
		if err != nil || mobileUseConfig == nil {
			return CallResultError(err)
		}
		handler, err := InitMobileUseService(ctx, mobileUseConfig)
		if err != nil {
			return CallResultError(err)
		}
		downloadUrl, ok := req.Params.Arguments["download_url"].(string)
		if !ok || downloadUrl == "" {
			return CallResultError(fmt.Errorf("download_url is required"))
		}
		if ok := isUrl(downloadUrl); !ok {
			return CallResultError(fmt.Errorf("download_url is invalid"))
		}
		err = handler.AutoInstallApp(ctx, req.Params.Arguments["download_url"].(string))
		if err != nil {
			return CallResultError(err)
		}
		return CallResultSuccess("Apk is being installed")
	}
}

func isUrl(downloadUrl string) bool {
	parsedUrl, err := url.Parse(downloadUrl)
	if err != nil || (parsedUrl.Scheme != "http" && parsedUrl.Scheme != "https") || parsedUrl.Host == "" {
		return false
	}
	return true
}
