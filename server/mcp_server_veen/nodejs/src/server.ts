import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

/**
 * The model context protocol server.
 */
export const server = new McpServer({
  name: 'volcano-edge-mcp',
  version: '1.0.0'
});

/**
 * Runs the server.
 * @param transport The optional standard I/O server transport.
 */
export async function init(transport: StdioServerTransport) {
  if (!transport) {
    transport = new StdioServerTransport();
  }

  await server.connect(transport);
}
