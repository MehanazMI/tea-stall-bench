"""
FastAPI Main Application for Tea Stall Bench

REST API exposing Writer and Publisher agents.
"""

import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.utils.llm_client import LLMClient
from backend.agents.writer_agent import WriterAgent
from backend.agents.publisher_agent import PublisherAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TeaStallBench.API")

# Global instances
llm_client: LLMClient = None
writer_agent: WriterAgent = None
publisher_agent: PublisherAgent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI app.
    Initializes agents on startup, cleans up on shutdown.
    """
    global llm_client, writer_agent, publisher_agent
    
    logger.info("Starting Tea Stall Bench API...")
    
    # Initialize LLM client and agents
    llm_client = LLMClient()
    writer_agent = WriterAgent(llm_client)
    publisher_agent = PublisherAgent(llm_client)
    
    logger.info("All agents initialized successfully")
    
    yield
    
    logger.info("Shutting down Tea Stall Bench API...")


# Create FastAPI app
app = FastAPI(
    title="Tea Stall Bench API",
    description="REST API for automated content generation and WhatsApp publishing",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import routes
from backend.api.v1 import routes

# Include API routes
app.include_router(routes.router, prefix="/api/v1", tags=["v1"])


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Tea Stall Bench API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "error_type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
