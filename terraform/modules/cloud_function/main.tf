resource "google_cloudfunctions2_function" "file_finalize_function" {
  name     = var.function_name
  location = var.region

  build_config {
    runtime     = "python312"
    entry_point = "hello_world"
    source {
      storage_source {
        bucket = var.bucket_name
        object = "main.zip"
      }
    }
  }

  service_config {
    available_memory = "512Mi"
    timeout_seconds  = 60
  }

  event_trigger {
    event_type = "google.cloud.storage.object.v1.finalized"
    event_filters {
      attribute = "bucket"
      value     = var.bucket_name
    }
  }

  depends_on = [var.function_archive_object]
}