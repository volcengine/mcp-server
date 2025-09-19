package main

import (
	"flag"
	"fmt"
	"log/slog"
	"os"
	"os/signal"
	"syscall"

	"mcp_server_mobile_use/internal/mobile_use/server"
)

var (
	transport string
	port      string
)

func init() {
	flag.StringVar(&transport, "transport", "stdio", "transport type (stdio,sse,streamable-http)")
	flag.StringVar(&transport, "t", "stdio", "transport type (stdio,sse,streamable-http)")
	flag.StringVar(&port, "port", "8080", "mcp server port while serve transport is sse mode")
	flag.StringVar(&port, "p", "8080", "mcp server port while serve transport is sse mode")
}

func main() {
	flag.Parse()

	s := server.NewMobileUseServer()

	// Set up signal handling for graceful shutdown
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	// Channel to receive server errors
	errCh := make(chan error, 1)

	// Start the appropriate server
	switch transport {
	case "stdio":
		if err := s.StartStdio(); err != nil {
			slog.Error("Failed to start stdio server", "error", err)
			os.Exit(1)
		}
	case "sse":
		baseUrl := fmt.Sprintf(":%s", port)
		if err := s.StartSSEWithServer(fmt.Sprintf(":%s", port), baseUrl); err != nil {
			slog.Error("Failed to start SSE server", "error", err)
			os.Exit(1)
		}
	case "streamable-http":
		if err := s.StartStreamableHTTPServer(fmt.Sprintf(":%s", port)); err != nil {
			slog.Error("Failed to start streamable-http server", "error", err)
			os.Exit(1)
		}
	default:
		slog.Error("Invalid transport", "transport", transport)
		os.Exit(1)
	}

	// Wait for server completion or signal
	go func() {
		if err := s.WaitForDone(); err != nil {
			errCh <- err
		} else {
			// Server completed naturally (esp. in stdio mode)
			errCh <- nil
		}
	}()

	// Wait for either a signal or server completion
	select {
	case sig := <-sigCh:
		slog.Info("Received signal, shutting down gracefully", "signal", sig)
		s.Shutdown()
		slog.Info("Server shutdown complete")
	case err := <-errCh:
		if err != nil {
			slog.Error("Server error", "error", err)
			os.Exit(1)
		} else {
			slog.Info("Server completed successfully")
		}
	}
}
