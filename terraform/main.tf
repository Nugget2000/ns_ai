terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

data "google_project" "project" {}

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

resource "google_project_service" "secret_manager" {
  service            = "secretmanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam_credentials" {
  service            = "iamcredentials.googleapis.com"
  disable_on_destroy = false
}

# Firebase APIs
resource "google_project_service" "firebase" {
  provider           = google-beta
  service            = "firebase.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "identitytoolkit" {
  provider           = google-beta
  service            = "identitytoolkit.googleapis.com"
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

# Firebase Project
resource "google_firebase_project" "default" {
  provider = google-beta
  project  = var.project_id

  depends_on = [
    google_project_service.firebase,
    google_project_service.identitytoolkit
  ]
}

# Firebase Web App
resource "google_firebase_web_app" "frontend" {
  provider     = google-beta
  project      = var.project_id
  display_name = "NS AI Frontend"

  depends_on = [google_firebase_project.default]
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

      env {
        name = "GEMINI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.gemini_api_key.secret_id
            version = "latest"
          }
        }
      }
    }
  }

  depends_on = [
    google_project_service.run,
    google_project_service.secret_manager,
    google_firestore_database.database
  ]
}

# Secret Manager Secret for Gemini API Key
resource "google_secret_manager_secret" "gemini_api_key" {
  secret_id = "gemini-api-key"

  replication {
    auto {}
  }

  depends_on = [google_project_service.secret_manager]
}

# New Secrets for Frontend Build
resource "google_secret_manager_secret" "api_base_url" {
  secret_id = "api-base-url"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "vite_auth_password" {
  secret_id = "vite-auth-password"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "vite_firebase_api_key" {
  secret_id = "vite-firebase-api-key"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "vite_firebase_auth_domain" {
  secret_id = "vite-firebase-auth-domain"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "vite_firebase_project_id" {
  secret_id = "vite-firebase-project-id"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "vite_firebase_storage_bucket" {
  secret_id = "vite-firebase-storage-bucket"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "vite_firebase_messaging_sender_id" {
  secret_id = "vite-firebase-messaging-sender-id"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "vite_firebase_app_id" {
  secret_id = "vite-firebase-app-id"
  replication {
    auto {}
  }
}

# Grant Secret Manager Secret Accessor role to backend service account
resource "google_secret_manager_secret_iam_member" "backend_secret_accessor" {
  project   = var.project_id
  secret_id = google_secret_manager_secret.gemini_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend_sa.email}"
}

# Grant Secret Manager Secret Accessor role to GitHub Actions SA for all secrets
resource "google_project_iam_member" "github_actions_secret_accessor" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.github_actions_sa.email}"
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

# Workload Identity Federation for GitHub Actions
resource "google_iam_workload_identity_pool" "github_pool" {
  workload_identity_pool_id = "github-actions-pool-unique"
  display_name              = "GitHub Actions Pool"
  description               = "Workload Identity Pool for GitHub Actions"
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-actions-provider"
  display_name                       = "GitHub Actions Provider"
  description                        = "Workload Identity Pool Provider for GitHub Actions"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.actor"      = "assertion.actor"
  }
  attribute_condition = "assertion.repository == 'per-svensson/ns_ai'"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# Allow GitHub Actions to impersonate the Service Account
resource "google_service_account_iam_member" "github_actions_sa_impersonation" {
  service_account_id = google_service_account.github_actions_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/per-svensson/ns_ai"
}

# Domain Mapping for Frontend
resource "google_cloud_run_domain_mapping" "frontend" {
  location = var.region
  name     = var.domain_name

  metadata {
    namespace = var.project_id
  }

  spec {
    route_name = google_cloud_run_v2_service.frontend.name
  }
}
