from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import verify_jwt_token

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user from JWT token."""
    try:
        token = credentials.credentials
        user_info = verify_jwt_token(token)
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Optional: Create a dependency that doesn't raise an error if no token
async def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Optional user dependency - returns None if no valid token."""
    try:
        if not credentials:
            return None
        token = credentials.credentials
        user_info = verify_jwt_token(token)
        return user_info
    except:
        return None