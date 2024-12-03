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
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.extract_summary_and_keywords_node.logger") as mock_logger:
            yield mock_logger

    @pytest.fixture()
    def mock_pipeline_state(self) -> PipelineState:
        return {
            "state": {
                "text": "Mocked extracted text",
                "paper_id": "paper_id"
            }
        }

    @pytest.fixture()
    def mock_pipeline_state_with_error(self) -> PipelineState:
        return {
            "state": {
                "paper_id": "paper_id"  # Missing "text" key to trigger an error
            }
        }

    @pytest.fixture()
    def extract_summary_and_keywords(self) -> ExtractSummaryAndKeywords:
        return ExtractSummaryAndKeywords()

    def test_extract_summary_and_keywords(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_summary_and_keywords_task: MagicMock,
        mock_logger: MagicMock,
        extract_summary_and_keywords: ExtractSummaryAndKeywords
    ) -> None:
        """Test ExtractSummaryAndKeywords node to verify the state output."""
        result = extract_summary_and_keywords(mock_pipeline_state)

        mock_extract_summary_and_keywords_task.assert_called_once_with("Mocked extracted text")
        mock_logger.info.assert_called_once_with(
            "Extracting summary and keywords from paper ID paper_id"
        )
        assert result == {
            "state": {
                "summary": {"summary": "summary", "keywords": ["keyword1", "keyword2"]}
            }
        }

    def test_extract_summary_and_keywords_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        mock_logger: MagicMock,
        extract_summary_and_keywords: ExtractSummaryAndKeywords
    ) -> None:
        """Test ExtractSummaryAndKeywords raises GraphError on exception."""
        with pytest.raises(GraphError):
            extract_summary_and_keywords(mock_pipeline_state_with_error)
        mock_logger.error.assert_called_once_with(
            "Failed to extract summary and keywords from paper ID paper_id: 'text'"
        )
