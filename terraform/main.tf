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
