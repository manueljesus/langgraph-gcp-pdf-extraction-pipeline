import os
from functools import lru_cache
from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuration settings for the pipeline.

    This class uses Pydantic's BaseSettings to manage environment variables and
    provides default values where applicable.
    It supports loading from an `.env` file if present in the working directory
    for local development purposes.

    Attributes:
        vertex_ai_llama_model (str): The Llama model name served on Vertex AI API service.
        bigquery_dataset_id (str): The BigQuery dataset ID for storing extracted data.
        google_storage_bucket_name (str): The Google Cloud Storage bucket name for storing extracted data.
    """

    vertex_ai_llama_model: str = Field(..., json_schema_extra={'env': 'VERTEX_AI_LLAMA_MODEL'})
    bigquery_dataset_id: str = Field(..., json_schema_extra={'env': 'BIGQUERY_DATASET_ID'})
    google_storage_bucket_name: str = Field(..., json_schema_extra={'env': 'GOOGLE_STORAGE_BUCKET_NAME'})
