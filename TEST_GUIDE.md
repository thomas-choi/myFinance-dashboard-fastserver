# API Testing Guide - FastAPI Finance Dashboard

## Overview

This guide provides detailed instructions for testing all 11 API endpoints with example requests and expected responses.

## Quick Start

### Option 1: Interactive Python Test Client (Recommended)
```bash
# Install requests if not already installed
pip install requests

# Run the interactive test client
python test_client.py
```

This provides:
- Interactive menu system
- Color-coded output
- Session management
- Automatic error handling

### Option 2: Bash Script with CURL
```bash
# Make script executable
chmod +x test_endpoints.sh

# Run the test script
bash test_endpoints.sh
```

This provides:
- Command examples you can copy/paste
- Interactive prompts for each test
- No Python dependencies

### Option 3: Manual CURL Commands
Use the curl commands below directly in your terminal.

---

## Testing Each Endpoint

### 0. Health Check

**Purpose:** Verify the server is running and responsive.

```bash
curl -X GET http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

**Status Code:** 200

---

## Trading Endpoints

### 1. Get ETF Options

**Endpoint:** `GET /api/trading/etf-options`

**Purpose:** Retrieve real-time ETF options data from the database.

**Command:**
```bash
curl -X GET http://localhost:8000/api/trading/etf-options | jq .
```

**Example Response:**
```json
{
  "data": [
    {
      "symbol": "SPY",
      "expiration": "2025-11-21",
      "pnc": "C",
      "strike": 500.0,
      "entry1": 495.0,
      "target": 510.0,
      "stop": 490.0,
      "trade_status": "ACTIVE",
      "date": "2025-11-13T15:30:00",
      "o_price": 50.25,
      "last_price": 52.75,
      "reward_percent": 3.9
    }
  ],
  "count": 1,
  "type": "ETF"
}
```

**Expected Status:** 200

**Notes:**
- Returns data from `Trading.sp_etf_trades_v2` stored procedure
- `count` indicates number of options returned
- `type` will always be "ETF"

---

### 2. Get Stock Options

**Endpoint:** `GET /api/trading/stock-options`

**Purpose:** Retrieve real-time US stock options data from the database.

**Command:**
```bash
curl -X GET http://localhost:8000/api/trading/stock-options | jq .
```

**Example Response:**
```json
{
  "data": [
    {
      "symbol": "AAPL",
      "expiration": "2025-11-21",
      "pnc": "P",
      "strike": 200.0,
      "entry1": 205.0,
      "target": 190.0,
      "stop": 210.0,
      "trade_status": "ACTIVE",
      "date": "2025-11-13T15:30:00",
      "o_price": 8.50,
      "last_price": 7.25,
      "reward_percent": 14.7
    }
  ],
  "count": 1,
  "type": "STK"
}
```

**Expected Status:** 200

**Notes:**
- Returns data from `Trading.sp_stock_trades_V3` stored procedure
- `pnc` can be "C" (Call) or "P" (Put)
- `type` will always be "STK"

---

### 3. Get Maximum Date from Table

**Endpoint:** `GET /api/trading/max-date/{table_name}`

**Purpose:** Get the maximum date for a specific table or symbol.

**Command:**
```bash
# Without symbol filter
curl -X GET "http://localhost:8000/api/trading/max-date/histdailyprice7" | jq .

# With symbol filter
curl -X GET "http://localhost:8000/api/trading/max-date/histdailyprice7?symbol=AAPL" | jq .
```

**Example Response (without symbol):**
```json
{
  "table": "histdailyprice7",
  "symbol": null,
  "max_date": "2025-11-13"
}
```

**Example Response (with symbol):**
```json
{
  "table": "histdailyprice7",
  "symbol": "AAPL",
  "max_date": "2025-11-13"
}
```

**Expected Status:** 200

**Parameters:**
- `table_name` (required): Name of the table to query
- `symbol` (optional): Filter by specific symbol

---

### 4. Execute Custom SQL Query

**Endpoint:** `POST /api/trading/custom-query`

**Purpose:** Execute a custom SQL query on the database.

⚠️ **Warning:** Only use with trusted input!

**Command:**
```bash
# Simple test query
curl -X POST "http://localhost:8000/api/trading/custom-query?query=SELECT%201%20as%20test" | jq .

# Query a table
curl -X POST "http://localhost:8000/api/trading/custom-query?query=SELECT%20*%20FROM%20OptionChains%20LIMIT%201" | jq .

# URL encoded query
# Query: SELECT COUNT(*) as count FROM OptionChains
curl -X POST "http://localhost:8000/api/trading/custom-query?query=SELECT%20COUNT(*)%20as%20count%20FROM%20OptionChains" | jq .
```

**Example Response:**
```json
{
  "count": 1,
  "data": [
    {
      "test": 1
    }
  ]
}
```

**Expected Status:** 200

**Notes:**
- Query must be URL encoded
- Results returned as array of objects
- `count` indicates number of rows returned

---

## Chat Endpoints

### 5. Create Chat Session

**Endpoint:** `POST /api/chat/session`

**Purpose:** Create a new chat session for a user.

**Command:**
```bash
curl -X POST "http://localhost:8000/api/chat/session?username=john" | jq .
```

**Example Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "username": "john",
  "created_at": null,
  "updated_at": null,
  "message_count": 0
}
```

**Expected Status:** 200

**Parameters:**
- `username` (required): Username for the session

**Notes:**
- Session ID is a UUID
- `message_count` starts at 0
- Save the session ID for subsequent requests

---

### 6. Get User Sessions

**Endpoint:** `GET /api/chat/sessions/{username}`

**Purpose:** List all chat sessions for a user.

**Command:**
```bash
curl -X GET "http://localhost:8000/api/chat/sessions/john" | jq .
```

**Example Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john",
    "created_at": null,
    "updated_at": null,
    "message_count": 3
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "username": "john",
    "created_at": null,
    "updated_at": null,
    "message_count": 1
  }
]
```

**Expected Status:** 200

**Parameters:**
- `username` (required): Username to get sessions for

**Notes:**
- Returns array of sessions
- Each session includes message count
- Empty array if no sessions exist

---

### 7. Save Chat Message

**Endpoint:** `POST /api/chat/message`

**Purpose:** Save a text message to a chat session.

**Command:**
```bash
curl -X POST "http://localhost:8000/api/chat/message" \
  -F "username=john" \
  -F "session_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "content=Hello! How are you today?" \
  -F "message_type=text" | jq .
```

**Example Response:**
```json
{
  "message_id": "f0e64c33-e8be-4f91-a4b5-be4a8e90d0f0",
  "username": "john",
  "file_path": "/path/to/chat_history/john/550e8400.../message_f0e64c33.txt",
  "timestamp": "2025-11-13 15:45:30",
  "message_type": "text"
}
```

**Expected Status:** 200

**Form Data:**
- `username` (required): Username
- `session_id` (required): Session ID
- `content` (required): Message text
- `message_type` (required): "text" or "image"

**Notes:**
- Messages are stored as files on disk
- Timestamp is generated server-side
- Message stored at `chat_history/{username}/{session_id}/`

---

### 8. Upload Chat Image

**Endpoint:** `POST /api/chat/upload/{username}/{session_id}`

**Purpose:** Upload an image file to a chat session.

**Command:**
```bash
curl -X POST "http://localhost:8000/api/chat/upload/john/550e8400-e29b-41d4-a716-446655440000" \
  -F "file=@path/to/image.jpg" | jq .
```

**Example Response:**
```json
{
  "message_id": "a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "username": "john",
  "file_path": "/path/to/chat_history/john/550e8400.../image_a1b2c3d4.jpg",
  "timestamp": "2025-11-13 15:46:00",
  "message_type": "image"
}
```

**Expected Status:** 200

**Parameters:**
- `username` (in URL): Username
- `session_id` (in URL): Session ID

**Form Data:**
- `file` (required): Image file (JPEG or PNG)

**Notes:**
- Supported formats: JPEG, PNG
- File stored with unique message ID
- Original filename not preserved

---

### 9. Get Chat History

**Endpoint:** `GET /api/chat/history/{username}/{session_id}`

**Purpose:** Retrieve all messages in a chat session.

**Command:**
```bash
curl -X GET "http://localhost:8000/api/chat/history/john/550e8400-e29b-41d4-a716-446655440000" | jq .
```

**Example Response:**
```json
{
  "session": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "john",
    "created_at": null,
    "updated_at": null,
    "message_count": 2
  },
  "messages": [
    {
      "type": "text",
      "content": "Hello! How are you today?",
      "file": "message_f0e64c33.txt"
    },
    {
      "type": "image",
      "file": "image_a1b2c3d4.jpg",
      "path": "/path/to/chat_history/john/550e8400.../image_a1b2c3d4.jpg"
    }
  ]
}
```

**Expected Status:** 200

**Parameters:**
- `username` (in URL): Username
- `session_id` (in URL): Session ID

**Notes:**
- Returns both text and image messages
- Messages ordered by filename (roughly chronological)
- Includes full file paths for images

---

### 10. Delete Chat Session

**Endpoint:** `DELETE /api/chat/session/{username}/{session_id}`

**Purpose:** Delete a chat session and all its messages.

**Command:**
```bash
curl -X DELETE "http://localhost:8000/api/chat/session/john/550e8400-e29b-41d4-a716-446655440000" | jq .
```

**Example Response:**
```json
{
  "status": "success",
  "message": "Session 550e8400-e29b-41d4-a716-446655440000 deleted"
}
```

**Expected Status:** 200

**Parameters:**
- `username` (in URL): Username
- `session_id` (in URL): Session ID

**Notes:**
- Deletes all messages in session
- Removes session directory completely
- Operation is irreversible

---

### 11. Download Chat File

**Endpoint:** `GET /api/chat/file/{username}/{session_id}/{filename}`

**Purpose:** Download a file from a chat session.

**Command:**
```bash
curl -X GET "http://localhost:8000/api/chat/file/john/550e8400-e29b-41d4-a716-446655440000/image_a1b2c3d4.jpg" \
  --output downloaded_image.jpg
```

**Expected Status:** 200

**Parameters:**
- `username` (in URL): Username
- `session_id` (in URL): Session ID
- `filename` (in URL): Filename to download

**Notes:**
- Returns binary file content
- Use `--output` flag with curl to save file
- Returns 404 if file doesn't exist

---

## Testing Workflow

### Complete Test Flow

1. **Start Server**
   ```bash
   python main.py
   ```

2. **Create a Session**
   ```bash
   SESSION_ID=$(curl -s -X POST "http://localhost:8000/api/chat/session?username=john" | jq -r '.id')
   echo "Session: $SESSION_ID"
   ```

3. **Save Some Messages**
   ```bash
   curl -X POST "http://localhost:8000/api/chat/message" \
     -F "username=john" \
     -F "session_id=$SESSION_ID" \
     -F "content=First message!" \
     -F "message_type=text"

   curl -X POST "http://localhost:8000/api/chat/message" \
     -F "username=john" \
     -F "session_id=$SESSION_ID" \
     -F "content=Second message!" \
     -F "message_type=text"
   ```

4. **View History**
   ```bash
   curl -X GET "http://localhost:8000/api/chat/history/john/$SESSION_ID" | jq .
   ```

5. **List All Sessions**
   ```bash
   curl -X GET "http://localhost:8000/api/chat/sessions/john" | jq .
   ```

6. **Clean Up**
   ```bash
   curl -X DELETE "http://localhost:8000/api/chat/session/john/$SESSION_ID" | jq .
   ```

---

## Troubleshooting

### Server Connection Issues
```bash
# Check if server is running
curl -X GET http://localhost:8000/health

# If connection refused, start the server:
python main.py
```

### Invalid JSON Response
```bash
# Remove jq to see raw response
curl -X GET http://localhost:8000/api/trading/etf-options

# Install jq if not available
# Ubuntu/Debian: sudo apt-get install jq
# macOS: brew install jq
```

### 400 Bad Request
- Check URL encoding for special characters
- Verify all required parameters are provided
- Check Content-Type headers

### 404 Not Found
- Verify endpoint path is correct
- Check session ID or file name exists
- Session IDs are case-sensitive

### 500 Internal Server Error
- Check database connection
- Verify .env credentials
- Check application logs

---

## API Response Formats

### Success Response (200)
```json
{
  "data": { ... },
  "status": "success",
  "count": 10
}
```

### Error Response (4xx, 5xx)
```json
{
  "detail": "Error message describing the issue"
}
```

---

## Testing Tips

1. **Use `jq` for pretty-printing JSON**
   ```bash
   curl -X GET http://localhost:8000/api/trading/etf-options | jq .
   ```

2. **Save responses to file**
   ```bash
   curl -X GET http://localhost:8000/api/trading/etf-options > response.json
   ```

3. **Test with different usernames**
   ```bash
   curl -X POST "http://localhost:8000/api/chat/session?username=alice"
   curl -X POST "http://localhost:8000/api/chat/session?username=bob"
   ```

4. **Use variables in bash**
   ```bash
   USERNAME="john"
   SESSION_ID="your-session-id"
   curl -X GET "http://localhost:8000/api/chat/history/$USERNAME/$SESSION_ID"
   ```

---

## Additional Resources

- **API Documentation:** http://localhost:8000/docs (Swagger UI)
- **Alternative Docs:** http://localhost:8000/redoc
- **Test Client Script:** `python test_client.py`
- **Bash Test Script:** `bash test_endpoints.sh`

---

This guide provides comprehensive examples for testing all endpoints. Choose the testing method that works best for your workflow!
