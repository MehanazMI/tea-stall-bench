"""
Pydantic models for API request and response validation.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# Request Models

class GenerateRequest(BaseModel):
    """Request model for content generation."""
    topic: str = Field(..., min_length=3, description="Topic to generate content about")
    style: Optional[str] = Field("storytelling", description="Writing style")
    max_length: Optional[int] = Field(None, ge=50, le=5000, description="Maximum content length in words")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "How AI agents collaborate like a tea stall crew",
                "style": "storytelling",
                "max_length": 800
            }
        }
    )


class PublishRequest(BaseModel):
    """Request model for publishing content."""
    phone_number: str = Field(..., min_length=11, description="Phone number with country code (e.g. +12345678900)")
    content: str = Field(..., min_length=1, description="Content to publish")
    title: Optional[str] = Field(None, description="Optional title")
    auto_send: bool = Field(True, description="Auto send (True) or manual review (False)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone_number": "+12345678900",
                "content": "Great Python tip!",
                "title": "Tip of the Day",
                "auto_send": True
            }
        }
    )


class GenerateAndPublishRequest(BaseModel):
    """Request model for full pipeline (generate + publish)."""
    topic: str = Field(..., min_length=3, description="Topic to generate content about")
    phone_number: str = Field(..., min_length=11, description="Phone number with country code (e.g. +12345678900)")
    style: Optional[str] = Field("storytelling", description="Writing style")
    max_length: Optional[int] = Field(None, ge=50, le=5000, description="Maximum content length in words")
    title: Optional[str] = Field(None, description="Optional title")
    auto_send: bool = Field(True, description="Auto send (True) or manual review (False)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "The art of multi-agent orchestration",
                "phone_number": "+12345678900",
                "style": "storytelling",
                "auto_send": True
            }
        }
    )


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


class ErrorResponse(BaseModel):
    """Standard error response model."""
    status: str = "error"
    detail: str
    error_type: Optional[str] = None


class PipelineRequest(BaseModel):
    """Request model for full Sprint 2 pipeline (Research → Outline → Write)."""
    topic: str = Field(..., min_length=3, description="Topic to create content about")
    content_type: Optional[str] = Field("blog", description="Content type (blog, post, tutorial)")
    style: Optional[str] = Field("professional", description="Writing style")
    length: Optional[str] = Field("medium", description="Desired length (short, medium, long)")
    channel: Optional[str] = Field("blog", description="Publishing channel")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "The future of multi-agent AI systems",
                "content_type": "blog",
                "style": "professional",
                "length": "medium",
                "channel": "blog"
            }
        }
    )


class PipelineResponse(BaseModel):
    """Response model for pipeline execution."""
    status: str
    trace_id: str
    topic: str
    research_data: Optional[str] = None
    research_sources: Optional[List[str]] = None
    outline: Optional[Dict[str, Any]] = None
    article_title: Optional[str] = None
    article_content: Optional[str] = None
    word_count: Optional[int] = None
    errors: List[str] = []
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
