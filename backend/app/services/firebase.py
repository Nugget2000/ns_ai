import logging
from google.cloud import firestore
from app.core.config import settings

# Initialize Firestore
if settings.GOOGLE_APPLICATION_CREDENTIALS:
    logging.info(
        "Initializing Firestore with service account from GOOGLE_APPLICATION_CREDENTIALS"
    )
else:
    logging.warning(
        "GOOGLE_APPLICATION_CREDENTIALS not set. "
        "Using Application Default Credentials (ADC). "
        "This is recommended for local development only."
    )

db = firestore.AsyncClient()

async def increment_visitor_count() -> int:
    """
    Retrieves the current page load count from Firestore,
    increments it by one, and returns the new count.
    """
    logging.info("Incrementing visitor count")

    try:
        # Reference to the visitor counter document
        doc_ref = db.collection("ns_ai").document("visitor_counter")

        @firestore.async_transactional
        async def increment_counter(transaction):
            snapshot = await doc_ref.get(transaction=transaction)

            # If the document exists but 'count' is missing or None, treat it as 0
            if snapshot.exists:
                current_count = snapshot.get("count") or 0
            else:
                current_count = 0

            new_count = current_count + 1
            transaction.set(doc_ref, {"count": new_count})
            return new_count

        # Execute the transaction
        transaction = db.transaction()
        count = await increment_counter(transaction)

        return count
    except Exception as e:
        logging.error(f"Error incrementing visitor count: {str(e)}")
        logging.exception(e)
        # Raise instead of returning None so callers (and FastAPI routes)
        # can handle the error and avoid returning an invalid response
        raise