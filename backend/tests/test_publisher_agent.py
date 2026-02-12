"""
Tests for Publisher Agent
"""

import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from backend.agents.publisher_agent import PublisherAgent
from backend.utils.llm_client import LLMClient


class TestPublisherAgentValidation:
    """Test suite for input validation."""
    
    def test_validate_missing_phone(self):
        """Test that missing phone number raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        with pytest.raises(ValueError, match="Phone number is required"):
            agent._validate_input({
                "content": "Test message"
            })
    
    def test_validate_empty_phone(self):
        """Test that empty phone number raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        with pytest.raises(ValueError, match="Phone number must be a non-empty string"):
            agent._validate_input({
                "phone_number": "",
                "content": "Test"
            })
    
    def test_validate_missing_content(self):
        """Test that missing content raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        with pytest.raises(ValueError, match="Content is required"):
            agent._validate_input({
                "phone_number": "+1234567890"
            })
    
    def test_validate_empty_content(self):
        """Test that empty content raises error."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        with pytest.raises(ValueError, match="Content must be a non-empty string"):
            agent._validate_input({
                "phone_number": "+1234567890",
                "content": ""
            })
    
    def test_validate_valid_input(self):
        """Test that valid input passes validation."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        # Should not raise
        agent._validate_input({
            "phone_number": "+1234567890",
            "content": "Test message"
        })


class TestPublisherAgentFormatting:
    """Test suite for message formatting."""
    
    def test_format_message_no_title(self):
        """Test formatting message without title."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        result = agent._format_message("Hello World")
        assert result == "Hello World"
    
    def test_format_message_with_title(self):
        """Test formatting message with title."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        result = agent._format_message("Hello World", "Greeting")
        assert result == "*Greeting*\n\nHello World"
    
    def test_format_message_strips_whitespace(self):
        """Test that formatting strips excessive whitespace."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        result = agent._format_message("  Hello  \n\n  World  ")
        assert result == "Hello  \n\n  World"  # Internal spaces preserved


class TestPublisherAgentExecution:
    """Test suite for publishing execution."""
    
    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Test successful publishing."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        # Mock WhatsApp client
        with patch.object(agent.whatsapp_client, 'send_message') as mock_send:
            mock_send.return_value = {
                'phone_number': '+12345678900',
                'message_length': 11,
                'sent_at': '2026-02-10T23:30:00'
            }
            
            result = await agent.execute({
                "phone_number": "+12345678900",
                "content": "Hello World"
            })
            
            assert result['status'] == 'success'
            assert result['phone_number'] == '+12345678900'
            assert result['message_length'] == 11
            assert result['delivery_method'] == 'automatic'
    
    @pytest.mark.asyncio
    async def test_execute_with_title(self):
        """Test publishing with title."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        with patch.object(agent.whatsapp_client, 'send_message') as mock_send:
            mock_send.return_value = {
                'phone_number': '+1234567890',
                'message_length': 30,
                'sent_at': '2026-02-10T23:30:00'
            }
            
            result = await agent.execute({
                "phone_number": "+1234567890",
                "content": "Hello World",
                "title": "Greeting"
            })
            
            # Verify formatted message was sent
            call_args = mock_send.call_args
            assert "*Greeting*" in call_args[0][1]  # Title in message
    
    @pytest.mark.asyncio
    async def test_execute_manual_review_mode(self):
        """Test publishing in manual review mode."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        with patch.object(agent.whatsapp_client, 'send_instant') as mock_instant:
            mock_instant.return_value = {
                'status': 'ready',
                'phone_number': '+12345678900'
            }
            
            result = await agent.execute({
                "phone_number": "+12345678900",
                "content": "Hello World",
                "auto_send": False  # Manual review mode
            })
            
            assert result['status'] == 'success'
            assert result['delivery_method'] == 'manual_review'
    
    @pytest.mark.asyncio
    async def test_execute_handles_errors(self):
        """Test that execution handles WhatsApp errors."""
        mock_client = MagicMock(spec=LLMClient)
        agent = PublisherAgent(mock_client)
        
        with patch.object(agent.whatsapp_client, 'send_message') as mock_send:
            mock_send.side_effect = Exception("WhatsApp connection failed")
            
            with pytest.raises(Exception, match="WhatsApp connection failed"):
                await agent.execute({
                    "phone_number": "+1234567890",
                    "content": "Hello World"
                })
