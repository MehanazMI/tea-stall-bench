"""
Additional tests for Writer Agent code review improvements
"""

import pytest
from unittest.mock import MagicMock
from backend.agents.writer_agent import WriterAgent
from backend.utils.llm_client import LLMClient


class TestWriterAgentTemperature:
    """Test suite for temperature configuration."""
    
    def test_temperature_for_technical_style(self):
        """Test that technical style uses lower temperature."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        temp = agent._get_temperature_for_style('technical')
        assert temp == 0.5
    
    def test_temperature_for_creative_style(self):
        """Test that creative style uses higher temperature."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        temp = agent._get_temperature_for_style('creative')
        assert temp == 0.9
    
    def test_temperature_for_professional_style(self):
        """Test that professional style uses balanced temperature."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        temp = agent._get_temperature_for_style('professional')
        assert temp == 0.7
    
    def test_temperature_for_casual_style(self):
        """Test that casual style uses slightly higher temperature."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        temp = agent._get_temperature_for_style('casual')
        assert temp == 0.8
    
    def test_temperature_default_for_unknown_style(self):
        """Test that unknown style defaults to 0.7."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        temp = agent._get_temperature_for_style('unknown')
        assert temp == 0.7


class TestWriterAgentParsing:
    """Test suite for improved title parsing."""
    
    def test_parse_content_with_preamble(self):
        """Test parsing content that has preamble before title."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        generated = """Here's your blog post:

10 Python Tips for Beginners

Python is a great language.
Here are 10 tips."""
        
        title, content = agent._parse_generated_content(generated)
        
        # Should skip preamble and get actual title
        assert "10 Python Tips" in title
        assert "Here's your blog post" not in title
    
    def test_parse_content_with_markdown_tripple_hash(self):
        """Test parsing content with ### prefix."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        generated = """### Python Best Practices

Content here."""
        
        title, content = agent._parse_generated_content(generated)
        
        assert title == "Python Best Practices"
        assert "###" not in title
