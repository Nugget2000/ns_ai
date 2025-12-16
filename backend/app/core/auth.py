import os
import firebase_admin
from firebase_admin import auth

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.user_service import UserService
from ..models.schemas import UserResponse, UserRole

# Initialize HTTPBearer scheme to extract the token from the Authorization header
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verifies the Firebase ID Token.
    Returns the decoded token or raises HTTPException.
    """
    token = credentials.credentials
    try:
        # Verify the token against Firebase Auth
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except firebase_admin.auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except firebase_admin.auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except firebase_admin.auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Revoked authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # Catch other errors (e.g., certificate fetch failed)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: dict = Depends(verify_token)) -> UserResponse:
    """
    Get the current user from Firestore based on the token.
    Creates the user if they don't exist.
    """
    uid = token.get("uid")
    email = token.get("email")
    if not uid:
        raise HTTPException(status_code=400, detail="Invalid token: no uid")
    
    return UserService.get_or_create_user(uid, email)

def get_active_user(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
    Ensure the user has access (not pending).
    """
    if user.role == UserRole.PENDING:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is pending approval"
        )
    return user

def get_admin_user(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """
    Ensure the user is an admin.
    """
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return user
