"""
LLM Client for Tea Stall Bench

This module provides a unified interface for interacting with different LLM providers
(Ollama for local LLMs, OpenAI for cloud LLMs). Configuration is loaded from environment
variables, and the client automatically initializes the appropriate provider.
"""

import os
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


class LLMClient:
    """
    Unified client for LLM interactions supporting multiple providers.
    
    Automatically configures based on environment variables:
    - LLM_TYPE: 'ollama' or 'openai'
    - MODEL_NAME: Model to use (e.g., 'llama3' for Ollama, 'gpt-4' for OpenAI)
    - OPENAI_API_KEY: Required when using OpenAI
    
    Example:
        >>> # With Ollama (local)
        >>> client = LLMClient()  # Reads from .env: LLM_TYPE=ollama, MODEL_NAME=llama3
        >>> response = await client.generate("Write a blog post about Python")
        
        >>> # With OpenAI (cloud)
        >>> # .env: LLM_TYPE=openai, MODEL_NAME=gpt-4, OPENAI_API_KEY=sk-...
        >>> client = LLMClient()
        >>> response = await client.generate("Write a blog post about Python")
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the LLM client with configuration from environment variables.
        
        Args:
            config_path (Optional[str]): Path to .env file. If None, uses default search.
        
        Raises:
            ValueError: If LLM_TYPE is not 'ollama' or 'openai'
            ValueError: If OPENAI_API_KEY is missing when using OpenAI
        """
        self.logger = logging.getLogger("TeaStallBench.LLMClient")
        
        # Load configuration
        self._load_config(config_path)
        
        # Initialize the appropriate client
        self._initialize_client()
        
        self.logger.info(f"LLM Client initialized: {self.llm_type} with model {self.model_name}")
    
    def _load_config(self, config_path: Optional[str] = None):
        """
        Load configuration from environment variables.
        
        Args:
            config_path (Optional[str]): Path to .env file
        """
        # Load .env file
        if config_path:
            load_dotenv(config_path)
        else:
            load_dotenv()
        
        # Get LLM type (ollama or openai)
        self.llm_type = os.getenv('LLM_TYPE', 'ollama').lower()
        
        if self.llm_type not in ['ollama', 'openai']:
            raise ValueError(
                f"Invalid LLM_TYPE: {self.llm_type}. Must be 'ollama' or 'openai'"
            )
        
        # Get model name
        default_model = 'llama3' if self.llm_type == 'ollama' else 'gpt-4'
        self.model_name = os.getenv('MODEL_NAME', default_model)
        
        # Get OpenAI API key if using OpenAI
        if self.llm_type == 'openai':
            self.api_key = os.getenv('OPENAI_API_KEY')
            if not self.api_key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required when LLM_TYPE=openai"
                )
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on configuration."""
        if self.llm_type == 'ollama':
            import ollama
            self.client = ollama
            self.logger.debug("Initialized Ollama client")
            
        elif self.llm_type == 'openai':
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=self.api_key)
            self.logger.debug("Initialized OpenAI client")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True
    )
    async def generate(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate content from a prompt using the configured LLM.
        
        This method automatically retries on connection errors with exponential backoff.
        
        Args:
            prompt (str): The user prompt/question to send to the LLM
            system_prompt (Optional[str]): System prompt to set context/behavior
            temperature (float): Randomness in generation (0.0-1.0). Default 0.7
            max_tokens (Optional[int]): Maximum tokens to generate
            **kwargs: Additional provider-specific parameters
        
        Returns:
            str: Generated text response from the LLM
        
        Raises:
            ConnectionError: If unable to connect to LLM service after retries
            TimeoutError: If request times out after retries
            ValueError: If prompt is empty
            Exception: Other LLM-specific errors
        
        Example:
            >>> response = await client.generate(
            ...     "Write a haiku about coding",
            ...     system_prompt="You are a creative poet",
            ...     temperature=0.9
            ... )
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        self.logger.info(f"Generating content with {self.llm_type}")
        self.logger.debug(f"Prompt: {prompt[:100]}...")
        
        try:
            if self.llm_type == 'ollama':
                return await self._generate_ollama(prompt, system_prompt, temperature, max_tokens, **kwargs)
            else:  # openai
                return await self._generate_openai(prompt, system_prompt, temperature, max_tokens, **kwargs)
                
        except Exception as e:
            self.logger.error(f"LLM generation failed: {str(e)}", exc_info=True)
            raise
    
    async def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        **kwargs
    ) -> str:
        """Generate content using Ollama."""
        import asyncio
        
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        # Ollama parameters
        options = {
            "temperature": temperature,
        }
        if max_tokens:
            options["num_predict"] = max_tokens
        
        # Merge with any additional kwargs
        options.update(kwargs)
        
        # Call Ollama (synchronous API - wrap in asyncio.to_thread)
        response = await asyncio.to_thread(
            self.client.chat,
            model=self.model_name,
            messages=messages,
            options=options
        )
        
        return response['message']['content']
    
    async def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
        **kwargs
    ) -> str:
        """Generate content using OpenAI."""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        # OpenAI parameters
        params: Dict[str, Any] = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            params["max_tokens"] = max_tokens
        
        # Merge with any additional kwargs
        params.update(kwargs)
        
        # Call OpenAI (async API)
        response = await self.client.chat.completions.create(**params)
        
        return response.choices[0].message.content
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"LLMClient(type='{self.llm_type}', model='{self.model_name}')"
