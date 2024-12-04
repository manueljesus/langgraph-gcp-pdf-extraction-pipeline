variable "project_id" {
  description = "The GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for resources"
  type        = string
  default     = "us-central1"
}

variable "bucket_name" {
  description = "Base name for the GCS bucket"
  type        = string
}
