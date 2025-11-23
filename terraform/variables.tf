variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "europe-north2"
}

variable "backend_image" {
  description = "Docker image for the backend service"
  type        = string
  default     = "europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest"
}

variable "frontend_image" {
  description = "Docker image for the frontend service"
  type        = string
  default     = "europe-north2-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest"
}

variable "backend_min_instances" {
  description = "Minimum number of backend instances"
  type        = number
  default     = 0
}

variable "backend_max_instances" {
  description = "Maximum number of backend instances"
  type        = number
  default     = 2
}

variable "frontend_min_instances" {
  description = "Minimum number of frontend instances"
  type        = number
  default     = 0
}

variable "frontend_max_instances" {
  description = "Maximum number of frontend instances"
  type        = number
  default     = 2
}
