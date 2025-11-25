import logging
import google.cloud.logging
from app.core.config import settings

def setup_logging():
    """
    Configures logging for the application.
    If ENABLE_CLOUD_LOGGING is True, sets up Google Cloud Logging.
    Otherwise, configures standard logging to stdout.
    """
    if settings.ENABLE_CLOUD_LOGGING:
        try:
            client = google.cloud.logging.Client()
            client.setup_logging()
            logging.info("Google Cloud Logging enabled")
        except Exception as e:
            logging.basicConfig(level=logging.INFO)
            logging.error(f"Failed to setup Google Cloud Logging: {e}")
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logging.info("Standard logging enabled")
