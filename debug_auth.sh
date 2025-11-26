#!/bin/bash

# Path to the key file
KEY_FILE="terraform/key.json"
PROJECT_ID="ns-ai-project"
REGION="europe-north2"
REPO="ns-ai-repo"

if [ ! -f "$KEY_FILE" ]; then
    echo "Error: Key file $KEY_FILE not found."
    exit 1
fi

echo "Authenticating with service account..."
gcloud auth activate-service-account --key-file="$KEY_FILE"

if [ $? -ne 0 ]; then
    echo "Authentication failed."
    exit 1
fi

echo "Authentication successful."

echo "Verifying access to repository $REPO..."
gcloud artifacts repositories describe "$REPO" --project="$PROJECT_ID" --location="$REGION"

if [ $? -ne 0 ]; then
    echo "Repository $REPO not found or access denied."
    echo "Attempting to check IAM policy for the repository..."
    gcloud artifacts repositories get-iam-policy "$REPO" --project="$PROJECT_ID" --location="$REGION"
    exit 1
else
    echo "Repository $REPO found and accessible."
    echo "The key in $KEY_FILE is valid and has access to the repository."
    echo "Please ensure the content of $KEY_FILE matches the GCP_SA_KEY secret in GitHub."
fi
