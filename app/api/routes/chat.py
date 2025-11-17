"""API routes for chat history management"""
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from app.services.chat_service import ChatHistoryService
from app.schemas.chat import (
    ChatMessageCreate, ChatMessageResponse,
    ChatSessionCreate, ChatSessionResponse,
    ChatHistoryResponse, ChatUploadResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize chat service
chat_service = ChatHistoryService()


@router.post("/session", response_model=ChatSessionResponse)
async def create_chat_session(username: str):
    """
    Create a new chat session for a user
    
    Args:
        username: Username
    
    Returns:
        New chat session details
    """
    try:
        session_id = chat_service.create_session(username)
        return ChatSessionResponse(
            id=session_id,
            username=username,
            created_at=None,  # Would come from database
            updated_at=None,  # Would come from database
            message_count=0
        )
    except Exception as e:
        logger.error(f"Error creating chat session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating chat session: {str(e)}"
        )


@router.get("/sessions/{username}", response_model=list[ChatSessionResponse])
async def get_user_sessions(username: str):
    """
    Get all chat sessions for a user
    
    Args:
        username: Username
    
    Returns:
        List of chat sessions
    """
    try:
        session_ids = chat_service.get_user_sessions(username)
        sessions = []
        
        for session_id in session_ids:
            messages = chat_service.get_session_messages(username, session_id)
            sessions.append(ChatSessionResponse(
                id=session_id,
                username=username,
                created_at=None,  # Would come from database
                updated_at=None,  # Would come from database
                message_count=len(messages)
            ))
        
        return sessions
    except Exception as e:
        logger.error(f"Error retrieving user sessions: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving sessions: {str(e)}"
        )


@router.post("/message", response_model=ChatUploadResponse)
async def save_chat_message(
    username: str = Query(..., description="Username"),
    session_id: str = Query(..., description="Chat session ID"),
    content: str = Form(..., description="Message content"),
    message_type: str = Form(default="text", description="Message type: text or image")
):
    """
    Save a chat message to history
    
    Args:
        username: Username
        session_id: Chat session ID
        content: Message content (text or file path for images)
        message_type: "text" or "image"
    
    Returns:
        Message metadata
    """
    try:
        result = chat_service.save_chat_message(
            username, session_id, content, message_type
        )
        return ChatUploadResponse(
            message_id=result["message_id"],
            username=result["username"],
            file_path=result["file_path"],
            timestamp=result["timestamp"],
            message_type=result["type"]
        )
    except Exception as e:
        logger.error(f"Error saving chat message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving message: {str(e)}"
        )


@router.post("/upload/{username}/{session_id}", response_model=ChatUploadResponse)
async def upload_chat_image(
    username: str,
    session_id: str,
    file: UploadFile = File(...)
):
    """
    Upload an image for a chat session
    
    File path format: {username}/{session_id}/images-{seq#}.{jpg,png}
    
    Args:
        username: Username
        session_id: Chat session ID
        file: Image file to upload
    
    Returns:
        Upload metadata
    """
    try:
        # Validate file type
        allowed_types = {"image/jpeg", "image/png", "image/jpg"}
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {allowed_types}"
            )
        
        # Read file content
        content = await file.read()
        
        # Save file using chat service
        result = chat_service.save_chat_message(
            username, session_id, content, "image"
        )
        
        return ChatUploadResponse(
            message_id=result["message_id"],
            username=result["username"],
            file_path=result["file_path"],
            timestamp=result["timestamp"],
            message_type=result["type"]
        )
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading image: {str(e)}"
        )


@router.get("/history/{username}/{session_id}")
async def get_chat_history(username: str, session_id: str):
    """
    Get complete chat history for a session
    
    Args:
        username: Username
        session_id: Chat session ID
    
    Returns:
        Chat history with all messages
    """
    try:
        messages = chat_service.get_session_messages(username, session_id)
        
        return ChatHistoryResponse(
            session=ChatSessionResponse(
                id=session_id,
                username=username,
                created_at=None,
                updated_at=None,
                message_count=len(messages)
            ),
            messages=messages
        )
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )


@router.delete("/session/{username}/{session_id}")
async def delete_chat_session(username: str, session_id: str):
    """
    Delete a chat session and all its messages
    
    Args:
        username: Username
        session_id: Session ID to delete
    
    Returns:
        Deletion confirmation
    """
    try:
        chat_service.delete_session(username, session_id)
        return {"status": "success", "message": f"Session {session_id} deleted"}
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting session: {str(e)}"
        )


@router.get("/file/{username}/{session_id}/{filename}")
async def get_chat_file(username: str, session_id: str, filename: str):
    """
    Download a file from chat history
    
    Args:
        username: Username
        session_id: Chat session ID
        filename: Filename to download
    
    Returns:
        File response
    """
    try:
        from pathlib import Path
        from app.core.config import settings
        
        file_path = Path(settings.CHAT_HISTORY_PATH) / username / session_id / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(path=file_path, filename=filename)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving file: {str(e)}"
        )
