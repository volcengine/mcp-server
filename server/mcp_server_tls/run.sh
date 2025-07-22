#!/bin/bash
set -ex
cd `dirname $0`

cd src
exec python3 -m mcp_server_tls.main -t streamable-http
