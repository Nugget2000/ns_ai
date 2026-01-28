#!/usr/bin/env bash
# Load .env file from backend directory if it exists
if [ -f backend/.env ]; then
  echo "Loading environment variables from backend/.env"
  export $(grep -v '^#' backend/.env | xargs)
fi

source backend/.venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
python3 -m app.services.nightscout_service

