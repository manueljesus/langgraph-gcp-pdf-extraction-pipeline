import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import ExtractSummaryAndKeywords, PipelineState, GraphError


class TestExtractSummaryAndKeywordsNode:
    @pytest.fixture()
    def mock_extract_summary_and_keywords_task(self) -> Generator[MagicMock, None, None]:
        with patch(
                "src.graph.extract_summary_and_keywords_node.extract_summary_and_keywords",
                return_value={"summary": "summary", "keywords": ["keyword1", "keyword2"]}
        ) as mock:
            yield mock

    @pytest.fixture()
    def mock_pipeline_state(self) -> PipelineState:
        return {
            "state": {"text": "Mocked extracted text"}
        }

    @pytest.fixture()
    def mock_pipeline_state_with_error(self) -> PipelineState:
        return {
            "state": {}  # No "text" key to trigger an error
        }

    @pytest.fixture()
    def extract_summary_and_keywords(self) -> ExtractSummaryAndKeywords:
        return ExtractSummaryAndKeywords()

    def test_extract_summary_and_keywords(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_summary_and_keywords_task: MagicMock,
        extract_summary_and_keywords: ExtractSummaryAndKeywords
    ) -> None:
        """Test ExtractSummaryAndKeywords node to verify the state output."""
        result = extract_summary_and_keywords(mock_pipeline_state)

        mock_extract_summary_and_keywords_task.assert_called_once_with("Mocked extracted text")
        assert result == {
            "state": {
                "summary": {"summary": "summary", "keywords": ["keyword1", "keyword2"]}
            }
        }

    def test_extract_summary_and_keywords_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        extract_summary_and_keywords: ExtractSummaryAndKeywords
    ) -> None:
        """Test ExtractSummaryAndKeywords raises GraphError on exception."""
        with pytest.raises(GraphError):
            extract_summary_and_keywords(mock_pipeline_state_with_error)
