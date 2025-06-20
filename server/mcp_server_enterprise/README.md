# Enterprise Services MCP Server

A newly launched MCP Server by Enterprise Services, featuring trademark query capabilities and supporting natural language interaction for easy trademark information, applicant information, and requirement information queries.

|   Version   |                              v0.1.0                              |
| :---------: | :--------------------------------------------------------------: |
| Description | Efficiently query trademark information through natural language |
|  Category   |                      Enterprise Application                      |
|    Tags     |                       Enterprise Services                        |

## Tools

This MCP Server provides the following Tools (tools/capabilities):

### Tool1: search_trademark

- Detailed Description: Query trademark information recorded in the Trademark Office, commonly used for evaluating the status of intended trademarks before registration. Supports independent search by trademark name, registration number, and applicant, with at least one required
- Trigger Example: Call search_trademark to get relevant data

### Tool2: search_trademark_info

- Detailed Description: Query trademark details based on trademark registration number
- Trigger Example: Call search_trademark_info to get relevant data

### Tool3: list_trademarks

- Detailed Description: Get the list of trademarks submitted by the current account
- Trigger Example: Call list_trademarks to get relevant data

### Tool4: get_trademark

- Detailed Description: Get trademark details of the current account
- Trigger Example: Call get_trademark to get relevant data

### Tool5: list_applicants

- Detailed Description: Get the list of trademark applicants
- Trigger Example: Call list_applicants to get relevant data

### Tool6: get_applicant

- Detailed Description: Get trademark applicant details
- Trigger Example: Call get_applicant to get relevant data

### Tool7: list_requirements

- Detailed Description: Get the list of trademark requirements
- Trigger Example: Call list_requirements to get relevant data

### Tool8: get_requirement

- Detailed Description: Get trademark requirement details
- Trigger Example: Call get_requirement to get relevant data

### Tool9: list_barrier_trademarks

- Detailed Description: Get the list of barrier trademarks
- Trigger Example: Call list_barrier_trademarks to get relevant data

## Most Easily Triggered Prompt Examples

### search_trademark

I want to check the status of the "Volcengine" trademark

### list_trademarks

I want to check my trademark list

## Compatible Platforms

Can be used with cline, cursor, claude desktop, or other terminals that support MCP server calls

## Service Activation Link (Overall Product)

<https://console.volcengine.com/enterprise/overview>

## Authentication Method

Obtain Volcengine Access Key ID and Secret Access Key from the Volcengine management console

## Installation

### Environment Requirements

- Python 3.13+
- Volcengine account and AccessKey/SecretKey

## Deployment

### Integration in MCP Client

```json
{
  "mcpServers": {
    "mcp-server-enterprise": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_enterprise",
        "mcp-server-enterprise"
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
