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

class HybridSearchProvider(SearchProvider):
    """
    Hybrid provider that tries Parallel.AI first, then falls back to DuckDuckGo.
    Implements the Circuit Breaker pattern (conceptually) via fallback.
    """
    
    def __init__(self, primary: SearchProvider, fallback: SearchProvider):
        self.primary = primary
        self.fallback = fallback
        
    def search(self, query: str) -> str:
        """
        Execute search with fallback logic.
        
        Args:
            query: Search query string
            
        Returns:
            str: Search results from primary or fallback provider
        """
        try:
            logger.info(f"Attempting search with primary provider: {type(self.primary).__name__}")
            return self.primary.search(query)
        except Exception as e:
            logger.warning(f"Primary search provider failed: {str(e)}")
            logger.info(f"Falling back to: {type(self.fallback).__name__}")
            try:
                return self.fallback.search(query)
            except Exception as fallback_error:
                logger.error(f"Fallback search provider also failed: {str(fallback_error)}")
                raise fallback_error


def get_search_provider() -> SearchProvider:
    """
    Factory function to get the appropriate search provider.
    Returns a HybridSearchProvider if Parallel key is present,
    otherwise returns DuckDuckGoProvider.
    """
    ddg_provider = DuckDuckGoProvider()
    
    parallel_key = os.getenv("PARALLEL_API_KEY")
    if parallel_key and parallel_key != "your_parallel_api_key_here":
        logger.info("Configuring Hybrid Search (Parallel Primary -> DDG Fallback)")
        parallel_provider = ParallelProvider(parallel_key)
        return HybridSearchProvider(primary=parallel_provider, fallback=ddg_provider)

    logger.info("Configuring Single Search Provider (DuckDuckGo)")
    return ddg_provider
