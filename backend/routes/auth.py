from fastapi import APIRouter, HTTPException
from typing import Dict, Any

router = APIRouter()

@router.get("/verify")
async def verify_auth():
    """
    Verify that the authentication API is working
    This endpoint is used by the frontend to check if the API is up
    """
    return {"status": "ok", "message": "Authentication API is working"}