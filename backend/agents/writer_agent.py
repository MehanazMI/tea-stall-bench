"""
Writer Agent (Ink) for Tea Stall Bench

This agent generates written content (blog posts, articles, tutorials) using the LLM Client.
It provides a clean interface for content creation with configurable styles and tones.
""" 

import re
from typing import Dict, Any, Optional
from backend.agents.base_agent import BaseAgent
from backend.utils.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """
    Agent that generates written content using LLM.
    
    Supports various content types (blog posts, articles, tutorials),
    writing styles (professional, casual, technical), and tones
    (friendly, formal, conversational).
    
    Example:
        >>> llm_client = LLMClient()
        >>> writer = WriterAgent(llm_client)
        >>> result = await writer.execute({
        ...     "topic": "Python Tips for Beginners",
        ...     "content_type": "blog_post",
        ...     "style": "professional",
        ...     "tone": "friendly"
        ... })
        >>> print(result['title'])
        >>> print(result['content'])
    """
    
    # Supported options
    CONTENT_TYPES = ['blog_post', 'article', 'tutorial', 'how_to_guide']
    
    # Writing styles (unified style + tone) - ordered by temperature (factual → creative)
    STYLES = [
        'technical',       # Precise, factual, detailed (temp: 0.3)
        'educational',     # Teaching, clear, structured (temp: 0.5)
        'professional',    # Business-like, polished (temp: 0.6)
        'friendly',        # Warm, casual, approachable (temp: 0.75)
        'inspirational',   # Motivating, uplifting (temp: 0.8)
        'storytelling'     # Narrative, engaging, compelling (temp: 0.9)
    ]
    LENGTHS = ['short', 'medium', 'long']
    CHANNELS = ['instagram', 'whatsapp', 'linkedin', 'email', 'blog']
    
    # Channel-specific length guidelines (in words)
    # Ordered by word count: shortest → longest
    CHANNEL_LENGTH_GUIDES = {
        'instagram': {
            'short': '50-100 words',
            'medium': '100-150 words',
            'long': '150-200 words'
        },
        'whatsapp': {
            'short': '100-200 words',
            'medium': '200-400 words',
            'long': '400-600 words'
        },
        'linkedin': {
            'short': '150-300 words',
            'medium': '300-600 words',
            'long': '600-1000 words'
        },
        'email': {
            'short': '200-400 words',
            'medium': '400-800 words',
            'long': '800-1200 words'
        },
        'blog': {
            'short': '300-500 words',
            'medium': '600-1000 words',
            'long': '1200-1800 words'
        }
    }
    
    def __init__(self, llm_client: LLMClient):
        """
        Initialize the Writer Agent.
        
        Args:
            llm_client (LLMClient): LLM client instance for content generation
            
        Raises:
            ValueError: If llm_client is None
        """
        if llm_client is None:
            raise ValueError("LLM client is required for WriterAgent")
            
        super().__init__(name="Writer", llm_client=llm_client)
    
    async def _execute_internal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate written content based on input parameters.
        
        Args:
            input_data (Dict[str, Any]): Input containing:
                - topic (str): The topic to write about (required)
                - content_type (str): Type of content (default: 'blog_post')
                - style (str): Writing style (default: 'professional')
                - length (str): Content length (default: 'medium')
                - channel (str): Publishing channel (default: 'blog')
                - additional_context (str): Extra context (optional)
        
        Returns:
            Dict[str, Any]: Generated content with:
                - title (str): Generated title
                - content (str): Full content body
                - word_count (int): Approximate word count
                - metadata (dict): Content metadata
        
        Raises:
            ValueError: If required parameters are missing
        """
        # Validate input
        self._validate_input(input_data)
        
        # Extract parameters
        topic = input_data['topic']
        content_type = input_data.get('content_type', 'blog_post')
        style = input_data.get('style', 'professional')
        length = input_data.get('length', 'medium')
        channel = input_data.get('channel', 'blog')
        additional_context = input_data.get('additional_context', '')
        
        # Build prompt
        prompt = self._build_prompt(
            topic=topic,
            content_type=content_type,
            style=style,
            length=length,
            channel=channel,
            additional_context=additional_context
        )
        
        self.logger.info(f"Generating {content_type} about '{topic}' with {style} style")
        
        # Determine temperature based on style
        temperature = self._get_temperature_for_style(style)
        
        # Generate content using LLM
        generated_content = await self.llm_client.generate(
            prompt=prompt,
            temperature=temperature
        )
        
        # Extract title and content
        title, content = self._parse_generated_content(generated_content)
        
        # Calculate word count using regex for accuracy
        word_count = len(re.findall(r'\b\w+\b', content))
        
        return {
            'title': title,
            'content': content,
            'word_count': word_count,
            'metadata': {
                'topic': topic,
                'content_type': content_type,
                'style': style,
                'length': length,
                'channel': channel
            }
        }
    
    def _validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate input parameters.
        
        Args:
            input_data: Input data to validate
            
        Raises:
            ValueError: If validation fails
        """
        if not input_data:
            raise ValueError("Input data cannot be empty")
        
        if 'topic' not in input_data or not input_data['topic']:
            raise ValueError("Topic is required")
        
        # Validate content_type if provided
        if 'content_type' in input_data:
            if input_data['content_type'] not in self.CONTENT_TYPES:
                raise ValueError(
                    f"Invalid content_type. Must be one of: {', '.join(self.CONTENT_TYPES)}"
                )
        
        # Validate style if provided
        if 'style' in input_data:
            if input_data['style'] not in self.STYLES:
                raise ValueError(
                    f"Invalid style. Must be one of: {', '.join(self.STYLES)}"
                )
        
        # Validate length if provided
        if 'length' in input_data:
            if input_data['length'] not in self.LENGTHS:
                raise ValueError(
                    f"Invalid length. Must be one of: {', '.join(self.LENGTHS)}"
                )
        
        # Validate channel if provided
        if 'channel' in input_data:
            if input_data['channel'] not in self.CHANNELS:
                raise ValueError(
                    f"Invalid channel. Must be one of: {', '.join(self.CHANNELS)}"
                )
        
        # Validate channel if provided
        if 'channel' in input_data:
            if input_data['channel'] not in self.CHANNELS:
                raise ValueError(
                    f"Invalid channel. Must be one of: {', '.join(self.CHANNELS)}"
                )
    
    def _build_prompt(
        self,
        topic: str,
        content_type: str,
        style: str,
        length: str,
        channel: str,
        additional_context: str
    ) -> str:
        """
        Build a prompt for the LLM based on parameters.
        
        Args:
            topic: Topic to write about
            content_type: Type of content
            style: Writing style
            length: Desired length
            channel: Publishing channel
            additional_context: Additional context
            
        Returns:
            str: Formatted prompt for LLM
        """
        # Get channel-specific length guidelines
        channel_guides = self.CHANNEL_LENGTH_GUIDES.get(channel, self.CHANNEL_LENGTH_GUIDES['blog'])
        length_guide = channel_guides[length]
        
        # Build the prompt
        prompt = f"""Write a {content_type} about: {topic}

Requirements:
- Style: {style}
- Publishing channel: {channel}
- Target length: {length_guide}
- Format: Start with a clear title on the first line, followed by the content

Note: Optimize content for {channel} platform with a {style} style.

"""
        
        if additional_context:
            prompt += f"Additional context: {additional_context}\n\n"
        
        prompt += """Please write an engaging and well-structured piece that:
1. Has a clear, catchy title
2. Has a strong introduction
3. Provides valuable information
4. Uses clear headings/sections if appropriate
5. Has a strong conclusion

Begin with the title on the first line, then the content."""
        
        return prompt
    
    def _get_temperature_for_style(self, style: str) -> float:
        """
        Get appropriate temperature setting based on writing style.
        
        Args:
            style: Writing style
            
        Returns:
            float: Temperature value (0.0-1.0)
        """
        # Ordered by creativity level: factual → creative
        temperature_map = {
            'technical': 0.3,        # Precise, factual, minimal creativity
            'educational': 0.5,      # Clear, structured, some examples
            'professional': 0.6,     # Polished, controlled creativity
            'friendly': 0.75,        # Natural, warm, conversational
            'inspirational': 0.8,    # Engaging, motivating, creative
            'storytelling': 0.9      # Highly creative, narrative
        }
        
        return temperature_map.get(style, 0.6)
    
    def _parse_generated_content(self, generated_content: str) -> tuple[str, str]:
        """
        Parse generated content to extract title and body.
        
        Args:
            generated_content: Raw content from LLM
            
        Returns:
            tuple: (title, content)
        """
        lines = generated_content.strip().split('\n')
        
        if not lines:
            return "Untitled", generated_content
        
        # Find the actual title (skip preamble lines like "Here's your blog post:")
        title_line_index = 0
        preamble_indicators = ['here', 'here\'s', 'below', 'following']
        
        for i, line in enumerate(lines[:3]):  # Check first 3 lines
            line_lower = line.strip().lower()
            # Skip lines that look like preamble
            if any(indicator in line_lower for indicator in preamble_indicators):
                continue
            # Found likely title line
            if line.strip():
                title_line_index = i
                break
        
        title = lines[title_line_index].strip()
        
        # Remove common title prefixes
        title_prefixes = ['Title:', 'title:', '#', '##', '###']
        for prefix in title_prefixes:
            if title.startswith(prefix):
                title = title[len(prefix):].strip()
        
        # Rest is content (skip empty lines after title)
        content_lines = []
        found_content = False
        for line in lines[title_line_index + 1:]:  # Start after title line
            if line.strip() or found_content:
                content_lines.append(line)
                found_content = True
        
        content = '\n'.join(content_lines).strip()
        
        # If no separate content, use everything as content
        if not content:
            content = generated_content.strip()
            title = content.split('\n')[0][:100] + "..."  # First line as title
        
        return title, content
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"WriterAgent(name='{self.name}')"
