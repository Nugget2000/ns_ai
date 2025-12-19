variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "ns-ai-project"
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "europe-north1"
}

variable "backend_image" {
  description = "Docker image for the backend service"
  type        = string
  default     = "europe-north1-docker.pkg.dev/ns-ai-project/ns-ai-repo/backend:latest"
}

variable "frontend_image" {
  description = "Docker image for the frontend service"
  type        = string
  default     = "europe-north1-docker.pkg.dev/ns-ai-project/ns-ai-repo/frontend:latest"
}

variable "backend_min_instances" {
  description = "Minimum number of backend instances"
  type        = number
  default     = 0
}

variable "backend_max_instances" {
  description = "Maximum number of backend instances"
  type        = number
  default     = 1
}

variable "frontend_min_instances" {
  description = "Minimum number of frontend instances"
  type        = number
  default     = 0
}

variable "frontend_max_instances" {
  description = "Maximum number of frontend instances"
  type        = number
  default     = 1
}

variable "domain_name" {
  description = "The custom domain name for the frontend"
  type        = string
  default     = "nsai.cucumba.se"
}
