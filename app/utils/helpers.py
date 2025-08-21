from datetime import datetime
from app.database import get_supabase_client

def generate_chat_id(user1_id: str, user2_id: str) -> str:
    """Generate consistent chat ID for two users"""
    # Strip any curly braces from both user IDs
    user1_id = user1_id.strip('{}')
    user2_id = user2_id.strip('{}')
    users = sorted([user1_id, user2_id])
    return f"{users[0]}_{users[1]}"

async def save_message_to_db(sender_id: str, receiver_id: str, message_text: str) -> dict:
    """Save message to database and update chat"""
    try:
        # Strip curly braces from IDs
        sender_id = sender_id.strip('{}')
        receiver_id = receiver_id.strip('{}')
        
        supabase = get_supabase_client()
        chat_id = generate_chat_id(sender_id, receiver_id)
        
        # Check if chat exists, create if not
        chat_result = supabase.table("chats").select("*").eq("chat_id", chat_id).execute()
        
        if not chat_result.data:
            # Create new chat
            supabase.table("chats").insert({
                "chat_id": chat_id,
                "user1_id": min(sender_id, receiver_id),
                "user2_id": max(sender_id, receiver_id),
                "last_message_at": datetime.now().isoformat()
            }).execute()
        else:
            # Update last message time
            supabase.table("chats").update({
                "last_message_at": datetime.now().isoformat()
            }).eq("chat_id", chat_id).execute()
        
        # Insert message
        result = supabase.table("messages").insert({
            "chat_id": chat_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message_text": message_text
        }).execute()
        
        return {
            "status": "success",
            "data": result.data[0] if result.data else None
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)} 