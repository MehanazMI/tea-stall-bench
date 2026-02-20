"""
FastAPI Main Application for Tea Stall Bench

REST API exposing Writer and Publisher agents.
Serves the frontend dashboard at root.
"""

import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("TeaStallBench.API")

# Frontend directory
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for FastAPI app.
    """
    logger.info("Starting Tea Stall Bench API...")
    logger.info("Agents will be initialized per-request via dependency injection")
    logger.info(f"Frontend directory: {FRONTEND_DIR}")
    
    yield
    
    logger.info("Shutting down Tea Stall Bench API...")


# Create FastAPI app
app = FastAPI(
    title="Tea Stall Bench API",
    description="REST API for automated content generation and WhatsApp publishing",
    version="2.0.0",
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

# Mount static files (CSS, JS)
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the frontend dashboard."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>Tea Stall Bench API</h1><p>Frontend not found. Visit <a href='/docs'>/docs</a> for API.</p>")


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
