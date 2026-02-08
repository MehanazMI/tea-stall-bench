"""
Unit tests for LLM Client

Tests the LLMClient class with mocked LLM providers to avoid real API calls.
"""

import pytest
import os
from unittest.mock import Mock, AsyncMock, patch, MagicMock


class TestLLMClientConfiguration:
    """Test suite for LLMClient configuration and initialization."""
    
    @patch.dict(os.environ, {
        'LLM_TYPE': 'ollama',
        'MODEL_NAME': 'llama3'
    })
    @patch('ollama.chat')
    def test_ollama_initialization(self, mock_chat):
        """Test that client initializes correctly for Ollama."""
        from backend.utils.llm_client import LLMClient
        
        client = LLMClient()
        
        assert client.llm_type == 'ollama'
        assert client.model_name == 'llama3'
    
    @patch.dict(os.environ, {
        'LLM_TYPE': 'openai',
        'MODEL_NAME': 'gpt-4',
        'OPENAI_API_KEY': 'sk-test123'
    })
    @patch('openai.AsyncOpenAI')
    def test_openai_initialization(self, mock_openai):
        """Test that client initializes correctly for OpenAI."""
        from backend.utils.llm_client import LLMClient
        
        client = LLMClient()
        
        assert client.llm_type == 'openai'
        assert client.model_name == 'gpt-4'
        assert client.api_key == 'sk-test123'
    
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'}, clear=True)
    @patch('ollama.chat')
    def test_default_model_ollama(self, mock_chat):
        """Test that default model is set correctly for Ollama."""
        from backend.utils.llm_client import LLMClient
        
        client = LLMClient()
        
        assert client.model_name == 'llama3'
    
    @patch.dict(os.environ, {
        'LLM_TYPE': 'openai',
        'OPENAI_API_KEY': 'sk-test'
    }, clear=True)
    @patch('openai.AsyncOpenAI')
    def test_default_model_openai(self, mock_openai):
        """Test that default model is set correctly for OpenAI."""
        from backend.utils.llm_client import LLMClient
        
        client = LLMClient()
        
        assert client.model_name == 'gpt-4'
    
    @patch.dict(os.environ,{'LLM_TYPE': 'invalid'}, clear=True)
    def test_invalid_llm_type(self):
        """Test that invalid LLM_TYPE raises ValueError."""
        from backend.utils.llm_client import LLMClient
        
        with pytest.raises(ValueError, match="Invalid LLM_TYPE"):
            LLMClient()
    
    @patch.dict(os.environ, {'LLM_TYPE': 'openai'}, clear=True)
    def test_missing_openai_api_key(self):
        """Test that missing OPENAI_API_KEY raises ValueError."""
        from backend.utils.llm_client import LLMClient
        
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            LLMClient()
    
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    def test_repr(self, mock_chat):
        """Test string representation of client."""
        from backend.utils.llm_client import LLMClient
        
        client = LLMClient()
        repr_str = repr(client)
        
        assert 'LLMClient' in repr_str
        assert 'ollama' in repr_str


class TestLLMClientGeneration:
    """Test suite for content generation with mocked LLM responses."""
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama', 'MODEL_NAME': 'llama3'})
    @patch('ollama.chat')
    async def test_ollama_generation(self, mock_chat):
        """Test content generation with Ollama."""
        from backend.utils.llm_client import LLMClient
        
        mock_chat.return_value = {
            'message': {'content': 'Generated content from Ollama'}
        }
        
        client = LLMClient()
        response = await client.generate("Test prompt")
        
        assert response == 'Generated content from Ollama'
        mock_chat.assert_called_once()
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {
        'LLM_TYPE': 'openai',
        'MODEL_NAME': 'gpt-4',
        'OPENAI_API_KEY': 'sk-test'
    })
    @patch('openai.AsyncOpenAI')
    async def test_openai_generation(self, mock_openai_class):
        """Test content generation with OpenAI."""
        from backend.utils.llm_client import LLMClient
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = 'Generated content from OpenAI'
        
        mock_client = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai_class.return_value = mock_client
        
        client = LLMClient()
        response = await client.generate("Test prompt")
        
        assert response == 'Generated content from OpenAI'
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    async def test_generation_with_system_prompt(self, mock_chat):
        """Test generation with system prompt."""
        from backend.utils.llm_client import LLMClient
        
        mock_chat.return_value = {
            'message': {'content': 'Response with system prompt'}
        }
        
        client = LLMClient()
        await client.generate(
            "User prompt",
            system_prompt="You are a helpful assistant"
        )
        
        # Verify system prompt was included
        call_kwargs = mock_chat.call_args.kwargs
        messages = call_kwargs['messages']
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    async def test_generation_with_temperature(self, mock_chat):
        """Test generation with custom temperature."""
        from backend.utils.llm_client import LLMClient
        
        mock_chat.return_value = {
            'message': {'content': 'Response'}
        }
        
        client = LLMClient()
        await client.generate("Test", temperature=0.9)
        
        call_kwargs = mock_chat.call_args.kwargs
        assert call_kwargs['options']['temperature'] == 0.9
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    async def test_empty_prompt_raises_error(self, mock_chat):
        """Test that empty prompt raises ValueError."""
        from backend.utils.llm_client import LLMClient
        
        client = LLMClient()
        
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            await client.generate("")
        
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            await client.generate("   ")
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    async def test_generation_exception_handling(self, mock_chat):
        """Test that exceptions from LLM are properly raised."""
        from backend.utils.llm_client import LLMClient
        
        mock_chat.side_effect = Exception("LLM service error")
        
        client = LLMClient()
        
        with pytest.raises(Exception, match="LLM service error"):
            await client.generate("Test prompt")


class TestLLMClientRetry:
    """Test suite for retry logic."""
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    async def test_retry_on_connection_error(self, mock_chat):
        """Test that client retries on ConnectionError."""
        from backend.utils.llm_client import LLMClient
        
        # Fail twice, then succeed
        mock_chat.side_effect = [
            ConnectionError("Connection failed"),
            ConnectionError("Connection failed again"),
            {'message': {'content': 'Success after retry'}}
        ]
        
        client = LLMClient()
        response = await client.generate("Test prompt")
        
        assert response == 'Success after retry'
        assert mock_chat.call_count == 3
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    async def test_max_retries_exceeded(self, mock_chat):
        """Test that client gives up after max retries."""
        from backend.utils.llm_client import LLMClient
        
        mock_chat.side_effect = ConnectionError("Persistent connection error")
        
        client = LLMClient()
        
        with pytest.raises(ConnectionError):
            await client.generate("Test prompt")
        
        # Should try 3 times (initial + 2 retries)
        assert mock_chat.call_count == 3


class TestLLMClientIntegration:
    """Integration-style tests for LLMClient."""
    
    @pytest.mark.asyncio
    @patch.dict(os.environ, {'LLM_TYPE': 'ollama'})
    @patch('ollama.chat')
    async def test_multiple_sequential_generations(self, mock_chat):
        """Test multiple generation calls work correctly."""
        from backend.utils.llm_client import LLMClient
        
        mock_chat.side_effect = [
            {'message': {'content': 'Response 1'}},
            {'message': {'content': 'Response 2'}},
            {'message': {'content': 'Response 3'}},
        ]
        
        client = LLMClient()
        
        resp1 = await client.generate("Prompt 1")
        resp2 = await client.generate("Prompt 2")
        resp3 = await client.generate("Prompt 3")
        
        assert resp1 == 'Response 1'
        assert resp2 == 'Response 2'
        assert resp3 == 'Response 3'
        assert mock_chat.call_count == 3
