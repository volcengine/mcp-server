package tool

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewTerminateTool() mcp.Tool {
	return mcp.NewTool("terminate",
		mcp.WithDescription("Terminate the current task"),
		mcp.WithString("reason",
			mcp.Description("The reason for terminating the task"),
			mcp.Required(),
		),
	)
}

func HandleTerminate() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	return func(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
		err := CheckAuth(ctx)
		if err != nil {
			return CallResultError(err)
		}
		mobileUseConfig, err := GetMobileUseConfig(ctx)
		if err != nil || mobileUseConfig == nil {
			return CallResultError(err)
		}
		args, err := CheckArgs(req.Params.Arguments)
		if err != nil {
			return CallResultError(err)
		}
		reason, ok := args["reason"].(string)
		if !ok || reason == "" {
			return CallResultError(fmt.Errorf("reason is required"))
		}
		return CallResultSuccess(fmt.Sprintf("Task terminated: %s", reason))
	}
}
