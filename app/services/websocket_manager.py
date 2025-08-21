from fastapi import WebSocket
from typing import Dict, List
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_chat_rooms: Dict[str, str] = {}  # user_id -> current_receiver_id
        print("ConnectionManager initialized")
    
    async def connect(self, websocket: WebSocket, user_id: str, receiver_id: str):
        await websocket.accept()
        
        # Strip curly braces from IDs
        user_id = user_id.strip('{}')
        receiver_id = receiver_id.strip('{}')
        
        # Disconnect previous connection if exists
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].close()
            except:
                pass
        
        self.active_connections[user_id] = websocket
        self.user_chat_rooms[user_id] = receiver_id
        print(f"User {user_id} connected to chat with {receiver_id}")
        print(f"Current active connections: {list(self.active_connections.keys())}")
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            if user_id in self.user_chat_rooms:
                del self.user_chat_rooms[user_id]
            print(f"User {user_id} disconnected")
            print(f"Remaining active connections: {list(self.active_connections.keys())}")
    
    async def send_to_user(self, user_id: str, message: dict):
        print(f"Attempting to send message to user {user_id}")
        print(f"Active connections: {list(self.active_connections.keys())}")
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(json.dumps(message))
                print(f"Successfully sent message to user {user_id}")
                return True
            except Exception as e:
                print(f"Error sending message to user {user_id}: {str(e)}")
                self.disconnect(user_id)
                return False
        print(f"User {user_id} not found in active connections")
        return False
    
    async def send_message_to_chat_participants(self, sender_id: str, receiver_id: str, message_data: dict):
        """Send message to receiver if they're online"""
        print(f"Attempting to send message from {sender_id} to {receiver_id}")
        print(f"Message data: {message_data}")
        if receiver_id in self.active_connections:
            print(f"Receiver {receiver_id} is online, sending message")
            await self.send_to_user(receiver_id, message_data)
        else:
            print(f"Receiver {receiver_id} is not online")
    
    async def broadcast_online_users(self):
        online_users = list(self.active_connections.keys())
        message = {
            "type": "online_users",
            "users": online_users,
            "count": len(online_users)
        }
        
        for user_id in list(self.active_connections.keys()):
            success = await self.send_to_user(user_id, message)
            if not success:
                self.disconnect(user_id)
    
    def get_online_users(self) -> List[str]:
        return list(self.active_connections.keys())

# Global instance
manager = ConnectionManager() 