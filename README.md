# LLM-based Academic Research Paper Processing LangGraph pipeline

[![pipeline-unit-tests](https://github.com/manueljesus/langgraph-gcp-pdf-extraction-pipeline/actions/workflows/pipeline-unit-tests.yml/badge.svg)](https://github.com/manueljesus/langgraph-gcp-pdf-extraction-pipeline/actions/workflows/pipeline-unit-tests.yml)
[![pipeline-deployment](https://github.com/manueljesus/langgraph-gcp-pdf-extraction-pipeline/actions/workflows/pipeline-deployment.yml/badge.svg)](https://github.com/manueljesus/langgraph-gcp-pdf-extraction-pipeline/actions/workflows/pipeline-deployment.yml)

This project is a scalable, cloud-native pipeline for processing academic research papers.
It demonstrates the integration of **LangGraph**, **Large Language Models (LLMs)**, and **Google Cloud Platform (GCP)** to extract and structure key information from academic PDFs and store the results in **BigQuery** for further analysis.

## Features

- **Document Ingestion:**
  - Accepts academic research papers in PDF format.
  - Preserves structural integrity during ingestion.

- **Information Extraction:**
  - Extracts metadata: title, authors, publication date, and abstract.
  - Identifies key research findings and methodologies.
  - Generates structured summaries and extracts keywords.

- **Data Storage:**
  - Stores extracted data in BigQuery tables with a robust schema for analysis.
  - Handles many-to-many relationships between authors, keywords, and research papers.

- **Cloud-Native Design:**
  - Event-driven pipeline triggered by Google Cloud Storage (GCS) events.
  - Deployed as a serverless Google Cloud Function.

## Pipeline overview

The processing pipeline uses a **LangGraph StateGraph** to orchestrate tasks, ensuring modular and scalable execution. Below is an overview of the pipeline:

1. **Get File:** Retrieve the uploaded PDF file from the configured GCS bucket.
2. **Check Processed Paper:** Check if the document has already been processed by querying BigQuery.
   - If the document exists, the pipeline terminates.
   - If not, the pipeline proceeds to the next steps.
3. **Load PDF:** Extract raw text from the PDF using the `pdfplumber` library.
4. **Information Extraction:** Parallel extraction tasks:
   - Metadata (title, authors, abstract...)
   - Key research findings and methodologies
   - Structured summaries and keywords
5. **Merge Results:** Combine extracted data into a unified format.
6. **Insert Data Into BigQuery:** Save structured data into pre-configured BigQuery tables.

![Pipeline Diagram](https://github.com/user-attachments/assets/915ec689-d872-4f10-bf43-4694f7cf7c1b)

## Infrastructure

This project uses **Terraform** for infrastructure setup and GitHub Actions for CI/CD.
See [Deploy the infrastructure: IaC deployment (Terraform)](#deploy-the-infrastructure-iac-deployment-terraform) for instructions on how to deploy it



### Infrastructure Overview

- **Google Cloud Storage (GCS):**
  - A GCS bucket serves as the event trigger for the pipeline.
  - Stores incoming files and Cloud Function code.

- **BigQuery:**
  - Configured with the following tables:
    - `research_papers`: Core paper details.
    - `authors`: Author metadata.
    - `authors_x_research_papers`: Many-to-many relationships between authors and papers.
    - `keywords`: Extracted keywords.
    - `keywords_x_research_papers`: Many-to-many relationships between keywords and papers.
    - `key_research_findings`: Key insights from research papers.

- **Google Cloud Function:**
  - Serverless function triggered by `google.storage.object.finalize` events.
  - Processes PDF files and inserts structured data into BigQuery.

### CI/CD Workflow

Two GitHub Actions automate testing and deployment:

1. **pipeline-unit-tests:** Runs the pipeline’s test suite.
2. **pipeline-deployment:** Deploys the pipeline to Google Cloud Platform.

## Development and deployment

### Prerequisites

- Docker and Docker Compose
- Terraform

### Setup

#### Google Cloud Platform

You will need a project set up and a Service account with the following roles granted:

- Pipeline deployment from GH actions and local testing:
  - BigQuery Data Editor
  - Cloud Functions Admin
  - Cloud Run Admin
  - Service Account User
  - Storage Admin

- Terraform IaC deployment:
  - BigQuery Job User
  - Cloud Functions Developer
  - Cloud Run Admin
  - Service Account User
  - Storage Object Admin

It's your choice to create separated accounts (recommended: least privilege enforcement) or just one for an easy setup.

#### Pipeline

1. Generate and download a `.json` credentials file to access the pipeline-configured Service Account.
2. Create a `pipeline/.env` file with your own configuration, use the `pipeline/.env.example` file as a template.
3. Build and launch the Docker container:

    ```bash
    docker-compose build
    ```

    ```bash
    docker-compose up -d
    ```

4. Run the test suite:

    ```bash
    pytest
    ```

#### Deploy the infrastructure: IaC deployment (Terraform)

To deploy the needed infrastructure: Google Cloud Storage Container, Google Cloud Function and BigQuery dataset with the designed schema, follow these steps:

1. Generate and download a `.json` credentials file to access the terraform-configured Service Account.

2. Create a `terraform/terraform.tfvars` file with your own configuration. Use the `terraform/terraform.tfvars.example` as a template.

3. Set the path of your `.json` credentials file as evironment variable, or prepend it in each of the following commands:

    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS=<your-credentials-file>.json
    ```

4. Init terraform, validate your changes, build the plan and apply it:


    ```bash
    terraform init
    ```

    ```bash
    terraform validate
    ```

    ```bash
    terraform plan -out=plan.out
    ```

    ```bash
    terraform apply plan.out
    ```

#### CI/CD configuration for deployment.

The `pipeline-deployment` GitHub action relies in certain secrets and environment variables that need to be configured in the repository in order to be able to deploy the project as expectede:

##### Secrets

- `GOOGLE_APPLICATION_CREDENTIALS`: This secret needs to have the value of your pipeline service account `.json` credentials file.

    Add it under Settings > Secrets and variables > Actions > Secrets. 

##### Variables

- `VERTEX_AI_LLAMA_MODEL`
- `BIGQUERY_DATASET_ID`
- `GOOGLE_STORAGE_BUCKET_NAME`
- `GOOGLE_CLOUD_FUNCTION_NAME`

    Add them under Settings > Secrets and variables > Actions > Variables.

Their values are the same you defined in your `pipeline/.env` and `terraform/terraform.tfvars` files.

Once you have configured the required variables, *always after deploying the infrastructure*, you can manually-deploy the solution to your Google Cloud Platform project by running the `pipeline-deployment` action.

## Design choices

### LangGraph Orchestration

- **Modular Task Nodes**

  Each processing step is encapsulated in modular task nodes that handle specific functions such as text extraction, metadata processing, or data insertion.
  - This enables **parallelism**, allowing tasks without dependencies to execute simultaneously, improving overall efficiency.
  - It alsoEnhances **reusability**, allowing nodes to be reconfigured or extended for additional functionalities without disrupting the entire pipeline.

- **StateGraph Architecture**
  - The pipeline is implemented as a **LangGraph StateGraph**, where nodes (tasks) are organized in a **directed acyclic graph (DAG)** structure.
  - **Conditional Routing**: Used to manage workflows by skipping redundant tasks for already processed documents.

- **Shared State**

  All nodes in the pipeline access a **shared state**, a centralized store of information persisting throughout the pipeline's execution.

  This ensures seamless transfer of intermediate outputs (e.g., extracted text, metadata, keywords) between nodes

- **Fault Tolerance**

  Shared state enables the pipeline to recover from failures mid-execution without restarting from the beginning.
  For instance, if the keyword extraction node fails, the pipeline can implement a retrieval mechanism for only that task using existing data in the shared state.

### Error Handling

- Custom exception handling for each module.
- Logging supports both local development and Google Cloud environments.

### BigQuery Schema

This schema is optimized to support structured queries and analytics. It handles complex relationships (e.g., authors and keywords) using normalized tables and join structures for many-to-many associations.

#### Key Features

##### Normalized Design

The schema adheres to the principles of database normalization up to Third Normal Form (3NF):

- **1NF**: Ensures atomic fields.
- **2NF**: Attributes are fully dependent on primary keys.
- **3NF**: No transitive dependencies.

##### Join Tables

- Many-to-many relationships (e.g., authors to research papers, keywords to research papers) are efficiently modeled using join tables:
  - `authors_x_research_papers`
  - `keywords_x_research_papers`
- This approach reduces redundancy and ensures scalability.

##### Scalability and Integrity

- Normalizing the schema preserves **data integrity** and supports **large-scale datasets** with efficient querying.

##### Avoids Redundancy

- Data duplication is minimized through separate tables for:
  - **Authors**
  - **Keywords**
  - **Findings**
- Each table references related entities via foreign keys.

This schema design ensures:

- **Robustness**: Strong data structure for complex analytics.
- **Flexibility**: Easily extensible to accommodate additional entities or relationships.
- **Performance**: Optimized for advanced querying and analytics.

## Future improvements

- Add a retry mechanism when a task fails, ensuring transactionality in critical operations.
- Add an alert system to notify when processing fails or new papers are processed successfully.
- Improve LLM prompts for better accuracy in metadata and key insights extraction.
- Implement a validation step to detect and handle incomplete or poorly formatted PDFs.
- Explore the use of embeddings for enhanced keyword extraction.

## Usage

1. Upload a PDF to the configured **Google Cloud Storage (GCS)** bucket.
2. The pipeline automatically triggers, processes the file, and extracts structured information.
3. Extracted data is saved into the configured **BigQuery** dataset schema for querying and analysis.

## Contributing

Contributions are welcome! If you have an idea or improvement, feel free to open an issue or a pull request. I’d love to hear from you and collaborate!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
