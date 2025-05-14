package tool

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewCloseAppTool() mcp.Tool {
	return mcp.NewTool("close_app",
		mcp.WithDescription("Close a running app on the cloud phone"),
		mcp.WithString("package_name",
			mcp.Description("The package name of apk"),
			mcp.Required(),
		),
	)
}

func HandleCloseAppTool() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
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
		packageName, ok := req.Params.Arguments["package_name"].(string)
		if !ok || packageName == "" {
			return CallResultError(fmt.Errorf("package_name is required"))
		}
		err = handler.CloseApp(ctx, packageName)
		if err != nil {
			return CallResultError(err)
		}
		return CallResultSuccess("Close app successfully")
	}
}
