"""
Pydantic models for API request and response validation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Request Models

class GenerateRequest(BaseModel):
    """Request model for content generation."""
    topic: str = Field(..., min_length=3, description="Topic to generate content about")
    style: Optional[str] = Field("storytelling", description="Writing style")
    max_length: Optional[int] = Field(None, description="Maximum content length")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Python tips for beginners",
                "style": "storytelling",
                "max_length": 800
            }
        }


class PublishRequest(BaseModel):
    """Request model for publishing content."""
    phone_number: str = Field(..., description="Phone number with country code")
    content: str = Field(..., min_length=1, description="Content to publish")
    title: Optional[str] = Field(None, description="Optional title")
    auto_send: bool = Field(True, description="Auto send (True) or manual review (False)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "phone_number": "+12345678900",
                "content": "Great Python tip!",
                "title": "Tip of the Day",
                "auto_send": True
            }
        }


class GenerateAndPublishRequest(BaseModel):
    """Request model for full pipeline (generate + publish)."""
    topic: str = Field(..., min_length=3, description="Topic to generate content about")
    phone_number: str = Field(..., description="Phone number with country code")
    style: Optional[str] = Field("storytelling", description="Writing style")
    max_length: Optional[int] = Field(None, description="Maximum content length")
    title: Optional[str] = Field(None, description="Optional title")
    auto_send: bool = Field(True, description="Auto send (True) or manual review (False)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Meditation benefits",
                "phone_number": "+12345678900",
                "style": "storytelling",
                "auto_send": True
            }
        }


# Response Models

class GenerateResponse(BaseModel):
    """Response model for content generation."""
    status: str
    content: str
    topic: str
    style: str
    word_count: int


class PublishResponse(BaseModel):
    """Response model for publishing."""
    status: str
    phone_number: str
    delivery_method: str
    message_length: int
    sent_at: Optional[str] = None


class GenerateAndPublishResponse(BaseModel):
    """Response model for full pipeline."""
    status: str
    topic: str
    content: str
    word_count: int
    phone_number: str
    delivery_method: str
    sent_at: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    service: str
    version: str


class StylesResponse(BaseModel):
    """Response model for available styles."""
    styles: List[Dict[str, str]]


class ChannelsResponse(BaseModel):
    """Response model for supported channels."""
    channels: List[Dict[str, Any]]
