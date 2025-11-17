"""Service for chat history management"""
import logging
import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class ChatHistoryService:
    """Service for managing chat history and file storage"""
    
    def __init__(self):
        """Initialize chat history service"""
        self.base_path = Path(settings.CHAT_HISTORY_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Chat history base path: {self.base_path}")
    
    def _get_session_dir(self, username: str, session_id: str) -> Path:
        """
        Get or create session directory
        Format: {username}/{session_id}/
        """
        session_dir = self.base_path / username / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir
    
    def save_chat_message(self, username: str, session_id: str, 
                         message: str, message_type: str = "text") -> Dict:
        """
        Save a chat message to disk
        
        Args:
            username: Username
            session_id: Chat session ID
            message: Message content
            message_type: "text" or "image"
        
        Returns:
            Dictionary with message metadata
        """
        try:
            session_dir = self._get_session_dir(username, session_id)
            timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            message_id = str(uuid.uuid4())
            
            # Save message content
            if message_type == "text":
                filename = f"message_{message_id}.txt"
                filepath = session_dir / filename
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(message)
            elif message_type == "image":
                # For images, message should contain the file path
                filename = f"image_{message_id}.jpg"
                filepath = session_dir / filename
                # Copy or move image file here if needed
            else:
                raise ValueError(f"Unsupported message type: {message_type}")
            
            logger.info(f"Saved {message_type} message for {username}/{session_id}")
            
            return {
                "message_id": message_id,
                "username": username,
                "session_id": session_id,
                "timestamp": timestamp,
                "type": message_type,
                "file_path": str(filepath)
            }
        except Exception as e:
            logger.error(f"Error saving chat message: {str(e)}")
            raise
    
    def get_session_messages(self, username: str, session_id: str) -> List[Dict]:
        """
        Retrieve all messages in a chat session
        
        Args:
            username: Username
            session_id: Chat session ID
        
        Returns:
            List of messages
        """
        try:
            session_dir = self._get_session_dir(username, session_id)
            messages = []
            
            if not session_dir.exists():
                logger.warning(f"Session directory not found: {session_dir}")
                return messages
            
            # Read all message files
            for file in sorted(session_dir.glob("message_*.txt")):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    messages.append({
                        "type": "text",
                        "content": content,
                        "file": file.name
                    })
            
            for file in sorted(session_dir.glob("image_*.jpg")):
                messages.append({
                    "type": "image",
                    "file": file.name,
                    "path": str(file)
                })
            
            logger.info(f"Retrieved {len(messages)} messages from {username}/{session_id}")
            return messages
        except Exception as e:
            logger.error(f"Error retrieving session messages: {str(e)}")
            raise
    
    def get_user_sessions(self, username: str) -> List[str]:
        """
        Get all session IDs for a user
        
        Args:
            username: Username
        
        Returns:
            List of session IDs
        """
        try:
            user_dir = self.base_path / username
            
            if not user_dir.exists():
                logger.info(f"No sessions found for user: {username}")
                return []
            
            sessions = [d.name for d in user_dir.iterdir() if d.is_dir()]
            logger.info(f"Found {len(sessions)} sessions for {username}")
            return sessions
        except Exception as e:
            logger.error(f"Error retrieving user sessions: {str(e)}")
            raise
    
    def create_session(self, username: str) -> str:
        """
        Create a new chat session
        
        Args:
            username: Username
        
        Returns:
            New session ID
        """
        try:
            session_id = str(uuid.uuid4())
            self._get_session_dir(username, session_id)
            
            logger.info(f"Created new session {session_id} for {username}")
            return session_id
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise
    
    def delete_session(self, username: str, session_id: str) -> bool:
        """
        Delete a chat session and all its messages
        
        Args:
            username: Username
            session_id: Session ID to delete
        
        Returns:
            True if successful
        """
        try:
            session_dir = self._get_session_dir(username, session_id)
            
            # Remove all files in the session
            for file in session_dir.iterdir():
                file.unlink()
            
            # Remove the session directory
            session_dir.rmdir()
            
            logger.info(f"Deleted session {session_id} for {username}")
            return True
        except Exception as e:
            logger.error(f"Error deleting session: {str(e)}")
            raise
