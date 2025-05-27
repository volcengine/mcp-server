import argparse
import logging
import os
import requests

from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from mcp_server_knowledgebase.config import config
from common.auth import prepare_request

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# knowledge base domain
g_knowledge_base_domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

# paths
search_knowledge_path = "/api/knowledge/collection/search_knowledge"
list_collections_path = "/api/knowledge/collection/list"
get_collections_path = "/api/knowledge/collection/info"

# Create MCP server
mcp = FastMCP("Knowledgebase MCP Server", port=int(os.getenv("PORT", "8000")))

@mcp.tool()
def get_collection(
        collection_name: str,
) -> Dict:
    """
    Get information about a collection from your project.
    This tool allows you to get information about a collection from your project by collection_name.
    Args:
         collection_name: the name of the knowledge base collection to get info for.

    Returns:
        collection_name: the name of the knowledge base collection.
        description: the description of the knowledge base collection.
        status: the status of the knowledge base collection.
        status：
            -1: To be built
            0: Building
            1: Build completed
            2: Build failed
            3: Changing

    """

    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")

        request_params = {
            "name": collection_name,
            "project": config.project,
        }

        get_collection_req = prepare_request(method="POST", path=get_collections_path, ak=config.ak, sk=config.sk, data=request_params)
        rsp = requests.request(
            method=get_collection_req.method,
            url="https://{}{}".format(g_knowledge_base_domain, get_collection_req.path),
            headers=get_collection_req.headers,
            data=get_collection_req.body)

        result = rsp.json()
        if result['code'] != 0:
            logger.error(f"Error in search_knowledge: {result['message']}")
            return {"error": result['message']}

        collection_info = result['data']
        if not collection_info:
            raise ValueError(f"Collection {collection_name} not found.")

        return {
            "collection_name": collection_info["collection_name"],
            "description": collection_info["description"],
            "status": collection_info["pipeline_list"][0]["index_list"][0]["status"]
        }

    except Exception as e:
        logger.error(f"Error in get_collection: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def list_collections(
) -> Dict:
    """
    List all collections of the globally configured project from the Viking Knowledgebase service.
    This tool allows you to list all collections in the Viking Knowledgebase service.

    Returns:
        A list of collections in the project.
        collection_name: the name of the knowledge base collection.
        description: the description of the knowledge base collection.

    """

    try:
        request_params = {
            "project": config.project,
        }

        list_collections_req = prepare_request(method="POST", path=list_collections_path, ak=config.ak, sk=config.sk, data=request_params)
        rsp = requests.request(
            method=list_collections_req.method,
            url="https://{}{}".format(g_knowledge_base_domain, list_collections_req.path),
            headers=list_collections_req.headers,
            data=list_collections_req.body)

        result = rsp.json()
        if result['code'] != 0:
            logger.error(f"Error in list_collections: {result['message']}")
            return {"error": result['message']}

        collections =result['data']['collection_list']
        if not collections:
            raise ValueError(f"No collections found in project {config.project}.")

        collection_list = []

        for collection in collections:
            collection_list.append({
                "collection_name": collection["collection_name"],
                "description": collection["description"],
            })

        return {
            "collection_list": collection_list,
        }

    except Exception as e:
        logger.error(f"Error in list_collections: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def search_knowledge(
        query: str,
        collection_name: str,
        limit: int = 3,
) -> Dict:
    """Search knowledge from the Viking Knowledgebase service And return Top limit related chunks of your query.
    This tool allows you to search knowledge in provided collection based on the given query.

    Args:
        query: the search query string.
        limit: the maximum number of results to return (default: 3).
        collection_name: the name of the knowledge base collection to search for.

    Returns:
        A list of search results.
        id: the id of the knowledge base chunk.
        content: the content of the knowledge base chunk.
    """

    logger.info(f"Received search_knowledge request with query: {query}, limit: {limit}")

    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")

        request_params = {
            "query": query,
            "limit": limit,
            "name": collection_name,
            "project": config.project,
        }

        search_req = prepare_request(method="POST", path=search_knowledge_path, ak=config.ak, sk=config.sk, data=request_params)
        rsp = requests.request(
            method=search_req.method,
            url="https://{}{}".format(g_knowledge_base_domain, search_req.path),
            headers=search_req.headers,
            data=search_req.body)

        result = rsp.json()
        if result['code'] != 0:
            logger.error(f"Error in search_knowledge: {result['message']}")
            return {"error": result['message']}

        if not result['data']['result_list']:
            raise ValueError(f"No results found for collection {collection_name}")


        chunks = result['data']['result_list']

        search_result = []

        for chunk in chunks:
            search_result.append({
                "id": chunk["id"],
                "content": chunk["content"],
            })

        return {
            "result_list": search_result,
        }
    except Exception as e:
        logger.error(f"Error in search_knowledge: {str(e)}")
        return {"error": str(e)}


def main():
    """Main entry point for the Knowledgebase MCP server."""
    parser = argparse.ArgumentParser(description='Run the Viking Knowledgebase MCP Server')
    parser.add_argument(
        "--transport",
        "-t",
        choices=["sse", "stdio"],
        default="stdio",
        help="Transport protocol to use (sse or stdio)",
    )
    args = parser.parse_args()
    logger.info(f"Starting Knowledgebase MCP Server with {args.transport} transport")

    try:
        # Run the MCP server
        logger.info( f"Starting Viking Knowledge Base MCP Server with {args.transport} transport")

        mcp.run(transport=args.transport)
    except Exception as e:
        logger.error(f"Error starting Knowledgebase MCP Server: {str(e)}")
        raise

if __name__ == "__main__":
    main()