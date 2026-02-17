import logging
import json
from typing import Dict, Any, Optional
from backend.agents.base_agent import BaseAgent
from backend.utils.search_client import get_search_provider

class ResearchAgent(BaseAgent):
    """
    Agent responsible for gathering information from the web.
    Uses DuckDuckGo or Parallel.AI via SearchProvider.
    """
    
    def __init__(self, client: Any = None, verbose: bool = True):
        # Pass llm_client to BaseAgent
        super().__init__(name="Research", llm_client=client)
        self.verbose = verbose
        self.search_provider = get_search_provider()

    async def _execute_internal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conducts research on the given topic.
        
        Args:
            input_data: Dict containing 'topic' (str)
            
        Returns:
            Dict containing 'research_data' and 'sources'
        """
        if not input_data or 'topic' not in input_data:
            raise ValueError("Input data must contain 'topic'")
            
        topic = input_data['topic']
        self.logger.info(f"🔍 Researching topic: {topic}")
        
        # 1. Search the web
        search_results = self.search_provider.search(topic)
        
        # 2. Summarize findings using LLM
        prompt = f"""
        You are a highly skilled Research Assistant named Scout.
        Your goal is to synthesize search results into a detailed, factual report.
        
        TOPIC: {topic}
        
        SEARCH RESULTS:
        {search_results}
        
        INSTRUCTIONS:
        1. Extract the most important facts, statistics, and trends.
        2. Identify key sources/URLs from the search results.
        3. Structure the output as a Markdown report with sections:
           - Executive Summary
           - Key Findings (bullet points)
           - Detailed Analysis
           - Reliable Sources (list of URLs)
        4. If search results are empty or irrelevant, state that clearly and provide general knowledge (but explicitly mark it as "General Knowledge").
        
        OUTPUT FORMAT:
        Return ONLY the Markdown report. Do not include introductory text like "Here is the report".
        """
        
        response = await self.llm_client.generate(prompt)
        
        return {
            "topic": topic,
            "research_data": response,
            "sources": self._extract_sources(search_results)
        }
        
    def _extract_sources(self, search_results: str) -> list[str]:
        """Helper to parse URLs from search results string."""
        sources = []
        for line in search_results.split('\n'):
            if line.startswith("URL: "):
                sources.append(line.replace("URL: ", "").strip())
        return sources
