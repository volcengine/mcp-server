package tool

import (
	"context"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
)

func NewTextInputTool() mcp.Tool {
	return mcp.NewTool("text_input",
		mcp.WithDescription("Input text on the screen"),
		mcp.WithString("text",
			mcp.Description("The text to input"),
			mcp.Required(),
		),
	)
}

func HandleTextInput() func(context.Context, mcp.CallToolRequest) (*mcp.CallToolResult, error) {
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
		err = handler.InputTextClear(ctx)
		if err != nil {
			return CallResultError(err)
		}
		args, err := CheckArgs(req.Params.Arguments)
		if err != nil {
			return CallResultError(err)
		}
		text, ok := args["text"].(string)
		if !ok {
			return CallResultError(fmt.Errorf("text is required"))
		}
		err = handler.InputText(ctx, text)
		if err != nil {
			return CallResultError(err)
		}
		return CallResultSuccess("Input text successfully")
	}
}
