import pytest
from unittest.mock import MagicMock, patch
from src.graph import PipelineState, GraphError, MergeResults


class TestMergeResultsNode:
    @pytest.fixture
    def mock_pipeline_state(self) -> PipelineState:
        """
        Fixture to provide a mock PipelineState with appropriate state data.
        """
        return {
            "state": {
                "text": "Text",
                "metadata": {"title": "title", "authors": "authors", "abstract": "abstract", "publication_date": "publication_date"},
                "summary": {"summary": "summary", "keywords": "keywords"},
                "research": {"methodology": "methodology", "key_research_findings": "key_research_findings"}
            }
        }

    @pytest.fixture
    def merge_results(self) -> MergeResults:
        return MergeResults()

    def test_merge_results_node(
        self,
        mock_pipeline_state: PipelineState,
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

        assert result == expected_result

    def test_merge_results_raises_graph_error(
        self,
        mock_pipeline_state: PipelineState,
        merge_results: MergeResults
    ) -> None:
        """Test MergeResults raises GraphError on exception."""

        # Simulate an error by modifying the state to cause an exception
        mock_pipeline_state["state"] = None  # This will break the reduce call

        with pytest.raises(GraphError):
            merge_results(mock_pipeline_state)
