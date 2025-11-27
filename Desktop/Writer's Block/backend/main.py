import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from config import get_settings
from database import init_db
from routes import songs, ai, audio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title="Writer's Block - Songwriting Studio API",
    description="Complete API for songwriting assistance with AI and music theory tools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    logger.info("Database initialized")
    logger.info(f"CORS origins: {settings.CORS_ORIGINS}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")

# Include routers
app.include_router(songs.router)
app.include_router(ai.router)
app.include_router(audio.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Writer's Block - Songwriting Studio API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "OK"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "debug_mode": settings.DEBUG,
        "ai_features_enabled": settings.ENABLE_AI_FEATURES
    }

# Static files (optional - for serving uploads)
uploads_dir = Path(settings.AUDIO_UPLOAD_DIR)
if uploads_dir.exists():
    app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
