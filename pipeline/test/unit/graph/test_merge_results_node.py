import pytest
from io import BytesIO
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import PipelineState, GraphError, MergeResults


class TestMergeResultsNode:
    @pytest.fixture
    def mock_pipeline_state(self) -> PipelineState:
        """
        Fixture to provide a mock PipelineState with appropriate state data.
        """
        return {
            "state": {
                "file": BytesIO(b"Mock PDF content"),
                "paper_id": "paper_id",
                "text": "Text",
                "metadata": {"title": "title", "authors": "authors", "abstract": "abstract", "publication_date": "publication_date"},
                "summary": {"summary": "summary", "keywords": "keywords"},
                "research": {"methodology": "methodology", "key_research_findings": "key_research_findings"}
            }
        }

    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        """
        Fixture to mock the logger for logging assertions.
        """
        with patch("src.graph.merge_results_node.logger") as mock_logger:
            yield mock_logger

    @pytest.fixture
    def merge_results(self) -> MergeResults:
        return MergeResults()

    def test_merge_results_node(
        self,
        mock_pipeline_state: PipelineState,
        mock_logger: MagicMock,
        merge_results: MergeResults
    ) -> None:
        """
        Test MergeResults node to verify the state output is correctly merged.
        """
        result = merge_results(mock_pipeline_state)

        expected_result = {
            "state": {
                "title": "title",
                "authors": "authors",
                "abstract": "abstract",
                "publication_date": "publication_date",
                "summary": "summary",
                "keywords": "keywords",
                "methodology": "methodology",
                "key_research_findings": "key_research_findings"
            }
        }

        mock_logger.info.assert_called_once_with("Merging results for paper ID paper_id")
        assert result == expected_result

    def test_merge_results_raises_graph_error(
        self,
        mock_pipeline_state: PipelineState,
        mock_logger: MagicMock,
        merge_results: MergeResults
    ) -> None:
        """Test MergeResults raises GraphError on exception."""
        mock_pipeline_state["state"] = None  # This will break the reduce call

        with pytest.raises(GraphError):
            merge_results(mock_pipeline_state)

        mock_logger.error.assert_called_once_with("Failed to merge results.")
