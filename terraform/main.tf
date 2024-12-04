module "storage" {
  source      = "./modules/storage"
  bucket_name = "${var.bucket_name}-${var.project_id}"
  project_id  = var.project_id
  region      = var.region
}

module "bigquery" {
  source          = "./modules/bigquery"
  project_id      = var.project_id
  bigquery_dataset = var.bigquery_dataset
}

module "cloud_function" {
  source        = "./modules/cloud_function"
  function_name = var.function_name
  project_id    = var.project_id
  region        = var.region
  dataset_name  = var.bigquery_dataset
  bucket_name   = "${var.bucket_name}-${var.project_id}"

  # Pass the output from the storage module
  function_archive_object = module.storage.function_archive_object
}
