#!/bin/bash
set -ex
cd `dirname $0`

cd src
exec python3 -m mcp_server_metrics.main -t streamable-http
