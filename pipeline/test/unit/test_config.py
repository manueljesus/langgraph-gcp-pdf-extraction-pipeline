import pytest
from pydantic import ValidationError
from src.config import Settings
from pydantic import ConfigDict

class TestSettings:
    """
    Test suite for the Settings class.
    """

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch: pytest.MonkeyPatch):
        """
        Reset the test environment
        """

        monkeypatch.delenv('VERTEX_AI_LLAMA_MODEL', raising=False)
        monkeypatch.delenv('BIGQUERY_DATASET_ID', raising=False)
        monkeypatch.delenv('GOOGLE_STORAGE_BUCKET_NAME', raising=False)

    @pytest.mark.parametrize(
        "env_vars, expected_values",
        [
            # Test all environment variables are set
            (
                {
                    'VERTEX_AI_LLAMA_MODEL': 'llama3.2-test',
                    'BIGQUERY_DATASET_ID': 'test_dataset',
                    'GOOGLE_STORAGE_BUCKET_NAME': 'test_bucket'
                },
                {
                    'vertex_ai_llama_model': 'llama3.2-test',
                    'bigquery_dataset_id': 'test_dataset',
                    'google_storage_bucket_name': 'test_bucket'
                }
            )
        ]
    )
    def test_settings_with_valid_env_vars(
        self,
        monkeypatch: pytest.MonkeyPatch,
        env_vars: dict,
        expected_values: dict
    ):
        """
        Test the Settings class with valid environment variables.

        Args:
            monkeypatch (MonkeyPatch): pytest's monkeypatch fixture for setting environment variables.
            env_vars (dict): Dictionary of environment variables to set.
            expected_values (dict): Expected values for Settings attributes.
        """
        # Set environment variables
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

        # Instantiate settings
        settings = Settings()

        # Assertions for each expected value
        assert settings.vertex_ai_llama_model == expected_values['vertex_ai_llama_model']

    @pytest.mark.parametrize(
        "missing_field, set_env_vars",
        [
            # Test missing vertex_ai_llama_model
            (
                'vertex_ai_llama_model',
                {'BIGQUERY_DATASET_ID': 'test_dataset', 'GOOGLE_STORAGE_BUCKET_NAME': 'test_bucket'},
            ),
            # Test missing bigquery_dataset_id
            (
                'bigquery_dataset_id',
                {'VERTEX_AI_LLAMA_MODEL': 'llama3.2-test', 'GOOGLE_STORAGE_BUCKET_NAME': 'test_bucket'}
            ),
            # Test missing google_storage_bucket_name
            (
                'google_storage_bucket_name',
                {'VERTEX_AI_LLAMA_MODEL': 'llama3.2-test', 'BIGQUERY_DATASET_ID': 'test_dataset'}
            ),
            # Test missing both vertex_ai_llama_model and bigquery_dataset_id
            (
                'ALL',
                {}
            )
        ]
    )
    def test_missing_required_env_vars(
        self,
        monkeypatch: pytest.MonkeyPatch,
        missing_field: str,
        set_env_vars: dict
    ):
        """
        Test the Settings class with missing required environment variables.

        Args:
            monkeypatch (MonkeyPatch): pytest's monkeypatch fixture for modifying environment variables.
            missing_field (str): The field name that is missing or "ALL" if all fields are missing.
            set_env_vars (dict): Dictionary of environment variables to set before the test.

        Asserts:
            - Instantiating Settings raises a ValidationError when a required field is missing.
        """
        # Set environment variables
        for key, value in set_env_vars.items():
            monkeypatch.setenv(key, value)

        # Expect a validation error due to the missing required field
        with pytest.raises(ValidationError) as exc_info:
            Settings()

        # Check the error message contains the missing field
        error_message = str(exc_info.value)

        if missing_field != 'ALL':
            assert missing_field in error_message, f"Error should mention missing field '{missing_field}'"
        else:
            assert any (
                field in error_message for field in ['vertex_ai_llama_model', 'bigquery_dataset_id']
            ), "Error should mention missing fields 'vertex_ai_llama_model' and 'bigquery_dataset_id'"
