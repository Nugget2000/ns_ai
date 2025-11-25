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

# Load .env file if it exists
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY is not set. Please set it in .env or export it."
    exit 1
fi

# Build the Docker image
docker build -t backend .

# Run the Docker container
# This passes the key file content and GEMINI_API_KEY as environment variables.
# It also maps container port 8000 to host port 8080.
docker run --rm -it \
  --name backend \
  -p 8000:8000 \
  -e GOOGLE_CREDENTIALS_CONTENT="$KEY_CONTENT" \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  backend