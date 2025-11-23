#!/bin/bash

# Build and push Docker images to Artifact Registry

set -e  # Exit on error

PROJECT_ID="ns-ai-project"
REGION="europe-north2"
REGISTRY="${REGION}-docker.pkg.dev"
REPO="${REGISTRY}/${PROJECT_ID}/ns-ai-repo"

# Default tag
TAG="${1:-latest}"

echo "🐋 NS AI Docker Build & Push Script"
echo "===================================="
echo "Tag: ${TAG}"
echo ""

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    exit 1
fi

# Authenticate Docker
echo "🔐 Authenticating Docker with Artifact Registry..."
gcloud auth configure-docker ${REGISTRY}

# Build and push backend
echo ""
echo "🔨 Building backend image..."
cd backend
docker build -t ${REPO}/backend:${TAG} -t ${REPO}/backend:latest .

echo "📤 Pushing backend image..."
docker push ${REPO}/backend:${TAG}
if [ "$TAG" != "latest" ]; then
    docker push ${REPO}/backend:latest
fi

cd ..

# Build and push frontend
echo ""
echo "🔨 Building frontend image..."
cd frontend
docker build -t ${REPO}/frontend:${TAG} -t ${REPO}/frontend:latest .

echo "📤 Pushing frontend image..."
docker push ${REPO}/frontend:${TAG}
if [ "$TAG" != "latest" ]; then
    docker push ${REPO}/frontend:latest
fi

cd ..

echo ""
echo "✅ All images built and pushed successfully!"
echo ""
echo "Images:"
echo "  Backend:  ${REPO}/backend:${TAG}"
echo "  Frontend: ${REPO}/frontend:${TAG}"
echo ""
echo "To deploy to Cloud Run:"
echo "  gcloud run deploy ns-ai-backend --image ${REPO}/backend:${TAG} --region ${REGION}"
echo "  gcloud run deploy ns-ai-frontend --image ${REPO}/frontend:${TAG} --region ${REGION}"
echo ""
