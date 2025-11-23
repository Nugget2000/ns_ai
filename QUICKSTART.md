# Quick Start Guide

This guide will help you quickly deploy the NS AI application to Google Cloud Platform.

## Prerequisites Checklist

- [ ] Google Cloud account with billing enabled
- [ ] Project ID: `ns-ai-project`
- [ ] gcloud CLI installed and configured
- [ ] Terraform installed (>= 1.0)
- [ ] Docker installed

## Step 1: Authenticate with Google Cloud

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project ns-ai-project

# Set application default credentials for Terraform
gcloud auth application-default login
```

## Step 2: Enable Required APIs

```bash
gcloud services enable firestore.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

## Step 3: Deploy Infrastructure with Terraform

```bash
cd terraform

# Copy the example variables file
cp terraform.tfvars.example terraform.tfvars

# Review and edit terraform.tfvars if needed
# (Default values are already set for ns-ai-project in europe-north2)

# Initialize Terraform
terraform init

# Preview the changes
terraform plan

# Deploy the infrastructure
terraform apply
```

When prompted, type `yes` to confirm.

## Step 4: Build and Push Docker Images

From the root directory:

```bash
cd ..

# Authenticate Docker with Artifact Registry
gcloud auth configure-docker europe-north2-docker.pkg.dev

# Build and push all images using the helper script
./build-and-push.sh
```

Or manually:

```bash
# Build and push backend
cd backend
docker build -t europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest .
docker push europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest

# Build and push frontend
cd ../frontend
docker build -t europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest .
docker push europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest
```

## Step 5: Deploy to Cloud Run

```bash
# Deploy backend
gcloud run deploy ns-ai-backend \
  --image europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest \
  --region europe-north2

# Deploy frontend
gcloud run deploy ns-ai-frontend \
  --image europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest \
  --region europe-north2
```

Or use Terraform:

```bash
cd terraform
terraform apply
```

## Step 6: Access Your Application

After deployment, Terraform will output the URLs:

```bash
cd terraform
terraform output
```

You should see:
- `backend_url` - The URL for your backend API
- `frontend_url` - The URL for your frontend application

Visit the frontend URL in your browser to see your application!

## Updating the Application

When you make changes to your code:

```bash
# Rebuild and push images with a new tag (e.g., v1.1.0)
./build-and-push.sh v1.1.0

# Update Cloud Run services
gcloud run deploy ns-ai-backend \
  --image europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:v1.1.0 \
  --region europe-north2

gcloud run deploy ns-ai-frontend \
  --image europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:v1.1.0 \
  --region europe-north2
```

## Destroying Resources

To remove all resources (⚠️ **Warning**: This deletes everything!):

```bash
cd terraform
terraform destroy
```

## Troubleshooting

### "Permission denied" errors

Make sure you have the necessary IAM roles:
```bash
gcloud projects add-iam-policy-binding ns-ai-project \
  --member="user:YOUR_EMAIL@example.com" \
  --role="roles/editor"
```

### Docker push fails

Re-authenticate:
```bash
gcloud auth configure-docker europe-north2-docker.pkg.dev
```

### Cloud Run service won't start

Check the logs:
```bash
gcloud run services logs read ns-ai-backend --region europe-north2 --limit 50
```

## Additional Resources

- Full documentation: See [terraform/README.md](terraform/README.md)
- Backend documentation: See [backend/README.md](backend/README.md)
- Frontend documentation: See [frontend/README.md](frontend/README.md)

## Support

For issues or questions, please refer to the main [README.md](README.md) or file an issue on the project repository.
