
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add backend directory to sys.path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Mock firebase_admin modules BEFORE importing app logic that uses them
sys.modules['firebase_admin'] = MagicMock()
sys.modules['firebase_admin.credentials'] = MagicMock()
sys.modules['firebase_admin.firestore'] = MagicMock()

# Now we can mock the specific firestore client call inside the service
with patch('app.services.firebase.firestore.client') as mock_client:
    # Setup the mock chain
    mock_db = MagicMock()
    mock_client.return_value = mock_db
    mock_collection = MagicMock()
    mock_db.collection.return_value = mock_collection
    
    # Import the function to test
    # Note: We need to import it inside the patch context or ensuring mocks are active
    # Because we mocked sys.modules, normal import should work but we need to rely on the patched client
    
    from app.services.firebase import log_login_event, db

    # Overwrite the db instance in the module with our mock if needed, 
    # but since 'db = firestore.client()' is at module level, it ran on import.
    # We might need to reload or patch the module attribute directly.
    import app.services.firebase
    app.services.firebase.db = mock_db

    def test_logging():
        print("Testing log_login_event...")
        user_data = {
            "uid": "test_user_123",
            "email": "test@example.com"
        }
        
        log_login_event(user_data)
        
        # Verify collection("ns_ai_logging") was accessed
        mock_db.collection.assert_called_with("ns_ai_logging")
        
        # Verify add() was called with correct data
        # We can't easily check SERVER_TIMESTAMP equality, so we check the other fields
        args, _ = mock_collection.add.call_args
        data = args[0]
        
        assert data["uid"] == "test_user_123"
        assert data["email"] == "test@example.com"
        assert data["event_type"] == "login"
        print("SUCCESS: log_login_event called Collection.add with correct data.")

    if __name__ == "__main__":
        try:
            test_logging()
        except AssertionError as e:
            print(f"FAILURE: Assertion failed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"FAILURE: {e}")
            sys.exit(1)
