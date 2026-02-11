"""
Additional tests for Writer Agent channel functionality
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
from backend.agents.writer_agent import WriterAgent
from backend.utils.llm_client import LLMClient


class TestWriterAgentChannels:
    """Test suite for channel-specific functionality."""
    
    def test_validate_invalid_channel(self):
        """Test that invalid channel raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        with pytest.raises(ValueError, match="Invalid channel"):
            agent._validate_input({
                "topic": "Test",
                "channel": "invalid_channel"
            })
    
    def test_validate_valid_channel(self):
        """Test that valid channel passes validation."""
        mock_client = MagicMock(spec=LLMClient)
        agent = WriterAgent(mock_client)
        
        # Should not raise
        for channel in WriterAgent.CHANNELS:
            agent._validate_input({
                "topic": "Test",
                "channel": channel
            })
    
    @pytest.mark.asyncio
    async def test_execute_with_whatsapp_channel(self):
        """Test generating with WhatsApp channel."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = "Quick Tip\\n\\nShort content for WhatsApp."
        
        agent = WriterAgent(mock_client)
        result = await agent.execute({
            "topic": "Python tip",
            "channel": "whatsapp",
            "length": "short"
        })
        
        assert result['metadata']['channel'] == 'whatsapp'
        # Verify prompt includes WhatsApp-specific length
        call_args = mock_client.generate.call_args
        assert "100-200 words" in call_args.kwargs['prompt']
    
    @pytest.mark.asyncio
    async def test_execute_with_instagram_channel(self):
        """Test generating with Instagram channel."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = "Caption\\n\\nBrief Instagram caption."
        
        agent = WriterAgent(mock_client)
        result = await agent.execute({
            "topic": "Code quote",
            "channel": "instagram",
            "length": "medium"
        })
        
        assert result['metadata']['channel'] == 'instagram'
        # Verify prompt includes Instagram-specific length
        call_args = mock_client.generate.call_args
        assert "100-150 words" in call_args.kwargs['prompt']
    
    @pytest.mark.asyncio
    async def test_channel_defaults_to_blog(self):
        """Test that channel defaults to 'blog' if not specified."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = "Title\\nContent"
        
        agent = WriterAgent(mock_client)
        result = await agent.execute({
            "topic": "Test"
        })
        
        assert result['metadata']['channel'] == 'blog'
    
    @pytest.mark.asyncio
    async def test_linkedin_channel_length(self):
        """Test LinkedIn channel uses correct length guidelines."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = "Professional Post\\nLinkedIn content."
        
        agent = WriterAgent(mock_client)
        result = await agent.execute({
            "topic": "Career advice",
            "channel": "linkedin",
            "length": "long"
        })
        
        assert result['metadata']['channel'] == 'linkedin'
        call_args = mock_client.generate.call_args
        assert "600-1000 words" in call_args.kwargs['prompt']
    
    @pytest.mark.asyncio
    async def test_email_channel_length(self):
        """Test Email channel uses correct length guidelines."""
        mock_client = AsyncMock(spec=LLMClient)
        mock_client.generate.return_value = "Newsletter Title\\nEmail content."
        
        agent = WriterAgent(mock_client)
        result = await agent.execute({
            "topic": "Weekly update",
            "channel": "email",
            "length": "short"
        })
        
        assert result['metadata']['channel'] == 'email'
        call_args = mock_client.generate.call_args
        assert "200-400 words" in call_args.kwargs['prompt']
