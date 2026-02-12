"""
Publisher Agent (Relay) for Tea Stall Bench

This agent publishes generated content to WhatsApp.
Handles formatting, validation, and delivery tracking.
"""

from typing import Dict, Any, Optional
from backend.agents.base_agent import BaseAgent
from backend.utils.whatsapp_client import WhatsAppClient


class PublisherAgent(BaseAgent):
    """
    Publisher Agent (Relay) - Publishes content to WhatsApp.
    
    Takes generated content and sends it to specified WhatsApp numbers.
    Handles phone validation, content formatting, and delivery tracking.
    
    Example:
        >>> llm_client = LLMClient()
        >>> publisher = PublisherAgent(llm_client)
        >>> result = await publisher.execute({
        ...     "phone_number": "+1234567890",
        ...     "content": "Amazing Python tip!",
        ...     "title": "Python Tips"
        ... })
        >>> print(result['status'])
        'success'
    """
    
    def __init__(self, llm_client=None):
        """
        Initialize Publisher Agent.
        
        Args:
            llm_client: LLM client (not used for publishing, but required by BaseAgent)
        """
        super().__init__("Publisher", llm_client)
        self.whatsapp_client = WhatsAppClient()
        self.logger.info("Publisher Agent initialized")
    
    async def _execute_internal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute publishing to WhatsApp.
        
        Args:
            input_data (Dict[str, Any]): Input containing:
                - phone_number (str): WhatsApp number with country code (required)
                - content (str): Message content to send (required)
                - title (str): Optional title to prepend
                - auto_send (bool): If True, send automatically; if False, open for manual review (default: True)
        
        Returns:
            Dict[str, Any]: Result containing:
                - status: 'success' or 'error'
                - phone_number: Formatted phone number
                - message_length: Length of sent message
                - sent_at: Timestamp of sending
                
        Raises:
            ValueError: If phone_number or content is missing/invalid
        """
        # Validate input
        self._validate_input(input_data)
        
        # Extract parameters
        phone_number = input_data['phone_number']
        content = input_data['content']
        title = input_data.get('title', '')
        auto_send = input_data.get('auto_send', True)  # Default: automatic
        
        # Format message
        message = self._format_message(content, title)
        
        self.logger.info(f"Publishing to WhatsApp: {phone_number}")
        
        try:
            # Send message
            if auto_send:
                result = self.whatsapp_client.send_message(phone_number, message)
                delivery = 'automatic'
            else:
                result = self.whatsapp_client.send_with_review(phone_number, message)
                delivery = 'manual_review'
            
            return {
                'status': 'success',
                'phone_number': result['phone_number'],
                'message_length': result.get('message_length', len(message)),
                'sent_at': result.get('sent_at', 'pending'),
                'delivery_method': delivery
            }
            
        except Exception as e:
            self.logger.error(f"Publishing failed: {str(e)}")
            raise
    
    def _validate_input(self, input_data: Dict[str, Any]) -> None:
        """
        Validate input parameters.
        
        Args:
            input_data: Input dictionary to validate
            
        Raises:
            ValueError: If required parameters are missing or invalid
        """
        # Check phone_number
        if 'phone_number' not in input_data:
            raise ValueError("Phone number is required")
        
        phone = input_data['phone_number']
        if not phone or not isinstance(phone, str):
            raise ValueError("Phone number must be a non-empty string")
        
        # Check content
        if 'content' not in input_data:
            raise ValueError("Content is required")
        
        content = input_data['content']
        if not content or not isinstance(content, str):
            raise ValueError("Content must be a non-empty string")
        
        # Validate title if provided
        if 'title' in input_data:
            title = input_data['title']
            if title and not isinstance(title, str):
                raise ValueError("Title must be a string")
    
    def _format_message(self, content: str, title: str = '') -> str:
        """
        Format message for WhatsApp.
        
        Combines title and content with proper formatting.
        
        Args:
            content: Main message content
            title: Optional title
            
        Returns:
            str: Formatted message
        """
        if title:
            # Add title with formatting
            message = f"*{title}*\n\n{content}"
        else:
            message = content
        
        # Strip excessive whitespace
        message = message.strip()
        
        return message
