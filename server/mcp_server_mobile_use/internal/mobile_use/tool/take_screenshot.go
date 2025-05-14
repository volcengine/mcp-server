package tool

import (
	"context"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewTakeScreenshotTool() mcp.Tool {
	return mcp.NewTool("take_screenshot",
		mcp.WithDescription("Take a screenshot of the cloud phone screen; if using this tool, please go to VolceEngine TOS and create a bucket."),
	)
}

func HandleTakeScreenshot() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
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
		screenShotUrl, err := handler.ScreenShot(ctx)
		if err != nil {
			return CallResultError(err)
		}
		return CallResultSuccess(screenShotUrl)
	}
}
