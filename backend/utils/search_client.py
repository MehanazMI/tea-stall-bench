import os
import logging
import requests
import json
from abc import ABC, abstractmethod
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

logger = logging.getLogger(__name__)

class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> str:
        """Execute search and return a string summary of results."""
        pass

class DuckDuckGoProvider(SearchProvider):
    def search(self, query: str) -> str:
        if not DDGS:
            return "Error: duckduckgo-search not installed."
        
        try:
            logger.info(f"Searching DuckDuckGo for: {query}")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                if not results:
                    return "No results found."
                
                # Format results
                summary = []
                for r in results:
                    title = r.get('title', 'No Title')
                    href = r.get('href', '#')
                    body = r.get('body', '')
                    summary.append(f"Title: {title}\nURL: {href}\nSummary: {body}\n")
                
                return "\n---\n".join(summary)
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")
            return f"Search error: {e}"

class ParallelProvider(SearchProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://search-mcp.parallel.ai/mcp"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json, text/event-stream"
        }
        
    def search(self, query: str) -> str:
        logger.info(f"Searching Parallel.AI for: {query}")
        
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 1,
            "params": {
                "name": "web_search_preview",
                "arguments": {
                    "objective": f"Find detailed information about: {query}",
                    "search_queries": [query]
                }
            }
        }
        
        try:
            response = requests.post(
                self.base_url, 
                headers=self.headers, 
                json=payload, 
                timeout=60
            )
            
            if response.status_code != 200:
                logger.error(f"Parallel API Error: {response.status_code} - {response.text}")
                return f"Error from Parallel.AI: {response.status_code}"
                
            data = response.json()
            
            # Check for JSON-RPC error
            if "error" in data:
                logger.error(f"Parallel JSON-RPC Error: {data['error']}")
                return f"Error from Parallel.AI: {data['error'].get('message')}"
            
            # Extract content from tool result
            # Expected structure: result.content[].text
            content_blocks = data.get("result", {}).get("content", [])
            output = []
            
            for block in content_blocks:
                if block.get("type") == "text":
                    output.append(block.get("text", ""))
            
            return "\n\n".join(output)
            
        except Exception as e:
            logger.error(f"Parallel search failed: {e}")
            return f"Search exception: {e}"

def get_search_provider() -> SearchProvider:
    """Factory to get the configured search provider."""
    parallel_key = os.getenv("PARALLEL_API_KEY")
    # Check if key is valid (not the example placeholder)
    if parallel_key and parallel_key != "your_parallel_api_key_here":
        logger.info("Using Parallel.AI Search Provider")
        return ParallelProvider(parallel_key)
    
    logger.info("Using DuckDuckGo Search Provider")
    return DuckDuckGoProvider()
