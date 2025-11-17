"""Database connection and engine setup"""
import logging
from typing import Optional
from sqlalchemy import create_engine, event, text
from sqlalchemy.pool import Pool
from sshtunnel import SSHTunnelForwarder
from app.core.config import settings

logger = logging.getLogger(__name__)

# Global variables for database connection and SSH tunnel
_db_engine = None
_ssh_tunnel: Optional[SSHTunnelForwarder] = None


def setup_db_ssh_tunnel() -> None:
    """Establish SSH tunnel if SSH credentials are provided"""
    global _ssh_tunnel
    
    if settings.SSHHOST and settings.SSHUSR and settings.SSHPWD:
        try:
            if _ssh_tunnel is not None:
                _ssh_tunnel.close()
            
            logger.info(f"Setting up SSH tunnel to {settings.SSHHOST}")
            _ssh_tunnel = SSHTunnelForwarder(
                settings.SSHHOST,
                ssh_username=settings.SSHUSR,
                ssh_password=settings.SSHPWD,
                remote_bind_address=(settings.DBHOST, settings.DBPORT)
            )
            _ssh_tunnel.start()
            logger.info(f"SSH tunnel established on local port {_ssh_tunnel.local_bind_port}")
        except Exception as e:
            logger.error(f"Failed to setup SSH tunnel: {str(e)}")
            raise


def get_database_url() -> str:
    """Generate database URL based on SSH tunnel or direct connection"""
    global _ssh_tunnel
    
    host = settings.DBHOST
    port = settings.DBPORT
    
    # If SSH tunnel is active, use local connection
    if _ssh_tunnel is not None:
        host = "127.0.0.1"
        port = _ssh_tunnel.local_bind_port
    
    db_url = (
        f"mysql+pymysql://{settings.DBUSER}:{settings.DBPWD}@"
        f"{host}:{port}/{settings.DBMKTDATA}"
    )
    return db_url


def get_db_engine():
    """Get or create SQLAlchemy database engine"""
    global _db_engine
    
    if _db_engine is None:
        db_url = get_database_url()
        logger.info(f"Creating database engine for {settings.DBMKTDATA}")
        logger.debug(f"Database URL: {db_url}")
        
        _db_engine = create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_recycle=3600,
            echo=settings.DEBUG
        )
        
        # Test the connection
        try:
            with _db_engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
                logger.info("Database connection successful")
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            _db_engine = None
            raise
    
    return _db_engine


def close_db_connection() -> None:
    """Close database engine and SSH tunnel"""
    global _db_engine, _ssh_tunnel
    
    if _db_engine is not None:
        _db_engine.dispose()
        _db_engine = None
        logger.info("Database connection closed")
    
    if _ssh_tunnel is not None:
        _ssh_tunnel.close()
        _ssh_tunnel = None
        logger.info("SSH tunnel closed")
