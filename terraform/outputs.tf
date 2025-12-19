output "backend_url" {
  value = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  value = google_cloud_run_v2_service.frontend.uri
}

output "workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github_provider.name
}

data "google_firebase_web_app_config" "frontend" {
  provider   = google-beta
  web_app_id = google_firebase_web_app.frontend.app_id
}

output "firebase_config" {
  value = {
    apiKey            = data.google_firebase_web_app_config.frontend.api_key
    authDomain        = data.google_firebase_web_app_config.frontend.auth_domain
    projectId         = var.project_id
    storageBucket     = data.google_firebase_web_app_config.frontend.storage_bucket
    messagingSenderId = data.google_firebase_web_app_config.frontend.messaging_sender_id
    appId             = google_firebase_web_app.frontend.app_id
  }
}

output "domain_mapping_records" {
  value = google_cloud_run_domain_mapping.frontend.status[0].resource_records
}
