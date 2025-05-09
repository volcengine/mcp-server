#!/bin/bash
set -e

mkdir -p output

## MCP Server
echo "Building MCP Server..."
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o output/mobile_use_mcp ./cmd/mobile_use_mcp/...

## Cap AOP
# echo "Building Cap AOP..."
# CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -v -o output/cap_tos ./cmd/cap_aop/...
