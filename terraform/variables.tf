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

variable "bigquery_dataset" {
  description = "The BigQuery dataset name"
  type        = string
}

variable "function_name" {
  description = "The name of the cloud function"
  type        = string
}

