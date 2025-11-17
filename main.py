"""FastAPI application entry point"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.db.database import setup_db_ssh_tunnel, close_db_connection
from app.api.routes import trading, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown
    """
    # Startup
    logger.info("Starting Finance Dashboard API Server...")
    try:
        setup_db_ssh_tunnel()
        logger.info("Database connection initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Finance Dashboard API Server...")
    close_db_connection()
    logger.info("Database connection closed")


# Create FastAPI application
app = FastAPI(
    title="Finance Dashboard API",
    description="FastAPI server for trading options monitor and chat history",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(trading.router)
app.include_router(chat.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Finance Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "trading": "/api/trading",
            "chat": "/api/chat"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
