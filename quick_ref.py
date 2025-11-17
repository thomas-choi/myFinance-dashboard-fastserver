#!/usr/bin/env python3
"""
FastAPI Finance Dashboard - Quick Test Reference Card
Print this to terminal for quick lookup while testing
"""

import subprocess
import sys

REFERENCE = """
╔═══════════════════════════════════════════════════════════════════════════╗
║         FastAPI FINANCE DASHBOARD - QUICK TEST REFERENCE CARD            ║
╚═══════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 THREE WAYS TO TEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. INTERACTIVE PYTHON TEST CLIENT (Recommended)
   $ python test_client.py
   → Interactive menu system with color-coded output
   → Automatic session management
   → All 11 endpoints in one tool

2. BASH SCRIPT WITH CURL EXAMPLES
   $ bash test_endpoints.sh
   → Copy-paste ready curl commands
   → Interactive prompts for each endpoint
   → No Python dependencies needed

3. MANUAL CURL COMMANDS
   See curl examples below

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 QUICK CURL COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 HEALTH & ROOT
 ─────────────────────────────────────────────────────────────────────────
  curl http://localhost:8000/health
  curl http://localhost:8000/

 TRADING (4 endpoints)
 ─────────────────────────────────────────────────────────────────────────
  curl http://localhost:8000/api/trading/etf-options
  curl http://localhost:8000/api/trading/stock-options
  curl "http://localhost:8000/api/trading/max-date/histdailyprice7"
  curl -X POST "http://localhost:8000/api/trading/custom-query?query=SELECT%201"

 CHAT (7 endpoints)
 ─────────────────────────────────────────────────────────────────────────
  SAVE SESSION_ID from create and use in other commands:
  
  CREATE:     curl -X POST http://localhost:8000/api/chat/session?username=john
  LIST:       curl http://localhost:8000/api/chat/sessions/john
  MESSAGE:    curl -X POST http://localhost:8000/api/chat/message \\
              -F username=john -F session_id=<ID> -F content=test -F message_type=text
  HISTORY:    curl http://localhost:8000/api/chat/history/john/<SESSION_ID>
  UPLOAD:     curl -X POST http://localhost:8000/api/chat/upload/john/<SESSION_ID> \\
              -F file=@image.jpg
  DELETE:     curl -X DELETE http://localhost:8000/api/chat/session/john/<SESSION_ID>
  DOWNLOAD:   curl http://localhost:8000/api/chat/file/john/<SESSION_ID>/filename.jpg

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 EXAMPLE WORKFLOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 # 1. Start server
 $ python main.py

 # 2. In another terminal:

 # 3. Create session and save ID
 $ SESSION_ID=$(curl -s -X POST http://localhost:8000/api/chat/session?username=john | jq -r '.id')

 # 4. Send messages
 $ curl -X POST http://localhost:8000/api/chat/message \\
   -F username=john -F session_id=$SESSION_ID \\
   -F content="Hello World!" -F message_type=text

 # 5. Get history
 $ curl http://localhost:8000/api/chat/history/john/$SESSION_ID | jq .

 # 6. Cleanup
 $ curl -X DELETE http://localhost:8000/api/chat/session/john/$SESSION_ID

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 ENDPOINTS SUMMARY (11 Total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 TRADING ENDPOINTS:
  1. GET  /api/trading/etf-options          → Real-time ETF options
  2. GET  /api/trading/stock-options        → Real-time stock options
  3. GET  /api/trading/max-date/{table}     → Max date from table
  4. POST /api/trading/custom-query         → Execute SQL query

 CHAT ENDPOINTS:
  5. POST   /api/chat/session               → Create session
  6. GET    /api/chat/sessions/{user}       → List sessions
  7. POST   /api/chat/message               → Save message
  8. POST   /api/chat/upload/{user}/{sess}  → Upload image
  9. GET    /api/chat/history/{user}/{sess} → Get chat history
 10. DELETE /api/chat/session/{user}/{sess} → Delete session
 11. GET    /api/chat/file/{user}/{sess}/{f}→ Download file

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 HELPFUL TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Pretty-print JSON:
  $ curl ... | jq .

 Save response to file:
  $ curl ... > response.json

 Extract specific field:
  $ curl -s ... | jq '.data[0].symbol'

 Use variables:
  $ USERNAME="john"
  $ SESSION_ID="550e8400-..."
  $ curl http://localhost:8000/api/chat/sessions/$USERNAME

 Check JSON syntax:
  $ jq . < file.json

 Create test image:
  $ python -c "open('test.jpg','wb').write(b'\\xff\\xd8\\xff\\xe0...\\xff\\xd9')"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 In-browser API docs:     http://localhost:8000/docs
 Alternative API docs:    http://localhost:8000/redoc
 Detailed test guide:     TEST_GUIDE.md
 Python test client:      test_client.py
 Bash test script:        test_endpoints.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 COMMON ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 Connection refused?
  → Start server: python main.py

 "jq: command not found"?
  → Install jq: apt-get install jq (Linux) or brew install jq (macOS)

 JSON parse error?
  → Remove | jq to see raw response

 404 Not Found?
  → Check endpoint path and parameters

 500 Internal Server Error?
  → Check .env database credentials
  → Check application logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Print this file for quick reference: python quick_ref.py
Full guide with examples:            cat TEST_GUIDE.md
Interactive testing:                 python test_client.py

═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    try:
        # Try to display with less/more for better viewing
        if sys.stdout.isatty():
            pager = subprocess.Popen(['less', '-R'], stdin=subprocess.PIPE, text=True)
            pager.communicate(input=REFERENCE)
        else:
            print(REFERENCE)
    except:
        print(REFERENCE)
