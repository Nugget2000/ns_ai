#!/bin/sh
export BACKEND_URL="http://localhost:8085"
if [ "$NODE_ENV" = "development" ]; then
  echo "Starting in development mode..."
  npm run dev
else
  echo "Starting in production mode..."
  node server.js
fi