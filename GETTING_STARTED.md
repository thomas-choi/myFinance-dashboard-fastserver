# 🚀 Getting Started with FastAPI Finance Dashboard Server

## ✅ What's Already Done

The complete FastAPI server has been created with all core features implemented:

- ✅ **ETF Options Monitor** - Real-time ETF options trading data
- ✅ **Stock Options Monitor** - Real-time US stock options trading data  
- ✅ **Chat History Management** - Persistent chat sessions with file storage
- ✅ **Database Integration** - MySQL with SSH tunnel support
- ✅ **Docker Support** - Containerized deployment ready
- ✅ **API Documentation** - Swagger UI and ReDoc
- ✅ **Tests** - Unit test suite included
- ✅ **All Dependencies Installed** - Python environment configured

## 🔧 What You Need to Do

### Step 1: Update Database Credentials

Edit the `.env` file with your DigitalOcean database credentials:

```bash
# Edit .env
DBHOST=your-db-host.ondigitalocean.com
DBPORT=25060
DBUSER=your_username
DBPWD=your_password
DBMKTDATA=GlobalMarketData
```

### Step 2: Verify Database Setup

Ensure these stored procedures exist in your MySQL database:
- `Trading.sp_etf_trades_v2` - For ETF options
- `Trading.sp_stock_trades_V3` - For stock options

### Step 3: Start the Server

**Option A: Direct Python (Development)**
```bash
cd /home/thomas/projects/myFinance-dashboard-pyserver
python main.py
```

**Option B: With Uvicorn**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: Docker (Production)**
```bash
docker compose up -d
```

### Step 4: Test the API

Once running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Quick Reference

### Trading Endpoints

```bash
# Get ETF options
curl http://localhost:8000/api/trading/etf-options

# Get stock options
curl http://localhost:8000/api/trading/stock-options

# Get max date from a table
curl "http://localhost:8000/api/trading/max-date/histdailyprice7?symbol=AAPL"

# Execute custom query
curl -X POST "http://localhost:8000/api/trading/custom-query?query=SELECT%20*%20FROM%20OptionChains%20LIMIT%201"
```

### Chat Endpoints

```bash
# Create a new chat session
curl -X POST "http://localhost:8000/api/chat/session?username=john"

# Get user sessions
curl http://localhost:8000/api/chat/sessions/john

# Get chat history
curl http://localhost:8000/api/chat/history/john/{session_id}

# Delete a session
curl -X DELETE "http://localhost:8000/api/chat/session/john/{session_id}"
```

## 📁 Project Structure

```
myFinance-dashboard-pyserver/
├── app/                          # Main application package
│   ├── api/routes/              # API endpoint definitions
│   │   ├── trading.py           # Trading endpoints
│   │   └── chat.py              # Chat endpoints
│   ├── services/                # Business logic
│   │   ├── trading_service.py   # Trading operations
│   │   └── chat_service.py      # Chat operations
│   ├── schemas/                 # Data validation (Pydantic)
│   ├── db/                      # Database management
│   ├── core/                    # Configuration & logging
│   └── models/                  # ORM models (placeholder)
├── tests/                        # Unit tests
├── chat_history/                # Chat file storage
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container config
├── docker-compose.yml           # Docker Compose setup
├── .env                         # Configuration (needs update)
├── .env.example                 # Template
├── README.md                    # Full documentation
├── QUICK_START.md              # Quick reference
└── GETTING_STARTED.md          # This file
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_trading.py::test_health_check -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Start services (builds if needed)
docker compose up -d

# View logs
docker compose logs -f financeagentserver

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

### Docker Commands Reference

```bash
# Build image
docker build -t myfinance-dashboard .

# Run container
docker run -d \
  --name financeserver \
  -p 8000:8000 \
  -v chat_history:/app/chat_history \
  -e DBHOST=your-host \
  -e DBUSER=your_user \
  -e DBPWD=your_password \
  myfinance-dashboard

# Execute command in container
docker exec financeserver curl http://localhost:8000/health

# View logs
docker logs financeserver -f
```

## 🔍 Troubleshooting

### Port Already in Use
```bash
# Change port in .env
APP_PORT=8001

# Or find and kill process on 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Database Connection Fails
```bash
# Test database connection directly
python -c "from app.db.database import get_db_engine; get_db_engine()"

# Check .env credentials
cat .env | grep DB
```

### Chat History Directory Issues
```bash
# Create with proper permissions
mkdir -p chat_history
chmod -R 755 chat_history

# Check permissions
ls -la chat_history/
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify environment
python -c "import fastapi; import pandas; import sqlalchemy; print('✓ All packages OK')"
```

## 📋 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DBHOST | localhost | Database host |
| DBPORT | 3306 | Database port |
| DBUSER | root | Database user |
| DBPWD | | **REQUIRED** - Database password |
| DBMKTDATA | GlobalMarketData | Database name |
| APP_PORT | 8000 | Server port |
| APP_HOST | 0.0.0.0 | Server bind address |
| DEBUG | True | Debug mode |
| CHAT_HISTORY_PATH | ./chat_history | Chat storage directory |
| SSHHOST | | Optional SSH host |
| SSHUSR | | Optional SSH user |
| SSHPWD | | Optional SSH password |

## 🔐 Security Notes

- ⚠️ **Never commit `.env` file** - It's in `.gitignore`
- Store database passwords securely
- Use SSH tunnels for remote database connections
- Use HTTPS in production
- Configure CORS for your domain
- Validate all user inputs (already done via Pydantic)

## 📚 Documentation

- **README.md** - Complete documentation
- **QUICK_START.md** - Quick reference guide
- **PROJECT_SUMMARY.txt** - Detailed project overview
- **Swagger UI** - Interactive API docs at `/docs`

## 🚀 Next Steps

1. ✅ Update `.env` with database credentials
2. ✅ Start the server: `python main.py`
3. ✅ Test endpoints in Swagger UI: `http://localhost:8000/docs`
4. ✅ Verify trading endpoints return data
5. ✅ Test chat endpoints
6. ✅ Deploy to Docker when ready

## 💡 Tips

- Use Swagger UI to test all endpoints without curl
- Check logs for debugging: `docker compose logs financeagentserver`
- Monitor database queries: Set `DEBUG=True` in .env
- Keep `.env` out of version control
- Use separate `.env` files for dev/prod

## 🆘 Need Help?

1. Check logs: `python main.py` shows real-time logs
2. Review README.md for detailed API documentation
3. Test endpoints in Swagger UI: http://localhost:8000/docs
4. Verify database connection: See Troubleshooting section

---

**Status**: ✅ Ready to Go!

All setup is complete. Update your `.env` credentials and run: `python main.py`

Then visit: **http://localhost:8000/docs**
