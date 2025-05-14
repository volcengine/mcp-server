# MCP Server Product: Domain Service MCP Server ![Product Logo](https://ti.volccdn.com/obj/net-fe/assets/Internet.svg)


## Version Information
v1

## Product Description
### Short Description
Efficiently query and register domains through natural language
### Long Description
The newly launched MCP Server for Domain Service features efficient domain registration capabilities, supporting easy querying of various domain prices through natural language interaction, and completing domain registration with one click, greatly simplifying the domain acquisition process and significantly improving domain registration efficiency and convenience.

## Category
Enterprise Applications

## Tags
Domain

## Tools
This MCP Server product provides the following Tools (capabilities):
### Tool1: check_fee
 - Detailed Description: Query domain price, registration availability, and information about restricted words.
 - Trigger Example: Call check_fee to get relevant data
### Tool2: get_domain
 - Detailed Description: Get detailed information about a specified domain.
 - Trigger Example: Call get_domain to get relevant data
### Tool3: get_async_task
 - Detailed Description: Query the execution status of asynchronous tasks in Volcano Engine domain service. Operations include domain registration, domain renewal, etc.
 - Trigger Example: Call get_async_task to get relevant data
### Tool4: get_template
 - Detailed Description: Get details of a domain information template.
 - Trigger Example: Call get_template to get relevant data
### Tool5: list_domains
 - Detailed Description: Query detailed information about domains hosted in your Volcano Engine domain service.
 - Trigger Example: Call list_domains to get relevant data
### Tool6: list_templates
 - Detailed Description: Get the list of domain information templates under the current account and the detailed information of each template in the list. You can specify one or more conditions to filter the returned domain list.
 - Trigger Example: Call list_templates to get relevant data
### Tool7: register_domain
 - Detailed Description: Register a domain. This operation will generate an asynchronous task. You can use get_async_task to query the status of the task.
 - Trigger Example: Call register_domain to get relevant data


## Most Easily Invoked Prompt Examples
### check_fee
I want to check the price of the volcengine.com domain

### list_domains
I want to check my domain list

### register_domain
I want to apply for an xxx.com domain


## Compatible Platforms  
Can be used with cline, cursor, claude desktop, or other terminals that support MCP server calls

## Service Activation Link (Overall Product)
<https://console.volcengine.com/domain-service>


## Authentication Method
Obtain Volcengine access key ID and secret access key from the Volcengine management console

## Installation

### Environment Requirements

- Python 3.13+
- Volcano Engine account and AccessKey/SecretKey


## Deployment
### Integration in MCP Client

```json
{
  "mcpServers": {
    "mcp-server-domain-service": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_domain_service",
        "mcp-server-domain-service"
      ],
      "env": {
        "VOLCENGINE_ACCESS_KEY": "Your Volcengine AK",
        "VOLCENGINE_SECRET_KEY": "Your Volcengine SK"
      }
    }
  }
}
```

## License
MIT