#!/bin/bash

# This script exports variables from the .env file into the current shell session.
# It must be sourced to affect the current shell: source export_env.sh

if [ -f .env ]; then
    # Export all variables defined in .env
    set -a
    source .env
    set +a
    echo "Variables from .env have been exported."
else
    echo "Error: .env file not found."
fi
