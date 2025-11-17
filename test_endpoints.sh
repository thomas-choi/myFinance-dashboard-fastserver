#!/bin/bash

# FastAPI Finance Dashboard - CURL Test Examples
# 
# This script provides curl examples for testing all API endpoints
# Usage: bash test_endpoints.sh
#
# Or copy/paste individual curl commands below

API="http://localhost:8000"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  FastAPI Finance Dashboard - API Test Examples                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# =========================================================================
# HEALTH CHECK
# =========================================================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "HEALTH CHECK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Check if server is running:"
echo "  curl -X GET http://localhost:8000/health"
curl -s -X GET $API/health | jq . 2>/dev/null || echo "Server not responding"
echo ""

# =========================================================================
# TRADING ENDPOINTS
# =========================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TRADING ENDPOINTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Get ETF Options
echo "1. GET /api/trading/etf-options"
echo "   Get real-time ETF options data"
echo "   Command:"
echo "     curl -X GET $API/api/trading/etf-options | jq ."
echo ""
read -p "   Run this test? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -s -X GET $API/api/trading/etf-options | jq . 2>/dev/null || echo "Error"
fi
echo ""

# 2. Get Stock Options
echo "2. GET /api/trading/stock-options"
echo "   Get real-time US stock options data"
echo "   Command:"
echo "     curl -X GET $API/api/trading/stock-options | jq ."
echo ""
read -p "   Run this test? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -s -X GET $API/api/trading/stock-options | jq . 2>/dev/null || echo "Error"
fi
echo ""

# 3. Get Max Date
echo "3. GET /api/trading/max-date/{table_name}"
echo "   Get maximum date from a table"
echo "   Command:"
echo "     curl -X GET \"$API/api/trading/max-date/histdailyprice7\" | jq ."
echo ""
read -p "   Run this test? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -s -X GET "$API/api/trading/max-date/histdailyprice7" | jq . 2>/dev/null || echo "Error"
fi
echo ""

# 4. Custom Query
echo "4. POST /api/trading/custom-query"
echo "   Execute a custom SQL query"
echo "   Command:"
echo "     curl -X POST \"$API/api/trading/custom-query?query=SELECT%201%20as%20test\" | jq ."
echo ""
read -p "   Run this test? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -s -X POST "$API/api/trading/custom-query?query=SELECT%201%20as%20test" | jq . 2>/dev/null || echo "Error"
fi
echo ""

# =========================================================================
# CHAT ENDPOINTS
# =========================================================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "CHAT ENDPOINTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

USERNAME="testuser"
echo "Using test username: $USERNAME"
echo ""

# 5. Create Chat Session
echo "5. POST /api/chat/session"
echo "   Create a new chat session"
echo "   Command:"
echo "     curl -X POST \"$API/api/chat/session?username=$USERNAME\" | jq ."
echo ""
read -p "   Run this test? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SESSION_RESPONSE=$(curl -s -X POST "$API/api/chat/session?username=$USERNAME")
    echo "$SESSION_RESPONSE" | jq . 2>/dev/null || echo "Error"
    SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.id' 2>/dev/null)
    echo "Session ID: $SESSION_ID"
else
    SESSION_ID=""
fi
echo ""

# 6. Get User Sessions
echo "6. GET /api/chat/sessions/{username}"
echo "   Get all sessions for a user"
echo "   Command:"
echo "     curl -X GET \"$API/api/chat/sessions/$USERNAME\" | jq ."
echo ""
read -p "   Run this test? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    curl -s -X GET "$API/api/chat/sessions/$USERNAME" | jq . 2>/dev/null || echo "Error"
fi
echo ""

# 7. Save Chat Message
if [ -n "$SESSION_ID" ]; then
    echo "7. POST /api/chat/message"
    echo "   Save a text message"
    echo "   Command:"
    echo "     curl -X POST \"$API/api/chat/message\" \\"
    echo "       -F \"username=$USERNAME\" \\"
    echo "       -F \"session_id=$SESSION_ID\" \\"
    echo "       -F \"content=Hello, this is a test message!\" \\"
    echo "       -F \"message_type=text\""
    echo ""
    read -p "   Run this test? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -s -X POST "$API/api/chat/message" \
            -F "username=$USERNAME" \
            -F "session_id=$SESSION_ID" \
            -F "content=Hello, this is a test message!" \
            -F "message_type=text" | jq . 2>/dev/null || echo "Error"
    fi
    echo ""

    # 8. Get Chat History
    echo "8. GET /api/chat/history/{username}/{session_id}"
    echo "   Get chat history for a session"
    echo "   Command:"
    echo "     curl -X GET \"$API/api/chat/history/$USERNAME/$SESSION_ID\" | jq ."
    echo ""
    read -p "   Run this test? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -s -X GET "$API/api/chat/history/$USERNAME/$SESSION_ID" | jq . 2>/dev/null || echo "Error"
    fi
    echo ""

    # 9. Upload Image (requires test image)
    echo "9. POST /api/chat/upload/{username}/{session_id}"
    echo "   Upload an image to a chat session"
    echo "   Command:"
    echo "     curl -X POST \"$API/api/chat/upload/$USERNAME/$SESSION_ID\" \\"
    echo "       -F \"file=@test_image.jpg\""
    echo ""
    echo "   Note: You need to have a test image file (test_image.jpg) in current directory"
    read -p "   Run this test? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -f "test_image.jpg" ]; then
            curl -s -X POST "$API/api/chat/upload/$USERNAME/$SESSION_ID" \
                -F "file=@test_image.jpg" | jq . 2>/dev/null || echo "Error"
        else
            echo "No test_image.jpg found. Skipping..."
        fi
    fi
    echo ""

    # 10. Delete Chat Session
    echo "10. DELETE /api/chat/session/{username}/{session_id}"
    echo "    Delete a chat session"
    echo "    Command:"
    echo "      curl -X DELETE \"$API/api/chat/session/$USERNAME/$SESSION_ID\""
    echo ""
    read -p "    Run this test? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        curl -s -X DELETE "$API/api/chat/session/$USERNAME/$SESSION_ID" | jq . 2>/dev/null || echo "Error"
    fi
    echo ""
else
    echo "Skipping remaining chat tests (no session ID available)"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  Testing Complete                                               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
