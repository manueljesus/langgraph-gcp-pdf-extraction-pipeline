variable "bucket_name" {
  description = "Base name for the GCS bucket"
  type        = string
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for the GCS bucket"
  type        = string
}
