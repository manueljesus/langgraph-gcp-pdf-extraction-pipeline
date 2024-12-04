resource "google_bigquery_dataset" "research_papers_dataset" {
  dataset_id = var.bigquery_dataset
  description = "Dataset to store research papers and related data"
}

resource "google_bigquery_table" "research_papers" {
  dataset_id = google_bigquery_dataset.research_papers_dataset.dataset_id
  table_id   = "research_papers"

  schema = <<EOF
[
  {
    "name": "id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "title",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "abstract",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "summary",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "methodology",
    "type": "STRING",
    "mode": "NULLABLE"
  },
  {
    "name": "publication_date",
    "type": "DATE",
    "mode": "NULLABLE"
  }
]
EOF
}

resource "google_bigquery_table" "authors" {
  dataset_id = google_bigquery_dataset.research_papers_dataset.dataset_id
  table_id   = "authors"

  schema = <<EOF
[
  {
    "name": "author_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "name",
    "type": "STRING",
    "mode": "REQUIRED"
  }
]
EOF
}

resource "google_bigquery_table" "authors_x_research_papers" {
  dataset_id = google_bigquery_dataset.research_papers_dataset.dataset_id
  table_id   = "authors_x_research_papers"

  schema = <<EOF
[
  {
    "name": "author_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "paper_id",
    "type": "STRING",
    "mode": "REQUIRED"
  }
]
EOF
}

resource "google_bigquery_table" "keywords" {
  dataset_id = google_bigquery_dataset.research_papers_dataset.dataset_id
  table_id   = "keywords"

  schema = <<EOF
[
  {
    "name": "keyword_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "keyword",
    "type": "STRING",
    "mode": "REQUIRED"
  }
]
EOF
}

resource "google_bigquery_table" "keywords_x_research_papers" {
  dataset_id = google_bigquery_dataset.research_papers_dataset.dataset_id
  table_id   = "keywords_x_research_papers"

  schema = <<EOF
[
  {
    "name": "keyword_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "paper_id",
    "type": "STRING",
    "mode": "REQUIRED"
  }
]
EOF
}

resource "google_bigquery_table" "key_research_findings" {
  dataset_id = google_bigquery_dataset.research_papers_dataset.dataset_id
  table_id   = "key_research_findings"

  schema = <<EOF
[
  {
    "name": "paper_id",
    "type": "STRING",
    "mode": "REQUIRED"
  },
  {
    "name": "finding",
    "type": "STRING",
    "mode": "REQUIRED"
  }
]
EOF
}
