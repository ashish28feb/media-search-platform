import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
from pydantic import BaseModel

class GoogleCredential(BaseModel):
    credential: str

class AuthResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    user: Optional[dict] = None
    authorized: Optional[bool] = None
    message: Optional[str] = None

# Environment variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
AUTHORIZED_USERS = os.getenv("AUTHORIZED_USERS", "").split(",")

def verify_google_token(credential: str) -> dict:
    """Verify Google OAuth token and return user info."""
    try:
        # Verify the token
        idinfo = id_token.verify_oauth2_token(
            credential, requests.Request(), GOOGLE_CLIENT_ID
        )
        
        # Extract user information
        user_info = {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "picture": idinfo.get("picture"),
            "google_id": idinfo.get("sub"),
        }
        
        return user_info
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def check_user_authorization(email: str) -> bool:
    """Check if user email is in authorized list."""
    # Clean up the authorized users list (remove empty strings and whitespace)
    authorized_list = [user.strip() for user in AUTHORIZED_USERS if user.strip()]
    
    print(f"Checking authorization for: {email}")
    print(f"Authorized users: {authorized_list}")
    
    return email in authorized_list

def create_jwt_token(user_info: dict) -> str:
    """Create JWT token for authenticated user."""
    payload = {
        "email": user_info["email"],
        "name": user_info["name"],
        "picture": user_info["picture"],
        "exp": datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
        "iat": datetime.utcnow(),
    }
    
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str) -> dict:
    """Verify JWT token and return user info."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def authenticate_google_user(credential: GoogleCredential) -> AuthResponse:
    """Main authentication flow."""
    try:
        # Step 1: Verify Google OAuth token
        user_info = verify_google_token(credential.credential)
        
        # Step 2: Check if user is authorized
        is_authorized = check_user_authorization(user_info["email"])
        
        if not is_authorized:
            return AuthResponse(
                success=False,
                authorized=False,
                user=user_info,
                message=f"Access denied. Email {user_info['email']} is not authorized."
            )
        
        # Step 3: Create JWT token for authorized user
        jwt_token = create_jwt_token(user_info)
        
        return AuthResponse(
            success=True,
            token=jwt_token,
            user=user_info,
            authorized=True,
            message="Authentication successful"
        )
        
    except Exception as e:
        return AuthResponse(
            success=False,
            message=f"Authentication failed: {str(e)}"
        )