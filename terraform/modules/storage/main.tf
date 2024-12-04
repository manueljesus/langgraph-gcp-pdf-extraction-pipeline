resource "google_storage_bucket" "event_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true
}

# Use the same bucket to upload a hello world function.
# This is needed to successfully create a Cloud Function via Terraform.

resource "google_storage_bucket_object" "function_archive" {
  name   = "main.zip"
  bucket = google_storage_bucket.event_bucket.name
  source = data.archive_file.function_archive.output_path
}

data "archive_file" "function_archive" {
  type        = "zip"
  source_dir  = "./template_function"
  output_path = "main.zip"
}