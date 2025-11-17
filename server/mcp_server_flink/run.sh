#!/bin/bash
set -ex
cd `dirname $0`

cd src
python3 -m mcp_server_flink.main -t streamable-http