#!/bin/bash


# Load environment variables from .env if present
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Build the Podman image
podman build \
  --build-arg VITE_AUTH_PASSWORD="$VITE_AUTH_PASSWORD" \
  --build-arg VITE_FIREBASE_API_KEY="$VITE_FIREBASE_API_KEY" \
  --build-arg VITE_FIREBASE_AUTH_DOMAIN="$VITE_FIREBASE_AUTH_DOMAIN" \
  --build-arg VITE_FIREBASE_PROJECT_ID="$VITE_FIREBASE_PROJECT_ID" \
  --build-arg VITE_FIREBASE_STORAGE_BUCKET="$VITE_FIREBASE_STORAGE_BUCKET" \
  --build-arg VITE_FIREBASE_MESSAGING_SENDER_ID="$VITE_FIREBASE_MESSAGING_SENDER_ID" \
  --build-arg VITE_FIREBASE_APP_ID="$VITE_FIREBASE_APP_ID" \
  -t frontend .

# Run the Podman container
# Using --network host so the container can access localhost:8080 (backend)
podman run --rm -it \
  --name frontend \
  --network host \
  -e BACKEND_URL="http://localhost:8000" \
  -e NODE_ENV="development" \
  frontend
