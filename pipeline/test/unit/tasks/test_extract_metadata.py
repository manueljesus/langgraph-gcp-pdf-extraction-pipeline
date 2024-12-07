import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
from src.tasks.extract_metadata import extract_metadata


class TestExtractMetadata:
    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to patch the logger."""
        with patch("src.tasks.extract_metadata.logger") as mock_logger:
            yield mock_logger

    @patch("src.tasks.extract_metadata.vertex_ai_llama_request")
    def test_extract_metadata_success(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.return_value = """{
            "title": "Advancements in Machine Learning",
            "authors": ["Alice Johnson", "Bob Smith"],
            "publication_date": "2022-08-30",
            "abstract": "This study explores recent advancements in machine learning techniques."
        }"""

        input_text = """Some content of the paper including title, authors, abstract, and date."""

        expected_output = {
            "title": "Advancements in Machine Learning",
            "authors": ["Alice Johnson", "Bob Smith"],
            "publication_date": "2022-08-30",
            "abstract": "This study explores recent advancements in machine learning techniques."
        }

        assert extract_metadata(input_text) == expected_output
        mock_logger.info.assert_called_once_with("Extracting metadata")

    @patch("src.tasks.extract_metadata.vertex_ai_llama_request")
    def test_extract_metadata_partial_data(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.return_value = """{
            "title": null,
            "authors": ["Alice Johnson"],
            "publication_date": "2022-08-30",
            "abstract": null
        }"""

        input_text = """LLM unable to find the title and abstract of the paper."""

        expected_output = {
            "title": None,
            "authors": ["Alice Johnson"],
            "publication_date": "2022-08-30",
            "abstract": None
        }

        assert extract_metadata(input_text) == expected_output
        mock_logger.info.assert_called_once_with("Extracting metadata")

    @patch("src.tasks.extract_metadata.vertex_ai_llama_request")
    def test_extract_metadata_error_handling(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.side_effect = Exception("Mocked exception")

        input_text = """Error during extraction of metadata."""

        expected_output = {
            "title": None,
            "authors": None,
            "publication_date": None,
            "abstract": None
        }

        assert extract_metadata(input_text) == expected_output
        mock_logger.error.assert_called_once_with("Error extracting metadata: Mocked exception")
