output "backend_url" {
  description = "URL of the backend Cloud Run service"
  value       = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  description = "URL of the frontend Cloud Run service"
  value       = google_cloud_run_v2_service.frontend.uri
}

output "artifact_registry_repository" {
  description = "Artifact Registry repository URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.ns_ai_repo.repository_id}"
}

output "firestore_database" {
  description = "Firestore database name"
  value       = google_firestore_database.database.name
}

output "backend_service_account" {
  description = "Backend service account email"
  value       = google_service_account.backend_sa.email
}

output "frontend_service_account" {
  description = "Frontend service account email"
  value       = google_service_account.frontend_sa.email
}

output "github_actions_service_account" {
  description = "GitHub Actions service account email"
  value       = google_service_account.github_actions_sa.email
}
