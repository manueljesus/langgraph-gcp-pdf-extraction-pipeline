import pytest
from unittest.mock import MagicMock, patch
from src.tasks.extract_key_research_findings_and_methodology import extract_key_research_findings_and_methodology


class TestExtractMetadata:
    @patch("src.tasks.extract_key_research_findings_and_methodology.vertex_ai_llama_request")
    def test_extract_key_research_findings_success(
        self,
        mock_llm_request: MagicMock
    ):
        mock_llm_request.return_value = """{
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to evaluate the effectiveness of the proposed algorithm.",
            "key_research_findings": ["The proposed algorithm outperformed baseline models in accuracy and demonstrated robustness across multiple datasets."]
        }"""

        input_text = """Some content of the paper including methodology and key research findings."""

        expected_output = {
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to evaluate the effectiveness of the proposed algorithm.",
            "key_research_findings": ["The proposed algorithm outperformed baseline models in accuracy and demonstrated robustness across multiple datasets."]
        }

        assert extract_key_research_findings_and_methodology(input_text) == expected_output

    @patch("src.tasks.extract_key_research_findings_and_methodology.vertex_ai_llama_request")
    def test_extract_key_research_findings_partial_data(
        self,
        mock_llm_request: MagicMock
    ):
        mock_llm_request.return_value = """{
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to evaluate the effectiveness of the proposed algorithm.",
            "key_research_findings": null
        }"""

        input_text = """LLM unable to find the key research findings of the paper."""

        expected_output = {
            "methodology": "We conducted a series of experiments using a randomized controlled trial design to evaluate the effectiveness of the proposed algorithm.",
            "key_research_findings": None
        }

        assert extract_key_research_findings_and_methodology(input_text) == expected_output

    @patch("src.tasks.extract_key_research_findings_and_methodology.vertex_ai_llama_request")
    def test_extract_key_research_findings_error_handling(
        self,
        mock_llm_request: MagicMock
    ):
        mock_llm_request.side_effect = Exception("Mocked exception")

        input_text = """Error during extraction of metadata."""

        expected_output = {
            "methodology": None,
            "key_research_findings": None
        }

        assert extract_key_research_findings_and_methodology(input_text) == expected_output
