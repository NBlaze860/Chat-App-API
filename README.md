# Chat App API

A real-time chat application built with FastAPI, WebSockets, and Supabase. This application provides both HTTP REST API endpoints and WebSocket connections for instant messaging between users.

## 🚀 Project Overview

This chat application enables users to:
- Send and receive messages in real-time via WebSockets
- Access chat history through REST API endpoints
- View online users and active conversations
- Authenticate using JWT tokens
- Store messages persistently in Supabase database

### Key Features

- **Real-time messaging** with WebSocket connections
- **RESTful API** for chat operations
- **JWT authentication** for secure user sessions
- **Supabase integration** for data persistence
- **CORS support** for cross-origin requests
- **Online user tracking** and presence indicators

## 🏗️ Architecture & Workflow

### Application Structure

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration and environment settings
├── database.py          # Supabase client initialization
├── models/
│   └── chat.py         # Pydantic models for request/response
├── routers/
│   ├── chat.py         # HTTP REST API endpoints
│   └── websocket.py    # WebSocket connection handling
├── services/
│   ├── auth.py         # JWT authentication logic
│   └── websocket_manager.py  # WebSocket connection management
└── utils/
    └── helpers.py      # Database operations and utilities
```

### Data Flow

1. **Authentication**: Users authenticate with JWT tokens
2. **Connection**: Users connect via WebSocket or HTTP endpoints
3. **Message Flow**:
   - User sends message via WebSocket or POST request
   - Message is saved to Supabase database
   - Message is broadcast to recipient if online
   - Chat metadata is updated (last message timestamp)

### Database Schema

- **chats**: Stores conversation metadata between users
- **messages**: Stores individual chat messages with timestamps

### WebSocket Workflow

1. Client connects to `/ws/{receiver_id}?token={jwt_token}`
2. Server validates JWT and establishes connection
3. Users exchange real-time messages
4. Server manages online user presence
5. Messages are persisted to database automatically

## 📦 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Supabase account and project
- Git (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd chat-app
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the root directory:

```env
# Supabase Configuration
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-anon-key

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key
```

### Step 5: Database Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)
2. Run the SQL schema from `database/schema.sql` in your Supabase SQL editor
3. Update your `.env` file with the Supabase URL and anon key

### Step 6: Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:8001`

## 🎯 Usage Guide

### Starting the Server

```bash
# Development mode with auto-reload
python run.py

# Or using uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### API Documentation

Once running, visit:
- **Interactive API docs**: `http://localhost:8001/docs`
- **ReDoc documentation**: `http://localhost:8001/redoc`

### REST API Endpoints

#### Get Chat Messages
```bash
GET /api/chat/{receiver_id}/messages?token={jwt_token}&limit=50
```

#### Send Message (HTTP)
```bash
POST /api/chat/{receiver_id}/send?token={jwt_token}
Content-Type: application/json

{
  "message_text": "Hello, how are you?"
}
```

#### Get User's Chats
```bash
GET /api/chats?token={jwt_token}
```

#### Get Online Users
```bash
GET /api/online-users?token={jwt_token}
```

### WebSocket Connection

Connect to WebSocket endpoint:
```javascript
const ws = new WebSocket('ws://localhost:8001/ws/{receiver_id}?token={jwt_token}');

// Send message
ws.send(JSON.stringify({
  type: "chat",
  message: "Hello from WebSocket!"
}));

// Receive messages
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

### Message Types

**Chat Message**:
```json
{
  "type": "chat",
  "message": "Your message text"
}
```

**Ping (Keep-alive)**:
```json
{
  "type": "ping"
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SUPABASE_URL` | Your Supabase project URL | Yes | - |
| `SUPABASE_KEY` | Supabase anon/public key | Yes | - |
| `JWT_SECRET` | Secret key for JWT token signing | Yes | - |

### Application Settings

The application uses Pydantic Settings for configuration management. Settings are loaded from:
1. Environment variables
2. `.env` file
3. Default values (if specified)

### CORS Configuration

The application is configured to allow all origins by default. For production, update the CORS settings in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🧪 Testing Instructions

### Manual Testing

1. **Start the server**: `python run.py`
2. **Open API docs**: Navigate to `http://localhost:8001/docs`
3. **Test endpoints**: Use the interactive documentation to test API endpoints
4. **WebSocket testing**: Use a WebSocket client or browser console

### Testing WebSocket Connection

```javascript
// Browser console test
const ws = new WebSocket('ws://localhost:8001/ws/user123?token=your-jwt-token');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', JSON.parse(e.data));
ws.send(JSON.stringify({type: "chat", message: "Test message"}));
```

### Database Testing

Verify your Supabase connection:
```bash
# Check if tables exist in Supabase dashboard
# Insert test data through the Supabase interface
# Verify API responses match database content
```

## 🔧 Troubleshooting & FAQ

### Common Issues

**1. "Authentication failed" on WebSocket connection**
- Verify JWT token is valid and not expired
- Check JWT_SECRET matches the one used to sign tokens
- Ensure token is passed as query parameter: `?token=your-jwt-token`

**2. "Connection refused" errors**
- Verify the server is running on port 8001
- Check firewall settings
- Ensure no other service is using port 8001

**3. Database connection issues**
- Verify Supabase URL and key in `.env` file
- Check Supabase project is active and accessible
- Ensure database schema has been applied

**4. CORS errors in browser**
- Check CORS middleware configuration in `app/main.py`
- Verify allowed origins include your frontend domain

**5. Messages not saving to database**
- Check Supabase logs for errors
- Verify database schema is correctly applied
- Check user IDs are properly formatted (no extra braces)

### Debug Mode

Enable debug logging by modifying the uvicorn run command:
```python
uvicorn.run(app, host="0.0.0.0", port=8001, reload=True, log_level="debug")
```

### Performance Considerations

- **Connection Limits**: Monitor active WebSocket connections
- **Database Queries**: Use pagination for large chat histories
- **Memory Usage**: WebSocket manager keeps connections in memory

## 🤝 Contributing Guide

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the existing code style
4. Test your changes thoroughly
5. Submit a pull request

### Code Style Guidelines

- Follow PEP 8 for Python code formatting
- Use type hints where appropriate
- Add docstrings for new functions and classes
- Keep functions focused and single-purpose

### Adding New Features

1. **Models**: Add new Pydantic models in `app/models/`
2. **Endpoints**: Create new routers in `app/routers/`
3. **Services**: Add business logic in `app/services/`
4. **Database**: Update schema in `database/schema.sql`

### Submitting Issues

When reporting bugs, include:
- Python version and OS
- Error messages and stack traces
- Steps to reproduce the issue
- Expected vs actual behavior

## 📄 License & Credits

### License

This project is licensed under the MIT License. See the LICENSE file for details.

### Credits

- **FastAPI**: Modern, fast web framework for building APIs
- **Supabase**: Open source Firebase alternative
- **Uvicorn**: Lightning-fast ASGI server
- **Pydantic**: Data validation using Python type annotations

### Dependencies

- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `websockets==12.0` - WebSocket support
- `supabase==2.15.3` - Supabase client
- `pydantic==2.5.0` - Data validation
- `PyJWT==2.8.0` - JWT token handling

---

For additional support or questions, please open an issue in the repository or refer to the API documentation at `/docs` when the server is running.