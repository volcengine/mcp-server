#!/bin/sh
set -e

exec uv --directory ./ run mcp-server-tls -t "$TRANSPORT_TYPE"
