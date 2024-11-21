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
    """

    vertex_ai_llama_model: str = Field(..., json_schema_extra={'env': 'VERTEX_AI_LLAMA_MODEL'})

    @classmethod
    def load_env_file_if_present(cls):
        """
        Check for `.env` file and set it in the configuration if it exists.
        """
        if os.path.exists(".env"):
            cls.model_config = ConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    """
    Get the configuration settings for the pipeline.

    This function dynamically loads the `.env` file (if present) and
    caches the settings instance for reuse.
    """
    return Settings.load_env_file_if_present()
