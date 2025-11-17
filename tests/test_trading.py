"""Tests for trading API endpoints"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Finance Dashboard API"


# Note: The following tests require database connection
# They are commented out for unit testing without database

# @pytest.mark.asyncio
# async def test_get_etf_options():
#     """Test ETF options endpoint"""
#     response = client.get("/api/trading/etf-options")
#     assert response.status_code == 200
#     assert "data" in response.json()
#     assert "count" in response.json()
#     assert response.json()["type"] == "ETF"


# @pytest.mark.asyncio
# async def test_get_stock_options():
#     """Test stock options endpoint"""
#     response = client.get("/api/trading/stock-options")
#     assert response.status_code == 200
#     assert "data" in response.json()
#     assert "count" in response.json()
#     assert response.json()["type"] == "STK"
