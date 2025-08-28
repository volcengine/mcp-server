#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";

const SMART_SEARCH_TOOL: Tool = {
  name: "smartsearch",
  description: "Performs a web search using a remote smart search API.",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string", description: "The search query." },
      count: { type: "number", description: "Number of results to return.", default: 10 },
      offset: { type: "number", description: "Offset for pagination.", default: 0 },
      setLang: { type: "string", description: "Language for the search.", default: "en" },
      safeSearch: { type: "string", description: "Safe search level ('Strict', 'Moderate', 'Off').", default: "Strict" },
    },
    required: ["query"],
  },
};

const server = new Server(
  {
    name: "smartsearch",
    version: "0.1.1",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

const SERVER_KEY = process.env.SERVER_KEY;
if (!SERVER_KEY) {
  console.error("Error: SERVER_KEY environment variable is required.");
  process.exit(1);
}

async function performSmartSearch(args: { [key: string]: any }) {
  const [endpoint, apiKey] = SERVER_KEY!.split("-");
  if (!endpoint || !apiKey) {
    throw new Error("Invalid SERVER_KEY format. Expected 'endpoint-apikey'.");
  }

  const url = new URL(`https://searchapi.xiaosuai.com/search/${endpoint}/smart`);
  url.searchParams.set('q', args.query);
  url.searchParams.set('count', (args.count ?? 10).toString());
  url.searchParams.set('offset', (args.offset ?? 0).toString());
  url.searchParams.set('mkt', args.setLang ?? 'en');
  url.searchParams.set('safeSearch', args.safeSearch ?? 'Strict');

  const response = await fetch(url.toString(), {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'pragma': 'no-cache',
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [SMART_SEARCH_TOOL],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  try {
    const { name, arguments: args } = request.params;

    if (name !== "smartsearch") {
      throw new Error(`Unknown tool: ${name}`);
    }
    if (!args || typeof args.query !== 'string') {
        throw new Error("Invalid arguments for smartsearch. 'query' is required.");
    }

    const result = await performSmartSearch(args);
    return {
      content: [
        {
          type: "text", // Change this from "json" to "text"
          text: JSON.stringify(result, null, 2) // Format for readability
        }
      ],
      isError: false,
    };

  } catch (error) {
    return {
      content: [{ type: "text", text: `Error: ${error instanceof Error ? error.message : String(error)}` }],
      isError: true,
    };
  }
});

async function runServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Smart Search MCP Server running on stdio");
}

runServer().catch((error) => {
  console.error("Fatal error running server:", error);
  process.exit(1);
});
