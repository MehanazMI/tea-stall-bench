"""
Tests for WhatsApp Client
"""

import pytest
from backend.utils.whatsapp_client import WhatsAppClient


class TestPhoneValidation:
    """Test suite for phone number validation."""
    
    def test_validate_with_plus(self):
        """Test validation of phone with + prefix."""
        client = WhatsAppClient()
        result = client.validate_phone_number("+12345678900")
        assert result == "+12345678900"
    
    def test_validate_without_plus(self):
        """Test validation adds + prefix."""
        client = WhatsAppClient()
        result = client.validate_phone_number("12345678900")
        assert result == "+12345678900"
    
    def test_validate_with_spaces(self):
        """Test validation removes spaces."""
        client = WhatsAppClient()
        result = client.validate_phone_number("+1 234 567 8900")
        assert result == "+12345678900"
    
    def test_validate_with_dashes(self):
        """Test validation removes dashes."""
        client = WhatsAppClient()
        result = client.validate_phone_number("+1-234-567-8900")
        assert result == "+12345678900"
    
    def test_validate_with_parentheses(self):
        """Test validation removes parentheses."""
        client = WhatsAppClient()
        result = client.validate_phone_number("+1(234)567-8900")
        assert result == "+12345678900"
    
    def test_validate_empty_raises_error(self):
        """Test that empty phone raises error."""
        client = WhatsAppClient()
        with pytest.raises(ValueError, match="Phone number cannot be empty"):
            client.validate_phone_number("")
    
    def test_validate_too_short_raises_error(self):
        """Test that phone without country code raises error."""
        client = WhatsAppClient()
        with pytest.raises(ValueError, match="must include country code"):
            client.validate_phone_number("2345678900")  # 10 digits, no country code
    
    def test_validate_too_long_raises_error(self):
        """Test that too long phone raises error."""
        client = WhatsAppClient()
        with pytest.raises(ValueError, match="Phone number too long"):
            client.validate_phone_number("+12345678901234567890")


class TestContentFormatting:
    """Test suite for content formatting."""
    
    def test_format_basic_content(self):
        """Test formatting basic content."""
        client = WhatsAppClient()
        result = client.format_content("Hello World")
        assert result == "Hello World"
    
    def test_format_strips_whitespace(self):
        """Test formatting strips leading/trailing whitespace."""
        client = WhatsAppClient()
        result = client.format_content("  Hello World  \n\n")
        assert result == "Hello World"
    
    def test_format_reduces_newlines(self):
        """Test formatting reduces excessive newlines."""
        client = WhatsAppClient()
        result = client.format_content("Hello\n\n\n\n\nWorld")
        assert result == "Hello\n\nWorld"
    
    def test_format_preserves_double_newlines(self):
        """Test formatting preserves double newlines."""
        client = WhatsAppClient()
        result = client.format_content("Hello\n\nWorld")
        assert result == "Hello\n\nWorld"
    
    def test_format_too_long_raises_error(self):
        """Test that content exceeding max length raises error."""
        client = WhatsAppClient()
        long_content = "A" * 5000
        with pytest.raises(ValueError, match="Content too long"):
            client.format_content(long_content, max_length=4000)
    
    def test_format_custom_max_length(self):
        """Test formatting with custom max length."""
        client = WhatsAppClient()
        content = "A" * 100
        result = client.format_content(content, max_length=150)
        assert len(result) == 100


class TestWhatsAppClientInit:
    """Test suite for client initialization."""
    
    def test_client_initializes(self):
        """Test that client initializes without error."""
        client = WhatsAppClient()
        assert client is not None
        assert client.logger is not None
