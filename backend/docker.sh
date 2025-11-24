#!/bin/bash

# --- IMPORTANT ---
# 1. Place your Google Cloud service account key file in this directory (the 'backend' directory).
# 2. Rename the key file to 'service-account-key.json'.
# 3. IMPORTANT: 'service-account-key.json' has been added to .gitignore to prevent committing secrets.
# -----------------

KEY_FILE="service-account-key.json"

if [ ! -f "$KEY_FILE" ]; then
    echo "Error: Service account key file not found at '$KEY_FILE'."
    echo "Please follow the instructions at the top of this script."
    exit 1
fi

# Read the key file content
KEY_CONTENT=$(cat "$KEY_FILE")

# Build the Docker image
docker build -t backend .

# Run the Docker container
# This passes the key file content and GEMINI_API_KEY as environment variables.
# It also maps container port 8000 to host port 8080.
docker run --rm -it \
  --name backend \
  -p 8080:8000 \
  -e GOOGLE_CREDENTIALS_CONTENT="$KEY_CONTENT" \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  backend