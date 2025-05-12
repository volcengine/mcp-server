package tool

import (
	"context"
	"encoding/json"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewListAppTool() mcp.Tool {
	return mcp.NewTool("list_apps",
		mcp.WithDescription("List all apps installed on cloud phone"),
	)
}

func HandleListAppTool() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
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
		appList, err := handler.ListApps(ctx)
		if err != nil {
			return CallResultError(err)
		}
		result := map[string]interface{}{
			"AppList": appList,
		}
		jsonResult, _ := json.Marshal(result)
		return CallResultSuccess(string(jsonResult))
	}
}
