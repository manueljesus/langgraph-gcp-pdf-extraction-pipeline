import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
from src.tasks.extract_summary_and_keywords import extract_summary_and_keywords


class TestExtractMetadata:
    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to patch the logger."""
        with patch("src.tasks.extract_summary_and_keywords.logger") as mock_logger:
            yield mock_logger

    @patch("src.tasks.extract_summary_and_keywords.vertex_ai_llama_request")
    def test_extract_key_research_findings_success(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.return_value = """{
            "summary": "We conducted a series of experiments using a randomized controlled trial...",
            "keywords": ["algorithm", "experiments", "randomized controlled trial"]
        }"""

        input_text = """Some content of the paper."""

        expected_output = {
            "summary": "We conducted a series of experiments using a randomized controlled trial...",
            "keywords": ["algorithm", "experiments", "randomized controlled trial"]
        }

        assert extract_summary_and_keywords(input_text) == expected_output
        mock_logger.info.assert_called_once_with("Extracting summary and keywords")

    @patch("src.tasks.extract_summary_and_keywords.vertex_ai_llama_request")
    def test_extract_key_research_findings_partial_data(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.return_value = """{
            "summary": null,
            "keywords": ["algorithm", "experiments", "randomized controlled trial"]
        }"""

        input_text = """LLM unable to create a summary for the paper"""

        expected_output = {
            "summary": None,
            "keywords": ["algorithm", "experiments", "randomized controlled trial"]
        }

        assert extract_summary_and_keywords(input_text) == expected_output
        mock_logger.info.assert_called_once_with("Extracting summary and keywords")

    @patch("src.tasks.extract_summary_and_keywords.vertex_ai_llama_request")
    def test_extract_key_research_findings_error_handling(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.side_effect = Exception("Mocked exception")

        input_text = """Error during extraction of data."""

        expected_output = {
            "summary": None,
            "keywords": None
        }

        assert extract_summary_and_keywords(input_text) == expected_output
        mock_logger.error.assert_called_once_with("Error extracting summary and keywords: Mocked exception")
