variable "function_name" {
  description = "The name of the cloud function"
  type        = string
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "Region for the Cloud Function"
  type        = string
}

variable "dataset_name" {
  description = "BigQuery dataset name"
  type        = string
}

variable "bucket_name" {
  description = "GCS bucket name for the trigger"
  type        = string
}

variable "function_archive_object" {
  description = "The storage object created in the storage module"
}
