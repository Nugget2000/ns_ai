"""
Activity Logging Service

Manages user sessions and activity event logging for admin tracking.
"""

import logging
import traceback
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from firebase_admin import firestore

db = firestore.client()

SESSIONS_COLLECTION = "user_sessions"
EVENTS_COLLECTION = "session_events"


class ActivityLoggingService:
    """Service for managing user activity logging."""

    @staticmethod
    def create_session(uid: str, email: str) -> str:
        """
        Creates a new session for a user login.
        Returns the session_id.
        """
        try:
            session_id = str(uuid.uuid4())
            session_data = {
                "session_id": session_id,
                "uid": uid,
                "email": email,
                "started_at": firestore.SERVER_TIMESTAMP,
                "last_activity": firestore.SERVER_TIMESTAMP,
                "event_count": 0,
                "error_count": 0
            }
            
            db.collection(SESSIONS_COLLECTION).document(session_id).set(session_data)
            logging.info(f"Created session {session_id} for user {uid}")
            return session_id
        except Exception as e:
            logging.error(f"Failed to create session: {e}")
            logging.error(traceback.format_exc())
            # Return a temporary session ID to not break the flow
            return f"temp-{uuid.uuid4()}"

    @staticmethod
    def log_event(
        session_id: str,
        event_type: str,
        data: Dict[str, Any],
        error_info: Optional[Dict[str, Any]] = None,
        stacktrace: Optional[str] = None
    ) -> Optional[str]:
        """
        Logs an event for a session.
        
        Args:
            session_id: The session to log the event for
            event_type: Type of event (login, chat_message, chat_response, error, page_view)
            data: Event-specific data
            error_info: Optional error information
            stacktrace: Optional stacktrace for errors
            
        Returns:
            The event_id if successful, None otherwise
        """
        try:
            event_id = str(uuid.uuid4())
            event_data = {
                "event_id": event_id,
                "session_id": session_id,
                "event_type": event_type,
                "timestamp": firestore.SERVER_TIMESTAMP,
                "data": data,
            }
            
            if error_info:
                event_data["error_info"] = error_info
            if stacktrace:
                event_data["stacktrace"] = stacktrace
            
            # Add the event
            db.collection(EVENTS_COLLECTION).document(event_id).set(event_data)
            
            # Update session stats
            session_ref = db.collection(SESSIONS_COLLECTION).document(session_id)
            session_doc = session_ref.get()
            
            if session_doc.exists:
                update_data = {
                    "last_activity": firestore.SERVER_TIMESTAMP,
                    "event_count": firestore.Increment(1)
                }
                if error_info or event_type == "error":
                    update_data["error_count"] = firestore.Increment(1)
                
                session_ref.update(update_data)
            
            logging.debug(f"Logged event {event_type} for session {session_id}")
            return event_id
        except Exception as e:
            logging.error(f"Failed to log event: {e}")
            logging.error(traceback.format_exc())
            return None

    @staticmethod
    def get_user_sessions(uid: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Gets all sessions for a user, ordered by most recent first.
        """
        try:
            sessions_ref = db.collection(SESSIONS_COLLECTION)
            # Query without order_by to avoid composite index requirement
            query = sessions_ref.where("uid", "==", uid).limit(limit)
            
            sessions = []
            for doc in query.stream():
                session_data = doc.to_dict()
                sessions.append(session_data)
            
            # Sort by started_at in Python (descending - most recent first)
            sessions.sort(key=lambda x: x.get("started_at") or datetime.min, reverse=True)
            
            # Convert timestamps to ISO format strings after sorting
            for session_data in sessions:
                if session_data.get("started_at"):
                    session_data["started_at"] = session_data["started_at"].isoformat()
                if session_data.get("last_activity"):
                    session_data["last_activity"] = session_data["last_activity"].isoformat()
            
            return sessions
        except Exception as e:
            logging.error(f"Failed to get user sessions: {e}")
            logging.error(traceback.format_exc())
            return []

    @staticmethod
    def get_session_events(session_id: str, limit: int = 200) -> List[Dict[str, Any]]:
        """
        Gets all events for a session, ordered by timestamp.
        """
        try:
            events_ref = db.collection(EVENTS_COLLECTION)
            # Query without order_by to avoid composite index requirement
            query = events_ref.where("session_id", "==", session_id).limit(limit)
            
            events = []
            for doc in query.stream():
                event_data = doc.to_dict()
                events.append(event_data)
            
            # Sort by timestamp in Python (ascending - chronological order)
            events.sort(key=lambda x: x.get("timestamp") or datetime.min)
            
            # Convert timestamp to ISO format string after sorting
            for event_data in events:
                if event_data.get("timestamp"):
                    event_data["timestamp"] = event_data["timestamp"].isoformat()
            
            return events
        except Exception as e:
            logging.error(f"Failed to get session events: {e}")
            logging.error(traceback.format_exc())
            return []

    @staticmethod
    def get_users_with_activity() -> List[Dict[str, Any]]:
        """
        Gets aggregated activity stats for all users.
        Returns list of users with total_sessions, total_events, total_errors, last_activity.
        """
        try:
            # Get all sessions grouped by user
            sessions_ref = db.collection(SESSIONS_COLLECTION)
            
            user_stats = {}
            for doc in sessions_ref.stream():
                session = doc.to_dict()
                uid = session.get("uid")
                
                if uid not in user_stats:
                    user_stats[uid] = {
                        "uid": uid,
                        "email": session.get("email"),
                        "total_sessions": 0,
                        "total_events": 0,
                        "total_errors": 0,
                        "last_activity": None
                    }
                
                user_stats[uid]["total_sessions"] += 1
                user_stats[uid]["total_events"] += session.get("event_count", 0)
                user_stats[uid]["total_errors"] += session.get("error_count", 0)
                
                # Track most recent activity
                session_activity = session.get("last_activity")
                if session_activity:
                    current_last = user_stats[uid]["last_activity"]
                    if not current_last or session_activity > current_last:
                        user_stats[uid]["last_activity"] = session_activity
            
            # Convert timestamps to ISO format
            result = []
            for uid, stats in user_stats.items():
                if stats["last_activity"]:
                    stats["last_activity"] = stats["last_activity"].isoformat()
                result.append(stats)
            
            # Sort by last_activity descending
            result.sort(key=lambda x: x.get("last_activity") or "", reverse=True)
            return result
        except Exception as e:
            logging.error(f"Failed to get users with activity: {e}")
            logging.error(traceback.format_exc())
            return []

    @staticmethod
    def log_login(session_id: str, uid: str, email: str, user_agent: str = None, ip: str = None) -> Optional[str]:
        """Convenience method to log a login event."""
        return ActivityLoggingService.log_event(
            session_id=session_id,
            event_type="login",
            data={
                "uid": uid,
                "email": email,
                "user_agent": user_agent,
                "ip": ip
            }
        )

    @staticmethod
    def log_chat_message(session_id: str, message: str) -> Optional[str]:
        """Convenience method to log a user chat message."""
        return ActivityLoggingService.log_event(
            session_id=session_id,
            event_type="chat_message",
            data={
                "message": message,
                "message_length": len(message)
            }
        )

    @staticmethod
    def log_chat_response(
        session_id: str,
        response: str,
        input_tokens: int = None,
        output_tokens: int = None,
        duration_ms: int = None
    ) -> Optional[str]:
        """Convenience method to log an Emanuel chat response."""
        return ActivityLoggingService.log_event(
            session_id=session_id,
            event_type="chat_response",
            data={
                "response": response[:2000] if response else None,  # Store up to 2000 chars
                "response_length": len(response) if response else 0,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "duration_ms": duration_ms
            }
        )

    @staticmethod
    def log_error(
        session_id: str,
        error_type: str,
        message: str,
        endpoint: str = None,
        stacktrace: str = None
    ) -> Optional[str]:
        """Convenience method to log an error event."""
        return ActivityLoggingService.log_event(
            session_id=session_id,
            event_type="error",
            data={
                "endpoint": endpoint
            },
            error_info={
                "error_type": error_type,
                "message": message
            },
            stacktrace=stacktrace
        )


# Singleton instance
activity_logging = ActivityLoggingService()
