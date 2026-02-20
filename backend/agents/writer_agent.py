"""
Writer Agent (Ink) for Tea Stall Bench

This agent generates written content (blog posts, articles, tutorials) using the LLM Client.
It provides a clean interface for content creation with configurable styles and tones.
""" 

import re
import json
import logging
from typing import Dict, Any, Optional, List
from backend.agents.base_agent import BaseAgent
from backend.utils.llm_client import LLMClient
from backend.config import CONTENT_TYPES, STYLES, LENGTHS, CHANNELS, CHANNEL_LENGTH_GUIDES


class WriterAgent(BaseAgent):
    """
    Writer Agent (Ink) - Content generation specialist.
    
    Generates written content optimized for different platforms with configurable
    styles and formats. Optimized for WhatsApp publishing with storytelling narratives.
    
    Default Configuration (WhatsApp-optimized):
        - content_type: 'story' (engaging narratives)
        - style: 'storytelling' (creative, narrative, temp: 0.9)
        - channel: 'whatsapp' (mobile-friendly, 100-200 words)
        - length: 'short' (quick reads)
    
    Supports 6 content types, 6 styles, 5 channels, and 3 lengths.
    
    Example:
        >>> llm_client = LLMClient()
        >>> writer = WriterAgent(llm_client)
        >>> result = await writer.execute({"topic": "Python Tips"})
        >>> print(result['title'], result['content'])
    """
    
    
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
                - content_type (str): Type of content (default: 'story')
                - style (str): Writing style (default: 'storytelling')
                - length (str): Content length (default: 'short')
                - channel (str): Publishing channel (default: 'whatsapp')
                - additional_context (str): Extra context (optional)
                - outline (dict): Structured outline from Draft agent (optional)
        
        Returns:
            Dict[str, Any]: Generated content with:
                - title (str): Generated title
                - content (str): Full content body
                - word_count (int): Approximate word count
                - metadata (dict): Content metadata
                - compliance (dict): Outline compliance score (if outline provided)
        
        Raises:
            ValueError: If required parameters are missing
        """
        # Validate input
        self._validate_input(input_data)
        
        # Extract parameters
        topic = input_data['topic']
        content_type = input_data.get('content_type', 'story')
        style = input_data.get('style', 'storytelling')
        length = input_data.get('length', 'short')
        channel = input_data.get('channel', 'whatsapp')
        additional_context = input_data.get('additional_context', '')
        outline = input_data.get('outline', None)
        
        # Build prompt (outline-aware if outline provided)
        prompt = self._build_prompt(
            topic=topic,
            content_type=content_type,
            style=style,
            length=length,
            channel=channel,
            additional_context=additional_context,
            outline=outline
        )
        
        self.logger.info(f"Generating {content_type} about '{topic}' with {style} style")
        if outline:
            section_count = len(outline.get('sections', []))
            self.logger.info(f"Outline-aware mode: {section_count} sections to follow")
        
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
        
        result = {
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
        
        # Run compliance check if outline was provided
        if outline:
            compliance = self._check_compliance(content, outline)
            result['compliance'] = compliance
            self.logger.info(
                f"Compliance: {compliance['score']:.0%} "
                f"({len(compliance['covered'])}/{len(compliance['covered']) + len(compliance['missing'])} sections)"
            )
        
        return result
    
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
        # Validate content_type if provided
        if 'content_type' in input_data:
            if input_data['content_type'] not in CONTENT_TYPES:
                raise ValueError(
                    f"Invalid content_type. Must be one of: {', '.join(CONTENT_TYPES)}"
                )
        
        # Validate style if provided
        # Validate style if provided
        if 'style' in input_data:
            if input_data['style'] not in STYLES:
                raise ValueError(
                    f"Invalid style. Must be one of: {', '.join(STYLES)}"
                )
        
        # Validate length if provided
        if 'length' in input_data:
            if input_data['length'] not in LENGTHS:
                raise ValueError(
                    f"Invalid length. Must be one of: {', '.join(LENGTHS)}"
                )
        
        # Validate channel if provided
        if 'channel' in input_data:
            if input_data['channel'] not in CHANNELS:
                raise ValueError(
                    f"Invalid channel. Must be one of: {', '.join(CHANNELS)}"
                )
    
    def _build_prompt(
        self,
        topic: str,
        content_type: str,
        style: str,
        length: str,
        channel: str,
        additional_context: str,
        outline: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Build a prompt for the LLM based on parameters.
        
        When an outline is provided, each section heading and its key points
        are injected as explicit numbered instructions so the LLM follows
        the structure strictly.
        
        Args:
            topic: Topic to write about
            content_type: Type of content
            style: Writing style
            length: Desired length
            channel: Publishing channel
            additional_context: Additional context
            outline: Structured outline from Draft agent (optional)
            
        Returns:
            str: Formatted prompt for LLM
        """
        # Get channel-specific length guidelines
        channel_guides = CHANNEL_LENGTH_GUIDES.get(channel, CHANNEL_LENGTH_GUIDES['blog'])
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
        
        # ── Outline-aware structure injection ──────────────────
        if outline and outline.get('sections'):
            prompt += "IMPORTANT: You MUST follow this exact structure.\n"
            prompt += "Write one section for each heading below, using the heading as a subheading in the article.\n\n"
            for i, section in enumerate(outline['sections'], 1):
                heading = section.get('heading', f'Section {i}')
                key_points = section.get('key_points', [])
                prompt += f"Section {i}: {heading}\n"
                if key_points:
                    prompt += f"  Cover these points: {'; '.join(key_points)}\n"
            prompt += "\n"
        
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

    def _check_compliance(
        self,
        content: str,
        outline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check if the generated content covers all outline sections.
        
        Performs case-insensitive matching of outline section headings
        against the article content.
        
        Args:
            content: The generated article content
            outline: The outline used to guide writing
            
        Returns:
            dict with: score (float 0-1), covered (list), missing (list)
        """
        sections = outline.get('sections', [])
        if not sections:
            return {'score': 1.0, 'covered': [], 'missing': []}
        
        content_lower = content.lower()
        covered = []
        missing = []
        
        for section in sections:
            heading = section.get('heading', '')
            if not heading:
                continue
            # Check if heading appears in content (case-insensitive)
            if heading.lower() in content_lower:
                covered.append(heading)
            else:
                # Also check partial matches (first significant word)
                words = [w for w in heading.split() if len(w) > 3]
                if any(w.lower() in content_lower for w in words):
                    covered.append(heading)
                else:
                    missing.append(heading)
        
        total = len(covered) + len(missing)
        score = len(covered) / total if total > 0 else 1.0
        
        return {
            'score': score,
            'covered': covered,
            'missing': missing
        }
    
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
