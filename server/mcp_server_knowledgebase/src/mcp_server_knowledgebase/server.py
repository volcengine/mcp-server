import argparse
import logging
import os
import requests

from typing import Dict, Optional, Final, Any
from mcp.server import FastMCP
from mcp_server_knowledgebase.config import config
from mcp_server_knowledgebase.common.auth import prepare_request

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
doc_add_path = "/api/knowledge/doc/add"
doc_info_path = "/api/knowledge/doc/info"

# Create MCP server
mcp = FastMCP("Knowledgebase MCP Server", port=int(os.getenv("PORT", "8000")),
              streamable_http_path=os.getenv("STREAMABLE_HTTP_PATH", "/mcp"))

@mcp.tool()
def add_doc(
        collection_name:str,
        add_type:str,
        doc_id: str,
        doc_name: str,
        doc_type: str,
        url: str,
) -> Dict:
    """
    Add a document to a collection in your project.
    This tool allows you to add a document to a collection in your project by collection_name.
    Args:
         collection_name: the name of the knowledge base collection to add document to.
         add_type: the type of the document to add. so far only support "url" now. so you must assign this parameter to "url".
         doc_id: you should generate a unique doc_id based on user's given url and timestamp, the doc_id can only use English letters, numbers, and underscores , and must start with an English letter. It cannot be empty.
                Length requirement: [1, 128], you can use a format like "mcp_server_auto_gen_doc_id_xxxxxxx.
         doc_name: the name of the document to add. you can1 generate a unique doc_name based on user given url and timestamp. the length of doc_name must between 1 and 256. you can use a
                format like "mcp_server_auto_gen_doc_name_xxxxxxx.
         doc_type: the type of the document to add. for structured document, we support xlsx, csv,jsonl, for unstructured document, wu support txt, doc, docx, pdf, markdown, faq.xlsx, pptx".
                   you should judge the doc_type based on user's given url and judge if we support this doc type. if supported, assign this parameter.
         url: the url of the document to add. user should give a valid url, we will add the doc to the collection.

    Returns:
        collection_name: the name of the knowledge base collection.
        doc_id: the doc_id of document user added to collection.

    """
    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")

        request_params = {
            "collection_name": collection_name,
            "project": config.project,
            "add_type": add_type,
            "doc_id": doc_id,
            "doc_name": doc_name,
            "doc_type": doc_type,
            "url": url,
        }

        doc_add_req = prepare_request(method="POST", path=doc_add_path, ak=config.ak, sk=config.sk, data=request_params)
        rsp = requests.request(
            method=doc_add_req.method,
            url="https://{}{}".format(g_knowledge_base_domain, doc_add_req.path),
            headers=doc_add_req.headers,
            data=doc_add_req.body)

        result = rsp.json()
        if result['code'] != 0:
            logger.error(f"Error in add_doc: {result['message']}")
            return {"error": result['message']}

        doc_add_data = result['data']
        if not doc_add_data:
            raise ValueError(f"doc {doc_id} has no data.")

        return {
            "collection_name": collection_name,
            "doc_id": doc_id,
        }

    except Exception as e:
        logger.error(f"Error in add_doc: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
def get_doc(
        collection_name: str,
        doc_id: str,
) -> Dict:
    """
    Get information about a document from your collection.
    This tool allows you to get information about a document from your project by collection_name and doc_id.
    Args:
         collection_name: the name of the knowledge base collection to get document from.
         doc_id: the doc_id of document user want to get information.
    Returns:
        collection_name: the name of the knowledge base collection.
        doc_id: the doc_id of document user added to collection.
        doc_name: the name of the document.
        doc_type: the type of the document.
        url: the url of the document.
        add_type: the type how to add document.
        create_time: the time when document added to collection.
        update_time: the time when document updated.
        point_num: The number of points extracted from the document.
        status: the status of the document. the status struct has two fields:
            - process_status: The processing status of the document.
                                0 means the processing is completed,
                                1 means the processing failed,
                                2 or 3 means it is in queue,
                                5 means it is being deleted,
                                and 6 means it is processing.
            - failed_code: the status message of the document.
    """

    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")

        request_params = {
            "collection_name": collection_name,
            "project": config.project,
            "doc_id": doc_id,
        }

        doc_info_req = prepare_request(method="POST", path=doc_info_path, ak=config.ak, sk=config.sk, data=request_params)
        rsp = requests.request(
            method=doc_info_req.method,
            url="https://{}{}".format(g_knowledge_base_domain, doc_info_req.path),
            headers=doc_info_req.headers,
            data=doc_info_req.body)

        result = rsp.json()
        if result['code'] != 0:
            logger.error(f"Error in add_doc: {result['message']}")
            return {"error": result['message']}

        doc_info_data = result['data']
        if not doc_info_data:
            raise ValueError(f"doc {doc_id} not found.")

        return doc_info_data

    except Exception as e:
        logger.error(f"Error in get_doc: {str(e)}")
        return {"error": str(e)}


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
        doc_filter: dict = None,
) -> Dict:
    """Search knowledge from the Viking Knowledgebase service And return Top limit related chunks of your query.
    This tool allows you to search knowledge in provided collection based on the given query.

    Args:
        query: the search query string.
        limit: the maximum number of results to return (default: 3).
        collection_name: the name of the knowledge base collection to search for.
        doc_filter: the filter is used to filter search results(default: None), which is structured as a JSON object with
        the following key components:
        - 'op': (string, required) specifies the query operator that defines the filtering logic. Valid values are
            'must' and 'must_not', 'must' means results must satisfy the condition (inclusion filter),'must_not' means
            results must not satisfy the condition (exclusion filter).
        - 'field':  (string, required) indicates the specific document field to apply the filter on (e.g., "doc_id").
        - 'conds': (array, required) contains the concrete values used for filtering. The data type
            of elements in the array depends on the field.

    Returns:
        A list of search results.
        id: the id of the knowledge base chunk.
        content: the content of the knowledge base chunk.
    """

    try:
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")

        request_params = {
            "query": query,
            "limit": limit,
            "name": collection_name,
            "project": config.project,
        }

        if doc_filter:
            request_params['query_param'] = {
                "doc_filter": doc_filter,
            }

        search_req = prepare_request(method="POST", path=search_knowledge_path, ak=config.ak, sk=config.sk, data=request_params)
        logger.debug("search param: {}".format(search_req.body))
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