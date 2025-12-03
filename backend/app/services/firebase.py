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

def save_emanuel_prompt(prompt_text: str):
    """
    Saves the compiled Emanuel prompt to Firestore.
    """
    logging.info("Saving Emanuel prompt to Firestore")
    try:
        doc_ref = db.collection("ns_ai").document("emanuel_context")
        doc_ref.set({"prompt": prompt_text})
        logging.info("Successfully saved Emanuel prompt to Firestore")
    except Exception as e:
        logging.error(f"Error saving Emanuel prompt to Firestore: {e}")
        raise e

def get_emanuel_prompt() -> str:
    """
    Retrieves the Emanuel prompt from Firestore.
    Returns the prompt text or a default message if not found.
    """
    logging.info("Fetching Emanuel prompt from Firestore")
    try:
        doc_ref = db.collection("ns_ai").document("emanuel_context")
        snapshot = doc_ref.get()
        
        if snapshot.exists:
            prompt = snapshot.get("prompt")
            logging.info("Successfully fetched Emanuel prompt from Firestore")
            return prompt
        else:
            logging.warning("Emanuel prompt not found in Firestore, using default.")
            return "Your name is Emanuel and I will try to help. The answers are short and consise and always 100% correct, never lie or come up with answes."
            
    except Exception as e:
        logging.error(f"Error fetching Emanuel prompt from Firestore: {e}")
        # Return default on error to keep service running
        return "Your name is Emanuel and I will try to help. The answers are short and consise and always 100% correct, never lie or come up with answes."
