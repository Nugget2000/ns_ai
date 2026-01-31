import os
import hashlib
import firebase_admin
from firebase_admin import auth
from functools import lru_cache
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.user_service import UserService
from ..services.activity_logging_service import activity_logging
from ..models.schemas import UserResponse, UserRole

# Initialize HTTPBearer scheme to extract the token from the Authorization header
security = HTTPBearer()

# Simple in-memory session cache: token_hash -> (session_id, created_at)
# Sessions are reused for requests with the same token
_session_cache: dict[str, tuple[str, datetime]] = {}
SESSION_CACHE_TTL_MINUTES = 30  # Reuse session for 30 minutes


def _get_or_create_session(token_hash: str, uid: str, email: str, user_agent: str, client_ip: str) -> str:
    """Get existing session from cache or create a new one."""
    now = datetime.utcnow()
    
    # Check cache for existing session
    if token_hash in _session_cache:
        session_id, created_at = _session_cache[token_hash]
        # Check if session is still valid (within TTL)
        if now - created_at < timedelta(minutes=SESSION_CACHE_TTL_MINUTES):
            return session_id
    
    # Create new session
    session_id = activity_logging.create_session(uid, email)
    _session_cache[token_hash] = (session_id, now)
    
    # Log the login event for new sessions
    activity_logging.log_login(session_id, uid, email, user_agent, client_ip)
    
    # Clean up old cache entries periodically
    _cleanup_session_cache()
    
    return session_id


def _cleanup_session_cache():
    """Remove expired entries from session cache."""
    now = datetime.utcnow()
    expired_keys = [
        key for key, (_, created_at) in _session_cache.items()
        if now - created_at > timedelta(minutes=SESSION_CACHE_TTL_MINUTES * 2)
    ]
    for key in expired_keys:
        del _session_cache[key]


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verifies the Firebase ID Token.
    Returns the decoded token or raises HTTPException.
    """
    token = credentials.credentials
    try:
        # Verify the token against Firebase Auth
        decoded_token = auth.verify_id_token(token)
        # Store token hash for session caching
        decoded_token['_token_hash'] = hashlib.sha256(token.encode()).hexdigest()[:16]
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

def get_current_user(token: dict = Depends(verify_token), request: Request = None) -> UserResponse:
    """
    Get the current user from Firestore based on the token.
    Creates the user if they don't exist.
    Gets or creates a session for activity logging.
    """
    uid = token.get("uid")
    email = token.get("email")
    token_hash = token.get("_token_hash", "")
    
    if not uid:
        raise HTTPException(status_code=400, detail="Invalid token: no uid")
    
    user = UserService.get_or_create_user(uid, email)
    
    # Get or create a session for this token
    if request and token_hash:
        user_agent = request.headers.get("user-agent", "")
        client_ip = request.client.host if request.client else ""
        session_id = _get_or_create_session(token_hash, uid, email, user_agent, client_ip)
        request.state.session_id = session_id
        request.state.user_uid = uid
        request.state.user_email = email
    
    return user

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


