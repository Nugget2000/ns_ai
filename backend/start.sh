#!/bin/bash

# --- IMPORTANT ---
# 1. Place your Google Cloud service account key file in this directory (the 'backend' directory).
# 2. Rename the key file to 'service-account-key.json'.
# -----------------

KEY_FILE="service-account-key.json"

if [ ! -f "$KEY_FILE" ]; then
    echo "Error: Service account key file not found at '$KEY_FILE'."
    echo "Please ensure 'service-account-key.json' is in the current directory."
    exit 1
fi

# Load .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Set Google Application Credentials
export GOOGLE_APPLICATION_CREDENTIALS=$(readlink -f "$KEY_FILE")

# Disable Cloud Logging for local development (matches podman.sh)
export ENABLE_CLOUD_LOGGING="False"

echo "Starting with credentials from: $GOOGLE_APPLICATION_CREDENTIALS"

./.venv/bin/uvicorn app.main:app --reload --port 8085
