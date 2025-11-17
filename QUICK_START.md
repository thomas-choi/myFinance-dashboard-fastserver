# FastAPI Finance Dashboard Server - Quick Start Guide

## 🚀 What's Been Created

A complete FastAPI server for managing:
1. **ETF Options Monitor** - Real-time ETF options trading data
2. **Stock Options Monitor** - Real-time US stock options trading data
3. **Chat History Management** - Persistent chat sessions with file storage

## 📁 Project Structure

```
myFinance-dashboard-pyserver/
├── app/
│   ├── api/routes/
│   │   ├── trading.py       # ETF & Stock options endpoints
│   │   └── chat.py          # Chat history endpoints
│   ├── core/
│   │   ├── config.py        # Settings management
│   │   └── logging.py       # Logging configuration
│   ├── db/
│   │   └── database.py      # MySQL connection with SSH tunnel
│   ├── schemas/
│   │   ├── trading.py       # Trading data schemas
│   │   └── chat.py          # Chat history schemas
│   └── services/
│       ├── trading_service.py  # Trading data logic
│       └── chat_service.py     # Chat history logic
├── tests/                   # Unit tests
├── main.py                  # FastAPI app entry point
├── requirements.txt         # Python dependencies (installed)
├── Dockerfile              # Docker container config
├── docker-compose.yml      # Docker Compose config with Redis
├── .env                    # Configuration (created)
├── .env.example           # Configuration template
└── README.md              # Full documentation
```

## ⚙️ Configuration

Edit `.env` file with your DigitalOcean database credentials:

```bash
DBHOST=your-db-host.ondigitalocean.com
DBPORT=25060
DBUSER=your_username
DBPWD=your_password
DBMKTDATA=GlobalMarketData
```

## 🏃 Running Locally

### Option 1: Direct Python (Development)
```bash
cd /home/thomas/projects/myFinance-dashboard-pyserver

# Activate virtual environment (already created)
source .venv/bin/activate

# Run the server
python main.py
```

### Option 2: With Uvicorn (More control)
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: http://localhost:8000

## 📚 API Documentation

Once running, access interactive docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🐳 Running with Docker

### Quick Start
```bash
# Build and run
docker compose up -d

# View logs
docker compose logs -f financeagentserver

# Stop
docker compose down
```

## 📊 API Endpoints

### Trading Endpoints

**Get ETF Options**
```
GET /api/trading/etf-options
```

**Get Stock Options**
```
GET /api/trading/stock-options
```

**Get Maximum Date**
```
GET /api/trading/max-date/{table_name}?symbol=OPTIONAL
```

**Custom Query**
```
POST /api/trading/custom-query?query=YOUR_SQL
```

### Chat Endpoints

**Create Session**
```
POST /api/chat/session?username=john
```

**Get Sessions**
```
GET /api/chat/sessions/{username}
```

**Save Message**
```
POST /api/chat/message
FormData:
  - username: john
  - session_id: uuid
  - content: "Hello"
  - message_type: "text"
```

**Upload Image**
```
POST /api/chat/upload/{username}/{session_id}
(multipart/form-data with file)
```

**Get History**
```
GET /api/chat/history/{username}/{session_id}
```

**Delete Session**
```
DELETE /api/chat/session/{username}/{session_id}
```

## 🔧 Key Features

✅ **Database Integration**
- MySQL connection with SQLAlchemy
- Connection pooling (pool_size=10, max_overflow=20)
- SSH tunnel support for secure remote connections
- Automatic cleanup on shutdown

✅ **Trading Data**
- Calls `Trading.sp_etf_trades_v2` for ETF options
- Calls `Trading.sp_stock_trades_V3` for stock options
- Custom SQL query execution

✅ **Chat Management**
- File-based storage: `chat_history/{username}/{session_id}/`
- Text message support
- Image upload support
- Session management

✅ **Production Ready**
- Docker containerization with health checks
- Docker Compose with Redis
- Pydantic data validation
- Error handling
- Comprehensive logging

## 🔑 Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| DBHOST | localhost | Database host |
| DBPORT | 3306 | Database port |
| DBUSER | root | Database user |
| DBPWD | | Database password |
| DBMKTDATA | GlobalMarketData | Database name |
| APP_PORT | 8000 | Server port |
| DEBUG | False | Debug mode |
| CHAT_HISTORY_PATH | ./chat_history | Chat storage |

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_trading.py -v

# With coverage
pytest tests/ --cov=app
```

## 📝 Next Steps

1. **Update `.env`** with your actual database credentials
2. **Test database connection** by starting the server
3. **Verify stored procedures** exist in your MySQL database:
   - `Trading.sp_etf_trades_v2`
   - `Trading.sp_stock_trades_V3`
4. **Access Swagger UI** at http://localhost:8000/docs to test endpoints
5. **Deploy to Docker** when ready for production

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Change in .env
APP_PORT=8001

# Or kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection failed?**
- Verify `.env` credentials
- Check if SSH tunnel is needed (use SSHHOST, SSHUSR, SSHPWD)
- Test with: `python -c "from app.db.database import get_db_engine; get_db_engine()"`

**Chat history not saving?**
- Verify `chat_history/` directory exists and is writable
- Check file permissions: `chmod -R 755 chat_history/`

## 📞 Support

Refer to `README.md` for:
- Complete API documentation
- Detailed architecture notes
- Security considerations
- Deployment instructions
- Database schema references

---

**Status**: ✅ Project setup complete and ready to run!
**Dependencies**: ✅ All packages installed
**Configuration**: ⚠️ Update `.env` with your credentials
**Testing**: ✅ Unit tests available
