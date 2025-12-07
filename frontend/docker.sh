#!/bin/bash


# Load environment variables from .env if present
if [ -f .env ]; then
  set -a
  source .env
  set +a
fi

# Build the Docker image
docker build \
  --build-arg VITE_AUTH_PASSWORD="$VITE_AUTH_PASSWORD" \
  -t frontend .

# Run the Docker container
# Using --network host so the container can access localhost:8080 (backend)
docker run --rm -it \
  --name frontend \
  --network host \
  -e BACKEND_URL="http://localhost:8000" \
  frontend