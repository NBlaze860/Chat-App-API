from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.models.chat import SendMessageRequest
from app.services.auth import get_current_user
from app.services.websocket_manager import manager
from app.utils.helpers import save_message_to_db, generate_chat_id
from app.database import get_supabase_client

router = APIRouter()

@router.get("/chat/{receiver_id}/messages")
async def get_chat_messages(
    receiver_id: str, 
    current_user: str = Depends(get_current_user),
    limit: int = 50
):
    """Get all messages for a chat with another user"""
    try:
        supabase = get_supabase_client()
        chat_id = generate_chat_id(current_user, receiver_id)
        
        result = supabase.table("messages").select("*").eq(
            "chat_id", chat_id
        ).order("created_at", desc=False).limit(limit).execute()
        
        return {
            "status": "success",
            "data": result.data or [],
            "chat_id": chat_id,
            "count": len(result.data) if result.data else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting messages: {str(e)}")

@router.post("/chat/{receiver_id}/send")
async def send_message_http(
    receiver_id: str,
    message: SendMessageRequest,
    current_user: str = Depends(get_current_user)
):
    """Send message via HTTP (alternative to WebSocket)"""
    try:
        result = await save_message_to_db(current_user, receiver_id, message.message_text)
        
        if result["status"] == "success":
            # Try to send via WebSocket if receiver is online
            chat_message = {
                "type": "message",
                "data": result["data"],
                "sender_id": current_user,
                "receiver_id": receiver_id,
                "message_text": message.message_text,
                "timestamp": datetime.now().isoformat()
            }
            
            await manager.send_message_to_chat_participants(
                current_user, receiver_id, chat_message
            )
            
            return result
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")

@router.get("/chats")
async def get_user_chats(current_user: str = Depends(get_current_user)):
    """Get all chats for current user"""
    try:
        supabase = get_supabase_client()
        result = supabase.table("chats").select("*").or_(
            f"user1_id.eq.{current_user},user2_id.eq.{current_user}"
        ).order("last_message_at", desc=True).execute()
        
        return {
            "status": "success",
            "data": result.data or [],
            "count": len(result.data) if result.data else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting chats: {str(e)}")

@router.get("/online-users")
async def get_online_users(current_user: str = Depends(get_current_user)):
    """Get list of currently online users"""
    return {
        "status": "success",
        "users": manager.get_online_users(),
        "count": len(manager.get_online_users())
    } 