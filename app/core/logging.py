"""Logging configuration for the application"""
import logging
import sys
from app.core.config import settings

# Map string log level to logging constants
LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# Get log level from settings, default to INFO if invalid
log_level = LOG_LEVEL_MAP.get(settings.LOG_LEVEL.upper(), logging.INFO)

# Configure logging
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)

logger = logging.getLogger(__name__)
