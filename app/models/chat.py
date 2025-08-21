from pydantic import BaseModel

class SendMessageRequest(BaseModel):
    message_text: str 