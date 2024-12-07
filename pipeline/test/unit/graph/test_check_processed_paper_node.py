import pytest
from typing import Generator
from unittest.mock import patch, MagicMock
from src.graph import CheckProcessedPaper, PipelineState, GraphError


class TestExtractSummaryAndKeywordsNode:
    @pytest.fixture()
    def mock_extract_summary_and_keywords_task(self) -> Generator[MagicMock, None, None]:
        with patch(
                "src.graph.check_processed_paper_node.check_processed_paper",
                return_value=True
        ) as mock:
            yield mock

    @pytest.fixture()
    def mock_pipeline_state(self) -> PipelineState:
        return {
            "state": {"paper_id": "paper_id"}
        }

    @pytest.fixture()
    def mock_pipeline_state_with_error(self) -> PipelineState:
        return {
            "state": {}  # No "paper_id" key to trigger an error
        }

    @pytest.fixture()
    def check_processed_paper(self) -> CheckProcessedPaper:
        return CheckProcessedPaper()

    @pytest.fixture()
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        with patch("src.graph.check_processed_paper_node.logger") as mock_logger:
            yield mock_logger

    def test_check_processed_paper_node(
        self,
        mock_pipeline_state: PipelineState,
        mock_extract_summary_and_keywords_task: MagicMock,
        check_processed_paper: CheckProcessedPaper,
        mock_logger: MagicMock
    ) -> None:
        """Test CheckProcessedPaper node to verify the state output."""
        result = check_processed_paper(mock_pipeline_state)

        mock_extract_summary_and_keywords_task.assert_called_once_with("paper_id")
        assert result
        mock_logger.info.assert_called_once_with("Checking if paper ID paper_id has been processed")

    def test_check_processed_paper_node_raises_graph_error(
        self,
        mock_pipeline_state_with_error: PipelineState,
        check_processed_paper: CheckProcessedPaper,
        mock_logger: MagicMock
    ) -> None:
        """Test CheckProcessedPaper raises GraphError on exception."""
        with pytest.raises(GraphError):
            check_processed_paper(mock_pipeline_state_with_error)
        mock_logger.error.assert_called_once()
