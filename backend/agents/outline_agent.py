from typing import Dict, Any, List, Optional
import json
import logging
from pydantic import BaseModel, Field, ValidationError
from backend.agents.base_agent import BaseAgent
from backend.utils.llm_client import LLMClient

# Configure logging
logger = logging.getLogger(__name__)

class OutlineSection(BaseModel):
    """A single section of the outline."""
    heading: str = Field(description="The main heading for this section")
    key_points: List[str] = Field(description="List of key points to cover in this section")

class Outline(BaseModel):
    """The complete outline structure."""
    title: str = Field(description="Proposed title for the article")
    sections: List[OutlineSection] = Field(description="List of sections")

class OutlineAgent(BaseAgent):
    """
    Agent responsible for creating structured outlines.
    Persona: 'Draft' / 'Vazhi' (Tamil: Path/Guide)
    """
    
    def __init__(self, llm_client: LLMClient):
        if not llm_client:
            raise ValueError("LLM client is required for OutlineAgent")
        super().__init__(name="Outline", llm_client=llm_client)
        
    async def _execute_internal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates an outline based on the topic and research data.
        
        Args:
            input_data: Dict containing 'topic' and optional 'research_data'
            
        Returns:
            Dict containing the 'outline' (as dict) and 'raw_json'
        """
        topic = input_data.get('topic')
        if not topic:
            raise ValueError("Topic is required")
            
        research_data = input_data.get('research_data', "No specific research provided.")
        
        prompt = self._build_prompt(topic, research_data)
        
        # Retry logic for valid JSON (simple loop)
        max_retries = 2
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                response = await self.llm_client.generate(prompt)
                
                # Clean code blocks if present
                cleaned_response = self._clean_json_string(response)
                
                # Validate with Pydantic
                outline_model = Outline.model_validate_json(cleaned_response)
                
                return {
                    "topic": topic,
                    "outline": outline_model.model_dump(),
                    "raw_json": cleaned_response
                }
            except (ValidationError, json.JSONDecodeError) as e:
                logger.warning(f"Attempt {attempt + 1} failed to parse/validate JSON: {e}")
                last_error = e
                # Update prompt to be more strict on retry?
                prompt += f"\n\nERROR: Previous output was invalid JSON. Error: {str(e)}\nPlease provide ONLY valid JSON matching the schema."
        
        raise ValueError(f"Failed to generate valid outline after {max_retries + 1} attempts. Last error: {last_error}")

    def _build_prompt(self, topic: str, research_data: str) -> str:
        return f"""
You are 'Draft' (aka Vazhi), an expert content strategist.
Your goal: Create a comprehensive, structured outline for an article about: "{topic}"

Research Data:
{research_data}

Instructions:
1. Analyze the research data to identify key themes.
2. Structure the content logically (Intro -> Body Sections -> Conclusion).
3. For each section, provide specific key points to cover.
4. Output MUST be valid JSON fitting this schema:

{{
    "title": "Catchy Title",
    "sections": [
        {{
            "heading": "Section Heading",
            "key_points": ["Point 1", "Point 2"]
        }}
    ]
}}

Provide ONLY the JSON output. No markdown, no conversational text.
"""

    def _clean_json_string(self, json_string: str) -> str:
        """Removes markdown code blocks if present."""
        if "```json" in json_string:
            json_string = json_string.split("```json")[1].split("```")[0]
        elif "```" in json_string:
            json_string = json_string.split("```")[1].split("```")[0]
        return json_string.strip()
