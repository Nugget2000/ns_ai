#!/bin/bash

# Deployment script for NS AI infrastructure

set -e  # Exit on error

PROJECT_ID="ns-ai-project"
REGION="europe-north2"
BACKEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/ns-ai-repo/backend"
FRONTEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/ns-ai-repo/frontend"

echo "🚀 NS AI Deployment Script"
echo "=========================="
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Error: Terraform is not installed"
    echo "Install it from: https://www.terraform.io/downloads"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Install it from: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ All required tools are installed"
echo ""

# Set the project
echo "📋 Setting GCP project..."
gcloud config set project $PROJECT_ID

# Authenticate Docker
echo "🔐 Authenticating Docker with Artifact Registry..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Navigate to terraform directory
cd terraform

# Check if terraform.tfvars exists
if [ ! -f terraform.tfvars ]; then
    echo "📝 Creating terraform.tfvars from example..."
    cp terraform.tfvars.example terraform.tfvars
    echo "⚠️  Please review terraform.tfvars and update if needed"
fi

# Initialize Terraform
echo "🔧 Initializing Terraform..."
terraform init

# Apply Terraform configuration
echo "📦 Deploying infrastructure..."
terraform apply

echo ""
echo "✅ Infrastructure deployed successfully!"
echo ""

# Get outputs
echo "📊 Deployment Information:"
terraform output

echo ""
echo "Next steps:"
echo "1. Build and push Docker images:"
echo "   cd ../backend && docker build -t ${BACKEND_IMAGE}:latest . && docker push ${BACKEND_IMAGE}:latest"
echo "   cd ../frontend && docker build -t ${FRONTEND_IMAGE}:latest . && docker push ${FRONTEND_IMAGE}:latest"
echo ""
echo "2. Update Cloud Run services:"
echo "   gcloud run deploy ns-ai-backend --image ${BACKEND_IMAGE}:latest --region ${REGION}"
echo "   gcloud run deploy ns-ai-frontend --image ${FRONTEND_IMAGE}:latest --region ${REGION}"
echo ""
