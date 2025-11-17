"""Schemas for chat history"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ChatMessageBase(BaseModel):
    """Base schema for chat message"""
    content: str
    message_type: str  # "text" or "image"


class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a new chat message"""
    pass


class ChatMessageResponse(ChatMessageBase):
    """Response schema for chat message"""
    id: str
    username: str
    chat_session_id: str
    timestamp: datetime
    file_path: Optional[str] = None
    
    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    """Base schema for chat session"""
    username: str


class ChatSessionCreate(ChatSessionBase):
    """Schema for creating a new chat session"""
    pass


class ChatSessionResponse(ChatSessionBase):
    """Response schema for chat session"""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    message_count: int = 0
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Response schema for chat history with messages"""
    session: ChatSessionResponse
    messages: List[ChatMessageResponse]


class ChatUploadResponse(BaseModel):
    """Response schema for file upload"""
    message_id: str
    username: str
    file_path: str
    timestamp: datetime
    message_type: str
