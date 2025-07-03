package tool

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewScreenTapTool() mcp.Tool {
	return mcp.NewTool("tap",
		mcp.WithDescription("Tap at specified coordinates on the cloud phone screen"),
		mcp.WithNumber("x",
			mcp.Description("The x coordinate of the tap point"),
			mcp.Required(),
		),
		mcp.WithNumber("y",
			mcp.Description("The y coordinate of the tap point"),
			mcp.Required(),
		),
	)
}

func HandleScreenTap() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
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
		args, err := CheckArgs(req.Params.Arguments)
		if err != nil {
			return CallResultError(err)
		}
		x, err := GetInt64Param(args, "x")
		if err != nil {
			return CallResultError(fmt.Errorf("x is required"))
		}
		y, err := GetInt64Param(args, "y")
		if err != nil {
			return CallResultError(fmt.Errorf("y is required"))
		}
		err = handler.ScreenTap(ctx, int(x), int(y))
		if err != nil {
			return CallResultError(err)
		}
		return CallResultSuccess("Tap the screen successfully")
	}
}
