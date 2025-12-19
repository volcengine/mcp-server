# ServerlessFlink MCP Server

## Overview

An MCP server for ServerlessFlink. ServerlessFlink MCP Server serves as a communication bridge between large language
models and ServerlessFlink, capable of efficiently transmitting information to achieve seamless docking and
collaboration between the two. It also provides intelligent services throughout the entire life cycle for
ServerlessFlink job development, resource pool development, log & events information query and flink job operation and
maintenance.

## Features

- Query project & directory information
- Resource pool development
- ServerlessFlink job development, operation and maintenance.
- Query log, events and runtime information

## Available Tools

The ServerlessFlink MCP Server supports querying and analyzing data information and job development, providing the
following tools.

### project development

- `list_flink_project`: Tool function to query Flink project list

### resource pool operation

- `list_flink_resource_pool`: Tool function to list Serverless Flink resource pools.

### job development

- `get_flink_application_draft`: Tool function to retrieve a Serverless Flink application draft.
- `create_flink_application_draft`: Tool function to create a new Serverless Flink application draft
- `update_flink_application_draft`: Tool function to update an existing Serverless Flink application draft
- `deploy_flink_application_draft`: Tool function to deploy a Serverless Flink application draft.
- `offline_flink_application_to_draft`: Tool function to offline a Serverless Flink application.
- `list_flink_directory`: Tool function to get the Serverless Flink directory list

### job operation

- `list_flink_application`: Tool function to get the Serverless Flink application list
- `start_flink_application`: Tool function to start a Serverless Flink application.
- `stop_flink_application`: Tool function to stop a Serverless Flink application.
- `restart_flink_application`: Tool function to restart a Serverless Flink application.
- `list_flink_application_log`: Tool function to retrieve logs for a Serverless Flink application.

### runtime

- `get_flink_application_event`: Tool function to retrieve events for a Serverless Flink application.
- `get_flink_runtime_application_info`: Tool function to retrieve runtime information for a Serverless Flink
  application.

## Usage Guide

### Prerequisites

- Python 3.12+
- UV

**Linux/macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation

Clone the repository:

```bash
git clone git@github.com:volcengine/mcp-server.git
```

### Usage

Start the server:

#### UV

```bash
cd mcp-server/server/mcp_server_flink
uv run mcp-server-flink

# Start with streamable-http mode (default is stdio)
uv run mcp-server-flink -t streamable-http
```

Use a client to interact with the server:

```
Trae | Cursor | ...
```

## Configuration

### Environment Variables

The following environment variables are available for configuring the MCP server:

| Environment Variable      | Description                              | Default Value |
|---------------------------|------------------------------------------|---------------|
| `VOLCENGINE_ACCESS_KEY`   | Volcengine account ACCESSKEY             | -             |
| `VOLCENGINE_SECRET_KEY`   | Volcengine account SECRETKEY             | -             |
| `VOLCENGINE_REGION`       | Volcengine resource region               | -             |
| `VOLCENGINE_PROJECT_NAME` | Volcengine Serverless Flink project name | -             |

For example, set these environment variables before starting the server:

```bash
export VOLCENGINE_ACCESS_KEY={ak}
export VOLCENGINE_SECRET_KEY={sk}
export VOLCENGINE_REGION={region}
export VOLCENGINE_PROJECT_NAME={project_name}
```

### Run with uvx

```json
{
  "mcpServers": {
    "mcp-server-flink": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_flink",
        "mcp-server-flink"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "your-access-key-id",
        "VOLCENGINE_SECRET_KEY": "your-access-key-secret",
        "VOLCENGINE_PROJECT_NAME": "your-project-name",
        "VOLCENGINE_REGION": "region"
      }
    }
  }
}
```

## Examples

### 1. job query & analyze

Query the Serverless Flink job list for the cdc-test project, displaying each job’s status, engine version, and job type
on a beautifully designed web page.

### 2. resource pool query & analyze

Query the Serverless Flink resource pool information for the cdc-test project and display it on a beautifully designed
web page.

### 3. job diagnosis

In the cdc-test project, check the running status and log information of test-failed-job, and analyze any potential
anomalies indicated in the logs.

### 4. job development

In the cdc-test project, under the Data Development directory, create a Flink draft job named flink_mcp_test .
Validate the SQL job syntax and make necessary adjustments.
Set the job parallelism to 20, deploy it to the test-c resource pool, then publish and start the job.

The Flink SQL is as follows:

``` sql
CREATE TABLE sales_data (
  supplier_id STRING,
  sales_amount DOUBLE,
  event_time TIMESTAMP(3),
  WATERMARK FOR event_time AS event_time - INTERVAL '10' SECOND
) WITH (
  'connector' = 'datagen',
  'rows-per-second' = '50',
  'fields.supplier_id.length' = '10',
  'fields.sales_amount.min' = '1',
  'fields.sales_amount.max' = '100'
);
CREATE TABLE print_result (
  window_start TIMESTAMP(3),
  window_end TIMESTAMP(3),
  supplier_id STRING,
  sales_amount DOUBLE,
  rownum BIGINT
) WITH (
  'connector' = 'print'
);
INSERT INTO print_result
SELECT
  window_start,
  window_end,
  supplier_id,
  sales_amount,
  rownum
FROM (
  SELECT
    supplier_id,
    sales_amount,
    window_start,
    window_end,
    ROW_NUMBER() OVER (PARTITION BY window_start, window_end ORDER BY sales_amount DESC) AS rownum
  FROM (
    SELECT
      supplier_id,
      SUM(sales_amount) as sales_amount,
      window_start,
      window_end
    FROM TABLE(TUMBLE(TABLE sales_data, DESCRIPTOR(event_time), INTERVAL '10' SECOND))
    GROUP BY window_start, window_end, supplier_id
  ) t
) r
WHERE rownum <= 3
```

### 5. job operation

In the cdc-test project, perform job operations including create, stop, publish (online), unpublish (offline), restart,
and start.

# License

volcengine/mcp-server is licensed under the [MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE).
