"""
FastAPI Main Application for Tea Stall Bench

REST API exposing Writer and Publisher agents.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TeaStallBench.API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI app.
    """
    logger.info("Starting Tea Stall Bench API...")
    logger.info("Agents will be initialized per-request via dependency injection")
    
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


# Import and include routes
from backend.api.v1 import routes

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
