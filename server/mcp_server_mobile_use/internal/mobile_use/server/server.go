package server

import (
	"context"
	"encoding/base64"
	"encoding/json"
	"errors"
	"net/http"
	"os"
	"strings"
	"sync"

	"mcp_server_mobile_use/internal/mobile_use/config"
	"mcp_server_mobile_use/internal/mobile_use/consts"
	"mcp_server_mobile_use/internal/mobile_use/tool"

	mcp_srv "github.com/mark3labs/mcp-go/server"
)

type MobileUseServer struct {
	server      *mcp_srv.MCPServer
	shutdownWg  sync.WaitGroup
	shutdownCtx context.Context
	cancel      context.CancelFunc
	doneCh      chan struct{}
}

func NewMobileUseServer() *MobileUseServer {
	mcpServer := mcp_srv.NewMCPServer(
		"mobile_use_mcp_server",
		"0.0.1",
		mcp_srv.WithToolCapabilities(true),
	)

	terminateTool := tool.NewTerminateTool()
	mcpServer.AddTool(terminateTool, tool.HandleTerminate())

	screenTapTool := tool.NewScreenTapTool()
	mcpServer.AddTool(screenTapTool, tool.HandleScreenTap())

	screenSwipeTool := tool.NewScreenSwipeTool()
	mcpServer.AddTool(screenSwipeTool, tool.HandleScreenSwipe())

	takeScreenshotTool := tool.NewTakeScreenshotTool()
	mcpServer.AddTool(takeScreenshotTool, tool.HandleTakeScreenshot())

	textInputTool := tool.NewTextInputTool()
	mcpServer.AddTool(textInputTool, tool.HandleTextInput())

	appUploadTool := tool.NewAppUploadTool()
	mcpServer.AddTool(appUploadTool, tool.HandleAppUploadTool())

	appLaunchTool := tool.NewLaunchAppTool()
	mcpServer.AddTool(appLaunchTool, tool.HandleLaunchAppTool())

	appCloseTool := tool.NewCloseAppTool()
	mcpServer.AddTool(appCloseTool, tool.HandleCloseAppTool())

	listAppsTool := tool.NewListAppTool()
	mcpServer.AddTool(listAppsTool, tool.HandleListAppTool())

	keyEventBackTool := tool.NewKeyEventBackTool()
	mcpServer.AddTool(keyEventBackTool, tool.HandleKeyEventBackTool())

	keyEventHomeTool := tool.NewKeyEventHomeTool()
	mcpServer.AddTool(keyEventHomeTool, tool.HandleKeyEventHomeTool())

	keyEventMenuTool := tool.NewKeyEventMenuTool()
	mcpServer.AddTool(keyEventMenuTool, tool.HandleKeyEventMenuTool())

	ctx, cancel := context.WithCancel(context.Background())
	return &MobileUseServer{
		server:      mcpServer,
		shutdownCtx: ctx,
		cancel:      cancel,
		doneCh:      make(chan struct{}),
	}
}

func (s *MobileUseServer) StartSSE(baseUrl string) *mcp_srv.SSEServer {
	return mcp_srv.NewSSEServer(s.server,
		mcp_srv.WithBaseURL(baseUrl),
		mcp_srv.WithSSEContextFunc(authFromRequest),
	)
}

// StartStdio starts the MCP server in stdio mode
// It returns a done channel that is closed when the stdio server exits
func (s *MobileUseServer) StartStdio() error {
	go func() {
		err := mcp_srv.ServeStdio(s.server, mcp_srv.WithStdioContextFunc(authFromEnv))
		s.cancel()      // Cancel context when stdio exits
		close(s.doneCh) // Signal that stdio is done
		if err != nil {
			// Log error or handle it somehow
		}
	}()
	return nil
}

// WaitForDone blocks until the server is done (either shutdown by signal or completed naturally)
func (s *MobileUseServer) WaitForDone() error {
	select {
	case <-s.doneCh:
		return nil
	case <-s.shutdownCtx.Done():
		return errors.New("server shutdown")
	}
}

// StartSSEWithServer starts the SSE server with a graceful shutdown capability
func (s *MobileUseServer) StartSSEWithServer(addr string, baseUrl string) error {
	sseServer := s.StartSSE(baseUrl)

	// Start HTTP server in a goroutine
	go func() {
		err := sseServer.Start(addr)
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			// If error is not due to server shutdown, signal server is done
			s.cancel()
		}
		close(s.doneCh)
	}()

	return nil
}

func (s *MobileUseServer) StartStreamableHTTPServer(addr string) error {
	server := mcp_srv.NewStreamableHTTPServer(s.server,
		mcp_srv.WithHTTPContextFunc(authFromRequest),
	)

	// Start HTTP server in a goroutine
	go func() {
		err := server.Start(addr)
		if err != nil && !errors.Is(err, http.ErrServerClosed) {
			// If error is not due to server shutdown, signal server is done
			s.cancel()
		}
		close(s.doneCh)
	}()
	return nil
}

// Shutdown gracefully stops the server
func (s *MobileUseServer) Shutdown() {
	s.cancel()
	s.shutdownWg.Wait()
}

func authFromEnv(ctx context.Context) context.Context {
	accessKeyId := os.Getenv("ACEP_ACCESS_KEY")
	accessKeySecret := os.Getenv("ACEP_SECRET_KEY")
	productId := os.Getenv("ACEP_PRODUCT_ID")
	deviceId := os.Getenv("ACEP_DEVICE_ID")
	acepHost := os.Getenv("ACEP_HOST")
	tosAccessKey := os.Getenv("TOS_ACCESS_KEY")
	tosSecretKey := os.Getenv("TOS_SECRET_KEY")
	bucket := os.Getenv("ACEP_TOS_BUCKET")
	region := os.Getenv("ACEP_TOS_REGION")
	endpoint := os.Getenv("ACEP_TOS_ENDPOINT")
	if accessKeyId == "" || accessKeySecret == "" || productId == "" || deviceId == "" || bucket == "" || region == "" || endpoint == "" {
		ctx = context.WithValue(ctx, consts.AuthResult{}, consts.AuthResultErrEmpty)
		return ctx
	}
	if tosAccessKey == "" {
		tosAccessKey = accessKeyId
	}
	if tosSecretKey == "" {
		tosSecretKey = accessKeySecret
	}
	ctx = context.WithValue(ctx, consts.AuthResult{}, consts.AuthResultOk)
	authInfo := config.AuthInfo{
		AccessKeyId:     accessKeyId,
		SecretAccessKey: accessKeySecret,
	}
	mobileUseConfig := config.MobileUseConfig{
		AuthInfo: authInfo,
		BizInfo: config.BizInfo{
			ProductId: productId,
			DeviceId:  deviceId,
			ACEPHost:  acepHost,
		},
		TosInfo: config.TosInfo{
			TosBucket:    bucket,
			TosRegion:    region,
			TosEndpoint:  endpoint,
			TosAccessKey: tosAccessKey,
			TosSecretKey: tosSecretKey,
		},
	}
	ctx = context.WithValue(ctx, consts.MobileUseConfigKey{}, mobileUseConfig)
	return ctx
}

func authFromRequest(ctx context.Context, r *http.Request) context.Context {
	authStr := r.Header.Get("Authorization")
	if authStr == "" {
		ctx = context.WithValue(ctx, consts.AuthResult{}, consts.AuthResultErrEmpty)
		return ctx
	}
	authStr = strings.TrimSpace(authStr)
	rawAuth, err := base64.StdEncoding.DecodeString(authStr)
	if err != nil {
		ctx = context.WithValue(ctx, consts.AuthResult{}, consts.AuthResultErrInvalid)
		return ctx
	}
	var authInfo config.AuthInfo
	err = json.Unmarshal(rawAuth, &authInfo)
	if err != nil {
		ctx = context.WithValue(ctx, consts.AuthResult{}, consts.AuthResultErrInvalid)
		return ctx
	}
	ctx = context.WithValue(ctx, consts.AuthResult{}, consts.AuthResultOk)
	mobileUseConfig := config.MobileUseConfig{
		AuthInfo: authInfo,
	}
	mobileUseConfig.BizInfo.ProductId = r.Header.Get("X-ACEP-ProductId")
	mobileUseConfig.BizInfo.DeviceId = r.Header.Get("X-ACEP-DeviceId")
	mobileUseConfig.BizInfo.ACEPHost = r.Header.Get("X-ACEP-Host")
	mobileUseConfig.TosInfo.TosBucket = r.Header.Get("X-ACEP-TosBucket")
	mobileUseConfig.TosInfo.TosRegion = r.Header.Get("X-ACEP-TosRegion")
	mobileUseConfig.TosInfo.TosEndpoint = r.Header.Get("X-ACEP-TosEndpoint")

	tosAccessKey := r.Header.Get("X-Tos-AccessKey")
	tosSecretKey := r.Header.Get("X-Tos-SecretKey")
	if tosAccessKey == "" || tosSecretKey == "" {
		tosAccessKey = authInfo.AccessKeyId
		tosSecretKey = authInfo.SecretAccessKey
	}
	mobileUseConfig.TosInfo.TosAccessKey = tosAccessKey
	mobileUseConfig.TosInfo.TosSecretKey = tosSecretKey
	mobileUseConfig.TosInfo.TosSessionToken = authInfo.SessionToken
	ctx = context.WithValue(ctx, consts.MobileUseConfigKey{}, mobileUseConfig)
	return ctx
}
