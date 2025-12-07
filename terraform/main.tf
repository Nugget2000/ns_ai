terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "firestore" {
  service            = "firestore.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "run" {
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifact_registry" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloud_build" {
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

# Artifact Registry Repository for Docker images
resource "google_artifact_registry_repository" "ns_ai_repo" {
  location      = var.region
  repository_id = "ns-ai-repo"
  description   = "Docker repository for NS AI application"
  format        = "DOCKER"

  depends_on = [google_project_service.artifact_registry]
}

# Firestore Database
resource "google_firestore_database" "database" {
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  # Prevent accidental deletion
  deletion_policy = "DELETE"

  depends_on = [google_project_service.firestore]
}

# Service Account for Backend Cloud Run
resource "google_service_account" "backend_sa" {
  account_id   = "ns-ai-backend"
  display_name = "NS AI Backend Service Account"
  description  = "Service account for NS AI backend Cloud Run service"
}

# Service Account for Frontend Cloud Run
resource "google_service_account" "frontend_sa" {
  account_id   = "ns-ai-frontend"
  display_name = "NS AI Frontend Service Account"
  description  = "Service account for NS AI frontend Cloud Run service"
}

# Grant Firestore access to backend service account
resource "google_project_iam_member" "backend_firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.backend_sa.email}"
}

# Cloud Run Service - Backend
resource "google_cloud_run_v2_service" "backend" {
  name     = "ns-ai-backend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.backend_sa.email

    scaling {
      min_instance_count = var.backend_min_instances
      max_instance_count = var.backend_max_instances
    }

    containers {
      image = var.backend_image

      ports {
        container_port = 8000
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }

      env {
        name  = "PROJECT_ID"
        value = var.project_id
      }

      env {
        name  = "ENVIRONMENT"
        value = "production"
      }
    }
  }

  depends_on = [
    google_project_service.run,
    google_firestore_database.database
  ]
}

# Cloud Run Service - Frontend
resource "google_cloud_run_v2_service" "frontend" {
  name     = "ns-ai-frontend"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.frontend_sa.email

    scaling {
      min_instance_count = var.frontend_min_instances
      max_instance_count = var.frontend_max_instances
    }

    containers {
      image = var.frontend_image

      ports {
        container_port = 80
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
        cpu_idle = true
      }

      env {
        name  = "BACKEND_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }

  depends_on = [
    google_project_service.run,
    google_cloud_run_v2_service.backend
  ]
}

# IAM policy to allow frontend service account to access backend
resource "google_cloud_run_v2_service_iam_member" "backend_frontend_access" {
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.frontend_sa.email}"
}

# IAM policy to allow unauthenticated access to frontend (adjust as needed)
resource "google_cloud_run_v2_service_iam_member" "frontend_noauth" {
  location = google_cloud_run_v2_service.frontend.location
  name     = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# IAM policy to allow unauthenticated access to backend (required for client-side calls)
resource "google_cloud_run_v2_service_iam_member" "backend_noauth" {
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Service Account for GitHub Actions
resource "google_service_account" "github_actions_sa" {
  account_id   = "github-actions-sa"
  display_name = "GitHub Actions Service Account"
  description  = "Service account for GitHub Actions CI/CD pipeline"
}

# Grant Artifact Registry Writer role to GitHub Actions SA
resource "google_artifact_registry_repository_iam_member" "github_actions_artifact_writer" {
  project    = var.project_id
  location   = google_artifact_registry_repository.ns_ai_repo.location
  repository = google_artifact_registry_repository.ns_ai_repo.name
  role       = "roles/artifactregistry.writer"
  member     = "serviceAccount:${google_service_account.github_actions_sa.email}"
}

# Grant Cloud Run Admin role to GitHub Actions SA
resource "google_project_iam_member" "github_actions_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.github_actions_sa.email}"
}

# Grant Service Account User role to GitHub Actions SA (to act as runtime SAs)
resource "google_project_iam_member" "github_actions_sa_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.github_actions_sa.email}"
}
