import os
import json
import base64
import logging
import traceback
import firebase_admin
from fastapi import HTTPException
from firebase_admin import credentials, firestore


# Initialize Firebase
# This uses Application Default Credentials (ADC) automatically.
# It will look for GOOGLE_APPLICATION_CREDENTIALS env var or metadata server.
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

async def increment_visitor_count() -> int:
    """
    Retrieves the current page load count from Firestore,
    increments it by one, and returns the new count.
    """
    logging.info("Incrementing visitor count")
    # Reference to the visitor counter document
    doc_ref = db.collection("ns_ai").document("visitor_counter")

    # Use a transaction to ensure atomic read-increment-write
    @firestore.transactional
    def increment_counter(transaction):
        snapshot = doc_ref.get(transaction=transaction)

        if snapshot.exists:
            current_count = snapshot.get("count")
        else:
            current_count = 0

        new_count = current_count + 1
        transaction.set(doc_ref, {"count": new_count})
        return new_count

    try:
        # Execute the transaction
        transaction = db.transaction()
        count = increment_counter(transaction)
        return count
    except Exception as e:


        logging.error(f"Error incrementing visitor count: {e}")
        logging.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
