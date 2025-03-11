from fastapi import HTTPException, Depends, Request
from firebase_admin import auth
from typing import Dict, Optional

async def verify_token(request: Request) -> Dict:
    """
    Verify Firebase ID token from Authorization header.
    Returns user info if token is valid, otherwise raises HTTPException.
    """
    authorization = request.headers.get("Authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization token")
    
    token = authorization.replace("Bearer ", "")
    
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

async def get_current_user(token_data: Dict = Depends(verify_token)) -> Dict:
    """
    Get current user from Firebase ID token.
    """
    return token_data

def is_authenticated(request: Request) -> bool:
    """
    Check if user is authenticated based on Authorization header.
    Returns True if authenticated, False otherwise.
    """
    authorization = request.headers.get("Authorization")
    
    if not authorization or not authorization.startswith("Bearer "):
        return False
    
    token = authorization.replace("Bearer ", "")
    
    try:
        auth.verify_id_token(token)
        return True
    except:
        return False