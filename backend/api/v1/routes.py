"""
API route handlers for Tea Stall Bench.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from backend.utils.llm_client import LLMClient
from backend.agents.writer_agent import WriterAgent
from backend.agents.publisher_agent import PublisherAgent
from backend.api.v1.models import (
    GenerateRequest,
    GenerateResponse,
    PublishRequest,
    PublishResponse,
    GenerateAndPublishRequest,
    GenerateAndPublishResponse,
    HealthResponse,
    StylesResponse,
    ChannelsResponse
)

logger = logging.getLogger("TeaStallBench.API.Routes")

router = APIRouter()

# Dependency injection for agents
def get_llm_client():
    """Get LLM client instance."""
    return LLMClient()

def get_writer_agent(llm_client: LLMClient = Depends(get_llm_client)):
    """Get Writer agent instance."""
    return WriterAgent(llm_client)

def get_publisher_agent(llm_client: LLMClient = Depends(get_llm_client)):
    """Get Publisher agent instance."""
    return PublisherAgent(llm_client)


@router.post("/generate", response_model=GenerateResponse)
async def generate_content(
    request: GenerateRequest,
    writer: WriterAgent = Depends(get_writer_agent)
):
    """
    Generate content using Writer Agent.
    
    - **topic**: Topic to write about (required)
    - **style**: Writing style (optional, default: storytelling)
    - **max_length**: Maximum content length (optional)
    """
    try:
        logger.info(f"Generating content for topic: {request.topic}")
        
        result = await writer.execute({
            "topic": request.topic,
            "style": request.style or "storytelling",
            "max_length": request.max_length
        })
        
        return GenerateResponse(
            status="success",
            content=result["content"],
            topic=result["topic"],
            style=result["style"],
            word_count=result["word_count"]
        )
        
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@router.post("/publish", response_model=PublishResponse)
async def publish_content(
    request: PublishRequest,
    publisher: PublisherAgent = Depends(get_publisher_agent)
):
    """
    Publish content to WhatsApp.
    
    - **phone_number**: Phone with country code (required)
    - **content**: Content to publish (required)
    - **title**: Optional title
    - **auto_send**: True for automatic, False for manual review
    """
    try:
        logger.info(f"Publishing to {request.phone_number}")
        
        result = await publisher.execute({
            "phone_number": request.phone_number,
            "content": request.content,
            "title": request.title,
            "auto_send": request.auto_send
        })
        
        return PublishResponse(
            status=result["status"],
            phone_number=result["phone_number"],
            delivery_method=result["delivery_method"],
            message_length=result["message_length"],
            sent_at=result.get("sent_at")
        )
        
    except Exception as e:
        logger.error(f"Publishing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Publishing failed: {str(e)}")


@router.post("/generate-and-publish", response_model=GenerateAndPublishResponse)
async def generate_and_publish(
    request: GenerateAndPublishRequest,
    writer: WriterAgent = Depends(get_writer_agent),
    publisher: PublisherAgent = Depends(get_publisher_agent)
):
    """
    Full pipeline: Generate content and publish to WhatsApp.
    
    Combines Writer and Publisher agents for one-step operation.
    """
    try:
        logger.info(f"Pipeline: {request.topic} → {request.phone_number}")
        
        # Step 1: Generate content
        gen_result = await writer.execute({
            "topic": request.topic,
            "style": request.style or "storytelling",
            "max_length": request.max_length
        })
        
        # Step 2: Publish content
        pub_result = await publisher.execute({
            "phone_number": request.phone_number,
            "content": gen_result["content"],
            "title": request.title,
            "auto_send": request.auto_send
        })
        
        return GenerateAndPublishResponse(
            status="success",
            topic=gen_result["topic"],
            content=gen_result["content"],
            word_count=gen_result["word_count"],
            phone_number=pub_result["phone_number"],
            delivery_method=pub_result["delivery_method"],
            sent_at=pub_result.get("sent_at")
        )
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")


@router.get("/styles", response_model=StylesResponse)
async def get_styles():
    """Get available writing styles."""
    styles = [
        {"name": "storytelling", "description": "Engaging narrative style with examples"},
        {"name": "professional", "description": "Formal, business-appropriate tone"},
        {"name": "casual", "description": "Friendly, conversational approach"},
        {"name": "educational", "description": "Clear, instructional format"},
        {"name": "inspirational", "description": "Motivational and uplifting"}
    ]
    return StylesResponse(styles=styles)


@router.get("/channels", response_model=ChannelsResponse)
async def get_channels():
    """Get supported publishing channels."""
    channels = [
        {
            "name": "whatsapp",
            "description": "WhatsApp messaging",
            "requires_phone": True,
            "max_length": 4000
        }
    ]
    return ChannelsResponse(channels=channels)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="Tea Stall Bench API",
        version="1.0.0"
    )
