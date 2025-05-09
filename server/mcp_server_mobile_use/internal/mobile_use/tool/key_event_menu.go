package tool

import (
	"context"

	"mcp_server_mobile_use/internal/mobile_use/consts"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewKeyEventMenuTool() mcp.Tool {
	return mcp.NewTool("menu",
		mcp.WithDescription("Open the Menu on the cloud phone"),
	)
}

func HandleKeyEventMenuTool() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
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
		err = handler.KeyEvent(ctx, consts.AndroidKeyEventMenu)
		if err != nil {
			return CallResultError(err)
		}
		return CallResultSuccess("Open the Menu successfully")
	}
}
