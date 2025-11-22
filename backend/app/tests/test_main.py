import sys
from unittest.mock import MagicMock

# Mock firebase_admin and firestore BEFORE importing app modules
mock_firebase = MagicMock()
mock_firestore = MagicMock()
sys.modules["firebase_admin"] = mock_firebase
sys.modules["firebase_admin.firestore"] = mock_firestore
sys.modules["google.cloud"] = MagicMock()
sys.modules["google.cloud.firestore"] = MagicMock()

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.1"}
