# Terraform Infrastructure for NS AI

This directory contains Terraform configuration files to manage the Google Cloud Platform infrastructure for the NS AI application.

## Prerequisites

1. **Terraform**: Install Terraform (>= 1.0)
   ```bash
   # On Ubuntu/Debian
   wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform
   
   # On macOS
   brew install terraform
   ```

2. **Google Cloud SDK**: Install and configure gcloud CLI
   ```bash
   # Install gcloud CLI
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   
   # Initialize and authenticate
   gcloud init
   gcloud auth application-default login
   ```

3. **GCP Project**: Ensure you have a GCP project with billing enabled
   - Project ID: `ns-ai-project`
   - Region: `europe-north2`

## Infrastructure Overview

The Terraform configuration creates the following resources:

- **Firestore Database**: Native mode database for application data
- **Artifact Registry**: Docker repository for container images
- **Cloud Run Services**:
  - Backend service (FastAPI application)
  - Frontend service (React application)
- **Service Accounts**: Separate service accounts for backend and frontend
- **IAM Permissions**: Firestore access for backend service

## Initial Setup

1. **Navigate to the terraform directory**:
   ```bash
   cd terraform
   ```

2. **Create your variables file**:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
   
   The default values are already configured for your project, but you can customize them if needed.

3. **Enable required APIs** (if not already enabled):
   ```bash
   gcloud config set project ns-ai-project
   gcloud services enable firestore.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable artifactregistry.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

4. **Initialize Terraform**:
   ```bash
   terraform init
   ```

## Deployment Workflow

### 1. Preview Changes

Always review what Terraform will create before applying:

```bash
terraform plan
```

### 2. Apply Infrastructure

Create the infrastructure:

```bash
terraform apply
```

Type `yes` when prompted to confirm.

After successful deployment, Terraform will output important URLs and resource information.

### 3. View Outputs

To see the outputs again later:

```bash
terraform output
```

## Building and Deploying Docker Images

After the infrastructure is created, you need to build and push your Docker images.

### Authenticate Docker with Artifact Registry

```bash
gcloud auth configure-docker europe-north2-docker.pkg.dev
```

### Build and Push Backend

```bash
cd ../backend
docker build -t europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest .
docker push europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest
```

### Build and Push Frontend

First, you may need to create a production Dockerfile for the frontend. Here's an example:

```dockerfile
# Create frontend/Dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Then build and push:

```bash
cd ../frontend
docker build -t europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest .
docker push europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest
```

### Deploy Updated Images

After pushing new images, Cloud Run will automatically redeploy if you're using the `latest` tag. Otherwise, you can trigger a deployment:

```bash
gcloud run deploy ns-ai-backend \
  --image europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest \
  --region europe-north2

gcloud run deploy ns-ai-frontend \
  --image europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest \
  --region europe-north2
```

Or simply run `terraform apply` again to update the services with the latest images.

## Updating Infrastructure

To modify the infrastructure:

1. Edit the Terraform files (`main.tf`, `variables.tf`, etc.)
2. Preview changes: `terraform plan`
3. Apply changes: `terraform apply`

## Destroying Resources

To remove all created resources:

```bash
terraform destroy
```

> **Warning**: This will delete all resources including the Firestore database. Make sure to backup any important data first.

## Common Operations

### View Current State

```bash
terraform show
```

### List All Resources

```bash
terraform state list
```

### Check Backend Service Logs

```bash
gcloud run services logs read ns-ai-backend --region europe-north2 --limit 50
```

### Check Frontend Service Logs

```bash
gcloud run services logs read ns-ai-frontend --region europe-north2 --limit 50
```

### Update Environment Variables

Edit the `env` blocks in `main.tf` under the respective Cloud Run services, then:

```bash
terraform apply
```

## Troubleshooting

### Issue: "API not enabled"

**Solution**: Enable the required API:
```bash
gcloud services enable <api-name>
```

### Issue: "Permission denied"

**Solution**: Ensure you have the necessary IAM roles:
- `roles/editor` or `roles/owner` for the project
- Or specific roles: `roles/run.admin`, `roles/artifactregistry.admin`, `roles/datastore.owner`

### Issue: Docker push fails

**Solution**: Re-authenticate:
```bash
gcloud auth configure-docker europe-north2-docker.pkg.dev
```

### Issue: Cloud Run service not starting

**Solution**: Check logs for errors:
```bash
gcloud run services logs read <service-name> --region europe-north2
```

Common issues:
- Container port mismatch (ensure backend uses port 8000, frontend uses port 80)
- Missing environment variables
- Image not found (verify push was successful)

## Security Considerations

### Current Configuration

The current setup allows **unauthenticated access** to both Cloud Run services (`allUsers` invoker role). This is suitable for a public-facing application.

### Restricting Access

To require authentication, remove or comment out these resources in `main.tf`:

```hcl
# resource "google_cloud_run_v2_service_iam_member" "backend_noauth" { ... }
# resource "google_cloud_run_v2_service_iam_member" "frontend_noauth" { ... }
```

Then grant specific users/service accounts access:

```hcl
resource "google_cloud_run_v2_service_iam_member" "backend_auth" {
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "user:your-email@example.com"
}
```

### Firestore Security Rules

Configure Firestore security rules through the Firebase Console or using Terraform with the `google_firebaserules_ruleset` resource.

## Cost Optimization

### Tips to Minimize Costs

1. **Use minimum instances = 0**: Allows Cloud Run to scale to zero when not in use (already configured)
2. **Set appropriate memory limits**: Current config uses 512Mi, adjust based on actual usage
3. **Monitor usage**: Use GCP's cost management tools
4. **Delete unused resources**: Run `terraform destroy` when not needed

### Estimated Costs

With the current configuration (scale to zero enabled):
- **Firestore**: Pay per read/write/delete operations and storage
- **Cloud Run**: Pay only when requests are being processed
- **Artifact Registry**: ~$0.10/GB/month for storage

With minimal traffic, monthly costs should be under $5 USD.

## Additional Resources

- [Terraform Google Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Firestore Documentation](https://cloud.google.com/firestore/docs)
- [Artifact Registry Documentation](https://cloud.google.com/artifact-registry/docs)
