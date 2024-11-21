import pytest
from unittest.mock import MagicMock, patch
from src.tasks.extract_summary_and_keywords import extract_summary_and_keywords


class TestExtractMetadata:
    @patch("src.tasks.extract_summary_and_keywords.vertex_ai_llama_request")
    def test_extract_key_research_findings_success(
        self,
        mock_llm_request: MagicMock
    ):
        mock_llm_request.return_value = """{
            "summary": "We conducted a series of experiments using a randomized controlled trial design to evaluate the effectiveness of the proposed algorithm.",
            "keywords": ["algorithm", "experiments", "randomized controlled trial"]
        }"""

        input_text = """Some content of the paper."""

        expected_output = {
            "summary": "We conducted a series of experiments using a randomized controlled trial design to evaluate the effectiveness of the proposed algorithm.",
            "keywords": ["algorithm", "experiments", "randomized controlled trial"]
        }

        assert extract_summary_and_keywords(input_text) == expected_output

    @patch("src.tasks.extract_summary_and_keywords.vertex_ai_llama_request")
    def test_extract_key_research_findings_partial_data(
        self,
        mock_llm_request: MagicMock
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

    @patch("src.tasks.extract_summary_and_keywords.vertex_ai_llama_request")
    def test_extract_key_research_findings_error_handling(
        self,
        mock_llm_request: MagicMock
    ):
        mock_llm_request.side_effect = Exception("Mocked exception")

        input_text = """Error during extraction of data."""

        expected_output = {
            "summary": None,
            "keywords": None
        }

        assert extract_summary_and_keywords(input_text) == expected_output
