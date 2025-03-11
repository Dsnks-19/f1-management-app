from firebase_admin import auth
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verify Firebase authentication token and return the user's UID.
    """
    token = credentials.credentials
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

def format_response(status: str, message: str, data: dict = None):
    """
    Standardized JSON response format.
    """
    response = {
        "status": status,
        "message": message
    }
    if data:
        response["data"] = data
    return response
