from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, websocket

app = FastAPI(title="Chat App", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api")
app.include_router(websocket.router)

@app.get("/")
async def root():
    return {"message": "Chat App API is running!"} 