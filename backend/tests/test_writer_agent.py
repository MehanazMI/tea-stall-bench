"""
Unit tests for Writer Agent

Tests the WriterAgent class with mocked LLM Client.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from backend.agents.writer_agent import WriterAgent
from backend.utils.llm_client import LLMClient


class TestWriterAgentInitialization:
    """Test suite for WriterAgent initialization."""
    
    def test_initialization_with_llm_client(self):
        """Test that agent initializes correctly with LLM client."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        assert agent.name == "Writer"
        assert agent.llm_client == mock_client
    
    def test_initialization_without_llm_client(self):
        """Test that initialization fails without LLM client."""
        with pytest.raises(ValueError, match="LLM client is required"):
            WriterAgent(None)
    
    def test_repr(self):
        """Test string representation."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        repr_str = repr(agent)
        assert "WriterAgent" in repr_str
        assert "Writer" in repr_str


class TestWriterAgentValidation:
    """Test suite for input validation."""
    
    def test_validate_empty_input(self):
        """Test that empty input raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Input data cannot be empty"):
            agent._validate_input({})
    
    def test_validate_missing_topic(self):
        """Test that missing topic raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Topic is required"):
            agent._validate_input({"content_type": "blog_post"})
    
    def test_validate_empty_topic(self):
        """Test that empty topic string raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Topic is required"):
            agent._validate_input({"topic": ""})
    
    def test_validate_invalid_content_type(self):
        """Test that invalid content_type raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Invalid content_type"):
            agent._validate_input({
                "topic": "Test",
                "content_type": "invalid_type"
            })
    
    def test_validate_invalid_style(self):
        """Test that invalid style raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Invalid style"):
            agent._validate_input({
                "topic": "Test",
                "style": "invalid_style"
            })
    
    def test_validate_invalid_tone(self):
        """Test that invalid tone raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Invalid tone"):
            agent._validate_input({
                "topic": "Test",
                "tone": "invalid_tone"
            })
    
    def test_validate_valid_input(self):
        """Test that valid input passes validation."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        # Should not raise
        agent._validate_input({
            "topic": "Python Tips",
            "content_type": "blog_post",
            "style": "professional",
            "tone": "friendly"
        })
    
    def test_validate_invalid_length(self):
        """Test that invalid length raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Invalid length"):
            agent._validate_input({
                "topic": "Test",
                "length": "invalid_length"
            })


class TestWriterAgentPromptBuilding:
    """Test suite for prompt building."""
    
    def test_build_basic_prompt(self):
        """Test building a basic prompt."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        prompt = agent._build_prompt(
            topic="Python Tips",
            content_type="blog_post",
            style="professional",
            tone="friendly",
            length="medium",
            channel="blog",
            additional_context=""
        )
        
        assert "Python Tips" in prompt
        assert "blog_post" in prompt
        assert "professional" in prompt
        assert "friendly" in prompt
    
    def test_build_prompt_with_context(self):
        """Test building prompt with additional context."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        prompt = agent._build_prompt(
            topic="Python Tips",
            content_type="blog_post",
            style="professional",
            tone="friendly",
            length="medium",
            channel="blog",
            additional_context="Focus on beginners"
        )
        
        assert "Focus on beginners" in prompt


class TestWriterAgentContentParsing:
    """Test suite for content parsing."""
    
    def test_parse_content_with_clear_title(self):
        """Test parsing content with clear title."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        generated = """10 Python Tips for Beginners

Python is a great language for beginners.
Here are 10 tips to get started."""
        
        title, content = agent._parse_generated_content(generated)
        
        assert title == "10 Python Tips for Beginners"
        assert "Python is a great language" in content
    
    def test_parse_content_with_title_prefix(self):
        """Test parsing content with 'Title:' prefix."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        generated = """Title: Python Best Practices

Content here."""
        
        title, content = agent._parse_generated_content(generated)
        
        assert title == "Python Best Practices"
        assert "Content here" in content
    
    def test_parse_content_with_markdown_header(self):
        """Test parsing content with markdown header."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        generated = """# Getting Started with Python

Python is easy to learn."""
        
        title, content = agent._parse_generated_content(generated)
        
        assert title == "Getting Started with Python"


class TestWriterAgentExecution:
    """Test suite for content generation."""
    
    @pytest.mark.asyncio
    async def test_execute_basic_blog_post(self):
        """Test generating a basic blog post."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = """Writing Great Code

Clean code is important.
Here are some tips."""
        
        agent = WriterAgent(mock_client)
        result = await agent.execute({
            "topic": "Writing Great Code"
        })
        
        assert result['status'] == 'success'
        assert result['agent'] == 'Writer'
        assert 'title' in result
        assert 'content' in result
        assert 'word_count' in result
        assert result['word_count'] > 0
        assert 'metadata' in result
    
    @pytest.mark.asyncio
    async def test_execute_with_all_options(self):
        """Test generating with all options specified."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = """Python Tutorial

This is a comprehensive tutorial."""
        
        agent = WriterAgent(mock_client)
        result = await agent.execute({
            "topic": "Python Basics",
            "content_type": "tutorial",
            "style": "technical",
            "tone": "formal",
            "length": "long",
            "additional_context": "For advanced users"
        })
        
        assert result['status'] == 'success'
        assert result['metadata']['content_type'] == 'tutorial'
        assert result['metadata']['style'] == 'technical'
        assert result['metadata']['tone'] == 'formal'
    
    @pytest.mark.asyncio
    async def test_execute_calls_llm_client(self):
        """Test that execution calls LLM client generate method."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = "Title\nContent"
        
        agent = WriterAgent(mock_client)
        await agent.execute({"topic": "Test Topic"})
        
        mock_client.generate.assert_called_once()
        call_args = mock_client.generate.call_args
        assert "Test Topic" in call_args.kwargs['prompt']
    
    @pytest.mark.asyncio
    async def test_execute_with_invalid_input(self):
        """Test that execution fails with invalid input."""
        mock_client = AsyncMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(Exception):  # Will raise ValueError via execute
            await agent.execute({"invalid": "data"})
    
    @pytest.mark.asyncio
    async def test_execute_different_content_types(self):
        """Test generating different content types."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = "Title\nContent"
        
        agent = WriterAgent(mock_client)
        
        for content_type in WriterAgent.CONTENT_TYPES:
            result = await agent.execute({
                "topic": "Test",
                "content_type": content_type
            })
            assert result['metadata']['content_type'] == content_type
