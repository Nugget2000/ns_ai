
import logging
from datetime import datetime
from typing import Optional, List
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from ..models.schemas import UserCreate, UserUpdate, UserResponse, UserRole

db = firestore.client()
COLLECTION_NAME = "users"

class UserService:
    @staticmethod
    def get_user(uid: str) -> Optional[UserResponse]:
        doc_ref = db.collection(COLLECTION_NAME).document(uid)
        doc = doc_ref.get()
        if doc.exists:
            return UserResponse(**doc.to_dict())
        return None

    @staticmethod
    def create_user(user: UserCreate) -> UserResponse:
        doc_ref = db.collection(COLLECTION_NAME).document(user.uid)
        user_data = user.dict()
        user_data["created_at"] = datetime.utcnow()
        user_data["last_login"] = datetime.utcnow()
        doc_ref.set(user_data)
        return UserResponse(**user_data)

    @staticmethod
    def update_user(uid: str, updates: UserUpdate) -> Optional[UserResponse]:
        doc_ref = db.collection(COLLECTION_NAME).document(uid)
        doc = doc_ref.get()
        if not doc.exists:
            return None
        
        update_data = updates.dict(exclude_unset=True)
        if not update_data:
            return UserResponse(**doc.to_dict())

        doc_ref.update(update_data)
        
        # Fetch updated
        updated_doc = doc_ref.get()
        return UserResponse(**updated_doc.to_dict())

    @staticmethod
    def update_last_login(uid: str):
        doc_ref = db.collection(COLLECTION_NAME).document(uid)
        doc_ref.update({"last_login": datetime.utcnow()})

    @staticmethod
    def list_users() -> List[UserResponse]:
        users_ref = db.collection(COLLECTION_NAME)
        docs = users_ref.stream()
        return [UserResponse(**doc.to_dict()) for doc in docs]

    @staticmethod
    def get_or_create_user(uid: str, email: str) -> UserResponse:
        user = UserService.get_user(uid)
        if user:
            UserService.update_last_login(uid)
            return user
        else:
            new_user = UserCreate(uid=uid, email=email, role=UserRole.PENDING)
            return UserService.create_user(new_user)
