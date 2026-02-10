"""
Writer Agent (Ink) for Tea Stall Bench

This agent generates written content (blog posts, articles, tutorials) using the LLM Client.
It provides a clean interface for content creation with configurable styles and tones.
"""

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
    STYLES = ['professional', 'casual', 'technical', 'creative']
    TONES = ['friendly', 'formal', 'conversational', 'authoritative']
    LENGTHS = ['short', 'medium', 'long']
    
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
                - tone (str): Writing tone (default: 'friendly')
                - length (str): Content length (default: 'medium')
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
        tone = input_data.get('tone', 'friendly')
        length = input_data.get('length', 'medium')
        additional_context = input_data.get('additional_context', '')
        
        # Build prompt
        prompt = self._build_prompt(
            topic=topic,
            content_type=content_type,
            style=style,
            tone=tone,
            length=length,
            additional_context=additional_context
        )
        
        self.logger.info(f"Generating {content_type} about '{topic}'")
        
        # Generate content using LLM
        generated_content = await self.llm_client.generate(
            prompt=prompt,
            temperature=0.7  # Balanced creativity
        )
        
        # Extract title and content
        title, content = self._parse_generated_content(generated_content)
        
        # Calculate word count
        word_count = len(content.split())
        
        return {
            'title': title,
            'content': content,
            'word_count': word_count,
            'metadata': {
                'topic': topic,
                'content_type': content_type,
                'style': style,
                'tone': tone,
                'length': length
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
        
        # Validate tone if provided
        if 'tone' in input_data:
            if input_data['tone'] not in self.TONES:
                raise ValueError(
                    f"Invalid tone. Must be one of: {', '.join(self.TONES)}"
                )
    
    def _build_prompt(
        self,
        topic: str,
        content_type: str,
        style: str,
        tone: str,
        length: str,
        additional_context: str
    ) -> str:
        """
        Build a prompt for the LLM based on parameters.
        
        Args:
            topic: Topic to write about
            content_type: Type of content
            style: Writing style
            tone: Writing tone
            length: Desired length
            additional_context: Additional context
            
        Returns:
            str: Formatted prompt for LLM
        """
        # Length guidelines
        length_guide = {
            'short': '300-500 words',
            'medium': '600-1000 words',
            'long': '1200-1800 words'
        }
        
        # Build the prompt
        prompt = f"""Write a {style} {content_type} about: {topic}

Requirements:
- Tone: {tone}
- Style: {style}
- Target length: {length_guide.get(length, '600-1000 words')}
- Format: Start with a clear title on the first line, followed by the content

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
        
        # First non-empty line is the title
        title = lines[0].strip()
        
        # Remove common title prefixes
        title_prefixes = ['Title:', 'title:', '#', '##']
        for prefix in title_prefixes:
            if title.startswith(prefix):
                title = title[len(prefix):].strip()
        
        # Rest is content (skip empty lines after title)
        content_lines = []
        found_content = False
        for line in lines[1:]:
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
