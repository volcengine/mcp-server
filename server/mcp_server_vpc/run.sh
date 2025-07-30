#!/bin/sh -ex

cd $(dirname $0)/src
exec python3 -m mcp_server_vpc.main -t streamable-http
