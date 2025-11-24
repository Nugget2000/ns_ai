#!/bin/bash


# Build the Docker image
docker build -t frontend .

# Run the Docker container
# Using --network host so the container can access localhost:8080 (backend)
docker run --rm -it \
  --name frontend \
  --network host \
  frontend