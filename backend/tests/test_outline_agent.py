
import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.agents.outline_agent import OutlineAgent, Outline
from backend.utils.llm_client import LLMClient

class TestOutlineAgent:
    
    @pytest.mark.asyncio
    async def test_execute_valid_outline(self):
        """Test generating a valid outline from LLM response."""
        mock_client = AsyncMock(spec=LLMClient)
        # Mock valid JSON response
        mock_client.generate.return_value = """
        {
            "title": "The Art of Tea",
            "sections": [
                {
                    "heading": "Introduction",
                    "key_points": ["History of tea", "Cultural significance"]
                }
            ]
        }
        """
        
        agent = OutlineAgent(mock_client)
        result = await agent.execute({"topic": "Tea"})
        
        assert result['status'] == 'success'
        assert result['outline']['title'] == "The Art of Tea"
        assert len(result['outline']['sections']) == 1
        assert result['outline']['sections'][0]['heading'] == "Introduction"

    @pytest.mark.asyncio
    async def test_execute_retry_logic(self):
        """Test that agent retries on invalid JSON."""
        mock_client = AsyncMock(spec=LLMClient)
        # First call returns garbage, second returns valid JSON
        mock_client.generate.side_effect = [
            "Not JSON at all",
            """
            {
                "title": "Retry Success",
                "sections": []
            }
            """
        ]
        
        agent = OutlineAgent(mock_client)
        result = await agent.execute({"topic": "Retry Test"})
        
        assert result['status'] == 'success'
        assert result['outline']['title'] == "Retry Success"
        # Verify generate was called twice
        assert mock_client.generate.call_count == 2

    @pytest.mark.asyncio
    async def test_execute_failure_after_max_retries(self):
        """Test that agent raises error after max retries."""
        mock_client = AsyncMock(spec=LLMClient)
        # All calls return invalid JSON
        mock_client.generate.return_value = "Invalid JSON"
        
        agent = OutlineAgent(mock_client)
        
        # Expect failure
        with pytest.raises(ValueError, match="Failed to generate valid outline"):
            await agent.execute({"topic": "Fail Test"})
