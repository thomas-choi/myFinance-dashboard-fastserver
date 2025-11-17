"""Tests for chat history API endpoints"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_chat_session():
    """Test creating a new chat session"""
    response = client.post("/api/chat/session?username=testuser")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "testuser"
    assert data["message_count"] == 0


def test_get_user_sessions():
    """Test retrieving user sessions"""
    # Create a session first
    client.post("/api/chat/session?username=testuser2")
    
    # Get sessions
    response = client.get("/api/chat/sessions/testuser2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
