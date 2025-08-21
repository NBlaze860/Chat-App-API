from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from datetime import datetime
import json
from app.services.auth import decode_jwt_token
from app.services.websocket_manager import manager
from app.utils.helpers import save_message_to_db, generate_chat_id

router = APIRouter()

@router.websocket("/ws/{receiver_id}")
async def websocket_endpoint(websocket: WebSocket, receiver_id: str, token: str = Query(...)):
    user_id = None  # Initialize user_id to avoid scope issues
    try:
        # Get current user from token
        try:
            user_id = decode_jwt_token(token)
            # Strip curly braces from IDs
            user_id = user_id.strip('{}')
            receiver_id = receiver_id.strip('{}')
        except Exception as e:
            print(f"JWT token decoding failed: {str(e)}")
            await websocket.close(code=4001, reason="Authentication failed")
            return
        
        print(f"WebSocket connection attempt - User: {user_id}, Receiver: {receiver_id}")
        
        # Connect user to specific chat
        await manager.connect(websocket, user_id, receiver_id)
        
        # Broadcast updated online users
        await manager.broadcast_online_users()
        
        # Send connection confirmation
        connection_msg = {
            "type": "connected",
            "message": f"Connected to chat with {receiver_id}",
            "chat_id": generate_chat_id(user_id, receiver_id)
        }
        print(f"Sending connection confirmation: {connection_msg}")
        await websocket.send_text(json.dumps(connection_msg))
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            print(f"Received message from {user_id}: {data}")
            
            try:
                message_data = json.loads(data)
                message_type = message_data.get("type", "chat")
                print(f"Message type: {message_type}")
                
                if message_type == "chat":
                    # Handle chat message
                    message_text = message_data.get("message", "")
                    if message_text.strip():
                        print(f"Processing chat message from {user_id} to {receiver_id}: {message_text}")
                        # Save message to database
                        result = await save_message_to_db(user_id, receiver_id, message_text)
                        print(f"Message save result: {result}")
                        
                        if result["status"] == "success":
                            # Send message to receiver if online
                            chat_message = {
                                "type": "message",
                                "data": result["data"],
                                "sender_id": user_id,
                                "receiver_id": receiver_id,
                                "message_text": message_text,
                                "timestamp": datetime.now().isoformat()
                            }
                            print(f"Sending chat message: {chat_message}")
                            
                            await manager.send_message_to_chat_participants(
                                user_id, receiver_id, chat_message
                            )
                
                elif message_type == "ping":
                    # Keep connection alive
                    await websocket.send_text(json.dumps({"type": "pong"}))
                    
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {str(e)}")
                # Handle plain text messages
                if data.strip():
                    result = await save_message_to_db(user_id, receiver_id, data)
                    if result["status"] == "success":
                        chat_message = {
                            "type": "message",
                            "data": result["data"],
                            "sender_id": user_id,
                            "receiver_id": receiver_id,
                            "message_text": data,
                            "timestamp": datetime.now().isoformat()
                        }
                        await manager.send_message_to_chat_participants(
                            user_id, receiver_id, chat_message
                        )
                
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user {user_id}")
        if user_id:
            manager.disconnect(user_id)
            await manager.broadcast_online_users()
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        try:
            if user_id:
                manager.disconnect(user_id)
                await manager.broadcast_online_users()
        except Exception as e:
            print(f"Error during disconnect: {str(e)}") 