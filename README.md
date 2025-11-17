# FastAPI Finance Dashboard Server

A FastAPI-based Python server for managing trading options monitor (ETF and stock) and chat history for the myFinance dashboard application.

## Features

- **ETF Options Monitor**: Real-time ETF options trading data
- **Stock Options Monitor**: Real-time US stock options trading data  
- **Chat History Management**: Persistent chat sessions with file storage
- **MySQL Database Integration**: Connect to DigitalOcean MySQL database
- **SSH Tunnel Support**: Optional SSH tunnel for secure database connections
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── trading.py      # Trading API endpoints
│   │       └── chat.py         # Chat history API endpoints
│   ├── core/
│   │   ├── config.py           # Application settings
│   │   └── logging.py          # Logging configuration
│   ├── db/
│   │   └── database.py         # Database connection management
│   ├── models/                 # SQLAlchemy models (placeholder)
│   ├── schemas/
│   │   ├── trading.py          # Trading data schemas
│   │   └── chat.py             # Chat history schemas
│   └── services/
│       ├── trading_service.py  # Trading data service
│       └── chat_service.py     # Chat history service
├── tests/                       # Unit tests
├── chat_history/               # Chat history file storage
├── main.py                     # FastAPI application entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose configuration
└── .env.example               # Environment variables template
```

## Installation

### Prerequisites

- Python 3.11+
- MySQL database on DigitalOcean (or compatible MySQL server)
- Docker and Docker Compose (optional, for containerized deployment)

### Setup

1. **Clone the repository**
   ```bash
   cd /home/thomas/projects/myFinance-dashboard-pyserver
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your database credentials:
   ```
   DBHOST=your-digitalocean-db-host
   DBPORT=25060
   DBUSER=your_db_user
   DBPWD=your_db_password
   DBMKTDATA=GlobalMarketData
   ```

5. **Run the application**
   ```bash
   python main.py
   ```
   
   Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start services
docker compose up -d

# View logs
docker compose logs -f myfin

# Stop services
docker compose down
```

### Using Docker directly

```bash
# Build image
docker build -t myfin_board_fastsvr .

# Run container
docker run -d \
  --name financeagentserver \
  -p 8000:8000 \
  -v /path/to/chat_history:/app/chat_history \
  -e DBHOST=your-host \
  -e DBPORT=25060 \
  -e DBUSER=your_user \
  -e DBPWD=your_password \
  myfin_board_fastsvr
```

## API Documentation

Once running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Trading Endpoints

#### Get ETF Options
```
GET /api/trading/etf-options
```
Returns latest ETF options with status and calculations.

#### Get Stock Options
```
GET /api/trading/stock-options
```
Returns latest US stock options with status and calculations.

#### Get Maximum Date
```
GET /api/trading/max-date/{table_name}?symbol=OPTIONAL_SYMBOL
```
Get the maximum date from a table.

#### Execute Custom Query
```
POST /api/trading/custom-query?query=YOUR_SQL_QUERY
```
Execute a custom SQL query.

### Chat History Endpoints

#### Create Chat Session
```
POST /api/chat/session?username=USERNAME
```

#### Get User Sessions
```
GET /api/chat/sessions/{username}
```

#### Save Chat Message
```
POST /api/chat/message
```
Form parameters:
- `username`: Username
- `session_id`: Session ID
- `content`: Message content
- `message_type`: "text" or "image"

#### Upload Chat Image
```
POST /api/chat/upload/{username}/{session_id}
```
Upload an image file for a chat session.

#### Get Chat History
```
GET /api/chat/history/{username}/{session_id}
```

#### Delete Chat Session
```
DELETE /api/chat/session/{username}/{session_id}
```

#### Download Chat File
```
GET /api/chat/file/{username}/{session_id}/{filename}
```

## Database Configuration

### Direct Connection
If your database is accessible directly:
```
DBHOST=your-host.ondigitalocean.com
DBPORT=25060
DBUSER=your_user
DBPWD=your_password
```

### SSH Tunnel Connection
For secure connection through SSH:
```
SSHHOST=your-ssh-host
SSHUSR=your-ssh-user
SSHPWD=your-ssh-password
DBHOST=internal-db-host
DBPORT=3306
```

## Chat History Storage

Chat history is stored in the local file system with the following structure:

```
chat_history/
├── {username}/
│   └── {session_id}/
│       ├── message_*.txt      # Text messages
│       └── image_*.jpg        # Image files
```

### Environment Configuration
```
CHAT_HISTORY_PATH=./chat_history
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Style
Ensure your code follows PEP 8:
```bash
pip install black flake8
black .
flake8 .
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DBHOST | localhost | Database host |
| DBPORT | 3306 | Database port |
| DBUSER | root | Database user |
| DBPWD | | Database password |
| DBMKTDATA | GlobalMarketData | Database name |
| APP_PORT | 8000 | Server port |
| APP_HOST | 0.0.0.0 | Server host |
| DEBUG | False | Debug mode |
| CHAT_HISTORY_PATH | ./chat_history | Chat storage directory |
| SSHHOST | | SSH host (optional) |
| SSHUSR | | SSH user (optional) |
| SSHPWD | | SSH password (optional) |

## Troubleshooting

### Database Connection Issues
```bash
# Test database connectivity
python -c "from app.db.database import get_db_engine; get_db_engine()"
```

### SSH Tunnel Issues
```bash
# Verify SSH credentials
ssh -v your-ssh-user@your-ssh-host
```

### Chat History Permissions
```bash
# Ensure chat_history directory is writable
chmod -R 755 chat_history/
```

## Security Considerations

- ⚠️ **Never commit `.env` file** - Add it to `.gitignore`
- Store credentials securely (use environment management systems in production)
- Restrict database user permissions to necessary tables only
- Use SSH tunnels for remote database connections
- Validate and sanitize all user inputs
- Use HTTPS in production

## Performance Optimization

- Database connection pooling is configured with `pool_size=10, max_overflow=20`
- SSH tunnel connection is reused across requests
- Chat history uses file-based storage for scalability
- Add Redis caching for frequently accessed trading data (configured in docker-compose)

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests for new functionality
4. Submit a pull request

## License

Proprietary - myFinance Dashboard Project

## Support

For issues or questions, contact the development team.

## Deployment Notes

### DigitalOcean Droplet Setup
```bash
# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose-plugin
sudo systemctl enable --now docker

# Clone repository and deploy
cd /home/thomas/projects/myFinance-dashboard-pyserver
cp .env.example .env
# Edit .env with your credentials
docker compose up -d
```

### Monitoring
Monitor the application logs:
```bash
docker compose logs -f financeagentserver
```

### Backup Chat History
```bash
docker cp financeagentserver:/app/chat_history ./chat_history_backup
```
