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



# Load .env file if it exists
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "Error: GEMINI_API_KEY is not set. Please set it in .env or export it."
    exit 1
fi

# Get absolute path to key file
ABS_KEY_FILE=$(readlink -f "$KEY_FILE")
echo "Mounting key file from: $ABS_KEY_FILE"

# Build the Docker image
docker build -t backend .

# Run the Docker container
# This mounts the key file into the container and sets GOOGLE_APPLICATION_CREDENTIALS.
# It also passes GEMINI_API_KEY as an environment variable.
# It maps container port 8000 to host port 8000.
# We override the default command to verify the file exists before starting the app.
# The :Z flag is used to relabel the file for SELinux compatibility.
# The --rm flag removes the container when it exits.
# The -it flag runs the container in interactive mode with a pseudo-TTY.

docker run --rm -it \
  --name backend \
  -p 8000:8000 \
  -v "$ABS_KEY_FILE":/app/service-account-key.json:Z \
  -e GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-key.json" \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  -e ENABLE_CLOUD_LOGGING="False" \
  backend \
  bash -c "if [ -f /app/service-account-key.json ]; then echo 'Key file found inside container.'; else echo 'ERROR: Key file NOT found inside container!'; ls -la /app; exit 1; fi; uvicorn app.main:app --host 0.0.0.0 --port 8000"