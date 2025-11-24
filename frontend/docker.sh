#!/bin/bash


# Build the Docker image
docker build -t frontend .

# Run the Docker container
docker run --rm -it \
  --name frontend \
  -p 80:5173 \
  frontend