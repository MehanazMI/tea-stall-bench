"""
WhatsApp Client for Tea Stall Bench

Handles WhatsApp messaging using pywhatkit.
Simple, reliable automation for sending messages.
"""

import pywhatkit as kit
import re
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class WhatsAppClient:
    """
    Client for sending messages to WhatsApp.
    
    Uses pywhatkit for simple, reliable message sending.
    Requires WhatsApp Web to be logged in on the browser.
    """
    
    def __init__(self):
        """Initialize WhatsApp client."""
        self.logger = logging.getLogger("TeaStallBench.WhatsAppClient")
        self.logger.info("WhatsApp Client initialized")
    
    def validate_phone_number(self, phone: str) -> str:
        """
        Validate and format phone number.
        
        Args:
            phone: Phone number (e.g., "+1234567890" or "1234567890")
            
        Returns:
            str: Formatted phone number with country code
            
        Raises:
            ValueError: If phone number is invalid
        
        Examples:
            >>> client = WhatsAppClient()
            >>> client.validate_phone_number("+1234567890")
            '+1234567890'
            >>> client.validate_phone_number("1234567890")
            '+1234567890'
        """
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        # Check if it's empty
        if not digits:
            raise ValueError("Phone number cannot be empty")
        
        # Check minimum length - require country code (11+ digits)
        # Most countries have 10-digit local numbers + 1-4 digit country code
        if len(digits) < 11:
            raise ValueError(
                f"Phone number must include country code. "
                f"Got {len(digits)} digits, need at least 11. "
                f"Example: +12345678900 (US) or +919876543210 (India)"
            )
        
        # Check maximum length (max 15 digits per E.164)
        if len(digits) > 15:
            raise ValueError(f"Phone number too long: {phone}")
        
        # Add + prefix (digits already cleaned)
        formatted = f"+{digits}"
        
        self.logger.debug(f"Validated phone: {phone} -> {formatted}")
        return formatted
    
    def format_content(self, content: str, max_length: int = 4000) -> str:
        """
        Format content for WhatsApp.
        
        WhatsApp supports up to 65k characters, but we limit to 4k for readability.
        Strips excessive whitespace and ensures proper formatting.
        
        Args:
            content: Content to format
            max_length: Maximum length (default: 4000)
            
        Returns:
            str: Formatted content
            
        Raises:
            ValueError: If content is too long
        """
        # Strip leading/trailing whitespace
        formatted = content.strip()
        
        # Check length
        if len(formatted) > max_length:
            raise ValueError(
                f"Content too long ({len(formatted)} chars). "
                f"Maximum: {max_length} chars"
            )
        
        # Replace multiple newlines with max 2
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        
        return formatted
    
    def send_message(
        self,
        phone_number: str,
        message: str,
        wait_time: int = 10
    ) -> Dict[str, Any]:
        """
        Send a message to WhatsApp.
        
        Args:
            phone_number: Phone number with country code
            message: Message to send
            wait_time: Seconds to wait before sending (default: 10)
            
        Returns:
            Dict with status information
            
        Raises:
            ValueError: If phone or message is invalid
            Exception: If sending fails
        """
        # Validate inputs
        formatted_phone = self.validate_phone_number(phone_number)
        formatted_message = self.format_content(message)
        
        self.logger.info(f"Sending WhatsApp message to {formatted_phone}")
        
        try:
            # Calculate send time (now + wait_time)
            now = datetime.now()
            send_time = now + timedelta(seconds=wait_time)
            hour = send_time.hour
            minute = send_time.minute
            
            # Send message using pywhatkit
            # This will open WhatsApp Web and send the message
            kit.sendwhatmsg(
                formatted_phone,
                formatted_message,
                hour,
                minute,
                wait_time=wait_time,
                tab_close=True,
                close_time=3
            )
            
            self.logger.info(f"Message sent successfully to {formatted_phone}")
            
            return {
                "status": "success",
                "phone_number": formatted_phone,
                "message_length": len(formatted_message),
                "sent_at": send_time.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {str(e)}")
            raise Exception(f"WhatsApp send failed: {str(e)}")
    
    def send_instant(
        self,
        phone_number: str,
        message: str
    ) -> Dict[str, Any]:
        """
        Send message instantly (opens WhatsApp Web with message ready).
        
        User must click Send manually. Useful for testing.
        
        Args:
            phone_number: Phone number with country code
            message: Message to send
            
        Returns:
            Dict with status information
        """
        formatted_phone = self.validate_phone_number(phone_number)
        formatted_message = self.format_content(message)
        
        self.logger.info(f"Preparing instant message to {formatted_phone}")
        
        try:
            # Open WhatsApp Web with message
            kit.sendwhatmsg_instantly(
                formatted_phone,
                formatted_message,
                wait_time=10,
                tab_close=False
            )
            
            return {
                "status": "ready",
                "phone_number": formatted_phone,
                "message": "WhatsApp Web opened. Click Send to deliver message."
            }
            
        except Exception as e:
            self.logger.error(f"Failed to prepare message: {str(e)}")
            raise Exception(f"WhatsApp preparation failed: {str(e)}")
