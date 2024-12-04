resource "google_storage_bucket" "event_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true
}
