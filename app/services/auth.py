from fastapi import HTTPException, Query
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError, InvalidSignatureError
from app.config import settings

def decode_jwt_token(token: str) -> str:
    """Extract user_id from JWT token"""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id = payload.get("user_id") or payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (InvalidTokenError, InvalidSignatureError):
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(token: str = Query(...)) -> str:
    """Dependency to get current user from token"""
    return decode_jwt_token(token) 