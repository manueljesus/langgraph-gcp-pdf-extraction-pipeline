import pytest
from typing import Generator
from unittest.mock import MagicMock, patch
from src.tasks.extract_key_research_findings_and_methodology import extract_key_research_findings_and_methodology


class TestExtractMetadata:
    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """Fixture to patch the logger."""
        with patch("src.tasks.extract_key_research_findings_and_methodology.logger") as mock_logger:
            yield mock_logger

    @patch("src.tasks.extract_key_research_findings_and_methodology.vertex_ai_llama_request")
    def test_extract_key_research_findings_success(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.return_value = """{
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to ...",
            "key_research_findings": ["The proposed algorithm outperformed baseline models in accuracy."]
        }"""

        input_text = """Some content of the paper including methodology and key research findings."""

        expected_output = {
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to ...",
            "key_research_findings": ["The proposed algorithm outperformed baseline models in accuracy."]
        }

        assert extract_key_research_findings_and_methodology(input_text) == expected_output
        mock_logger.info.assert_called_once_with("Extracting key research findings and methodology")

    @patch("src.tasks.extract_key_research_findings_and_methodology.vertex_ai_llama_request")
    def test_extract_key_research_findings_partial_data(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.return_value = """{
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to ...",
            "key_research_findings": null
        }"""

        input_text = """LLM unable to find the key research findings of the paper."""

        expected_output = {
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to ...",
            "key_research_findings": None
        }

        assert extract_key_research_findings_and_methodology(input_text) == expected_output
        mock_logger.info.assert_called_once_with("Extracting key research findings and methodology")

    @patch("src.tasks.extract_key_research_findings_and_methodology.vertex_ai_llama_request")
    def test_extract_key_research_findings_error_handling(
        self,
        mock_llm_request: MagicMock,
        mock_logger: MagicMock
    ):
        mock_llm_request.side_effect = Exception("Mocked exception")

        input_text = """Error during extraction of metadata."""

        expected_output = {
            "methodology": None,
            "key_research_findings": None
        }

        assert extract_key_research_findings_and_methodology(input_text) == expected_output
        mock_logger.error.assert_called_once_with("Error extracting key research findings and methodology: Mocked exception")
